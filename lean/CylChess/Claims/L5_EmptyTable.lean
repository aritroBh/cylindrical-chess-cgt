import CylChess.Claims.L5_Eighth

/-!
# L5, empty race table: `1/8` for every race assignment (`dist/tog/sections/07_targets.tex`, `thm:eighth`)

Model: the sum model of `Game.lean` (a position is a sum of components; a race is decided by the environment's
function `Env.race`).

`L5_Eighth.lean` checks the position `posG` for every complete table of race outcomes, but with the *fast search*
(`Search.isValue`). This file states the same thing on the *specification* `Game.isValue`, by two steps.

1. (`eighth_empty_table_*`, computed) With `race := fun _ _ => none`, that is, with *no* race outcome known,
   `Game.isValue` still returns `true` for `posG` and `1/8`, for each of the three e.p. options (and, since the
   race rule is not used once `race` is replaced, for each of the nine settings).
2. (`isValue_mono`, `eighth_every_race_function`, proved in Lean) A definite answer of `Game.wins` (`some b`) only
   uses moves whose verdict is defined: a move to an undefined race makes its option `none`, and `anyOpt` returns
   `some b` only from options that are `some` (a `some true` option, or all options `some false`). So if a race
   function `r1` answers `none` wherever it differs from `r2`, every `some b` answer under `r1` is the same
   `some b` under `r2` (`wins_mono`, by induction on the fuel, with `anyOpt_mono` for the option lists). With
   `r1` = the empty table this gives the value `1/8` for **every** race function `r2`, total or partial,
   in particular for every one of the `2^k` assignments, without the breadth-first walk `raceKeys`.

The proof of step 2 is not an argument in words: it is in this file (about 120 lines, no `sorry`).
-/
namespace CylChess.Claims

/-- `a` is no more defined than `b`. -/
def Le {α : Type} (a b : Option α) : Prop := a = none ∨ a = b

/-- Pointwise relation between two lists. -/
inductive Pw {α : Type} (R : α → α → Prop) : List α → List α → Prop
  | nil : Pw R [] []
  | cons {a b : α} {l m : List α} : R a b → Pw R l m → Pw R (a :: l) (b :: m)

theorem le_refl' {α : Type} (a : Option α) : Le a a := Or.inr rfl

theorem forall₂_map {α β : Type} (f g : α → β) (R : β → β → Prop) :
    ∀ l : List α, (∀ a, R (f a) (g a)) → Pw R (l.map f) (l.map g)
  | [], _ => Pw.nil
  | _ :: l, h => Pw.cons (h _) (forall₂_map f g R l h)

theorem forall₂_refl {α : Type} (R : α → α → Prop) (hr : ∀ a, R a a) :
    ∀ l : List α, Pw R l l
  | [] => Pw.nil
  | _ :: l => Pw.cons (hr _) (forall₂_refl R hr l)

theorem forall₂_append {α : Type} {R : α → α → Prop} :
    ∀ {l1 l2 m1 m2 : List α}, Pw R l1 l2 → Pw R m1 m2 → Pw R (l1 ++ m1) (l2 ++ m2)
  | _, _, _, _, Pw.nil, h => h
  | _, _, _, _, Pw.cons a h1, h => Pw.cons a (forall₂_append h1 h)

theorem forall₂_map_rel {α β : Type} {R : α → α → Prop} {Q : β → β → Prop} (f : α → β)
    (hf : ∀ a b, R a b → Q (f a) (f b)) :
    ∀ {l1 l2 : List α}, Pw R l1 l2 → Pw Q (l1.map f) (l2.map f)
  | _, _, Pw.nil => Pw.nil
  | _, _, Pw.cons a h => Pw.cons (hf _ _ a) (forall₂_map_rel f hf h)

theorem forall₂_map_rel' {α β : Type} {R : α → α → Prop} {Q : β → β → Prop} (f g : α → β)
    {l1 l2 : List α} (h : Pw R l1 l2) (hf : ∀ a b, R a b → Q (f a) (g b)) :
    Pw Q (l1.map f) (l2.map g) := by
  induction h with
  | nil => exact Pw.nil
  | cons a _ ih => exact Pw.cons (hf _ _ a) ih

theorem anyOpt_mono :
    ∀ {L1 L2 : List (Option Bool)}, Pw Le L1 L2 → ∀ b : Bool, anyOpt L1 = some b → anyOpt L2 = some b
  | _, _, Pw.nil, _, h => h
  | _, _, @Pw.cons _ _ o1 o2 os1 os2 hr hs, b, h => by
    have ih := anyOpt_mono hs
    cases o1 with
    | none =>
      simp only [anyOpt] at h
      split at h
      · rename_i hh
        have h2 := ih _ hh
        cases h
        cases o2 with
        | none => simp only [anyOpt, h2]
        | some x => cases x <;> simp only [anyOpt, h2]
      · cases h
    | some x =>
      have : o2 = some x := by rcases hr with h | h <;> simp_all
      subst this
      cases x
      · simp only [anyOpt] at h ⊢; exact ih _ h
      · simp only [anyOpt] at h ⊢; exact h


/-- The environment `e` with the race function `r`. -/
def withRace (e : Env) (r : Position → Color → Option Color) : Env := { e with race := r }

