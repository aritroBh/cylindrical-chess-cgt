import CylChess
import CylChess.HeapsAgrees
import CylChess.SearchWideAgrees
import CylChess.Dawson
import CylChess.Claims.L9_Cut

open CylChess

namespace Referee

-- One stuck pair, no heap. A reference implementation that always says "unknown".
#eval HeapsAgrees.agreeWith (fun _ _ _ _ => none) 0
  (Census.env, Position.ofSquares [(0,2)] [(0,3)])

-- The fast sentinel has a real counterexample on a valid tall board.
def tall : Board := { files := 1, ranks := 1003, topology := .flat }
def lone : Position := Position.ofSquares [] [(0,1001)]
#eval (lone.valid tall, hasPassed Settings.default tall lone .black,
  Wide.passedF Settings.default tall lone .black)

-- Exact coverage, including unique keys, unlike a length assertion alone.
#eval (Census.expected.map (fun (w,n,_) => (w,n))).eraseDups ==
  (List.range' 1 4).flatMap (fun w => (List.range' 2 5).map (fun n => (w,n)))
#eval Census.expected.length
#eval (Agrees.family.length, Agrees.cases.length, WideAgrees.casesAll.length, WideAgrees.casesOpen.length)
#eval (Agrees.cases.filter (fun (e,p) => !(p.valid e.b))).length
#eval (WideAgrees.casesOpen.filter (fun (e,p) => !(p.valid e.b))).length
#eval [EpRule.off, .textbook, .aware].map (fun ep => Claims.Cut.famSize ⟨ep,.count⟩ 6 8 2 0)
#print axioms Claims.eighth_every_race_function
#print axioms Claims.eighth_empty_table_default_kernel
#print axioms Claims.roots_open_X
#print axioms Claims.fh_black_threat
#print axioms Claims.census_small
#print axioms Claims.census_big
#print axioms Claims.census_totals
#print axioms Claims.wall_rings_star2
#print axioms Wide.WH_all_larger_heaps
#print axioms Dawson.ring_grundy
#print axioms Dawson.ring_naive_kernel
#print axioms Claims.Cut.cut_step_6_8_2

-- Strengthen all the HeapsAgrees tests to equality with a DEFINITE answer.
def strict (win : Env → List Comp → Nat → Color → Option Bool) (jmax : Nat) (ep : Env × Position) : Bool :=
  let (e, p) := ep
  let cs := Comp.ofPosition e p
  match (Heaps.sets e 400 cs).run' {} with
  | none => false
  | some (l,r) => (List.range (jmax+1)).all fun j =>
      win e cs j .white == some (l.mem j) && win e cs j .black == some (r.mem j)
#eval Agrees.cases.all (strict HeapsAgrees.spec 3)
#eval Agrees.cases.all (strict HeapsAgrees.fast 7)
#eval (HeapsAgrees.censusCases 2 2 2 ++ HeapsAgrees.censusCases 2 2 1).all (strict HeapsAgrees.spec 3)
#eval (HeapsAgrees.censusCases 3 2 2).all (strict HeapsAgrees.fast 7)
#eval WideAgrees.casesOpen.all fun (e,p) => [0,1,2].all fun h => Agrees.colors.all fun c =>
  let w := Wide.WH e 60 p h c
  w.isSome && w == Wide.wideRun e 400 p h c
end Referee
