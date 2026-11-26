import CylChess.RingScan

/-!
# L11: minimality on `C_4` (step 4)

> "on `C_4` the first are `W a4 b2 c2 / B b6 c5 d6 d7` and its color-reversed twin, with seven ... No smaller ring on either is a
> `*2`: the atlas, a C scan and an independent ring solver agree" (S6)

No ring on `C_4` with 4, 5 or 6 pawns is `*2` (nor has any value `*j`, `j ≥ 2`): counts of all rings (every file occupied, ranks
2-6 / 3-7, no passed pawn, no symmetry reduction) and `*2` count 0. The seven-pawn rings are in `L7a_S6Rings`
(`c4_seven_pawn_rings`). The six-pawn scan alone takes about 11 minutes.
-/
namespace CylChess.Claims
open RingScan

theorem ring_min_C4 :
    scan 4 4 2000 = ⟨1490, 0, 0, 0⟩ ∧ scan 4 5 2000 = ⟨32752, 0, 0, 0⟩ ∧ scan 4 6 2000 = ⟨336992, 0, 0, 0⟩ := by
  native_decide

end CylChess.Claims
