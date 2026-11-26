import CylChess.Claims.WideCommon

/-!
# L7b: Möbius strip rings (N5, N6), whole-board game

> "One pawn per file is enough on eight files, not on nine, and on every strip of ten or more files, by the cylinder's
> insertion proof away from the seam \lab{S} (Section S15). Nine pawns give a `*3` on five and on six files \lab{C2},
> and `n+1` pawns on every strip of `n ≥ 11` files \lab{S}." (`08_star2.tex`, "Möbius strip")

Model (N5, section 1): the strip with eight ranks, `Topology.mobius` of `Rules.lean`; race rule `count`, e.p. on and
e.p.-aware passed test; whole-board game with a nim heap. The families (N5): `F1(m)` (`n = 2m+8` files, `n` pawns),
`F2(m)` (`n = 2m+9`, `n` pawns), `F3(m)` (`n = 2m+7`, `n+1` pawns), each `*2` for `m ≥ 1` (`F3`: `m ≥ 0`); (N6) `TT(m)`
(`n = 2m+10`, `n+1` pawns), `*3` for `m ≥ 1`, and `SS(m)` (`n = 2m+11`, `n+1` pawns), `*3` for `m ≥ 0`.
The theorems check the finite instances up to the `m` stated. The three controls are the cases the notes say fail:
`F1(0)` is `RNRRR`, `F2(0)` is `NNRRR`, `TT(0)` is `LLLLL` (outcome classes of `G + *h`, `h = 0..4`).
-/
namespace CylChess.Claims
open Wide

/-- The family member for `m` repeats on its strip: right width, right pawn count, `G + *h` lost by the mover exactly
for `h = k` (`h ≤ hmaxW`). -/
def checkMob (fam : Nat → List String) (k : Nat) (width size : Nat → Nat) (m : Nat) : Bool :=
  let fs := fam m
  fs.length == width m && (ofFiles fs).size == size m &&
    starTest (defEnv (mobius fs.length)) wideFuel (ofFiles fs) k hmaxW

def sigMob (fam : Nat → List String) (m : Nat) : String :=
  sigString (defEnv (mobius (fam m).length)) wideFuel (ofFiles (fam m)) 4

theorem F1_star2 : (allWidths 1 20).all (checkMob Fam.f1 2 (2 * · + 8) (2 * · + 8)) = true := by native_decide

theorem F2_star2 : (allWidths 1 20).all (checkMob Fam.f2 2 (2 * · + 9) (2 * · + 9)) = true := by native_decide

theorem F3_star2 : (allWidths 0 20).all (checkMob Fam.f3 2 (2 * · + 7) (2 * · + 8)) = true := by native_decide

theorem TT_star3 : (allWidths 1 14).all (checkMob Fam.tt 3 (2 * · + 10) (2 * · + 11)) = true := by native_decide

/-- The controls: the smallest members are not `*2`, `*3` (the notes' signatures). -/
theorem Mobius_controls :
    sigMob Fam.f1 0 = "RNRRR" ∧ sigMob Fam.f2 0 = "NNRRR" ∧ sigMob Fam.tt 0 = "LLLLL" := by native_decide

end CylChess.Claims
