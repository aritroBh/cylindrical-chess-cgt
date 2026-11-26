import CylChess.Claims.Common
import CylChess.Search

/-!
# L9: Theorem `thm:cut` (`dist/tog/sections/02_rules.tex`)

> "A pawn position on the n-file cylinder with at least one empty file has the same value as the position on the
> flat board of n-1 files obtained by cutting the cylinder open along that file."

## What is checked

`cut n e P` is the flat position of `n - 1` files obtained from a cylinder position `P` whose file `e` is empty:
file `f` becomes file `(f - e - 1) mod n`, so the file after `e` is the first one and the file before `e` the
last; ranks, directions and the e.p. square (relabelled) are unchanged, and the pawn lists are sorted again.

The family `F` (`fam`) for the parameters `(n, r, k, s)`, a number of files, ranks, a bound on the number of
pawns and a setting `s`, and an empty file `e`, is the explicit list of all normal-form positions on the cylinder
`C_n` with `r` ranks in which file `e` holds no pawn, no white pawn is on rank 1, no black pawn on rank `r`, and at
most `k` pawns stand, together (for an e.p. option of `s` other than `off`) with every such position that carries a
real e.p. right (the normal form of `Rules.lean`). It is produced by `gen`, which `famBrute` cross-checks against
a brute-force filter of all 3^(n r) fillings of the board on three tiny boards.

For every position `P` of `F`, every setting, both colours `c`, `step` checks:

1. (closure) every move of `c` from `P` lands in `F` (so in particular file `e` stays empty);
2. (one step of the induction) `cut`, applied to the list `moves cyl P c`, gives, as a set, the list
   `moves flat (cut P) c`;
3. `hasPassed` for both colours and `classify` (for each mover) agree on `P` and `cut P`;
4. the e.p. right agrees: `cut` of the e.p. square is the e.p. square of `cut P`, `cut P` is again in normal form
   (`Position.normalize` leaves it fixed), and for every pawn `epCapturable` agrees;
5. the components of `P`, after `cut`, are as a set the components of `cut P` (the sum model of
   `Game.lean` splits a position along its empty files after every move, so this is needed too).

## Why this gives equal values on all of `F`

Which file stays empty: a pawn changes file only by capturing, onto the square of an enemy pawn on a
neighbouring file (the target holds a pawn, so is not on an empty file), or by e.p. onto the skipped square, which
lies on the file of the enemy pawn that has just double-stepped (again a file with a pawn). Straight steps keep
the file. Hence a move never puts a pawn on file `e`, and file `e` stays empty in every position reached from `P`.
The number of pawns never grows and no pawn leaves the allowed ranks, so a move of a position of `F` is a position
with the same `e` empty and at most `k` pawns: `F` is closed under moves. (Item 1 checks this for the explicit
list, by hash lookup, without trusting the argument.)

The value of a position is defined from the options `Comp.options` of `Game.lean`: the moves `moves`, then
`verdict` (passed pawns, race) and the split `components`. Items 2 to 5 say that for `P` in `F` the options of
`P` and of `cut P` correspond one to one up to `cut`: same moves (as sets), same verdict on each move (item 3 for
the child, which is in `F` by item 1), same split (item 5). By induction on the fuel of `Game.wins`
(`wins f (P :: rest) c = wins f (cut P :: rest') c` where `rest'` is the `cut` of the rest, when every component is in
`F`), the outcomes of every sum `P + T` and `cut P + T` agree for every game tree `T`, for both movers, so
`P` and `cut P` have the same value. The induction itself is **not** formalised in Lean here; what is formalised is the
finite one-step statement it uses. (The e.p. right that survives in a sum across components is the other reading
of `Game.lean`; it concerns only the flag, which `cut` relabels along with its component.)

## The second check (weaker)

`valueAgree` compares `Search.outcome` of `P + T` on the cylinder with that of `cut P + T` on the flat board, for
`T` in `0, *1, *2, 1, -1` and both movers, in all nine settings, on a smaller family. It needs `BIG` only to exceed the
number of moves a side can make (stated at the theorem), so `big` is set to `20`. It is weaker: five test games,
not all games, and the memoized `Search`, not the specification.
-/
namespace CylChess.Claims.Cut

/-- File `f` of the cylinder with `n` files after cutting along the empty file `e`. -/
def cutFile (n e f : Nat) : Nat := (f + n - e - 1) % n

def cutPawn (n e : Nat) (p : Pawn) : Pawn := { p with file := cutFile n e p.file }

