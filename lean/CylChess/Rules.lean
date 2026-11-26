/-!
# The pawn game of the paper: rules only

This file is the trusted base. It states the rules and nothing else; searches and theorems live elsewhere.

Sources, cited below as
* §2.1 ... §2.5: `dist/tog/sections/02_rules.tex` (2.1 Board and Moves, 2.3 Normal Play and the Passed-Pawn
  Convention, 2.4 En Passant and the Passed-Pawn Test, 2.5 Components and the Cut Lemma);
* §5: `dist/tog/sections/05_sums.tex`, "When Is the Sum Model Right?";
* S6: `dist/tog/supp/s06.tex`, "Rings on the Möbius Strip";
* N5: `dist/tog/supp_src/s15_note5.md`, §1 "Rules" (the Möbius rules in full).

Coordinates: files `0 .. files-1` (file a is `0`), ranks `1 .. ranks`. Kings are not modelled (§2.3: the
model "never moves them and counts the group as 0").

Choices settled only by N5 (the main text is silent on them). All the programs follow N5, and so does this file:
1. A pawn's home rank (and so its double step) follows its direction, also for a pawn reversed on the strip
   (`Board.homeRank`; N5 "home rank, double step and distance follow d").
2. En passant on the strip may be taken by any pawn whose diagonal capture square is the skipped square, not
   only by a pawn beside the arrival square (`Board.epCaptures`; N5 "any pawn whose diagonal capture square it
   is").
3. An enemy pawn blocks a passed pawn whatever its own direction (`Board.blocks`; N5 "no enemy pawn (either
   direction)").
4. The count rule uses only the front passed pawns of each side (`isFront`, `raceDistance`; N5 "over front
   passed pawns"). On flat boards and cylinders this gives the same minimum as the main text; on the strip two
   passed pawns of one colour facing each other on a file are both not front.
5. In a sum, an e.p. right survives moves made in other components and is cleared by the next move in its own
   component (N5 keeps the flag over heap moves). Here `moves` drops the right with any move of the position it
   is given, and `components` keeps it in the component of its pawn; the sum layer must keep it across moves
   made elsewhere.
-/
namespace CylChess

/-! ## Board -/

/-- The two players. "white (Left) ... black (Right)" (§2.2). -/
inductive Color | white | black
  deriving DecidableEq, Repr, Inhabited

def Color.other : Color → Color
  | .white => .black
  | .black => .white

/-- How the first and last files are joined.
* `flat`: "the ordinary board" (§2.1);
* `cylinder`: "the a-file joined to the h-file. Only the files wrap: ranks 1 and 8 are still edges" (§2.1);
* `mobius`: "The strip joins the first and last files with the ranks reversed: square (n,r) is beside
  (1,9-r)" (S6). -/
inductive Topology | flat | cylinder | mobius
  deriving DecidableEq, Repr

/-- "We write C_n and F_n for the cylinder and the ordinary board with n files and, unless we say otherwise,
eight ranks" (§2.1). The boards the rules are meant for are those with `Board.valid`. -/
structure Board where
  files : Nat
  ranks : Nat := 8
  topology : Topology
  deriving DecidableEq, Repr

/-- A board the rules are meant for (a decidable test): at least 3 files on the cylinder and on the Möbius
strip, the smallest the paper uses (C_3, and the strip from three files). The formulas below would still compute
on smaller boards, but not a game the paper means: on a 1-file cylinder file a is its own neighbour, so a pawn
would capture an enemy pawn straight ahead of it; on a 2-file cylinder or strip the other file is the
neighbour on both sides, so it is a neighbour twice (on the strip once straight and once in mirrored ranks).
Flat boards have no lower bound. -/
def Board.valid (b : Board) : Bool :=
  b.topology == Topology.flat || 3 ≤ b.files

/-- A square `(file, rank)`. -/
abbrev Square := Nat × Nat

/-- Rank `r` lies on the board. -/
def Board.onBoard (b : Board) (r : Nat) : Bool := 1 ≤ r && r ≤ b.ranks

/-- Rank `r` seen across the Möbius seam: "(n,r) is beside (1,9-r)" (S6), with `9 = ranks + 1`. -/
def Board.mirror (b : Board) (r : Nat) : Nat := b.ranks + 1 - r

/-- The file beside file `f` on the right (`right = true`, towards higher files) or on the left, and whether
ranks are mirrored there. "On the cylinder, a and h are neighbors" (§2.4); on the strip the neighbour across
the seam is "read in mirrored ranks" (S6); on the flat board an edge file has one neighbour. -/
def Board.beside (b : Board) (f : Nat) (right : Bool) : Option (Nat × Bool) :=
  -- The neighbour across the seam, which is file `g`: file 0 to the right of the last file, the last file to
  -- the left of file 0.
  let acrossSeam (g : Nat) : Option (Nat × Bool) := match b.topology with
    | .flat => none                 -- an edge file has one neighbour
    | .cylinder => some (g, false)  -- "the a-file joined to the h-file"
    | .mobius => some (g, true)     -- "(n,r) is beside (1,9-r)": ranks mirrored
  if right then (if f + 1 < b.files then some (f + 1, false) else acrossSeam 0)
  else (if 0 < f then some (f - 1, false) else acrossSeam (b.files - 1))

/-! ## Pawns and positions -/

/-- A pawn: its square and its direction (`up = true`: towards rank `ranks`). On the flat board and the
cylinder white pawns move up and black pawns down. On the strip "Every pawn has a direction; white pawns start
moving up and black pawns down, and a capture across the seam lands on the mirrored rank and reverses the
direction of the capturing pawn" (S6). -/
structure Pawn where
  file : Nat
  rank : Nat
  up : Bool
  deriving DecidableEq, Repr

def Pawn.sq (p : Pawn) : Square := (p.file, p.rank)

/-- The order of the normal form: by file, then by rank. -/
def Pawn.before (p q : Pawn) : Bool := p.file < q.file || (p.file == q.file && p.rank < q.rank)

/-- The rank one step ahead of rank `r` for a pawn moving `up` (`0` or `ranks + 1` means off the board). -/
def ahead (up : Bool) (r : Nat) : Nat := if up then r + 1 else r - 1

/-- Rank `s` is strictly ahead of rank `r` for a pawn moving `up`. -/
def isAhead (up : Bool) (r s : Nat) : Bool := if up then r < s else s < r

/-- The home rank, from which a double step is allowed: 2 for a pawn moving up, `ranks - 1` moving down
(ordinary chess, §2.1); on the strip "Double step and promotion follow the direction" (S6). -/
def Board.homeRank (b : Board) (up : Bool) : Nat := if up then 2 else b.ranks - 1

/-- A position: white pawns, black pawns, and the square of a pawn that may be taken en passant now.
Normal form (`Position.normalize`): each list sorted strictly by `Pawn.before`; `ep = some q` only if the pawn
on `q` has just made a double step and an enemy pawn can take it en passant. Then equal positions are equal
terms. The side to move is not part of a position (normal play: both sides' options are listed, §2.2).

Who may use the e.p. right: only the colour that does not own the pawn on `ep` (its opponent), on its next move.
Asking `moves` for the owner's colour (a second move in the same component, as in a sum) simply clears it. -/
structure Position where
  white : List Pawn
  black : List Pawn
  ep : Option Square := none
  deriving DecidableEq, Repr

def Position.pawns (pos : Position) : Color → List Pawn
  | .white => pos.white
  | .black => pos.black

def Position.occupied (pos : Position) (q : Square) : Bool :=
  (pos.white ++ pos.black).any (·.sq == q)

/-- The colour and pawn standing on square `q`, if any. -/
def Position.at? (pos : Position) (q : Square) : Option (Color × Pawn) :=
  match pos.white.find? (·.sq == q), pos.black.find? (·.sq == q) with
  | some p, _ => some (.white, p)
  | none, some p => some (.black, p)
  | none, none => none

/-- Insertion sort (structural, so that `decide` can evaluate it). -/
def insertBy {α : Type} (lt : α → α → Bool) (x : α) : List α → List α
  | [] => [x]
  | y :: ys => if lt y x then y :: insertBy lt x ys else x :: y :: ys

def sortBy {α : Type} (lt : α → α → Bool) : List α → List α
  | [] => []
  | x :: xs => insertBy lt x (sortBy lt xs)

/-! ## Settings -/

/-- "three e.p. options (textbook test, e.p.-aware test, e.p. off)" (§2.4). -/
inductive EpRule | off | textbook | aware
  deriving DecidableEq, Repr

/-- The three race rules `count`, `mover`, `opponent` (§2.3). -/
inductive RaceRule | count | mover | opponent
  deriving DecidableEq, Repr

/-- "The three race rules and three e.p. options ... give nine settings" (§2.4). -/
structure Settings where
  ep : EpRule
  race : RaceRule
  deriving DecidableEq, Repr

/-- "the default setting (count rule, e.p.-aware test)" (§2.4). -/
def Settings.default : Settings := ⟨.aware, .count⟩

/-- "we use BIG = 256" (§2.3): the score of a won component in the sum model S(X) (§5). -/
def BIG : Int := 256

/-! ## Moves -/

/-- Where pawn `p` lands when it captures diagonally forward on the `right` or left side, with its new
direction: "a white pawn on h4 can capture on a5" (§2.1); on the strip "a capture across the seam lands on the
mirrored rank and reverses the direction of the capturing pawn" (S6). -/
def Board.captureTo (b : Board) (p : Pawn) (right : Bool) : Option Pawn :=
  match b.beside p.file right with
  | none => none
  | some (g, flip) =>
    let r := ahead p.up p.rank
    if !b.onBoard r then none
    else if flip then some ⟨g, b.mirror r, !p.up⟩ else some ⟨g, r, p.up⟩

def Board.captureTargets (b : Board) (p : Pawn) : List Pawn := [true, false].filterMap (b.captureTo p)

/-- The en passant captures of pawn `v` of colour `c`, which has just made a double step, as pairs
(capturer, capturer after the capture): "the opponent may, on the next move only, capture onto the skipped
square with any pawn whose diagonal capture square it is" (N5); "En passant (e.p.) is allowed, across the seam
too" (§2.1). -/
def Board.epCaptures (b : Board) (pos : Position) (c : Color) (v : Pawn) : List (Pawn × Pawn) :=
  let skipped : Square := (v.file, ahead (!v.up) v.rank)
  (pos.pawns c.other).flatMap fun q =>
    (b.captureTargets q).filterMap fun t => if t.sq == skipped then some (q, t) else none

/-- The position after colour `c` moved, from `c`'s pawns `mine` and the opponent's pawns `theirs`. -/
def Position.build (c : Color) (mine theirs : List Pawn) (ep : Option Square) : Position :=
  let m := sortBy Pawn.before mine
  let t := sortBy Pawn.before theirs
  match c with
  | .white => ⟨m, t, ep⟩
  | .black => ⟨t, m, ep⟩

/-! Each of the next four functions lists the moves of one kind of pawn `p` of colour `c` ("ordinary chess",
§2.1). Every result drops an earlier e.p. right (the right lapses with any move), except that a double step may
record a new one. Off-board ranks are `0` and `ranks + 1` (`ahead` uses `Nat` subtraction); `onBoard` rejects
both. -/

/-- Single step: one square ahead, onto an empty square. -/
def stepMoves (b : Board) (pos : Position) (c : Color) (p : Pawn) : List Position :=
  let r1 := ahead p.up p.rank
  if b.onBoard r1 && !pos.occupied (p.file, r1) then
    [Position.build c ({ p with rank := r1 } :: (pos.pawns c).erase p) (pos.pawns c.other) none]
  else []

/-- Double step: from the home rank, two squares ahead, both empty. It records an e.p. right on the arrival
square only if e.p. is on and an enemy pawn can use it (normal form). -/
def doubleStepMoves (s : Settings) (b : Board) (pos : Position) (c : Color) (p : Pawn) : List Position :=
  let r1 := ahead p.up p.rank
  let r2 := ahead p.up r1
  if p.rank == b.homeRank p.up && b.onBoard r1 && b.onBoard r2
      && !pos.occupied (p.file, r1) && !pos.occupied (p.file, r2) then
    let p2 : Pawn := { p with rank := r2 }
    let after := Position.build c (p2 :: (pos.pawns c).erase p) (pos.pawns c.other) none
    let ep := if s.ep != EpRule.off && !(b.epCaptures after c p2).isEmpty then some p2.sq else none
    [{ after with ep := ep }]
  else []

/-- Capture: diagonally forward onto an enemy pawn, across the seam where there is one: "a white pawn on h4
can capture on a5" (§2.1). -/
def captureMoves (b : Board) (pos : Position) (c : Color) (p : Pawn) : List Position :=
  let theirs := pos.pawns c.other
  (b.captureTargets p).filterMap fun t =>
    (theirs.find? (·.sq == t.sq)).map fun q => Position.build c (t :: (pos.pawns c).erase p) (theirs.erase q) none

/-- En passant: "En passant (e.p.) is allowed, across the seam too" (§2.1). Only the colour `c` that does not
own the pawn `v` on the e.p. square can use the right (`v` is looked up among `c`'s enemies), with any pawn
whose diagonal capture square is the skipped square (N5). -/
def epMoves (s : Settings) (b : Board) (pos : Position) (c : Color) (p : Pawn) : List Position :=
  let theirs := pos.pawns c.other
  match pos.ep with
  | none => []
  | some e =>
    match theirs.find? (·.sq == e) with
    | none => []
    | some v =>
      if s.ep == EpRule.off then [] else
      (b.epCaptures pos c.other v).filterMap fun (q, t) =>
        if q == p then some (Position.build c (t :: (pos.pawns c).erase p) (theirs.erase v) none) else none

/-- All positions colour `c` can reach in one move: single step, double step, capture, en passant, for every
pawn of `c`, without repeats. "a player who has no move loses; there are no null moves" (§2.3): an empty list is
a loss for `c`. -/
def moves (s : Settings) (b : Board) (pos : Position) (c : Color) : List Position :=
  ((pos.pawns c).flatMap fun p =>
    stepMoves b pos c p ++ doubleStepMoves s b pos c p ++ captureMoves b pos c p ++ epMoves s b pos c p).eraseDups

/-! ## Passed pawns and the end of the game -/

/-- Enemy pawn `q` stands ahead of pawn `p`: "no enemy pawn stands ahead of it on its own file or a
neighboring file (on the cylinder, a and h are neighbors)" (§2.4); on the strip "no enemy pawn is strictly
ahead of it, in its own direction, on its file or a neighboring file, the seam neighbor being read in mirrored
ranks" (S6). -/
def Board.blocks (b : Board) (p q : Pawn) : Bool :=
  (q.file == p.file && isAhead p.up p.rank q.rank) ||
  [true, false].any fun right =>
    match b.beside p.file right with
    | some (g, flip) => q.file == g && isAhead p.up p.rank (if flip then b.mirror q.rank else q.rank)
    | none => false

/-- "The textbook test calls a pawn passed if no enemy pawn stands ahead of it on its own file or a
neighboring file" (§2.4). A pawn on its last rank passes it: "a pawn on its last rank counts as passed" (§2.3). -/
def textbookPassed (b : Board) (pos : Position) (c : Color) (p : Pawn) : Bool :=
  (pos.pawns c.other).all fun q => !b.blocks p q

/-- Pawn `p` of colour `c` "can be captured en passant on the opponent's next move" (Definition `def:epaware`). -/
def epCapturable (b : Board) (pos : Position) (c : Color) (p : Pawn) : Bool :=
  pos.ep == some p.sq && !(b.epCaptures pos c p).isEmpty

/-- Definition `def:epaware` (E.p.-aware passed pawn): "A pawn is passed if it passes the textbook test and cannot be
captured en passant on the opponent's next move." Under `textbook` and `off` only the textbook test applies. -/
def passed (s : Settings) (b : Board) (pos : Position) (c : Color) (p : Pawn) : Bool :=
  textbookPassed b pos c p && !(s.ep == EpRule.aware && epCapturable b pos c p)

def hasPassed (s : Settings) (b : Board) (pos : Position) (c : Color) : Bool :=
  (pos.pawns c).any (passed s b pos c)

/-- Moves to promote "as on an empty board with a double step as one move" (§2.3, count rule). -/
def Board.distance (b : Board) (p : Pawn) : Nat :=
  let d := if p.up then b.ranks - p.rank else p.rank - 1
  if p.rank == b.homeRank p.up && 2 ≤ d then d - 1 else d

/-- "A front pawn has no pawn of either colour ahead on its own file in its direction" (N5). -/
def isFront (pos : Position) (p : Pawn) : Bool :=
  !(pos.white ++ pos.black).any fun q => q.file == p.file && isAhead p.up p.rank q.rank

/-- The least distance over the front passed pawns of colour `c`; `none` stands for infinity (N5). -/
def raceDistance (s : Settings) (b : Board) (pos : Position) (c : Color) : Option Nat :=
  (((pos.pawns c).filter fun p => passed s b pos c p && isFront pos p).map b.distance).min?

/-- `x ≤ y` with `none` as infinity. -/
def leInf : Option Nat → Option Nat → Bool
  | _, none => true
  | none, some _ => false
  | some x, some y => x ≤ y

/-- The winner of a race position reached by a move of `mover` (§2.3): "count: the side whose passed pawn
needs fewer moves to promote wins ...; a tie goes to the side that did not move; mover: the side that made the
move wins; opponent: the other side wins." -/
def raceWinner (s : Settings) (b : Board) (pos : Position) (mover : Color) : Color :=
  match s.race with
  | .mover => mover
  | .opponent => mover.other
  | .count =>
    if leInf (raceDistance s b pos mover.other) (raceDistance s b pos mover) then mover.other else mover

/-- The classification of a position. -/
inductive Outcome
  | notEnded
  | won (c : Color)
  | race (winner : Color)
  deriving DecidableEq, Repr

/-- The position reached by a move of `mover`: "A position in which exactly one side has a passed pawn is
decided" (§2.3); "A move that gives both sides a passed pawn makes a race position, decided by one of three
rules" (§2.3). On the whole board "the first passed pawn ends the game" (§5).

`mover` must be the colour that has just moved to reach `pos`; it matters only for a race. -/
def classify (s : Settings) (b : Board) (pos : Position) (mover : Color) : Outcome :=
  match hasPassed s b pos .white, hasPassed s b pos .black with
  | false, false => .notEnded
  | true, false => .won .white
  | false, true => .won .black
  | true, true => .race (raceWinner s b pos mover)

/-! ## Components -/

/-- Maximal runs of consecutive numbers in an increasing list. -/
def runs : List Nat → List (List Nat)
  | [] => []
  | f :: fs =>
    match runs fs with
    | (g :: gs) :: rest => if g == f + 1 then (f :: g :: gs) :: rest else [f] :: (g :: gs) :: rest
    | other => [f] :: other

/-- The pawns (and the e.p. right) on the files `fs`. -/
def Position.restrict (pos : Position) (fs : List Nat) : Position :=
  { white := pos.white.filter (fs.contains ·.file), black := pos.black.filter (fs.contains ·.file),
    ep := pos.ep.filter (fs.contains ·.1) }

/-- "Each block of neighboring occupied files is a game of its own, a component ...; on the cylinder a
component is an arc or one ring that uses every file" (§2.5). An arc may wrap around the seam (cylinder and
strip). Components stay on the same board, in the same coordinates. -/
def components (b : Board) (pos : Position) : List Position :=
  let occ := (List.range b.files).filter fun f => (pos.white ++ pos.black).any (·.file == f)
  let groups := runs occ
  -- Off the flat board, merge the run ending at the last file with the run starting at file 0: they are
  -- neighbours across the seam. `middle` is every run after `first`, so `middle.dropLast` is the runs between
  -- `first` and `last`. With a single run there is nothing to merge (if it starts at 0 and ends at the last
  -- file it is the ring).
  let groups := match groups, groups.getLast? with
    | first :: middle@(_ :: _), some last =>
      if b.topology != Topology.flat && first.head? == some 0 && last.getLast? == some (b.files - 1) then
        (last ++ first) :: middle.dropLast
      else groups
    | _, _ => groups
  groups.map pos.restrict

/-! ## Normal form -/

/-- Sort both lists and keep an e.p. right only if it is real: e.p. is on, the pawn on that square stands two
steps ahead of its home rank with the two squares behind it empty, and an enemy pawn can take it. -/
def Position.normalize (s : Settings) (b : Board) (pos : Position) : Position :=
  let base : Position := ⟨sortBy Pawn.before pos.white, sortBy Pawn.before pos.black, none⟩
  let ep := pos.ep.filter fun e =>
    match base.at? e with
    | none => false
    | some (c, v) =>
      let home := b.homeRank v.up
      s.ep != EpRule.off && v.rank == ahead v.up (ahead v.up home)
        && !base.occupied (v.file, ahead v.up home) && !base.occupied (v.file, home)
        && !(b.epCaptures base c v).isEmpty
  { base with ep := ep }

/-- A position the rules accept: a valid board (`Board.valid`), squares on the board, no two pawns on one square,
and, on flat boards and cylinders, white pawns moving up and not on rank 1, black pawns moving down and not on
the last rank (the atlas, `dist/tog/sections/06_atlas.tex`, has "every pawn on ranks 2--7"; a pawn behind its home rank occurs in no game).
On the strip pawns may move either way and no rank is excluded: the analogous condition (no pawn on the rank
behind its home rank, in its own direction) is not stated in the paper, so the strip is left as it was. -/
def Position.valid (b : Board) (pos : Position) : Bool :=
  let all := pos.white ++ pos.black
  b.valid
    && all.all (fun p => p.file < b.files && b.onBoard p.rank)
    && (all.map Pawn.sq).eraseDups.length == all.length
    && (b.topology == Topology.mobius
        || (pos.white.all (fun p => p.up && p.rank != 1) && pos.black.all (fun p => !p.up && p.rank != b.ranks)))

end CylChess
