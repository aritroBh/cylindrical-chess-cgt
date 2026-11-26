import CylChess.SearchWide

/-!
# Large heaps: a loss at `*k` gives a win at every `*h`, `h > k`

The claims of S13 etc. are "for every heap `h < 256`" (S13) or "for every heap" (N1, H8); the searches check the heaps
`0 .. 6`. For the specification `WH` the rest follows from one move: the player to move lowers the heap `h` to `k`.
-/
namespace CylChess
namespace Wide

theorem anyOpt_true_of_mem {l : List (Option Bool)} (h : some true ∈ l) : anyOpt l = some true := by
  induction l with
  | nil => simp at h
  | cons o os ih =>
    rcases List.mem_cons.mp h with rfl | h'
    · simp [anyOpt]
    · cases o with
      | none => simp [anyOpt, ih h']
      | some b => cases b <;> simp [anyOpt, ih h']

/-- If the opponent loses `pos + *k` (with the answer `some false` of `WH` at fuel `f`), the mover wins `pos + *h` for
every `h > k` (at fuel `f + 1`): he lowers the heap to `k`. -/
theorem WH_heap_win (e : Env) (f : Nat) (pos : Position) (k h : Nat) (c : Color) (hk : k < h)
    (hl : WH e f pos k c.other = some false) : WH e (f + 1) pos h c = some true := by
  unfold WH
  apply anyOpt_true_of_mem
  apply List.mem_append_right
  rw [List.mem_map]
  exact ⟨k, List.mem_range.mpr hk, by simp [hl]⟩

/-- Both movers lose `pos + *k` at fuel `f`: both movers win `pos + *h` for every `h > k` at fuel `f + 1`. -/
theorem WH_all_larger_heaps (e : Env) (f : Nat) (pos : Position) (k : Nat)
    (hl : ∀ c, WH e f pos k c = some false) : ∀ h c, k < h → WH e (f + 1) pos h c = some true :=
  fun h c hk => WH_heap_win e f pos k h c hk (hl c.other)

end Wide
end CylChess
