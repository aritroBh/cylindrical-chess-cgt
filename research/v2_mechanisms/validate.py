"""Validate the scratch pawn engine: FG vs kpsolve --frozen (root + every pawn move value), CG vs stored cylcgt outcomes."""
import json, sys, collections
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms")
import pawngame as pg, kp
R = "/Users/aritro/Downloads/Research/Chessendgames/kings/results/"
cfg = {"cyl7x6": ("exp_cyl7x6_epon_Q_conv.jsonl", "cyl:7x6", 2, 3, 6),
       "cyl6x6": ("exp_cyl6x6_epon_Q_conv.jsonl", "cyl:6x6", 1, 3, 6),
       "flat5x6": ("exp_flat5x6_epon_Q_conv.jsonl", "flat:5x6", 1, 0, 6)}
report = {}
for name, (fn, board, k, off, H) in cfg.items():
    rows = [json.loads(l) for l in open(R + fn)]
    G = pg.Game(k, H, True, off)
    root_bad = move_bad = nroots = nmoves = 0
    lines = []
    for r in rows:
        lines += [r["wtm"], r["btm"]]
    res, err = kp.run(lines, board, frozen=True, cap=1, tag="validate_" + name)
    for r in rows:
        pos = G.parse(r["P"])
        for side, key in (("W", "wtm"), ("B", "btm")):
            a, b, mv = res[r[key]]
            mine, _ = G.fg(pos, side)
            nroots += 1
            exp = {"W": "W", "L": "L"}[mine]
            if not (a == b == exp): root_bad += 1
            # stored frozen
            sf = r["frozen"][key]
            if not (sf[0] == sf[1] == exp): root_bad += 1000
            # move values: kpsolve lists king moves too (K...) -> compare pawn moves only
            fm = G.fg_moves(pos, side)
            km = {m: v for m, v in mv.items() if m[0] == "P"}
            conv = {}
            for lab, (rs, n, promo) in fm.items():
                conv[lab] = rs
            # map kpsolve move names (Pd2d3, Pd2e3, Pd5d6=Q) to labels (d2-d3, d2xe3, d2xe3ep)
            kmap = {}
            for m, v in km.items():
                body = m[1:].split("=")[0]
                kmap[body] = v
            mymap = {}
            for lab, rs in conv.items():
                body = lab.replace("-", "").replace("x", "").replace("ep", "")
                mymap[body] = rs
            nmoves += len(mymap)
            if kmap != mymap:
                move_bad += 1
                if move_bad < 4: print("MOVEDIFF", name, r[key], kmap, mymap)
    # CG vs stored
    cg_bad = collections.Counter(); cg_n = collections.Counter()
    for r in rows:
        pos = G.parse(r["P"])
        for rule, resp in (("textbook", False), ("ep-aware", True)):
            stored = r[f"convention_{rule}"]["outcome"]
            try:
                g = G.cg(pos, "W", resp), G.cg(pos, "B", resp)
            except ValueError:
                mine = "race"
            else:
                # outcome class from (white-to-move result, black-to-move result)
                mine = {("W", "W"): "L", ("L", "L"): "R", ("W", "L"): "N", ("L", "W"): "P"}[g]
            cg_n[rule] += 1
            if mine != stored:
                cg_bad[rule] += 1
                if cg_bad[rule] < 4: print("CGDIFF", name, rule, r["P"], mine, stored)
    report[name] = dict(roots=nroots, root_mismatch=root_bad, pawn_move_value_sets=nmoves, moveset_mismatch=move_bad,
                        cg_rows=dict(cg_n), cg_mismatch=dict(cg_bad), kpsolve_log=err)
    print(name, report[name])
json.dump(report, open("/Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms/validate_result.json", "w"), indent=1)
