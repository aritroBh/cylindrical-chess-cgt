# Cylinder value atlas rerun under the e.p.-aware passed test

**Output directory:** `atlas/cylinder/ep_aware/`
**Date:** 2026-10-21
**Convention:** `cylcgt.pawns.PASSED_RESPECTS_EP = True` (default since commit d3d080e). A pawn that can still be taken en passant is NOT passed.

---

## 5-line summary

1. Reran the full cylinder atlas (≤5 pawns, widths 3–8, cylinder and flat, count rule, e.p. on) with the current e.p.-aware cylcgt. 1,223,689 positions evaluated, yielding 10,561 distinct canonical values (vs 10,369 in the textbook atlas).

2. **85,391 positions (7.0%) change value** compared to the textbook atlas; **0 outcome classes change**. The e.p.-aware test mainly affects positions where a double-step creates an en passant capture that blocks a passed-pawn threat.

3. **Cylinder-only values without ±W**: 3-file gains 6 (42→48), 4-file loses 5 (13→8). The 4-file cylinder value `{3/2±1/2 | −3/2±1/2}` becomes `{2±1 | −2±1}`. The 3-file ring values `3/4`, `−3/4`, `1/4±1/4` **survive unchanged**.

4. **No *k (k ≥ 2) appears anywhere** in the e.p.-aware atlas. The flat 4-file `*2` at `W a2 c2 / B b7 d7` becomes `{2±1 | −2±1}`; no new nimber ≥ *2 emerges on any cylinder or flat strip.

5. The ring value sets shift: 3-file rings have 2,251 values (was 2,254), 4-file rings 2,222 (was 2,232), 5-file rings 496 (unchanged). Cylinder-only ring values without ±W increase on 3 files (1267→1285) and 4 files (986→1021).

---

## What was computed

Same enumeration as the textbook atlas: every canonical pawn-only position with `w+b ≤ 5` on cylinders and flat strips of widths 3–8 (ranks 2–7), with the count race rule and en passant on. Positions with a passed pawn at the root are excluded. Cylinder positions reduced by dihedral symmetry (order 2n); flat by mirror symmetry.

**Commands** (from project root):
```
PYTHONPATH=. .venv/bin/python atlas/cylinder/ep_aware/atlas_run.py --widths 3,4,5,6,7,8 --minpawns 2 --maxpawns 5 --mode all --shards 2 --jobs 6 --outdir atlas/cylinder/ep_aware/parts
PYTHONPATH=. .venv/bin/python atlas/cylinder/ep_aware/analyze.py
```

Wall time: ~12 minutes (widths 3–5: 163 s; widths 6–8: 561 s).

---

## Comparison with the textbook atlas (atlas/cylinder/)

### Position counts (identical)

| Board | Width | 2 pawns | 3 pawns | 4 pawns | 5 pawns | Total |
|-------|-------|---------|---------|---------|---------|-------|
| cyl   | 3     | 30      | 260     | 1,680   | 8,378   | 10,348 |
| cyl   | 4     | 30      | 260     | 2,405   | 17,288  | 19,983 |
| cyl   | 5     | 30      | 260     | 2,870   | 26,522  | 29,682 |
| cyl   | 6     | 30      | 260     | 3,455   | 37,172  | 40,917 |
| cyl   | 7     | 30      | 260     | 3,905   | 46,772  | 50,967 |
| cyl   | 8     | 30      | 260     | 4,490   | 57,422  | 62,202 |
| flat  | 3     | 60      | 450     | 2,980   | 15,292  | 18,782 |
| flat  | 4     | 75      | 640     | 5,970   | 43,632  | 50,317 |
| flat  | 5     | 105     | 900     | 10,160  | 92,204  | 103,369 |
| flat  | 6     | 120     | 1,090   | 15,175  | 160,318 | 176,703 |
| flat  | 7     | 150     | 1,350   | 21,390  | 249,390 | 272,280 |
| flat  | 8     | 165     | 1,540   | 28,430  | 358,004 | 388,139 |
| **Total** | | | | | | **1,223,689** |

### Value counts per width (ALL level, all values)

| Width | Cylinder values | Flat values |
|-------|-----------------|-------------|
|       | Textbook → Ep-aware | Textbook → Ep-aware |
| 3     | 2,614 → 2,613 (−1) | 4,116 → 4,198 (+82) |
| 4     | 5,550 → 5,597 (+47) | 7,130 → 7,257 (+127) |
| 5     | 7,336 → 7,469 (+133) | 7,922 → 8,065 (+143) |
| 6     | 7,922 → 8,065 (+143) | 7,964 → 8,107 (+143) |
| 7     | 7,964 → 8,107 (+143) | 7,964 → 8,107 (+143) |
| 8     | 7,964 → 8,107 (+143) | 7,964 → 8,107 (+143) |

