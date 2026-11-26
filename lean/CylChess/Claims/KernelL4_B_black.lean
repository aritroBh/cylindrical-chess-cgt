import CylChess.Claims.L4_Star2

/-! L4 by the kernel: position B, black to move in `B + *2` (one module per outcome to keep memory under 4 GB). -/
namespace CylChess.Claims

set_option maxRecDepth 200000 in
theorem star2_B_black_kernel :
    outcome (env Settings.default flat8) fuel posB (Tree.star 2).neg .black = some false := by
  decide +kernel

end CylChess.Claims
