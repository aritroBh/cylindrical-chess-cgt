"""Stand-alone spot check (does not import identities.py): five hand-built cells + one negative control.
Run: PYTHONPATH=. .venv/bin/python kings/delegate/out/K5b/spotcheck.py"""
from sumtest.sumsolver import Geometry, Rules, SumSolver, Trees

def outcome(geo, rules, pos, build, mode):
    T = Trees()
    k = T.neg(build(T))                       # G + (-V)
    s = SumSolver(rules, T, mode=mode, ep_scope="component")
    W, B = geo.parse(pos)
    wl, wr = s.solve(s.start_state(W, B))
    return SumSolver.outcome(wl, wr, k)

def num(T, n):
    return T.node([num(T, n - 1)], []) if n > 0 else T.node()
def dy(T, d):                                  # 1/2^d
    v = num(T, 1)
    for _ in range(d):
        v = T.node([T.node()], [v])
    return v
def star(T):
    z = T.node(); return T.node([z], [z])
def star2(T):
    z = T.node(); s = star(T); return T.node([z, s], [z, s])
def tiny1(T):
    z = T.node(); return T.node([z], [T.node([z], [T.node([], [z])])])
def neg_num(T, n):                             # -n = { | -n+1}
    return T.node([], [neg_num(T, n - 1)]) if n > 0 else T.node()
def sw(T):                                     # {{3|1} | {-1|-3}}
    return T.node([T.node([num(T, 3)], [num(T, 1)])],
                  [T.node([neg_num(T, 1)], [neg_num(T, 3)])])

flat, cyl = Geometry(8, False), Geometry(3, True)
aware = lambda g: Rules(g, ep=True, ep_aware=True, race_rule="count")
cells = [
    ("T1 1/8", flat, aware(flat), "W: a2 a3 b2 / B: a6 b5 b6", lambda T: dy(T, 3), "P"),
    ("T4 1/16", flat, aware(flat), "W: a2 b2 c3 / B: b5 b6 c7", lambda T: dy(T, 4), "P"),
    ("T7 tiny(1)", flat, aware(flat), "W: a2 b2 b6 / B: a6 b7 c6", tiny1, "P"),
    ("T8 {2+-1|-2+-1}", flat, aware(flat), "W: a2 c2 / B: b7 d7", sw, "P"),
    ("T9 *2 (cyl 3x8)", cyl, aware(cyl), "W: a2 a3 b2 / B: b7 c6 c7", star2, "P"),
    ("negative: T1 vs 1/16", flat, aware(flat), "W: a2 a3 b2 / B: a6 b5 b6", lambda T: dy(T, 4), "L"),
]
ok = True
for name, g, r, pos, b, exp in cells:
    got = [outcome(g, r, pos, b, m) for m in ("whole", "comp")]
    good = got == [exp, exp]
    ok &= good
    print(f"{'PASS' if good else 'FAIL'} {name}: whole={got[0]} comp={got[1]} (expected {exp})")
raise SystemExit(0 if ok else 1)
