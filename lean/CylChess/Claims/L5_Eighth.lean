import CylChess.Claims.Common
import CylChess.Search

/-!
# L5: Theorem `thm:eighth` (`dist/tog/sections/07_targets.tex`)

> "In the pawn model, white a2, b2, b3 against black a5, a6, b6 has value exactly 1/8 in all nine settings
> and for every assignment of outcomes to its race positions (Section II)."

"Race positions" (§2.3): a move that gives both sides a passed pawn. The outcome of such a position is a
winner, normally given by the setting's race rule. Here an assignment is a table giving a winner to each pair
(race position reached, side that moved). The race positions are the ones reached in the pawn game of the
position, component by component (see `Game.lean`); there are `k` of them (`raceKeys`), so there are `2^k`
assignments, and all are checked, for each of the three e.p. options. A race reached that the table does not
cover is *not* an error: it makes the options through it unknown, and the check can still return a definite
`true` (so this check does not show that the list of race positions is complete). Completeness is not needed for
the statement: `L5_EmptyTable.lean` proves on the specification that the value is `1/8` when every race is
unknown, and (`eighth_every_race_function`) that it is then `1/8` for every race function whatever. The sentence
"in the sum model": all values in this file are values in the sum model of `Game.lean`.

Monotonicity: the paper's remark (replacing a race outcome by a better one for White can only help White, so
the two extremes suffice) is not what is formalised here; the statement proved is the one of `L5_EmptyTable.lean`
(a definite answer under unknown races stays the same for every race function). Both extremes are among the
assignments checked below.
-/
namespace CylChess.Claims

def posG : Position :=
  Position.ofSquares [sqr 'a' 2, sqr 'b' 2, sqr 'b' 3] [sqr 'a' 5, sqr 'a' 6, sqr 'b' 6]

/-- The mirror image (files a and b exchanged), on which the paper says its checks ran (Section S5). -/
def posGMirror : Position :=
  Position.ofSquares [sqr 'b' 2, sqr 'a' 2, sqr 'a' 3] [sqr 'b' 5, sqr 'b' 6, sqr 'a' 6]

/-- "has value exactly 1/8 in all nine settings", with the specification. -/
theorem eighth_nine_settings :
    ∀ s ∈ allSettings, IsValue (env s flat8) fuel posG Tree.eighth := by native_decide

/-- The same for the mirror image. -/
theorem eighth_mirror_nine_settings :
    ∀ s ∈ allSettings, IsValue (env s flat8) fuel posGMirror Tree.eighth := by native_decide

/-! ### Every assignment of outcomes to the race positions -/

/-- All (race position, mover) pairs reachable from the pawn components of `pos`: breadth-first over the
component positions, following only moves that leave the game open. Not trusted, and not needed to be
complete: if it missed a race position, the table would not cover it, `Env.race` would answer `none` there, and
the check would run on a partial table, which `L5_EmptyTable.lean` shows is also covered (a missed key does
not make the check fail). -/
def raceKeys (e : Env) (pos : Position) : List (Position × Color) :=
  let rec go : Nat → List Position → List Position → List (Position × Color) → List (Position × Color)
    | 0, _, _, acc => acc
    | _ + 1, [], _, acc => acc
    | n + 1, p :: todo, seen, acc =>
      if seen.contains p then go n todo seen acc else
      let kids := [Color.white, .black].flatMap fun c => (moves e.s e.b p c).map (c, ·)
      let races := kids.filter fun (_, q) => hasPassed e.s e.b q .white && hasPassed e.s e.b q .black
      let opens := (kids.filter fun (_, q) => !hasPassed e.s e.b q .white && !hasPassed e.s e.b q .black).flatMap
        fun (_, q) => components e.b q
      let acc := races.foldl (fun a (c, q) => if a.contains (q, c) then a else a ++ [(q, c)]) acc
      go n (todo ++ opens) (p :: seen) acc
  go 100000 (components e.b pos) [] []

/-- The environment whose race outcomes are the table `t`. -/
def envTable (s : Settings) (t : List ((Position × Color) × Color)) : Env :=
  { s := s, b := flat8, race := fun p m => t.lookup (p, m) }

/-- All `2^k` lists of `k` winners. -/
def allWinners : Nat → List (List Color)
  | 0 => [[]]
  | k + 1 => (allWinners k).flatMap fun l => [Color.white :: l, Color.black :: l]

/-- Every assignment of winners to the race positions makes `pos` equal to `1/8`. -/
def eighthForAllAssignments (ep : EpRule) (pos : Position) : Bool :=
  let s : Settings := ⟨ep, .count⟩
  let keys := raceKeys (env s flat8) pos
  (allWinners keys.length).all fun ws => Search.isValue (envTable s (keys.zip ws)) fuel pos Tree.eighth

/-- How many race positions the pawn game of `pos` has, per e.p. option. -/
def raceCounts (pos : Position) : List Nat :=
  [EpRule.aware, .textbook, .off].map fun ep => (raceKeys (env ⟨ep, .count⟩ flat8) pos).length

/-- The race positions of the pawn game, per e.p. option (aware, textbook, off): 9, 10, 9. -/
theorem eighth_race_counts : raceCounts posG = [9, 10, 9] := by native_decide

/-- "for every assignment of outcomes to its race positions": all `2^k` assignments, for each e.p. option
(fast search; the three race rules are three of the assignments). -/
theorem eighth_all_assignments :
    ∀ ep ∈ [EpRule.aware, .textbook, .off], eighthForAllAssignments ep posG = true := by native_decide

end CylChess.Claims
