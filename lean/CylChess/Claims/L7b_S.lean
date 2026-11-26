import CylChess.Claims.WideCommon

/-!
# L7b: `S_n`, the odd `*3` ring with `n + 1` pawns (N4), whole-board game, default setting

> "... with `n+1` pawns ... on every `C_n` with `n ≥ 12`" (`08_star2.tex`); N4: `S_n` for odd `n ≥ 13`, base `n_0 = 23`
> (the reduced graph at `n_0` has 40,445 nodes).
-/
namespace CylChess.Claims
open Wide

theorem S_rings_star3 :
    (widths 13 25).all (checkFam cylinder Fam.sOdd 3 hmaxW (· + 1)) = true := by native_decide

end CylChess.Claims
