# Deploy the volunteer reading room to Cloudflare

Storage: [what to preserve and where new work belongs](STORAGE.md). Historical paths remain available through compatibility links.

This deploys the existing static export to the resources you prepared:

- R2 bucket: `maso-archive-reading-room-volunteer`
- Worker: `maso-archive-reading-room-volunteer`
- Address: `https://maso-archive-reading-room-volunteer.iolo.workers.dev`

The share URL will be `https://maso-archive-reading-room-volunteer.iolo.workers.dev/<random-token>/#/review`.
Anyone with that link can read the collection; there are no accounts or passwords.
The app remains static. The Worker checks the URL token and streams exported files
from R2, including JSON, images, text, and ZIP downloads. Review notes still live
in each volunteer's browser and are exported manually as JSON.

## One-time preparation

Use Python 3.10+ for deployment. Node.js is only needed to rebuild the frontend
or run the Worker tests. There is no Wrangler or AWS CLI dependency.

From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r tools/reading_room/requirements-deploy.txt
```

If `.venv` already exists, reuse it and run only the install command.

In the R2 bucket's **Settings**, leave the **Public Development URL** disabled
and do not attach a public custom domain. The Worker accesses the bucket through
its binding; enabling a separate public endpoint would bypass the share link.
No R2 CORS configuration is needed: every browser request uses the Worker origin.
The script does not change bucket public-access settings.

Prepare these credentials:

| Environment variable | Where to get it / permissions |
| --- | --- |
| `CLOUDFLARE_ACCOUNT_ID` | Your 32-character account ID from the Cloudflare dashboard. |
| `CLOUDFLARE_API_TOKEN` | An API token with **Account → Workers Scripts → Edit**, limited to the account containing this Worker. The API documentation calls this permission `Workers Scripts Write`. |
| `R2_ACCESS_KEY_ID` | The S3 Access Key ID from an R2 API token with **Object Read & Write**, restricted to `maso-archive-reading-room-volunteer`. |
| `R2_SECRET_ACCESS_KEY` | The matching S3 Secret Access Key, shown when the R2 token is created. |

These are two different credential sets. The account API token deploys the
Worker; the R2 S3 key pair uploads objects. Do not use your global account API
key. This script assumes the bucket is in R2's default jurisdiction, whose S3
endpoint is `<account-id>.r2.cloudflarestorage.com`.
See [R2 authentication](https://developers.cloudflare.com/r2/api/tokens/) and the
[Worker upload API](https://developers.cloudflare.com/api/resources/workers/subresources/scripts/methods/update/).

Keep credentials outside tracked files. For example, create a local file:

```sh
mkdir -p archive/operations/reading-room-deploy
chmod 700 archive/operations/reading-room-deploy
touch archive/operations/reading-room-deploy/credentials.env
chmod 600 archive/operations/reading-room-deploy/credentials.env
```

Edit that file in your editor, replacing these placeholders:

```sh
export CLOUDFLARE_ACCOUNT_ID='your-account-id'
export CLOUDFLARE_API_TOKEN='your-workers-api-token'
export R2_ACCESS_KEY_ID='your-r2-access-key-id'
export R2_SECRET_ACCESS_KEY='your-r2-secret-access-key'
```

Load it into the current terminal:

```sh
. archive/operations/reading-room-deploy/credentials.env
```

`archive/` is Git-ignored. Credentials are never sent to visitors,
embedded in the frontend, or stored as Worker bindings. Only the independently
generated **share token** is installed as a Worker secret. Do not paste API keys
into chat, commit them, or run the deployment with shell tracing (`set -x`).

## Validate and deploy

The prepared frontend is already built with relative URLs. When rebuilding it:

```sh
make build-volunteer-reading-room VOLUNTEER_BASE=./
```

Run the local dry run first. It needs neither credentials nor boto3:

```sh
python3 tools/reading_room/deploy_cloudflare.py
```

It validates every file against `data/manifest.json`, verifies that the entry
page uses relative asset URLs, and prints the size and file count. It makes no
network requests, uploads nothing, and creates no secret. The current release
has about **119,311 files / 15.36 GB**. Expect the full local hash pass to take
some time.

Then publish:

```sh
.venv/bin/python tools/reading_room/deploy_cloudflare.py --apply
```

This command:

1. Validates the export and authenticates against both services.
2. Uploads manifest-listed data and `assets/` under the bucket's `site/` prefix.
   Unlisted files elsewhere in the output directory are not uploaded.
3. Skips objects with matching SHA-256 metadata, size, content type, and cache
   policy. New uploads carry an MD5 integrity check and are checked afterward.
4. Uploads `data/manifest.json` and `index.html` after all other files succeed.
5. Replaces the named Worker's code and bindings with this static delivery
   Worker, its `ARCHIVE` R2 binding, and its `SHARE_TOKEN` secret. It disables
   Worker observability, enables the existing workers.dev endpoint, and disables
   preview URLs. It does not create a bucket, register a domain, or delete objects.
6. Checks the hosted entry page and catalog against local hashes, checks response
   headers, and verifies that an unlisted data URL returns 404.

The initial upload may take a while because the collection has many small files.
The default is eight upload threads; use `--jobs 4` for a slower connection.
Do not rebuild the export or run a second deployment while it is uploading.

The script intentionally owns this dedicated Worker's code and bindings. Any
existing placeholder implementation or unrelated bindings will be replaced.
The Worker source is [cloudflare-worker.mjs](../tools/reading_room/cloudflare-worker.mjs).

After a successful deployment, obtain the link:

```sh
.venv/bin/python tools/reading_room/deploy_cloudflare.py --show-link
```

This prints the real share URL. It is omitted from normal deployment logs.
The random token is stored with mode `0600` in
`archive/operations/reading-room-deploy/share-token` and is reused on later deployments.
Back up that file privately if you want to deploy from another machine.

The bare Worker address returning **404 is expected**. Open the complete share
link, including the token and the slash before `#/review`.

