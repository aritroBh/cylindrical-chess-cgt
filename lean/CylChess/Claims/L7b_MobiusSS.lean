import CylChess.Claims.L7b_Mobius

/-!
# L7b: `SS(m)` on the Möbius strip (N6), `*3`, `n = 2m + 11` files, `n + 1` pawns, `m ≥ 0` (the slowest strip family)
-/
namespace CylChess.Claims
open Wide

theorem SS_star3 : (allWidths 0 8).all (checkMob Fam.ss 3 (2 * · + 11) (2 * · + 12)) = true := by native_decide

end CylChess.Claims
