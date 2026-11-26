import CylChess.Search

/-!
# The whole-board game with a nim heap, and a search for wide boards

The wall-ring proofs of the supplement (S13, S14, Notes 1 to 6 of S15) use a different game from the sum model
`S(X)` of `Game.lean`:

> "In the *whole-board game* `G + *h` the players alternate; the player to move makes a pawn move on `G` or
> lowers the heap. A pawn move to a terminal position ends the game, won by the winner of that position whoever
> would move next. A player with no move loses. There is no splitting of `G` into components." (S13, Model)
>
> "a heap move leaves the board and the flag unchanged" (S13, Model)

and (Section 5 of the paper): "We call `W(X)` a `*k` when `W(X) + *h` has the outcome of `*k + *h` for every heap `h`".

* `WH`: the specification, naive recursion on a fuel, the same shape as `Game.W` with the heap moves added. A
  terminal position is decided by `Env.verdict` (so by the race rule of the setting). The e.p. right of `pos` survives
  a heap move (`pos` is passed on unchanged); a pawn move drops it (`Rules.moves`).
* `wide`: the same outcomes, memoized, for wide boards. It differs from `WH` in these ways only:
  (1) `hasPassed` is replaced by `passedF`, which reads the highest and the lowest enemy rank on each file instead of
  looking at every enemy pawn (`SearchWideAgrees.lean` tests that they agree on every position reached);
  (2) the moves of a pawn are the four lists of `Rules.lean` (`stepMoves`, `doubleStepMoves`, `captureMoves`,
  `epMoves`), taken pawn by pawn, without `eraseDups` (a repeated option changes no outcome);
  (3) a move that wins at once is looked for first, among the pawns near the file of the last move (order and early
  exit change no outcome, since an answer `some true` needs one winning option and `some false` needs all of them
  lost);
  (4) only answers that needed a search below the node are stored.
  An answer `some b` is the true outcome whatever the fuel is (as in `Search`).

No `partial`, `unsafe`, axiom or `sorry`.
-/
namespace CylChess

/-- Number of pawns. -/
def Position.size (p : Position) : Nat := p.white.length + p.black.length

namespace Wide

/-! ## Writing positions as the supplement does -/

/-- A file written as in the supplement: `"W23B4"` is white pawns on ranks 2 and 3 and a black pawn on rank 4.
Returns the white and the black pawns of file `f`. -/
def parseFile (f : Nat) (s : String) : List Pawn × List Pawn :=
  let st := s.toList.foldl
    (fun (st : Bool × List Pawn × List Pawn) ch =>
      if ch == 'W' then (true, st.2.1, st.2.2)
      else if ch == 'B' then (false, st.2.1, st.2.2)
      else
        let r := ch.toNat - '0'.toNat
        if st.1 then (st.1, ⟨f, r, true⟩ :: st.2.1, st.2.2) else (st.1, st.2.1, ⟨f, r, false⟩ :: st.2.2))
    (true, [], [])
  (st.2.1, st.2.2)

/-- The position with file `i` holding `fs[i]`; no e.p. right. White pawns move up, black pawns down. -/
def ofFiles (fs : List String) : Position :=
  let ps := (fs.zipIdx).map fun (s, i) => parseFile i s
  ⟨sortBy Pawn.before (ps.flatMap (·.1)), sortBy Pawn.before (ps.flatMap (·.2)), none⟩

/-! ## The specification: whole board plus one heap -/

/-- `WH e fuel pos h c`: does the player `c` to move win the whole-board game `pos + *h`? `none`: the fuel ran out
(or an unassigned race). -/
def WH (e : Env) : Nat → Position → Nat → Color → Option Bool
  | 0, _, _, _ => none
  | f + 1, pos, h, c =>
    anyOpt (((moves e.s e.b pos c).map fun q =>
        match e.verdict q c with
        | .open_ => (WH e f q h c.other).map (!·)
        | .decided w => some (w == c)
        | .undefined => none) ++
      ((List.range h).map fun i => (WH e f pos i c.other).map (!·)))

/-! ## Fast passed-pawn test -/

/-- The highest and lowest rank of the pawns of one colour on each file (`0` and `1000` on an empty file). -/
structure Ext where
  mx : Array Nat
  mn : Array Nat

def Ext.ofPawns (n : Nat) (ps : List Pawn) : Ext :=
  ps.foldl (fun e p => ⟨e.mx.modify p.file (max · p.rank), e.mn.modify p.file (min · p.rank)⟩)
    ⟨Array.replicate n 0, Array.replicate n 1000⟩

