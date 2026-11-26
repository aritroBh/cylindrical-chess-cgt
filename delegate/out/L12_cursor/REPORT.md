# L12 cold read (Cursor): Lean 4 check vs paper

## 5-line summary

1. The three Lean claim packages assert the paper’s board, squares, settings and value/outcome statements for `thm:star2seven`, `thm:eighth` and `prop:sumcounter`, with two deliberate omissions (“X is not HSS”; kernel proof of `A + *2` with Black to move).
2. Trusted `Rules.lean` / `Game.lean` match `02_rules.tex` on the points that matter for these claims; fuel exhaustion cannot turn `IsValue` / `NotValue` / `= some b` into a false positive.
3. Headline theorems are mostly `native_decide` (compiler trust); Search-backed theorems also depend on `Classical.choice` / `Quot.sound`. Kernel `decide +kernel` covers only a slice.
4. An independent Python solver written here from the paper rules (no `cylcgt` / Lean tools) agrees with every numerical claim checked.
5. Verdict: **not wrong** on the formalised sentences; **says less** in the places listed below; one documentation claim in `L5_Eighth.lean` is false.

---

## Verdicts per theorem

### `thm:star2seven` (`L4_Star2.lean` + `KernelL4_*.lean`)

| Paper | Lean | Verdict |
|---|---|---|
| Default setting: A and B have value `*2` | `star2seven_default`: `IsValue` for `Tree.star 2` under `Settings.default` on `flat8` | **Says what the paper says** (pawn-model / sum value test) |
| Neither is `*2` with e.p. off | `star2seven_not_ep_off`: `NotValue` for all three race rules | **Says what the paper says** |
| Neither is `*2` under the opponent rule | `star2seven_not_opponent`: all three e.p. options | **Says what the paper says** |
| Table extras (mover+aware; textbook+count/mover) | `star2seven_table_extra` | Extra, matches table; not required by the theorem sentence |
| Squares / board | `posA`/`posB` match the `.tex`; board is full `flat8`, not a 4-file board | **OK for these closed a–d positions** (empty e–h never gain pawns; edge adjacency for a/d matches) |

**Says less (kernel path):** there is `star2_A_white_kernel`, `star2_B_white_kernel`, `star2_B_black_kernel`, but **no** `star2_A_black_kernel`. So of the four halves of “`A=*2` and `B=*2`” in the default setting, Black-to-move on `A + (-*2)` is only `native_decide` (`lean/notes/L3.md` notes ~4.8 GB for the kernel). Negative claims (`NotValue`) are native-only.

Paper’s nearby remark that S and W agree on this `*2` is **not** part of `thm:star2seven` and is not claimed in L4.

### `thm:eighth` (`L5_Eighth.lean` + `KernelL5.lean`)

| Paper | Lean | Verdict |
|---|---|---|
| Value exactly `1/8` in all nine settings | `eighth_nine_settings` / `Tree.eighth = dy 3 = {0\|1/4}` | **Says what the paper says** |
| Every assignment of race outcomes | `eighth_all_assignments` over `2^k` tables from `raceKeys` | **Says what the paper says** (and more: keyed by `(position, mover)`) |
| Checks also on the mirror | `eighth_mirror_nine_settings` | Matches the prose “checks ran on its mirror” |

**Says less / trust:** `eighth_default_kernel` re-checks only the **default** setting with the kernel. The other eight settings and all assignment sweeps are `native_decide`. The assignment theorem uses `Search.isValue`, not `Game.isValue`.

**Documentation error (not a wrong theorem):** `L5_Eighth.lean` lines 14–15 claim a missed race key makes the answer unknown, “so the check also shows that the table is complete.” That is false: an unassigned race on a line the winner never needs need not block a definite `some false`. Independently, with an **empty** race table (`race_table={}` in this directory’s solver), `IsValue(1/8)` is still true for aware/textbook/off — so **no race is reachable in the `G + (−1/8)` tree**, and the `2^k` loop is redundant for the value claim (control: empty table on position A is *not* `IsValue(*2)`).

### `prop:sumcounter` (`L6_SumCounter.lean` + `KernelL6*.lean`)

| Paper | Lean | Verdict |
|---|---|---|
| C₈, e.p. off, count; X = given squares; one component | `envX`, `posX`, `sumcounter_shape` | **Says what the paper says** |
| `S(X)` Black win whoever starts | `sumcounter_S`: White `some false`, Black `some true` | **Says what the paper says** |
| `W(X)` first-player win | `sumcounter_W` (+ kernel both movers) | **Says what the paper says** |
| Moreover X is not HSS | — | **Says less** (explicitly unformalised in the file header) |

**Trust:** `sumcounter_S` is `Search.S` + `native_decide` (axioms include `Classical.choice`, `Quot.sound`). Mitigation: `sumcounter_S_spec_big24` runs naive `S` with `big := 24` (comment: max plies from X are 18/21). That bound is **not proved in Lean**; if it were wrong, BIG=24 could differ from 256. Independent check below used BIG=256 and agreed.

---

## Rules / Game / Search audit (errors and doubts)

### No mismatch found vs `02_rules.tex` for these claims

Checked in `Rules.lean` against §2.1–2.5:

- Flat vs cylinder adjacency and e.p. across the seam (`beside`, `captureTo`, `epCaptures`).
- Textbook vs e.p.-aware passed test (`passed`, `epCapturable`); e.p. off disables e.p. moves and uses textbook passed.
- Count / mover / opponent (`raceWinner`); count tie → non-mover; distance with double step as one move (`Board.distance`).
- Components: maximal occupied-file runs; cylinder seam merge (`components`).
- `Settings.default = ⟨aware, count⟩`, `BIG = 256`.

