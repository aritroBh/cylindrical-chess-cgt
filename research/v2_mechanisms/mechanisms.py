"""Mechanism analysis of the 34 7x6 'passed pawn does not win at once' failures (frozen-king game, exact).
Usage: python3 -I mechanisms.py   -> writes mechanisms_34.jsonl and prints the histogram."""
import json, sys, collections
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms")
import pawngame as pg
R = "/Users/aritro/Downloads/Research/Chessendgames/kings/results/"
rows = [json.loads(l) for l in open(R + "exp_cyl7x6_epon_Q_conv.jsonl")]
G = pg.Game(2, 6, True, 3)
OUT = "/Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms/"


def sel52(rows):
    return [r for r in rows if r["verdict_textbook"] == "MISMATCH" and not r["frozen_matches_convention"]]


def fzpred(r):
    return [r["frozen"]["wtm"][0], r["frozen"]["btm"][0]]


m52 = sel52(rows)
m34 = [r for r in m52 if r["predicted_ep-aware"] != fzpred(r)]
m18 = [r for r in m52 if r["predicted_ep-aware"] == fzpred(r)]
assert len(m52) == 52 and len(m34) == 34 and len(m18) == 18
assert all(r["predicted_ep-aware"] == r["predicted_textbook"] for r in m34)


def other(s): return "B" if s == "W" else "W"


def cg_children(pos, side, resp):
    """list of (label, child, cg_result_of_child_node or race-resolved)"""
    out = []
    for lab, p, promo in G.moves(pos, side):
        wp, bp = G.passed(p, "W", resp), G.passed(p, "B", resp)
        if wp and bp:
            oth = other(side)
            win = oth if G.promote_distance(p, oth, resp) <= G.promote_distance(p, side, resp) else side
            res, kind = ("W" if win == "W" else "L"), "race-count"
        else:
            res, kind = G._cg_node(p, other(side), resp), ("decisive" if (wp != bp) else "play")
        out.append((lab, p, res, kind))
    return out


def sdist(side, f, r):
    """unobstructed number of own moves to promote (double step from start rank)"""
    if side == "W":
        return G.H - r - (1 if r == 2 else 0)
    return r - 1 - (1 if r == G.H - 1 else 0)


def front(pos, side, s):
    W, B, _ = pos
    occ = W | B
    f, r = s
    rng = range(r + 1, G.H + 1) if side == "W" else range(1, r)
    return not any((f, t) in occ for t in rng)


def analyse(pos0, side0, resp=False):
    """follow the line X (convention winner) plays its CG-winning moves (fastest), Y plays FG-winning moves (fastest);
    stop at the first decisive node N*. Return diagnostics."""
    X = G.cg(pos0, side0, resp)  # convention winner 'W'/'L'
    Xs = "W" if X == "W" else "B"
    Y = "L" if X == "W" else "W"
    pos, side, path = pos0, side0, []
    while True:
        wp, bp = G.passed(pos, "W", resp), G.passed(pos, "B", resp)
        if wp != bp or (wp and bp and path):
            break
        if wp and bp:
            raise RuntimeError("race at root")
        mv = cg_children(pos, side, resp)
        if side == Xs:
            cand = [(lab, p, k) for lab, p, res, k in mv if res == X]
            # prefer the move that decides soonest: a decisive child first, then any
            cand.sort(key=lambda t: (t[2] == "play",))
            lab, p, k = cand[0]
        else:
            # Y plays an FG-winning move, shortest
            fm = G.fg_moves(pos, side)
            ys = sorted(((n, lab) for lab, (rs, n, pr) in fm.items() if rs == Y))
            lab = ys[0][1]
            p = [pp for l, pp, pr in G.moves(pos, side) if l == lab][0]
        path.append((side, lab))
        pos, side = p, other(side)
    return X, Xs, Y, path, pos, side


def fg_pv(pos, side):
    """principal variation of the frozen game: winner shortest, loser longest."""
    pv, res = [], None
    while True:
        r, n = G.fg(pos, side)
        mv = G.fg_moves(pos, side)
        if not mv:
            return pv, ("no-move", side, r)
        me = "W" if side == "W" else "L"
        if r == me:
            lab = min((nn, l) for l, (rs, nn, pr) in mv.items() if rs == me)[1]
        else:
            lab = max((nn, l) for l, (rs, nn, pr) in mv.items() if rs != me)[1]
        rs, nn, promo = mv[lab]
        pv.append((side, lab))
        if promo:
            return pv, ("promotion", side, r)
        pos = [p for l, p, pr in G.moves(pos, side) if l == lab][0]
        side = other(side)


