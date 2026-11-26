import CylChess.Families

/-!
# Shared by the whole-board family claims (`L7b_*`)

`checkFam mk fam k hmax size n` says: the family member for the width `n` has exactly `n` files and `size n` pawns,
has no passed pawn, and `G + *h` is lost by the mover (either mover) exactly for `h = k`, for every heap `h ≤ hmax`
(`Wide.starTest`, the search of `SearchWide.lean`). By `Wide.WH_all_larger_heaps` (for the specification) a loss at
`*k` gives a win at every larger heap, so the outcome classes agree with those of `*k + *h` for every `h` there.
-/
namespace CylChess.Claims
open Wide

def checkFam (mk : Nat → Board) (fam : Nat → List String) (k hmax : Nat) (size : Nat → Nat) (n : Nat) : Bool :=
  let fs := fam n
  fs.length == n && (ofFiles fs).size == size n && starTest (defEnv (mk n)) wideFuel (ofFiles fs) k hmax

/-- The widths `lo, lo + 2, ..., ≤ hi`. -/
def widths (lo hi : Nat) : List Nat := (List.range ((hi - lo) / 2 + 1)).map fun i => lo + 2 * i

/-- Every width `lo .. hi`. -/
def allWidths (lo hi : Nat) : List Nat := List.range' lo (hi - lo + 1)

/-- The largest heap tested. -/
def hmaxW : Nat := 6

end CylChess.Claims
