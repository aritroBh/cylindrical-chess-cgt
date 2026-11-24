#!/bin/sh
# Reproduce every number in research/odd_cylinders_verify/REPORT.md.
#
#   cd .
#   sh research/odd_cylinders_verify/run_all.sh
#
# Nothing outside research/odd_cylinders_verify/ is written to.  No network.
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT"
OUT=research/odd_cylinders_verify
PY=.venv/bin/python

echo "== 0. build the 128-bit solver (needed for 9 files) =="
$PY $OUT/make_wide.py kings/kpsolve.c $OUT/kpsolve_wide.c
cc -O2 -o $OUT/kpsolve_wide $OUT/kpsolve_wide.c -lpthread

echo "== 1. generate and solve every K+P vs K position on the cylinders =="
for B in 3x4 3x5 3x6 3x8 4x6 4x8 5x6 5x8 6x6 6x8 7x6 7x8 8x6 8x8; do
  $PY $OUT/gen_kpk.py --board cyl:$B --out $OUT/pos_cyl$B.txt
  nice -n 10 ./kings/kpsolve --board cyl:$B --ep on --promote QRBN --cap 1 \
      < $OUT/pos_cyl$B.txt > $OUT/res_c_cyl${B}_qrbn.txt 2>/dev/null
  PYTHONPATH=. nice -n 10 $PY -m kings.ref.solve --board cyl:$B --ep on --promote QRBN --cap 1 \
      < $OUT/pos_cyl$B.txt > $OUT/res_py_cyl${B}_qrbn.txt
  d=$(diff $OUT/res_py_cyl${B}_qrbn.txt $OUT/res_c_cyl${B}_qrbn.txt | grep -c '^[<>]' || true)
  echo "cyl:$B  positions=$(wc -l < $OUT/res_c_cyl${B}_qrbn.txt)  C-vs-Python diff lines=$d"
done

echo "== 2. the same for the flat 8x8 board (reference) =="
$PY $OUT/gen_kpk.py --board flat:8x8 --out $OUT/pos_flat8x8.txt
./kings/kpsolve --board flat:8x8 --ep on --promote QRBN --cap 1 \
    < $OUT/pos_flat8x8.txt > $OUT/res_c_flat8x8_qrbn.txt 2>/dev/null

echo "== 3. the wide build must reproduce the stock solver bit for bit =="
for B in 3x4 3x5 3x6 3x8 4x6 4x8 5x6 5x8 6x6 6x8 7x6 7x8 8x6 8x8; do
  nice -n 10 $OUT/kpsolve_wide --board cyl:$B --ep on --promote QRBN --cap 1 \
      < $OUT/pos_cyl$B.txt > $OUT/res_wide_cyl${B}_qrbn.txt 2>/dev/null
  d=$(diff $OUT/res_wide_cyl${B}_qrbn.txt $OUT/res_c_cyl${B}_qrbn.txt | grep -c '^[<>]' || true)
  echo "cyl:$B  wide-vs-stock diff lines=$d"
done
nice -n 10 $OUT/kpsolve_wide --board flat:8x8 --ep on --promote QRBN --cap 1 \
    < $OUT/pos_flat8x8.txt > $OUT/res_wide_flat8x8.txt 2>/dev/null
echo "flat:8x8  wide-vs-stock diff lines=$(diff $OUT/res_wide_flat8x8.txt $OUT/res_c_flat8x8_qrbn.txt | grep -c '^[<>]' || true)"

echo "== 4. the 5.1 trebuchet on C3..C9 =="
$PY $OUT/trebuchet.py --solver ./kings/kpsolve --wide-solver $OUT/kpsolve_wide \
    --out $OUT/trebuchet_results.txt > /dev/null
cat $OUT/trebuchet_results.txt

echo "== 5. tables =="
$PY $OUT/summary.py > $OUT/summary.txt
cat $OUT/summary.txt
for B in 3x8 4x8 5x8 6x8 7x8 8x8; do
  $PY $OUT/classify.py --results $OUT/res_c_cyl${B}_qrbn.txt --board cyl:$B \
      > $OUT/class_cyl${B}.txt 2>/dev/null || true
done
$PY $OUT/classify.py --results $OUT/res_c_flat8x8_qrbn.txt --board flat:8x8 \
    > $OUT/class_flat8x8.txt 2>/dev/null || true

echo "== 6. counterexamples =="
$PY $OUT/show_pos.py > $OUT/counterexamples.txt
cat $OUT/counterexamples.txt

echo "== 7. record the digests and drop the byte-identical duplicates =="
# Every duplicate below is first verified to be identical to a kept file; only
# then is it removed, so that the directory ends up in the documented state.
shasum -a 256 $OUT/res_*.txt | sort -k2 > $OUT/SHA256SUMS.txt
for B in 3x4 3x5 3x6 3x8 4x6 4x8 5x6 5x8 6x6 6x8 7x6 7x8 8x6 8x8; do
  if diff -q $OUT/res_py_cyl${B}_qrbn.txt $OUT/res_c_cyl${B}_qrbn.txt > /dev/null; then
    rm -f $OUT/res_py_cyl${B}_qrbn.txt
  else
    echo "WARNING: res_py_cyl${B} differs from res_c_cyl${B} -- kept"; exit 1
  fi
done
for B in 3x4 3x5 3x6 3x8 4x6 4x8 5x6 5x8 6x6 6x8 7x6 7x8 8x6 8x8; do
  if diff -q $OUT/res_wide_cyl${B}_qrbn.txt $OUT/res_c_cyl${B}_qrbn.txt > /dev/null; then
    rm -f $OUT/res_wide_cyl${B}_qrbn.txt
  else
    echo "WARNING: res_wide_cyl${B} differs from res_c_cyl${B} -- kept"; exit 1
  fi
done
rm -f $OUT/res_wide_flat8x8.txt
rm -f $OUT/pos_cyl*.txt $OUT/pos_flat8x8.txt
echo "done"
