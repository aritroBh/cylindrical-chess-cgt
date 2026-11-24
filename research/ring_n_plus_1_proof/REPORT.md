# T65: proof note — a ring *2 with n+1 pawns on every C_n, n >= 9

## 5-line summary
1. Theorem: in the whole-board game on C_n (race rule "count", e.p. on, an e.p.-capturable pawn is not passed), for every n>=9 the (n+1)-pawn ring N1_n is *2.
2. Odd n use c=6, n0=19 (2404 reduced nodes); even n use c=4, n0=18 (435 reduced nodes); both satisfy T50's insertion lemmas.
3. Base cases n=9..17 (odd) and 10..16 (even) were checked by direct search; E ran both parities to n=25, all NNPNN.
4. Three programs (rg, myeng, codex engine) agree on the reduced graphs and base cases; sensitivity controls fail when the arc reaches the zone.
5. Full details and commands are in PROOF_N1.md; scope is the whole-board game with race rule "count" only.

## What was produced
- `check_N1.py` (reduced-graph, Lemma 2, Lemma 3, sensitivity checks for both parities)
- `base_N1.py` (direct unreduced search, both parities, n up to 25)
- `base_codex.py` (third program, n=9..14)
- `PROOF_N1.md` (proof note in PROOF_odd.md format)
- logs in `logs/`

## Key numbers
- Odd N1_19: 2404 nodes, 7067 K-moves, 3348 T-moves, zone {0,1,12..17}, signature NNPNN.
- Even N1_18: 435 nodes, 1118 K-moves, 404 T-moves, zone {10..15}, signature NNPNN.
- All base cases n=9..25 (odd) and 10..25 (even): NNPNN under both e.p.-across-heap readings.
- Sensitivity: Lemma 3 fails at 2975/4808 (odd, c=11) and 595/870 (even, c=9).

## Reproduce
- `PYTHONPATH=. nice -n 15 .venv/bin/python research/ring_n_plus_1_proof/check_N1.py N1 19 6`
- `PYTHONPATH=. nice -n 15 .venv/bin/python research/ring_n_plus_1_proof/check_N1.py N1even 18 4`
- `PYTHONPATH=. nice -n 15 .venv/bin/python research/ring_n_plus_1_proof/base_N1.py 25`
- `PYTHONPATH=. nice -n 15 .venv/bin/python research/ring_n_plus_1_proof/base_codex.py 14`
- pump logs: `research/ring_n_plus_2_proof/pump_verify.py N1odd 9 41` and `N1even 10 40`
