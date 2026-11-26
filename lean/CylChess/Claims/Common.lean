import CylChess.Game

/-! Boards and settings shared by the claim files. -/
namespace CylChess.Claims

/-- The ordinary 8x8 board. -/
def flat8 : Board := { files := 8, topology := .flat }

/-- The cylinder C_8. -/
def cyl8 : Board := { files := 8, topology := .cylinder }

/-- The environment of a setting on a board: `big = BIG = 256`, races decided by the setting's rule. -/
def env (s : Settings) (b : Board) : Env := { s := s, b := b }

/-- The nine settings of §2.4. -/
def allSettings : List Settings :=
  [EpRule.aware, .textbook, .off].flatMap fun ep => [RaceRule.count, .mover, .opponent].map fun r => ⟨ep, r⟩

/-- Fuel for every claim. An answer `some b` of `Game.wins` or of a search is the outcome whatever the fuel is;
with too little fuel the answer is `none` and the claim does not compile. -/
def fuel : Nat := 400

end CylChess.Claims
