import CylChess.Search
import CylChess.Claims.L4_Star2
import CylChess.Claims.L5_Eighth
/-! L3 referee: hand-worked positions against `Game.isValue` (spec) and `Search.isValue`. Files a = 0. -/
namespace L3
open CylChess CylChess.Claims

def cyl (n : Nat) (R : Nat := 8) : Board := { files := n, ranks := R, topology := .cylinder }
def flat (n : Nat) (R : Nat := 8) : Board := { files := n, ranks := R, topology := .flat }
def P (w b : List Square) : Position := Position.ofSquares w b

open Tree in
def intT : Nat → Tree
  | 0 => zero
  | n + 1 => node [intT n] []
def negInt (n : Nat) : Tree := (intT n).neg
def up : Tree := .node [Tree.zero] [Tree.star 1]
def down : Tree := up.neg
-- {0 | -1}
def sw : Tree := .node [Tree.zero] [negInt 1]
-- tiny-1 = {0 || 0 | -1}
def tiny1 : Tree := .node [Tree.zero] [sw]

/-- the named candidates -/
def cands : List (String × Tree) :=
  [("0", Tree.zero), ("*", Tree.star 1), ("*2", Tree.star 2), ("*3", Tree.star 3), ("1", intT 1),
   ("-1", negInt 1), ("2", intT 2), ("1/2", Tree.dy 1), ("1/4", Tree.dy 2), ("1/8", Tree.eighth),
   ("up", up), ("down", down), ("{0|-1}", sw), ("tiny1", tiny1)]

/-- Which candidates the spec and the search accept, and the raw outcomes of X + 0 (spec, Search). -/
def report (e : Env) (fuel : Nat) (pos : Position) : String :=
  let spec := cands.filter (fun (_, t) => isValue e fuel pos t) |>.map (·.1)
  let fast := cands.filter (fun (_, t) => Search.isValue e fuel pos t) |>.map (·.1)
  let oc := ([Color.white, .black].map fun c => outcome e fuel pos Tree.zero c)
  let os := ([Color.white, .black].map fun c => Search.outcome e fuel pos Tree.zero c)
  s!"spec={spec} search={fast} S-outcome(W,B to move) spec={oc} search={os}"

def D := Settings.default
def st (ep : EpRule) (r : RaceRule) : Settings := ⟨ep, r⟩

-- H1..H3: one-file gap games
#eval ("H1 1f r4 W a2/B a3 (0)", report (env D (flat 1 4)) 400 (P [sqr 'a' 2] [sqr 'a' 3]))
#eval ("H2 1f r5 W a2/B a4 (*)", report (env D (flat 1 5)) 400 (P [sqr 'a' 2] [sqr 'a' 4]))
#eval ("H3 1f r6 W a2/B a5 (*2)", report (env D (flat 1 6)) 400 (P [sqr 'a' 2] [sqr 'a' 5]))
-- H4..H6: integers
#eval ("H4 1f W a2 a4/B a5 (1)", report (env D (flat 1)) 400 (P [sqr 'a' 2, sqr 'a' 4] [sqr 'a' 5]))
#eval ("H5 1f W a4/B a5 a7 (-1)", report (env D (flat 1)) 400 (P [sqr 'a' 4] [sqr 'a' 5, sqr 'a' 7]))
#eval ("H6 1f W a2 a5/B a6 (2)", report (env D (flat 1)) 400 (P [sqr 'a' 2, sqr 'a' 5] [sqr 'a' 6]))
-- H7, H8: sums of two components
#eval ("H7 3f r6 *2 + * (*3)", report (env D (flat 3 6)) 400 (P [sqr 'a' 2, sqr 'c' 2] [sqr 'a' 5, sqr 'c' 4]))
#eval ("H8 3f 1 + -1 (0)", report (env D (flat 3)) 400
  (P [sqr 'a' 2, sqr 'a' 4, sqr 'c' 4] [sqr 'a' 5, sqr 'c' 5, sqr 'c' 7]))