theorem comp_options_le (e : Env) (r1 r2 : Position → Color → Option Color)
    (hr : ∀ p m, Le (r1 p m) (r2 p m)) (c : Color) :
    ∀ x : Comp, Pw Le (x.options (withRace e r1) c) (x.options (withRace e r2) c) := by
  intro x
  cases x with
  | num n => exact forall₂_refl _ le_refl' _
  | tree t => cases t; exact forall₂_refl _ le_refl' _
  | pawns pos =>
    simp only [Comp.options]
    apply forall₂_map
    intro q
    simp only [Env.verdict, withRace]
    cases hasPassed e.s e.b q .white <;> cases hasPassed e.s e.b q .black <;> simp only [Le]
    · simp
    · simp
    · simp
    · rcases hr q c with h | h
      · rw [h]; simp
      · rw [h]; exact Or.inr rfl

theorem sum_options_le (e : Env) (r1 r2 : Position → Color → Option Color)
    (hr : ∀ p m, Le (r1 p m) (r2 p m)) (c : Color) :
    ∀ cs : List Comp, Pw Le (Sum.options (withRace e r1) c cs) (Sum.options (withRace e r2) c cs)
  | [] => Pw.nil
  | x :: xs => by
    simp only [Sum.options]
    have hmap : ∀ g : List Comp → List Comp, ∀ a b : Option (List Comp), Le a b → Le (a.map g) (b.map g) := by
      intro g a b h
      rcases h with h | h <;> subst h <;> simp [Le]
    exact forall₂_append (forall₂_map_rel _ (fun a b h => hmap _ a b h) (comp_options_le e r1 r2 hr c x))
      (forall₂_map_rel _ (fun a b h => hmap _ a b h) (sum_options_le e r1 r2 hr c xs))

theorem wins_mono (e : Env) (r1 r2 : Position → Color → Option Color)
    (hr : ∀ p m, Le (r1 p m) (r2 p m)) :
    ∀ (f : Nat) (cs : List Comp) (c : Color) (b : Bool),
      Game.wins (withRace e r1) f cs c = some b → Game.wins (withRace e r2) f cs c = some b := by
  intro f
  induction f with
  | zero => intro cs c b h; simp [Game.wins] at h
  | succ f ih =>
    intro cs c b h
    simp only [Game.wins] at h ⊢
    refine anyOpt_mono ?_ b h
    refine forall₂_map_rel' _ _ (sum_options_le e r1 r2 hr c cs) ?_
    intro o1 o2 ho
    rcases ho with ho | ho
    · subst ho; exact Or.inl rfl
    · subst ho
      cases o1 with
      | none => exact Or.inl rfl
      | some cs' =>
        simp only []
        cases h1 : Game.wins (withRace e r1) f cs' c.other with
        | none => exact Or.inl rfl
        | some b' => rw [ih _ _ _ h1]; exact Or.inr rfl


/-- A setting's environment on the flat board with no race outcome known. -/
def envEmpty (s : Settings) : Env := withRace (env s flat8) fun _ _ => none

/-- Step 1, nine settings, specification, compiled code: `posG` has value `1/8` when every race is unknown. -/
theorem eighth_empty_table_nine_settings :
    ∀ s ∈ allSettings, IsValue (envEmpty s) fuel posG Tree.eighth := by native_decide

/-- The same for the default setting, in the kernel (no compiled code; 2.9 GB, about 9 s). The other two e.p.
options in the kernel together with this one need 3.5 GB in one module, so they are left to `native_decide`. -/
theorem eighth_empty_table_default_kernel :
    IsValue (envEmpty Settings.default) fuel posG Tree.eighth := by decide +kernel

/-- Monotonicity of `isValue` in the race function. -/
theorem isValue_mono (e : Env) (r1 r2 : Position → Color → Option Color)
    (hr : ∀ p m, Le (r1 p m) (r2 p m)) (fuel : Nat) (pos : Position) (v : Tree)
    (h : isValue (withRace e r1) fuel pos v = true) : isValue (withRace e r2) fuel pos v = true := by
  simp only [isValue, outcome, Bool.and_eq_true, beq_iff_eq, Bool.not_eq_true'] at h ⊢
  obtain ⟨⟨⟨h1, h2⟩, h3⟩, h4⟩ := h
  exact ⟨⟨⟨h1, h2⟩, wins_mono e r1 r2 hr _ _ _ _ h3⟩, wins_mono e r1 r2 hr _ _ _ _ h4⟩

/-- Step 2: `posG` has value `1/8` in all nine settings for every race function whatever (every assignment of
outcomes to race positions, complete or not), on the specification. -/
theorem eighth_every_race_function :
    ∀ s ∈ allSettings, ∀ r : Position → Color → Option Color,
      IsValue (withRace (env s flat8) r) fuel posG Tree.eighth := fun s hs r =>
  isValue_mono (env s flat8) (fun _ _ => none) r (fun _ _ => Or.inl rfl) fuel posG Tree.eighth
    (eighth_empty_table_nine_settings s hs)

#print axioms eighth_empty_table_default_kernel
#print axioms eighth_every_race_function

end CylChess.Claims
