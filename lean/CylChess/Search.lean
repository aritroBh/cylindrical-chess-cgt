import CylChess.Game
import Std.Data.HashMap

/-!
# The fast search

The same definite outcomes as `Game.wins` and `W` (a definite answer `some b` is the true outcome whatever the fuel),
but not the same answers at equal fuel: merging integers makes some branches shorter, so at a small fuel the fast
search can answer `some b` where the specification says `none` (unknown); `SearchAgrees.lean` tests only fuel 400.
It is memoized in a hash map threaded through the recursion, and with
the integer components of a sum merged into one (`n` free moves for Left and `m` for Right are `n - m`;
a component equal to `0` is dropped). It is trusted like `Game.lean`; `SearchAgrees.lean` tests that it
agrees with it, which is a test and not a proof.

Only definite answers (`some b`) are stored: they are correct whatever the fuel is, so a stored answer never
depends on the fuel of the call that found it. Unknown answers (`none`) are recomputed.
-/
namespace CylChess

deriving instance Hashable for Color
deriving instance Hashable for Pawn
deriving instance Hashable for Position
deriving instance BEq for Tree
deriving instance Hashable for Tree
deriving instance BEq, Hashable for Comp

namespace Search

/-- Merge all integer components into one and drop empty ones (a zero integer, a tree with no moves). -/
def norm (cs : List Comp) : List Comp :=
  let n := cs.foldl (fun acc c => match c with | .num k => acc + k | _ => acc) 0
  let rest := cs.filter fun c => match c with
    | .num _ => false
    | .tree (.node [] []) => false
    | _ => true
  if n == 0 then rest else rest ++ [.num n]

abbrev Memo := Std.HashMap (List Comp × Color) Bool
abbrev M := StateM Memo

/-- Look at the options one at a time, stopping at the first win; the same answer as `anyOpt`. -/
def anyM (os : List (M (Option Bool))) : M (Option Bool) :=
  match os with
  | [] => pure (some false)
  | o :: rest => do
    match ← o with
    | some true => pure (some true)
    | some false => anyM rest
    | none => do
      match ← anyM rest with
      | some true => pure (some true)
      | _ => pure none

/-- `Game.wins`, memoized. -/
def wins (e : Env) : Nat → List Comp → Color → M (Option Bool)
  | 0, _, _ => pure none
  | f + 1, cs, c => do
    let cs := norm cs
    match (← get)[(cs, c)]? with
    | some b => pure (some b)
    | none =>
      let r ← anyM ((Sum.options e c cs).map fun o =>
        match o with
        | none => pure none
        | some cs' => do return (← wins e f cs' c.other).map (!·))
      if let some b := r then modify (·.insert (cs, c) b)
      pure r

/-- `Game.wins` for a fresh memo. -/
def run (e : Env) (fuel : Nat) (cs : List Comp) (c : Color) : Option Bool :=
  ((wins e fuel cs c).run' {})

/-- `outcome`, fast; the memo is shared by both movers. -/
def outcome (e : Env) (fuel : Nat) (pos : Position) (t : Tree) (c : Color) : Option Bool :=
  run e fuel (Comp.ofPosition e pos ++ [.tree t]) c

/-- `isValue`, fast: one memo for both movers. -/
def isValue (e : Env) (fuel : Nat) (pos : Position) (v : Tree) : Bool :=
  let cs := Comp.ofPosition e pos ++ [.tree v.neg]
  !hasPassed e.s e.b pos .white && !hasPassed e.s e.b pos .black &&
  ((do let a ← wins e fuel cs .white
       let b ← wins e fuel cs .black
       pure (a == some false && b == some false) : M Bool).run' {})

/-- `S`, fast. -/
def S (e : Env) (fuel : Nat) (pos : Position) (c : Color) : Option Bool :=
  run e fuel (Comp.ofPosition e pos) c

/-- `W`, memoized on (position, mover). -/
def W (e : Env) : Nat → Position → Color → StateM (Std.HashMap (Position × Color) Bool) (Option Bool)
  | 0, _, _ => pure none
  | f + 1, pos, c => do
    match (← get)[(pos, c)]? with
    | some b => pure (some b)
    | none =>
      let mut res : Option Bool := some false
      let mut unknown := false
      for q in moves e.s e.b pos c do
        let r ← match e.verdict q c with
          | .open_ => do pure ((← W e f q c.other).map (!·))
          | .decided w => pure (some (w == c))
          | .undefined => pure none
        match r with
        | some true => res := some true; break
        | some false => pure ()
        | none => unknown := true
      let out := if res == some true then res else if unknown then none else some false
      if let some b := out then modify (·.insert (pos, c) b)
      pure out

/-- `W`, fast. -/
def wholeBoard (e : Env) (fuel : Nat) (pos : Position) (c : Color) : Option Bool :=
  ((W e fuel pos c).run' {})

end Search
end CylChess
