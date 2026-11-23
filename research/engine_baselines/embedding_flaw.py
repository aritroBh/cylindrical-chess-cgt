"""Split ChessSums embedded positions by king-group placement. Offline.
Run from repo root: .venv/bin/python research/engine_baselines/embedding_flaw.py"""
import json, math, collections, chess
D = "engine/runs/chesssums/"
meta = json.load(open(D + "meta.json")); M = {m["id"]: m for m in meta}
ids = json.load(open(D + "subset_ids.json"))
def klass(m):
    fz = m["freeze"]; gs = {fz[x][0] for x in ("wk", "bk", "wp", "bp")}
    gsq = {fz[x] for x in ("wk", "bk", "wp", "bp")}
    b = chess.Board(m["fen"] + " 0 1")
    cf = {chess.square_file(s) for s in b.pieces(chess.PAWN, True) | b.pieces(chess.PAWN, False)
          if chess.square_name(s) not in gsq}
    g = {ord(c) - 97 for c in gs}
    if cf & g: return "SHARED"
    if any(abs(a - c) == 1 for a in cf for c in g): return "ADJACENT"
    return "APART"
for m in meta: m["cls"] = klass(m)
def wilson(k, n, z=1.96):
    if n == 0: return "-"
    p = k / n; den = 1 + z * z / n; c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return f"{100*(c-h):.0f}-{100*(c+h):.0f}"
res = {"SF1k": [r for r in json.load(open(D + "sf_results.json"))["results"] if r["limit"] == "nodes 1000"],
       "SF10k": [r for r in json.load(open(D + "sf_results.json"))["results"] if r["limit"] == "nodes 10000"],
       "SF100k": [r for r in json.load(open(D + "sf_results.json"))["results"] if r["limit"] == "nodes 100000"],
       "SF1M": [r for r in json.load(open(D + "sf_results.json"))["results"] if r["limit"] == "nodes 1000000"],
       "Lc1k": json.load(open(D + "lc0_1k_merged.json"))["results"],
       "Lc10k": json.load(open(D + "lc0_10k_merged.json"))["results"]}
R = {e: {r["id"]: r for r in l} for e, l in res.items()}
nonebest = collections.Counter()
def stats(sel):
    n = len(sel); o = {"n": n}
    o["P"] = sum(M[i]["outcome"] == "P" for i in sel)
    rows = []
    for i in sel:
        b = chess.Board(M[i]["fen"] + " 0 1")
        L = {x.uci() for x in b.legal_moves}
        pw = {x.uci() for x in b.legal_moves if b.piece_type_at(x.from_square) == chess.PAWN}
        S = set(M[i]["solutions_uci"]); rows.append((len(L), len(pw), len(S & L), len(S & pw), len(S)))
    o["legalwin"] = sum(r[2] > 0 for r in rows)
    o["haswin"] = sum(r[4] > 0 for r in rows)
    o["illegal_listed"] = sum(r[4] - r[2] for r in rows)
    o["pos_illegal"] = sum(r[4] > r[2] for r in rows)
    o["rl"] = 100 * sum(r[2] / r[0] for r in rows) / n
    o["rp"] = 100 * sum(r[3] / r[1] for r in rows if r[1]) / n
    o["eng"] = {}
    for e in R:
        k = sum(R[e][i]["solved"] for i in sel)
        kw = sum(R[e][i]["solved"] for i in sel if M[i]["solutions_uci"])
        wrong = [i for i in sel if not R[e][i]["solved"]]
        kmv = 0
        for i in wrong:
            b = chess.Board(M[i]["fen"] + " 0 1")
            bm = R[e][i]["best"]
            if bm is None: nonebest[e] += 1; continue
            kmv += b.piece_type_at(chess.Move.from_uci(bm).from_square) == chess.KING
        o["eng"][e] = dict(k=k, kw=kw, nw=o["haswin"], ci=wilson(k, n), ciw=wilson(kw, o["haswin"]), wrong=len(wrong), kingwrong=kmv)
    return o
