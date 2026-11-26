import CylChess.Heaps

/-!
# The census of Section 4 (`dist/tog/sections/06_atlas.tex`, Theorem `thm:census`): the list of positions

> "The census holds every such position with at most six pawns on `F_1, ..., F_4`, up to translation and mirror
> image: 231,071 records standing for 459,443 positions." (every such position: every pawn on ranks 2-7, at least
> one pawn per side, no passed pawn.)

The list is generated here exactly as `atlas/flat8/rerun/enumerate.py` (`gen_class`) generates it: for each width
`W` in `1..4`, and each `w, b ≥ 1` with `w + b ≤ 6`, the positions with `w` white pawns on ranks 2-6 and `b` black pawns
on ranks 3-7 of files `0 .. W-1`, files `0` and `W-1` both occupied (so a position that fits on at most four files
appears once up to translation), no passed pawn (textbook test; with no e.p. right at the root the e.p.-aware test
agrees), and the lexicographically smaller of the position and its mirror image `f ↦ W-1-f` (a position equal to its
mirror image stands for one board position, the others for two). Ranks 2-6 for White and 3-7 for Black: a white pawn
on rank 7 and a black pawn on rank 2 is always passed, and rank 8 (rank 1) holds no pawn of the other side.
-/
namespace CylChess
namespace Census

/-- All `k`-element sublists, in the order of the list. -/
def combos {α : Type} : Nat → List α → List (List α)
  | 0, _ => [[]]
  | _ + 1, [] => []
  | k + 1, x :: xs => (combos k xs).map (x :: ·) ++ combos (k + 1) xs

/-- Lexicographic order on lists of squares. -/
def lexLt : List Square → List Square → Bool
  | [], _ => false
  | _ :: _, [] => false
  | a :: as, b :: bs => a.1 < b.1 || (a.1 == b.1 && (a.2 < b.2 || (a.2 == b.2 && lexLt as bs)))

/-- The squares on files `0 .. W-1` and ranks `lo .. hi`, files first (so sublists come out sorted). -/
def squares (W lo hi : Nat) : List Square :=
  (List.range W).flatMap fun f => (List.range (hi - lo + 1)).map fun r => (f, lo + r)

def mirrorSq (W : Nat) (q : Square) : Square := (W - 1 - q.1, q.2)

/-- The board of the census: a flat board with four files (a position on fewer files is the same game). -/
def board : Board := { files := 4, topology := .flat }

/-- A record: the position, and the number of board positions it stands for (1 or 2). -/
structure Rec where
  pos : Position
  mult : Nat

/-- The records of the class `(W, w, b)`. -/
def records (W w b : Nat) : List Rec :=
  (combos w (squares W 2 6)).flatMap fun wt =>
    (combos b (squares W 3 7)).filterMap fun bt =>
      let files := (wt ++ bt).map (·.1)
      if wt.any (fun q => bt.contains q) then none
      else if !(files.contains 0 && files.contains (W - 1)) then none
      else
        let mw := (wt.map (mirrorSq W)).toArray.qsort (fun x y => lexLt [x] [y]) |>.toList
        let mb := (bt.map (mirrorSq W)).toArray.qsort (fun x y => lexLt [x] [y]) |>.toList
        let key := wt ++ bt
        let mkey := mw ++ mb
        if lexLt mkey key then none
        else
          let pos := Position.ofSquares wt bt
          if hasPassed ⟨.textbook, .count⟩ board pos .white || hasPassed ⟨.textbook, .count⟩ board pos .black then none
          else some ⟨pos, if key == mkey then 1 else 2⟩

/-- The classes `(W, w, b)` in scope. -/
def classes : List (Nat × Nat × Nat) :=
  (List.range 4).flatMap fun i => (List.range 5).flatMap fun a => (List.range (5 - a)).map fun c => (i + 1, a + 1, c + 1)

end Census
end CylChess

namespace CylChess
namespace Census
open Heaps

/-- Tally of a batch of records: records, board positions they stand for, records of value `0`, records of value `*`,
records whose set of heaps `j` with `X + *j` lost by the mover is neither `{0}`, `{1}` nor empty and contains no `j ≥ 2`
(`odd`, none expected), records with such a heap `j ≥ 2` (`big`, i.e. `X = *j`), records the computation did not settle
(`failed`). -/
structure Tally where
  recs : Nat := 0
  pos : Nat := 0
  zeros : Nat := 0
  stars : Nat := 0
  noNimber : Nat := 0
  big : Nat := 0
  failed : Nat := 0
  deriving DecidableEq, Repr

def Tally.add (a b : Tally) : Tally :=
  ⟨a.recs + b.recs, a.pos + b.pos, a.zeros + b.zeros, a.stars + b.stars, a.noNimber + b.noNimber,
   a.big + b.big, a.failed + b.failed⟩

/-- The environment of the census: the default setting (count rule, e.p.-aware test), `BIG` as given. -/
def env (big : Int := BIG) : Env := { s := Settings.default, b := board, big := big }

/-- Classify one record from the set of heaps `j` with `X + *j` lost by the mover whoever it is. -/
def classify (r : Rec) (lost : NS) : Tally :=
  let t : Tally := { recs := 1, pos := r.mult }
  if lost.cof || lost.bits >>> 2 != 0 then { t with big := 1 }
  else if lost.bits == 1 then { t with zeros := 1 }
  else if lost.bits == 2 then { t with stars := 1 }
  else { t with noNimber := 1 }

/-- Run a batch of records with one shared memo. -/
def tally (e : Env) (fuel : Nat) (rs : List Rec) : Tally :=
  let step (r : Rec) : StateM Memo Tally := do
    match ← Heaps.ofPosition e fuel r.pos with
    | none => pure { recs := 1, pos := r.mult, failed := 1 }
    | some p => pure (classify r (lostHeaps p))
  let act : StateM Memo Tally := rs.foldlM (fun acc r => do pure (acc.add (← step r))) {}
  act.run' {}

end Census
end CylChess

namespace CylChess
namespace Census

/-- Cut a list into pieces of at most `k` elements (`fuel` is the length of the list). -/
def chunksAux {α : Type} (k : Nat) : Nat → List α → List (List α)
  | 0, _ => []
  | _ + 1, [] => []
  | f + 1, l => l.take k :: chunksAux k f (l.drop k)

def chunks {α : Type} (k : Nat) (l : List α) : List (List α) := chunksAux (max k 1) l.length l

/-- The tally of a whole class `(W, w, b)`, in pieces of `chunk` records with a fresh memo for each piece. -/
def classTally (e : Env) (fuel chunk W w b : Nat) : Tally :=
  ((chunks chunk (records W w b)).map (tally e fuel)).foldl Tally.add {}

/-- The tally of a list of classes. -/
def classesTally (e : Env) (fuel chunk : Nat) (cs : List (Nat × Nat × Nat)) : Tally :=
  (cs.map fun (W, w, b) => classTally e fuel chunk W w b).foldl Tally.add {}

end Census
end CylChess
