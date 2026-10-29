"""Tables, CIs, rule ranking, feature fit and mismatch classes from pool_scored.json (offline, stdlib)."""
from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter, defaultdict

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
OUT = os.path.join(ROOT, "research", "flat_xtarget_census")
sys.path.insert(0, ROOT)

rows = json.load(open(os.path.join(OUT, "pool_scored.json")))
meta = json.load(open(os.path.join(OUT, "pool_meta.json")))
RULES = ("count", "mover", "opponent")
CONVS = ("textbook", "e.p.-aware")
SETS = [f"{c}|{r}" for c in CONVS for r in RULES]
MAIN = "e.p.-aware|count"
TARGETS = []
for r in rows:
    for c in CONVS:
        for t in r["tree"][c]:
            if t not in TARGETS:
                TARGETS.append(t)


def wilson(k, n, z=1.959964):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def fmt_ci(k, n):
    if n == 0:
        return "n/a"
    lo, hi = wilson(k, n)
    return f"{k}/{n} = {100*k/n:.1f}% [{100*lo:.1f}, {100*hi:.1f}]"


def cls(r, s):
    p = r["pred"][s]
    if p is None:
        return "outside"
    if r["res"] == 0:
        return "draw"
    return "agree" if (r["res"] == 1) == p else "disagree"


def tally(rs, s):
    c = Counter(cls(r, s) for r in rs)
    return {k: c.get(k, 0) for k in ("agree", "disagree", "draw", "outside")}


def binom_two_sided(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    s = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * s)


out = {}
md = []


def H(t):
    md.append("\n" + t + "\n")


def table(head, body):
    md.append("| " + " | ".join(head) + " |")
    md.append("|" + "|".join("---" for _ in head) + "|")
    for b in body:
        md.append("| " + " | ".join(str(x) for x in b) + " |")
    md.append("")


# ---------------------------------------------------------------- 0. pool
H("## 0. Pool")
src_fam = Counter()
for r in rows:
    fam = tuple(sorted({s.split(":")[0] for s in r["src"]}))
    src_fam[fam] += 1
out["pool"] = {"positions": len(rows), "conflicts": len(meta["conflicts"]),
               "by_men": dict(sorted(Counter(r["men"] for r in rows).items())),
               "by_source_family": {"+".join(k): v for k, v in src_fam.items()},
               "sources_loaded": meta["sources_loaded"]}
kp_overlap = [r for r in rows if any(s.startswith("kpsolve") for s in r["src"]) and
              any(not s.startswith("kpsolve") for s in r["src"])]
out["pool"]["kpsolve_positions"] = sum(1 for r in rows if any(s.startswith("kpsolve") for s in r["src"]))
out["pool"]["kpsolve_overlap_with_other_source"] = len(kp_overlap)
table(["item", "value"], [["distinct positions (normal FEN)", len(rows)],
                          ["source conflicts (same FEN, different result)", len(meta["conflicts"])],
                          ["positions by men", out["pool"]["by_men"]],
                          ["kpsolve exact positions", out["pool"]["kpsolve_positions"]],
                          ["kpsolve positions also answered by a Lichess/search source (all agree, 0 conflicts)", len(kp_overlap)]])

# --------------------------------------------------- 1. reproduce A2 figures
H("## 1. Reproduction of the A2 node figures (462 positions, 295 resolved)")
a2 = [r for r in rows if "A2nodes" in r["src"]]
repro = {}
body = []
for s in SETS:
    t = tally(a2, s)
    repro[s] = t
    body.append([s, t["agree"], t["disagree"], t["draw"], t["outside"]])
table(["setting", "agree", "disagree", "real draw", "outside"], body)
out["A2_repro_positions"] = repro
# configuration level, same logic as realchess/compare_nodes.py (key = component string, both sides resolved)
nodes = json.load(open(os.path.join(ROOT, "realchess/results/comp_Wa2c2_Bb7d7_nodes_pure_offline.json")))["nodes"]
from realchess import movegen as mg   # noqa: E402
byfen = {r["fen"]: r for r in rows}


def clsAB(w_first_white, b_first_white):
    m = {(1, 1): "L", (-1, -1): "R", (1, -1): "N", (-1, 1): "P"}
    return m.get((w_first_white, b_first_white), "D")