groups = {c: [i for i in ids if M[i]["cls"] == c] for c in ("SHARED", "ADJACENT", "APART")}
groups["ADJ+APART"] = groups["ADJACENT"] + groups["APART"]
groups["ALL200"] = list(ids)
out = {c: stats(s) for c, s in groups.items()}
allc = collections.Counter((m["cls"], m["k"]) for m in meta)
allt = collections.Counter(m["cls"] for m in meta)
lines = ["| class | n | outcome P | has listed win | has legal win | positions w/ illegal listed | illegal listed moves | random legal % | random pawn % |", "|---|---|---|---|---|---|---|---|---|"]
for c, o in out.items():
    lines.append(f"| {c} | {o['n']} | {o['P']} | {o['haswin']} | {o['legalwin']} | {o['pos_illegal']} | {o['illegal_listed']} | {o['rl']:.1f} | {o['rp']:.1f} |")
lines += ["", "Engine right (k/n %, Wilson95 over n) and right among positions with a listed winning move (k/nw %, Wilson95); wrong answers that were king moves (kw/wrong)", "",
          "| class | engine | k/n | % | CI | k/nw | % | CI | king moves among wrong |", "|---|---|---|---|---|---|---|---|---|"]
for c, o in out.items():
    for e, v in o["eng"].items():
        lines.append(f"| {c} | {e} | {v['k']}/{o['n']} | {100*v['k']/o['n']:.1f} | {v['ci']} | {v['kw']}/{v['nw']} | {100*v['kw']/v['nw']:.1f} | {v['ciw']} | {v['kingwrong']}/{v['wrong']} |" if v['nw'] else f"| {c} | {e} | {v['k']}/{o['n']} | {100*v['k']/o['n']:.1f} | {v['ci']} | 0/0 | - | - | {v['kingwrong']}/{v['wrong']} |")
lines += ["", "All embedded rows in meta.json, by class and k (APART = clean):", "", "| class | k=1 | k=2 | k=3 | k=4 | total |", "|---|---|---|---|---|---|"]
for c in ("SHARED", "ADJACENT", "APART"):
    lines.append(f"| {c} | " + " | ".join(str(allc[(c, k)]) for k in (1, 2, 3, 4)) + f" | {allt[c]} |")
lines.append("| all | " + " | ".join(str(sum(allc[(c, k)] for c in allt)) for k in (1, 2, 3, 4)) + f" | {len(meta)} |")
print("best=None counts (all groups, may double count):", dict(nonebest))
open("research/engine_baselines/embedding_flaw_tables.md", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))

# Stockfish crashes ("engine exited") on positions with more than 8 pawns on one side
crash = {i for i in ids if R["SF1k"][i]["best"] is None}
assert all(R[e][i]["best"] is None for e in ("SF10k", "SF100k", "SF1M") for i in crash)
ok = [i for i in ids if i not in crash]
okw = [i for i in ok if M[i]["solutions_uci"]]
ex = ["", "## Stockfish crashes", f"Stockfish exited on {len(crash)} of 200 positions at every budget (all have a listed winning move, all have >8 pawns for one side; classes: {dict(collections.Counter(M[i]['cls'] for i in crash))}), scored as errors. Lc0 answered them.", "",
      "| engine | right/ n | % | Wilson95 | right / n with a listed win | % | Wilson95 |", "|---|---|---|---|---|---|---|"]
for e in R:
    k = sum(R[e][i]["solved"] for i in ok); kw = sum(R[e][i]["solved"] for i in okw)
    ex.append(f"| {e} (the 173 non-crash positions) | {k}/{len(ok)} | {100*k/len(ok):.1f} | {wilson(k, len(ok))} | {kw}/{len(okw)} | {100*kw/len(okw):.1f} | {wilson(kw, len(okw))} |")
open("research/engine_baselines/embedding_flaw_tables.md", "a").write("\n".join(ex) + "\n")
print("\n".join(ex))
