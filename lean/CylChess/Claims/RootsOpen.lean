import CylChess.Claims.L4_Star2
import CylChess.Claims.L5_Eighth
import CylChess.Claims.L6_SumCounter

/-!
# The starting positions of the claims have no passed pawn

Model: the sum model of `Game.lean`. `IsValue` / `isValue` checks that the root has no passed pawn; `NotValue`,
`S` and `W` do not. A race or a passed pawn is defined in the paper only as the result of a move, so a claim
about a root that already has a passed pawn would be a different statement. Here every root position of the
claims that use `NotValue`, `S` or `W` (and, for the record, those that use `IsValue`) is checked to have no
passed pawn for either colour, in each setting of the claim.

Not added for the L7 to L10 files: their theorems use `Search.isValue` or `Wide.starTest`, and both begin with
`!hasPassed .. .white && !hasPassed .. .black` on the root (`Search.lean`, `SearchWide.lean`); the L9 families
compare whole families of positions and are not roots of a value claim.
-/
namespace CylChess.Claims

/-- No passed pawn for either colour in `pos` under the setting `s` on the board `b`. -/
def open_ (s : Settings) (b : Board) (pos : Position) : Bool :=
  !hasPassed s b pos .white && !hasPassed s b pos .black

/-- L4: `posA` and `posB` on the ordinary board, in all nine settings. -/
theorem roots_open_AB :
    ∀ s ∈ allSettings, open_ s flat8 posA = true ∧ open_ s flat8 posB = true := by decide

/-- L5: `posG` and its mirror image, in all nine settings. -/
theorem roots_open_G :
    ∀ s ∈ allSettings, open_ s flat8 posG = true ∧ open_ s flat8 posGMirror = true := by decide

/-- L6: `posX` on `C_8`, e.p. off, count rule (the setting of the claim). -/
theorem roots_open_X : open_ ⟨.off, .count⟩ cyl8 posX = true := by decide

end CylChess.Claims
