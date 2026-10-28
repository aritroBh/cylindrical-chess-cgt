"""K21: N random contexts (1-4 pawns on the e,f files of cyl:7x6) for Z_onT1: prediction vs P-model (kp_p).  usage: chess_rand.py gen N seed | chess_rand.py cmp"""
import sys, json, random, os
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames")
from chess_pred import *
here = os.path.dirname(os.path.abspath(__file__)); ch = os.path.join(here, "..", "chess")
if sys.argv[1] == "gen":
    N, seed = int(sys.argv[2]), int(sys.argv[3]); rng = random.Random(seed)
    sq_ = [f + str(r) for f in "ef" for r in (2, 3, 4, 5)]
    seen = set(); rows = []
    while len(rows) < N:
        nw, nb = rng.choice([(1, 1), (1, 2), (2, 1), (2, 2), (1, 0), (0, 1), (2, 0), (0, 2), (3, 1), (1, 3)])
        w = rng.sample(sq_, nw); b = rng.sample([s for s in sq_ if s not in w], nb)
        pos = pos_from(w, b)
        if pos in seen or lc.terminal(BOARD, pos) is not None: continue
        seen.add(pos); rows.append({"group": "on", "ctx": fen_ctx(pos), "pred": predict(pos), "base": "Ka5 Pb4 Pc5 kc6 pb5"})
    json.dump(rows, open(os.path.join(ch, "pred_rand.json"), "w"), indent=0)
    with open(os.path.join(ch, "positions_rand.txt"), "w") as f:
        for r in rows:
            f.write(r["base"] + " " + r["ctx"] + " w -\n"); f.write(r["base"] + " " + r["ctx"] + " b -\n")
else:
    rows = json.load(open(os.path.join(ch, "pred_rand.json"))); res = {}
    for l in open(os.path.join(ch, "results_rand_P.txt")):
        if " | " in l:
            pos, r = l.rsplit(" | ", 1); res[pos.strip()] = r.split()
    cls = {}
    for r in rows:
        base = r["base"] + " " + r["ctx"]; w, b = res[base + " w -"], res[base + " b -"]
        got = (w[0], b[0]); pred = tuple(r["pred"])
        k = (pred, "ok" if got == pred else "DIFF->%s%s" % got); cls[k] = cls.get(k, 0) + 1
        if got != pred: print("DIFF", r["ctx"], "pred", pred, "P", got)
    print({str(k): v for k, v in sorted(cls.items())})
    print("agree", sum(v for k, v in cls.items() if k[1] == "ok"), "of", len(rows))