-- H9..H11: up, down, 0 on 7 ranks
#eval ("H9 1f r7 W a2/B a5 (up)", report (env D (flat 1 7)) 400 (P [sqr 'a' 2] [sqr 'a' 5]))
#eval ("H10 1f r7 W a3/B a6 (down)", report (env D (flat 1 7)) 400 (P [sqr 'a' 3] [sqr 'a' 6]))
#eval ("H11 1f r7 W a2/B a6 (0)", report (env D (flat 1 7)) 400 (P [sqr 'a' 2] [sqr 'a' 6]))
-- H12: Fig 1(a) W a2 / B b4 (0, default)
#eval ("H12 2f W a2/B b4 default (0)", report (env D (flat 2)) 400 (P [sqr 'a' 2] [sqr 'b' 4]))
-- H13: W a2 b3 / B b4 under several settings
def p13 := P [sqr 'a' 2, sqr 'b' 3] [sqr 'b' 4]
#eval ("H13 aware/count (0)", report (env D (flat 2)) 400 p13)
#eval ("H13 aware/mover (0)", report (env (st .aware .mover) (flat 2)) 400 p13)
#eval ("H13 aware/opponent (L)", report (env (st .aware .opponent) (flat 2)) 400 p13)
#eval ("H13 textbook/count, BIG=4 (5) spec",
  isValue { s := st .textbook .count, b := flat 2, big := 4 } 400 p13 (intT 5),
  Search.isValue { s := st .textbook .count, b := flat 2, big := 4 } 400 p13 (intT 5),
  isValue { s := st .textbook .count, b := flat 2, big := 4 } 400 p13 (intT 4))
#eval ("H13 textbook/count BIG=256 (257) search", Search.isValue (env (st .textbook .count) (flat 2)) 400 p13 (intT 257),
  Search.isValue (env (st .textbook .count) (flat 2)) 400 p13 (intT 256))
#eval ("H13 textbook/count BIG=256 (257) spec", isValue (env (st .textbook .count) (flat 2)) 600 p13 (intT 257))
#eval ("H13 off/count BIG=4 (5)", isValue { s := st .off .count, b := flat 2, big := 4 } 400 p13 (intT 5))
#eval ("H13 textbook/opponent BIG=4 (5)", isValue { s := st .textbook .opponent, b := flat 2, big := 4 } 400 p13 (intT 5))
-- H14: W a2 / B b4 textbook: count 0, opponent 0, mover L
def p14 := P [sqr 'a' 2] [sqr 'b' 4]
#eval ("H14 textbook/count (0)", report (env (st .textbook .count) (flat 2)) 400 p14)
#eval ("H14 textbook/opponent (0)", report (env (st .textbook .opponent) (flat 2)) 400 p14)
#eval ("H14 textbook/mover (L)", report (env (st .textbook .mover) (flat 2)) 400 p14)
-- H15, H16: Fig 1(b) on C8 and its h2 variant
def p15 := P [sqr 'a' 4, sqr 'h' 3] [sqr 'a' 5, sqr 'h' 6]
#eval ("H15 C8 W a4 h3/B a5 h6 (0 in all nine)",
  allSettings.map fun s => (isValue (env s (cyl 8)) 400 p15 Tree.zero, Search.isValue (env s (cyl 8)) 400 p15 Tree.zero))
#eval ("H16 C8 W a4 h2/B a5 h6 (1)", report (env D (cyl 8)) 400 (P [sqr 'a' 4, sqr 'h' 2] [sqr 'a' 5, sqr 'h' 6]))
-- H17: the same squares on the flat board: a-file locked (0) + h-file gap game {*|*} = 0
#eval ("H17 F8 W a4 h3/B a5 h6", report (env D (flat 8)) 400 p15)
-- Paper-derived (not hand-solved in full): Fig 1(c), posG followers, Fig1(b) a5/h2 variant
#eval ("P1 C8 Fig1(c) (tiny1)", report (env D (cyl 8)) 400
  (P [sqr 'a' 4, sqr 'h' 2, sqr 'h' 4] [sqr 'a' 5, sqr 'a' 6, sqr 'a' 7, sqr 'h' 3]))
#eval ("P2 C8 after a5xh4 ({0|-1})", report (env D (cyl 8)) 400
  (P [sqr 'a' 4, sqr 'h' 2] [sqr 'a' 6, sqr 'a' 7, sqr 'h' 3, sqr 'h' 4]))
