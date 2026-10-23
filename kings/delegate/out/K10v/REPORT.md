> **Integrator note (2026-10-22).** Codex was out of quota, so this ran on opencode beam-free. The computation
> was reviewed: the checker implements (H1)–(H5) as LOOPY states them, the comparison with kpsolve counts any
> missing or misaligned result as a violation, and its cyl:6×6 count (74,410) equals K10's, from unrelated code. It is
> accepted as CHECKED-2 for the computation. The proof verdict "SOUND" comes without a written derivation, so the
> recommended relabel of the proof to CHECKED-2 was **not** applied. (The targeted case "β to move with an ω pawn at
> ρ(p)+1 beside p" cannot occur at y, since (H1) excludes it; it arises only during play.)

# K10v: independent check of Proposition 2.11

## 5-line summary

1. Re-derived Proposition 2.11 step by step: Steps 0–5 are SOUND, and Corollaries 2.11a and 2.11b hold as stated.
2. Independent checker (own move generator; μ_ω by BFS over G_ω) agrees with cylcgt's `passed` on 2,000 random positions (0 mismatches).
3. Across 119,654 certified (position, side-to-move, beneficiary) instances on cyl:6×6/7×6/8×6 and 6,572 ep-right positions, `kpsolve --frozen` gives 0 violations.
4. Controls work: dropping (H4) gives 80/24/23 violations in the parked layouts; dropping (H2)/(H3) gives 3,277/2,086 violations with random kings; dropping (H5) gives tens of thousands.
5. Recommend upgrading Proposition 2.11, and the (V2) part of P11, from PROVED to CHECKED-2 in the frozen model.

## Proof re-derivation

All of F1–F3, Step 1 (king safety), Step 2 (invariant under β move, ω push, double step, capture into the strip from outside, capture out of the strip, and the e.p. capture offered at y), Step 3 (consequences), Step 4 (every real ω move is a move of G_ω, so k ≥ μ_ω), and Step 5 (timing for both move orders, e = d or d − 1) are **SOUND**. No missing step or counterexample found.

- **Corollary 2.11a vs `_child`:** matches exactly. With mover M and side to move N at the terminal: only M passed → b = M; only N passed → b = N; race under the count rule → b = N iff dp(N) ≤ dp(M), else b = M. This is precisely `_child`'s `RACE_RULE == "count"` branch (and the only-M / only-N cases follow from `value`). The e values are e = d when b = M (opponent moves first) and e = d − 1 when b = N (beneficiary moves first).
- **Corollary 2.11b (cyl:8×6, Ka1 ka6, pawns on c–g):** verified computationally for both colours: (H2) and (H3) hold, and no king stands on p's file. Only the passed front pawn, (H4) and (H5) need checking.

## Independent computation

Checker: `kings/delegate/out/K10v/check.py` (own move generator; μ_ω by BFS over G_ω, including e.p. as the first move only). Self-test: `.venv/bin/python kings/delegate/out/K10v/check.py` gives 0 mismatches against cylcgt's `passed` on 2,000 random positions. kpsolve build: `nice -n 10 cc -O2 -o kings/delegate/out/K10v/kp kings/kpsolve.c -lpthread`.

Run commands (each under 45 minutes, `nice -n 10`):

- `.venv/bin/python kings/delegate/out/K10v/run.py a`
- `.venv/bin/python kings/delegate/out/K10v/run.py b`
- `.venv/bin/python kings/delegate/out/K10v/run.py b_rand`
- `.venv/bin/python kings/delegate/out/K10v/run.py c`
- `.venv/bin/python kings/delegate/out/K10v/ep_targeted.py`

kpsolve invocation used by the scripts: `nice -n 10 kings/delegate/out/K10v/kp --board cyl:WxH --frozen --cap 1 --threads 2 < in.txt > out.txt`.

| Case | Layout | (pos,stm) tested | Certified instances (p) | Certified (pos,stm) | Violations |
|---|---|---|---|---|---|
| (a) | cyl:6×6, Ka1 ka6, pawns c–e, ≤3/side | 86,598 | 91,074 | 74,410 | 0 |
| (b) | cyl:7×6, same, pawns c–f, ≤2/side | 29,586 | 29,140 | 25,260 | 0 |
| (b_rand) | cyl:7×6, same, 20,000 random with 3/side | 20,000 | 23,363 | 17,879 | 0 |
| (c) | cyl:8×6, random legal kings, ≤3 pawns/side, ep included | 10,000 | 2,751 | 2,105 | 0 |
| (ep) | cyl:6×6, Ka1 ka6, pawns c–e, ep rights where legal | 6,572 | 5,716 | — | 0 |

Controls (violations when one hypothesis is dropped):

| Dropped | (a) | (b) | (b_rand) | (c) |
|---|---|---|---|---|
| (H2) | 0 | 0 | 0 | 3,277 |
| (H3) | 0 | 0 | 0 | 2,086 |
| (H4) | 80 | 24 | 23 | 0 |
| (H5) | 71,390 | 27,576 | 17,636 | 551 |

## Targeted search

- **(H4) at its bound** ρ(q) = ρ(p) + 1: 5,248 certified instances across (a)–(c); 0 violations.
- **e.p. right at y:** 6,572 positions, 5,716 certified instances, 0 violations. In 2,356 of these the e.p. captured pawn is a non-p beneficiary pawn; the rest capture an ω pawn. No instance has p itself e.p.-capturable (excluded by (H1)).
- **ω captures entering the strip:** covered by the μ_ω search (all captures, including into the strip); the 0-violation totals above include them.
- **β to move with an ω pawn at ρ(p)+1 beside p:** 0 certified instances in all runs (0 of 119,654 plus ep), so no violation can occur; the condition simply does not arise among certified instances.

## Recommended labels

- **Proposition 2.11:** upgrade from PROVED to **CHECKED-2** (frozen model). Proof re-derivation SOUND and independent computation agrees (0 violations).
- **P11:** upgrade the (V2) certificate part to **CHECKED-2** (frozen model), still conditional on (E) and hereditary sum-safety as before.