/-- The flat position of `n - 1` files obtained by cutting the cylinder along the empty file `e`. -/
def cut (n e : Nat) (P : Position) : Position :=
  { white := sortBy Pawn.before (P.white.map (cutPawn n e))
    black := sortBy Pawn.before (P.black.map (cutPawn n e))
    ep := P.ep.map fun q => (cutFile n e q.1, q.2) }

def cylB (n r : Nat) : Board := { files := n, ranks := r, topology := .cylinder }
def flatB (n r : Nat) : Board := { files := n - 1, ranks := r, topology := .flat }

/-! ## The family -/

/-- All ways to fill the squares `sqs` (files ascending, ranks ascending in each file) with at most `k` pawns on
a board of `r` ranks: no white pawn on rank 1, no black pawn on rank `r`. The lists come out sorted by
`Pawn.before`. -/
def fill (r : Nat) : List Square → Nat → List Pawn → List Pawn → List (List Pawn × List Pawn)
  | [], _, w, b => [(w.reverse, b.reverse)]
  | (f, rk) :: rest, k, w, b =>
    fill r rest k w b ++
    (if 0 < k && 2 ≤ rk then fill r rest (k - 1) (⟨f, rk, true⟩ :: w) b else []) ++
    (if 0 < k && rk < r then fill r rest (k - 1) w (⟨f, rk, false⟩ :: b) else [])
termination_by sqs => sqs.length

/-- Base positions (no e.p. right) with at most `k` pawns, none on file `e`, of the cylinder with `n` files and
`r` ranks. -/
def base (n r k e : Nat) : List Position :=
  let sqs := ((List.range n).filter (· != e)).flatMap fun f => (List.range r).map fun i => (f, i + 1)
  (fill r sqs k [] []).map fun (w, b) => ⟨w, b, none⟩

/-- The family `F` for the setting `s`: base positions, and (if e.p. is on) every normal-form position with a real
e.p. right. -/
def fam (s : Settings) (n r k e : Nat) : List Position :=
  let bd := cylB n r
  (base n r k e).flatMap fun P =>
    P :: (if s.ep == EpRule.off then [] else
      ((P.white ++ P.black).filterMap fun q =>
        let Q := Position.normalize s bd { P with ep := some q.sq }
        if Q.ep.isSome then some Q else none))

def sameSet (a b : List Position) : Bool := a.all b.contains && b.all a.contains

def emptyFile (e : Nat) (P : Position) : Bool := (P.white ++ P.black).all (·.file != e)

/-- Everything checked for one position `P` of the family, for one setting `s`. `inF` is membership of the
family (a hash set of the explicit list). -/
def step (s : Settings) (n r e : Nat) (inF : Position → Bool) (P : Position) : Bool :=
  let cb := cylB n r
  let fb := flatB n r
  let cP := cut n e P
  emptyFile e P && Position.valid cb P && Position.valid fb cP
    && Position.normalize s cb P == P && Position.normalize s fb cP == cP
    && (components cb P).length == (components fb cP).length
    && sameSet ((components cb P).map (cut n e)) (components fb cP)
    && [Color.white, .black].all fun c =>
      hasPassed s cb P c == hasPassed s fb cP c
      && classify s cb P c == classify s fb cP c
      && (P.pawns c).all (fun p => epCapturable cb P c p == epCapturable fb cP c (cutPawn n e p))
      && (moves s cb P c).all inF
      && sameSet ((moves s cb P c).map (cut n e)) (moves s fb cP c)

/-- Check one family `(n, r, k)` with the empty file `e`, in setting `s`; also report its size. -/
def famCheck (s : Settings) (n r k e : Nat) : Bool :=
  let F := fam s n r k e
  let set : Std.HashSet Position := F.foldl (fun h P => h.insert P) {}
  F.all (step s n r e (set.contains ·))

def famSize (s : Settings) (n r k e : Nat) : Nat := (fam s n r k e).length

/-- Check `(n, r, k)` for every empty file `e` and every setting. -/
def allCheck (n r k : Nat) : Bool :=
  (List.range n).all fun e => allSettings.all fun s => famCheck s n r k e

/-! ### The generator against a brute-force filter (tiny boards) -/

/-- Every filling of the `n x r` board by `{empty, white, black}` (3^(n r) of them), kept when it is a base
position of the family (no pawn on `e`, white not on rank 1, black not on rank `r`, at most `k` pawns). -/
def brute (n r k e : Nat) : List Position :=
  let sqs := (List.range n).flatMap fun f => (List.range r).map fun i => (f, i + 1)
  let all : List (List Nat) := sqs.foldr (fun _ acc => acc.flatMap fun l => [0 :: l, 1 :: l, 2 :: l]) [[]]
  all.filterMap fun a =>
    let cells := sqs.zip a
    let w := (cells.filter (·.2 == 1)).map fun (q, _) => (⟨q.1, q.2, true⟩ : Pawn)
    let b := (cells.filter (·.2 == 2)).map fun (q, _) => (⟨q.1, q.2, false⟩ : Pawn)
    if w.length + b.length ≤ k && (w ++ b).all (·.file != e) && w.all (·.rank != 1) && b.all (·.rank != r)
    then some ⟨w, b, none⟩ else none