#eval ("P3 posG after a2-a4 (0)", report (env D (flat 8)) 400 (P [sqr 'a' 4, sqr 'b' 2, sqr 'b' 3] [sqr 'a' 5, sqr 'a' 6, sqr 'b' 6]))
#eval ("P4 posG after a2-a3 (*)", report (env D (flat 8)) 400 (P [sqr 'a' 3, sqr 'b' 2, sqr 'b' 3] [sqr 'a' 5, sqr 'a' 6, sqr 'b' 6]))
#eval ("P5 posG after b6-b5 (1/4)", report (env D (flat 8)) 400 (P [sqr 'a' 2, sqr 'b' 2, sqr 'b' 3] [sqr 'a' 5, sqr 'a' 6, sqr 'b' 5]))
#eval ("P6 C8 W a5 h2/B a6 h7 default (2)", report (env D (cyl 8)) 400 (P [sqr 'a' 5, sqr 'h' 2] [sqr 'a' 6, sqr 'h' 7]))
-- Up Up * = up + up + * ; test X + down + down + * is P via a tree: X - (UpUp*) = X + downdown*
-- (removed placeholder)
#eval ("P7 same, ep off: outcome only (paper: Up Up *, positive)",
  report (env (st .off .count) (cyl 8)) 400 (P [sqr 'a' 5, sqr 'h' 2] [sqr 'a' 6, sqr 'h' 7]))
-- Fuel: too little fuel must give neither IsValue nor NotValue
#eval ("F1 fuel 2 on *2", isValue (env D (flat 1 6)) 2 (P [sqr 'a' 2] [sqr 'a' 5]) (Tree.star 2),
  notValue (env D (flat 1 6)) 2 (P [sqr 'a' 2] [sqr 'a' 5]) (Tree.star 2),
  notValue (env D (flat 1 6)) 2 (P [sqr 'a' 2] [sqr 'a' 5]) (Tree.star 1),
  notValue (env D (flat 1 6)) 400 (P [sqr 'a' 2] [sqr 'a' 5]) (Tree.star 1),
  notValue (env D (flat 1 6)) 400 (P [sqr 'a' 2] [sqr 'a' 5]) (Tree.star 2))
-- Won root: a lone white pawn (passed) has no value in IsValue's sense
#eval ("W1 lone pawn", cands.map fun (n, t) => (n, isValue (env D (flat 1)) 400 (P [sqr 'a' 2] []) t))
-- Tree sanity
#eval ("T stars", repr (Tree.star 2 |> fun t => match t with | .node l r => (l.length, r.length)))

end L3

namespace L3
open CylChess CylChess.Claims
-- {0,up|0} is NOT the canonical form of Up Up * (my mistake); P7c below uses the sum up+up+* instead
def upupstar : Tree := .node [Tree.zero, up] [Tree.zero]
#eval ("P7b C8 W a5 h2/B a6 h7 ep off = UpUp* ({0,up|0})",
  isValue (env (st .off .count) (cyl 8)) 400 (P [sqr 'a' 5, sqr 'h' 2] [sqr 'a' 6, sqr 'h' 7]) upupstar,
  Search.isValue (env (st .off .count) (cyl 8)) 400 (P [sqr 'a' 5, sqr 'h' 2] [sqr 'a' 6, sqr 'h' 7]) upupstar)
#eval ("H13 textbook/count BIG=256 (257) search fuel 600", Search.isValue (env (st .textbook .count) (flat 2)) 600 p13 (intT 257))
-- e.p. right kept in a sum: flat 5 files r8, component a-b: W a2 / B b4 (Fig 1a); component d-e... use d only: W d2/B d5 r8 gap game
def pep := P [sqr 'a' 2, sqr 'd' 3] [sqr 'b' 4, sqr 'd' 6]
#eval ("E1 sum with e.p. right, spec vs search",
  [D, st .textbook .count, st .off .count].map fun s =>
    ([Color.white, .black].map fun c => (outcome (env s (flat 5)) 400 pep Tree.zero c, Search.outcome (env s (flat 5)) 400 pep Tree.zero c)))
-- Kernel coverage gap check: A with black to move (native here, same as star2seven_default)
#eval ("A black", Search.outcome (env D (flat 8)) 400 CylChess.Claims.posA (Tree.star 2) .black)
end L3

