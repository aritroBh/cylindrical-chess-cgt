import CylChess.Claims.Common
import CylChess.Families
import CylChess.Search

/-!
# L7a: the ring positions written out in `dist/tog/sections/08_star2.tex`

Two models occur in the paper and each claim names the one it is stated in:

* the **sum model** `S(X)` of `Game.lean` (a position is a sum of components; "the CGT engine"): `Search.isValue`, the
  memoized search of `Search.lean` (`BIG = 256`), which `SearchAgrees.lean` tests against the specification `IsValue`.
  The specification itself (naive recursion, no memo) does not finish on these rings (more than 10 minutes for the
  six-pawn ring on `C_3`), so no claim here is stated with `IsValue`;
* the **whole-board game with a nim heap** of S13: `Wide.WideStar` (`SearchWide.lean`; the heaps `h = 0 .. 6`; for
  `h > 2` the heap move to `*2` shows the rest, which is not formalised).
-/
namespace CylChess.Claims
open Wide

def cyl3 : Board := { files := 3, topology := .cylinder }

/-- "the six-pawn `W a2 a3 b2 / B b7 c6 c7` on `C_3`". -/
def ring6 : Position :=
  Position.ofSquares [sqr 'a' 2, sqr 'a' 3, sqr 'b' 2] [sqr 'b' 7, sqr 'c' 6, sqr 'c' 7]

/-- "`W b2 d2 e3 h3 j5 / B a4 c6 f6 g7 i7` on `C_10` (the ring `M_10` of Fig. `fig:ring`)". -/
def ringM10 : Position :=
  Position.ofSquares [sqr 'b' 2, sqr 'd' 2, sqr 'e' 3, sqr 'h' 3, sqr 'j' 5]
    [sqr 'a' 4, sqr 'c' 6, sqr 'f' 6, sqr 'g' 7, sqr 'i' 7]

/-- "`W c5 e3 h3 i2 k2 / B a4 b7 d7 f7 g6 j6` on `C_11`". -/
def ringO11 : Position :=
  Position.ofSquares [sqr 'c' 5, sqr 'e' 3, sqr 'h' 3, sqr 'i' 2, sqr 'k' 2]
    [sqr 'a' 4, sqr 'b' 7, sqr 'd' 7, sqr 'f' 7, sqr 'g' 6, sqr 'j' 6]

/-- The two named ten- and eleven-pawn rings are the members `M_10` and `O_11` of the families of S14 (the paper
writes them in a different notation). -/
theorem named_rings_are_family_members :
    ringM10 = Wide.ofFiles (Fam.mEven 10) ∧ ringO11 = Wide.ofFiles (Fam.oneOdd 11) := by native_decide

/-- "the six-pawn ... on `C_3`" has six pawns, is a single component (a ring: every file is occupied) and has no
passed pawn. -/
theorem ring6_shape :
    ring6.size = 6 ∧ (components cyl3 ring6).length = 1 ∧
    hasPassed Settings.default cyl3 ring6 .white = false ∧ hasPassed Settings.default cyl3 ring6 .black = false := by
  native_decide

/-- "The first ring `*2` on `C_n` has `n+3` pawns for `n = 3, ..., 7` \lab{C2}, among them the six-pawn
`W a2 a3 b2 / B b7 c6 c7` on `C_3`": value `*2` in the default setting, sum model (fast search). -/
theorem ring6_star2 : Search.isValue (env Settings.default cyl3) fuel ring6 (Tree.star 2) = true := by native_decide

/-- "...; it needs two en passant captures, and with e.p. off it is `0`": with e.p. off and the default race rule
(`count`; the paper names no other) the value is `0`. The count "two en passant captures" is not formalised. -/
theorem ring6_ep_off_zero :
    Search.isValue (env ⟨.off, .count⟩ cyl3) fuel ring6 Tree.zero = true := by native_decide

/-- "From `C_10` on, one pawn per file suffices: `W b2 d2 e3 h3 j5 / B a4 c6 f6 g7 i7` on `C_10` (the ring `M_10`) and
`W c5 e3 h3 i2 k2 / B a4 b7 d7 f7 g6 j6` on `C_11` are `*2` \lab{C2}": the sum model, default setting (fast search,
the memoized `Search`). -/
theorem rings_M10_O11_star2_sum :
    Search.isValue (env Settings.default (cylinder 10)) fuel ringM10 (Tree.star 2) = true ∧
    Search.isValue (env Settings.default (cylinder 11)) fuel ringO11 (Tree.star 2) = true := by native_decide

/-- The same two rings as whole-board games with a nim heap (S14: `M_n`, even `n ≥ 10`, and the odd ring, odd
`n ≥ 11`, are `*2` against every heap): `G + *h` is lost by the mover exactly for `h = 2` (`h ≤ 6`). -/
theorem rings_M10_O11_star2_whole :
    WideStar (defEnv (cylinder 10)) wideFuel ringM10 2 6 ∧ WideStar (defEnv (cylinder 11)) wideFuel ringO11 2 6 := by
  native_decide

/-- "A `*3` lies just beyond these scans, as a single component with nine pawns: ... `W a2 b4 c2 d2 / B a4 a6 a7 c6 d5`
is `*3` on four files \lab{C2}" (default setting, ordinary board; not a ring). -/
def pos9 : Position :=
  Position.ofSquares [sqr 'a' 2, sqr 'b' 4, sqr 'c' 2, sqr 'd' 2] [sqr 'a' 4, sqr 'a' 6, sqr 'a' 7, sqr 'c' 6, sqr 'd' 5]

theorem star3_nine_pawns :
    (components { files := 4, topology := .flat } pos9).length = 1 ∧
    Search.isValue (env Settings.default { files := 4, topology := .flat }) fuel pos9 (Tree.star 3) = true := by
  native_decide

/-- "on boards of three to five files, seven ranks give a `*2` with four pawns, `W a2 c2 / B c3 b6`" (default setting;
ordinary boards with seven ranks, `Board.ranks := 7`; not a ring). -/
theorem star2_seven_ranks :
    ∀ w ∈ [3, 4, 5],
      Search.isValue (env Settings.default { files := w, ranks := 7, topology := .flat })
        fuel (Position.ofSquares [sqr 'a' 2, sqr 'c' 2] [sqr 'c' 3, sqr 'b' 6]) (Tree.star 2) = true := by
  native_decide

end CylChess.Claims