The increases for widths ≥5 come entirely from the cut lemma: a cylinder with an empty file equals the flat strip of width n−1. Since the flat strips gain values, the cylinders inherit them.

### Cylinder-only values without ±W (the "genuine" cylinder values)

| Width | Textbook | Ep-aware | Change |
|-------|----------|----------|--------|
| 3     | 42       | 48       | +6 |
| 4     | 13       | 8        | −5 |
| 5     | 0        | 0        | 0 |
| 6–8   | 0        | 0        | 0 |

**Width 3 (48 values, all from rings):** The 6 gained values are `+W`, `−W`, `5/2`, `−5/2`, `{0 | {0, * | −1}}`, `{{1 | 0, *} | 0}`. These involve positions where the e.p.-aware test prevents a pawn from being passed, creating new ±W options or shifting the mean.

**Width 4 (8 values, all from rings):** 7 values lost, 2 gained.
- **Lost (textbook only):** `{3/2±1/2 | −3/2±1/2}`, `{3/2±1/2 | −1}`, `{2* | 1}`, `{2* | 1/2±1/2}`, `{1 | −3/2±1/2}`, `{−1 | −2*}`, `{−1/2±1/2 | −2*}`.
- **Gained (ep-aware only):** `{5/2±1/2 | 1/2±1/2}`, `{−1/2±1/2 | −5/2±1/2}`.

The headline 4-file ring value `{3/2±1/2 | −3/2±1/2}` at `W a2 c2 / B b7 d7` **does not survive**; it becomes `{2±1 | −2±1}` (mean 0, temperature 2).

**Widths 5–8:** No cylinder-only values without ±W in either atlas, consistent with the cut lemma (rings need ≥n pawns).

### Flat-only values without ±W

| Width | Textbook | Ep-aware | Change |
|-------|----------|----------|--------|
| 3     | 200      | 204      | +4 |
| 4     | 41       | 32       | −9 |
| 5     | 0        | 2        | +2 |
| 6–8   | 0        | 0        | 0 |

No value occurs on a flat strip and on no cylinder (as in the textbook atlas).

---

## Headline positions: survival of the ring values

| Position | Board | Textbook value | Ep-aware value | Survives? |
|----------|-------|----------------|----------------|-----------|
| `W a2 b4 / B b7 c6` | cyl 3 | `3/4` | `3/4` | **YES** |
| `W a2 b3 / B a5 c7` | cyl 3 | `−3/4` | `−3/4` | **YES** |
| `W a2 b2 / B c5 c6` | cyl 3 | `1/4±1/4` | `1/4±1/4` | **YES** |
| `W a2 c2 / B b7 d7` | cyl 4 | `{3/2±1/2 | −3/2±1/2}` | `{2±1 | −2±1}` | **NO** (changes) |
| `W a2 c2 / B b7 d7` | flat 4 | `*2` | `{2±1 | −2±1}` | **NO** (changes) |

The three 3-file cylinder ring values are robust to the e.p.-aware test. The 4-file ring value and the flat 4-file `*2` both change to the same switch `{2±1 | −2±1}`.

---

## Nimbers *k (k ≥ 2)

| Atlas | *2 occurrences | *3 or higher |
|-------|----------------|--------------|
| Textbook | 1 (flat 4-file: `W a2 c2 / B b7 d7`) | 0 |
| Ep-aware | **0** | **0** |

**No *k with k ≥ 2 appears anywhere in the e.p.-aware atlas** (cylinder or flat, widths 3–8, ≤5 pawns). The unique textbook `*2` was an artefact of the textbook passed-pawn test: the double-step `a2–a4` was considered passed, but with e.p. aware it is not, and the position becomes a temperature-2 switch.

---

## Ring components

| Cylinder | Positions | Values | Values not in any flat atom |
|----------|-----------|--------|-----------------------------|
|          | Textbook → Ep-aware | Textbook → Ep-aware | Textbook → Ep-aware |
| 3 files  | 6,905 → 6,905 | 2,254 → 2,251 | 1,267 → 1,285 |
| 4 files  | 4,629 → 4,629 | 2,232 → 2,222 | 986 → 1,021 |
| 5 files  | 1,034 → 1,034 | 496 → 496 | 166 → 168 |

Ring positions are identical (same pawns on every file). The value sets shrink slightly because some textbook ring values merge under the e.p.-aware test, but the number of cylinder-only ring values grows because the flat strips lose some values that the rings keep.

