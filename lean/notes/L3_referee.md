# L3 referee report: `Game.lean`, `Search.lean` and the three claims

Referee: independent, blind first (paper read and claims written down before any Lean; `notes/L3.md` read last).
Scratch file: `lean/scratch/L3Referee.lean` (run: `cd lean && nice -n 15 lake env lean scratch/L3Referee.lean`,
about 25 s, 0.55 GB). No other file was edited; nothing was built or committed.

## 0. The claims as I read them in the paper (before the Lean)

* **Value.** `G = v` iff `G - v` is a second-player win: in `G + (-v)` the player to move loses, for both
  movers (§2.2). The pawn model is the sum model `S`: a component whose move gives exactly one side a passed pawn
  becomes the integer `+BIG` / `-BIG` (`BIG = 256`); both sides passed is a race, scored by the rule; otherwise the
  component is re-split along empty files and the components add.
* **`thm:star2seven`.** Ordinary 8x8 board (pawns on files a-d), default setting (count, e.p.-aware).
  A = W a4 b3 d2 d3 / B a7 b7 c5, B = W b4 c2 d2 / B a6 a7 c6 d5. (i) both `= *2`; (ii) neither `= *2` in the
  three e.p.-off settings nor in the three opponent-rule settings (five settings in all). Value in the pawn model (S);
  §5 adds that S and W agree on this `*2`, which is a separate remark, not part of the theorem.
* **`thm:eighth`.** Pawn model, ordinary board, W a2 b2 b3 / B a5 a6 b6 `= {0 | 1/4} = 1/8` in all nine settings;
  and, for each e.p. option, for every function giving a winner to each race position (a race position = position
  reached by a move that gives both sides a passed pawn, with the side that moved), the value is still `1/8`.
  The three race rules are three such functions, so "every assignment" contains "nine settings".
* **`prop:sumcounter`.** C_8 (8 files, 8 ranks, a-h joined), e.p. off, count rule,
  X = W b2 d4 g3 h5 / B a7 c7 f7 g4. X is one component (file e empty, the arc f-g-h-a-b-c-d); `S(X)` is a Black
  win whoever starts (outcome R); `W(X)` is a first-player win (outcome N). "X is not HSS" is a further claim.

## 1. Answers a-f

**a. `IsValue`, negation, the trees.** Correct. `isValue` requires no passed pawn at the root and
`outcome ... v.neg .white = some false` and the same for `.black`: exactly "the player to move loses in
`G + (-v)`, either mover". `Tree.neg (node l r) = node (negs r) (negs l)` swaps the players recursively; correct.
`stars 0 = []`, `stars (k+1) = stars k ++ [star k]`, so `star 2 = node [0, *] [0, *]` with
`0 = node [] []`, `* = node [0] [0]`: the canonical `*2 = {0,* | 0,*}` (scratch also prints option counts 2, 2).
`dy 0 = {0 |} = 1`, `dy 1 = {0 | 1}`, `dy 2 = {0 | 1/2}`, `dy 3 = {0 | 1/4}`: `eighth` is the canonical `1/8`, the
form in Table `tab:targets`. `neg eighth = {-1/4 | 0}`, as it should be.

**b. BIG, fuel, `NotValue`.** `Comp.num n` gives White one option `n-1` if `n > 0` and Black one option `n+1` if
`n < 0`: the canonical integer, i.e. the winner has `|n|` free moves and the loser none there, as §2.3 says.
A decided pawn component becomes `num (±e.big)`, `big = BIG = 256` by default (all claim environments use the
default through `Claims.env`). Fuel cannot make a theorem true wrongly: `Game.wins` returns `none` at fuel 0,
`anyOpt` returns `some true` only if some option is `some true` and `some false` only if all options are
`some false`; by induction on the fuel every `some b` is the true outcome. `isValue` needs two `some false`,
`notValue` a `some true`, and the S/W theorems state `= some b`; so running out of fuel can only make them fail.
(Scratch F1: with fuel 2 on a `*2` position both `isValue` and `notValue` are false.) `NotValue` is
"some mover wins `G - v`", which for a finite game is exactly `G - v` not in P, i.e. `G ≠ v`; with enough fuel it is
the negation of `IsValue` (up to the root-passed-pawn conjunct, which no claim position triggers). One fuel remark:
fuel 400 is *not* "more than everything" in the spec when a sum holds both `+256` and `-256` (512 plies); the spec
then answers `none` on those lines. This is harmless (soundness above), only a mis-statement in `Common.lean`'s
comment. Scratch H13: the spec proves value `257` with fuel 600 and `Search` with fuel 400 does not (needs 600).

