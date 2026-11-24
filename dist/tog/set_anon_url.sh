#!/bin/sh
# Set the anonymous code link in both anonymous builds, rebuild, and check it.
# Usage: sh dist/tog/set_anon_url.sh [--dry-run] https://anonymous.4open.science/r/<id>
#   --dry-run: work on temporary copies of tog.tex and supplement.tex, show the change, build nothing.
DRY=0
if [ "$1" = "--dry-run" ]; then DRY=1; shift; fi
URL=$1
HERE=$(cd "$(dirname "$0")" && pwd)
if [ -z "$URL" ] || ! printf '%s\n' "$URL" | grep -Eq '^https://anonymous\.4open\.science/r/[A-Za-z0-9._-]+/?$'; then
  echo "REFUSED: URL must match ^https://anonymous\\.4open\\.science/r/[A-Za-z0-9._-]+/?\$ (got: '$URL')"; exit 2
fi
if [ "$DRY" = 1 ]; then
  W=$(mktemp -d); cp "$HERE/tog.tex" "$HERE/supplement.tex" "$W/"; D=$W
else
  D=$HERE
fi
URL="$URL" D="$D" DRYRUN="$DRY" python3 - <<'PY' || { echo "FAIL: could not edit the macro (need exactly one occurrence per file)"; exit 1; }
import os, re, shutil, sys
url, d = os.environ['URL'], os.environ['D']
rx = re.compile(r'\\newcommand\{\\anoncodeurl\}\{(?:[^{}]|\{[^{}]*\})*\}')
for f in ('tog.tex', 'supplement.tex'):
    p = os.path.join(d, f); s = open(p, encoding='utf-8').read()
    if len(rx.findall(s)) != 1:
        print('%s: found %d occurrences of \\anoncodeurl, need 1' % (f, len(rx.findall(s)))); sys.exit(1)
    new = '\\newcommand{\\anoncodeurl}{\\url{%s}}' % url
    if os.environ.get('DRYRUN') != '1':
        shutil.copyfile(p, p + '.bak')
    open(p, 'w', encoding='utf-8').write(rx.sub(lambda m: new, s))
    print('%s: %s' % (f, new))
PY
if [ "$DRY" = 1 ]; then
  echo "DRY RUN: edited temporary copies in $D (originals untouched, nothing built)"; rm -rf "$D"; exit 0
fi
sh "$HERE/rebuild.sh" || { echo "FAIL: rebuild.sh did not finish (the .bak files keep the old tog.tex and supplement.tex)"; exit 1; }
cd "$HERE" || exit 1
ok=1
for f in tog_review supplement_review; do
  n=$(pdftotext build/$f.pdf - | tr -d '\n ' | grep -cF "$(printf '%s' "$URL" | tr -d ' ')")
  echo "$f: URL found: $n match(es)"; [ "$n" -ge 1 ] || ok=0
done
n=$(pdftotext build/tog.pdf - | tr -d '\n ' | grep -cF "anonymous.4open.science")
echo "tog (named): anonymous URL found: $n match(es) (must be 0)"; [ "$n" -eq 0 ] || ok=0
if [ $ok = 1 ]; then echo "PASS"; else echo "FAIL"; exit 1; fi