cfgs = {}
for n in nodes:
    w, b = n.get("W_fen"), n.get("B_fen")
    if not (w and b):
        continue
    w, b = mg.normal_fen(w), mg.normal_fen(b)
    if w in byfen and b in byfen and "A2nodes" in byfen[w]["src"] and "A2nodes" in byfen[b]["src"]:
        cfgs[n["component"]] = (byfen[w], byfen[b])
body = []
cfg_repro = {}
real_cls = Counter(clsAB(w["res"], -b["res"]) for w, b in cfgs.values())
for s in SETS:
    ag = 0
    for w, b in cfgs.values():
        pw, pb = w["pred"][s], b["pred"][s]
        if pw is None or pb is None:
            continue
        mc = clsAB(1 if pw else -1, -1 if pb else 1)
        ag += mc == clsAB(w["res"], -b["res"])
    cfg_repro[s] = ag
    body.append([s, f"{ag}/{len(cfgs)}"])
table(["setting", "configurations whose outcome class agrees"], body)
out["A2_repro_configurations"] = {"n": len(cfgs), "real_classes": dict(real_cls), "agree": cfg_repro}
md.append(f"Real classes of the {len(cfgs)} configurations: {dict(real_cls)}.\n")
md.append("Stored values in realchess/results/comp_Wa2c2_Bb7d7_nodes_vs_model_offline.json: e.p.-aware count 268/14/13, "
          "mover 266/16/13, opponent 247/35/13; textbook count 263/19/13, mover 261/21/13, opponent 239/43/13; "
          "configurations 92/91/85 (e.p.-aware) and 91/90/85 (textbook) of 119.\n")

# ------------------------------------------------ 2. whole pool by kind
H("## 2. Whole pool by kind of position (decisive agreement, Wilson 95% CI)")


def kind(r, c):
    return "end-position side" if r["term"][c] else "internal node"


def evid(r):
    if any(s.startswith("kpsolve") for s in r["src"]):
        return "kpsolve (exact)"
    if r["men"] <= 7:
        return "tablebase <=7 men"
    if r["l8"]:
        return "Lichess 8-man category only"
    return "8+ men search over tablebase"


body = []
agg = {}
for c in CONVS:
    for kd in ("end-position side", "internal node", "all"):
        sub = [r for r in rows if (kd == "all" or kind(r, c) == kd)]
        for rule in RULES:
            t = tally(sub, f"{c}|{rule}")
            dec = t["agree"] + t["disagree"]
            agg[f"{c}|{rule}|{kd}"] = t
            body.append([c, rule, kd, fmt_ci(t["agree"], dec), t["draw"], t["outside"], len(sub)])
table(["passer test", "race rule", "kind", "agree / decisive", "real draws", "not scored", "n"], body)
out["by_kind"] = agg

H("### 2b. End-position sides by evidence class and by men (e.p.-aware, count)")
body = []
for ev in ("tablebase <=7 men", "Lichess 8-man category only", "8+ men search over tablebase", "kpsolve (exact)"):
    for mn in (5, 6, 7, 8, 9, 10, 11):
        sub = [r for r in rows if r["term"]["e.p.-aware"] and evid(r) == ev and r["men"] == mn]
        if not sub:
            continue
        t = tally(sub, MAIN)
        body.append([ev, mn, fmt_ci(t["agree"], t["agree"] + t["disagree"]), t["draw"], len(sub)])
table(["evidence", "men", "agree / decisive", "real draws", "n"], body)

# ------------------------------------------------------- 3. per target
H("## 3. Per target (positions of the target's own tree that have an exact real result)")
out["targets"] = {}
for c in CONVS:
    H(f"### 3.{CONVS.index(c)+1} Passer test: {c}")
    body = []
    for tn in TARGETS:
        for kd in ("end-position side", "internal node"):
            sub = [r for r in rows if tn in r["tree"][c] and kind(r, c) == kd]
            if not sub:
                continue
            cell = []
            for rule in RULES:
                t = tally(sub, f"{c}|{rule}")
                cell.append(f"{t['agree']}/{t['disagree']}")
            t = tally(sub, f"{c}|count")
            men = Counter(r["men"] for r in sub)
            out["targets"].setdefault(c, {})[f"{tn}|{kd}"] = {
                rule: tally(sub, f"{c}|{rule}") for rule in RULES} | {"n": len(sub), "men": dict(men)}
            body.append([tn, kd, len(sub), t["draw"], cell[0], cell[1], cell[2],
                         fmt_ci(t["agree"], t["agree"] + t["disagree"]), dict(sorted(men.items()))])
    table(["target", "kind", "n", "real draws", "count a/d", "mover a/d", "opponent a/d",
           "count agree/decisive [CI]", "men"], body)
