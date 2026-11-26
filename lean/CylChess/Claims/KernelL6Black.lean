import CylChess.Claims.L6_SumCounter

/-!
# L6 again, by the kernel: `W(X)` with Black to move (separate module to keep memory under 4 GB)
-/
namespace CylChess.Claims

set_option maxRecDepth 200000 in
theorem sumcounter_W_black_kernel : W envX fuel posX .black = some true := by decide +kernel

end CylChess.Claims
