import CylChess.Rules
/-! L2 referee: edge-case positions against `CylChess.Rules`. Files a = 0 ... h = 7. -/
namespace L2
open CylChess

def w (f r : Nat) : Pawn := ⟨f, r, true⟩
def k (f r : Nat) : Pawn := ⟨f, r, false⟩
def cyl (n : Nat) (R : Nat := 8) : Board := { files := n, ranks := R, topology := .cylinder }
def flat (n : Nat) (R : Nat := 8) : Board := { files := n, ranks := R, topology := .flat }
def mob (n : Nat) (R : Nat := 8) : Board := { files := n, ranks := R, topology := .mobius }
def D := Settings.default
def TB : Settings := ⟨.textbook, .count⟩
def OFF : Settings := ⟨.off, .count⟩

-- T1 seam captures on C8, both colours
#eval ("T1w", moves D (cyl 8) ⟨[w 7 4], [k 0 5], none⟩ .white)
#eval ("T1b", moves D (cyl 8) ⟨[w 7 4], [k 0 5], none⟩ .black)
-- T2 two-file cylinder: W a4 / B b5; one capture (both sides land on b5), plus a5
#eval ("T2", moves D (cyl 2) ⟨[w 0 4], [k 1 5], none⟩ .white)
#eval ("T2pass", hasPassed D (cyl 2) ⟨[w 0 4], [k 1 3], none⟩ .white, hasPassed D (cyl 2) ⟨[w 0 4], [k 1 6], none⟩ .white)
-- T3 three-file cylinder seam captures: a4xc5 and c4xa5
#eval ("T3a", moves D (cyl 3) ⟨[w 0 4], [k 2 5], none⟩ .white)
#eval ("T3c", moves D (cyl 3) ⟨[w 2 4], [k 0 5], none⟩ .white)
-- T4 e.p. across the seam on C8: W h2 / B a4. h2-h4 records ep; black a4xh3 e.p.
#eval ("T4mv", moves D (cyl 8) ⟨[w 7 2], [k 0 4], none⟩ .white)
#eval ("T4ep", moves D (cyl 8) ⟨[w 7 4], [k 0 4], some (7, 4)⟩ .black)
#eval ("T4cls", classify D (cyl 8) ⟨[w 7 4], [k 0 4], some (7, 4)⟩ .white,
                 classify TB (cyl 8) ⟨[w 7 4], [k 0 4], some (7, 4)⟩ .white,
                 classify D (flat 8) ⟨[w 7 4], [k 0 4], none⟩ .white)
-- T5 double step blocked on the skipped square / on the target square
#eval ("T5skip", moves D (flat 8) ⟨[w 0 2], [k 0 3], none⟩ .white)
#eval ("T5targ", moves D (flat 8) ⟨[w 0 2], [k 0 4], none⟩ .white)
-- T6 e.p. right expires: black plays g7-g6 instead; then no e.p. on the next black move
#eval ("T6a", moves D (flat 8) ⟨[w 0 4, w 7 2], [k 1 4, k 6 7], some (0, 4)⟩ .black)
#eval ("T6b", moves D (flat 8) ⟨[w 0 4, w 7 2], [k 1 4, k 6 6], none⟩ .black)
-- T6c: right on a white pawn; white moves twice in the component (sum play): white cannot use it, right clears
#eval ("T6c", moves D (flat 8) ⟨[w 0 4, w 7 2], [k 1 4], some (0, 4)⟩ .white)
-- T7 adjacent same-rank enemy is not "ahead": W a5 / B b5 after white's a4-a5 is a race; W 3 B 4 -> white
#eval ("T7", classify D (flat 8) ⟨[w 0 5], [k 1 5], none⟩ .white)
-- T7b ep-aware vs textbook on the cylinder seam already in T4; e.p. off: the a2-a4 pawn is passed (cls won white)
#eval ("T7b", moves OFF (flat 8) ⟨[w 0 2], [k 1 4], none⟩ .white,
              classify OFF (flat 8) ⟨[w 0 4], [k 1 4], none⟩ .white)