md.append("a/d = agree/disagree among decisive sides. A position in several targets' trees is counted in each row; "
          "the rows are not additive (see section 2 for the distinct-position totals).\n")

# ------------------------------------------------ 4. rule ranking
H("## 4. Ranking of the six settings (passer test x race rule)")
ok = [r for r in rows if r["res"] != 0 and all(r["pred"][s] is not None for s in SETS)]
subsets = {"all decisive scored positions": ok,
           "end-position sides only (e.p.-aware tree)": [r for r in ok if r["term"]["e.p.-aware"]],
           "internal nodes only": [r for r in ok if not r["term"]["e.p.-aware"]],
           "race terminals only (both sides have a passer)": [r for r in ok if r["race"]["e.p.-aware"]],
           "excluding Lichess-8-man-category-only positions": [r for r in ok if not (r["l8"] and r["men"] >= 8)],
           "positions where the settings differ": [r for r in ok if len({r["pred"][s] for s in SETS}) > 1]}
out["ranking"] = {}
for name, sub in subsets.items():
    H(f"### {name} (n = {len(sub)})")
    acc = {s: sum(1 for r in sub if (r['res'] == 1) == r['pred'][s]) for s in SETS}
    order = sorted(SETS, key=lambda s: -acc[s])
    table(["rank", "setting", "agree / n [95% CI]"], [[i + 1, s, fmt_ci(acc[s], len(sub))] for i, s in enumerate(order)])
    pr = []
    for i, a in enumerate(order):
        for b in order[i + 1:]:
            only_a = sum(1 for r in sub if (r["res"] == 1) == r["pred"][a] and (r["res"] == 1) != r["pred"][b])
            only_b = sum(1 for r in sub if (r["res"] == 1) != r["pred"][a] and (r["res"] == 1) == r["pred"][b])
            pr.append([a, b, only_a, only_b, f"{binom_two_sided(only_a, only_b):.4g}"])
    table(["better-ranked", "lower-ranked", "only first right", "only second right", "exact McNemar p"], pr)
    out["ranking"][name] = {"n": len(sub), "agree": acc, "order": order}
md.append("The pairs share positions and many positions share one terminal (two sides) and overlapping trees, so the "
          "McNemar p-values and CIs treat dependent items as independent and are optimistic. Draws are excluded from this "
          "section; they are model-independent in count (the model has no draw value).\n")

# ---------------------------------- 5. features: logistic + stumps
H("## 5. Which features predict disagreement? (e.p.-aware, count; decisive scored positions)")
dec = [r for r in rows if r["res"] != 0 and r["pred"][MAIN] is not None]
for r in dec:
    r["dis"] = int((r["res"] == 1) != r["pred"][MAIN])
FE = [("men_minus_8", lambda r: r["men"] - 8), ("a_file_pawns", lambda r: r["afile"]),
      ("race", lambda r: int(r["race"]["e.p.-aware"])), ("ep_available", lambda r: int(r["ep"])),
      ("end_position", lambda r: int(r["term"]["e.p.-aware"])), ("white_to_move", lambda r: int(r["stm"] == "W")),
      ("l8_only", lambda r: int(r["l8"] and r["men"] >= 8))]