namespace L3
open CylChess CylChess.Claims
/-- disjunctive sum of trees, bounded by depth fuel -/
def tadd : Nat → Tree → Tree → Tree
  | 0, _, _ => Tree.zero
  | n + 1, .node gl gr, .node hl hr =>
    let g := Tree.node gl gr
    let h := Tree.node hl hr
    .node ((gl.map fun x => tadd n x h) ++ (hl.map fun y => tadd n g y))
          ((gr.map fun x => tadd n x h) ++ (hr.map fun y => tadd n g y))
def uus : Tree := tadd 20 up (tadd 20 up (Tree.star 1))
def uu : Tree := tadd 20 up up
def p7 := P [sqr 'a' 5, sqr 'h' 2] [sqr 'a' 6, sqr 'h' 7]
#eval ("P7c ep off: = up+up+* ?, = up+up ?, = up ?, = up* ?",
  Search.isValue (env (st .off .count) (cyl 8)) 400 p7 uus,
  Search.isValue (env (st .off .count) (cyl 8)) 400 p7 uu,
  Search.isValue (env (st .off .count) (cyl 8)) 400 p7 up,
  Search.isValue (env (st .off .count) (cyl 8)) 400 p7 (tadd 20 up (Tree.star 1)))
#eval ("P7d other ep-off rules / textbook, up+up+*",
  [st .off .mover, st .off .opponent].map fun s => Search.isValue (env s (cyl 8)) 400 p7 uus)
-- sanity: tree {0,up|0} equals up+up+* as games? compare via a pawn-free check: H9 (up) + H9 ... not available; check 1f r7 positions
#eval ("sanity: H9 (up) = tadd up 0", Search.isValue (env D (flat 1 7)) 400 (P [sqr 'a' 2] [sqr 'a' 5]) (tadd 20 up Tree.zero))
end L3

namespace L3
open CylChess CylChess.Claims
/-- Whole positions reachable by moves of either side in any order, before any passed pawn; returns
(number explored, positions with >= 2 components and a live e.p. right). -/
def epSplit (s : Settings) (b : Board) (root : Position) : Nat × List Position :=
  let rec go : Nat → List Position → List Position → List Position → Nat × List Position
    | 0, _, seen, acc => (seen.length, acc)
    | _ + 1, [], seen, acc => (seen.length, acc)
    | n + 1, p :: todo, seen, acc =>
      if seen.contains p then go n todo seen acc else
      let kids := [Color.white, .black].flatMap fun c => moves s b p c
      let opens := kids.filter fun q => !hasPassed s b q .white && !hasPassed s b q .black
      let acc := if p.ep.isSome && (components b p).length ≥ 2 then p :: acc else acc
      go n (todo ++ opens) (p :: seen) acc
  go 200000 [root] [] []
#eval ("epSplit A", (epSplit D (flat 8) posA).1, (epSplit D (flat 8) posA).2.length)
#eval ("epSplit B", (epSplit D (flat 8) posB).1, (epSplit D (flat 8) posB).2.length)
#eval ("epSplit A textbook", (epSplit ⟨.textbook, .count⟩ (flat 8) posA).2.length,
       "B textbook", (epSplit ⟨.textbook, .count⟩ (flat 8) posB).2.length)
#eval ("epSplit 1/8", [EpRule.aware, .textbook].map fun ep => (epSplit ⟨ep, .count⟩ (flat 8) (P [sqr 'a' 2, sqr 'b' 2, sqr 'b' 3] [sqr 'a' 5, sqr 'a' 6, sqr 'b' 6])).2.length)
#eval ("splits at all? A, B, 1/8: max components",
  [posA, posB, P [sqr 'a' 2, sqr 'b' 2, sqr 'b' 3] [sqr 'a' 5, sqr 'a' 6, sqr 'b' 6]].map fun r =>
    let (_, _) := epSplit D (flat 8) r
    0)
end L3

namespace L3
open CylChess CylChess.Claims
/-- Variant sum: the chess rule for e.p. in a sum (any move, in any component, ends every other e.p. right). -/
def clearEp : Comp → Comp
  | .pawns p => .pawns { p with ep := none }
  | c => c
