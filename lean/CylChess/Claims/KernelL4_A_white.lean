import CylChess.Claims.L4_Star2

/-! L4 by the kernel: position A, white to move in `A + *2` (one module per outcome to keep memory under 4 GB). -/
namespace CylChess.Claims

set_option maxRecDepth 200000 in
theorem star2_A_white_kernel :
    outcome (env Settings.default flat8) fuel posA (Tree.star 2).neg .white = some false := by
  decide +kernel

end CylChess.Claims
