# Length scan on (A,B,f1,f2) groups whose matched rings were all non-nimbers: does failure persist at longer walls?
import sys, json, random
from collections import defaultdict
from lib import *
exec(open("analyze_two.py").read().split("def stats")[0])
random.seed(5)
m = [r for r in rows if r['matched'] and r['ring_sig'] not in ('ILLEGAL', 'ABORT', 'FULL') and r['kind'] in ('SS', 'BS', 'BB')]
pair = defaultdict(list)
for r in m: pair[(r['A_block'], r['A_type'], r['B_block'], r['B_type'], r['f1'], r['f2'])].append(r)
fail = [k for k, v in pair.items() if all(x['rv'] is None for x in v)]
ok = [k for k, v in pair.items() if all(x['rv'] is not None for x in v)]
cost = lambda k: len(k[0].split()) + len(k[2].split())
fail.sort(key=cost); ok.sort(key=cost)
sel = [("fail", k) for k in fail[:30]] + [("ok", k) for k in random.sample(ok[:120], 10)]
ev = Evaluator("results_failscan.tsv", tbits=23, nodelim=3000000, extra=("results.tsv", "results_blocks.tsv", "results_two_0.tsv", "results_two_1.tsv"))
out = open("failscan.tsv", "w")
out.write("group_status\tA\tAtype\tB\tBtype\tf1\tf2\tL1\tL2\tn\tsig\tval\tpred\n")
for status, k in sel:
    A, At, B, Bt, f1, f2 = k
    a, b = R(A), R(B)
    r0 = pair[k][0]
    p1, p2 = r0['L1'] % 2, r0['L2'] % 2
    vA, vB = int(r0['A_v']), int(r0['B_v'])
    for L1 in ([3, 5, 7, 9, 11] if p1 else [2, 4, 6, 8, 10]):
        for L2 in ([3, 5, 7, 9, 11] if p2 else [2, 4, 6, 8, 10]):
            ring = a + wall(L1, f1) + b + wall(L2, f2)
            if len(ring) > 24 or not legal_start(ring): continue
            sig = ev.sig(ring)
            out.write("\t".join(map(str, [status, A, At, B, Bt, f1, f2, L1, L2, len(ring), sig, nimber(sig), vA ^ vB])) + "\n"); out.flush()
print("done")
