#!/bin/zsh
# C++ tempo profile (on lk.cpp) against the independent Python profile (lk_py) with the same N: histograms must be identical.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
N=4
while read kind W H pairs; do
  b=$kind:${W}x$H
  nice -n 15 $D/bin/tempo profile $b $pairs free $N | egrep "^  Lw" | sed -E 's/^  (Lw=[-0-9]+ Fw=[-0-9]+ Lb=[-0-9]+ Fb=[-0-9]+) +([0-9]+) .*/\1 \2/' | sort > /tmp/k31_c.txt
  nice -n 15 $PY $D/scripts/py_profile.py $kind $W $H $N $pairs | egrep "^  Lw" | sed -E 's/^  (Lw=[-0-9]+ Fw=[-0-9]+ Lb=[-0-9]+ Fb=[-0-9]+) +([0-9]+)$/\1 \2/' | sort > /tmp/k31_p.txt
  if diff -q /tmp/k31_c.txt /tmp/k31_p.txt > /dev/null; then echo "SAME   $b $pairs ($(wc -l < /tmp/k31_c.txt) profile classes, $(awk '{s+=$NF} END {print s}' /tmp/k31_c.txt) roots)"; else echo "DIFF   $b $pairs"; fi
done <<'LIST'
cyl 6 6 a2
cyl 6 6 a3
cyl 6 6 a4
cyl 8 6 a2
cyl 8 6 a3
cyl 5 6 a3
cyl 7 6 a2,c3
cyl 6 6 a2,d2
cyl 8 6 a2,d3
flat 6 6 a2,c4
flat 6 6 a3,c2
flat 7 6 b2,e3
LIST
