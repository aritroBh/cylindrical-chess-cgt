import CylChess.Claims.WideCommon

/-!
# L7b: the wall rings (S13, N1, N3), whole-board game, default setting, base cases by program

> "As a whole-board game this gives a ring `*2` with `n+3` pawns on every `C_n` with `n ≥ 5` \lab{S}, checked by two
> programs for `n ≤ 61` \lab{C2}" (`08_star2.tex`, Section 6, "Rings and Higher Nimbers"; S13)

The model is S13's: the whole-board game `G + *h` on `C_n` (eight ranks), race rule `count`, e.p. on with the
e.p.-aware passed test (= `Settings.default`), no splitting into components, the first passed pawn ends the game. The
paper proves the statement for every `n` by an insertion argument from base cases; here the finite instances are
checked for every width up to the bound stated in each theorem. (The paper's own finite checks C1 at `n_0 = 16, 17`
and C2 below are of this kind; the insertion lemma itself is not formalised.)

The same checks for `P_n` (even `n ≥ 8`) and `R_n` (odd `n ≥ 11`), the `n + 2` pawn rings of N1 and N3 (the paper's
"two `n`-pawn families" are `L7b_OnePerFile`; the `n+2` families are the base of its `*3` constructions).
-/
namespace CylChess.Claims
open Wide

/-- S13 Theorem: `G_n + *h` is a P-position for `h = 2` and an N-position otherwise (`h ≤ 6`), `G_n` with `n + 3`
pawns, for every `n = 5 .. 61`. -/
theorem wall_rings_star2 :
    (allWidths 5 61).all (checkFam cylinder Fam.wall 2 hmaxW (· + 3)) = true := by native_decide

/-- N1: `P_n` (`n + 2` pawns) is `*2` against the heaps `h ≤ 6`, for every even `n = 8 .. 60`. -/
theorem P_rings_star2 :
    (widths 8 60).all (checkFam cylinder Fam.pEven 2 hmaxW (· + 2)) = true := by native_decide

/-- N3: `R_n` (`n + 2` pawns) is `*2` against the heaps `h ≤ 6`, for every odd `n = 11 .. 59`. -/
theorem R_rings_star2 :
    (widths 11 59).all (checkFam cylinder Fam.rOdd 2 hmaxW (· + 2)) = true := by native_decide

end CylChess.Claims
