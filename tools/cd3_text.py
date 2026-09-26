"""Source-accounted CD3 RTF text parser configuration."""

import re

from tools.build_cd2_pilot import COSMETIC, parse

SKIP = re.compile(
    rb"\{\\up [+#$K!]\}\{\\footnote\\pard\\plain\{\\up [+#$K!]\}[^}]*\}"
    rb"|\{\\up [+#$K!]\}|\{\\v [^}]+\}"
)
COSMETIC_CD3 = COSMETIC | set("""
    f fi lang langfe deff ansi froman fnil fswiss fmodern fscript fdecor ftech
    fbidi deflang deflangfe viewkind stylesheet fonttbl colortbl info generator
    bupt rtldoc paperw paperh margl margr margt margb widctlpar nowidctlpar
    widowctrl hyphpar hyphcaps hyphauto hyphconsec
""".split())


def parse_cd3(raw, base):
    return parse(raw, base, skip=SKIP, cosmetic=COSMETIC_CD3)