-- T8 races under the three rules: W a6 / B h3 (2 v 2), after white or black moved
#eval ("T8", classify D (flat 8) ⟨[w 0 6], [k 7 3], none⟩ .white, classify D (flat 8) ⟨[w 0 6], [k 7 3], none⟩ .black,
       classify ⟨.aware, .mover⟩ (flat 8) ⟨[w 0 6], [k 7 3], none⟩ .black,
       classify ⟨.aware, .opponent⟩ (flat 8) ⟨[w 0 6], [k 7 3], none⟩ .black)
-- T9 race with a home-rank double step counted as one: W a2 (5) / B h4 (3) -> black whoever moved
#eval ("T9", classify D (flat 8) ⟨[w 0 2], [k 7 4], none⟩ .white, classify D (flat 8) ⟨[w 0 2], [k 7 4], none⟩ .black,
       (flat 8).distance (w 0 2), (flat 8).distance (k 7 7), (flat 8).distance (k 7 4))
-- T10 doubled pawns: W a3 a4 / B h3: white front a4 needs 4, black 2
#eval ("T10", raceDistance D (flat 8) ⟨[w 0 3, w 0 4], [k 7 3], none⟩ .white)
-- T11 other heights: 5, 6, 7 ranks; black home = R-1
#eval ("T11h", (flat 3 5).homeRank false, (flat 3 6).homeRank false, (flat 3 7).homeRank false)
#eval ("T11r5", moves D (flat 3 5) ⟨[w 0 2], [k 1 4], none⟩ .black)
#eval ("T11r6", moves D (flat 3 6) ⟨[w 0 3], [k 1 5], none⟩ .black)
#eval ("T11r6ep", moves D (flat 3 6) ⟨[w 0 3], [k 1 3], some (1, 3)⟩ .white)
#eval ("T11r7", moves D (flat 3 7) ⟨[w 0 2], [k 1 6], none⟩ .black,
       (flat 3 7).distance (k 1 6), (flat 3 5).distance (k 1 4), (flat 3 5).distance (w 0 2))
-- T12 Möbius: black a5 takes across the seam onto h, mirrored rank, reversed
#eval ("T12", moves D (mob 8) ⟨[w 7 5], [k 0 5], none⟩ .black)
#eval ("T12dist", (mob 8).distance ⟨7, 5, true⟩)
-- T13 Möbius e.p. across the seam: W a2-a4; black h7 (down) has (a,3) as a diagonal capture square
#eval ("T13mv", moves D (mob 8) ⟨[w 0 2], [k 7 7], none⟩ .white)
#eval ("T13ep", moves D (mob 8) ⟨[w 0 4], [k 7 7], some (0, 4)⟩ .black)
#eval ("T13cls", classify D (mob 8) ⟨[w 0 4], [k 7 7], some (0, 4)⟩ .white,
       classify TB (mob 8) ⟨[w 0 4], [k 7 7], some (0, 4)⟩ .white)
-- T14 Möbius: reversed white pawn on rank 7 double-steps down; reversed black pawn on rank 2 double-steps up
#eval ("T14", moves D (mob 8) ⟨[⟨3, 7, false⟩], [⟨5, 2, true⟩], none⟩ .white,
              moves D (mob 8) ⟨[⟨3, 7, false⟩], [⟨5, 2, true⟩], none⟩ .black)
