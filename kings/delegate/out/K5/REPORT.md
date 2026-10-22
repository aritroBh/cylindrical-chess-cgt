# K5 — independent check of cylcgt's canonical forms

## Summary (5 lines)

1. Wrote an independent short-game engine (`canon.py`) from textbook definitions (Siegel; BCG Winning Ways) with
   its own canonical-form, <=, negation, sum, number, nimber and show code; it does not import `cylcgt.cgt`.
2. `test_canon.py` passes: 10/10 (star+star=0, up+down=0, 1/2+1/2=1, *2+*2=0, up+* fuzzy 0, up^2 between 0
   and up, up^2+* = {0,* | down}, tiny(1)>0, 1/8={0|1/4}, self-negating G+G=0).
3. Ran all 9 targets x 9 settings (81 cases): V_own agrees with converted V_cyl in every case (CHECKED-2);
   no RaceError was raised by either engine.
4. Claimed values verified where a claim exists: 1/8 (T1,T2 all; T3 aware count), 1/16 (T4 aware count),
   up^2 (T5 aware count), up^2* (T6 all), tiny(1) (T7 aware count), *2/0/{2+-1 | -2+-1} (T8 as claimed),
   *2 (T9 aware count). T9 off/textbook and non-count settings are not claimed and differ.
5. No disagreement between the two engines was found, so no game-tree descent was needed; tiny(1) is < both up
   and up^2 (COMPUTED-1), and up^2+* = {0,* | down} holds (CHECKED-2 by construction).

## Pytest result

```
$ PYTHONPATH=. .venv/bin/python -m pytest kings/delegate/out/K5/test_canon.py -q
..........                                                               [100%]
10 passed in 0.06s
```

Reproduce: `bash kings/delegate/out/K5/run.sh`.

## Tiny(1) comparisons (COMPUTED-1)

`test_tiny1` printed:
- `tiny vs UP: le(tiny,UP)= True le(UP,tiny)= False`  => tiny(1) < up
- `tiny vs up2: le(tiny,up2)= True le(up2,tiny)= False` => tiny(1) < up^2

## 9 x 9 table

V_own printed form (BIG values print as +-W). `cyl` = equals converted cylcgt value (all yes). `claim` =
equals the claimed value for that setting (yes / no claim). Full machine-readable table in `targets.tsv`.

### Target 1 — flat 8x8, `W: a2 a3 b2 / B: a6 b5 b6`

| ep \ race | count | mover | opponent |
|---|---|---|---|
| off | 1/8 (yes, yes) | 1/8 (yes, yes) | 1/8 (yes, yes) |
| textbook | 1/8 (yes, yes) | 1/8 (yes, yes) | 1/8 (yes, yes) |
| aware | 1/8 (yes, yes) | 1/8 (yes, yes) | 1/8 (yes, yes) |

### Target 2 — flat 8x8, `W: a2 b2 b3 / B: a5 a6 b6`

| ep \ race | count | mover | opponent |
|---|---|---|---|
| off | 1/8 (yes, yes) | 1/8 (yes, yes) | 1/8 (yes, yes) |
| textbook | 1/8 (yes, yes) | 1/8 (yes, yes) | 1/8 (yes, yes) |
| aware | 1/8 (yes, yes) | 1/8 (yes, yes) | 1/8 (yes, yes) |

### Target 3 — flat 8x8, `W: a2 b4 c4 / B: a7 b7 d6`

| ep \ race | count | mover | opponent |
|---|---|---|---|
| off | 1/8 (yes, no claim) | {0 | {-W, {+W | -W, +-+W} | -W}} (yes, no claim) | * (yes, no claim) |
| textbook | 1/8 (yes, no claim) | {0 | {-W, {+W | -W, +-+W} | -W}} (yes, no claim) | * (yes, no claim) |
| aware | 1/8 (yes, yes) | {0 | {-W, {+W | -W, +-+W} | -W}} (yes, no claim) | * (yes, no claim) |

### Target 4 — flat 8x8, `W: a2 b2 c3 / B: b5 b6 c7`

| ep \ race | count | mover | opponent |
|---|---|---|---|
| off | 1/2 (yes, no claim) | 3/4 (yes, no claim) | 1/2 (yes, no claim) |
| textbook | 1/16 (yes, no claim) | 1/16 (yes, no claim) | 1/8 (yes, no claim) |
| aware | 1/16 (yes, yes) | 1/16 (yes, no claim) | 1/8 (yes, no claim) |

