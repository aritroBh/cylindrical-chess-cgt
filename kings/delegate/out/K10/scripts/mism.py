import sys
from e2e import *
bd = Board(8, 6, True, True); wk, bk = (0,1),(0,6)
D_ = D(bd, wk, bk)
def show(txt, stm):
    p = Pos.parse(txt)
    r = run_kp(bd, [line(bd, p, wk, bk, stm)])
    print(txt, stm, "D-winner:", D_.dwin(p, stm), "certW/B:", D_.cw_(p, stm, 'W'), D_.cw_(p, stm, 'B'), "allcert:", D_.allcert(p, stm), "kp:", r)
# smallest mismatches in 8x6, 2 pawns
cnt = 0
for w, b in enum_positions(bd, list(range(2,7)), 2, range(2,6)):
    pos = Pos(w, b)
    if passed(bd,pos,'W') or passed(bd,pos,'B') or not w or not b: continue
    for stm in 'WB':
        dw = D_.dwin(pos, stm)
        r = run_kp(bd, [line(bd, pos, wk, bk, stm)])
        key = list(r.values())[0]
        kpw = {'W':'W','L':'B','D':'D'}[key[0]]
        if kpw != dw and cnt < 8 and len(w)+len(b) <= 4:
            cnt += 1; print("MISMATCH", pos, stm, dw, key, "allcert", D_.allcert(pos, stm))
