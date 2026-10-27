# Produces tables.md from rows*_k.tsv, failscan.tsv, triple.tsv.
import csv, glob, io
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
    r['matched'] = int(r['matched']); r['n'] = int(r['n']); r['AvI'] = int(r['A_v']); r['BvI'] = int(r['B_v'])
    r['status'] = ('ILLEGAL' if r['ring_sig'] == 'ILLEGAL' else 'UNDECIDED' if r['ring_sig'] in ('ABORT', 'FULL') else
                   'nimber' if r['rv'] is not None else 'N+' if r['ring_sig'] == 'NNNNNNNN' else 'decisive/other')
out = io.StringIO()
def P(*a): print(*a, file=out)
def table(title, groups, cols=("rows", "undecided", "nimber", "nim=nim-sum", "nim!=nim-sum", "N+ (all-N)", "decisive/other", "% nimber of decided")):
    P(f"\n**{title}**\n"); P("| group | " + " | ".join(cols) + " |"); P("|" + "---|" * (len(cols) + 1))
    for name, sel in groups:
        sel = [r for r in sel if r['status'] != 'ILLEGAL']
        und = sum(r['status'] == 'UNDECIDED' for r in sel)
        nim = [r for r in sel if r['status'] == 'nimber']
        eq = sum(r['rv'] == r['ps'] for r in nim)
        npl = sum(r['status'] == 'N+' for r in sel); dec = sum(r['status'] == 'decisive/other' for r in sel)
        dd = len(sel) - und
        P(f"| {name} | {len(sel)} | {und} | {len(nim)} | {eq} | {len(nim) - eq} | {npl} | {dec} | {100 * len(nim) / max(1, dd):.1f} |")
M = [r for r in rows if r['matched']]
table("Matched walls, by kind (SS = small x small, BS = big x small, BB = big x big)",
      [(k, [r for r in M if r['kind'] == k]) for k in ('SS', 'BS', 'BB')] + [("all matched", M)])
same = lambda r: r['A_type'][0] == r['B_type'][0]
table("Matched walls, by relative handedness of the two cores (same = both cores start their wall with the same pawn)",
      [("same handedness", [r for r in M if same(r)]), ("opposite handedness", [r for r in M if not same(r)])])
table("Matched walls, by shorter wall length min(L1,L2)", [(f"min L = {m}", [r for r in M if min(r['L1'], r['L2']) == m]) for m in (2, 3, 4, 5, 6)])
table("Matched walls, by wall parities (e = even, o = odd)", [(f"L1 {a}, L2 {b}", [r for r in M if ('o' if r['L1'] % 2 else 'e') == a and ('o' if r['L2'] % 2 else 'e') == b]) for a in 'eo' for b in 'eo'])
vals = sorted(set((min(r['AvI'], r['BvI']), max(r['AvI'], r['BvI'])) for r in M))
table("Matched walls, by the stable values (vA, vB) of the two cores", [(f"*{a} + *{b}", [r for r in M if (min(r['AvI'], r['BvI']), max(r['AvI'], r['BvI'])) == (a, b)]) for a, b in vals])
U = [r for r in rows if r['kind'] == 'UN']
table("Unmatched wall types (kind UN, full 100-point wall grids for a few core pairs): prediction vA^vB",
      [("UN matched", [r for r in U if r['matched']]), ("UN unmatched", [r for r in U if not r['matched']])])
P("\n**Non-nimber signatures among matched, decided rings**\n")
c = Counter(r['ring_sig'] for r in M if r['status'] in ('decisive/other', 'N+'))
P(", ".join(f"`{s}` x{n}" for s, n in c.most_common()))
mm = [r for r in M if r['status'] == 'nimber' and r['rv'] != r['ps']]
P(f"\n**Matched rings that are nimbers but differ from vA xor vB: {len(mm)}**\n")
for r in mm[:20]: P("- ", r['ring'])
P("\n**Reference-ring version (single-core rings built by splicing the two walls, A+W1+W2 and B+W2+W1)**\n")
refn = [r for r in M if r['pr'] is not None and r['status'] in ('nimber', 'N+', 'decisive/other')]
okr = [r for r in refn if r['rv'] == r['pr']]
P(f"rows with both reference rings nimbers: {len(refn)}; ring is a nimber equal to refA xor refB: {len(okr)}; ring is a nimber different from it: "
  f"{sum(1 for r in refn if r['rv'] is not None and r['rv'] != r['pr'])}; ring not a nimber: {sum(1 for r in refn if r['rv'] is None)}")
# max value seen
P("\n**Largest ring value seen in the two-core experiment:** " + str(max([r['rv'] for r in rows if r['rv'] is not None] or [None])))
# failscan
try:
    fs = list(csv.DictReader(open("failscan.tsv"), delimiter="\t"))
    g = defaultdict(dict)
    for r in fs: g[(r['group_status'], r['A'], r['Atype'], r['B'], r['Btype'], r['f1'], r['f2'])][(int(r['L1']), int(r['L2']))] = r['val'].isdigit()
    P("\n**Length scan (wall lengths up to 11) of 30 pairs whose matched rings with L<=6 were all non-nimbers, and 10 pairs that were all nimbers**\n")
    cnt = Counter(); thr = []
    for k, v in g.items():
        st = set(v.values())
        cnt[(k[0], 'all nimber' if st == {True} else 'never nimber' if st == {False} else 'nimber only for some lengths')] += 1
        bad = [x for x in fs if (x['group_status'], x['A'], x['Atype'], x['B'], x['Btype'], x['f1'], x['f2']) == k and x['val'] == str(x['pred'])]
        mism = [x for x in fs if (x['group_status'], x['A'], x['Atype'], x['B'], x['Btype'], x['f1'], x['f2']) == k and x['val'].isdigit() and x['val'] != str(x['pred'])]
        if mism: P("MISMATCH", k)
        # threshold: smallest wall length L such that some ring with L1==L or L2==L is a nimber
        if k[0] == 'fail':
            nimL = [(a, b) for (a, b), s in v.items() if s]
            if nimL: thr.append((min(max(a, b) for a, b in nimL), min(min(a, b) for a, b in nimL)))
    for k, n in sorted(cnt.items()): P(f"- {k[0]} groups, {k[1]}: {n}")
    P(f"- value of every nimber ring in the length scan equals vA xor vB: {all(x['val'] == str(x['pred']) for x in fs if x['val'].isdigit())} ({sum(1 for x in fs if x['val'].isdigit())} nimber rings)")
    if thr: P(f"- for the failing groups, the smallest longer wall that restores a nimber has length (max of the two lengths of the first nimber ring) in {sorted(t[0] for t in thr)}")
except FileNotFoundError: pass
try:
    tr = list(csv.DictReader(open("triple.tsv"), delimiter="\t"))
    P("\n**Three- and four-core rings (matched walls)**\n")
    for k in ('3', '4'):
        for sm in ('1', '0'):
            sel = [r for r in tr if r['k'] == k and r['same_f'] == sm]
            nim = [r for r in sel if r['val'].isdigit()]
            P(f"- {k} cores, {'same' if sm == '1' else 'mixed'} handedness: rings {len(sel)}, nimbers {len(nim)}, equal to nim-sum {sum(1 for r in nim if r['val'] == r['pred'])}")
except FileNotFoundError: pass
open("tables.md", "w").write(out.getvalue())
print(out.getvalue())
