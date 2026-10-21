"""Independent re-check of the 10 crosscheck disagreements (crosscheck/REPORT_after_fix.md):
HSS must be False for each (else Theorem 2.1 would be contradicted), o(W) must equal the exact class,
and o(S) must equal the CGT class reported there."""
import re, sys
sys.path.insert(0, "verify/lemmas/L2.1-HSS-theorem-reproduce")
from indep_l21 import B, o_S, o_W, analyse, FILES
def parse(t):
    w, b = t.split("/")
    sq = lambda s: (FILES.index(s[0]), int(s[1:]))
    return (frozenset(map(sq, w.split(":")[1].split())), frozenset(map(sq, b.split(":")[1].split())), None)
txt = open("crosscheck/REPORT_after_fix.md").read()
ok = 0
for bl in txt.split("### ")[1:]:
    m = re.search(r"board: (\w+), 8x8; e.p. rule: (\w+)", bl)
    t = re.search(r"Position: `([^`]*)`", bl).group(1)
    exact = re.search(r"Exact wins:.*class `(\w)`", bl).group(1)
    cg = re.search(r"CGT:.*outcome class `(\w)`", bl).group(1)
    bd = B(8, 8, m.group(1) == "cylinder", m.group(2) == "on"); p = parse(t)
    h, E, nt = analyse(bd, p)
    s, w = o_S(bd, p, "count"), o_W(bd, p, "count")
    good = (not h) and w == exact and s == cg
    ok += good
    print(f"{bd} {t}: HSS={h} E={E} o(W)={w} exact={exact} o(S)={s} reportedCGT={cg} {'OK' if good else 'MISMATCH'}")
print("ok", ok, "of 10")
