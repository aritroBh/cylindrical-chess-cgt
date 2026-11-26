import CylChess.Census

/-!
# The census, by width `W` and number of pawns `n`: expected tallies

The numbers below were produced by `Census.classesTally` (this development) and are re-derived by the claim modules
`L10_CensusSmall` and `L10_CensusBig`; they agree, group by group, with an independent tabulation of
`atlas/flat8/rerun/census.tsv` (column `count/epon/aware` = the default setting) made with Python. Each entry is
`(W, n, tally)` with `tally = ⟨records, board positions, value 0, value *, no nimber, a heap j ≥ 2 (X = *j), unsettled⟩`.
-/
namespace CylChess
namespace Census

def expected : List (Nat × Nat × Tally) :=
  [(1, 2, ⟨15, 15, 7, 4, 4, 0, 0⟩), (1, 3, ⟨40, 40, 8, 0, 32, 0, 0⟩), (1, 4, ⟨60, 60, 18, 6, 36, 0, 0⟩),
   (1, 5, ⟨48, 48, 20, 4, 24, 0, 0⟩), (1, 6, ⟨16, 16, 16, 0, 0, 0, 0⟩),
   (2, 2, ⟨15, 30, 5, 3, 7, 0, 0⟩), (2, 3, ⟨150, 300, 4, 0, 146, 0, 0⟩), (2, 4, ⟨755, 1495, 70, 37, 648, 0, 0⟩),
   (2, 5, ⟨2360, 4720, 90, 30, 2240, 0, 0⟩), (2, 6, ⟨5188, 10336, 200, 80, 4908, 0, 0⟩),
   (3, 2, ⟨0, 0, 0, 0, 0, 0, 0⟩), (3, 3, ⟨70, 110, 4, 0, 66, 0, 0⟩), (3, 4, ⟨1365, 2565, 140, 84, 1141, 0, 0⟩),
   (3, 5, ⟨10476, 20402, 222, 98, 10156, 0, 0⟩), (3, 6, ⟨51089, 100843, 1396, 673, 49020, 0, 0⟩),
   (4, 2, ⟨0, 0, 0, 0, 0, 0, 0⟩), (4, 3, ⟨0, 0, 0, 0, 0, 0, 0⟩), (4, 4, ⟨1035, 2025, 198, 152, 685, 0, 0⟩),
   (4, 5, ⟨16054, 32108, 290, 158, 15606, 0, 0⟩), (4, 6, ⟨142335, 284330, 4036, 2713, 135586, 0, 0⟩)]

/-- The entries of `expected` for the width `W` and a list of pawn counts. -/
def groupsOf (Ws ns : List Nat) : List (Nat × Nat × Tally) :=
  expected.filter fun (W, n, _) => Ws.contains W && ns.contains n

/-- Does `classesTally` give the expected tally for every group in the list? -/
def checkGroups (gs : List (Nat × Nat × Tally)) : Bool :=
  gs.all fun (W, n, t) => classesTally env 400 2000 (classes.filter fun (W', w, b) => W' == W && w + b == n) == t

/-- The sum of the tallies of the list. -/
def sumTally (gs : List (Nat × Nat × Tally)) : Tally := (gs.map (·.2.2)).foldl Tally.add {}

end Census
end CylChess
