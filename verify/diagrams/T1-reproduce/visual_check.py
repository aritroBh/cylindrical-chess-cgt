"""T1 reproduce-lens check (verifier, 2026-10-16).

VIS = my own reading of each PNG (viewed directly with the image reader this session),
written as piece lists, not copied from the worker's FENs. Compared against:
  (a) cylcgt.verify_paper.CLAIMS (pawn sets),
  (b) the worker's MINE dict in verify/diagrams/rerun.py,
  (c) the FEN column of the Part A table in notes/diagram_audit.md.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/diagrams/T1-reproduce/visual_check.py
"""
import importlib.util, re
from cylcgt.verify_paper import CLAIMS
from cylcgt.pawns import Pos

VIS = {  # key: (white pieces, black pieces); uppercase letter prefix K = king, else pawn
    "2.1": ("e4", "e5"),
    "2.2": ("a2 h1", "a3 h4"),
    "2.3": ("c1 d2", "c4 d3"),
    "3.1": ("a3 h1", "a4 h5"),
    "3.2": ("a4 h1", "a5 h6"),
    "4.1": ("e4", "e6"),
    "4.2": ("e3", "e6"),
    "4.3": ("a4 h2 h4", "a5 a6 a7 h3"),
    "5.1": ("a4 Kh5", "a5 Kb4"),
    "7.1": ("a4 a5 c2 c3 f3 f4 h2 h3", "a7 c5 c6 f7 h6"),
    "7.2": ("a2 b2 h3 d7 Ke6", "a6 b7 h7 e7 Kd8"),
    "7.3": ("a1 a5 c1 c3 d3 f7 g1 h1 Kg8", "c2 d4 d5 d6 g3 g7 h4 Kf6"),
}


def sq(s):
    return ("abcdefgh".index(s[0]), int(s[1]))


def vis_sets(key):
    w, b = VIS[key]
    W = {t for t in w.split()}
    B = {t for t in b.split()}
    return ({sq(t) for t in W if not t.startswith("K")}, {sq(t) for t in B if not t.startswith("K")},
            {sq(t[1:]) for t in W if t.startswith("K")}, {sq(t[1:]) for t in B if t.startswith("K")})


def fen_sets(fen):
    out = {"P": set(), "p": set(), "K": set(), "k": set()}
    for i, row in enumerate(fen.split("/")):
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                out[ch].add((f, 8 - i)); f += 1
        assert f == 8
    return out["P"], out["p"], out["K"], out["k"]


name = lambda S: " ".join(sorted("abcdefgh"[f] + str(r) for f, r in S)) or "-"

spec = importlib.util.spec_from_file_location("rerun", "verify/diagrams/rerun.py")
rerun = importlib.util.module_from_spec(spec); spec.loader.exec_module(rerun)

print("== (b) my visual reading vs worker MINE (rerun.py), all pieces incl. kings ==")
for k in VIS:
    a, m = vis_sets(k), fen_sets(rerun.MINE[k])
    print(f"  {k}: {'SAME' if a == m else 'DIFF ' + str([name(x) for x in m])}")

print("== (c) Part A table FENs in notes/diagram_audit.md vs MINE ==")
txt = open("notes/diagram_audit.md").read()
for k in VIS:
    m = re.search(r"^\| " + re.escape(k) + r" \|[^\n]*?`([^`]+)`", txt, re.M)
    print(f"  {k}: PartA={m.group(1) if m else None}  {'SAME' if m and m.group(1) == rerun.MINE[k] else 'DIFF/MISSING'}")

print("== (a) my visual reading vs CLAIMS (pawn sets) ==")
covered = set()
for label, text, claim in CLAIMS:
    key = label.split()[0]; covered.add(key)
    cp = Pos.parse(text)
    W, B, KW, KB = vis_sets(key)
    files = {f for f, _ in cp.white | cp.black}
    Wf = {s for s in W if s[0] in files}; Bf = {s for s in B if s[0] in files}
    full = W == set(cp.white) and B == set(cp.black)
    onf = Wf == set(cp.white) and Bf == set(cp.black)
    extra = "" if full else (f" diagram-only W[{name(W - set(cp.white))}] B[{name(B - set(cp.black))}]"
                             f" claims-only W[{name(set(cp.white) - W)}] B[{name(set(cp.black) - B)}]")
    print(f"  {label:32s} full={full!s:5} on-own-files={onf!s:5} kings-in-diagram W[{name(KW)}] B[{name(KB)}]{extra}")
print("  diagrams with no CLAIMS entry:", sorted(set(VIS) - covered))
