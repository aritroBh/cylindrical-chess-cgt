import Std.Data.HashMap
import Std.Data.HashSet

/-!
# Dawson's chess on a 3 x n strip and on the 3 x n cylinder: rules and searches

Source: `dist/tog/sections/11_dawson.tex`. The rules, quoted:

> "Dawson's chess is played on a 3 x n board with white pawns on rank 1, black pawns on rank 3 and rank 2
> empty. Pawns move and capture as in chess, captures are compulsory, and no pawn can double-step or promote.
> The last player to move wins; in the misère form that Dawson posed, the last player loses."

This file takes the **normal** convention (the last player to move wins, so a player with no move loses), which
is the one the Grundy statements of the paper use ("the first player wins the ordinary 3 x n board exactly when
g(n) != 0"). Misère is not treated.

Everything is written from the pawn rules; the octal game 0.137 (`g`, below) appears only as the thing the
results are compared with.

* Squares: file `f` (`0 .. n-1`), rank index `r` (`0, 1, 2` for ranks 1, 2, 3). A position is the list of the
  `3 n` cells, file by file, rank 1 first.
* A white pawn moves one square straight up onto an empty square, or captures one square diagonally up onto a
  black pawn; a black pawn does the same downwards. A pawn on its last rank has no move (nothing promotes).
  There is no double step (no room), hence no en passant.
* "Captures are compulsory": a side that has a capture must capture (any capture).
* On the cylinder the file `n-1` is beside file `0` (the paper's cylinder; `n >= 3`). On the strip it is not.
* A side with no move loses (normal play).

Searches are by recursion on a fuel (no `partial`). An answer `some _` is the true answer whatever the fuel; `none`
means the fuel ran out.
-/
namespace CylChess.Dawson

/-! ## The rules -/

inductive Cell | e | w | b
  deriving DecidableEq, Hashable, Repr

inductive Side | white | black
  deriving DecidableEq, Hashable, Repr

def Side.other : Side → Side
  | .white => .black
  | .black => .white

/-- The pawn of a side. -/
def Side.pawn : Side → Cell
  | .white => .w
  | .black => .b

/-- The rank index a pawn of this side reaches in one step from rank index `r` (`none`: off the board). White
moves towards rank 3, black towards rank 1. -/
def Side.fwd : Side → Nat → Option Nat
  | .white, r => if r + 1 ≤ 2 then some (r + 1) else none
  | .black, r => if 1 ≤ r then some (r - 1) else none

/-- A board: `n` files; `wrap = true` is the cylinder (files `n-1` and `0` are beside each other). -/
structure Board where
  n : Nat
  wrap : Bool

def Board.strip (n : Nat) : Board := ⟨n, false⟩
def Board.cyl (n : Nat) : Board := ⟨n, true⟩

/-- The files beside `f`: "On a cylinder every file is alike" (§ Dawson). -/
def Board.nbrs (b : Board) (f : Nat) : List Nat :=
  (if f + 1 < b.n then [f + 1] else if b.wrap then [0] else []) ++
  (if 0 < f then [f - 1] else if b.wrap then [b.n - 1] else [])

abbrev Pos := List Cell

def Pos.at (p : Pos) (f r : Nat) : Cell := p.getD (3 * f + r) .e
def Pos.put (p : Pos) (f r : Nat) (c : Cell) : Pos := p.set (3 * f + r) c

/-- "white pawns on rank 1, black pawns on rank 3 and rank 2 empty": `n` untouched files. -/
def start (n : Nat) : Pos := (List.range n).flatMap fun _ => [Cell.w, .e, .b]

/-- The captures of side `s`: a pawn takes an enemy pawn one square diagonally forward. -/
def captures (bd : Board) (p : Pos) (s : Side) : List Pos :=
  (List.range bd.n).flatMap fun f => (List.range 3).flatMap fun r =>
    if p.at f r == s.pawn then
      match s.fwd r with
      | none => []
      | some r' => (bd.nbrs f).filterMap fun g =>
          if p.at g r' == s.other.pawn then some ((p.put f r .e).put g r' s.pawn) else none
    else []

/-- The pushes of side `s`: a pawn steps one square straight forward onto an empty square. -/
def pushes (bd : Board) (p : Pos) (s : Side) : List Pos :=
  (List.range bd.n).flatMap fun f => (List.range 3).flatMap fun r =>
    if p.at f r == s.pawn then
      match s.fwd r with
      | none => []
      | some r' => if p.at f r' == .e then [(p.put f r .e).put f r' s.pawn] else []
    else []

/-- All moves of side `s`: "captures are compulsory", so if there is a capture only captures are legal. -/
def moves (bd : Board) (p : Pos) (s : Side) : List Pos :=
  let c := captures bd p s
  if c.isEmpty then pushes bd p s else c

/-! ## The outcome: the specification (naive) and the memoized search -/

def anyOpt : List (Option Bool) → Option Bool
  | [] => some false
  | o :: os =>
    match o with
    | some true => some true
    | some false => anyOpt os
    | none => match anyOpt os with | some true => some true | _ => none

/-- Normal play, naive recursion: does the side `s` to move win? (A side with no move loses.) -/
def wins (bd : Board) : Nat → Pos → Side → Option Bool
  | 0, _, _ => none
  | f + 1, p, s => anyOpt ((moves bd p s).map fun q => (wins bd f q s.other).map (!·))

def Cell.code : Cell → Nat
  | .e => 0
  | .w => 1
  | .b => 2

/-- An injective code of (position, side to move) for hashing (positions of one board have one length). -/
def key (p : Pos) (s : Side) : Nat :=
  2 * p.foldl (fun a c => 3 * a + c.code) 0 + (match s with | .white => 0 | .black => 1)

abbrev Memo := Std.HashMap Nat Bool
abbrev M := StateM Memo

def anyM (os : List (M (Option Bool))) : M (Option Bool) :=
  match os with
  | [] => pure (some false)
  | o :: rest => do
    match ← o with
    | some true => pure (some true)
    | some false => anyM rest
    | none => do
      match ← anyM rest with
      | some true => pure (some true)
      | _ => pure none

/-- `wins`, memoized (only definite answers are stored, so a stored answer does not depend on the fuel). -/
def winsM (bd : Board) : Nat → Pos → Side → M (Option Bool)
  | 0, _, _ => pure none
  | f + 1, p, s => do
    let k := key p s
    match (← get)[k]? with
    | some b => pure (some b)
    | none =>
      let r ← anyM ((moves bd p s).map fun q => do return (← winsM bd f q s.other).map (!·))
      if let some b := r then modify (·.insert k b)
      pure r

def fastWins (bd : Board) (fuel : Nat) (p : Pos) (s : Side) : Option Bool :=
  (winsM bd fuel p s).run' {}

/-! ## Every reachable position: no pawn ever reaches its last rank -/

/-- A pawn stands on its last rank (a promotion square). -/
def promoted (p : Pos) : Bool :=
  (List.range (p.length / 3)).any fun f => p.at f 2 == .w || p.at f 0 == .b

structure Reach where
  seen : Std.HashSet Nat := {}
  promo : Bool := false
  complete : Bool := true

/-- Breadth-first walk over the (position, side to move) pairs reachable from `frontier`. -/
def reachLoop (bd : Board) : Nat → List (Pos × Side) → Reach → Reach
  | 0, fr, r => { r with complete := r.complete && fr.isEmpty }
  | f + 1, fr, r =>
    if fr.isEmpty then r else
    let (next, r') := fr.foldl
      (fun (acc : List (Pos × Side) × Reach) (ps : Pos × Side) =>
        (moves bd ps.1 ps.2).foldl
          (fun (acc : List (Pos × Side) × Reach) q =>
            let k := key q ps.2.other
            if acc.2.seen.contains k then acc
            else
              let st := acc.2
              ((q, ps.2.other) :: acc.1, { st with seen := st.seen.insert k, promo := st.promo || promoted q }))
          acc)
      ([], r)
    reachLoop bd f next r'

/-- Start from `start n` with `s` to move. -/
def reach (bd : Board) (fuel : Nat) (s : Side) : Reach :=
  reachLoop bd fuel [(start bd.n, s)] { seen := (({} : Std.HashSet Nat).insert (key (start bd.n) s)) }

/-! ## The impartial structure: a push and the forced captures that follow it -/

/-- "Counting each forced sequence as one move": from a position after a push, play out the forced captures
until the side to move has none. All choices are listed; `none` if the fuel ran out. -/
def settle (bd : Board) : Nat → Pos → Side → Option (List (Pos × Side))
  | 0, _, _ => none
  | f + 1, p, s =>
    let cs := captures bd p s
    if cs.isEmpty then some [(p, s)]
    else (cs.mapM fun q => settle bd f q s.other).map List.flatten

/-- The results of one push by `s` followed by the forced captures: the list of (position, side to move). -/
def afterPush (bd : Board) (fuel : Nat) (q : Pos) (s : Side) : Option (List (Pos × Side)) :=
  settle bd fuel q s.other

/-- The macro-moves of a quiet position (one where `s` has no capture): every push with its forced captures. -/
def macroMoves (bd : Board) (fuel : Nat) (p : Pos) (s : Side) : Option (List (Pos × Side)) :=
  if (captures bd p s).isEmpty then
    ((pushes bd p s).mapM fun q => afterPush bd fuel q s).map List.flatten
  else none

def mex (l : List Nat) : Nat := ((List.range (l.length + 1)).find? fun k => !l.contains k).getD 0

abbrev GMemo := Std.HashMap Nat Nat

/-- The Grundy value of a quiet position, from the macro-moves: `none` if the fuel ran out, if some
macro-move does not hand the turn to the opponent (the game would not be impartial), or if a reached position
is not quiet. -/
def grundyM (bd : Board) (fuel : Nat) : Nat → Pos → Side → StateM GMemo (Option Nat)
  | 0, _, _ => pure none
  | f + 1, p, s => do
    let k := key p s
    match (← get)[k]? with
    | some g => pure (some g)
    | none =>
      match macroMoves bd fuel p s with
      | none => pure none
      | some opts =>
        if !(opts.all fun o => o.2 == s.other) then pure none else
        let mut gs : List Nat := []
        for o in opts do
          match ← grundyM bd fuel f o.1 o.2 with
          | none => return none
          | some g => gs := g :: gs
        let g := mex gs
        modify (·.insert k g)
        pure (some g)

def grundy (bd : Board) (fuel : Nat) (p : Pos) (s : Side) : Option Nat :=
  (grundyM bd fuel fuel p s).run' {}

/-! ## The octal game 0.137 (the paper's equation `eq:dawson`) -/

/-- The list `[g(0), ..., g(n)]`, computed with `g(0) = 0`, `g(1) = 1` and, for `n >= 2`,
`g(n) = mex({g(n-2)} ∪ {g(a) xor g(b) : a + b = n - 3})`. -/
def gList : Nat → List Nat
  | 0 => [0]
  | n + 1 =>
    let prev := gList n
    let m := n + 1
    if m = 1 then prev ++ [1] else
    let ab := (List.range (m - 2)).map fun a => prev.getD a 0 ^^^ prev.getD (m - 3 - a) 0
    prev ++ [mex (prev.getD (m - 2) 0 :: ab)]

def g (n : Nat) : Nat := (gList n).getD n 0

/-- A direct statement of the recurrence, for `n >= 2`. -/
def gRec (n : Nat) : Nat :=
  mex (g (n - 2) :: (List.range (n - 2)).map fun a => g a ^^^ g (n - 3 - a))

/-! ## The ring rule: the expected position after a first move -/

/-- The cylinder position after side `s` has pushed on file `i` and the forced captures are over: file `i` is
blocked (white above its start square for a white first move, `[e, w, b]`; black below, `[w, b, e]`), the files
`i - 1` and `i + 1` are empty, the other `n - 3` files are untouched. -/
def afterRing (n i : Nat) (s : Side) : Pos :=
  (List.range n).flatMap fun f =>
    if f == i then (match s with | .white => [Cell.e, .w, .b] | .black => [.w, .b, .e])
    else if f == (i + 1) % n || f == (i + n - 1) % n then [.e, .e, .e]
    else [.w, .e, .b]

/-- The `i`-th push of side `s` from the start position (file `i`). -/
def pushAt (n i : Nat) (s : Side) : Pos :=
  (start n).put i (match s with | .white => 0 | .black => 2) .e |>.put i 1 s.pawn

/-- Statement (iii) of the ring rule on `n` files, first mover `s`: `s` has no capture at the start, its
first moves are exactly the `n` pushes `pushAt n i s`, and after each push, every choice of the forced captures
ends (fuel 20 is enough; `none` would fail the check) in `afterRing n i s` with the opponent of `s` to move. -/
def ringStructure (n : Nat) (s : Side) : Bool :=
  let bd := Board.cyl n
  captures bd (start n) s == [] &&
  pushes bd (start n) s == (List.range n).map (fun i => pushAt n i s) &&
  (List.range n).all fun i =>
    match afterPush bd 20 (pushAt n i s) s with
    | none => false
    | some rs => !rs.isEmpty && rs.all fun r => r == (afterRing n i s, s.other)

/-! ## The checks -/

/-- The paper's Grundy table for Dawson's chess (octal game 0.137), n = 0 .. 33, as printed in
`dawson/octal_300.txt` and listed in the literature (Guy-Smith). -/
def gKnown : List Nat :=
  [0,1,1,2,0,3,1,1,0,3,3,2,2,4,0,5,2,2,3,3,0,1,1,3,0,2,1,1,0,4,5,2,7,4]

def both : List Side := [.white, .black]

/-- (i) the first player wins the `n`-file cylinder iff `g(n-3) = 0`, whoever moves first; fast search. -/
def ringWins (n : Nat) : Bool :=
  both.all fun s => fastWins (Board.cyl n) 200 (start n) s == some (g (n - 3) == 0)

/-- (ii) the cylinder's Grundy value, from the pawn macro-moves, is `mex {g(n-3)}`, and the option after a push
on file `i` has Grundy value `g(n-3)`, computed from the pawn macro-moves too (every `i` for `n <= 12`, files 0 and
1 above, for time); for both first movers. -/
def ringGrundy (n : Nat) : Bool :=
  both.all fun s =>
    grundy (Board.cyl n) 40 (start n) s == some (mex [g (n - 3)]) &&
    (if n ≤ 12 then List.range n else [0, 1]).all fun i =>
      grundy (Board.cyl n) 40 (afterRing n i s) s.other == some (g (n - 3))

/-- The ordinary 3 x m board: the first player wins iff `g(m) != 0`, and the Grundy value from the pawn
macro-moves is `g(m)`. -/
def stripCheck (m : Nat) : Bool :=
  both.all fun s =>
    fastWins (Board.strip m) 200 (start m) s == some (g m != 0) &&
    grundy (Board.strip m) 60 (start m) s == some (g m)

/-- No pawn ever reaches its last rank, from either first mover; the walk over all positions finished. -/
def noPromotion (bd : Board) : Bool :=
  both.all fun s => let r := reach bd 200 s; r.complete && !r.promo

/-- The naive specification search (no memo) agrees with the answer `g(n-3) = 0`. -/
def ringWinsNaive (n : Nat) : Bool :=
  both.all fun s => wins (Board.cyl n) 60 (start n) s == some (g (n - 3) == 0)

def stripWinsNaive (m : Nat) : Bool :=
  both.all fun s => wins (Board.strip m) 60 (start m) s == some (g m != 0)

/-- The values `g` against the table, and the recurrence of the paper restated directly. -/
theorem g_table : (List.range 34).map g = gKnown := by decide +kernel

theorem g_recurrence : ∀ n ∈ List.range' 2 70, gRec n = g n := by decide +kernel

/-- The cylinders of 3 to 57 files that the first player wins are exactly those of the list of the paper
(`n = 3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57`), by `g`. -/
theorem ring_win_list :
    (List.range' 3 55).filter (fun n => g (n - 3) == 0) = [3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57] := by
  decide +kernel

/-- (i), n = 3 .. 20, from the pawn rules (memoized search). -/
theorem ring_outcome : ∀ n ∈ List.range' 3 18, ringWins n = true := by native_decide

/-- In that range the first player wins exactly for n = 3, 7, 11, 17. -/
theorem ring_win_range :
    (List.range' 3 18).filter (fun n => fastWins (Board.cyl n) 200 (start n) .white == some true) =
      [3, 7, 11, 17] := by native_decide

/-- (ii) and the Grundy value of the option, n = 3 .. 16 (the pawn-level Grundy search on the 13-file strip
is the cost). -/
theorem ring_grundy : ∀ n ∈ List.range' 3 14, ringGrundy n = true := by native_decide

/-- (iii) the structure: for n = 3 .. 20, both first movers. -/
theorem ring_structure : ∀ n ∈ List.range' 3 18, both.all (ringStructure n ·) = true := by native_decide

/-- The ordinary 3 x m board, m = 1 .. 15. -/
theorem strip_check : ∀ m ∈ List.range' 1 15, stripCheck m = true := by native_decide

/-- No promotion is ever reached, on the cylinders with n = 3 .. 14 and the strips with m = 1 .. 14. -/
theorem no_promotion :
    (∀ n ∈ List.range' 3 12, noPromotion (Board.cyl n) = true) ∧
    (∀ m ∈ List.range' 1 14, noPromotion (Board.strip m) = true) := by native_decide

/-- The naive specification search (kernel), small boards. -/
theorem ring_naive_kernel : ∀ n ∈ List.range' 3 4, ringWinsNaive n = true := by decide +kernel

theorem strip_naive_kernel : ∀ m ∈ List.range' 1 6, stripWinsNaive m = true := by decide +kernel

/-- The naive specification search against the memoized one, further (compiled). -/
theorem naive_native :
    (∀ n ∈ List.range' 3 6, ringWinsNaive n = true) ∧ (∀ m ∈ List.range' 1 9, stripWinsNaive m = true) := by
  native_decide

#print axioms g_table
#print axioms g_recurrence
#print axioms ring_win_list
#print axioms ring_outcome
#print axioms ring_win_range
#print axioms ring_grundy
#print axioms ring_structure
#print axioms strip_check
#print axioms no_promotion
#print axioms ring_naive_kernel
#print axioms strip_naive_kernel
#print axioms naive_native

end CylChess.Dawson
