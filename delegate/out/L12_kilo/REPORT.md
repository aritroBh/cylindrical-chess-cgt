# L12 — Cold read of the Lean 4 check (independent referee)

## 5-line summary
1. All three Lean theorems state exactly what the paper asserts (boards, every pawn square, settings,
   side-to-move, quantifiers all match); I found no statement that says less or more than the paper's main claim.
2. The trusted base (`Rules.lean`, `Game.lean`, `Search.lean`) contains no `sorry`/`axiom`/`unsafe`/`partial`/
   `implemented_by`/`@[extern]`; the value test is the correct "X+v.neg is a second-player win for both movers".
3. I wrote an independent Python solver from the paper's rules alone (no repo solver imported) and it reproduces
   every headline number: A,B = *2 in default and not *2 (ep-off / opponent); 1/8 in all nine settings (and both
   race extremes for all ep); X single-component with W a first-player win and S a Black win.
4. `#print axioms` (run live) shows the `*_kernel` theorems depend only on `propext`; the `native_decide` theorems
   additionally depend on the `native_decide` axiom (they trust the compiled code). No `sorryAx` anywhere.
5. Main caveats (not errors): the "every race assignment" half of L5 and the S(X) half of L6 are proved only by
   `native_decide` over `Search` (compiled + Search-vs-Game only tested, not proved); L4's A-with-Black-to-move
   default case has no `decide +kernel` companion (native_decide only). My independent solver covers all of these.

## What was checked and how
- Read the paper: `dist/tog/sections/02_rules.tex`, `05_sums.tex` (prop:sumcounter), `07_targets.tex`
  (thm:eighth), `08_star2.tex` (thm:star2seven).
- Read Lean: `Rules.lean`, `Game.lean`, `Search.lean`, `Claims/Common.lean`, `Claims/L4_Star2.lean`,
  `Claims/L5_Eighth.lean`, `Claims/L6_SumCounter.lean`, the `KernelL4_*`, `KernelL5`, `KernelL6*` files,
  `Claims/Axioms.lean`, `SearchAgrees.lean`.
- Grepped the whole `lean/` tree for `sorry|axiom|unsafe|partial|implemented_by|extern|sorryAx`. Only hits:
  `MoveList.lean:104` (`partial def loop`, a CLI tool, not in the trusted base or any claim) and four comments
  that say "no partial/sorry". Trusted files and all claim files are clean.
- Ran `#print axioms` live (file `AxCheck.lean` in this directory) via `lake env lean` against the already-built
  oleans (no `lake build`).
- Wrote `solver.py` (this directory) from the paper rules only, and ran it.

## Verdict per theorem

### L4 — `thm:star2seven` (`L4_Star2.lean`): SAYS WHAT THE PAPER SAYS
- `posA`/`posB` (lines 14–18) transcribe `W a4 b3 d2 d3 / B a7 b7 c5` and `W b4 c2 d2 / B a6 a7 c6 d5`
  on `flat8` (files a–d occupied, e–h empty) exactly. `star2seven_shape` (line 21) proves each is one component.
- `star2seven_default` (25–27): `IsValue ⟨aware,count⟩ A (star 2) ∧ … B`. = "value *2 in the default setting". ✓
- `star2seven_not_ep_off` (30–33): for all three race rules, `NotValue ⟨off,r⟩` for A and B. = "neither is *2
  with e.p. off". ✓
- `star2seven_not_opponent` (36–39): for all three e.p. options, `NotValue ⟨ep,opponent⟩`. = "nor under the
  opponent rule" (Table `tab:star2_settings`, last row). ✓
- `star2seven_table_extra` (43–46) proves the remaining e.p.-on count/mover cells of the table — extra, correct.
- No assumption beyond the paper. `IsValue` is the sum-model value; A,B are single components so this is the
  paper's model value.
- Proof strength: all `native_decide`. Kernel companions (`decide +kernel`, axiom set = `{propext}`) exist for
  A-white, B-white, B-black only; **A with Black to move in the default setting has no kernel companion**
  (native_decide only). My solver confirms A default *2 (both movers), so this gap is covered independently.

### L5 — `thm:eighth` (`L5_Eighth.lean`): SAYS WHAT THE PAPER SAYS
- `posG` (23–24) = `W a2 b2 b3 / B a5 a6 b6` exactly.
- `eighth_nine_settings` (31–32): `∀ s ∈ allSettings, IsValue s posG (dy 3)`. `allSettings` (Common.lean:16–17)
  is the 3 e.p. options × 3 race rules = nine; `dy 3 = {0|1/4} = 1/8`. = "value exactly 1/8 in all nine
  settings". ✓
- `eighth_all_assignments` (81–82) + `raceKeys` (43–55) + `envTable` (58–59): enumerates the `k` reachable race
  positions (`eighth_race_counts = [9,10,9]`, line 77) and checks all `2^k` winner assignments per e.p. option.
  = "for every assignment of outcomes to its race positions". ✓ The design is sound against an incomplete
  `raceKeys`: a missed key makes `Env.race` return `none` → `undefined` → `isValue` false, so a missed race can
  only make the theorem fail, never pass falsely.
