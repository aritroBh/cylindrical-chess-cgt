"""Rerun of sumtest comparison with the engine's passed-pawn flag selectable.
Imports solver/enumeration/ref_games from the local copies. Writes only under data/ and logs/.
Engine settings: aware (ep on, PASSED_RESPECTS_EP=True), textbook (ep on, flag False), off (ep off).
Solver variants: aware/aware-global/plain/plain-global/off x whole/comp (global only whole).
"""
import gzip, json, os, sys, time
from multiprocessing import Pool
import enum_positions as E
from enum_positions import BOARDS, positions, OUT
from sumsolver import REF_NAMES
from compare_cylcgt import ref_games

RULES = ("count", "mover", "opponent")
ENG = {"aware": (True, True), "textbook": (True, False), "off": (False, True)}  # (board ep, flag)

def eng_path(b, r, e): return os.path.join(OUT, f"eng__{b}__{r}__{e}.json.gz")

def run_eng(t):
    b, r, e = t
    p = eng_path(b, r, e)
    if os.path.exists(p): return p
    from cylcgt import cgt, pawns
    ep, flag = ENG[e]
    pawns.PASSED_RESPECTS_EP = flag
    pawns.RACE_RULE = r
    pawns._value.cache_clear()
    files, wrap = BOARDS[b]
    geo, pos = positions(files, wrap)
    board = pawns.Board(files, 8, wrap, ep)
    R = ref_games(); res = {}; info = {}
    for W, B in pos:
        text = geo.show(W, B)
        v = pawns.value(board, pawns.Pos.parse(text))
        res[text] = "".join(cgt.outcome(cgt.add(v, R[n])) for n in REF_NAMES)
        info[text] = cgt.show(v)
    with gzip.open(p + ".tmp", "wt") as fh: json.dump({"flag": pawns.PASSED_RESPECTS_EP, "outcomes": res, "value": info}, fh)
    os.replace(p + ".tmp", p)
    return p

def run_mine(t):
    b, r, v, m = t
    return E.run(b, r, v, m)

def load(p):
    with gzip.open(p, "rt") as fh: return json.load(fh)

# (row label, engine setting, solver epv, modes)
ROWS = [("aware/aware", "aware", "aware", ("whole", "comp")),
        ("aware/aware-global", "aware", "aware-global", ("whole",)),
        ("textbook/plain (control)", "textbook", "plain", ("whole", "comp")),
        ("textbook/plain-global (control)", "textbook", "plain-global", ("whole",)),
        ("ep-off (control)", "off", "off", ("whole", "comp")),
        ("aware engine vs plain solver (expected mismatch, as old run)", "aware", "plain", ("whole",)),
        ("textbook engine vs aware solver (expected mismatch)", "textbook", "aware", ("whole",))]

def main():
    jobs = 2
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    with Pool(jobs) as p:
        et = [(b, r, e) for b in BOARDS for r in RULES for e in ENG]
        for x in p.imap_unordered(run_eng, et): print("eng", x, round(time.time()-t0), flush=True)
        mt = sorted({(b, r, v, m) for b in BOARDS for r in RULES for (_, _, v, ms) in ROWS for m in ms},
                    key=lambda t: -BOARDS[t[0]][0])
        for x in p.imap_unordered(run_mine, mt): print("mine", x[0] if x else None, round(time.time()-t0), flush=True)
    out = {}
    print("\n| row | solver mode | cases | pairs | cases differing | pairs differing |\n|---|---|---|---|---|---|")
    first = {}
    for label, e, v, ms in ROWS:
        for m in ms:
            cases = pairs = dc = dp = 0
            for b in BOARDS:
                for r in RULES:
                    eng = load(eng_path(b, r, e))["outcomes"]
                    mine = load(os.path.join(OUT, f"mine__{b}__{r}__{v}__{m}.json.gz"))["outcomes"]
                    assert set(eng) == set(mine)
                    for k in mine:
                        cases += 1; pairs += len(mine[k])
                        if mine[k] != eng[k]:
                            dc += 1; dp += sum(x != y for x, y in zip(mine[k], eng[k]))
                            first.setdefault((label, m, r), []).append((len(k.replace("W:", "").replace("B:", "").replace("/", " ").split()), b, k))
            print(f"| {label} | {m} | {cases:,} | {pairs:,} | {dc:,} | {dp:,} |", flush=True)
    print("\nsmallest differing positions (pawn count, board, text) per row/mode/rule, only for non-zero rows:")
    for key, lst in sorted(first.items()):
        if key[0].startswith(("aware/", "textbook/", "ep-off")):
            print(key, "ndiff", len(lst), "smallest", sorted(lst)[:3])
    print("wall seconds", round(time.time() - t0))

if __name__ == "__main__":
    main()
