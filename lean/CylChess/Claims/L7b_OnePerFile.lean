import CylChess.Claims.WideCommon

/-!
# L7b: one pawn per file (S14), whole-board game, default setting

> "From `C_10` on, one pawn per file suffices ... The same argument proves the two `n`-pawn families above `*2` as
> whole-board games for every `n ≥ 10` \lab{S}; as sums of components they are `*2` on `C_10` and `C_11` \lab{C1}."

`M_n` (even `n ≥ 10`) and the odd ring (odd `n ≥ 11`, called `O_n` in S14) have exactly `n` pawns. The sum-model
statement for `C_10` and `C_11` is in `L7a_NamedRings`.
-/
namespace CylChess.Claims
open Wide

theorem M_rings_star2 :
    (widths 10 50).all (checkFam cylinder Fam.mEven 2 hmaxW (· + 0)) = true := by native_decide

theorem oddOnePerFile_rings_star2 :
    (widths 11 49).all (checkFam cylinder Fam.oneOdd 2 hmaxW (· + 0)) = true := by native_decide

end CylChess.Claims
