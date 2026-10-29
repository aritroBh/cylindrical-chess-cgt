"""Corrected convention CC: cylcgt's pawn game where a passed pawn ends the game only if it is CERTIFIED
(S = square rule, or RP = run-the-passer search); otherwise play continues.  Boolean minimax, ep-aware passed test.
Also: exhaustive soundness check of S and RP over all small placements, and the re-score of the 7x6/6x6/5x6 sweeps.
Usage: python3 -I cc.py"""
import json, sys, itertools, collections
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms")
import pawngame as pg, tests as T
R = "/Users/aritro/Downloads/Research/Chessendgames/kings/results/"
OUT = "/Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms/"
cfg = {"cyl7x6": ("exp_cyl7x6_epon_Q_conv.jsonl", 2, 3, 6), "cyl6x6": ("exp_cyl6x6_epon_Q_conv.jsonl", 1, 3, 6),
       "flat5x6": ("exp_flat5x6_epon_Q_conv.jsonl", 1, 0, 6)}
PRED = {("W", "W"): "L", ("L", "L"): "R", ("W", "L"): "N", ("L", "W"): "P"}   # (white-to-move result, black-to-move result)


class CC:
    def __init__(self, G, cert):
        self.G, self.cert, self.memo = G, cert, {}
        self.expanded_passed = 0   # nodes where some side has a passed pawn but no certificate -> play on
        self.nodes = 0

    def node(self, pos, side):
        key = (pos, side)
        r = self.memo.get(key)
        if r is not None:
            return r
        G = self.G
        cw = self.cert(G, pos, side, "W", True)
        cb = self.cert(G, pos, side, "B", True)
        assert not (cw and cb), ("two certified winners", G.show(pos), side)
        self.nodes += 1
        if cw:
            r = "W"
        elif cb:
            r = "L"
        else:
            if G.passed(pos, "W", True) or G.passed(pos, "B", True):
                self.expanded_passed += 1
            me = "W" if side == "W" else "L"
            r = "L" if side == "W" else "W"
            for lab, p, promo in G.moves(pos, side):
                if self.node(p, T.other(side)) == me:
                    r = me
                    break
        self.memo[key] = r
        return r


def exhaustive_soundness(k, H, maxw, maxb):
    """every placement (pawns on ranks 2..H-1, no shared square, <= maxw white, <= maxb black), both sides to move,
    plus every single e.p. right that can legally exist: S/RP certificates (ep-aware) must never contradict FG"""
    G = pg.Game(k, H, True, 0)
    sqs = [(f, r) for f in range(k) for r in range(2, H)]
    res = collections.Counter()
    for nw in range(0, maxw + 1):
        for ws in itertools.combinations(sqs, nw):
            rest = [s for s in sqs if s not in ws]
            for nb in range(0, maxb + 1):
                for bs in itertools.combinations(rest, nb):
                    W, B = frozenset(ws), frozenset(bs)
                    eps = [None]
                    if G.ep_on:
                        for (f, r) in W:
                            if r == 4 and (f, 3) not in W | B:   # white pawn just made f2-f4
                                eps.append(((f, 3), (f, 4), "B"))
                        for (f, r) in B:
                            if r == H - 3 and (f, H - 2) not in W | B:
                                eps.append(((f, H - 2), (f, H - 3), "W"))
                    for ep in eps:
                        pos = (W, B, ep)
                        for side in "WB":
                            truth = G.fg(pos, side)[0]
                            res["positions"] += 1
                            for X in "WB":
                                xw = "W" if X == "W" else "L"
                                s_ = T.S_cert(G, pos, side, X, True)
                                rp = T.RP_cert(G, pos, side, X, True)
                                if s_:
                                    res["S_certified"] += 1
                                    if truth != xw: res["S_UNSOUND"] += 1
                                if rp:
                                    res["RP_certified"] += 1
                                    if truth != xw: res["RP_UNSOUND"] += 1
                                if s_ and not rp: res["S_not_in_RP"] += 1
    return dict(res)


if __name__ == "__main__":
    out = {}
    # 1. exhaustive soundness
    sound = {}
    for k, H, mw, mb in ((2, 6, 3, 3), (3, 6, 2, 2), (2, 8, 3, 3), (1, 8, 3, 3)):
        sound[f"{k}files_{H}ranks_le{mw}v{mb}"] = exhaustive_soundness(k, H, mw, mb)
        print(k, H, sound[f"{k}files_{H}ranks_le{mw}v{mb}"], flush=True)
    out["exhaustive_soundness"] = sound
    # 2. re-score
    rescore = {}
    detail = {}
    for name, (fn, k, off, H) in cfg.items():
        rows = [json.loads(l) for l in open(R + fn)]
        G = pg.Game(k, H, True, off)
        ccs = {"S": CC(G, T.S_cert), "RP": CC(G, T.RP_cert)}
        tally = collections.Counter()
        for r in rows:
            pos = G.parse(r["P"])
            res = {}
            for nm_, c in ccs.items():
                res[nm_] = (c.node(pos, "W"), c.node(pos, "B"))
            assert res["S"] == res["RP"], r["P"]
            fz = (r["frozen"]["wtm"][0], r["frozen"]["btm"][0])
            assert res["S"] == fz, ("CC != FG", r["P"], res["S"], fz)     # CC reproduces the exact frozen game
            tally["CC==frozen (all rows)"] += 1
            outc = r["convention_textbook"]["outcome"]
            testable = outc != "race" and r["exact"]
            exact = r["exact"]
            real = (r["real"]["wtm"][0], r["real"]["btm"][0])
            ccpred = res["S"]
            if exact and outc == "race":
                tally["race-at-start rows with exact real value"] += 1
                tally["  race rows: CC matches real"] += (ccpred == real)
            if testable:
                tally["testable"] += 1
                tally["before: textbook mismatch"] += (r["verdict_textbook"] == "MISMATCH")
                tally["before: ep-aware mismatch"] += (r["verdict_ep-aware"] == "MISMATCH")
                tally["after: CC mismatch"] += (ccpred != real)
                tally["after: CC mismatch (frozen==real, i.e. 0 expected)"] += 0
                if ccpred != real:
                    tally["after: CC mismatch where frozen==CC (king effect)"] += 1
        rescore[name] = dict(tally)
        rescore[name]["nodes_S"] = ccs["S"].nodes
        rescore[name]["expanded_passed_nodes_S"] = ccs["S"].expanded_passed
        rescore[name]["nodes_RP"] = ccs["RP"].nodes
        rescore[name]["expanded_passed_nodes_RP"] = ccs["RP"].expanded_passed
        print(name, rescore[name], flush=True)
    out["rescore"] = rescore
    json.dump(out, open(OUT + "cc_result.json", "w"), indent=1)
