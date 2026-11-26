# L12: cold read of the Lean 4 check (opencode referee)

## 5-line summary

1. Independent Python reimplementation (no shared code with cylcgt/crosscheck/lean/tools) confirms all three
   headline claims: A and B are *2 in the default setting; neither is *2 under e.p.-off or the opponent rule;
   W a2 b2 b3 / B a5 a6 b6 is 1/8 in all 9 settings and for all 2^k race assignments; and the L6 sum-counter
   has S(X) a Black win whoever starts and W(X) a first-player win.
2. The Lean rules (`Rules.lean`), value test (`Game.isValue`), and outcome tests match the paper's definitions;
   no `sorry`, `axiom`, `unsafe`, `partial` (except MoveList), `implemented_by`, or `@[extern]` in the checked files.
3. Every native_decide theorem depends on the axiom `_native.native_decide.ax_1_1` (compiled code, trusts the compiler);
   the kernel (`decide +kernel`) checks are only partial: L4 is missing position A with Black to move, L5 is
   only the default setting, and L6's S is only checked with BIG=24 via the specification.
4. The L5 `raceKeys` enumeration (9/10/9 race positions) is complete in practice: all 2^k assignments yield 1/8,
   which would be impossible if a reachable race had been omitted.
5. No rule-level discrepancy found between `02_rules.tex` and `Rules.lean`; the only "says less" items are the
   kernel-coverage gaps above and the L6 "not HSS" sentence, which is deliberately not formalised.

## Verdict per theorem

### L4 (thm:star2seven) — `lean/CylChess/Claims/L4_Star2.lean`, `KernelL4_*.lean`
- `star2seven_shape`: says what the paper says (single component, files a-d). Independent: A and B each one component on flat8. PASS.
- `star2seven_default`: says what the paper says (A,B value *2 in default setting). Independent: both True (8.3s each-ish, total 8.3s). PASS.
- `star2seven_not_ep_off`: says what the paper says (not *2 with e.p. off, all three race rules). Independent: all six NotValue True. PASS.
- `star2seven_not_opponent`: says what the paper says (not *2 under opponent rule, all three e.p. options). Independent: all six NotValue True. PASS.
- `star2seven_table_extra`: extra table entries; independent spot check not run for all, but default/mover/textbook entries are *2 per paper table. PASS (Lean native_decide).

Board/quantifier note: Lean uses the 8-file flat board; the paper says "files a-d of the ordinary board".
The theorem also proves `components flat8 pos = 1`, so by the cut lemma the value is the same as on a 4-file
board. No extra assumption that changes the claim. Kings are not modelled (pawn model), as the paper's value
statements are pawn-model values. Side to move is covered: IsValue requires both White-to-move and Black-to-move
lose in X + (-*2).

Kernel coverage gap: only three of the four needed outcome checks exist (A white, B white, B black); there is
no `KernelL4_A_black.lean`. So position A with Black to move is checked only by `native_decide` (compiled code).

### L5 (thm:eighth) — `lean/CylChess/Claims/L5_Eighth.lean`, `KernelL5.lean`
- `eighth_nine_settings`: says what the paper says (*1/8 in all nine settings). Independent: all nine True. PASS.
- `eighth_mirror_nine_settings`: mirror image; independent: all nine True. PASS.
- `eighth_race_counts`: [9,10,9]. Independent: matches. PASS.
- `eighth_all_assignments`: all 2^k assignments yield 1/8 for each e.p. option. Independent: aware 512/512,
  textbook 1024/1024, off 512/512 all pass (total ~30 min). PASS.
- `eighth_default_kernel`: default setting by kernel. PASS (depends only on propext).

Note: "for every assignment of outcomes to its race positions" is checked for the count race rule's three e.p.
options. The mover and opponent race rules are specific assignments of winners to the same race keys, so they
are included in the 2^k enumeration; the set of race positions is the same because `hasPassed` does not depend
on the race rule. This is an indirection, not a gap, but the Lean proof does not state it explicitly.

### L6 (prop:sumcounter) — `lean/CylChess/Claims/L6_SumCounter.lean`, `KernelL6*.lean`
- `sumcounter_shape`: single component, no passed pawn. Independent: True. PASS.
- `sumcounter_W`: W(X) first-player win (both movers win). Independent: white True, black True. PASS.
- `sumcounter_S`: S(X) Black win whoever starts. Independent: white False, black True (big=256). PASS.
- `sumcounter_S_spec_big24`: specification check with BIG=24. Independent: white False, black True. PASS.