def classify(pos, side, X, Xs, Y):
    """label the failure at the decisive node N* (pos, side to move)."""
    W, B, ep = pos
    wp = G.passed_set(pos, "W", False)
    bp = G.passed_set(pos, "B", False)
    xp = wp if Xs == "W" else bp
    Ys = other(Xs)
    ypawns = B if Xs == "W" else W
    xpawns = W if Xs == "W" else B
    pv, term = fg_pv(pos, side)
    info = {"Nstar": G.show(pos), "mover": side, "X_passers": [pg.nm((f + 3, r)) for f, r in xp],
            "X_passer_dist": {pg.nm((f + 3, r)): sdist(Xs, f, r) for f, r in xp},
            "X_passer_is_front": {pg.nm((f + 3, r)): front(pos, Xs, (f, r)) for f, r in xp},
            "Y_pawn_dist": {pg.nm((f + 3, r)): sdist(Ys, f, r) for f, r in ypawns},
            "pv": [f"{s}:{l}" for s, l in pv], "pv_end": term[0:2]}
    nX = min(info["X_passer_dist"].values())
    dY = min(info["Y_pawn_dist"].values())
    # square rule at N*: X certified iff n <= dY (X to move) / n < dY (Y to move)
    info["square_rule_certifies_X"] = (nX <= dY) if side == Xs else (nX < dY)
    # events in the pv
    caps = [(s, l) for s, l in pv if "x" in l]
    ycaps = [l for s, l in caps if s == Ys]
    xcaps = [l for s, l in caps if s == Xs]
    info["Y_captures"] = ycaps
    info["X_captures"] = xcaps
    if term[0] == "no-move":
        label = "NO_MOVE_LOSS"  # X (or someone) has no pawn move and king moves lose
    elif any(l.endswith("ep") for s, l in caps if s == Ys):
        label = "EP_CAPTURE"
    elif not any(info["X_passer_is_front"].values()):
        label = "PASSER_STUCK_BEHIND_OWN_PAWN"
    elif ycaps:
        label = "CAPTURE_THEN_RUN"
    else:
        label = None
    return info, label, pv, term



import tests as T
ZTOK = "Pa3 pa4 Kg4 kb3"


def kp_line(pos, side):
    W, B, ep = pos
    toks = [ZTOK] + ["P" + pg.nm((f + 3, r)) for f, r in sorted(W)] + ["p" + pg.nm((f + 3, r)) for f, r in sorted(B)]
    e = "-"
    if ep and ep[2] == side:
        e = pg.nm((ep[0][0] + 3, ep[0][1]))
    return " ".join(toks) + (" w " if side == "W" else " b ") + e


def trace_runner(pv, Ys):
    """the Y pawn that promotes: list of its squares along the PV"""
    ymoves = [(i, l) for i, (s, l) in enumerate(pv) if s == Ys]
    last = ymoves[-1][1]
    chain = [last]
    ptr = last.replace("x", "-").split("-")[0]
    for i, l in reversed(ymoves[:-1]):
        body = l.replace("x", "-").replace("ep", "")
        a, b = body.split("-")[0], body.split("-")[1]
        if b == chain[0].replace("x", "-").split("-")[0]:
            chain.insert(0, l)
    return chain


def features(pos, side, Xs, Ys, pv, term):
    W, B, ep = pos
    yp = B if Xs == "W" else W
    xp = W if Xs == "W" else B
    chain = trace_runner(pv, Ys)
    q0 = chain[0].replace("x", "-").replace("ep", "").split("-")[0]
    q0sq = pg.sq(q0)
    q0sq = (q0sq[0] - 3, q0sq[1])
    # blockers of q0: X pawns ahead on same/adjacent file
    f, r = q0sq
    files = {f} | {g for g in (G.nb(f, -1), G.nb(f, 1)) if g is not None}
    if Ys == "B":
        blockers = sorted(pg.nm((g + 3, s)) for g, s in xp if g in files and s < r)
    else:
        blockers = sorted(pg.nm((g + 3, s)) for g, s in xp if g in files and s > r)
    q_passed = q0sq in G.passed_set(pos, Ys, True)
    first_q_move = chain[0]
    first_is_capture = "x" in first_q_move
    # does q become passed right after its first move (everything else equal)?
    # (replay: move q only, ignore the rest)
    return dict(runner_start=q0, runner_chain=chain, runner_blocked_at_Nstar=(not q_passed), blockers=blockers,
                runner_first_move_is_capture=first_is_capture, runner_moves_in_pv=len(chain))


