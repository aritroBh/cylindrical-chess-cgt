import CylChess.Search

/-!
# All heaps at once: which nim heaps `*j` can be added to a position so that the mover loses

For a position `X` (a sum of components, `Game.lean`) let `WL(X)` (`WR(X)`) be the set of heaps `j` such that
the player Left (Right) to move wins `X + *j` in the sum model of `Game.lean`. Splitting the options of a sum plus a
heap into "move in `X`" and "lower the heap to `i`" gives, for every `j`,

* `j ∈ WL(X)`  iff  some Left option `X'` of `X` has `j ∉ WR(X')`, or some `i < j` has `i ∉ WR(X)`;
* `j ∈ WR(X)`  iff  some Right option `X'` has `j ∉ WL(X')`, or some `i < j` has `i ∉ WL(X)`.

Each set is finite or cofinite (induction on the options: the set of "lower the heap" wins is a final segment), so a set
is stored as `NS`: a flag and the bits of its exceptions. The heaps `j` with `X + *j` lost by the mover whoever it is
are the complement of `WL(X) ∪ WR(X)`: `X = *j` in the sense of `IsValue` exactly for those `j` (`X` has value `*j`
iff `X + *j` is a second-player win, §2.2). This gives the whole nimber test with no bound on `j`.

`solve` computes the two sets from the two sets of options, `sets` runs the recursion over the options of `Game.lean`
(`Sum.options`), memoized. The tests are in `HeapsAgrees.lean`: the sets are compared with `Game.wins` (the
specification) for the heaps `0 .. 3` and with `Search.run` (the fast search) for the heaps `0 .. 7`. No `partial`,
no `sorry`.
-/
namespace CylChess
namespace Heaps

/-- A finite or cofinite set of heap sizes: `cof = false`: the set of the set bits; `cof = true`: all sizes except the
set bits. -/
structure NS where
  cof : Bool
  bits : Nat
  deriving BEq, Hashable, Repr

def NS.mem (s : NS) (j : Nat) : Bool := s.bits.testBit j != s.cof

def NS.compl (s : NS) : NS := ⟨!s.cof, s.bits⟩

def NS.empty : NS := ⟨false, 0⟩

def NS.union (a b : NS) : NS :=
  match a.cof, b.cof with
  | false, false => ⟨false, a.bits ||| b.bits⟩
  | true, true => ⟨true, a.bits &&& b.bits⟩
  | false, true => ⟨true, b.bits ^^^ (b.bits &&& a.bits)⟩
  | true, false => ⟨true, a.bits ^^^ (a.bits &&& b.bits)⟩

/-- One more than the highest set bit (`0` if none). -/
def NS.len (s : NS) : Nat := if s.bits == 0 then 0 else s.bits.log2 + 1

/-- The least `j` not in the set, if any, up to `n` (exclusive of nothing beyond). -/
def NS.members (s : NS) (n : Nat) : List Nat := (List.range n).filter s.mem

/-- From the options' contributions `OL`, `OR` (the heaps `j` for which Left, resp. Right, has a winning move *in the
position*), the sets `(WL, WR)` of heaps for which Left, resp. Right, wins moving first:
`WL[j] = OL[j] ∨ ∃ i < j, ¬WR[i]`, `WR[j] = OR[j] ∨ ∃ i < j, ¬WL[i]`. Computed for `j ≤ J = max(len) + 4`, where both
sequences are constant from `max(len) + 1` on; returns `none` if they are not constant at the end. -/
def solve (OL OR : NS) : Option (NS × NS) :=
  let J := max OL.len OR.len + 4
  let st := (List.range (J + 1)).foldl
    (fun (st : Nat × Nat × Option Nat × Option Nat × Bool × Bool × Bool × Bool) j =>
      let (wlb, wrb, ml, mr, lastL, lastR, _, _) := st
      let wl := OL.mem j || (match mr with | some m => decide (m < j) | none => false)
      let wr := OR.mem j || (match ml with | some m => decide (m < j) | none => false)
      (if wl then wlb ||| (1 <<< j) else wlb, if wr then wrb ||| (1 <<< j) else wrb,
       (if !wl && ml.isNone then some j else ml), (if !wr && mr.isNone then some j else mr),
       wl, wr, lastL, lastR))
    (0, 0, none, none, false, false, false, false)
  let (wlb, wrb, _, _, tl, tr, pl, pr) := st
  if tl != pl || tr != pr then none
  else
    let full := (1 <<< (J + 1)) - 1
    some ((if tl then ⟨true, full ^^^ wlb⟩ else ⟨false, wlb⟩), (if tr then ⟨true, full ^^^ wrb⟩ else ⟨false, wrb⟩))

abbrev Memo := Std.HashMap (List Comp) (NS × NS)

/-- `(WL, WR)` of the sum `cs`, memoized; `none` when the fuel runs out, a race is unassigned, or `solve` fails. -/
def sets (e : Env) : Nat → List Comp → StateM Memo (Option (NS × NS))
  | 0, _ => pure none
  | f + 1, cs0 => do
    let cs := Search.norm cs0
    match (← get)[cs]? with
    | some r => pure (some r)
    | none =>
      let mut ol := NS.empty
      let mut or := NS.empty
      for o in Sum.options e .white cs do
        match o with
        | none => return none
        | some cs' =>
          match ← sets e f cs' with
          | none => return none
          | some (_, wr') => ol := ol.union wr'.compl
      for o in Sum.options e .black cs do
        match o with
        | none => return none
        | some cs' =>
          match ← sets e f cs' with
          | none => return none
          | some (wl', _) => or := or.union wl'.compl
      match solve ol or with
      | none => pure none
      | some r =>
        modify (·.insert cs r)
        pure (some r)

/-- The heaps `j` with `X + *j` lost by the mover whoever it is, as a set (`X` is `*j` exactly for those `j`). -/
def lostHeaps (p : NS × NS) : NS := (p.1.union p.2).compl

/-- The sets for the position `pos` of the sum model (`Comp.ofPosition`). -/
def ofPosition (e : Env) (fuel : Nat) (pos : Position) : StateM Memo (Option (NS × NS)) :=
  sets e fuel (Comp.ofPosition e pos)

end Heaps
end CylChess
