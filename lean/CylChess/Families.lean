import CylChess.SearchWide

/-!
# The ring families of the supplement, as lists of files

Each family is written file by file as in the supplement (`W23B4` is white pawns on ranks 2 and 3 and a black
pawn on rank 4; files are listed from file `0`), and turned into a `Position` by `Wide.ofFiles`. The sources are
quoted at each definition (`dist/tog/supp/s13.tex` = S13, `dist/tog/supp/s14.tex` = S14, and the notes
`dist/tog/supp_src/s15_note1.md` ... `s15_note6.md`, here N1 ... N6).

The functions take the width `n` (the number of files) and return the files. A width below the family's least
width, or of the wrong parity, gives the empty list (so it gives no claim).
-/
namespace CylChess
namespace Fam
open Wide

def rep (k : Nat) (xs : List String) : List String := (List.replicate k xs).flatten

/-- S13, `O_n` for odd `n = 2k + 3 ≥ 5` with `n + 3` pawns: `W23B4, B5, W2B5, (W3, B5)^k`. -/
def wallOdd (n : Nat) : List String :=
  if n % 2 == 1 && 5 ≤ n then ["W23B4", "B5", "W2B5"] ++ rep ((n - 3) / 2) ["W3", "B5"] else []

/-- S13, `E_n` for even `n = 2m + 6 ≥ 6` with `n + 3` pawns: `B5, W2B5, W35B6, W2, (B4, W2)^(m+1)`. -/
def wallEven (n : Nat) : List String :=
  if n % 2 == 0 && 6 ≤ n then ["B5", "W2B5", "W35B6", "W2"] ++ rep ((n - 6) / 2 + 1) ["B4", "W2"] else []

/-- S13: the wall ring `G_n` (`O_n` for odd `n`, `E_n` for even `n`), `n ≥ 5`, `n + 3` pawns. -/
def wall (n : Nat) : List String := if n % 2 == 1 then wallOdd n else wallEven n

/-- N1, `P_n` for even `n ≥ 8` with `n + 2` pawns: `W5, B7, W4, W4B7, B6, W3B6, (W2, B4)^((n-6)/2)`. -/
def pEven (n : Nat) : List String :=
  if n % 2 == 0 && 8 ≤ n then ["W5", "B7", "W4", "W4B7", "B6", "W3B6"] ++ rep ((n - 6) / 2) ["W2", "B4"] else []