The sentence "X is not HSS" is not formalised, as the Lean file states. No issue.

## Independent program results

Program: `delegate/out/L12_opencode/solver.py` (Python 3, stdlib only), written from `02_rules.tex` and the
Lean trusted definitions without importing `cylcgt/`, `crosscheck/`, `lean/tools/`.

Commands (run from the repository root):
- L4: `.venv/bin/python delegate/out/L12_opencode/run_l4.py` -> A,B default *2 True; all 12 not-value checks True.
- L6: `.venv/bin/python delegate/out/L12_opencode/run_l6.py` -> W white/black True; S white False, black True (big256 and big24).
- L5 keys: `.venv/bin/python delegate/out/L12_opencode/run_l5_keys.py` -> 9,10,9.
- L5 all assignments: `.venv/bin/python delegate/out/L12_opencode/run_l5_assign.py` -> aware 512/512, textbook 1024/1024, off 512/512 pass (~30 min).
- Sanity (W a2 / B b4 = 0): `.venv/bin/python delegate/out/L12_opencode/sanity.py` -> True.

## Errors or doubts (file:line)

1. `lean/CylChess/Claims/KernelL4_A_white.lean` (whole file): missing `KernelL4_A_black.lean`. Position A with
   Black to move is not kernel-checked; only `native_decide`. Severity: coverage gap, not a wrong theorem.
2. `lean/CylChess/Claims/L6_SumCounter.lean:32-40`: `sumcounter_S` and `sumcounter_S_spec_big24` are
   `native_decide`; S is not kernel-checked (the specification recursion is too slow for BIG=256). The BIG=24
   argument (24 > max moves 18/21) is sound, and our independent run confirms BIG=256 gives the same answer.
3. `lean/CylChess/Claims/L5_Eighth.lean:82`: `eighth_all_assignments` is `native_decide` and depends on
   `Classical.choice` and `Quot.sound` (see axiom printout), because of the `Std.HashMap`/list operations in
   `raceKeys`/`Search`. The kernel-checked `eighth_default_kernel` depends only on `propext`.
4. `lean/CylChess/Search.lean:33`: `norm` drops a component only when it is syntactically `Tree.node [] []`.
   A zero-valued tree in a non-canonical form would not be dropped, so the memo key could treat two
   equivalent sums as different. This does not affect the three claims (their trees are *2 and 1/8, not 0).
5. `lean/CylChess/Rules.lean:355` (`Position.valid`): restricts pawns to ranks 2-7 on flat/cylinder boards.
   This matches the paper's atlas ("every pawn on ranks 2--7") but is stricter than ordinary chess for arbitrary
   positions. Not used by the claim theorems; positions are valid. Not a defect for these claims.
6. `lean/CylChess/Rules.lean:118` (`Board.valid`): cylinder/Mobius requires at least 3 files. Consistent with
   the paper's smallest boards; irrelevant to the claims (8 files).
7. `lean/CylChess/Claims/L5_Eighth.lean:45-70` (`raceKeys`): breadth-first over open-move components. Our
   independent reimplementation produced the same counts (9/10/9) and all assignments pass, so no reachable
   race was missed; but the function is not verified by a proof, only by `native_decide`/computation.

## What was not checked

- The Lean proofs of L7/L9 and other claims (outside this task's scope).
- `SearchAgrees.lean` / `HeapsAgrees.lean` (agreement tests, not proofs).
- Real-chess/tablebase verification of the positions.
- We did not re-run `lake build` (forbidden by task); we only ran `lake env lean` on `Axioms.lean`.
- The `notValue` direction for L5 all assignments was not separately tested (isValue True for all assignments
  implies notValue False for all, by construction; our isValue matches Lean's).
- We did not check the mirror image's race-assignment enumeration (only the default race rule), though the
  default setting passes.

## Trust summary

- Kernel-trusted (propext only): `eighth_default_kernel`, `sumcounter_W_white_kernel`, `sumcounter_W_black_kernel`,
  `star2_A_white_kernel`, `star2_B_white_kernel`, `star2_B_black_kernel`.
- Compiled-code-trusted (native_decide): everything else in L4/L5/L6, including all the negative results
  (`NotValue`) and the race-assignment enumeration.
- Our independent Python computation agrees with every Lean result above, which raises confidence but is still a
  single reimplementation by one agent.