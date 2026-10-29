"""Census of every decisive node of the convention's game trees (all roots of a sweep, both sides to move):
CG verdict vs the exact frozen result FG, and the two certificates S and RP.
Usage: python3 -I census.py   -> census_result.json"""
import json, sys, collections
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms")
import pawngame as pg, tests as T
R = "/Users/aritro/Downloads/Research/Chessendgames/kings/results/"
OUT = "/Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms/"
cfg = {"cyl7x6": ("exp_cyl7x6_epon_Q_conv.jsonl", 2, 3, 6), "cyl6x6": ("exp_cyl6x6_epon_Q_conv.jsonl", 1, 3, 6),
       "flat5x6": ("exp_flat5x6_epon_Q_conv.jsonl", 1, 0, 6)}


def collect(G, roots, resp):
    """decisive nodes (pos, mover, kind, cg_winner) reachable from roots through non-decisive nodes"""
    seen, nodes, stack = set(), {}, []
    for pos in roots:
        for side in "WB":
            stack.append((pos, side))
    while stack:
        pos, side = stack.pop()
        if (pos, side) in seen:
            continue
        seen.add((pos, side))
        wp, bp = G.passed(pos, "W", resp), G.passed(pos, "B", resp)
        if wp != bp:
            nodes[(pos, side)] = ("one-sided", "W" if wp else "L")
            continue
        if wp and bp:
            continue  # root-level race: excluded (cylcgt raises RaceError)
        for lab, p, promo in G.moves(pos, side):
            o = T.other(side)
            wp2, bp2 = G.passed(p, "W", resp), G.passed(p, "B", resp)
            if wp2 and bp2:
                oth = o
                win = oth if G.promote_distance(p, oth, resp) <= G.promote_distance(p, side, resp) else side
                nodes[(p, o)] = ("race", "W" if win == "W" else "L")
            else:
                stack.append((p, o))
    return nodes


result = {}
for name, (fn, k, off, H) in cfg.items():
    rows = [json.loads(l) for l in open(R + fn)]
    G = pg.Game(k, H, True, off)
    roots = [G.parse(r["P"]) for r in rows]
    for rule, resp in (("textbook", False), ("ep-aware", True)):
        nodes = collect(G, roots, resp)
        c = collections.Counter()
        bad_examples = []
        for (pos, side), (kind, cgw) in nodes.items():
            truth = G.fg(pos, side)[0]
            X = cgw_side = "W" if cgw == "W" else "B"
            Sx = T.S_cert(G, pos, side, X, resp)
            Rx = T.RP_cert(G, pos, side, X, resp)
            Sy = T.S_cert(G, pos, side, T.other(X), resp)
            Ry = T.RP_cert(G, pos, side, T.other(X), resp)
            correct = truth == cgw
            key = (kind, "cg_correct" if correct else "cg_WRONG")
            c[key + ("nodes",)] += 1
            c[key + ("S_cert_X",)] += Sx
            c[key + ("RP_cert_X",)] += Rx
            c[key + ("S_cert_other_side",)] += Sy       # must be 0 unless the other side really wins
            c[key + ("RP_cert_other_side",)] += Ry
            # soundness: a certified side must be the true winner
            for who, cert in (("S", Sx), ("RP", Rx)):
                if cert and not correct:
                    c[("UNSOUND", who, kind)] += 1
            for who, cert in (("S", Sy), ("RP", Ry)):
                if cert and correct:
                    c[("UNSOUND-other", who, kind)] += 1
            if Sx and not Rx:
                c[("S_not_subset_RP",)] += 1
            # S as a stand-alone verdict: X wins iff S certifies X (uncertified -> Y wins)
            verdictS = cgw if Sx else ("L" if cgw == "W" else "W")
            c[key + ("S_as_verdict_right",)] += (verdictS == truth)
        result[f"{name}/{rule}"] = {"|".join(map(str, k_)): v for k_, v in sorted(c.items(), key=str)}
        print(name, rule, len(nodes), "decisive nodes")
        for k_, v in sorted(c.items(), key=str):
            print("   ", k_, v)
json.dump(result, open(OUT + "census_result.json", "w"), indent=1)
