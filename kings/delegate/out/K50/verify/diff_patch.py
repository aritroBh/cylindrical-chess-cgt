"""K50 referee: original vs patched embed_check (strict) on two-component contexts with double-step chances, beside
groups whose bare data allow the Proposition 2.11 route. Prints every position where a verdict or the (V2) passer
clause differs. Run from the project root: python3 .../diff_patch.py <jobs_random.json> <n_per_group> <seed>"""
import importlib.util
import json
import os
import random
import sys

sys.path.insert(0, os.getcwd())
import kings.embed_check as O  # noqa: E402

spec = importlib.util.spec_from_file_location("pe", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                 "patched", "kings", "embed_check.py"))
Pm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Pm)

jobs = json.load(open(sys.argv[1]))
n, seed = int(sys.argv[2]), int(sys.argv[3])
rnd = random.Random(seed)
tot = diff = cert = 0
for bd, fz, gid, grp, cf in jobs:
    kind, size = bd.split(":")
    W, H = map(int, size.split("x"))
    files0 = [O.FILES.index(c) for c in cf]
    co = O.Checker(O.Board(W, H, kind == "cyl"), 6, 300000, False, 20)
    cp = Pm.Checker(Pm.Board(W, H, kind == "cyl"), 6, 300000, False, 20)
    for _ in range(n):
        files = list(files0)
        toks = []
        used = set()
        if os.environ.get("TARGET"):  # comp A: an o pawn on its start rank, an s pawn beside its landing square
            fa, fb = files[0], files[1]
            o = rnd.choice("Pp")
            if o == "P":
                toks += [f"P{O.FILES[fa]}2", f"p{O.FILES[fb]}4"]; used |= {(fa, 2), (fb, 4)}
            else:
                toks += [f"p{O.FILES[fa]}{H - 1}", f"P{O.FILES[fb]}{H - 3}"]; used |= {(fa, H - 1), (fb, H - 3)}
            files = files[3:] if len(files) > 3 else files[-1:]
        for f in files:
            if rnd.random() < 0.3:
                continue
            for _ in range(rnd.randint(1, 2)):
                c = rnd.choice("Pp")
                r = rnd.choice([2, 2, H - 1, H - 1, 3, 4, H - 2])
                if (f, r) in used:
                    continue
                used.add((f, r))
                toks.append(f"{c}{O.FILES[f]}{r}")
        if not toks:
            continue
        for stm in "wb":
            txt = f"{grp} {' '.join(toks)} {stm} -"
            try:
                a = co.run(txt, fz)
                b = cp.run(txt, fz)
            except Exception as e:  # noqa: BLE001
                print(json.dumps({"pos": txt, "err": repr(e)}))
                continue
            tot += 1
            va = (a["verdict"], json.dumps(a.get("V2", {}).get("passer_and_race_terminals", {}).get("verdict")),
                  json.dumps(a.get("sharp_form", {}).get("parts")))
            vb = (b["verdict"], json.dumps(b.get("V2", {}).get("passer_and_race_terminals", {}).get("verdict")),
                  json.dumps(b.get("sharp_form", {}).get("parts")))
            cert += a["verdict"] == "CERTIFIED"
            if va != vb:
                diff += 1
                print(json.dumps({"board": bd, "fz": fz, "pos": txt, "orig": va, "patched": vb}), flush=True)
print("TOTAL", tot, "orig CERTIFIED", cert, "differ", diff)
