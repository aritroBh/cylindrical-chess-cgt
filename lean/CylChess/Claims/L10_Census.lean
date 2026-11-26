import CylChess.Claims.L10_CensusSmall
import CylChess.Claims.L10_CensusBig

/-!
# L10: Theorem `thm:census`, the totals

The tallies of `L10_CensusSmall` and `L10_CensusBig` cover all twenty groups (width 1-4, 2-6 pawns); their sum is the
statement of the theorem: 231,071 records standing for 459,443 positions; 6,724 of value `0`, 4,042 of value `*`, none
`*k` for any `k ≥ 2` (the field `big` is zero: no record has any heap `j ≥ 2` with `X + *j` lost by the mover), none
unsettled.
-/
namespace CylChess.Claims
open Census

theorem census_all_groups_covered :
    (groupsOf [1, 2, 3] [2, 3, 4, 5, 6] ++ groupsOf [4] [2, 3, 4, 5] ++ groupsOf [4] [6]).length = 20 := by decide

/-- The census of `06_atlas.tex` / `08_star2.tex`: totals. -/
theorem census_totals :
    sumTally expected = ⟨231071, 459443, 6724, 4042, 220305, 0, 0⟩ := by decide

end CylChess.Claims