---

## Value classes (ALL level, all widths combined, excluding involves_W)

| Class | Textbook | Ep-aware | Change |
|-------|----------|----------|--------|
| dyadic | 96 | 74 | −22 |
| hot | 2,424 | 2,452 | +28 |
| integer | 180 | 180 | 0 |
| nimber | 21 | 12 | −9 |
| number+nimber | 92 | 70 | −22 |
| other_inf | 356 | 402 | +46 |
| switch | 497 | 406 | −91 |
| tiny | 136 | 136 | 0 |
| ups | 404 | 404 | 0 |
| won | 382 | 358 | −24 |

The nimber count drops from 21 to 12 because the `*2` and several `*`-containing switches disappear. Switches drop significantly as many become `hot` or `other_inf`.

---

## Outcome class stability

**0 outcome class changes** across all 1,223,689 positions. Every position that changes value keeps the same outcome (L, R, N, or P). The e.p.-aware test affects the *exact* value but not the winner.

---

## Total distinct values

| | Textbook | Ep-aware |
|---|----------|----------|
| Distinct canonical values | 10,369 | 10,561 |
| Shared (same vid) | — | 9,106 |
| Only in textbook | — | 1,263 |
| Only in ep-aware | — | 1,455 |

The net increase of 192 distinct values comes from the flat strips (which are larger sets) gaining more values than they lose.

---

## Reproduce

```bash
# Full atlas (widths 3–8, all boards, count rule, e.p. on)
PYTHONPATH=. .venv/bin/python atlas/cylinder/ep_aware/atlas_run.py \
  --widths 3,4,5,6,7,8 --minpawns 2 --maxpawns 5 \
  --mode all --shards 2 --jobs 6 \
  --outdir atlas/cylinder/ep_aware/parts

# Merge and summarise
PYTHONPATH=. .venv/bin/python atlas/cylinder/ep_aware/analyze.py

# Summary tables
cd atlas/cylinder/ep_aware && ../../.venv/bin/python tables.py > logs/tables.txt
```

---

## Claims

| id | importance | status | statement |
|----|------------|--------|-----------|
| E1 | key | COMPUTED-1 | Rerunning the cylinder atlas with `PASSED_RESPECTS_EP=True` (count rule, e.p. on, ≤5 pawns, widths 3–8) produces 1,223,689 positions with 10,561 distinct values. 85,391 positions change value vs the textbook atlas; 0 change outcome class. |
| E2 | headline | COMPUTED-1 | The 3-file cylinder ring values `3/4`, `−3/4`, `1/4±1/4` survive unchanged. The 4-file cylinder ring value `{3/2±1/2 | −3/2±1/2}` becomes `{2±1 | −2±1}`. |
| E3 | headline | COMPUTED-1 | No *k (k ≥ 2) occurs in the e.p.-aware atlas. The textbook `*2` on the flat 4-file strip (`W a2 c2 / B b7 d7`) and the 4-file cylinder ring both become `{2±1 | −2±1}`. |
| E4 | key | COMPUTED-1 | Cylinder-only values without ±W: 3-file gains 6 (42→48), 4-file loses 5 (13→8). Widths 5–8 remain at 0. |
| E5 | minor | COMPUTED-1 | Ring value sets: 3-file 2,254→2,251, 4-file 2,232→2,222, 5-file 496→496. Cylinder-only ring values without ±W increase on 3 and 4 files. |
| E6 | minor | COMPUTED-1 | Value class shifts: nimbers 21→12, switches 497→406, hot 2424→2452, other_inf 356→402. The lost nimbers are `*2` and several `*`-containing switches. |

---

## Open questions

- The 4-file ring value change `{3/2±1/2 | −3/2±1/2} → {2±1 | −2±1}` is a direct consequence of the e.p.-aware test. Does any race rule restore the original value? (The textbook atlas showed it was stable across all three race rules *with* the textbook test.)
- Are there any *k ≥ 2 at 6+ pawns on 4-file flat strips or rings? Not enumerated.
- The 3-file cylinder gains ±W-only values (`+W`, `−W`, `±5/2`). Are these artefacts of the short-game e.p. model, or do they reflect genuine chess features?

---

## Files produced

- `parts/` — 240 JSONL shards (`.jsonl` + `.vals`)
- `values.jsonl` — 1,223,689 lines, one per canonical position
- `value_index.jsonl` — 10,561 lines, one per distinct value
- `summary.json` — machine-readable aggregates (this report's source)
- `logs/` — (to be generated by `tables.py`)