/-- Some enemy pawn (the enemy's extremes are `ext`) stands strictly ahead of `p`, on its own file or a
neighbouring file, in the sense of `Board.blocks`; the seam neighbour is read in mirrored ranks. -/
def blockedF (b : Board) (ext : Ext) (p : Pawn) : Bool :=
  let r := p.rank
  let own := if p.up then decide (r < ext.mx[p.file]!) else decide (ext.mn[p.file]! < r)
  let nb (right : Bool) : Bool :=
    match b.beside p.file right with
    | none => false
    | some (g, flip) =>
      if flip then
        (if p.up then decide (ext.mn[g]! < b.ranks + 1 - r) else decide (b.ranks + 1 - r < ext.mx[g]!))
      else
        (if p.up then decide (r < ext.mx[g]!) else decide (ext.mn[g]! < r))
  own || nb true || nb false

/-- `hasPassed`, from the extremes of the enemy ranks per file. -/
def passedF (s : Settings) (b : Board) (pos : Position) (c : Color) : Bool :=
  let ext := Ext.ofPawns b.files (pos.pawns c.other)
  (pos.pawns c).any fun p => !blockedF b ext p && !(s.ep == EpRule.aware && epCapturable b pos c p)

/-- `Env.verdict`, with `passedF`. -/
def verdictF (e : Env) (pos : Position) (mover : Color) : Verdict :=
  match passedF e.s e.b pos .white, passedF e.s e.b pos .black with
  | false, false => .open_
  | true, false => .decided .white
  | false, true => .decided .black
  | true, true => match e.race pos mover with
    | some w => .decided w
    | none => .undefined

/-! ## The moves, pawn by pawn -/

/-- The moves of the pawn `p` of colour `c` (the four lists of `Rules.moves`). -/
def pawnMoves (e : Env) (pos : Position) (c : Color) (p : Pawn) : List Position :=
  stepMoves e.b pos c p ++ doubleStepMoves e.s e.b pos c p ++ captureMoves e.b pos c p ++ epMoves e.s e.b pos c p

/-- The pawns of `c`, those within two files of file `near` (round the seam, on a board with a seam) first. -/
def order (e : Env) (ps : List Pawn) (near : Nat) : List Pawn :=
  let n := e.b.files
  let close (p : Pawn) : Bool :=
    let d := if p.file < near then near - p.file else p.file - near
    d ≤ 2 || (e.b.topology != Topology.flat && (n - d) ≤ 2)
  ps.filter close ++ ps.filter (fun p => !close p)

/-! ## The search -/

abbrev Memo := Std.HashMap (Position × Nat × Color) Bool
abbrev M := StateM Memo

/-- The first pass over the moves of `c`: `none` if some move wins at once (a terminal position won by `c`);
otherwise the open children (with the file the moving pawn came from) and whether some move led to an unassigned
race. -/
def scan (e : Env) (pos : Position) (c : Color) (near : Nat) : Option (List (Position × Nat) × Bool) :=
  (order e (pos.pawns c) near).foldl
    (fun (acc : Option (List (Position × Nat) × Bool)) p =>
      match acc with
      | none => none
      | some (kids, unk) =>
        (pawnMoves e pos c p).foldl
          (fun (acc2 : Option (List (Position × Nat) × Bool)) q =>
            match acc2 with
            | none => none
            | some (kids, unk) =>
              match verdictF e q c with
              | .open_ => some ((q, p.file) :: kids, unk)
              | .decided w => if w == c then none else some (kids, unk)
              | .undefined => some (kids, true))
          (some (kids, unk)))
    (some ([], false))

/-- The outcome of the whole-board game `pos + *h` for the mover `c`; `near` is only a hint for the order. -/
def wide (e : Env) : Nat → Position → Nat → Color → Nat → M (Option Bool)
  | 0, _, _, _, _ => pure none
  | f + 1, pos, h, c, near => do
    match (← get)[(pos, h, c)]? with
    | some b => pure (some b)
    | none =>
      match scan e pos c near with
      | none => pure (some true)         -- a move that wins at once (not stored: it is quick to find again)
      | some (kids, unk) =>
        let mut unknown := unk
        let mut res : Option Bool := some false
        -- heap moves first, then the open children
        for i in List.range h do
          match ← wide e f pos i c.other near with
          | some false => res := some true; break
          | some true => pure ()
          | none => unknown := true
        if res != some true then
          for (q, fl) in kids do
            match ← wide e f q h c.other fl with
            | some false => res := some true; break
            | some true => pure ()
            | none => unknown := true
        let out := if res == some true then res else if unknown then none else some false
        if let some b := out then modify (·.insert (pos, h, c) b)
        pure out

/-- The outcome of `pos + *h` for mover `c`, fresh memo. -/
def wideRun (e : Env) (fuel : Nat) (pos : Position) (h : Nat) (c : Color) : Option Bool :=
  (wide e fuel pos h c 0).run' {}

/-- `pos + *h` is a P-position (the mover loses, whoever it is) and an N-position (the mover wins), one shared memo
for all heaps up to `hmax`. -/
def starTest (e : Env) (fuel : Nat) (pos : Position) (k hmax : Nat) : Bool :=
  !hasPassed e.s e.b pos .white && !hasPassed e.s e.b pos .black &&
  ((do
      let mut ok := true
      for h in List.range (hmax + 1) do
        let w ← wide e fuel pos h .white 0
        let b ← wide e fuel pos h .black 0
        let want : Option Bool := some (h != k)
        if !(w == want && b == want) then ok := false
      pure ok : M Bool).run' {})

/-- The outcomes (White to move, Black to move) for heaps `0..hmax`, for display. -/
def signature (e : Env) (fuel : Nat) (pos : Position) (hmax : Nat) : List (Option Bool × Option Bool) :=
  ((do
      let mut out := []
      for h in List.range (hmax + 1) do
        let w ← wide e fuel pos h .white 0
        let b ← wide e fuel pos h .black 0
        out := out ++ [(w, b)]
      pure out : M (List (Option Bool × Option Bool))).run' {})

/-- `W(pos + *k) ~ *k`: for each heap `h ≤ hmax`, `pos + *h` is lost by the mover (both movers) if `h = k` and won by
the mover (both movers) otherwise. -/
def WideStar (e : Env) (fuel : Nat) (pos : Position) (k hmax : Nat) : Prop := starTest e fuel pos k hmax = true

instance (e : Env) (fuel : Nat) (pos : Position) (k hmax : Nat) : Decidable (WideStar e fuel pos k hmax) :=
  inferInstanceAs (Decidable (starTest e fuel pos k hmax = true))

end Wide
end CylChess
