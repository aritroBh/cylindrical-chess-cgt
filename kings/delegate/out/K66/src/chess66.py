"""K66: Definition 4.8 in chess, from Syzygy answers (Lichess tablebase), written by the K66 checker.

Run from the repository root with  python3 -B kings/delegate/out/K66/src/chess66.py [--online N]
Reads tablebase records through realchess.probe.Prober (cache only by default; the K65 referee's cache, unpacked
into kings/delegate/out/K66/work/tbcache, and the K66 cache kings/delegate/out/K66/work/tbcache66 for fresh lookups).

Reading of Definition 4.8 with chess values ("a move loses at once" = the position after it is lost, by the
tablebase, for the side that made it):
 (O0) no king in check at the four roots and at the q's;
 (O1) at both roots, Black to move: the shuttle is legal and every other Black move loses (White to move wins);
 (O2) at both roots, White to move: at least one White move does not lose (a freeze);
 (O3) for EVERY freeze: q, Black to move (with the e.p. right if the freeze is a double step), has a move and every
      Black move loses;
 (O4) the same q, White to move, no right: has a move and every White move loses.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
K66 = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(K66, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
from realchess.probe import Prober, CapReached  # noqa: E402

GROUPS = [
    ("C125_01", "Ke5 kg4/kg5 Pb3 Pf2 pb4 pf5"),
    ("C125_02", "Kc5 ka4/ka5 Pb2 Pf3 pb5 pf4"),
    ("C125_04", "Ka5 kc5/kc6 Pb2 Pf6 pb7 pf7"),
    ("C125_05", "Kd4 kb4/kb5 Pb6 Pc2 Pc5 pb7 pc6"),
    ("C125_08", "Ke5 kc5/kc6 Pb2 Pb6 Pf6 pb7 pf7"),
    ("C125_09", "Kc4 ke4/ke5 Pb5 Pf2 Pf6 pb6 pf7"),
    ("C125_10", "Kc5 ke5/ke6 Pb6 Pf2 Pf6 pb7 pf7"),
    ("C125_11", "Kg5 ke5/ke6 Pc5 Pf2 Pf6 pb7 pf7"),
    ("C125_12", "Ka4 kc4/kc5 Pb2 Pf3 Pf4 pb6 pf5"),
    ("C125_13", "Kf6 ke8/kf8 Pc5 Pf2 pb7 pc6 pf7"),
    ("C145_07", "Kg4 ke4/ke5 Pe6 Pf2 Pf5 pe7 pf6"),
    ("C145_09", "Kd4 kf4/kf5 Pe2 Pe5 Pf6 pe6 pf7"),
    ("C145_13", "Ka5 kc5/kc6 Pb2 Pe5 Pe6 pb7 pe7"),
    ("C145_15", "Ka4 kc4/kc5 Pb2 Pf3 Pf4 pb6 pe6"),
    ("C145_16", "Kb6 kb8/kc8 Pb2 Pe5 pb7 pe6 pf7"),
]


def sq(n):
    return 8 * (int(n[1]) - 1) + "abcdefgh".index(n[0])


def sqn(s):
    return "abcdefgh"[s % 8] + str(s // 8 + 1)


def parse(spec):
    wk = None; bks = []; wp = set(); bp = set()
    for t in spec.split():
        if t[0] == "K": wk = sq(t[1:3])
        elif t[0] == "k": bks = [sq(x.lstrip("k")) for x in t[1:].split("/")]
        elif t[0] == "P": wp.add(sq(t[1:3]))
        elif t[0] == "p": bp.add(sq(t[1:3]))
    return wk, bks, wp, bp


def fen(wk, bk, wp, bp, stm, ep=None):
    board = {wk: "K", bk: "k"}
    for s in wp: board[s] = "P"
    for s in bp: board[s] = "p"
    rows = []
    for r in range(7, -1, -1):
        row, e = "", 0
        for f in range(8):
            p = board.get(8 * r + f)
            if p is None: e += 1
            else:
                if e: row += str(e); e = 0
                row += p
        if e: row += str(e)
        rows.append(row)
    return "/".join(rows) + f" {stm} - {sqn(ep) if ep is not None else '-'} 0 1"


def attacked_by_white_pawns(s, wp):
    return any(p + 8 + d == s and abs((p % 8) - (s % 8)) == 1 for p in wp for d in (-1, 1))


def attacked_by_black_pawns(s, bp):
    return any(p - 8 + d == s and abs((p % 8) - (s % 8)) == 1 for p in bp for d in (-1, 1))


def apply_white(uci, wk, wp, bp):
    a, b = sq(uci[0:2]), sq(uci[2:4])
    wp, bp = set(wp), set(bp)
    ep = None
    if a == wk:
        wk = b; bp.discard(b)
    else:
        wp.discard(a); wp.add(b); bp.discard(b)
        if b - a == 16: ep = a + 8
    return wk, wp, bp, ep


class TB:
    def __init__(self, online_cap):
        self.old = Prober(0, os.path.join(K66, "work", "ledger_unused.jsonl"), os.path.join(K66, "work", "tbcache"),
                          tag="K66", offline=True)
        self.new = Prober(online_cap, os.path.join(K66, "tb_ledger.jsonl"), os.path.join(K66, "work", "tbcache66"),
                          tag="K66", offline=(online_cap == 0))
        self.missing = []
        self.used = []

    def get(self, f, fresh=False):
        rec = None if fresh else self.old.cached(f)
        src = "K65 cache"
        if rec is None:
            rec = self.new.cached(f); src = "K66 lookup"   # never the network here; fresh lookups only in --fresh
            if rec is None or rec.get("data") is None:
                self.missing.append(f); return None, None
        self.used.append((f, src))
        d = rec["data"]
        return d["category"], {m["uci"]: m["category"] for m in d["moves"]}


def main():
    online = 0
    if "--online" in sys.argv: online = int(sys.argv[sys.argv.index("--online") + 1])
    tb = TB(online)
    out = []
    cats = set()
    for name, spec in GROUPS:
        wk, bks, wp, bp = parse(spec)
        fails = []
        fens = {}
        okall = True
        for i, bk in enumerate(bks):
            other = bks[1 - i]
            if attacked_by_white_pawns(bk, wp) or attacked_by_black_pawns(wk, bp):
                fails.append(f"(O0) check at root k{sqn(bk)}")
            fb = fen(wk, bk, wp, bp, "b"); fw = fen(wk, bk, wp, bp, "w")
            fens[f"root k{sqn(bk)} b"] = fb; fens[f"root k{sqn(bk)} w"] = fw
            cb, mb = tb.get(fb); cw, mw = tb.get(fw)
            if mb is None or mw is None: okall = False; continue
            cats.update([cb, cw]); cats.update(mb.values()); cats.update(mw.values())
            sh = sqn(bk) + sqn(other)
            if sh not in mb: fails.append(f"(O1) shuttle illegal at k{sqn(bk)}")
            bad = [u for u, c in mb.items() if u != sh and c != "win"]
            if bad: fails.append(f"(O1) at k{sqn(bk)}: " + ", ".join(f"...{u} {mb[u]}" for u in bad))
            freezes = [u for u, c in mw.items() if c != "win"]
            if not freezes: fails.append(f"(O2) no freeze at k{sqn(bk)} (root, White to move: {cw})")
            for u in freezes:
                nwk, nwp, nbp, ep = apply_white(u, wk, wp, bp)
                if ep is not None and not any(abs((p % 8) - (ep % 8)) == 1 and p // 8 == 3 for p in nbp): ep = None
                qb = fen(nwk, bk, nwp, nbp, "b", ep); qw = fen(nwk, bk, nwp, nbp, "w")
                fens[f"q {u} at k{sqn(bk)} b"] = qb; fens[f"q {u} at k{sqn(bk)} w"] = qw
                if attacked_by_white_pawns(bk, nwp) or attacked_by_black_pawns(nwk, nbp):
                    fails.append(f"(O0) check at q after {u}")
                if u[0:2] == sqn(wk) and tb.old.cached(qw) is None and tb.new.cached(qw) is None:
                    # king freeze, q not cached: in q, White to move, the king can step back to the root square
                    # (legal: it was legal there), reaching the root with Black to move; that move loses only if
                    # the root, Black to move, is a Black win.
                    if cb != "loss" and cb != "draw":
                        okall = False; continue
                    fails.append(f"(O4) q after {u} (k{sqn(bk)}), White to move: K{u[2:4]}-{u[0:2]} back to the root "
                                 f"does not lose (root, Black to move: {cb}) [deduced, q not probed]")
                    continue
                cqb, mqb = tb.get(qb); cqw, mqw = tb.get(qw)
                if mqb is None or mqw is None: okall = False; continue
                cats.update([cqb, cqw]); cats.update(mqb.values()); cats.update(mqw.values())
                if not mqb or any(c != "win" for c in mqb.values()):
                    fails.append(f"(O3) q after {u} (k{sqn(bk)}), Black to move: {cqb}")
                if not mqw or any(c != "win" for c in mqw.values()):
                    fails.append(f"(O4) q after {u} (k{sqn(bk)}), White to move: {cqw}")
            fens[f"freezes at k{sqn(bk)}"] = " ".join(f"{u}({mw[u]})" for u in freezes)
        verdict = "no" if fails else ("YES" if okall else "INCOMPLETE")
        out.append({"group": name, "spec": spec, "verdict": verdict, "fails": fails, "fens": fens})
    for r in out:
        print(f"{r['group']} {r['spec']}: {r['verdict']}")
        for f in r["fails"]: print("   ", f)
        for k, v in r["fens"].items(): print(f"      {k}: {v}")
    print("categories seen:", sorted(c for c in cats if c))
    print("records used:", len(tb.used), "distinct", len(set(f for f, _ in tb.used)),
          "fresh lookups:", sum(1 for _, s in tb.used if s == "K66 lookup"))
    if "--fresh" in sys.argv:
        # spot-check: fresh lookups (own cache and ledger) of cached answers for the YES groups
        picks = []
        for r in out:
            if r["verdict"] != "YES": continue
            ks = list(r["fens"].keys())
            roots = [k for k in ks if k.startswith("root")]
            qs = [k for k in ks if k.startswith("q ")]
            sel = [roots[0], roots[1]] + qs[:2] + [qs[-1]]
            picks += [r["fens"][k] for k in sel]
        picks = picks[:max(0, tb.new.remaining())]
        agree = 0
        for f in picks:
            old = tb.old.cached(f)
            new = tb.new.probe(f)
            co, mo = old["data"]["category"], {m["uci"]: m["category"] for m in old["data"]["moves"]}
            cn, mn = new["data"]["category"], {m["uci"]: m["category"] for m in new["data"]["moves"]}
            same = (co == cn and mo == mn)
            agree += same
            print(f"fresh {'agree' if same else 'DIFFER'}: {f}  {cn} ({len(mn)} moves)")
        print(f"fresh lookups: {len(picks)}, agree {agree}; ledger entries {tb.new.ledger_count()}")
    if tb.missing:
        print("MISSING (not cached):")
        for f in dict.fromkeys(tb.missing): print("   ", f)


if __name__ == "__main__":
    main()
