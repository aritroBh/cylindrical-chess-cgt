#!/bin/zsh
# diag.sh BOARD TESTOUT CTXFILE OUTDIR WCONF  -- re-run every FAIL line of TESTOUT under three diagnostic variants:
# m1 = a stalemate of White counts as a Black win; m2 = White's king may only step onto the files WCONF;
# m3 = both.
B=$1; T=$2; C=$3; O=$4; WC=$5
mkdir -p $O
for c in $(grep '^FAIL' $T | awk -F' [|] ' '{print $2}' | sort -u); do
  python3 - $T $C $c > $O/s_$c.txt <<'P'
import sys
T, C, c = sys.argv[1:4]
ctx = next(l.split()[1:] for l in open(C) if l.split()[0] == c)
for l in open(T):
    p = l.rstrip("\n").split(" | ")
    if p[0] != "FAIL" or p[1] != c: continue
    toks = p[5].split(); body = [t for t in toks[:-2] if t not in ctx]
    print(f"{p[2]} | {p[3]} | {' '.join(body + toks[-2:])} | {p[4]}")
P
  grep "^$c " $C > $O/c_$c.txt
  ./bin_k42b test --maxmb 1500 --board $B --sorties $O/s_$c.txt --contexts $O/c_$c.txt --wstalemate-loss > $O/m1_$c.txt 2>/dev/null
  ./bin_k42b test --maxmb 1500 --board $B --sorties $O/s_$c.txt --contexts $O/c_$c.txt --wconfine $WC > $O/m2_$c.txt 2>/dev/null
  ./bin_k42b test --maxmb 1500 --board $B --sorties $O/s_$c.txt --contexts $O/c_$c.txt --wstalemate-loss --wconfine $WC > $O/m3_$c.txt 2>/dev/null
done