-- T15 Möbius on 2 files: a4 sees b both straight (b5) and mirrored (b4)
#eval ("T15", moves D (mob 2) ⟨[w 0 4], [k 1 4], none⟩ .white, moves D (mob 2) ⟨[w 0 4], [k 1 5], none⟩ .white)
-- T16 one-file cylinder: a "capture" straight ahead
#eval ("T16", moves D (cyl 1) ⟨[w 0 4], [k 0 5], none⟩ .white)
-- T17 Möbius: two passed white pawns facing each other on one file are neither "front"; race distance infinite
#eval ("T17", hasPassed D (mob 8) ⟨[w 0 3, ⟨0, 6, false⟩], [k 4 6], none⟩ .white,
              raceDistance D (mob 8) ⟨[w 0 3, ⟨0, 6, false⟩], [k 4 6], none⟩ .white,
              classify D (mob 8) ⟨[w 0 3, ⟨0, 6, false⟩], [k 4 6], none⟩ .black)
-- T18 flat edge vs cylinder: W a4 / B h5
#eval ("T18", hasPassed D (flat 8) ⟨[w 0 4], [k 7 5], none⟩ .white, hasPassed D (cyl 8) ⟨[w 0 4], [k 7 5], none⟩ .white)
-- T19 last rank: W a8 / B b2 is a race; white 0, black 1
#eval ("T19", classify D (flat 8) ⟨[w 0 8], [k 1 2], none⟩ .white, classify D (flat 8) ⟨[w 0 8], [k 1 2], none⟩ .black)
-- T20 Möbius seam blocking: W a4; black on h moving down at h4 is seen at rank 5 = ahead -> not passed;
--     black at h6 seen at 3 = behind -> passed
#eval ("T20", hasPassed D (mob 8) ⟨[w 0 4], [k 7 4], none⟩ .white, hasPassed D (mob 8) ⟨[w 0 4], [k 7 6], none⟩ .white)
-- T21 components: cylinder arc across the seam, Möbius likewise, ring
#eval ("T21", (components (cyl 8) ⟨[w 0 2, w 7 2, w 3 2], [k 1 3], none⟩).length,
              (components (mob 8) ⟨[w 0 2, w 7 2, w 3 2], [k 1 3], none⟩).length,
              (components (flat 8) ⟨[w 0 2, w 7 2, w 3 2], [k 1 3], none⟩).length,
              (components (cyl 3) ⟨[w 0 2, w 1 2, w 2 2], [], none⟩).length)
-- T22 normalize drops a fake e.p. right (pawn not two steps from home) and keeps a real one
#eval ("T22", (Position.normalize D (flat 8) ⟨[w 0 5], [k 1 5], some (0, 5)⟩).ep,
              (Position.normalize D (flat 8) ⟨[w 0 4], [k 1 4], some (0, 4)⟩).ep,
              (Position.normalize OFF (flat 8) ⟨[w 0 4], [k 1 4], some (0, 4)⟩).ep)
-- T23 the paper's own example W a2 b3 / B b4: black has no move; every white move lets black reach a passed pawn
#eval ("T23", moves D (flat 8) ⟨[w 0 2, w 1 3], [k 1 4], none⟩ .black,
              moves D (flat 8) ⟨[w 0 2, w 1 3], [k 1 4], none⟩ .white)
-- T24 Fig 1(b) value-2 claim W a5 h2 / B a6 h7 on C8: h7-h5 is met by a5xh6 e.p. across the seam
#eval ("T24", moves D (cyl 8) ⟨[w 0 5, w 7 2], [k 0 6, k 7 7], none⟩ .black)
#eval ("T24ep", moves D (cyl 8) ⟨[w 0 5, w 7 2], [k 0 6, k 7 5], some (7, 5)⟩ .white)
-- T25 rank-1 white pawn is "valid" and can step to rank 2 then double step (impossible in chess)
#eval ("T25", Position.valid (flat 8) ⟨[w 0 1], [k 1 8], none⟩)
-- T26 Möbius race where the reversed passed pawn and a normal passed pawn race: W h5 reversed up? black reversed
#eval ("T26", classify D (mob 8) ⟨[w 2 6], [⟨7, 5, true⟩], none⟩ .black)
end L2
