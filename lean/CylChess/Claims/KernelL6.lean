import CylChess.Claims.L6_SumCounter

/-!
# L6 again, checked by the kernel (`decide +kernel`) instead of compiled code

Only the part that the specification can run in reasonable time and memory: `W(X)`, White to move (Black
to move is `KernelL6Black.lean`, a separate module to keep memory per process under 4 GB). `S(X)` with the
naive recursion is too slow; it is checked with `Search` in `L6_SumCounter.lean`.
-/
namespace CylChess.Claims

set_option maxRecDepth 200000 in
theorem sumcounter_W_white_kernel : W envX fuel posX .white = some true := by decide +kernel

end CylChess.Claims
