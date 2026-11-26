import CylChess.Claims.L5_Eighth

/-!
# L5 again, checked by the kernel (`decide +kernel`) in the default setting
-/
namespace CylChess.Claims

set_option maxRecDepth 200000 in
theorem eighth_default_kernel : IsValue (env Settings.default flat8) fuel posG Tree.eighth := by
  decide +kernel

end CylChess.Claims
