import CylChess.SearchWide
import CylChess.SearchAgrees

/-!
# Evidence that `Wide.wide` computes what `Wide.WH` specifies

**A test, not a proof** (like `SearchAgrees.lean`). The naive specification `WH` cannot run on the ring families
(the game tree is far too large), so the search is compared with it only on small positions, and the faster
parts of the search are compared with the rules one at a time:

1. `passedF` (highest and lowest enemy rank per file) equals `hasPassed` of `Rules.lean` for both colours, on every
   position reachable from the 3378 positions of `SearchAgrees.family` (flat board, cylinder and Möbius strip, three
   files, five ranks, the three settings `⟨aware, count⟩`, `⟨textbook, mover⟩`, `⟨off, opponent⟩`): `passed_agrees`.
2. `wide` equals `WH` (naive) on the positions of that family, on all three boards and settings, for the heaps
   `0, 1, 2` and both movers: `wide_agrees_spec`.
3. `wide` equals `wideSlow` (the same search with `moves`, `Env.verdict` and `hasPassed` of `Rules.lean`, no
   ordering, no early exit, every answer stored) on the wall rings on the cylinder for the widths where that runs:
   `wide_agrees_slow_rings`.
-/
namespace CylChess.WideAgrees
open CylChess CylChess.Wide CylChess.Claims CylChess.Agrees

/-- `wide` with the rules of `Rules.lean` used directly: all moves, `Env.verdict`, no ordering. -/
def wideSlow (e : Env) : Nat → Position → Nat → Color → M (Option Bool)
  | 0, _, _, _ => pure none
  | f + 1, pos, h, c => do
    match (← get)[(pos, h, c)]? with
    | some b => pure (some b)
    | none =>
      let mut unknown := false
      let mut res : Option Bool := some false
      for q in moves e.s e.b pos c do
        match e.verdict q c with
        | .decided w => if w == c then res := some true
        | .undefined => unknown := true
        | .open_ =>
          match ← wideSlow e f q h c.other with
          | some false => res := some true
          | some true => pure ()
          | none => unknown := true
      for i in List.range h do
        match ← wideSlow e f pos i c.other with
        | some false => res := some true
        | some true => pure ()
        | none => unknown := true
      let out := if res == some true then res else if unknown then none else some false
      if let some b := out then modify (·.insert (pos, h, c) b)
      pure out

def slowRun (e : Env) (fuel : Nat) (pos : Position) (h : Nat) (c : Color) : Option Bool :=
  (wideSlow e fuel pos h c).run' {}

/-! ## 1. The passed-pawn test -/

def boards3 : List Board :=
  [{ files := 3, ranks := 5, topology := .flat }, { files := 3, ranks := 5, topology := .cylinder },
   { files := 3, ranks := 5, topology := .mobius }]

/-- All positions reachable from `p` by pawn moves of either side in any order (depth-first, no repeats
suppressed: the trees are small). -/
def reach (e : Env) : Nat → Position → List Position
  | 0, p => [p]
  | f + 1, p => p :: ((moves e.s e.b p .white ++ moves e.s e.b p .black).flatMap (reach e f))

def passedAgreesOn (e : Env) (q : Position) : Bool :=
  passedF e.s e.b q .white == hasPassed e.s e.b q .white && passedF e.s e.b q .black == hasPassed e.s e.b q .black

def casesAll : List (Env × Position) :=
  boards3.flatMap fun b => settings3.flatMap fun s => family.map fun p => (env s b, p)

/-- Every position reached within two moves (either side) of a family position. -/
def passedAgreesFrom (ep : Env × Position) : Bool :=
  (reach ep.1 2 ep.2).all (passedAgreesOn ep.1)

theorem passed_agrees : casesAll.all passedAgreesFrom = true := by native_decide

/-! ## 2. The search against the naive specification -/

def casesOpen : List (Env × Position) :=
  casesAll.filter fun (e, p) => !hasPassed e.s e.b p .white && !hasPassed e.s e.b p .black

def agreeSpec (ep : Env × Position) : Bool :=
  let (e, p) := ep
  [0, 1, 2].all fun h => colors.all fun c => WH e 60 p h c == wideRun e 400 p h c

theorem family_open_size : casesOpen.length = 5010 := by native_decide

theorem wide_agrees_spec : casesOpen.all agreeSpec = true := by native_decide

/-! ## 3. The search against the unordered, fully stored search on rings -/

def rep (k : Nat) (xs : List String) : List String := (List.replicate k xs).flatten

/-- `O_n` for odd `n ≥ 5` (S13): `W23B4, B5, W2B5, (W3, B5)^k`. -/
def wallOdd (n : Nat) : Position := ofFiles (["W23B4", "B5", "W2B5"] ++ rep ((n - 3) / 2) ["W3", "B5"])

/-- `E_n` for even `n ≥ 6` (S13): `B5, W2B5, W35B6, W2, (B4, W2)^(m+1)`, `n = 2m + 6`. -/
def wallEven (n : Nat) : Position := ofFiles (["B5", "W2B5", "W35B6", "W2"] ++ rep ((n - 6) / 2 + 1) ["B4", "W2"])

def wall (n : Nat) : Position := if n % 2 == 1 then wallOdd n else wallEven n

def cylEnv (n : Nat) : Env := { s := Settings.default, b := { files := n, topology := .cylinder } }

def agreeRing (n : Nat) : Bool :=
  [0, 1, 2, 3].all fun h => colors.all fun c =>
    wideRun (cylEnv n) 600 (wall n) h c == slowRun (cylEnv n) 600 (wall n) h c

theorem wide_agrees_slow_rings : (List.range 6).all (fun i => agreeRing (5 + i)) = true := by native_decide

end CylChess.WideAgrees
