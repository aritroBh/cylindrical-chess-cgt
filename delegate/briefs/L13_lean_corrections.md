# L13: corrections to the Lean check after the referees' reads

Project: `lean/` (Lean 4.36.0, no Mathlib). Read first: `lean/notes/L3_referee.md` (Opus referee) and
`delegate/out/L12_codex/REPORT.md`, `delegate/out/L12_cursor/REPORT.md` (outside referees). Their findings are
model output: check each against the Lean source before acting.

Rules: never use pkill, killall, `kill -- -1` or `kill $(pgrep ...)`; signal only PIDs you started and recorded.
Other projects share this machine. nice -n 15 for every build, one `lake build` at a time, under 4 GB per process.
No `sorry`, `axiom`, `unsafe`, `partial`, `implemented_by`, `@[extern]`. Do not edit `Rules.lean`, `Game.lean`,
`Search.lean`, `paper/`, `dist/`, `kings/`. Do not commit. No network.

## Tasks

1. **Empty race table for 1/8** (new file `lean/CylChess/Claims/L5_EmptyTable.lean`).
   Prove, on the specification `Game.isValue` (not `Search`), that the position of `L5_Eighth.lean` has value 1/8
   for each of the three e.p. options when the environment's race function answers `none` for every race
   (`race := fun _ _ => none`). `native_decide`; add a `decide +kernel` version if it fits in 3 GB and 10 minutes.
   In the file's header explain in three or four sentences why this implies the value for every assignment: a
   definite answer of `Game.wins` uses only moves whose verdict is defined, so it stays the same when unknown races
   are given any winner. Say plainly that this monotonicity step is an argument in words, not a Lean theorem,
   unless you can prove it in Lean in under about 80 lines (try; stop after an hour).

2. **Correct the false statements.**
   - `L5_Eighth.lean` header and the `raceKeys` docstring: a missed race key does NOT make the check fail.
     Replace by the true statement and point to `L5_EmptyTable.lean`.
   - `lean/notes/L3.md` decision 6 (same error) and decision 2 (A and B do split into two components later, with a
     live e.p. right, in 18 reachable positions; rerunning with the chess rule gives the same results: say that).
   - `L4_Star2.lean`: the docstring of `star2seven_shape` says more than the statement (it checks component
     counts only). Make the docstring match, or better do task 3.
   - `SearchAgrees.lean` / `Search.lean` header: "same outcomes" holds for definite answers; at equal small fuel the
     fast search can answer where the specification says unknown (it cancels integers). Comment change only;
     `Search.lean` code must not change.
   - Wherever a claim file's prose says "value" without the model, say "in the sum model" once per file header.
   Do NOT edit `Claims/Common.lean` (the main session will fix its fuel comment itself).

3. **Starting positions are open** (new file `lean/CylChess/Claims/RootsOpen.lean`).
   `notValue`, `S` and `W` do not test that the root has no passed pawn. State and prove (`decide` if it goes
   through, else `native_decide`): for every setting in `allSettings`, `posA` and `posB` on `flat8` have no passed
   pawn for either colour; the same for `posG`, `posGMirror`; and `posX` on `cyl8` under e.p. off / count.
   Do the same for the starting positions of the L7 to L10 claim files if those files exist and expose their
   positions (look in `lean/CylChess/Claims/L7*.lean`, `L9_Cut.lean`); if their theorems already use `IsValue`
   only, note that `isValue` guards the root and add nothing.

4. **"X is not hereditarily sum-safe"** (new file `lean/CylChess/Claims/L6_NotHSS.lean`).
   Definition `def:hss` in `dist/tog/sections/05_sums.tex` (lines 31 to 35). Formalise the witness, not the general
   definition: from `posX` (cylinder C_8, e.p. off, count), the moves h5-h6 then a7xh6 (across the seam) are legal
   (each is in `moves`), no passed pawn appears, and the result has exactly two components (files b to d, files
   f to h). In the b-d component the line d4-d5, c7-c5 is legal, has no passed pawn before its last position and
   leaves White (and only check what is true: run it) a passed pawn. In the f-h component the line h6-h5, h5-h4,
   g3xh4 is legal, has no passed pawn before its last position and leaves Black a passed pawn.
   Write a small checker `lineOK : Env → Position → List (Color × Position) → Bool` (each step is a member of
   `moves`, no passed pawn before the last step) and state the facts with it. Use `decide` (kernel) if it goes
   through. If any step of this line is not legal or a passed pawn appears earlier, do not force it: report
   exactly what Lean says and search for another witness with a short program (`#eval`), then prove that one.
   The header must quote the definition and say that the theorem proves this one witness, which is what "not HSS"
   needs.

5. Build each new file with `nice -n 15 lake build CylChess.Claims.<Name>` (from `lean/`). Do not edit
   `lean/CylChess.lean` (the main session wires the imports). Record time and peak memory
   (`/usr/bin/time -l`).

## Report (final message, under 400 words)

For each task: done / not done, the theorem names and exact statements, `decide` or `native_decide`, build time and
peak memory, and anything that turned out different from what the referees said. List every file you changed.
