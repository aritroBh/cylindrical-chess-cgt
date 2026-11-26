import CylChess.Claims.Common
import CylChess.Families
import CylChess.Search

/-!
# L7a (supplement): the example rings of Section S6 (`dist/tog/supp/s06.tex`), sum model

These positions are not written out in `08_star2.tex`; its text refers to them ("Section S6 lists example rings, counts
and checks for every `n`"). Each is checked as a single value in the sum model (default setting, `BIG = 256`, the fast
search `Search.isValue`, which `SearchAgrees.lean` tests against the specification), on the cylinder with eight ranks.
-/
namespace CylChess.Claims
open Wide

def S6 (w b : List (Char × Nat)) : Position :=
  Position.ofSquares (w.map fun (c, r) => sqr c r) (b.map fun (c, r) => sqr c r)

def sumStar (n k : Nat) (p : Position) : Bool :=
  Search.isValue (env Settings.default (cylinder n)) fuel p (Tree.star k)

/-- "on `C_4` the first are `W a4 b2 c2 / B b6 c5 d6 d7` and its color-reversed twin, with seven; our engine confirms
both values". The twin: colours exchanged and ranks `r ↦ 9 - r`. -/
theorem c4_seven_pawn_rings :
    sumStar 4 2 (S6 [('a', 4), ('b', 2), ('c', 2)] [('b', 6), ('c', 5), ('d', 6), ('d', 7)]) = true ∧
    sumStar 4 2 (S6 [('b', 3), ('c', 4), ('d', 3), ('d', 2)] [('a', 5), ('b', 7), ('c', 7)]) = true := by native_decide

/-- "On `C_6` the first rings have nine pawns: ... `W a4 c4 d2 e2 / B b6 b7 d6 e5 f6`". -/
theorem c6_nine_pawn_ring :
    sumStar 6 2 (S6 [('a', 4), ('c', 4), ('d', 2), ('e', 2)] [('b', 6), ('b', 7), ('d', 6), ('e', 5), ('f', 6)]) = true := by
  native_decide

/-- "`C_7`: the ten-pawn rings with five pawns a side include 63 of value `*2`, such as
`W a2 a3 c3 e3 f2 / B a4 b5 d5 f5 g5`", and "eight of value `*3`, among them `W a2 a5 c4 e2 f2 / B a7 b4 d7 e5 g7`,
`*3` in both models". -/
theorem c7_ten_pawn_rings :
    sumStar 7 2 (S6 [('a', 2), ('a', 3), ('c', 3), ('e', 3), ('f', 2)] [('a', 4), ('b', 5), ('d', 5), ('f', 5), ('g', 5)]) = true ∧
    sumStar 7 3 (S6 [('a', 2), ('a', 5), ('c', 4), ('e', 2), ('f', 2)] [('a', 7), ('b', 4), ('d', 7), ('e', 5), ('g', 7)]) = true := by
  native_decide

/-- "`C_8`: ... of the ten-pawn rings 18 are `*2` and two `*3` ... for example `W a3 b3 c3 d2 f2 / B b6 d5 e5 g4 h5`";
"On `C_8` the ten-pawn `W a4 c3 d3 e2 g2 / B b7 c6 e5 f5 h4` is `*3`". -/
theorem c8_ten_pawn_rings :
    sumStar 8 2 (S6 [('a', 3), ('b', 3), ('c', 3), ('d', 2), ('f', 2)] [('b', 6), ('d', 5), ('e', 5), ('g', 4), ('h', 5)]) = true ∧
    sumStar 8 3 (S6 [('a', 4), ('c', 3), ('d', 3), ('e', 2), ('g', 2)] [('b', 7), ('c', 6), ('e', 5), ('f', 5), ('h', 4)]) = true := by
  native_decide

/-- The example wall ring on `C_8`, `W b2 c3 c5 d2 f2 h2 / B a5 b5 c6 e4 g4`, is the member `E_8` of S13's family. -/
theorem c8_wall_example_is_E8 :
    S6 [('b', 2), ('c', 3), ('c', 5), ('d', 2), ('f', 2), ('h', 2)] [('a', 5), ('b', 5), ('c', 6), ('e', 4), ('g', 4)] =
      Wide.ofFiles (Fam.wall 8) := by native_decide

/-- "`C_11`: the twelve-pawn `W c4 d6 e3 h3 i2 k2 / B a4 b7 d7 f7 g6 j6` is `*3` \lab{C2}": sum model, and the
whole-board game with a heap (not stated for this model in the paper). -/
theorem c11_twelve_pawn_ring_sum :
    sumStar 11 3 (S6 [('c', 4), ('d', 6), ('e', 3), ('h', 3), ('i', 2), ('k', 2)]
      [('a', 4), ('b', 7), ('d', 7), ('f', 7), ('g', 6), ('j', 6)]) = true := by native_decide

end CylChess.Claims
