# T1: independent Codex verification of the pawn-game headlines

## Summary

1. **AGREE — CHECKED-2:** (a) textbook e.p. gives `*2` for count/mover and `0` for opponent, with e.p. on or off.
2. **AGREE — CHECKED-2:** (b) e.p.-aware with e.p. on gives `{2±1|-2±1}` for count and mover.
3. **AGREE — CHECKED-2:** (c) no `*k`, `k >= 2`, was found; the independent nimber test covered every candidate through `k=292`.
4. **AGREE — CHECKED-2:** (d) the first position is `1/8` in all nine race/e.p. settings.
5. **AGREE — CHECKED-2:** (e) the second position is `{0,*|↓}` in all nine race/e.p. settings.

## Claim-by-claim evidence

| Claim | Verdict | Evidence | Reproduce from project root |
|---|---|---|---|
| (a) `W a2 c2 / B b7 d7` | **AGREE — CHECKED-2** | Count: `*2` with e.p. off/on. Mover: `*2` with e.p. off/on. Opponent: `0` with e.p. off/on. All six values match the existing result. | `PYTHONPATH=. .venv/bin/python verify_ext/codex/selfcheck.py` |
| (b) Same position, e.p.-aware and e.p. on | **AGREE — CHECKED-2** | Count and mover both canonicalize to `{2±1|-2±1}`. | `PYTHONPATH=. .venv/bin/python verify_ext/codex/selfcheck.py` |
| (c) No `*k`, `k >= 2`, in scope | **AGREE — CHECKED-2** | Zero second-player-win hits for `G+*k`, for every tested root and `k=2..292`. The unquotiented root counts were width 1: 179; width 2: 17,239; width 3: 158,219; width 4: 617,662; total: **793,299** (**COMPUTED-1** count). The existing full-form census also reports no such nimber. Its separate nimber-only cross-check covered `k<=4`; this run extends the nimber test through the short-game birthday bound. | `PYTHONPATH=. .venv/bin/python verify_ext/codex/solver.py census` |
| (d) `W a2 a3 b2 / B a6 b5 b6` | **AGREE — CHECKED-2** | `1/8` for each race rule (`count`, `mover`, `opponent`) under e.p. off, textbook with e.p. on, and e.p.-aware with e.p. on: all nine settings. | `PYTHONPATH=. .venv/bin/python verify_ext/codex/selfcheck.py` |
| (e) `W a2 b2 b6 / B a6 b7 c5` | **AGREE — CHECKED-2** | `{0,*|↓}` for the same nine settings. | `PYTHONPATH=. .venv/bin/python verify_ext/codex/selfcheck.py` |

For (c), the `292` bound is **PROVED** from this model's move graph: at most six pawns can each advance at most six ranks (36 pawn moves total), after which a one-sided passer is the terminal value `±256`, whose birthday is 256. Thus the root game's birthday is at most `36+256=292`; a nimber `*k` has birthday `k`. The test covers every possible nimber size in that bound.

The `793,299` count is for every labeled placement on each listed width. It does not quotient mirror images, translations, or positions embedded in a wider board with empty edge files. The project atlas reports 231,071 canonical records standing for 459,443 positions after requiring occupied edge files and reducing mirrors. The present enumeration is broader; these count conventions explain the denominator difference.

## Implementation and reproduction

`solver.py` is a stdlib-only implementation written for this task. It generates pawn single steps, home-rank double steps, captures, and en passant; evaluates textbook and e.p.-aware passed pawns; resolves all three race rules; and recursively builds canonical short games by removing dominated and reversible options. It searches complete boards directly and does not import code from `cylcgt/`, `sumtest/`, `lemmas/`, `crosscheck/`, or `atlas/`.

The nine settings are the three race rules crossed with: e.p. disabled; textbook passed test with e.p. enabled; e.p.-aware passed test with e.p. enabled. Count compares minimum promotion moves, using a legal home-rank double step where available and breaking ties for the next mover. The mover/opponent rules use the last pawn mover. A double step sets an e.p. target in its child state; every next move clears that target unless it is another double step.

The final headline self-check reported 27 passes (26 setting checks plus a check that the outcome-vector routine recognizes the textbook candidate as `*2` exactly at `G+*2`). Its exact command is:

```sh
PYTHONPATH=. .venv/bin/python verify_ext/codex/selfcheck.py
```

The exhaustive claim (c) command is:

```sh
PYTHONPATH=. .venv/bin/python verify_ext/codex/solver.py census
```

The full headline output is also available from:

```sh
PYTHONPATH=. .venv/bin/python verify_ext/codex/solver.py headlines
```