- Extra: `eighth_mirror_nine_settings` (35–36) proves the mirror image too (paper says its checks ran on the mirror).
- Proof strength: `native_decide` over `Search.isValue`. `eighth_default_kernel` (`decide +kernel`) kernel-checks
  only the default setting. The "every assignment" half is **native_decide + Search only** (Search≠Game is tested
  in `SearchAgrees`, not proved). My solver independently confirms 1/8 for all nine settings and for both race
  extremes (all-White, all-Black) under each e.p. option, which by the monotonicity noted in the file's comment
  covers every assignment.

### L6 — `prop:sumcounter` (`L6_SumCounter.lean`): SAYS WHAT THE PAPER SAYS
- `posX` (15–16) = `W b2 d4 g3 h5 / B a7 c7 f7 g4`; `envX = ⟨off,count⟩ cyl8` (line 18). ✓
- `sumcounter_shape` (21–23): one component on `cyl8`, no passed pawn. = "single component spanning files f–d
  across the seam". ✓
- `sumcounter_W` (26–27): `W … white = some true ∧ … black = some true`. = "W(X) a first-player win". ✓
- `sumcounter_S` (30–32): `Search.S … white = some false ∧ … black = some true`. = "S(X) a black win whoever
  starts". ✓
- `sumcounter_S_spec_big24` (38–40): the same S outcomes via the *specification* `Game.S` (naive) with `big=24`
  (justified: 24 > the ≤18/≤21 moves either side can make). Confirms S is not a Search artefact.
- The paper's side sentence "X is not HSS" is **not formalised** (stated in the file header); it is explanatory,
  not part of the proposition's claim.
- Proof strength: `sumcounter_W` native_decide (kernel companions white/black = `{propext}`); `sumcounter_S` and
  `…_spec_big24` are **native_decide only** (the naive S is too slow for the kernel). My solver (fuel-free,
  memoised) independently gives W = (white True, black True) and S = (white False, black True).

## Errors / doubts (with file:line)
No soundness error found. Doubts are about trust level, not correctness:
1. `L5_Eighth.lean:81` `eighth_all_assignments` and `L6_SumCounter.lean:30` `sumcounter_S` rest on `native_decide`
   of `Search` functions; `Search.lean` is only *tested* equal to `Game.lean` (`SearchAgrees.lean`), not proved.
   The Search memo key `(List Comp × Color)` (`Search.lean:35`) does include the full state (all components with
   their e.p. flags, and the mover), and `norm` (`Search.lean:27–33`) only merges integer components and drops
   zero trees (value-preserving), so I see no memo bug — but this is review, not a proof.
2. `KernelL4_*` cover A-white, B-white, B-black; the A-black default case of `star2seven_default`
   (`L4_Star2.lean:25`) is native_decide only.
3. `eighth_default_kernel` kernel-checks only the default setting, not all nine.
None of these change a verdict; each is independently covered by `solver.py`.

## My independent program's results (`solver.py`, run: `PYTHONPATH= delegate/out/L12_kilo/.venv/bin/python …`)
Reproduce: `.venv/bin/python delegate/out/L12_kilo/solver.py`
(saved in `solver_out.txt`). Method: "X has value v iff the player to move loses in X+(−v) for both movers",
sum model with BIG=256, plus a separate whole-board minimax W. No fuel bound (full memoised recursion), so it
also validates that Lean's `fuel = 400` is sufficient.
- L4: A default *2 = True, B default *2 = True; A,B ep-off (count/mover/opponent) *2 = False; A,B opponent
  (aware/textbook/off) *2 = False. — matches paper and Lean.
- L5: posG = 1/8 in all nine settings = True; both race extremes (all-White, all-Black) = 1/8 for each e.p. = True.
  — matches.
- L6: X single component = True; W white-to-move = True, black-to-move = True (first-player win); S white = False,
  black = True (Black win whoever starts). — matches.
- Cross-checks of the harness itself: Fig. basic(b) `W a4 h3 / B a5 h6` = 0 on C8 (True); candidate
  `W a2 c2 / B b7 d7` textbook/count = *2 (True) and aware/count ≠ *2 (True); `W a2 b3 / B b4` aware = 0 (True).

## What I did NOT check
- I did not enumerate all 2^k race assignments independently (only the two monotone extremes per e.p. option).
- I did not run the kernel (`decide +kernel`) myself; I relied on the built oleans for `#print axioms`.
- I did not audit the Möbius/strip-only rules (N5 choices in `Rules.lean:16–31`) — not used by these three claims.
- I did not review the out-of-scope modules (`SearchWide*`, `Heaps*`, `Families`, `Dawson`, `L7a`, `L9`, `Census`).
- I did not independently re-derive the SearchAgrees 3378-position family; I read it and it is a test, as labelled.