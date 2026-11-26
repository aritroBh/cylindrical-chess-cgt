import CylChess.Claims.Common

/-!
# L4: Theorem `thm:star2seven` (`dist/tog/sections/08_star2.tex`)

> "In the default setting, position A, W a4 b3 d2 d3 / B a7 b7 c5, and position B, W b4 c2 d2 /
> B a6 a7 c6 d5, on files a--d of the ordinary board, have value *2. Neither is *2 with e.p. off or under
> the opponent rule."

Stated with the specification (`Game.lean`, naive recursion, no memo): `IsValue` / `NotValue`.
-/
namespace CylChess.Claims

def posA : Position :=
  Position.ofSquares [sqr 'a' 4, sqr 'b' 3, sqr 'd' 2, sqr 'd' 3] [sqr 'a' 7, sqr 'b' 7, sqr 'c' 5]

def posB : Position :=
  Position.ofSquares [sqr 'b' 4, sqr 'c' 2, sqr 'd' 2] [sqr 'a' 6, sqr 'a' 7, sqr 'c' 6, sqr 'd' 5]

/-- Both positions have no passed pawn and each is a single component (files a-d). -/
theorem star2seven_shape :
    (components flat8 posA).length = 1 ∧ (components flat8 posB).length = 1 := by native_decide

/-- "position A ... and position B ... have value *2" in the default setting. -/
theorem star2seven_default :
    IsValue (env Settings.default flat8) fuel posA (Tree.star 2) ∧
    IsValue (env Settings.default flat8) fuel posB (Tree.star 2) := by native_decide

/-- "Neither is *2 with e.p. off": for each of the three race rules. -/
theorem star2seven_not_ep_off :
    ∀ r ∈ [RaceRule.count, .mover, .opponent],
      NotValue (env ⟨.off, r⟩ flat8) fuel posA (Tree.star 2) ∧
      NotValue (env ⟨.off, r⟩ flat8) fuel posB (Tree.star 2) := by native_decide

/-- "Neither is *2 ... under the opponent rule": for each of the three e.p. options. -/
theorem star2seven_not_opponent :
    ∀ ep ∈ [EpRule.aware, .textbook, .off],
      NotValue (env ⟨ep, .opponent⟩ flat8) fuel posA (Tree.star 2) ∧
      NotValue (env ⟨ep, .opponent⟩ flat8) fuel posB (Tree.star 2) := by native_decide

/-- Table `tab:star2_settings`, for A and B: *2 in the other settings with e.p. on and the count or
mover rule (an extra, not part of the theorem). -/
theorem star2seven_table_extra :
    ∀ s ∈ [(⟨.aware, .mover⟩ : Settings), ⟨.textbook, .count⟩, ⟨.textbook, .mover⟩],
      IsValue (env s flat8) fuel posA (Tree.star 2) ∧ IsValue (env s flat8) fuel posB (Tree.star 2) := by
  native_decide

end CylChess.Claims