def solve(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        p = max(range(i, n), key=lambda j: abs(M[j][i]))
        M[i], M[p] = M[p], M[i]
        for j in range(n):
            if j != i:
                f = M[j][i] / M[i][i]
                for k in range(i, n + 1):
                    M[j][k] -= f * M[i][k]
    return [M[i][n] / M[i][i] for i in range(n)]


def inv(A):
    n = len(A)
    cols = []
    for j in range(n):
        e = [1.0 if i == j else 0.0 for i in range(n)]
        cols.append(solve(A, e))
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def logit(X, y, lam=0.5, iters=60):
    k = len(X[0])
    w = [0.0] * k
    for _ in range(iters):
        g = [0.0] * k
        Hm = [[0.0] * k for _ in range(k)]
        for xi, yi in zip(X, y):
            z = sum(a * b for a, b in zip(w, xi))
            p = 1 / (1 + math.exp(-max(-30, min(30, z))))
            for a in range(k):
                g[a] += (yi - p) * xi[a]
                for b in range(k):
                    Hm[a][b] += p * (1 - p) * xi[a] * xi[b]
        for a in range(1, k):
            g[a] -= lam * w[a]
            Hm[a][a] += lam
        step = solve(Hm, g)
        w = [a + b for a, b in zip(w, step)]
        if max(abs(s) for s in step) < 1e-9:
            break
    cov = inv(Hm)
    return w, [math.sqrt(max(cov[i][i], 0)) for i in range(k)]


def gini(k, n):
    if n == 0:
        return 0.0
    p = k / n
    return 2 * p * (1 - p)


def feature_fit(dec, label, tag):
    global X, y
    H(f"### Subset: {label}")
    X = [[1.0] + [f(r) for _, f in FE] for r in dec]
    y = [r["dis"] for r in dec]
    w, se = logit(X, y)
    names = ["intercept"] + [n for n, _ in FE]
    body = [[n, f"{a:+.3f}", f"{s:.3f}", f"{math.exp(a):.3g}" if n != "intercept" else "", f"{a/s:+.2f}"]
            for n, a, s in zip(names, w, se)]
    table(["feature", "coef (log-odds of disagreement)", "approx SE", "odds ratio", "z"], body)
    out.setdefault("logistic", {})[tag] = {"n": len(dec), "disagreements": sum(y), "ridge_lambda": 0.5, "features": dict(zip(names, w)),
                       "se": dict(zip(names, se))}
    md.append(f"n = {len(dec)} decisive scored positions, {sum(y)} disagreements. Ridge penalty 0.5 on slopes (the data are sparse "
              "and partly collinear: race implies end_position). Standard errors are model-based and ignore clustering.\n")


    H("### Decision stumps (single split, weighted Gini reduction)")
    base = gini(sum(y), len(y))
    st = []
    for (n, f) in FE:
        vals = sorted({f(r) for r in dec})
        for th in vals[:-1]:
            L = [r["dis"] for r in dec if f(r) <= th]
            R_ = [r["dis"] for r in dec if f(r) > th]
            g = base - (len(L) * gini(sum(L), len(L)) + len(R_) * gini(sum(R_), len(R_))) / len(dec)
            st.append((g, n, th, sum(L), len(L), sum(R_), len(R_)))
    st.sort(reverse=True)
    table(["feature <= threshold", "disagree in <= branch", "disagree in > branch", "Gini reduction"],
          [[f"{n} <= {th}", fmt_ci(a, b), fmt_ci(c, d), f"{g:.4f}"] for g, n, th, a, b, c, d in st[:10]])
    out.setdefault("stumps", {})[tag] = [{"feature": n, "threshold": th, "le": [a, b], "gt": [c, d], "gini_gain": g} for g, n, th, a, b, c, d in st[:10]]

    H("### Disagreement rate by single feature value (e.p.-aware, count)")
    body = []
    for n, f in FE:
        for v in sorted({f(r) for r in dec}):
            sub = [r for r in dec if f(r) == v]
            body.append([n, v, fmt_ci(sum(r["dis"] for r in sub), len(sub))])
    table(["feature", "value", "disagree / decisive [CI]"], body)



dec_all = [r for r in rows if r["res"] != 0 and r["pred"][MAIN] is not None]
for r in dec_all:
    r["dis"] = int((r["res"] == 1) != r["pred"][MAIN])
feature_fit(dec_all, "all decisive scored positions", "all")
feature_fit([r for r in dec_all if not (r["l8"] and r["men"] >= 8)], "excluding Lichess-8-man-category-only positions", "no_l8")

# ----------------------------------------- 6. mismatch classification
H("## 6. Every mismatch classified (e.p.-aware, count)")


def mclass(r):
    p = r["pred"][MAIN]
    if p is None:
        return "not scored (internal node with more than 6 pawns)"
    real = r["res"]
    if real == 0:
        return "real draw; model says " + ("win" if p else "loss") + (" (end-position side)" if r["term"]["e.p.-aware"] else " (internal node)")
    if (real == 1) == p:
        return None
    if r["race"]["e.p.-aware"]:
        return "disagree: race terminal (race rule picks the wrong winner)"
    if r["term"]["e.p.-aware"]:
        return "disagree: one-sided passer, the passer's owner does not win in real chess"
    return "disagree: internal node (model first-player outcome wrong)"


mc = defaultdict(list)
for r in rows:
    k = mclass(r)
    if k:
        mc[k].append(r)
body = [[k, len(v), dict(sorted(Counter(r["men"] for r in v).items())), sum(1 for r in v if r["ep"])]
        for k, v in sorted(mc.items(), key=lambda kv: -len(kv[1]))]
table(["class", "count", "by men", "with e.p. right"], body)
out["mismatch_classes"] = {k: len(v) for k, v in mc.items()}
with open(os.path.join(OUT, "mismatches.tsv"), "w") as fh:
    fh.write("class\tfen\tmen\treal_for_side_to_move\tmodel_stm_wins_by_setting\ttargets_e.p.-aware\tsources\n")
    for k, v in mc.items():
        for r in v:
            fh.write("\t".join([k, r["fen"], str(r["men"]), str(r["res"]),
                                ",".join(f"{s}={r['pred'][s]}" for s in SETS), ";".join(r["tree"]["e.p.-aware"]),
                                ";".join(r["src"])]) + "\n")

# disagreement by target
H("### Disagreements and real draws by target and mechanism (e.p.-aware, count)")
body = []
for tn in TARGETS:
    sub = [r for r in rows if tn in r["tree"]["e.p.-aware"]]
    c = Counter(mclass(r) for r in sub if mclass(r))
    body.append([tn, len(sub), sum(c.values()), dict(c)])
table(["target", "resolved positions", "mismatches", "by class"], body)

# who is in agreement across settings
H("## 7. Sensitivity of the class counts to the setting")
body = []
for s in SETS:
    c = Counter()
    for r in rows:
        k = None
        p = r["pred"][s]
        if p is not None and r["res"] != 0 and (r["res"] == 1) != p:
            k = "race" if r["race"][s.split("|")[0]] else ("terminal" if r["term"][s.split("|")[0]] else "node")
        if k:
            c[k] += 1
    body.append([s, sum(c.values()), dict(c)])
table(["setting", "disagreements", "by kind"], body)


H("## 8. Headline numbers excluding positions whose only evidence is a Lichess 8-man category")
clean = [r for r in rows if not (r["l8"] and r["men"] >= 8)]
body = []
for c in CONVS:
    for kd in ("end-position side", "internal node", "all"):
        sub = [r for r in clean if kd == "all" or kind(r, c) == kd]
        t = tally(sub, f"{c}|count")
        body.append([c, kd, fmt_ci(t["agree"], t["agree"] + t["disagree"]), t["draw"], len(sub)])
table(["passer test", "kind", "count rule: agree / decisive", "real draws", "n"], body)
out["clean_headline"] = {c: tally(clean, f"{c}|count") for c in CONVS}
out["all_resolved_incl_draws_as_miss"] = {s: [tally(rows, s)["agree"], len(rows)] for s in SETS}

H("## 9. One-sided passer disagreements (e.p.-aware, count): who moves and how far the passer is")
from cylcgt import pawns as _pw   # noqa: E402
from cylcgt.pawns import Pos as _Pos   # noqa: E402
from realchess import component as _C   # noqa: E402
_pw.PASSED_RESPECTS_EP = True
rowsb = Counter()
tot = Counter()
for r in rows:
    if not r["term"]["e.p.-aware"] or r["race"]["e.p.-aware"] or r["pred"][MAIN] is None or r["res"] == 0:
        continue
    pos = mg.parse_fen(r["fen"])
    cp = _C.component_of(pos)
    owner = "W" if _pw.passed(_C.BOARD4, cp, "W") else "B"
    stm = r["stm"]
    d = _pw.promote_distance(_C.BOARD4, cp, owner)
    key = ("owner to move" if owner == stm else "owner's opponent to move", f"dist {min(d, 6)}")
    tot[key] += 1
    if (r["res"] == 1) != r["pred"][MAIN]:
        rowsb[key] += 1
table(["mover", "passer distance to queen (moves, capped 6)", "disagree / one-sided decisive sides"],
      [[k[0], k[1], fmt_ci(rowsb[k], tot[k])] for k in sorted(tot)])
out["one_sided_by_mover_distance"] = {f"{k[0]}|{k[1]}": [rowsb[k], tot[k]] for k in tot}

json.dump(out, open(os.path.join(OUT, "census.json"), "w"), indent=1, default=str)
open(os.path.join(OUT, "tables.md"), "w").write("\n".join(md))
print("\n".join(md))
