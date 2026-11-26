import CylChess.Heaps
import CylChess.SearchAgrees
import CylChess.Census

/-!
# Evidence that `Heaps.sets` computes `{ j | the mover wins X + *j }`

**A test, not a proof** (like `SearchAgrees.lean`). For the positions of `SearchAgrees.family` (3378 positions: flat
board and cylinder, three files, five ranks, two white and two black pawns, three settings, no passed pawn at the
root) the sets `WL`, `WR` of `Heaps.sets` are compared, for each mover, with

* `Game.wins` (the specification, naive recursion) on `X + *j`, `j = 0 .. 3`: `heaps_agree_spec`;
* `Search.run` (memoized) on `X + *j`, `j = 0 .. 7`: `heaps_agree_search`;
* the same two comparisons on census records of the census environment (`BIG = 256`, flat board, default setting):
  `heaps_agree_census_spec` (the specification, `j = 0 .. 3`, the 385 records of class `W=2, w=2, b=2` and the
  75 of `W=2, w=2, b=1`) and `heaps_agree_census_search` (`j = 0 .. 7`, the 915 records of `W=3, w=2, b=2`).
-/
namespace CylChess.HeapsAgrees
open CylChess CylChess.Claims CylChess.Agrees

def agreeWith (win : Env → List Comp → Nat → Color → Option Bool) (jmax : Nat) (ep : Env × Position) : Bool :=
  let (e, p) := ep
  let cs := Comp.ofPosition e p
  match (Heaps.sets e 400 cs).run' {} with
  | none => false
  | some (wl, wr) =>
    (List.range (jmax + 1)).all fun j =>
      wl.mem j == (win e cs j .white == some true) && wr.mem j == (win e cs j .black == some true)

def spec (e : Env) (cs : List Comp) (j : Nat) (c : Color) : Option Bool :=
  Game.wins e 400 (cs ++ [.tree (Tree.star j)]) c

def fast (e : Env) (cs : List Comp) (j : Nat) (c : Color) : Option Bool :=
  Search.run e 400 (cs ++ [.tree (Tree.star j)]) c

theorem heaps_agree_spec : cases.all (agreeWith spec 3) = true := by native_decide

theorem heaps_agree_search : cases.all (agreeWith fast 7) = true := by native_decide

def censusCases (W w b : Nat) : List (Env × Position) :=
  (Census.records W w b).map fun r => (Census.env, r.pos)

theorem heaps_agree_census_spec :
    (censusCases 2 2 2 ++ censusCases 2 2 1).all (agreeWith spec 3) = true := by native_decide

theorem heaps_agree_census_search : (censusCases 3 2 2).all (agreeWith fast 7) = true := by native_decide

end CylChess.HeapsAgrees
