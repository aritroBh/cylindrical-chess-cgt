"""C2-theory: flip test re-judged against the tablebase on both sides (originals from suite, twins probed).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/engines/C2-theory/tb_flip.py
"""
import json
from collections import Counter
from pathlib import Path
R = Path("/Users/aritro/Downloads/Research/Chessendgames")
se = {r["id"]: r for r in json.loads((R/"engine/experiments/results/static_eval.json").read_text())["rows"]}
lc = {r["id"]: r for r in json.loads((R/"engine/experiments/results/lc0_value_n1.json").read_text())["rows"]}
tw = {}
for x in json.loads((R/"verify/engines/C2-theory/twin_probe_results.json").read_text()):
    tw[x["id"]] = x["tb_root_twin"]
for x in json.loads((R/"verify/engines/C4-theory/twin_results.json").read_text()):
    tw.setdefault(x["id"], x["tb_root_twin"])
SC = {"win": 1, "cursed-win": 0, "draw": 0, "blessed-loss": 0, "loss": -1}  # 50-move: cursed/blessed = draw
def wpov(cat, stm):
    s = SC[cat]
    return s if stm == "W" else -s
rows = []
for i, t in tw.items():
    r = se[i]; l = lc[i]
    tstm = "B" if r["stm"] == "W" else "W"
    rW = wpov(r["tb_root"], r["stm"]) if r["stm"] == "W" else wpov(t, tstm)
    rB = wpov(t, tstm) if r["stm"] == "W" else wpov(r["tb_root"], r["stm"])
    sgn = 1 if r["stm"] == "W" else -1
    dsf = (r["final"] - r["twin_final"]) * sgn
    dlc = (l["lc0_orig_white_cp"] - l["lc0_twin_white_cp"]) * sgn
    eW_sf = r["final"] if r["stm"] == "W" else r["twin_final"]; eB_sf = r["twin_final"] if r["stm"] == "W" else r["final"]
    eW_lc = l["lc0_orig_white_cp"] if r["stm"] == "W" else l["lc0_twin_white_cp"]; eB_lc = l["lc0_twin_white_cp"] if r["stm"] == "W" else l["lc0_orig_white_cp"]
    rows.append(dict(id=i, o=r["o"], value=r["value_count"], rW=rW, rB=rB, dsf=dsf, dlc=dlc,
                     eW_sf=eW_sf, eB_sf=eB_sf, eW_lc=eW_lc, eB_lc=eB_lc, tb_orig=r["tb_root"], tb_twin=t))
print("twins with TB data:", len(rows), Counter(r["o"] for r in rows))
print("non-standard twin categories:", Counter(r["tb_twin"] for r in rows if r["tb_twin"] not in ("win","loss","draw")))
def real_class(r):
    return {(1, -1): "N", (-1, 1): "P", (1, 1): "L", (-1, -1): "R"}.get((r["rW"], r["rB"]), f"({r['rW']},{r['rB']})")
for o in "NP":
    rs = [r for r in rows if r["o"] == o]
    print(f"\n== CGT-model class {o}: n={len(rs)}")
    print(" real (rW,rB) classes:", Counter(real_class(r) for r in rs))
    want_model = 1 if o == "N" else -1
    sf_m = sum((r["dsf"] > 0) == (want_model > 0) for r in rs)
    lc_m = sum((r["dlc"] > 0) == (want_model > 0) for r in rs)
    print(f" direction right vs MODEL: SF {sf_m}/{len(rs)}, Lc0 {lc_m}/{len(rs)}")
    dd = [r for r in rs if r["rW"] != r["rB"]]
    sf_t = sum((r["dsf"] > 0) == (r["rW"] > r["rB"]) for r in dd)
    lc_t = sum((r["dlc"] > 0) == (r["rW"] > r["rB"]) for r in dd)
    print(f" pairs where TB predicts a direction: {len(dd)} (model direction == TB direction in "
          f"{sum((r['rW'] > r['rB']) == (want_model > 0) for r in dd)})")
    print(f" direction right vs TABLEBASE: SF {sf_t}/{len(dd)}, Lc0 {lc_t}/{len(dd)}")
    print(f" TB says no change (rW == rB): {len(rs) - len(dd)}")
    # both signs right vs TB, on pairs where both sides are decisive
    dec = [r for r in rs if r["rW"] != 0 and r["rB"] != 0]
    bs = lambda eW, eB, r: (eW > 0) == (r["rW"] > 0) and (eB > 0) == (r["rB"] > 0)
    print(f" both sides decisive in TB: {len(dec)}; both eval signs right: SF {sum(bs(r['eW_sf'], r['eB_sf'], r) for r in dec)}, "
          f"Lc0 {sum(bs(r['eW_lc'], r['eB_lc'], r) for r in dec)}")
    for r in rs:
        print(f"  {r['id']} {r['value']:>14} TB W-to-move {r['rW']:+d} B-to-move {r['rB']:+d} | SF d={r['dsf']:+.2f} "
              f"(W {r['eW_sf']:+.2f}, B {r['eB_sf']:+.2f}) | Lc0 d={r['dlc']:+5d} (W {r['eW_lc']:+5d}, B {r['eB_lc']:+5d})")
