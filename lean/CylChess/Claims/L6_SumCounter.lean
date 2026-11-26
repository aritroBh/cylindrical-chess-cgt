import CylChess.Claims.Common
import CylChess.Search

/-!
# L6: Proposition `prop:sumcounter` (`dist/tog/sections/05_sums.tex`)

> "on C_8 with en passant off and the count rule, X = W b2 d4 g3 h5 / B a7 c7 f7 g4 is a single component,
> spanning files f to d across the seam, so such a test passes it; yet S(X) is a black win whoever starts and
> W(X) a first-player win."

(The further sentence "X is not HSS" is not formalised.) `S` and `W` are `Game.S` and `Game.W`.
-/
namespace CylChess.Claims

def posX : Position :=
  Position.ofSquares [sqr 'b' 2, sqr 'd' 4, sqr 'g' 3, sqr 'h' 5] [sqr 'a' 7, sqr 'c' 7, sqr 'f' 7, sqr 'g' 4]

def envX : Env := env ⟨.off, .count⟩ cyl8

/-- X has no passed pawn and is a single component. -/
theorem sumcounter_shape :
    (components cyl8 posX).length = 1 ∧ hasPassed envX.s cyl8 posX .white = false ∧
    hasPassed envX.s cyl8 posX .black = false := by native_decide

/-- "W(X) a first-player win": the player to move wins, whoever it is (specification). -/
theorem sumcounter_W :
    W envX fuel posX .white = some true ∧ W envX fuel posX .black = some true := by native_decide

/-- "S(X) is a black win whoever starts": White to move loses, Black to move wins (fast search). -/
theorem sumcounter_S :
    Search.S envX fuel posX .white = some false ∧ Search.S envX fuel posX .black = some true := by
  native_decide

set_option maxHeartbeats 4000000 in
/-- The same two outcomes of `S(X)` with the *specification* (naive recursion), with `BIG = 24` instead of 256
(with 256 the naive recursion is too slow). 24 exceeds the number of moves either side can make from `X`
(at most 18 for White and 21 for Black), which is all that `BIG` has to satisfy (§2.3). -/
theorem sumcounter_S_spec_big24 :
    S { envX with big := 24 } 100 posX .white = some false ∧
    S { envX with big := 24 } 100 posX .black = some true := by native_decide

end CylChess.Claims
