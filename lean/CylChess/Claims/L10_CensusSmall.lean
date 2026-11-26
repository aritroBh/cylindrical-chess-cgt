import CylChess.CensusData

/-!
# L10: Theorem `thm:census`, widths 1 to 3 and width 4 with at most five pawns

> "In the census of Section 4, in the default setting, no position has value `*k` with `k ≥ 2`; the census has 6,724
> zeros and 4,042 stars." (`08_star2.tex`, Theorem `thm:census`; the census: "every such position with at most six
> pawns on `F_1, ..., F_4`, up to translation and mirror image: 231,071 records standing for 459,443 positions",
> `06_atlas.tex`)

The default setting is `⟨aware, count⟩`, `BIG = 256`, the sum model of `Game.lean`. `checkGroups` enumerates the
records of each (width, pawns) group (`Census.records`), computes for each record the set of heaps `j` with
`X + *j` lost by the mover whoever it is (`Heaps.sets`: *all* `j` at once, no bound), and tallies: value `0`
(`{0}`), value `*` (`{1}`), a heap `j ≥ 2` (`X = *j`), neither. See `Heaps.lean`, `HeapsAgrees.lean`.
-/
namespace CylChess.Claims
open Census

theorem census_small : checkGroups (groupsOf [1, 2, 3] [2, 3, 4, 5, 6] ++ groupsOf [4] [2, 3, 4, 5]) = true := by
  native_decide

end CylChess.Claims
