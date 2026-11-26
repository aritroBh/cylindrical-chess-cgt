import CylChess.Claims.KernelL4_A_white
import CylChess.Claims.KernelL4_B_white
import CylChess.Claims.KernelL4_B_black
import CylChess.Claims.KernelL5
import CylChess.Claims.KernelL6
import CylChess.Claims.KernelL6Black

open CylChess CylChess.Claims

#print axioms star2seven_shape
#print axioms star2seven_default
#print axioms star2seven_not_ep_off
#print axioms star2seven_not_opponent
#print axioms star2seven_table_extra
#print axioms star2_A_white_kernel
#print axioms star2_B_white_kernel
#print axioms star2_B_black_kernel
#print axioms eighth_nine_settings
#print axioms eighth_mirror_nine_settings
#print axioms eighth_race_counts
#print axioms eighth_all_assignments
#print axioms eighth_default_kernel
#print axioms sumcounter_shape
#print axioms sumcounter_W
#print axioms sumcounter_S
#print axioms sumcounter_S_spec_big24
#print axioms sumcounter_W_white_kernel
#print axioms sumcounter_W_black_kernel

-- An empty assignment, followed by the number of single-key omissions out
-- of the all-White assignment that still certify the root.
#eval [EpRule.aware, .textbook, .off].map fun ep => Id.run do
  let s : Settings := ⟨ep, .count⟩
  let keys := raceKeys (env s flat8) posG
  let table := keys.map fun k => (k, Color.white)
  let check := fun t => Search.isValue (envTable s t) fuel posG Tree.eighth
  return (ep, keys.length, check [], (table.filter (fun row => check (table.erase row))).length)

-- A terminal input with a White passer already on its last rank.
private def nonnegative : Nat → Tree
  | 0 => Tree.zero
  | n + 1 => .node [nonnegative n] []

#eval Id.run do
  let p := Position.ofSquares [sqr 'a' 8] []
  let e := env Settings.default flat8
  return (hasPassed e.s flat8 p .white, W e fuel p .white, S e fuel p .white,
          notValue e fuel p (nonnegative 256))

-- Same normal-play sum, different bounded-search answers.
#eval Id.run do
  let e := env Settings.default flat8
  let cs : List Comp := [.num 1, .num (-1)]
  return (Game.wins e 1 cs .white, Search.run e 1 cs .white)

-- Separate coverage check: refuse exhausted fuel, inspect every pawn option
-- for each colour, and test membership before doing any minimax evaluation.
private def covers (e : Env) (keys : List (Position × Color)) : Nat → Position → Bool
  | 0, _ => false
  | n+1, p => [Color.white, .black].all fun c => (moves e.s e.b p c).all fun q =>
    match hasPassed e.s e.b q .white, hasPassed e.s e.b q .black with
    | true, true => keys.contains (q,c)
    | false, false => (components e.b q).all (covers e keys n)
    | _, _ => true

#eval [EpRule.aware, .textbook, .off].map fun ep => Id.run do
  let e := env ⟨ep, .count⟩ flat8
  let keys := raceKeys e posG
  return (ep, covers e keys 40 posG, covers e [] 40 posG)
