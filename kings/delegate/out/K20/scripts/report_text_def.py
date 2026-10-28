# Text of the definition section (K20).  Imported by build_summary.py, which writes summary.json.
DEFINITION = r"""
LOCAL KING GAME LK(pairs, R)

Data. A board (cyl:WxH or flat:WxH; ranks 1..H; cyclic file adjacency on a cylinder; rules of kings/SPEC.md), a set
of blocked pawn pairs (a white pawn on (f, r) with a black pawn on (f, r+1), 2 <= r <= H-2; at most two pairs, on
files within a window of at most 4 files) and a region R of squares.

Positions. x = (S, wk, bk): S = set of pawns still alive, wk and bk the king squares. Legal: kings not adjacent,
no shared squares, no king on a square attacked by an enemy pawn of S. The initial S is the full set and has no
passed pawn. Passed = no enemy pawn on the same or an adjacent file strictly ahead (cyclic adjacency on a cylinder),
the test of cylcgt.pawns.passed; no e.p. right can exist because no pawn ever moves.

Moves. LK is a D-game (LOOPY Definition 1.1): option sets L(x) (White) and R(x) (Black) are defined for every x.
Only kings move; pawns never move (blocked or frozen). A king steps to a neighbouring square t of R such that t is
not occupied by an own pawn, t is not adjacent to the enemy king, and after the step t is not attacked by an enemy
pawn of S (a captured pawn no longer attacks). If t holds an enemy pawn the step is a capture and the pawn leaves S.

Decisive events. If after a capture the pawn set has a passed pawn for exactly one side, the move is an option to
the terminal of that side (+ White has won, - Black has won): the D-model rule 'a king capture of a pawn that
creates a passer'. A capture can only remove a blocker of the capturer's own pawns, so the other side never gains a
passer at the same time; the race rule is never needed (the solver counts races: 0 in every run). A capture after
which no passer exists is an ordinary move to the position with the smaller S (pawns still frozen). No promotion
occurs because no pawn moves.

Normal play. A player with no legal move loses (LOOPY Definition 1.2). Chess would call a king with no legal move
and not in check stalemate (a draw). No king is ever in check in LK (only frozen pawns attack, and a king never
steps onto an attacked square), so check never interferes.

Faithful configurations. A configuration is faithful if in every alive set reachable by non-decisive captures no
pawn has a push or a pawn capture. Then LK is chess with frozen pawns, up to the decisive-event convention (V2 of
LOOPY Theorem 1.14). Two pairs on files at cyclic distance >= 2 are faithful (every king capture creates a passer);
two pairs on adjacent files are not, and for them LK is a model only.

Sortie. R is the set of squares the kings may use; a sortie is a king step leaving R.
 - Free (F): R = whole board, no sorties; LK is the isolated K+P group with an empty context.
 - Box(m): R = the files of the pawns (arc from leftmost to rightmost pawn file) widened by m files on each side
   (m = 0, 1, 2); leaving the box is illegal (a wall).
 - Sortie as suicide (an option to the opponent's terminal) is the same as Box(m) in every D-sum: PROVED. A suicide
   option is the worst option for its owner; by LOOPY Lemma 1.7 it can be deleted, and when it is the only option the
   owner loses either way, since 'no move' also loses under normal play. So only F and Box(m) are computed.

Pass. A pass is not a move of LK. In a sum G (+) K a player passes by moving in K. Reservoirs: on (White passes
forever), off (Black), dud (both), the integers n and -n (n White or Black spare moves), n = 1, 2, 3. The local games
L_T of Definition 2.6 (one side forcing, the other passing forever) are G (+) on and G (+) off.

Sum and value. LOOPY Definition 1.3: a move in one coordinate; a move to a terminal in either coordinate ends the
whole play; a player with no move in any coordinate loses; infinite play is a draw. Outcome pair (r_w, r_b) = result
with White to move, with Black to move, each W, D or L from White's view. Two D-games are battery-equal if their sums
with every game K of a fixed battery have the same outcome pair. Battery B34: 34 games, namely 0, *, +-1, +-2, +-3,
+-1/2, up, down, up*, down*, *2, on, off, dud, over, under, tis, tisn, the threats {+|}, {|-}, {+|-}, {+|0}, {0|-},
{+|on}, {off|-}, the switches {1|0}, {0|-1}, {2|0}, {0|-2}, and {on|off}. Battery B4553 (extended): 64 games
{A|B}, A and B subsets of {+,-,0}, and all 4489 games with at most one option per side taken from {+,-} and those
64 games, plus the B34 games. A root is NAMED by the reference game H when its battery signature equals H's.
This is an approximation of equality in all sums (open question 4 of LOOPY section 8 is about exactly that).
Short games would get canonical forms (BIG translation, cylcgt.cgt); only trivial short roots occur.
"""
