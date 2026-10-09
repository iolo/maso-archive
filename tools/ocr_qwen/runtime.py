"""Owned llama-server lifecycle and sampled local resource accounting."""
from contextlib import AbstractContextManager
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import threading
import time
from urllib.error import URLError
from urllib.request import Request, urlopen

import psutil

from tools.pdf_restore.inventory import digest, write_json


def request(url, payload=None, timeout=600):
    data = None if payload is None else json.dumps(payload).encode()
    req = Request(url, data=data, headers={'Content-Type': 'application/json'})
    with urlopen(req, timeout=timeout) as response:
        return json.load(response)


class Monitor(AbstractContextManager):
    """Sample a PID and its descendants; GPU values are PID-specific when supported."""
    def __init__(self, pid=None):
        self.pid = pid or os.getpid()
        self.stop = threading.Event()
        self.cpu = {}
        self.rss = 0
        self.gpu = None
        self.samples = 0
        self.gpu_samples = 0
        self.smi = shutil.which('nvidia-smi')

    def sample(self):
        try:
            process = psutil.Process(self.pid)
            processes = [process, *process.children(recursive=True)]
        except psutil.Error:
            return
        rss, pids = 0, set()
        for proc in processes:
            try:
                pids.add(proc.pid)
                rss += proc.memory_info().rss
                cpu = proc.cpu_times()
                self.cpu[(proc.pid, proc.create_time())] = cpu.user + cpu.system
            except psutil.Error:
                pass
        self.rss = max(self.rss, rss)
        self.samples += 1
        if self.smi:
            try:
                result = subprocess.run([self.smi, '--query-compute-apps=pid,used_gpu_memory',
                                         '--format=csv,noheader,nounits'], capture_output=True,
                                        text=True, timeout=3, check=True)
                values = [int(parts[1]) for line in result.stdout.splitlines()
                          if len(parts := line.split(',')) == 2 and parts[0].strip().isdigit()
                          and int(parts[0]) in pids and parts[1].strip().isdigit()]
                if values:
                    self.gpu = max(self.gpu or 0, sum(values))
                    self.gpu_samples += 1
            except (OSError, ValueError, subprocess.SubprocessError):
                pass

    def __enter__(self):
        self.started = time.monotonic()
        self.sample()
        self.initial_cpu = dict(self.cpu)
        def loop():
            while not self.stop.wait(.1):
                self.sample()
        self.thread = threading.Thread(target=loop, daemon=True)
        self.thread.start()
        return self

    def __exit__(self, *exc):
        self.stop.set()
        self.thread.join()
        self.sample()
        self.metrics = dict(wall_seconds=time.monotonic() - self.started,
                            cpu_seconds_sampled=sum(max(0, v-self.initial_cpu.get(k, 0))
                                                    for k, v in self.cpu.items()),
                            peak_rss_mib_sampled=self.rss / 2**20,
                            peak_gpu_mib_sampled=self.gpu, samples=self.samples,
                            gpu_samples=self.gpu_samples,
                            resource_scope='PID plus descendants; 100ms target interval plus nvidia-smi overhead; RSS includes shared mappings; short-lived CPU/RSS peaks may be missed; GPU null means unavailable/no matching allocation')


def cached_models():
    base = Path.home() / '.cache/huggingface/hub/models--unsloth--Qwen3-VL-8B-Instruct-GGUF/snapshots'
    candidates = sorted(base.glob('*/Qwen3-VL-8B-Instruct-UD-Q4_K_XL.gguf'))
    if len(candidates) != 1:
        raise ValueError('Specify --model and --mmproj (cache must contain exactly one matching snapshot)')
    return candidates[0], candidates[0].parent / 'mmproj-BF16.gguf'


class Server(AbstractContextManager):
    def __init__(self, output, binary=None, model=None, mmproj=None, context=8192,
                 gpu_layers=99, image_tokens=4096, startup_timeout=180):
        self.output = Path(output)
        self.binary = Path(binary or Path.home() / 'workspace/ai/llama.cpp/build/bin/llama-server').expanduser()
        if model is None and mmproj is None:
            model, mmproj = cached_models()
        if model is None or mmproj is None:
            raise ValueError('--model and --mmproj must be supplied together')
        self.model, self.mmproj = Path(model).expanduser(), Path(mmproj).expanduser()
        self.context, self.gpu_layers, self.image_tokens = context, gpu_layers, image_tokens
        self.startup_timeout = startup_timeout
        self.process = None

    def __enter__(self):
        self.output.mkdir(parents=True, exist_ok=True)
        files = [dict(path=str(p), sha256=digest(p), bytes=p.stat().st_size)
                 for p in (self.binary, self.model, self.mmproj)]
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        self.url = f'http://127.0.0.1:{port}'
        args = [str(self.binary), '-m', str(self.model), '--mmproj', str(self.mmproj),
                '--host', '127.0.0.1', '--port', str(port), '--parallel', '1',
                '--n-gpu-layers', str(self.gpu_layers), '--ctx-size', str(self.context),
                '--image-max-tokens', str(self.image_tokens), '--jinja', '--flash-attn', 'on',
                '--top-p', '0.8', '--top-k', '20', '--temp', '0.7', '--min-p', '0.0',
                '--presence-penalty', '1.5', '--offline']
        self.log = (self.output / 'server.log').open('wb')
        started = time.monotonic()
        try:
            self.process = subprocess.Popen(args, stdout=self.log, stderr=subprocess.STDOUT)
            with Monitor(self.process.pid) as monitor:
                while time.monotonic() - started < self.startup_timeout:
                    if self.process.poll() is not None:
                        raise RuntimeError(f'llama-server exited; see {self.output / "server.log"}')
                    try:
                        if request(self.url + '/health', timeout=1).get('status') == 'ok':
                            break
                    except (URLError, TimeoutError, OSError):
                        pass
                    time.sleep(.2)
                else:
                    raise TimeoutError('llama-server did not become healthy')
            self.metadata = dict(files=files, command=args, startup=monitor.metrics,
                                 version=subprocess.check_output([str(self.binary), '--version'],
                                                                 stderr=subprocess.STDOUT, text=True).strip())
            write_json(self.output / 'runtime.json', self.metadata)
            return self
        except BaseException:
            self.__exit__()
            raise

    def __exit__(self, *exc):
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
        if hasattr(self, 'log'):
            self.log.close()
