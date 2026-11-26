import CylChess.Rules

/-!
# The specification: the pawn game as a combinatorial game, and who wins a sum

This file is trusted, together with `Rules.lean`. It is plain and slow on purpose.

* `Tree`: finite game trees (Left = White, Right = Black), nimbers `Tree.star k`, dyadic numbers
  `Tree.dy`, negatives `Tree.neg`.
* `Env`: board, settings, the score `big` of a won component, and the race assignment. By default a race
  position is decided by the setting's race rule (§2.3); a table of outcomes can replace it (Theorem
  `thm:eighth`: "for every assignment of outcomes to its race positions").
* The pawn game in the paper's value model (§2.3, §5): a pawn component offers the legal moves (`moves` of
  `Rules.lean`). After a move, if exactly one side has a passed pawn, the component *is* the integer
  `+big` (White) or `-big` (Black): `big` free moves for the winner, none for the other; if both have one
  (a race) the component is that integer for the race's winner; otherwise it is re-split along empty files
  (`components`) and the pieces add up.
* `Game.wins`: normal play (the player with no move loses) on a sum of components, by recursion on a fuel
  argument; `none` means the fuel ran out before the answer was known. An answer `some b` is the true
  outcome whatever the fuel is.
* `IsValue`: `X` has value `v` iff `X + (-v)` is a second-player win (the mover loses, either mover).
* `S`: the sum model of §5; `W`: the whole-board game of §5.

No `partial`, `unsafe`, axiom or `sorry`.
-/
namespace CylChess

/-! ## Writing positions -/

/-- The square named by a file letter and a rank: `sqr 'a' 4` is a4 (file a is `0`). -/
def sqr (c : Char) (r : Nat) : Square := (c.toNat - 'a'.toNat, r)

/-- A position without an e.p. right from lists of squares: white pawns moving up, black pawns moving down,
in the normal form of `Rules.lean`. -/
def Position.ofSquares (w b : List Square) : Position :=
  ⟨sortBy Pawn.before (w.map fun q => ⟨q.1, q.2, true⟩),
   sortBy Pawn.before (b.map fun q => ⟨q.1, q.2, false⟩), none⟩

/-! ## Game trees -/

/-- A finite game: the games Left (White) can move to, and the games Right (Black) can move to. -/
inductive Tree
  | node (left right : List Tree)

namespace Tree

/-! The negative: swap the roles of the players everywhere. -/
mutual
def neg : Tree → Tree
  | node l r => node (negs r) (negs l)
def negs : List Tree → List Tree
  | [] => []
  | t :: ts => neg t :: negs ts
end

def zero : Tree := node [] []

/-- `stars k` is the list `*0, ..., *(k-1)`. -/
def stars : Nat → List Tree
  | 0 => []
  | k + 1 => stars k ++ [node (stars k) (stars k)]

/-- The nimber `*k`: either player may move to any of `*0, ..., *(k-1)` (§2.2). -/
def star (k : Nat) : Tree := node (stars k) (stars k)

/-- The dyadic number `1 / 2^k` in canonical form: `1 = {0 | }`, `1/2 = {0 | 1}`, `1/4 = {0 | 1/2}`,
`1/8 = {0 | 1/4}`. -/
def dy : Nat → Tree
  | 0 => node [zero] []
  | k + 1 => node [zero] [dy k]

/-- `1/8`. -/
def eighth : Tree := dy 3

end Tree

/-! ## Environment -/

/-- Everything the game depends on besides the position. `big` is the score of a won component
("we use BIG = 256", §2.3). `race pos mover` is the winner of the race position `pos` reached by a move of
`mover`; `none` means "not assigned": any outcome that depends on it is reported as unknown. -/
structure Env where
  s : Settings
  b : Board
  big : Int := BIG
  race : Position → Color → Option Color := fun pos mover => some (raceWinner s b pos mover)

/-- What a move led to. -/
inductive Verdict
  | open_                 -- no passed pawn: play goes on
  | decided (w : Color)   -- a passed pawn, or a race that `w` wins
  | undefined             -- a race the assignment does not cover

/-- §2.3: "A position in which exactly one side has a passed pawn is decided"; "A move that gives both sides
a passed pawn makes a race position". -/
def Env.verdict (e : Env) (pos : Position) (mover : Color) : Verdict :=
  match hasPassed e.s e.b pos .white, hasPassed e.s e.b pos .black with
  | false, false => .open_
  | true, false => .decided .white
  | false, true => .decided .black
  | true, true => match e.race pos mover with
    | some w => .decided w
    | none => .undefined

/-! ## Components and sums -/

/-- A component of a sum: a pawn position, an integer (`n > 0`: Left has `n` free moves; `n < 0`: Right has
`-n`), or a game tree. -/
inductive Comp
  | pawns (pos : Position)
  | num (n : Int)
  | tree (t : Tree)

