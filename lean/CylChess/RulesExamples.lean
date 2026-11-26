import CylChess.Rules

/-! Sanity checks of `CylChess.Rules`, all by `decide` (kernel evaluation). Files: a = 0, ..., h = 7. -/
namespace CylChess.Examples
open CylChess

/-- A white pawn (moving up) and a black pawn (moving down) on file `f`, rank `r`. -/
def w (f r : Nat) : Pawn := ⟨f, r, true⟩
def k (f r : Nat) : Pawn := ⟨f, r, false⟩

def cyl8 : Board := { files := 8, topology := .cylinder }
def flat8 : Board := { files := 8, topology := .flat }
def mob8 : Board := { files := 8, topology := .mobius }
def dflt := Settings.default
def tbook : Settings := ⟨.textbook, .count⟩

/-- Seam capture (§2.1): on the cylinder the white pawn on h4 takes on a5. -/
example : (moves dflt cyl8 ⟨[w 7 4], [k 0 5], none⟩ .white).contains ⟨[w 0 5], [], none⟩ := by decide
/-- ... but not on the ordinary board. -/
example : moves dflt flat8 ⟨[w 7 4], [k 0 5], none⟩ .white = [⟨[w 7 5], [k 0 5], none⟩] := by decide

/-- Möbius seam capture: h4 takes across the seam, lands on a4 (rank 9-5) and now moves down (S6). -/
example : (moves dflt mob8 ⟨[w 7 4], [k 0 4], none⟩ .white).contains ⟨[⟨0, 4, false⟩], [], none⟩ := by
  decide

/-- Fig. 1(a): W a2 / B b4. White's a2-a4 records an e.p. right on a4 ... -/
example : moves dflt flat8 ⟨[w 0 2], [k 1 4], none⟩ .white
    = [⟨[w 0 3], [k 1 4], none⟩, ⟨[w 0 4], [k 1 4], some (0, 4)⟩] := by decide
/-- ... and black takes en passant, b4xa3. -/
example : (moves dflt flat8 ⟨[w 0 4], [k 1 4], some (0, 4)⟩ .black).contains ⟨[], [k 0 3], none⟩ := by decide
/-- With e.p. off no right is recorded. -/
example : (moves ⟨.off, .count⟩ flat8 ⟨[w 0 2], [k 1 4], none⟩ .white).contains ⟨[w 0 4], [k 1 4], none⟩ := by
  decide

/-- A passed pawn: in W a5 c4 / B c5 on the flat board only the a-pawn is passed. -/
example : classify dflt flat8 ⟨[w 0 5, w 2 4], [k 2 5], none⟩ .black = .won .white := by decide
/-- On the cylinder a black pawn on h6 stops it (a and h are neighbours), and a5 stops h6 in turn. -/
example : classify dflt cyl8 ⟨[w 0 5, w 2 4], [k 2 5, k 7 6], none⟩ .black = .notEnded := by decide
/-- A pawn on its last rank counts as passed (§2.3). -/
example : hasPassed dflt flat8 ⟨[w 1 8], [k 1 7], none⟩ .white := by decide

/-- Not passed only because of en passant (§2.4): after a2-a4 in W a2 b3 / B b4 the textbook test calls the
a-pawn passed, the e.p.-aware test does not. -/
example : classify tbook flat8 ⟨[w 0 4, w 1 3], [k 1 4], some (0, 4)⟩ .white = .won .white := by decide
example : classify dflt flat8 ⟨[w 0 4, w 1 3], [k 1 4], some (0, 4)⟩ .white = .notEnded := by decide

/-- Fig. 1(b), W a4 h3 / B a5 h6 on the cylinder: white's only move is h3-h4, and a5xh4 across the seam gives
black a passed pawn. -/
example : moves dflt cyl8 ⟨[w 0 4, w 7 3], [k 0 5, k 7 6], none⟩ .white
    = [⟨[w 0 4, w 7 4], [k 0 5, k 7 6], none⟩] := by decide
example : classify dflt cyl8 ⟨[w 0 4], [k 7 4, k 7 6], none⟩ .black = .won .black := by decide

/-- A race under the count rule: W a6 / B h3 after white's a5-a6, both passed; white needs 2, black 2, the tie
goes to black, who did not move. Under `mover` white wins. -/
example : classify dflt flat8 ⟨[w 0 6], [k 7 3], none⟩ .white = .race .black := by decide
example : classify ⟨.aware, .mover⟩ flat8 ⟨[w 0 6], [k 7 3], none⟩ .white = .race .white := by decide