results, hist, hist2, arith = [], collections.Counter(), collections.Counter(), collections.Counter()
checks = collections.Counter()
kp_nodes = []
for r in m34:
    pos0 = G.parse(r["P"])
    sides = []
    for side, key, k in (("W", "wtm", 0), ("B", "btm", 1)):
        if r["predicted_textbook"][k] == r["frozen"][key][0]:
            continue
        X, Xs, Y, path, Npos, Nside = analyse(pos0, side, True)
        info, label, pv, term = classify(Npos, Nside, X, Xs, Y)
        Ys = other(Xs)
        ft = features(Npos, Nside, Xs, Ys, pv, term)
        info.update(ft)
        info.update({"mover_at_root": side, "convention_winner": X, "frozen_winner": Y,
                     "root_to_Nstar": [f"{s}:{l}" for s, l in path]})
        # path kind
        if not path:
            pk = "passer already on board at the root (Y to move)" if Nside == Ys else "passer already on board, X to move"
        else:
            first = path[0][1]
            pk = "X creates the passer by a capture" if "x" in first else "X creates the passer by a push"
            if path[0][0] != Xs:
                pk = "Y moves first, then X creates the passer"
        info["path_kind"] = pk
        # automatic mechanism label
        if term[0] == "no-move":
            lab = "NO_MOVE_LOSS"
        elif any(l.endswith("ep") for s_, l in pv):
            lab = "EP_CAPTURE"
        elif not any(info["X_passer_is_front"].values()):
            lab = "PASSER_STUCK_BEHIND_OWN_PAWN"
        elif info["runner_blocked_at_Nstar"] and not info["runner_first_move_is_capture"] and not info["Y_captures"]:
            lab = "STEP_PAST_RACE"       # Y's blocked pawn steps level with its blocker, becomes passed, wins the race
        elif info["runner_first_move_is_capture"] or info["Y_captures"]:
            lab = "CAPTURE_FREES_RUNNER"
        elif not info["runner_blocked_at_Nstar"]:
            lab = "UNCOUNTED_RACE (Y runner already passed)"
        else:
            lab = "OTHER"
        info["mechanism"] = lab
        # kpsolve confirmation of the frozen values along the whole line root -> N* -> end of PV
        poslist, p, sd = [], pos0, side
        nodes = [(pos0, side)]
        for s_, l in path:
            p = [pp for ll, pp, pr in G.moves(p, s_) if ll == l][0]
            nodes.append((p, other(s_)))
        p, sd = Npos, Nside
        for s_, l in pv:
            mv = [(ll, pp, pr) for ll, pp, pr in G.moves(p, s_) if ll == l][0]
            if mv[2]:
                break
            p = mv[1]
            nodes.append((p, other(s_)))
        for (pp, ss) in nodes:
            kp_nodes.append((kp_line(pp, ss), G.fg(pp, ss)[0]))
        sides.append(info)
        hist[lab] += 0
    results.append({"P": r["P"], "value": r["value"], "sides": sides, "real": r["real"], "frozen": r["frozen"],
                    "real_matches_frozen": r["real_matches_frozen"]})
# row-level primary mechanism: deterministic priority (first disputed side listed)
for x in results:
    labs = {s["mechanism"] for s in x["sides"]}
    x["row_mechanism"] = sorted(labs)[0] if len(labs) == 1 else "MIXED:" + "+".join(sorted(labs))
    hist[x["row_mechanism"]] += 1
    for s in x["sides"]:
        hist2[(s["mechanism"], s["path_kind"])] += 1
        arith[(s["mover"] == s["mover_at_root"] and "N* mover = root mover" or "N* mover differs", "n_X=%d" % min(s["X_passer_dist"].values()), "d_Y=%d" % min(s["Y_pawn_dist"].values()), "mover_at_N*=" + ("Y" if s["mover"] != s["convention_winner"][0:1] and ((s["mover"] == "W") != (s["convention_winner"] == "W")) else "X"))] += 1
# independent confirmation with kpsolve --frozen on every node of every line
uniq = {}
for line, res in kp_nodes:
    uniq[line] = res
import kp
kres, kerr = kp.run(list(uniq), "cyl:7x6", frozen=True, cap=1, moves=False, tag="mechanisms_lines")
bad = [l for l, res in uniq.items() if not (kres[l][0] == kres[l][1] == res)]
checks["nodes on the 34 lines (unique)"] = len(uniq)
checks["kpsolve --frozen disagreements with the scratch FG"] = len(bad)
# each N* is a false passer: convention says X wins, kpsolve frozen says Y
with open(OUT + "mechanisms_34.jsonl", "w") as fh:
    for x in results:
        fh.write(json.dumps(x) + "\n")
summary = {"row_mechanism_histogram": dict(hist), "n_rows": len(results), "disputed_sides": sum(len(x["sides"]) for x in results),
           "mechanism_by_path_kind": {f"{a} | {b}": v for (a, b), v in hist2.items()},
           "race_arithmetic": {" ".join(k_): v for k_, v in arith.items()}, "checks": dict(checks)}
json.dump(summary, open(OUT + "mechanism_histogram.json", "w"), indent=1)
print(json.dumps(summary, indent=1))
for x in results:
    for s in x["sides"]:
        print(x["P"], "|", s["mover_at_root"], "->", s["Nstar"], "to move", s["mover"], "|", s["path_kind"], "| runner", s["runner_chain"], "blocked by", s["blockers"], "| nX", min(s["X_passer_dist"].values()), "dY", min(s["Y_pawn_dist"].values()), "| real=frozen", x["real_matches_frozen"], "|", s["mechanism"])
