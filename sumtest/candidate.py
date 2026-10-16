"""Part 2(a): outcomes of G, G+*, G+*2, G+*3 for the *2 candidate.

G = W a2 c2 / B b7 d7 on a 4-file flat board, 8 ranks.
G = *2 exactly iff G + *2 is P.

  PYTHONPATH=. .venv/bin/python -m sumtest.candidate
"""
import sys

from sumtest.sumsolver import REF_NAMES, Geometry, Rules, SumSolver, Trees, reference_set

POS = "W: a2 c2 / B: b7 d7"
EPV = [("off", False, True, "component"),
       ("on, plain passer, e.p. right local to G", True, False, "component"),
       ("on, plain passer, e.p. right expires on any move", True, False, "global"),
       ("on, e.p.-aware passer, local", True, True, "component"),
       ("on, e.p.-aware passer, expires on any move", True, True, "global")]


def star2_vector():
    """Outcome classes of *2 + X for every reference X (from the solver, G = 0)."""
    T = Trees()
    ref = reference_set(T)
    sums = {n: T.add(ref["*2"], ref[n]) for n in REF_NAMES}
    s = SumSolver(Rules(Geometry(1, False)), T)
    wl, wr = s.solve((0, 0, -1))
    return "".join(s.outcome(wl, wr, sums[n]) for n in REF_NAMES)


def main(pos=POS, files=4, wrap=False):
    target = star2_vector()
    print(f"Position {pos}, {files} files, {'cylinder' if wrap else 'flat'}, 8 ranks")
    print("Reference order:", " ".join(REF_NAMES))
    print(f"*2 + X vector    : {target}")
    print()
    print("| race rule | en passant | mode | G | G+* | G+*2 | G+*3 | G = *2 ? | full vector | equals *2's vector | race nodes | states |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for rule in ("count", "mover", "opponent"):
        for name, ep, aware, scope in EPV:
            for mode in ("whole", "comp"):
                if mode == "comp" and scope == "global":
                    continue
                geo = Geometry(files, wrap)
                T = Trees()
                ref = reference_set(T)
                s = SumSolver(Rules(geo, ep=ep, ep_aware=aware, race_rule=rule), T, mode=mode, ep_scope=scope)
                W, B = geo.parse(pos)
                wl, wr = s.solve(s.start_state(W, B))
                vec = "".join(s.outcome(wl, wr, ref[n]) for n in REF_NAMES)
                o = {n: s.outcome(wl, wr, ref[n]) for n in REF_NAMES}
                print(f"| {rule} | {name} | {mode} | {o['0']} | {o['*']} | {o['*2']} | {o['*3']} | "
                      f"{'yes' if o['*2'] == 'P' else 'no'} | {vec} | {'yes' if vec == target else 'no'} | "
                      f"{s.rules.race_hits} | {s.nodes} |")


if __name__ == "__main__":
    main()