**c. Statements vs the paper, square by square.** All squares checked by hand against the `.tex`:
posA = a4 b3 d2 d3 / a7 b7 c5, posB = b4 c2 d2 / a6 a7 c6 d5, posG = a2 b2 b3 / a5 a6 b6,
posGMirror = files a, b exchanged, posX = b2 d4 g3 h5 / a7 c7 f7 g4; `sqr` maps a to file 0 and white pawns move up.
Boards: `flat8` (8 files, 8 ranks by default, flat) for A, B and 1/8, matching "files a-d of the ordinary board" and the
"ordinary board" caption of Fig. `fig:eighth`; `cyl8` for X. Settings: `Settings.default = ⟨aware, count⟩`; the
five negative settings of `thm:star2seven` are exactly `star2seven_not_ep_off` (off x count/mover/opponent) and
`star2seven_not_opponent` (aware/textbook/off x opponent); `allSettings` is the nine. Side to move: values for
both movers; "first-player win" = both movers `some true` in `W`; "black win whoever starts" = White to move
`some false`, Black to move `some true` in `S`. Quantifiers match. `star2seven_table_extra` (the other three
`*2` rows of Table `tab:star2_settings`) also matches the table.

**d. "Every assignment".** The formal reading (all `2^k` tables over the pairs (component position after the move,
mover) found by `raceKeys`, for each e.p. option) is at least as strong as the paper's: a table keyed by position
alone is a special case, and pairs the walk might miss answer `none`, which (see b) can only make a definite
answer hold for every completion. But the documentation's reason is wrong: `L5_Eighth.lean` says "a race reached that
the table does not cover makes the answer unknown, so the check also shows that the table is complete", and `L3.md`
decision 6 says a missing pair "would make the check fail". Not so: an unassigned race inside a branch the winner
avoids does not stop the answer being found. I checked the extreme case. With the **empty** table
(`race := fun _ _ => none`, every race unknown) the *specification* proves `IsValue ... posG Tree.eighth` for all
three e.p. options (scratch, about 2 s each). By the soundness of `none` this says the value is `1/8` for every
outcome of every race, even path-dependent ones: a stronger statement than the paper's, on the spec, with no
`Search` and no `2^k` loop. So the race positions never decide the value; `eighth_race_counts` is irrelevant to the
claim. (Control: with the empty table posA is undecided, so `none` is not vacuous.)

**e. `S(X)` vs `W(X)`.** `S` = `Game.wins` on `components pos`: after a move the moved component becomes `±BIG` if a
side has a passed pawn in it (race rule if both), otherwise it is re-split along empty files; the components add.
That is the paper's sentence word for word. `W` stops at the first move whose result has a passed pawn and gives the win to
the side that has it (race rule if both). For a single component the two differ exactly as the paper says: in `S`,
once a move splits X, a decided component is a number `±256` and play goes on in the others (a `+256` can be cancelled
by a later `-256`); in `W` the first passed pawn ends the game. The e.p. bookkeeping also differs (a right lasts in its
component in `S`, lapses after one move in `W`), but X is e.p. off. This is the paper's distinction.