/-- Components: W a2 h2 / B a3 h3 is one arc across the seam on the cylinder and two on the flat board. -/
example : (components cyl8 ⟨[w 0 2, w 7 2], [k 0 3, k 7 3], none⟩).length = 1 := by decide
example : (components flat8 ⟨[w 0 2, w 7 2], [k 0 3, k 7 3], none⟩).length = 2 := by decide

/-! ## Test positions kept from the referee's read (`notes/L2_referee.md`, section 3; T-numbers as there) -/

/-- T15, T16: cylinders and strips need at least three files; flat boards need none. -/
example : ([1, 2, 3].map fun n => (({ files := n, topology := .cylinder } : Board).valid,
    ({ files := n, topology := .mobius } : Board).valid)) = [(false, false), (false, false), (true, true)]
    ∧ ({ files := 1, topology := .flat } : Board).valid := by decide
/-- T25: a white pawn on rank 1 or a black pawn on the last rank is not a valid position off the strip. -/
example : !Position.valid flat8 ⟨[w 0 1], [k 1 7], none⟩ ∧ !Position.valid flat8 ⟨[w 0 2], [k 1 8], none⟩
    ∧ Position.valid flat8 ⟨[w 0 2], [k 1 7], none⟩ := by decide
/-- T4: on C8, W h2 / B a4: h2-h4 records an e.p. right, and black takes a4xh3 en passant across the seam. -/
example : (moves dflt cyl8 ⟨[w 7 2], [k 0 4], none⟩ .white).contains ⟨[w 7 4], [k 0 4], some (7, 4)⟩
    ∧ (moves dflt cyl8 ⟨[w 7 4], [k 0 4], some (7, 4)⟩ .black).contains ⟨[], [k 7 3], none⟩ := by decide
/-- T5: W a2 / B a3: the double step needs the skipped square empty, so white has no move (and loses). -/
example : moves dflt flat8 ⟨[w 0 2], [k 0 3], none⟩ .white = [] := by decide
/-- T6c: only the opponent of the pawn on the e.p. square can use the right; a move by its owner clears it. -/
example : (moves dflt flat8 ⟨[w 0 4, w 7 2], [k 1 4], some (0, 4)⟩ .white).all (·.ep == none) := by decide
/-- T13 (N5 rule 2 of the header): on the strip, after W a2-a4, the black h7 pawn (moving down) has a3 as a
diagonal capture square across the seam, so the right is recorded and h7 takes en passant, landing on a3
and now moving up. -/
example : (moves dflt mob8 ⟨[w 0 2], [k 7 7], none⟩ .white).contains ⟨[w 0 4], [k 7 7], some (0, 4)⟩
    ∧ (moves dflt mob8 ⟨[w 0 4], [k 7 7], some (0, 4)⟩ .black).contains ⟨[], [⟨0, 3, true⟩], none⟩ := by decide
/-- T14 (N5 rule 1): on the strip a reversed white pawn on d7 moving down double-steps to d5. -/
example : (moves dflt mob8 ⟨[⟨3, 7, false⟩], [⟨5, 2, true⟩], none⟩ .white).contains
    ⟨[⟨3, 5, false⟩], [⟨5, 2, true⟩], none⟩ := by decide
/-- T20 (N5 rule 3): on the strip W a4 is blocked by a black pawn on h4 moving down (seen across the seam on
rank 5, ahead), not by one on h6 (seen on rank 3, behind). -/
example : !hasPassed dflt mob8 ⟨[w 0 4], [k 7 4], none⟩ .white ∧ hasPassed dflt mob8 ⟨[w 0 4], [k 7 6], none⟩ .white := by
  decide
/-- T17 (N5 rule 4): on the strip W a3 (up) and W a6 (down) face each other; both are passed but neither is a
front pawn, so white's race distance is infinite and black (B e6) wins the race after black's move. -/
example : raceDistance dflt mob8 ⟨[w 0 3, ⟨0, 6, false⟩], [k 4 6], none⟩ .white = none
    ∧ classify dflt mob8 ⟨[w 0 3, ⟨0, 6, false⟩], [k 4 6], none⟩ .black = .race .black := by decide

end CylChess.Examples
