#!/bin/sh
# Build order: paper (anonymous, keeps the .aux), supplement sources, supplement (anonymous and named), paper (named).
cd "$(dirname "$0")"
tectonic -X compile --only-cached --keep-intermediates --keep-logs --outdir build tog_review.tex > build/review.out 2>&1 || exit 1
python3 tools/build_supplement.py || exit 1
tectonic -X compile --only-cached --keep-logs --outdir build supplement_review.tex > build/supp.out 2>&1 || { grep "^error" build/supp.out; exit 1; }
tectonic -X compile --only-cached --keep-logs --outdir build supplement.tex > build/suppn.out 2>&1 || { grep "^error" build/suppn.out; exit 1; }
tectonic -X compile --only-cached --keep-logs --outdir build tog.tex > build/named.out 2>&1 || exit 1
echo built