**f. `Search`.** No defect found. The memo key is `(norm cs, mover)`: the full component list including every
`Position` (pawns *and* the `ep` field), every number and the tree; the side to move is in the key. Hash collisions
are not equalities: `Std.HashMap` compares keys with `BEq`, here the structural `DecidableEq`-derived equality on
`Position` and derived `BEq` on `Comp`/`Tree`. Fuel is not in the key, but only definite answers are stored, and those
are fuel-independent. The `Env` (race table, BIG) is not in the key, but each `run`/`isValue` call starts with an empty
memo; in `eighthForAllAssignments` each table is a fresh call. `norm` merges integer components and drops `0`
components: not syntactically the spec, but value-preserving (`n + m` and `n - m` are integer games; replacing a
component by an equal game keeps the outcome). `Search.W` memoizes `(Position, mover)` with `ep` included.
`SearchAgrees` is a reasonable test (3378 positions x 8 outcomes, non-vacuous) but small boards only.
Trust: `sumcounter_S` I trust well: `sumcounter_S_spec_big24` gives the same outcomes on the spec, and the BIG-only
difference is covered by the bound (each pawn move advances at least one rank: at most 6+4+5+3 = 18 White moves and
6+6+6+3 = 21 Black moves from X, so 24 exceeds them; the paper's convention needs nothing more). `eighth_all_assignments`
I would not need to trust at all: the empty-table spec check in d replaces it.

## 2. Hand-worked positions (step 4)

All values in S (`isValue` against the candidate list 0, *, *2, *3, 1, -1, 2, 1/2, 1/4, 1/8, up, down, {0|-1},
tiny-1; "accepted" lists every candidate accepted). Spec and `Search` gave identical results on every line.

| # | Board, setting | Position | Hand value | Spec | Search |
|---|---|---|---|---|---|
| H1 | flat 1 file, 4 ranks, default | W a2 / B a3 | 0 (no moves) | 0 | 0 |
| H2 | 1 file, 5 ranks | W a2 / B a4 | * (one shared gap square) | * | * |
| H3 | 1 file, 6 ranks | W a2 / B a5 | *2 = {*, 0 \| *, 0} (single or double step) | *2 | *2 |
| H4 | 1 file, 8 ranks | W a2 a4 / B a5 | 1 (only a2-a3) | 1 | 1 |
| H5 | 1 file, 8 ranks | W a4 / B a5 a7 | -1 | -1 | -1 |
| H6 | 1 file, 8 ranks | W a2 a5 / B a6 | 2 = {1, 0 \|} | 2 | 2 |
| H7 | flat 3 files, 6 ranks | W a2 c2 / B a5 c4 | *2 + * = *3 (two components) | *3 | *3 |
| H8 | flat 3 files | W a2 a4 c4 / B a5 c5 c7 | 1 + (-1) = 0 | 0 | 0 |
| H9 | 1 file, 7 ranks | W a2 / B a5 | up = {0, * \| *} (worked state by state) | up | up |
| H10 | 1 file, 7 ranks | W a3 / B a6 | down = {* \| 0, *} | down | down |
| H11 | 1 file, 7 ranks | W a2 / B a6 | {down, * \| up, *} = 0 | 0 | 0 |
| H12 | flat 2 files, default | W a2 / B b4 (Fig. 1(a)) | 0 | 0 | 0 |
| H13 | flat 2 files | W a2 b3 / B b4 (§2.4) | aware/count 0; aware/mover 0; aware/opponent: White first wins, Black first loses (b4xa3 race goes to White); textbook/count {256 \|} = 257; off/count 257; textbook/opponent 257 | 0; 0; (W wins, B loses); 257 (fuel 600; with BIG = 4 the value is 5, also matched); 5 with BIG = 4; 5 with BIG = 4 | same (257 needs fuel 600) |
| H14 | flat 2 files, textbook | W a2 / B b4 | count 0; opponent 0; mover: a2-a4 race goes to the mover, White first wins, Black first loses | 0; 0; (W wins, B loses) | same |
| H15 | C_8, all nine settings | W a4 h3 / B a5 h6 (Fig. 1(b)) | 0 (h3-h4 a5xh4 across the seam; h6-h5 a4xh5) | 0 in all nine | 0 in all nine |
| H16 | C_8, default | W a4 h2 / B a5 h6 | 1 = {0 \| big} | 1 | 1 |
| H17 | F_8, default | W a4 h3 / B a5 h6 | locked a-file 0 + h-file {* \| *} = 0 | 0 | 0 |
| W1 | 1 file | W a2 alone (passed, won) | no value in `IsValue`'s sense (root race/won excluded) | none accepted | - |
| F1 | 1 file, 6 ranks, fuel 2 | H3 | undecided: neither IsValue nor NotValue | false, false | - |

Paper-derived checks (the paper's value, not re-derived by me in full): Fig. 1(c) on C_8 = tiny-1 (accepted);
after a5xh4 = {0 \| -1} (accepted); posG after a2-a4 = 0, after a2-a3 = *, after b6-b5 = 1/4 (all accepted);
C_8 W a5 h2 / B a6 h7 = 2 in default (accepted) and up+up+* with e.p. off (accepted against the tree sum
up+up+*, under off/count, off/mover, off/opponent; not equal to up+up, up or up*). My first attempt used
{0, up \| 0} as the canonical form of up+up+*; it is not, and both programs correctly rejected it.

No mismatch between hand values and either program.

## 3. Attempts to break it

1. **E.p. rights in sums (the main risk I found in `L3.md`).** `L3.md` decision 2 says the e.p.-in-sums reading
   "does not matter: A, B and the 1/8 position are one component". That is wrong as a reason: they are one component
   *at the root*. From A and from B, 735 open positions are reachable (either side moving), and 18 of each have two
   or more components *and* a live e.p. right (e.g. after d3-d4 c5xd4 file c is empty). There the `S` reading
   (the right survives moves elsewhere) differs from the chess rule. I wrote a variant search in which every move
   clears the e.p. rights of all other components and reran: A and B are still `*2` in the default setting and in
   aware/mover, textbook/count, textbook/mover, and still not `*2` under aware/opponent and textbook/opponent
   (e.p. off is unaffected). The 1/8 position never reaches such a position (0 found). So the claims do not depend on
   this reading; the note's reason should be replaced by this check.
2. **Race table emptied** (d above): 1/8 survives with every race unknown, on the spec.
3. **Spec extremes for the other e.p. options.** `search_agrees_eighth` checks all-White/all-Black tables on the spec
   only for the aware option; I ran them for textbook and off on the spec: all `true`.
4. **W(A), W(B)**: first-player wins for both movers, consistent with `*2` (no value claim made for W).
5. Fuel, hash collisions, the memo key, stale memo across environments: see b and f; nothing found.

## 4. Mismatches between a theorem statement and the paper

None in the statements. Points of scope or documentation:

* `eighth_all_assignments` rests on `Search`; its docstring and `L3.md` decision 6 give a wrong reason for
  completeness (see d). The claim itself is correct and follows from a stronger spec check.
* `L3.md` decision 2 ("none of the claims depends on this") has a false premise for A and B (see 3.1); the
  conclusion is true by the variant check.
* `Common.lean`: "fuel 400 = more than BIG plus the longest pawn game plus the tree" is not true of the spec when
  `+256` and `-256` coexist; harmless.
* `thm:star2seven` and `thm:eighth` are checked in `S` only (the pawn model); §5's remark that `W` agrees is not
  formalised (and `W(X) + *h` cannot be expressed with the Lean `W`). The theorems do not claim it, so this is not a
  mismatch.
* "X is not HSS" (`prop:sumcounter`) is not formalised; the Lean theorem is the outcome part only.
* Kernel coverage: A with Black to move is native only.

## 5. What must change before citing

Required:
1. Fix the documentation of `eighth_all_assignments` (`L5_Eighth.lean` header and `eighthForAllAssignments`, `L3.md`
   decision 6): a missing race pair does not make the check fail; completeness of `raceKeys` is irrelevant because
   `none` is sound for all completions.
2. Fix `L3.md` decision 2: A and B do reach multi-component positions with live e.p. rights; say that the claims
   were rechecked under the chess e.p. rule in sums with the same results (or add that check as a theorem).

Recommended (would raise the trust level):
3. Replace or supplement `eighth_all_assignments` by a spec theorem
   `∀ ep, IsValue { s := ⟨ep, .count⟩, b := flat8, race := fun _ _ => none } fuel posG Tree.eighth`
   (cheap; probably kernel-checkable) and a short lemma that a `some b` from `Game.wins` under a partial race
   oracle is the answer under every total oracle extending it (induction on fuel). This removes `Search` and
   the informal monotonicity remark from L5 entirely.
4. Correct the fuel comment in `Common.lean`.
5. When citing, say "in the sum model S" for the `*2` and `1/8` theorems, and "outcome part" for `prop:sumcounter`.

## 6. `notes/L3.md`, its list of doubts

1. *`sumcounter_S` and `eighth_all_assignments` rest on `Search`.* For L6 the spec run with BIG = 24 plus the move
   bound closes the gap in substance. For L5 the doubt can be removed outright (recommendation 3).
2. *`native_decide`.* Fair. The negative L4 claims, A-black, and eight settings of L5 are compiler-trusted only.
   The empty-table L5 check would be small enough to try in the kernel.
3. *Not formalised: HSS, monotonicity, the ⇑* value.* Correct list; monotonicity becomes unnecessary (d). I checked
   the ⇑* value in scratch (up+up+* with e.p. off, three rules): it holds in `S`.
4. *L1 D10/D5/D8 do not touch these claims.* Not re-examined (Rules taken as given).
5. *Python flags.* No comment.
Missing from the list: the e.p.-in-sums premise (3.1) and the wrong completeness reason (d).

## 7. Verdicts

* **`thm:star2seven`** (`star2seven_default`, `_not_ep_off`, `_not_opponent`): **says what the paper says**
  (value in the sum model S, ordinary board, default setting; the five negative settings). Robust to the e.p.-in-sums
  reading. Trust: native_decide; three of four default outcomes also kernel-checked.
* **`thm:eighth`** (`eighth_nine_settings`, `eighth_all_assignments`): **says what the paper says**; the
  all-assignments part is at least as strong as the paper's reading. Its proof rests on `Search` and its stated
  completeness argument is wrong, but the claim holds on the specification by a stronger check (every race left
  unknown).
* **`prop:sumcounter`** (`sumcounter_shape`, `sumcounter_W`, `sumcounter_S`): **says something weaker**, only in
  that "X is not HSS" is not formalised; the single-component, S-outcome R and W-outcome N parts say what the paper says.
