import CylChess.Dawson

/-!
# L8: the period of the Grundy values of Dawson's chess up to `n = 300`

> "The values have period 34 with last exception `n = 51`, which two programs reproduce for `n ≤ 300`"
> (`dist/tog/sections/11_dawson.tex`)

`g` is the recurrence of the paper's equation `eq:dawson` (`Dawson.lean`). Checked here: `g (n + 34) = g n` for every
`n` from 52 to 266 (so every value up to `g 300` is covered), and `g 85 ≠ g 51`. Compiled code (`native_decide`).
That the period continues beyond 300 is the theorem of Guy and Smith, not checked here.
-/
namespace CylChess.Dawson

theorem g_period_to_300 : ∀ n ∈ List.range' 52 215, g (n + 34) = g n := by native_decide

theorem g_last_exception : g (51 + 34) ≠ g 51 := by native_decide

end CylChess.Dawson
