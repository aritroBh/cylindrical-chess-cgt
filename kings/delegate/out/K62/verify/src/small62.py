"""K62 referee: PROOF.md 2.5.2 (no e.p., at most 4 boards => (C)) and 2.5.3 (M2, no checks, no e.p., 5 boards => N* <= 2)
on random exact groups. Usage: .venv/bin/python kings/delegate/out/K62/verify/src/small62.py SEED TRIES"""
import random
import sys
from chk62 import rand_group, analyse, INF

seed, tries = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
for label, b, pchk, m2, claim in (('2.5.2 b=4 no e.p., checks', 4, 0.4, False, 0),
                                   ('2.5.2 b=4 no e.p., no checks', 4, 0.0, False, 0),
                                   ('2.5.3 b=5 M2 no e.p. no checks', 5, 0.0, True, 2),
                                   ('b=5 M2 no e.p. with checks (open in PROOF)', 5, 0.4, True, None)):
    ng = nb = 0
    worst = -1
    for _ in range(tries):
        for reading in ('strict', 'literal'):
            G = rand_group(rng, b, 1, pchk, 0.0, 0.0, rng.choice([0.15, 0.3, 0.5]), reading == 'strict', m2,
                           bias=rng.random() < 0.5)
            if G is None:
                continue
            res, _ = analyse(G, reading, m2)
            if res is None:
                continue
            ng += 1
            for r in res['rows']:
                nb += 1
                if r['Nstar'] < INF:
                    worst = max(worst, r['Nstar'])
                    if claim is not None and r['Nstar'] > claim:
                        print('COUNTEREXAMPLE', label, r, G.mv, G.chk)
            assert not res['viol'], res['viol']
    print('%s: %d exact groups, %d bad moves, largest finite N* = %s (claim: %s)'
          % (label, ng, nb, worst if worst >= 0 else 'none (all satisfy (C))', 'none' if claim == 0 else claim))