Möbius-only N5 extensions are irrelevant to A/B/G/X.

### Value test (`Game.lean` 161–171)

`isValue` = no root passer and both movers lose in `X + (-v)`. Matches §2.2 / the brief. `Tree.star 2` and `Tree.eighth` are the canonical forms. Fuel 0 → `none`; `isValue` / `notValue` require `some false` / `some true`, so **fuel cannot invent a proof**.

Doubt (comment only): `Common.lean` line 19 says fuel 400 exceeds “BIG free moves plus…”. A sum that holds both `+256` and `−256` as **separate** integer components before `Search.norm` merges them needs more than 400 plies in the naive spec; Search merges integers, so it answers with less fuel. Harmless for soundness of `some _`, but the comment oversells the fuel.

### Search memo key (`Search.lean` 35–64, 86–106)

- Sum memo key: `(norm cs, Color)`. `norm` merges integer comps and drops `0` / empty trees. That is CGT-correct for numbers (`n + (−n) = 0`); not a bug.
- Key includes full `Position` (pawns + `ep`) via derived `Hashable`/`BEq` on `Comp`.
- Env (settings, board, race fn, big) is fixed in the closure of each `run` / fresh memo — not omitted across settings.
- Only definite `some b` answers are stored; `none` is recomputed.
- `W` memo: `(Position × Color)` — includes `ep`.

**Unproved equality:** `Search` ≠ proved equal to `Game`. `SearchAgrees.lean` is an explicit **test** (3378 small positions + eighth on nine settings and three tables), itself `native_decide`. Theorems that rest on Search: `eighth_all_assignments`, `sumcounter_S`.

### Vacuity / untrusted constructs

| Check | Result |
|---|---|
| `sorry` / `unsafe` / `partial` / `implemented_by` / `@[extern]` in `Rules`/`Game`/`Search`/Claims L4–L6 | **None** |
| `axiom` in those files | **None** (only `native_decide` auxiliary axioms at use sites) |
| False hypothesis / trivialising def | **Not found** for these claims |
| `#print axioms` (this run) | See below |

```
star2seven_default          : propext, …native_decide.ax_1_1
star2_A_white_kernel        : propext
eighth_nine_settings        : propext, …native_decide.ax_1_1
eighth_default_kernel       : propext
eighth_all_assignments      : propext, Classical.choice, Quot.sound, …native_decide.ax_1_1
sumcounter_S                : propext, Classical.choice, Quot.sound, …native_decide.ax_1_1
sumcounter_W                : propext, …native_decide.ax_1_1
sumcounter_W_white_kernel   : propext
```

Reproduce axioms print:

```bash
cd lean && nice -n 15 lake env lean ../delegate/out/L12_cursor/print_axioms.lean
```

---

## Independent recomputation (COMPUTED-1 here; compared to paper / Lean)

Solver: `delegate/out/L12_cursor/indep_solver.py` — written from `02_rules.tex` only; does **not** import or copy `cylcgt/`, `crosscheck/`, or `lean/tools/`. Method: `X = v` iff both movers lose in `X + (−v)`. Passed test: e.p.-aware / textbook / off as named. BIG = 256.

```bash
cd <repository root>
PYTHONPATH=. nice -n 15 .venv/bin/python -u delegate/out/L12_cursor/indep_solver.py
# log: delegate/out/L12_cursor/indep_run.log  (~24 s)
```

| Claim | Paper / Lean | This solver |
|---|---|---|
| A, B = `*2` (aware+count) | yes | **True / True** |
| Not `*2` for e.p. off × {count,mover,opponent} | NotValue | **all True** |
| Not `*2` for opponent × {aware,textbook,off} | NotValue | **all True** |
| Table extras (3 settings) still `*2` | IsValue | **all True** |
| G = `1/8` in all 9 settings | IsValue | **all True** |
| Race key counts | Lean `[9,10,9]` | **9, 10, 9** |
| All `2^k` race assignments → `1/8` | Lean true | **True** (512+1024+512) |
| Empty race table → still `1/8` | (spec fact; L5 docs wrong) | **True** for all three e.p. |
| X one component, no passer (cyl, ep off) | shape | **1 / False/False** |
| S(X): White loses, Black wins | some false / true | **False / True** |
| W(X): both movers win | some true / true | **True / True** |

Status label for this cross-check: **CHECKED-2** against Lean’s claimed answers (independent implementation), for the finite outcomes above. No claim that the Lean *proof objects* are verified beyond reading statements and axioms.

---

## What was not checked

- Full `lake build` (forbidden; other jobs building). Relied on existing `.olean`s for `#print axioms`.
- Kernel proof of `star2_A_black` (file absent; memory).
- Proof that Search ≡ Game on all positions, or that BIG=24 equals BIG=256 for every line of `S(X)`.
- “X is not HSS”, legality of pawn history for A/B/G, S↔W agreement remark for the seven-pawn `*2`.
- Hash collision / `Hashable` correctness beyond “derived + Std.HashMap”.
- Exhaustive line-by-line comparison of every sentence of N5 Möbius rules (unused here).
- Whether `native_decide`’s compiled evaluator matches the kernel on the unkernelised theorems (by definition trusted only if one trusts the compiler).

---

## Bottom line for a reader of the paper

The Lean check **supports** the three formalised claim sentences; an independent solver **agrees**. Treat “machine-checked” as: **specification in `Rules`/`Game` + mostly compiled `native_decide`, with kernel coverage of a proper subset, and `Search` used where the naive spec is too slow.** Do not read L6 as having formalised “not HSS”, and do not read L5’s race-key completeness story as proved by the `2^k` loop.
