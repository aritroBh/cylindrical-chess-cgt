import CylChess.Claims.L6_SumCounter

/-!
# L6: "X is not HSS" (`prop:sumcounter`, `dist/tog/sections/05_sums.tex`, `def:hss`)

Model: the sum model of `Game.lean`.

> "Positions are reachable by moves of either side in any order. A component carries a threat for a side if play
> on its own files can reach a position, with no passed pawn earlier, that gives that side a passed pawn (a race
> gives both sides one). A position X is hereditarily sum-safe (HSS) if no position reachable from X before the
> first passed pawn, X included, has two components with opposite threats."

> "Moreover X is not HSS: components with opposite threats appear later in its tree."

**What is proved.** Not the general definition but one witness, which is all that "X is not HSS" needs: a position
`x2` reachable from `posX` (cylinder `C_8`, e.p. off, count rule) by two moves with no passed pawn at any point
(the root `posX`, `x1`, and `x2` itself), which has exactly two components, `bd` (files b to d) and `fh` (files f to
h), such that

* in `bd` the line d4-d5, c7-c5 is legal, no position before its last one has a passed pawn, and the last gives White
  a passed pawn (and Black none): `bd` carries a threat for White;
* in `fh` the line f7-f5, f5-f4, f4-f3 is legal, no position before its last one has a passed pawn, and the last
  gives Black a passed pawn (and White none): `fh` carries a threat for Black. The line given in the task:
  h6-h5, h5-h4, g3xh4, is also legal with no earlier passed pawn, but its last position is a race (both
  sides have a passed pawn: White's h4 is passed as well), which the definition also counts as a Black threat; it is
  proved too (`fh_race_line`).

So `x2` has two components with opposite threats. `lineOK` is a checker: every step is a member of `moves` for the
colour given, and every position from which a step is made (the start and the intermediate ones) has no passed
pawn; the last position is not tested by `lineOK`.
-/
namespace CylChess.Claims

/-- `lineOK e pos steps`: starting at `pos`, each step `(c, q)` is a legal move of `c` (a member of `moves`), and
every position from which a step is made has no passed pawn for either colour. The position reached by the last
step is not tested. -/
def lineOK (e : Env) (pos : Position) : List (Color × Position) → Bool
  | [] => true
  | (c, q) :: rest =>
    !hasPassed e.s e.b pos .white && !hasPassed e.s e.b pos .black &&
      (moves e.s e.b pos c).contains q && lineOK e q rest

/-- After h5-h6. -/
def x1 : Position :=
  Position.ofSquares [sqr 'b' 2, sqr 'd' 4, sqr 'g' 3, sqr 'h' 6] [sqr 'a' 7, sqr 'c' 7, sqr 'f' 7, sqr 'g' 4]

/-- After a7xh6 across the seam. -/
def x2 : Position :=
  Position.ofSquares [sqr 'b' 2, sqr 'd' 4, sqr 'g' 3] [sqr 'h' 6, sqr 'c' 7, sqr 'f' 7, sqr 'g' 4]

/-- The component on files b to d. -/
def bd : Position := Position.ofSquares [sqr 'b' 2, sqr 'd' 4] [sqr 'c' 7]

/-- The component on files f to h. -/
def fh : Position := Position.ofSquares [sqr 'g' 3] [sqr 'f' 7, sqr 'g' 4, sqr 'h' 6]

/-- `bd` after d4-d5, then after c7-c5. -/
def bd1 : Position := Position.ofSquares [sqr 'b' 2, sqr 'd' 5] [sqr 'c' 7]
def bd2 : Position := Position.ofSquares [sqr 'b' 2, sqr 'd' 5] [sqr 'c' 5]

/-- `fh` after f7-f5, f5-f4, f4-f3. -/
def fh1 : Position := Position.ofSquares [sqr 'g' 3] [sqr 'f' 5, sqr 'g' 4, sqr 'h' 6]
def fh2 : Position := Position.ofSquares [sqr 'g' 3] [sqr 'f' 4, sqr 'g' 4, sqr 'h' 6]
def fh3 : Position := Position.ofSquares [sqr 'g' 3] [sqr 'f' 3, sqr 'g' 4, sqr 'h' 6]

/-- The line of the task in `fh`: h6-h5, h5-h4, g3xh4. -/
def fhr1 : Position := Position.ofSquares [sqr 'g' 3] [sqr 'f' 7, sqr 'g' 4, sqr 'h' 5]
def fhr2 : Position := Position.ofSquares [sqr 'g' 3] [sqr 'f' 7, sqr 'g' 4, sqr 'h' 4]
def fhr3 : Position := Position.ofSquares [sqr 'h' 4] [sqr 'f' 7, sqr 'g' 4]

/-- The way in: h5-h6 (White), a7xh6 (Black, across the seam). The roots `posX`, `x1` have no passed pawn
(`lineOK`), and neither has `x2`; `x2` has exactly the two components `bd` and `fh`. -/
theorem notHSS_way_in :
    lineOK envX posX [(.white, x1), (.black, x2)] = true ∧
    hasPassed envX.s cyl8 x2 .white = false ∧ hasPassed envX.s cyl8 x2 .black = false ∧
    components cyl8 x2 = [bd, fh] := by decide

/-- The component `bd` carries a threat for White: d4-d5 (White), c7-c5 (Black) is legal, `bd` and `bd1` have no
passed pawn, and `bd2` gives White a passed pawn and Black none. -/
theorem bd_white_threat :
    lineOK envX bd [(.white, bd1), (.black, bd2)] = true ∧
    hasPassed envX.s cyl8 bd2 .white = true ∧ hasPassed envX.s cyl8 bd2 .black = false := by decide

/-- The component `fh` carries a threat for Black: f7-f5, f5-f4, f4-f3 (Black) is legal, `fh`, `fh1`, `fh2` have no
passed pawn, and `fh3` gives Black a passed pawn and White none. -/
theorem fh_black_threat :
    lineOK envX fh [(.black, fh1), (.black, fh2), (.black, fh3)] = true ∧
    hasPassed envX.s cyl8 fh3 .black = true ∧ hasPassed envX.s cyl8 fh3 .white = false := by decide

/-- The line of the task: h6-h5, h5-h4 (Black), g3xh4 (White) is legal with no earlier passed pawn, and the last
position gives Black a passed pawn (and also White: it is a race). -/
theorem fh_race_line :
    lineOK envX fh [(.black, fhr1), (.black, fhr2), (.white, fhr3)] = true ∧
    hasPassed envX.s cyl8 fhr3 .black = true ∧ hasPassed envX.s cyl8 fhr3 .white = true := by decide

end CylChess.Claims
