"""K63 referee: probe the Lichess (Syzygy) tablebase for F1-F4 and the mirror of F2.

Read-only use of realchess.probe.Prober (cap 150, own ledger and cache).  Each position is
given twice: as a piece list (turned into a FEN here) and as a FEN typed by hand; the two must
agree, and the API's move list must equal realchess.movegen's legal moves.
Run from the repository root:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python kings/delegate/out/K63/verify/src/tb_probe.py
"""
import json, sys, time
from realchess.probe import Prober, categories
from realchess import movegen as mg

V = "kings/delegate/out/K63/verify"
PR = Prober(cap=150, ledger=f"{V}/tb_ledger.jsonl", cache_dir=f"{V}/tbcache", tag="K63ref")

def fen_of(pieces, stm):
    b = [["."] * 8 for _ in range(8)]
    for p in pieces.split():
        f, r = "abcdefgh".index(p[1]), int(p[2]) - 1
        assert b[r][f] == "."
        b[r][f] = p[0]
    rows = []
    for r in range(7, -1, -1):
        s, n = "", 0
        for c in b[r]:
            if c == ".": n += 1
            else:
                if n: s += str(n); n = 0
                s += c
        if n: s += str(n)
        rows.append(s)
    return "/".join(rows) + f" {stm} - - 0 1"

def diagram(fen):
    rows = fen.split()[0].split("/")
    out = []
    for i, row in enumerate(rows):
        line = ""
        for ch in row:
            line += "." * int(ch) if ch.isdigit() else ch
        out.append(f"  {8-i} " + " ".join(line))
    out.append("    a b c d e f g h")
    return "\n".join(out)

# (group, label, pieces, hand-typed board part)
POS = []
def grp(g, rootA, rootB, qA, qB):
    for lab, (pc, hand) in (("rootA", rootA), ("rootB", rootB), ("qA", qA), ("qB", qB)):
        if pc is None: continue
        for stm in "wb":
            POS.append((g, lab, pc, hand, stm))

grp("F2", ("Ka4 kc4 Pb2 Pf5 pb6 pf6", "8/8/1p3p2/5P2/K1k5/8/1P6/8"),
          ("Ka4 kc5 Pb2 Pf5 pb6 pf6", "8/8/1p3p2/2k2P2/K7/8/1P6/8"),
          ("Ka4 kc4 Pb4 Pf5 pb6 pf6", "8/8/1p3p2/5P2/KPk5/8/8/8"),
          ("Ka4 kc5 Pb3 Pf5 pb6 pf6", "8/8/1p3p2/2k2P2/K7/1P6/8/8"))
grp("F1", ("Ka4 kc4 Pb2 Pe4 Pe5 pb6 pe6", "8/8/1p2p3/4P3/K1k1P3/8/1P6/8"),
          ("Ka4 kc5 Pb2 Pe4 Pe5 pb6 pe6", "8/8/1p2p3/2k1P3/K3P3/8/1P6/8"),
          ("Ka4 kc4 Pb4 Pe4 Pe5 pb6 pe6", "8/8/1p2p3/4P3/KPk1P3/8/8/8"),
          ("Ka4 kc5 Pb3 Pe4 Pe5 pb6 pe6", "8/8/1p2p3/2k1P3/K3P3/1P6/8/8"))
grp("F3", ("Ke4 kc4 Pb2 Pb5 Pf5 pb6 pf6", "8/8/1p3p2/1P3P2/2k1K3/8/1P6/8"),
          ("Ke4 kc5 Pb2 Pb5 Pf5 pb6 pf6", "8/8/1p3p2/1Pk2P2/4K3/8/1P6/8"),
          ("Ke4 kc4 Pb4 Pb5 Pf5 pb6 pf6", "8/8/1p3p2/1P3P2/1Pk1K3/8/8/8"),
          ("Ke4 kc5 Pb3 Pb5 Pf5 pb6 pf6", "8/8/1p3p2/1Pk2P2/4K3/1P6/8/8"))
grp("F4", ("Kc4 ke4 Pb5 Pf2 Pf5 pb6 pf6", "8/8/1p3p2/1P3P2/2K1k3/8/5P2/8"),
          ("Kc4 ke5 Pb5 Pf2 Pf5 pb6 pf6", "8/8/1p3p2/1P2kP2/2K5/8/5P2/8"),
          ("Kc4 ke4 Pb5 Pf4 Pf5 pb6 pf6", "8/8/1p3p2/1P3P2/2K1kP2/8/8/8"),
          ("Kc4 ke5 Pb5 Pf3 Pf5 pb6 pf6", "8/8/1p3p2/1P2kP2/2K5/5P2/8/8"))
# mirror of F2 (under group): White shuttles c5/c4; q after ...b7-b5 (at Kc5) and ...b7-b6 (at Kc4)
grp("F2mirror", ("Kc5 ka5 Pb3 Pf3 pb7 pf4", "8/1p6/8/k1K5/5p2/1P3P2/8/8"),
                ("Kc4 ka5 Pb3 Pf3 pb7 pf4", "8/1p6/8/k7/2K2p2/1P3P2/8/8"),
                ("Kc5 ka5 Pb3 Pf3 pb5 pf4", "8/8/8/kpK5/5p2/1P3P2/8/8"),
                ("Kc4 ka5 Pb3 Pf3 pb6 pf4", "8/8/1p6/k7/2K2p2/1P3P2/8/8"))

def main(only=None):
    res = []
    for g, lab, pc, hand, stm in POS:
        if only and g not in only: continue
        fen = fen_of(pc, stm)
        assert fen.split()[0] == hand, (g, lab, fen, hand)
        pos = mg.parse_fen(fen)
        errs = mg.validity_errors(pos)
        print(f"### {g} {lab} {pc}  {'White' if stm=='w' else 'Black'} to move")
        print(f"FEN {fen}")
        print(diagram(fen))
        if errs:
            print("ILLEGAL:", errs); print(); continue
        rec = PR.probe(fen)
        cat, mv = categories(rec)
        legal = sorted(m.uci() for m in mg.legal_moves(pos))
        assert sorted(mv) == legal, (fen, sorted(mv), legal)
        d = rec["data"]
        print(f"category {cat}  dtz {d.get('dtz')} dtm {d.get('dtm')}  checkmate {d.get('checkmate')} stalemate {d.get('stalemate')}  fetched {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime(rec['fetched']))}")
        for m in d["moves"]:
            print(f"    {m['uci']:6s} {m.get('san',''):8s} -> {m.get('category'):13s} (side to move after the move)  dtz {m.get('dtz')}")
        print()
        res.append({"group": g, "label": lab, "pieces": pc, "stm": stm, "fen": fen, "category": cat,
                    "moves": {m["uci"]: [m.get("san"), m.get("category"), m.get("dtz")] for m in d["moves"]},
                    "fetched": rec["fetched"]})
    json.dump(res, open(f"{V}/logs/tb_results.json", "w"), indent=1)
    print(f"requests in ledger: {PR.ledger_count()}  cache hits this run: {PR.hits}")

if __name__ == "__main__":
    main(sys.argv[1:] or None)