def famBrute (n r k : Nat) : Bool :=
  (List.range n).all fun e => sameSet (base n r k e) (brute n r k e) && (base n r k e).length == (brute n r k e).length

/-! ## The second check: outcomes in sums with test games -/

def testGames : List Tree := [Tree.zero, Tree.star 1, Tree.star 2, Tree.dy 0, (Tree.dy 0).neg]

def valueAgree (s : Settings) (n r k e : Nat) : Bool :=
  let eC : Env := { s := s, b := cylB n r, big := 20 }
  let eF : Env := { s := s, b := flatB n r, big := 20 }
  (fam s n r k e).all fun P =>
    testGames.all fun t => [Color.white, .black].all fun c =>
      let a := Search.outcome eC 100 P t c
      a.isSome && a == Search.outcome eF 100 (cut n e P) t c

def valueAll (n r k : Nat) : Bool :=
  (List.range n).all fun e => allSettings.all fun s => valueAgree s n r k e

/-- Non-vacuity: the family for `(4, 8, 3)` in the default setting has positions with a real e.p. right, positions in
which both sides have a passed pawn (a race), and positions in which exactly one side has one. -/
def nonVacuous : Bool :=
  let s := Settings.default
  let F := fam s 4 8 3 0
  let cb := cylB 4 8
  F.any (·.ep.isSome) &&
  F.any (fun P => hasPassed s cb P .white && hasPassed s cb P .black) &&
  F.any (fun P => hasPassed s cb P .white && !hasPassed s cb P .black)

/-! ## The theorems -/

/-- The generator `base` equals a brute-force filter of all 3^(n r) fillings, on three tiny boards. -/
theorem fam_generator_brute : famBrute 3 3 6 = true ∧ famBrute 3 4 4 = true ∧ famBrute 4 3 4 = true := by
  native_decide

theorem fam_nonvacuous : nonVacuous = true := by native_decide

/-! One-step statement (items 1 to 5 above) on the families `F(n, r, k)`: all empty files `e`, all nine settings. -/

theorem cut_step_3_5_6 : allCheck 3 5 6 = true := by native_decide
theorem cut_step_3_8_4 : allCheck 3 8 4 = true := by native_decide
theorem cut_step_4_5_4 : allCheck 4 5 4 = true := by native_decide
theorem cut_step_4_6_4 : allCheck 4 6 4 = true := by native_decide
theorem cut_step_4_8_3 : allCheck 4 8 3 = true := by native_decide
theorem cut_step_5_5_4 : allCheck 5 5 4 = true := by native_decide
theorem cut_step_5_6_3 : allCheck 5 6 3 = true := by native_decide
theorem cut_step_5_8_3 : allCheck 5 8 3 = true := by native_decide
theorem cut_step_6_8_2 : allCheck 6 8 2 = true := by native_decide
theorem cut_step_7_5_3 : allCheck 7 5 3 = true := by native_decide
theorem cut_step_8_5_2 : allCheck 8 5 2 = true := by native_decide

/-! The second, weaker check: outcomes in sums with `0, *1, *2, 1, -1`, cylinder against cut flat board. -/

theorem cut_value_3_5_4 : valueAll 3 5 4 = true := by native_decide
theorem cut_value_4_5_3 : valueAll 4 5 3 = true := by native_decide
theorem cut_value_5_4_3 : valueAll 5 4 3 = true := by native_decide
theorem cut_value_4_6_3 : valueAll 4 6 3 = true := by native_decide

#print axioms fam_generator_brute
#print axioms fam_nonvacuous
#print axioms cut_step_3_5_6
#print axioms cut_step_3_8_4
#print axioms cut_step_4_5_4
#print axioms cut_step_4_6_4
#print axioms cut_step_4_8_3
#print axioms cut_step_5_5_4
#print axioms cut_step_5_6_3
#print axioms cut_step_5_8_3
#print axioms cut_step_6_8_2
#print axioms cut_step_7_5_3
#print axioms cut_step_8_5_2
#print axioms cut_value_3_5_4
#print axioms cut_value_4_5_3
#print axioms cut_value_5_4_3
#print axioms cut_value_4_6_3

end CylChess.Claims.Cut
