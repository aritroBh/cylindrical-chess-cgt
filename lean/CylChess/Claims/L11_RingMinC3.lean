import CylChess.RingScan
import CylChess.Claims.Common

/-!
# L11: minimality on `C_3` (step 4)

> "The first ring `*2` on `C_n` has `n+3` pawns for `n = 3, ..., 7` \lab{C2}, among them the six-pawn
> `W a2 a3 b2 / B b7 c6 c7` on `C_3`" (`08_star2.tex`); "On `C_3` the only ring `*2` with six pawns in the default setting is
> `W a2 a3 b2 / B b7 c6 c7`" (S6: "No smaller ring on either is a `*2`").

`RingScan.rings 3 w b`: every position on `C_3` with `w` white pawns on ranks 2-6, `b` black pawns on ranks 3-7, every file
occupied, no passed pawn (default setting), no reduction by symmetry; the value is computed in the sum model (`Heaps.sets`,
`BIG = 256`) and `*2` means `X + *2` lost by the mover whoever it is. Pawns on rank 7 (white) and rank 2 (black) are passed at once
and rank 8 / rank 1 hold no pawn, so the ranks 2-7 cover every ring without a passed pawn; a ring on `C_3` has at least 3
pawns and at least one of each colour.
-/
namespace CylChess.Claims
open RingScan

/-- Counts of the rings on `C_3` by number of pawns `p` (all of them, not up to symmetry), and how many are `*2`, how many have
a value `*j` with `j ≥ 2`; none unsettled. No ring with at most five pawns is `*2` (or any `*j`, `j ≥ 2`). -/
theorem ring_min_C3_below :
    scan 3 3 2000 = ⟨330, 0, 0, 0⟩ ∧ scan 3 4 2000 = ⟨4740, 0, 0, 0⟩ ∧ scan 3 5 2000 = ⟨34170, 0, 0, 0⟩ := by
  native_decide

/-- `W a2 a3 b2 / B b7 c6 c7`. -/
def ring6' : Position := Position.ofSquares [sqr 'a' 2, sqr 'a' 3, sqr 'b' 2] [sqr 'b' 7, sqr 'c' 6, sqr 'c' 7]

/-- The six-pawn rings on `C_3` that are `*2`. -/
def star2SixRings : List Position := star2Rings 3 6 2000

/-- With six pawns there are 160,515 rings, six of them `*2` and no other has a value `*j`, `j ≥ 2`; the six are exactly the images of
`W a2 a3 b2 / B b7 c6 c7` under the three rotations, the mirror image and the colour reversal. -/
theorem ring_min_C3_six :
    scan 3 6 2000 = ⟨160515, 6, 6, 0⟩ ∧
    (∀ q ∈ star2SixRings, q ∈ orbit 3 ring6') ∧ (∀ q ∈ orbit 3 ring6', q ∈ star2SixRings) := by
  native_decide

end CylChess.Claims
