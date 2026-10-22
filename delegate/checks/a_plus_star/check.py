import sys, time
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames'); sys.setrecursionlimit(1000000)
mode = sys.argv[1]; pos = "W: a4 b3 d2 d3 f4 / B: a7 b7 c5 f6"
t = time.time()
if mode in ("sum", "nosplit"):
    from cylcgt import pawns, cgt
    pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True
    if mode == "nosplit": pawns.components = lambda b, p: [p]
    v = cgt.show(pawns.value(pawns.Board(6, 8, False, True), pawns.Pos.parse(pos)))
else:
    sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/verify_ext/codex'); import solver as cx
    g = cx.PawnGame(6, "count", True, "aware"); w, b = cx.parse_position(pos.replace(":", ""), 6); v = cx.show(g.value(w, b))
print(pos, mode, v, f"{time.time()-t:.0f}s")
