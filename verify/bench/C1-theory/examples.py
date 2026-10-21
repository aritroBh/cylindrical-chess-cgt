import sys
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/verify/bench/C1-theory")
from indep import *

def main():
    def V(text, files, ep, aware, race="count"):
        return Rules(files, ep, aware, race).value(parse(text))
    out = []
    def chk(label, g, ref):
        out.append(f"{label}: {eq(g, ref)}")
    for race in ("count", "mover", "opponent"):
        for ep in (True, False):
            tag = f"[{race}, ep {'on' if ep else 'off'}]"
            chk(f"C0312 W a2 c2 / B a3 b6 textbook == 1/2 {tag}", V("W: a2 c2 / B: a3 b6", 3, ep, False, race), HALF)
            chk(f"C0312 aware == up {tag}", V("W: a2 c2 / B: a3 b6", 3, ep, True, race), UP)
            chk(f"C0312 aware == 1/2 {tag}", V("W: a2 c2 / B: a3 b6", 3, ep, True, race), HALF)
            chk(f"C0311 W a2 c2 / B a3 b5 textbook == 1 {tag}", V("W: a2 c2 / B: a3 b5", 3, ep, False, race), ONE)
            chk(f"C0311 aware == * {tag}", V("W: a2 c2 / B: a3 b5", 3, ep, True, race), STAR)
            chk(f"C0413 W a6 b3 / B a7 c7 textbook == -1/2 {tag}", V("W: a6 b3 / B: a7 c7", 3, ep, False, race), neg(HALF))
            chk(f"C0413 aware == down {tag}", V("W: a6 b3 / B: a7 c7", 3, ep, True, race), DOWN)
            ref14 = G([STAR, ZERO], [G([STAR], [integer(-1)])])
            chk(f"C0314 W a2 c2 / B a4 b6 textbook == 1/2* {tag}", V("W: a2 c2 / B: a4 b6", 3, ep, False, race), add(HALF, STAR))
            chk(f"C0314 aware == {{*,0|{{*|-1}}}} {tag}", V("W: a2 c2 / B: a4 b6", 3, ep, True, race), ref14)
            kf_tb = V("W: a2 c2 / B: b7 d7", 4, ep, False, race)
            kf_aw = V("W: a2 c2 / B: b7 d7", 4, ep, True, race)
            two_pm_one = G([integer(3)], [ONE]); m = neg(two_pm_one)
            chk(f"KEYFACT textbook == *2 {tag}", kf_tb, nim(2))
            chk(f"KEYFACT textbook == 0 {tag}", kf_tb, ZERO)
            chk(f"KEYFACT aware == *2 {tag}", kf_aw, nim(2))
            chk(f"KEYFACT aware == 0 {tag}", kf_aw, ZERO)
            chk(f"KEYFACT aware == {{2+-1|-2+-1}} {tag}", kf_aw, G([two_pm_one], [m]))
    return out
for line in run(main):
    print(line)
