import CylChess.Search
import CylChess.Claims.L5_Eighth

/-!
# Evidence that `Search` computes what `Game` specifies

**This is a test, not a proof.** "Agree" means: at fuel 400 the two return the same answer on the family below. They
need not agree at equal small fuel (the fast search cancels integers and can be definite where the specification runs
out of fuel); only the definite answers `some b` are the true outcomes. `Search.lean` is not shown equal to `Game.lean`; both are only run on a finite
family of positions and compared with `native_decide` (compiled code, so this also trusts the compiler).

## The family (exact)

For each board `flat` and `cylinder` with 3 files and 5 ranks, each of the three settings
`⟨aware, count⟩`, `⟨textbook, mover⟩`, `⟨off, opponent⟩`, and each position with
* exactly two white pawns on files a-c, ranks 2-4, and exactly two black pawns on files a-c, ranks 2-5, on four
  distinct squares (36 white pairs; black pairs among the remaining squares),
* no passed pawn at the root (in that setting),
the following eight outcomes agree between `Game` and `Search` (`BIG = 256`, fuel 400), 3378 positions
in all (`family_size`): `W` with White to move and with Black to move; and `outcome` (the sum of the position's
components and a game tree) for each mover and each of the trees `0` (this is `S`), `*1` and `1/2`.

Then one more test on the position of Theorem `thm:eighth`: the specification and the fast search agree on
`isValue` for the nine settings, and for three race assignments (all won by White, all won by Black,
alternating) on the 8x8 board.
-/
namespace CylChess.Agrees
open CylChess CylChess.Claims

/-- Unordered pairs. -/
def pairs {α : Type} : List α → List (α × α)
  | [] => []
  | x :: xs => xs.map (x, ·) ++ pairs xs

def sq35 (rlo rhi : Nat) : List Square :=
  (List.range 3).flatMap fun f => (List.range (rhi - rlo + 1)).map fun r => (f, rlo + r)

/-- All positions of the family (before the passed-pawn filter). -/
def family : List Position :=
  (pairs (sq35 2 4)).flatMap fun (w1, w2) =>
    ((pairs ((sq35 2 5).filter fun q => q != w1 && q != w2))).map fun (b1, b2) =>
      Position.ofSquares [w1, w2] [b1, b2]

def boards : List Board := [{ files := 3, ranks := 5, topology := .flat }, { files := 3, ranks := 5, topology := .cylinder }]

def settings3 : List Settings := [⟨.aware, .count⟩, ⟨.textbook, .mover⟩, ⟨.off, .opponent⟩]

def trees : List Tree := [Tree.zero, Tree.star 1, Tree.dy 1]

def colors : List Color := [.white, .black]

/-- Every position of the family on every board and setting. -/
def cases : List (Env × Position) :=
  boards.flatMap fun b => settings3.flatMap fun s =>
    (family.filter fun p => !hasPassed s b p .white && !hasPassed s b p .black).map fun p => (env s b, p)

/-- One position: the specification and the search give the same answers. -/
def agreeOn (ep : Env × Position) : Bool :=
  let (e, p) := ep
  colors.all (fun c => W e fuel p c == Search.wholeBoard e fuel p c) &&
  trees.all fun t => colors.all fun c => outcome e fuel p t c == Search.outcome e fuel p t c

theorem family_size : cases.length = 3378 := by native_decide

theorem search_agrees_on_family : cases.all agreeOn = true := by native_decide

/-- The position of Theorem `thm:eighth`: nine settings, and three race assignments. -/
def agreeEighth : Bool :=
  allSettings.all (fun s => isValue (env s flat8) fuel posG Tree.eighth == Search.isValue (env s flat8) fuel posG Tree.eighth) &&
  (let s : Settings := ⟨.aware, .count⟩
   let keys := raceKeys (env s flat8) posG
   [keys.map fun _ => Color.white, keys.map fun _ => Color.black,
    (List.range keys.length).map fun i => if i % 2 == 0 then Color.white else Color.black].all fun ws =>
     let e := envTable s (keys.zip ws)
     isValue e fuel posG Tree.eighth == Search.isValue e fuel posG Tree.eighth)

theorem search_agrees_eighth : agreeEighth = true := by native_decide

end CylChess.Agrees
