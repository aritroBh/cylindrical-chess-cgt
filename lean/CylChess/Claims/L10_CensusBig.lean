import CylChess.CensusData

/-!
# L10: Theorem `thm:census`, width 4 with six pawns (142,335 of the 231,071 records)

See `L10_CensusSmall`. The class is cut into pieces of 2000 records, each run with a fresh memo.
-/
namespace CylChess.Claims
open Census

theorem census_big : checkGroups (groupsOf [4] [6]) = true := by native_decide

end CylChess.Claims
