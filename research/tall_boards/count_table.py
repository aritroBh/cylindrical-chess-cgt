#!/usr/bin/env python3
"""Count single-component roots per (board, R, pawns, split) with tw --count (nw<=nb; colour reversal identified when nw==nb).
usage: count_table.py out.tsv   (each call limited to 40 s; INCOMPLETE rows are lower bounds)"""
import subprocess, sys, os
T = os.path.dirname(os.path.abspath(__file__))
boards = [(3,1),(4,1),(5,1),(3,0),(4,0)]
rows = []
out = open(sys.argv[1], "a")
for (F, w) in boards:
    for R in range(5, 13):
        for p in range(F, 15):
            tot = 0; inc = False
            for nw in range(1, p // 2 + 1):
                nb = p - nw
                r = subprocess.run(["nice","-n","15",T+"/tw","--scan",str(F),str(w),str(R),str(nw),str(nb),"--count","--tlimit","20"],capture_output=True,text=True).stdout
                n = int(r.split("roots=")[1].split()[0]); tot += n; inc |= "INCOMPLETE" in r
            out.write(f"{F}\t{w}\t{R}\t{p}\t{tot}\t{int(inc)}\n"); out.flush()
            if inc or tot > 3e9: break