### Target 5 — flat 8x8, `W: a2 b2 d4 / B: a7 c6 d7`

| ep \ race | count | mover | opponent |
|---|---|---|---|
| off | {0 | {0 | {0, * | {down, {+W | down} | -W}}}} (yes, no claim) | {0, down* | 0, {0, {{+W | +W, {+W | +W, +-+W}} | -W} | -W}} (yes, no claim) | {1 | {1 | {*, {+W | *} | -W, {-W, +-+W, {-W, +-+W | -W} | -W}}}} (yes, no claim) |
| textbook | {0 | down*} (yes, no claim) | {0, down* | 0, {0, {{+W | +W, {+W | +W, +-+W}} | -W} | -W}} (yes, no claim) | {1 | {1 | {*, {+W | *} | -W, {-W, +-+W, {-W, +-+W | -W} | -W}}}} (yes, no claim) |
| aware | {0 | down*} (yes, yes) | * (yes, no claim) | {1 | {1 | {*, {+W | *} | -W, {-W, +-+W, {-W, +-+W | -W} | -W}}}} (yes, no claim) |

### Target 6 — flat 8x8, `W: a2 b2 b6 / B: a6 b7 c5`

| ep \ race | count | mover | opponent |
|---|---|---|---|
| off | {0, * | down} (yes, yes) | {0, * | down} (yes, yes) | {0, * | down} (yes, yes) |
| textbook | {0, * | down} (yes, yes) | {0, * | down} (yes, yes) | {0, * | down} (yes, yes) |
| aware | {0, * | down} (yes, yes) | {0, * | down} (yes, yes) | {0, * | down} (yes, yes) |

### Target 7 — flat 8x8, `W: a2 b2 b6 / B: a6 b7 c6`

| ep \ race | count | mover | opponent |
|---|---|---|---|
| off | up (yes, no claim) | up (yes, no claim) | up (yes, no claim) |
| textbook | tiny(1) (yes, no claim) | tiny(1) (yes, no claim) | tiny(1) (yes, no claim) |
| aware | tiny(1) (yes, yes) | tiny(1) (yes, no claim) | tiny(1) (yes, no claim) |

### Target 8 — flat 8x8, `W: a2 c2 / B: b7 d7`

| ep \ race | count | mover | opponent |
|---|---|---|---|
| off | *2 (yes, yes) | *2 (yes, yes) | 0 (yes, yes) |
| textbook | *2 (yes, yes) | *2 (yes, yes) | 0 (yes, yes) |
| aware | {2+-1 | -2+-1} (yes, yes) | {2+-1 | -2+-1} (yes, no claim) | 0 (yes, no claim) |

### Target 9 — cyl 3x8, `W: a2 a3 b2 / B: b7 c6 c7`

| ep \ race | count | mover | opponent |
|---|---|---|---|
| off | 0 (yes, no claim) | 0 (yes, no claim) | *2 (yes, no claim) |
| textbook | *2 (yes, no claim) | 0 (yes, no claim) | *2 (yes, no claim) |
| aware | *2 (yes, yes) | 0 (yes, no claim) | *2 (yes, no claim) |

## Disagreements

None. Every one of the 81 (target, setting) cases gives V_own identical to the converted cylcgt value
(eq_cyl = yes). No RaceError was raised by either engine. Therefore no game-tree descent to find a first
differing subposition was required.

## Notes on claims

- T3/T4 show the claimed value only under the e.p.-aware test + count rule; other settings give different
  values (e.g. T4 off/count = 1/2), which is expected and not a disagreement.
- T5: up^2 appears as {0 | down*} only under e.p.-aware count (textbook count gives the same form but is
  not in the claim list); other settings give non-canonical-looking forms.
- T7: tiny(1) appears under textbook count as well, but the claim is only for e.p.-aware count.
- T8: under e.p.-aware count the value is {2+-1 | -2+-1} (not *2), matching the adopted convention; *2
  survives only under the textbook/off tests with count/mover rules, as claimed.
- T9: *2 under e.p.-aware count, as claimed; other settings differ.

## Labels

- Agreement V_own = V_cyl: CHECKED-2 (two independent implementations).
- Tiny(1) ordering vs up and up^2: COMPUTED-1 (only this engine).
- All other printed forms: COMPUTED-1 (this engine), corroborated by cylcgt (CHECKED-2 where eq_cyl=yes).
