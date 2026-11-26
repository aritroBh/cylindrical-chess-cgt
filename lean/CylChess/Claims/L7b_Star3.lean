import CylChess.Claims.WideCommon

/-!
# L7b: the `*3` rings with `n + 2` and `n + 1` pawns (N2, N3, N4), whole-board game, default setting

> "Wall insertion gives a whole-board `*3` with `n+2` pawns on every `C_n` with even `n ≥ 8` and odd `n ≥ 11` \lab{S},
> and with `n+1` pawns on `C_11` \lab{C2} and on every `C_n` with `n ≥ 12` \lab{S}." (`08_star2.tex`)

`Q_n` (even `n ≥ 8`, N2) and `Qo_n` (odd `n ≥ 11`, N3) have `n + 2` pawns; `T_n` (even `n ≥ 12`) and `S_n` (odd `n ≥ 13`)
(N4) have `n + 1`. "`*3`" is the heap test of S13: `G + *h` is lost by the mover exactly for `h = 3`. The paper's induction
needs base cases `n_0 = 22, 22, 20, 23` for `Q, Qo (19), T, S`; the instances below go up to the bound in each
theorem. (`S_n` is in `L7b_S`, it is the slowest family.)
-/
namespace CylChess.Claims
open Wide

theorem Q_rings_star3 :
    (widths 8 40).all (checkFam cylinder Fam.qEven 3 hmaxW (· + 2)) = true := by native_decide

theorem Qo_rings_star3 :
    (widths 11 39).all (checkFam cylinder Fam.qoOdd 3 hmaxW (· + 2)) = true := by native_decide

theorem T_rings_star3 :
    (widths 12 40).all (checkFam cylinder Fam.tEven 3 hmaxW (· + 1)) = true := by native_decide

end CylChess.Claims
