import CylChess.Census

/-!
# Exhaustive scan of the rings with few pawns on `C_n` (minimality of `n + 3`)

`rings n w b`: every position on the cylinder `C_n` (eight ranks) with `w` white pawns on ranks 2-6 and `b` black pawns
on ranks 3-7 (a white pawn on rank 7 or a black pawn on rank 2 is passed, as in the census), every file occupied (a
*ring*: one pawn on every file at least, §2.5), and no passed pawn in the default setting. No reduction by rotation or
mirror image is made.

`scan n p` tallies the rings with `p` pawns in total: how many there are, and how many have value `*2` (and how many have
a value `*j` for some `j ≥ 2`), by `Heaps.sets` (all heaps at once).
-/
namespace CylChess
namespace RingScan
open Census Heaps

def cyl (n : Nat) : Board := { files := n, topology := .cylinder }

def rings (n w b : Nat) : List Position :=
  (combos w (squares n 2 6)).flatMap fun wt =>
    (combos b (squares n 3 7)).filterMap fun bt =>
      let files := (wt ++ bt).map (·.1)
      if wt.any (fun q => bt.contains q) then none
      else if !((List.range n).all fun f => files.contains f) then none
      else
        let pos := Position.ofSquares wt bt
        if hasPassed Settings.default (cyl n) pos .white || hasPassed Settings.default (cyl n) pos .black then none
        else some pos

structure RTally where
  rings : Nat := 0
  star2 : Nat := 0
  anyBig : Nat := 0
  failed : Nat := 0
  deriving DecidableEq, Repr

def RTally.add (a b : RTally) : RTally := ⟨a.rings + b.rings, a.star2 + b.star2, a.anyBig + b.anyBig, a.failed + b.failed⟩

def tallyRings (n : Nat) (ps : List Position) : RTally :=
  let e : Env := { s := Settings.default, b := cyl n }
  let act : StateM Memo RTally := ps.foldlM (fun acc p => do
    match ← Heaps.ofPosition e 400 p with
    | none => pure (acc.add { rings := 1, failed := 1 })
    | some q =>
      let lost := lostHeaps q
      pure (acc.add { rings := 1, star2 := if lost.mem 2 then 1 else 0,
                      anyBig := if lost.cof || lost.bits >>> 2 != 0 then 1 else 0 })) {}
  act.run' {}

/-- All rings on `C_n` with exactly `p` pawns, in pieces of `chunk` positions with a fresh memo for each. -/
def scan (n p chunk : Nat) : RTally :=
  ((List.range (p - 1)).map fun i =>
    (chunks chunk (rings n (i + 1) (p - 1 - i))).map (tallyRings n)
      |>.foldl RTally.add {}).foldl RTally.add {}

end RingScan
end CylChess

namespace CylChess
namespace RingScan
open Census Heaps

/-- The rings with `p` pawns on `C_n` whose value is `*2`, as positions (the same enumeration as `scan`). -/
def star2Rings (n p chunk : Nat) : List Position :=
  ((List.range (p - 1)).flatMap fun i =>
    (chunks chunk (rings n (i + 1) (p - 1 - i))).flatMap fun ps =>
      let e : Env := { s := Settings.default, b := cyl n }
      let act : StateM Memo (List Position) := ps.filterM (fun q => do
        match ← Heaps.ofPosition e 400 q with
        | none => pure true            -- unsettled: keep it, so that nothing is lost silently
        | some r => pure ((lostHeaps r).mem 2))
      act.run' {})

/-- The image of a position on `C_n` under: mirror `f ↦ n-1-f` (if `mir`), then rotation `f ↦ f + rot`, then exchange of
the colours with the ranks `r ↦ 9 - r` (if `swap`). -/
def transform (n rot : Nat) (mir swap : Bool) (p : Position) : Position :=
  let g (q : Pawn) : Square := (((if mir then n - 1 - q.file else q.file) + rot) % n, if swap then 9 - q.rank else q.rank)
  let w := p.white.map g
  let b := p.black.map g
  if swap then Position.ofSquares b w else Position.ofSquares w b

/-- The orbit of a position under the `n` rotations, the mirror image and the colour reversal (as a list, repeats allowed). -/
def orbit (n : Nat) (p : Position) : List Position :=
  (List.range n).flatMap fun r => [false, true].flatMap fun m => [false, true].map fun s => transform n r m s p

end RingScan
end CylChess
