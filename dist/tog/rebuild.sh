#!/bin/sh
# Rebuild the ToG paper + supplement, run checks, copy the PDFs, refresh the submission hashes.
# Usage: sh dist/tog/rebuild.sh   (from anywhere; the repository root is found from this script's location)
set -e
R=$(cd "$(dirname "$0")/../.." && pwd); cd "$R/dist/tog"
nice -n 15 sh sbuild.sh > build/sbuild.stdout 2>&1; tail -1 build/sbuild.stdout
for f in tog tog_review supplement supplement_review; do echo "$f $(pdfinfo build/$f.pdf | awk '/Pages/{print $2}')"; done
sh freespace.sh build/tog.pdf | tail -1; python3 check_numbers.py | tail -1
for f in tog_review supplement_review; do echo "$f anon hits: $(pdftotext build/$f.pdf - | grep -ciE 'aritro|bhattacharjee|uiuc|illinois|morley|gatech|georgia')"; done
echo "overfull/undef-ref: $(grep -c 'Overfull\|Reference.*undefined\|Undefined control' build/tog.log) $(grep -c 'Overfull\|Reference.*undefined\|Undefined control' build/supplement.log)"
[ "$(pdfinfo build/tog.pdf | awk '/Pages/{print $2}')" = 10 ] && [ "$(pdfinfo build/tog_review.pdf | awk '/Pages/{print $2}')" = 10 ] || { echo "PAGE COUNT WRONG, not copying"; exit 1; }
cp build/tog.pdf build/tog_review.pdf build/supplement.pdf build/supplement_review.pdf .
cp tog.pdf ../../paper/Bhattacharjee_Cylinder_Chess_ToG_10pages.pdf; cp tog_review.pdf ../../paper/Bhattacharjee_Cylinder_Chess_ToG_10pages_anonymous.pdf; cp supplement_review.pdf ../../paper/Bhattacharjee_Cylinder_Chess_ToG_supplement_anonymous.pdf
cd "$R"; python3 - <<'PY'
import re,hashlib,os,subprocess
p='dist/tog/submission/files_to_upload.md'; s=open(p).read(); n=[0]
def row(m):
    f=m.group(1); b=os.path.getsize(f); pg=re.search(r'Pages:\s+(\d+)',subprocess.check_output(['pdfinfo',f]).decode()).group(1)
    n[0]+=1; return f"`{f}` | {b} | {pg} | `{hashlib.sha256(open(f,'rb').read()).hexdigest()}`"
open(p,'w').write(re.sub(r'`(dist/tog/[^`]+\.pdf)` \| \d+ \| \d+ \| `[0-9a-f]{64}`', row, s))
q='dist/tog/submission/pdf_checks.md'; t=open(q).read()
sz=[os.path.getsize('dist/tog/'+f+'.pdf') for f in ('tog','tog_review','supplement','supplement_review')]
t2=re.sub(r'\| File size \(bytes\) \|[^\n]*', '| File size (bytes) | %d | %d | %d | %d |'%tuple(sz), t); assert t2.count('File size (bytes)')==1
open(q,'w').write(t2); print('submission rows refreshed', n[0], sz)
PY
