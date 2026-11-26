import CylChess.Claims.WideCommon

/-!
# L7b: negative controls

The notes state that the next smaller member of a family (zero repeats of its wall block) is *not* the nimber, with
these outcome classes of `G + *h` (L: White wins whoever starts, R: Black wins whoever starts, N: next player wins,
P: previous player wins). The checks reproduce them, so the searches do not answer `*2` or `*3` to everything.

* N3: "both fail at `n = 9` (LLLL)" for `R_9`, `Qo_9`;
* S14: "`M_8` and `O_9` ... At heap 2 their outcomes are N and R";
* N4: "`T_10` and `S_11` ... At heap 3 their outcomes are L and R".
-/
namespace CylChess.Claims
open Wide

def R9 : List String := ["W5", "B7", "W2", "W3B6", "W3", "W2B5", "B5", "W2", "B4"]
def Qo9 : List String := ["W4", "B7", "W2", "W3B6", "W3", "W2B5", "B5", "W2", "B4"]
def M8 : List String := ["B6", "W2", "W3", "B6", "B7", "W3", "B7", "W5"]
def O9 : List String := ["B4", "B7", "W3", "B7", "B6", "W3", "W2", "B6", "W2"]
def T10 : List String := ["B5", "W2", "W6B7", "W3", "B7", "B6", "W3", "W2", "B6", "W2"]
def S11 : List String := ["B4", "B6", "W3", "W6B7", "W3", "B7", "B6", "W3", "W2", "B6", "W2"]

/-- The class of `G + *h` for `h = 0 .. 4`. -/
def sig (n : Nat) (fs : List String) : String := sigString (defEnv (cylinder n)) wideFuel (ofFiles fs) 4

theorem controls_cylinder :
    sig 9 R9 = "LLLLL" ∧ sig 9 Qo9 = "LLLLL" ∧
    (sig 8 M8).toList[2]? = some 'N' ∧ (sig 9 O9).toList[2]? = some 'R' ∧
    (sig 10 T10).toList[3]? = some 'L' ∧ (sig 11 S11).toList[3]? = some 'R' := by
  native_decide

end CylChess.Claims
