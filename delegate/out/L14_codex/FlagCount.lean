import CylChess.Census
open CylChess
namespace Referee
open Census

-- A live flag and its mover reconstruct the preceding flag-free diagram uniquely.
-- A reflection can identify two double steps only when the predecessor is symmetric.
def live (W : Nat) (r : Rec) : List Rec :=
  [Color.white,.black].flatMap fun c => (moves Settings.default board r.pos c).filterMap fun p =>
    match p.ep with
    | none => none
    | some (f,_) =>
      if (r.mult != 1 || f ≤ W-1-f) && !hasPassed Settings.default board p .white &&
          !hasPassed Settings.default board p .black then some ⟨p,1⟩ else none

def row (W : Nat) : Tally :=
  (classes.filter (fun t => t.1 == W)).foldl (fun acc (_,w,b) =>
    let rs := (records W w b).flatMap (live W)
    ((chunks 1000 rs).map (tally env 400)).foldl Tally.add acc) {}

#eval (List.range' 2 3).map fun w =>
  let t := row w
  (w, t.recs, t.zeros, t.stars, t.big, t.failed)
end Referee