## Updates, recovery, and changing the link

For frontend changes, rebuild and run `--apply` again. For new archive data,
prepare and validate a new export first, then use `--output` if its location is
different:

```sh
.venv/bin/python tools/reading_room/deploy_cloudflare.py \
  --output dist/reading-room-volunteer-rebuild --apply
```

The upload is resumable: rerun the same command after an interruption. Files
already uploaded and verified are skipped. SDK retries handle transient R2
errors. Objects are updated **in place**, so an update is not an atomic release;
readers may see a mixture of old and new data during an upload. Run data updates
between volunteer review sessions. Upload failures stop before publishing the
new manifest, entry page, or Worker. There is no automatic rollback or deletion
of obsolete objects; files removed from a later export remain stored until you
remove them separately.

To update only the Worker code, or to rotate the secret link without uploading
the collection again:

```sh
# Worker update; retain the share URL.
.venv/bin/python tools/reading_room/deploy_cloudflare.py --apply --worker-only

# Replace the share URL; old links will stop working once the Worker is deployed.
.venv/bin/python tools/reading_room/deploy_cloudflare.py --apply --worker-only --rotate-link
.venv/bin/python tools/reading_room/deploy_cloudflare.py --show-link
```

`--worker-only` requires the local entry page and export manifest to match the
previously uploaded versions. Use a full deployment if they differ. Link changes
do not change the browser origin, so saved review notes remain available in the
same browser. Downloaded files and notes are not revoked.

If Worker publication is interrupted, `share-token.pending` preserves the token
that may have reached Cloudflare. The next deployment stops rather than silently
generating another link. Recover by adopting that token and redeploying:

```sh
# First preserve the previous token if the share-token file exists:
cp archive/operations/reading-room-deploy/share-token archive/operations/reading-room-deploy/share-token.previous
# If this was the first deployment, skip the cp command above.
mv archive/operations/reading-room-deploy/share-token.pending archive/operations/reading-room-deploy/share-token
.venv/bin/python tools/reading_room/deploy_cloudflare.py --apply --worker-only
```

The retry publishes the saved token consistently. If publication succeeded but
live verification failed, there may already be a working deployment; retry
`--apply --worker-only` after checking the Worker binding and credentials.

For 401/403 API errors, check the account ID and token scopes. A failed or
interrupted upload does not require clearing the bucket. No deployment can
complete until all files match the local manifest.

## Sharing behavior and cost

The Worker returns 404 for a missing or incorrect token, offers no directory
listing, accepts only GET/HEAD for files, and supports conditional and ranged
downloads. It sends `noindex`, `no-referrer`, and `private, no-store` headers.
There is no shared CDN cache that could continue serving files after link
rotation. Link recipients can still copy or forward the link. Robots directives
discourage indexing; they are not access controls.

Use **R2 Standard**, which includes 10 GB-month, one million Class A operations,
and ten million Class B operations per month. For this roughly 15.36 GB
collection, storage is approximately **US$0.09/month**, assuming the free tier
is otherwise unused. Each upload run checks remote metadata; new objects add
write and verification requests. Downloads have no R2 egress charge. Current
rates are in [R2 pricing](https://developers.cloudflare.com/r2/pricing/).

The Workers free plan allows 100,000 requests per day. Each asset/data fetch
counts, not just each visitor; exceeding the daily free limit can interrupt
access. This Worker usually makes one R2 HEAD and one GET per file request.
See [Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/).

## Local verification

```sh
python3 -m unittest discover -s tests -p test_reading_room_deploy.py
node tools/reading_room/cloudflare-worker.test.mjs
python3 tools/reading_room/deploy_cloudflare.py
```

Tests exercise resumable uploads, failed-upload ordering, credential handling,
path restrictions, MIME types, Unicode paths, conditional requests, ranges,
token checks, and storage failures. They use local fakes; they do not deploy or
require an account. Live verification runs automatically after `--apply`.

Implementation references:
[R2 with boto3](https://developers.cloudflare.com/r2/examples/aws/boto3/),
[Worker multipart upload metadata](https://developers.cloudflare.com/workers/configuration/multipart-upload-metadata/),
[R2 Worker API](https://developers.cloudflare.com/r2/api/workers/workers-api-reference/).