/-- The games a player can move to from a component; `none` is a move whose result is undefined (an
unassigned race). A pawn move to an open position re-splits it along empty files. -/
def Comp.options (e : Env) (c : Color) : Comp → List (Option (List Comp))
  | .num n =>
    match c with
    | .white => if 0 < n then [some [.num (n - 1)]] else []
    | .black => if n < 0 then [some [.num (n + 1)]] else []
  | .tree (.node l r) => (match c with | .white => l | .black => r).map fun t => some [.tree t]
  | .pawns pos => (moves e.s e.b pos c).map fun q =>
    match e.verdict q c with
    | .open_ => some ((components e.b q).map .pawns)
    | .decided .white => some [.num e.big]
    | .decided .black => some [.num (-e.big)]
    | .undefined => none

/-- The moves of `c` in a sum: choose one component and move in it. -/
def Sum.options (e : Env) (c : Color) : List Comp → List (Option (List Comp))
  | [] => []
  | x :: xs =>
    (x.options e c).map (·.map (· ++ xs)) ++ (Sum.options e c xs).map (·.map (x :: ·))

/-- Did a search find a winning option? `some true` if some option is `some true`; `some false` if all are
`some false`; otherwise unknown. -/
def anyOpt : List (Option Bool) → Option Bool
  | [] => some false
  | o :: os =>
    match o with
    | some true => some true
    | some false => anyOpt os
    | none => match anyOpt os with | some true => some true | _ => none

/-- Normal play: does the player `c` to move win the sum `cs`? The player with no move loses. -/
def Game.wins (e : Env) : Nat → List Comp → Color → Option Bool
  | 0, _, _ => none
  | f + 1, cs, c =>
    anyOpt ((Sum.options e c cs).map fun o =>
      match o with
      | none => none
      | some cs' => (Game.wins e f cs' c.other).map (!·))

/-- The components of a position as a sum of pawn games. -/
def Comp.ofPosition (e : Env) (pos : Position) : List Comp := (components e.b pos).map .pawns

/-- The outcome of "pawn position + game tree" for the player `c` to move. -/
def outcome (e : Env) (fuel : Nat) (pos : Position) (t : Tree) (c : Color) : Option Bool :=
  Game.wins e fuel (Comp.ofPosition e pos ++ [.tree t]) c

/-- `X` has value `v` (§2.2: `G = H` exactly when `G - H` is a second-player win): in `X + (-v)` the player
to move loses, whoever it is. Returns `false` if this was not established within the fuel. The root position
must have no passed pawn (the paper defines a race only as the result of a move). -/
def isValue (e : Env) (fuel : Nat) (pos : Position) (v : Tree) : Bool :=
  !hasPassed e.s e.b pos .white && !hasPassed e.s e.b pos .black &&
  outcome e fuel pos v.neg .white == some false && outcome e fuel pos v.neg .black == some false

/-- `X` does not have value `v`: some player to move wins `X + (-v)`. (Unlike `¬ IsValue`, this is not
satisfied by running out of fuel.) -/
def notValue (e : Env) (fuel : Nat) (pos : Position) (v : Tree) : Bool :=
  outcome e fuel pos v.neg .white == some true || outcome e fuel pos v.neg .black == some true

def NotValue (e : Env) (fuel : Nat) (pos : Position) (v : Tree) : Prop := notValue e fuel pos v = true

instance (e : Env) (fuel : Nat) (pos : Position) (v : Tree) : Decidable (NotValue e fuel pos v) :=
  inferInstanceAs (Decidable (notValue e fuel pos v = true))

def IsValue (e : Env) (fuel : Nat) (pos : Position) (v : Tree) : Prop := isValue e fuel pos v = true

instance (e : Env) (fuel : Nat) (pos : Position) (v : Tree) : Decidable (IsValue e fuel pos v) :=
  inferInstanceAs (Decidable (isValue e fuel pos v = true))

/-! ## The two models of §5 -/

/-- `S(X)`, the sum model (§5): "after a move, the moved component becomes ±BIG if a side has a passed pawn
in it (by the race rule if both have one); otherwise it is re-split along empty files (one ring if no file is
empty); and the components add up." Here `S e fuel pos c`: does the player `c` to move win the sum of the
components of `pos`? (`none`: fuel ran out.)

Reading where the paper is silent: an en passant right belongs to the component of the pawn that made the
double step and stays available there after moves in other components (sum of games, as in
`cylcgt/pawns.py`, `_value`). Condition (E) of Theorem `thm:hss` excludes the cases where this differs from
the chess rule; `W` below applies the chess rule (the right lapses after one move). -/
def S (e : Env) (fuel : Nat) (pos : Position) (c : Color) : Option Bool :=
  Game.wins e fuel (Comp.ofPosition e pos) c

/-- `W(X)`, the whole-board game (§5): "the first passed pawn ends the game": the player whose move gives
exactly one side a passed pawn (or wins the race) has won; a player with no move loses. `W e fuel pos c`:
does the player `c` to move win? (`none`: fuel ran out or an unassigned race.) -/
def W (e : Env) : Nat → Position → Color → Option Bool
  | 0, _, _ => none
  | f + 1, pos, c =>
    anyOpt ((moves e.s e.b pos c).map fun q =>
      match e.verdict q c with
      | .open_ => (W e f q c.other).map (!·)
      | .decided w => some (w == c)
      | .undefined => none)

end CylChess
