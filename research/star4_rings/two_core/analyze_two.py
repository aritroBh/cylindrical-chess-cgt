import sys, glob
from collections import Counter, defaultdict
hdr = open("rows_header.txt").read().rstrip("\n").split("\t")
rows = []
for f in sorted(glob.glob("rows*_[0-9].tsv")):
    for line in open(f):
        p = line.rstrip("\n").split("\t")
        if len(p) == len(hdr): rows.append(dict(zip(hdr, p)))
def iv(x):
    try: return int(x)
    except: return None
for r in rows:
    r['rv'] = iv(r['ring_val']); r['pa'] = iv(r['refA_val']); r['pb'] = iv(r['refB_val'])
    r['ps'] = iv(r['pred_stable']); r['pr'] = iv(r['pred_ref']); r['L1'] = int(r['L1']); r['L2'] = int(r['L2'])
    r['matched'] = int(r['matched']); r['n'] = int(r['n'])
print("rows", len(rows), Counter(r['kind'] for r in rows))
def stats(sel, label):
    sel = list(sel)
    if not sel: print(f"{label}: none"); return
    legal = [r for r in sel if r['ring_sig'] != 'ILLEGAL' and r['ring_sig'] not in ('ABORT', 'FULL')]
    nim = [r for r in legal if r['rv'] is not None]
    ok_s = [r for r in nim if r['rv'] == r['ps']]
    refn = [r for r in legal if r['pr'] is not None]
    ok_r = [r for r in refn if r['rv'] == r['pr']]
    print(f"{label}: rows={len(sel)} legal={len(legal)} ring_is_nimber={len(nim)} ring==vA^vB(stable)={len(ok_s)} "
          f"({100*len(ok_s)/max(1,len(legal)):.1f}% of legal) | refs both nimbers={len(refn)} ring==refA^refB={len(ok_r)} "
          f"({100*len(ok_r)/max(1,len(refn)):.1f}% of those)")
for kind in ('SS', 'BS', 'BB'):
    stats([r for r in rows if r['kind'] == kind and r['matched']], f"{kind} matched")
stats([r for r in rows if r['kind'] != 'UN' and r['matched']], "ALL matched")
stats([r for r in rows if r['kind'] == 'UN' and r['matched']], "UN matched")
stats([r for r in rows if r['kind'] == 'UN' and not r['matched']], "UN unmatched")
stats([r for r in rows if r['kind'] == 'UN' and not r['matched'] and not int(r['defectA']) and not int(r['defectB'])], "UN unmatched, no splice defect")
