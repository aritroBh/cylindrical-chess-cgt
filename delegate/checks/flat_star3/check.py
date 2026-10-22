"""Check T42's single-component default-setting *3 on flat boards: cylcgt (sum, whole-board) and the Codex solver.
Usage: .venv/bin/python -I delegate/checks/flat_star3/check.py WIDTH "POSITION" MODE  (MODE = sum | nosplit | codex)"""
import sys, time
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames'); sys.setrecursionlimit(1000000)
w, pos, mode = int(sys.argv[1]), sys.argv[2], sys.argv[3]
t = time.time()
if mode in ("sum", "nosplit"):
    from cylcgt import pawns, cgt
    pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True
    B = pawns.Board(w, 8, False, True); P = pawns.Pos.parse(pos)
    ncomp = len(pawns.components(B, P))
    if mode == "nosplit": pawns.components = lambda b, p: [p]
    v = cgt.show(pawns.value(B, P)); extra = f"components={ncomp}"
else:
    sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/verify_ext/codex'); import solver as cx
    g = cx.PawnGame(w, "count", True, "aware"); wm, bm = cx.parse_position(pos.replace(":", ""), w); v = cx.show(g.value(wm, bm)); extra = ""
print(f"w{w}\t{pos}\t{mode}\t{v}\t{extra}\t{time.time()-t:.0f}s")