/-- N3, `R_n` for odd `n ≥ 11` with `n + 2` pawns: `W5, B7, (W2, B4)^((n-9)/2), W2, W3B6, W3, W2B5, B5, W2, B4`.
Star-2 (the paper's "n+2 pawns"). -/
def rOdd (n : Nat) : List String :=
  if n % 2 == 1 && 11 ≤ n then
    ["W5", "B7"] ++ rep ((n - 9) / 2) ["W2", "B4"] ++ ["W2", "W3B6", "W3", "W2B5", "B5", "W2", "B4"]
  else []

/-- N2, `Q_n` for even `n ≥ 8` with `n + 2` pawns: `W4, B7, (B4, W2)^((n-8)/2), W3B6, W3, W2B5, B5, W2, B4`.
Star-3. -/
def qEven (n : Nat) : List String :=
  if n % 2 == 0 && 8 ≤ n then
    ["W4", "B7"] ++ rep ((n - 8) / 2) ["B4", "W2"] ++ ["W3B6", "W3", "W2B5", "B5", "W2", "B4"]
  else []

/-- N3, `Qo_n` for odd `n ≥ 11` with `n + 2` pawns: `R_n` with `W4` for `W5`. Star-3. -/
def qoOdd (n : Nat) : List String :=
  match rOdd n with
  | [] => []
  | _ :: rest => "W4" :: rest

/-- S14, `M_n` for even `n ≥ 10` with `n` pawns:
`(B4 W2)^((n-8)/2) B6 W2 W3 B6 B7 W3 B7 W5`. Star-2. -/
def mEven (n : Nat) : List String :=
  if n % 2 == 0 && 10 ≤ n then rep ((n - 8) / 2) ["B4", "W2"] ++ ["B6", "W2", "W3", "B6", "B7", "W3", "B7", "W5"]
  else []

/-- S14, the odd one-pawn-per-file ring (called `O_n` there; renamed to avoid S13's `O_n`), odd `n ≥ 11`, `n` pawns:
`B4 (B7 W5)^((n-9)/2) B7 W3 B7 B6 W3 W2 B6 W2`. Star-2. -/
def oneOdd (n : Nat) : List String :=
  if n % 2 == 1 && 11 ≤ n then
    ["B4"] ++ rep ((n - 9) / 2) ["B7", "W5"] ++ ["B7", "W3", "B7", "B6", "W3", "W2", "B6", "W2"]
  else []

/-- N4, `T_n` for even `n ≥ 12` with `n + 1` pawns:
`(B4 W2)^((n-10)/2) B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2`. Star-3. -/
def tEven (n : Nat) : List String :=
  if n % 2 == 0 && 12 ≤ n then
    rep ((n - 10) / 2) ["B4", "W2"] ++ ["B5", "W2", "W6B7", "W3", "B7", "B6", "W3", "W2", "B6", "W2"]
  else []

/-- N4, `S_n` for odd `n ≥ 13` with `n + 1` pawns:
`B4 B6 W3 (W2 B4)^((n-11)/2) W6B7 W3 B7 B6 W3 W2 B6 W2`. Star-3. -/
def sOdd (n : Nat) : List String :=
  if n % 2 == 1 && 13 ≤ n then
    ["B4", "B6", "W3"] ++ rep ((n - 11) / 2) ["W2", "B4"] ++ ["W6B7", "W3", "B7", "B6", "W3", "W2", "B6", "W2"]
  else []

/-! ### Möbius strip (N5, N6); `m` is the number of repeats and the width is given by the formula -/

/-- N5, `F1(m) = (B4 W2)^m B6 W2 W3 B6 B7 W3 B7 W5`, `n = 2m + 8`. Star-2 for `m ≥ 1`. -/
def f1 (m : Nat) : List String := rep m ["B4", "W2"] ++ ["B6", "W2", "W3", "B6", "B7", "W3", "B7", "W5"]

/-- N5, `F2(m) = F1(m) B7`, `n = 2m + 9`. Star-2 for `m ≥ 1`. -/
def f2 (m : Nat) : List String := f1 m ++ ["B7"]

/-- N5, `F3(m) = B6 W2 W3 B6 B7 W3 (B7 W5)^m W6B7`, `n = 2m + 7`, `n + 1` pawns. Star-2 for `m ≥ 0`. -/
def f3 (m : Nat) : List String := ["B6", "W2", "W3", "B6", "B7", "W3"] ++ rep m ["B7", "W5"] ++ ["W6B7"]

/-- N6, `TT(m) = B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2 (B4 W2)^m`, `n = 2m + 10`, `n + 1` pawns. Star-3 for `m ≥ 1`. -/
def tt (m : Nat) : List String :=
  ["B5", "W2", "W6B7", "W3", "B7", "B6", "W3", "W2", "B6", "W2"] ++ rep m ["B4", "W2"]

/-- N6, `SS(m) = B6 W3 (W2 B4)^m W6B7 W3 B7 B6 W3 W2 B6 W2 B4`, `n = 2m + 11`, `n + 1` pawns. Star-3 for `m ≥ 0`. -/
def ss (m : Nat) : List String :=
  ["B6", "W3"] ++ rep m ["W2", "B4"] ++ ["W6B7", "W3", "B7", "B6", "W3", "W2", "B6", "W2", "B4"]

end Fam

namespace Wide

/-- The cylinder `C_n`: `n` files, eight ranks. -/
def cylinder (n : Nat) : Board := { files := n, topology := .cylinder }

/-- The Möbius strip with `n` files and eight ranks. -/
def mobius (n : Nat) : Board := { files := n, topology := .mobius }

/-- The default setting (count rule, e.p.-aware passed test), `BIG = 256`, on the board `b`. -/
def defEnv (b : Board) : Env := { s := Settings.default, b := b }

/-- Fuel of the whole-board searches: more than the number of single steps all pawns can make. -/
def wideFuel : Nat := 5000

/-- Outcome class of a pair of answers (White to move, Black to move): `N` the next player wins, `P` the previous
player wins, `L` White wins whoever starts, `R` Black wins whoever starts. -/
def cls : Option Bool × Option Bool → String
  | (some true, some true) => "N"
  | (some false, some false) => "P"
  | (some true, some false) => "L"
  | (some false, some true) => "R"
  | _ => "?"

/-- The classes of `pos + *h` for `h = 0 .. hmax`, as a string such as `"NNPNN"`. -/
def sigString (e : Env) (fuel : Nat) (pos : Position) (hmax : Nat) : String :=
  String.join ((signature e fuel pos hmax).map cls)

end Wide
end CylChess