def optsChess (e : Env) (c : Color) : List Comp → List (Option (List Comp))
  | [] => []
  | x :: xs =>
    (x.options e c).map (·.map (· ++ xs.map clearEp)) ++ (optsChess e c xs).map (·.map (clearEp x :: ·))
def winsChess (e : Env) : Nat → List Comp → Color → Search.M (Option Bool)
  | 0, _, _ => pure none
  | f + 1, cs, c => do
    let cs := Search.norm cs
    match (← get)[(cs, c)]? with
    | some b => pure (some b)
    | none =>
      let r ← Search.anyM ((optsChess e c cs).map fun o =>
        match o with
        | none => pure none
        | some cs' => do return (← winsChess e f cs' c.other).map (!·))
      if let some b := r then modify (·.insert (cs, c) b)
      pure r
def isValueChess (e : Env) (fuel : Nat) (pos : Position) (v : Tree) : Bool :=
  let cs := Comp.ofPosition e pos ++ [.tree v.neg]
  ((do let a ← winsChess e fuel cs .white
       let b ← winsChess e fuel cs .black
       pure (a == some false && b == some false) : Search.M Bool).run' {})
#eval ("chess-rule e.p. in sums: A, B *2 in default / aware-mover / textbook count+mover",
  [D, ⟨.aware, .mover⟩, ⟨.textbook, .count⟩, ⟨.textbook, .mover⟩].map fun s =>
    (isValueChess (env s (flat 8)) 400 posA (Tree.star 2), isValueChess (env s (flat 8)) 400 posB (Tree.star 2)))
#eval ("sanity: variant on posG 1/8 default", isValueChess (env D (flat 8)) 400 (P [sqr 'a' 2, sqr 'b' 2, sqr 'b' 3] [sqr 'a' 5, sqr 'a' 6, sqr 'b' 6]) Tree.eighth)
#eval ("whole-board W from A, B (both movers)", [posA, posB].map fun p => [Color.white, .black].map fun c => Search.wholeBoard (env D (flat 8)) 400 p c)
end L3

namespace L3
open CylChess CylChess.Claims
def notValueChess (e : Env) (fuel : Nat) (pos : Position) (v : Tree) : Bool :=
  let cs := Comp.ofPosition e pos ++ [.tree v.neg]
  [Color.white, .black].any fun c => (Id.run ((winsChess e fuel cs c).run' {})) == some true
#eval ("chess-rule e.p.: not *2 under opponent aware/textbook (A, B)",
  [(⟨.aware, .opponent⟩ : Settings), ⟨.textbook, .opponent⟩].map fun s =>
    (notValueChess (env s (flat 8)) 400 posA (Tree.star 2), notValueChess (env s (flat 8)) 400 posB (Tree.star 2)))
end L3

namespace L3
open CylChess CylChess.Claims
#eval ("spec extremes of the race tables, textbook and off (all White, all Black)",
  [EpRule.textbook, .off].map fun ep =>
    let s : Settings := ⟨ep, .count⟩
    let keys := raceKeys (env s flat8) posG
    [Color.white, .black].map fun w => isValue (envTable s (keys.map fun k => (k, w))) fuel posG Tree.eighth)
-- a table that leaves every race unassigned: then nothing should be decided unless races are avoidable
#eval ("empty table (every race unknown), aware", isValue (envTable ⟨.aware, .count⟩ []) fuel posG Tree.eighth,
   notValue (envTable ⟨.aware, .count⟩ []) fuel posG Tree.eighth)
end L3

namespace L3
open CylChess CylChess.Claims
#eval ("empty table, spec, textbook and off", [EpRule.textbook, .off].map fun ep =>
   isValue (envTable ⟨ep, .count⟩ []) fuel posG Tree.eighth)
#eval ("empty table on posA (should be undecided): isValue, notValue",
   Search.isValue { s := Settings.default, b := flat8, race := fun _ _ => none } fuel posA (Tree.star 2),
   Search.outcome { s := Settings.default, b := flat8, race := fun _ _ => none } fuel posA (Tree.star 2) .white,
   Search.outcome { s := Settings.default, b := flat8, race := fun _ _ => none } fuel posA (Tree.star 2) .black)
end L3
