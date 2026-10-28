import re
L = open("/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md").read()
edits = []
def E(label, old, new):
    assert L.count(old) == 1, (label, L.count(old))
    edits.append(f"### EDIT {label}\n<<<<<<< OLD\n{old}\n=======\n{new}\n>>>>>>> NEW\n")

E("status row (V1a)",
 '| §1.5 "each hypothesis is needed" | (V1b), (V2), (V3), (V4): counterexamples given. (V1a): none given, so "needed" is a CONJECTURE | R1 item 4, R2 item 7 |',
 '| §1.5 "each hypothesis is needed" | (V1b), (V2), (V3), (V4): counterexamples given. (V1a): the clause "no checks" is needed, PROVED by an isolated counterexample (cyl:6×6 `Ka2 kb4 Pa3 pa4 Pd2 pe3 b -`, a Z-pawn check; CHECKED-2 in P with real kings, K17). The clause (E) (e.p. across components): no isolated counterexample in a bounded search, so "(E) is needed" stays a CONJECTURE; in the structured class of Definition 2.1 these two clauses are the only ways (V1a) can fail (PROVED, Proposition 1.15) | R1 item 4, R2 item 7, K17 |')

E("heading",
 '**Each hypothesis is needed — except that for (V1a) this is a CONJECTURE (revised after review: R1 item 4,\nR2 item 7).** Each can fail and change the result.',
 '**Each hypothesis is needed (revised after K17, 2026-10-27: (V1a) now has an isolated counterexample for its "no\nchecks" clause; for its clause (E) "needed" is still a CONJECTURE).** Each can fail and change the result.')

E("why exact",
 '(V1)–(V4) are sufficient, and none can be dropped, except that for\n(V1a) this is a CONJECTURE (table below).',
 '(V1)–(V4) are sufficient, and none can be dropped (table below; for the clause (E) of (V1a) this is\na CONJECTURE).')

E("table row (V1a)",
 [l for l in L.splitlines() if l.startswith("| (V1a) non-interaction |")][0],
 '| (V1a) non-interaction | **The clause "no checks": PROVED needed (K17), CHECKED-2.** cyl:6×6 `Ka2 kb4 Pa3 pa4 Pd2 pe3 b -`. Z = Ka2, kb4 and the locked pair Pa3/pa4 on F_Z = {a, b}; context Pd2/pe3 on d, e; buffer c, f. The Z-pawn a3 checks kb4, so Black\'s only legal moves are the four king moves (Z-moves), and every one loses in P with real kings (`kp_p --pmodel`: W; independent solver `K17/scripts/refp.py`: W). D, with Z deleted, lets Black play e3–e2 or e3×d2, a passer at once: D(Black to move) = Black wins (D_whole, D_fix and o(S) all give N). So P(X) = W ≠ D(X) = L. Here (V1b) holds (4 legal moves), (V2) and (V3) hold at every chess-reachable position (X alone, because every legal move is a Z-move), and (V4) holds (HSS, one component, tempo bound). The twin with kb5 (no check) satisfies (V1)–(V4) at every chess-reachable position and P = D for both sides to move (W to move: W, Black to move: L), so the check is the only cause. A deeper context, `Kb6 kb3 Pa2 pa3 Pd2 Pe3 pe5 b -` (twin kb2, 6 + 4 chess-reachable positions for the two sides to move), behaves the same (COMPUTED-1, kpsolve only: X = W; twin W to move: W, Black to move: L; D = N in all three D models). With frozen kings (V3 by fiat) `Ka1 kb4 Pa3 pa4 Pd2 pe3 b -` behaves the same (`kpsolve --frozen`: W; twin kb5: L). Statistics of the search in `kings/delegate/out/K17/`: frozen, 514/514 (flat:6×6 and cyl:7×6, ≤ 2+2 pawns on 3 context files), 411/411 (cyl:6×6, ≤ 3+3 pawns on 2 files) and 6/6 (cyl:5×6, one context file) contexts where Black wins D moving first give P ≠ D at the checked root; real kings, 781 (cyl:6×6), 3780 (flat:6×6), 3657 (cyl:7×6) layouts with P = W ≠ D = Black, of which 257, 1362 and 1210 have a twin that satisfies all of (V1)–(V4) with real kings. The king sorties found earlier (41 of 449 tablebase king moves draw and 7 win, `engine/suite/`, RESULTS §1) remain (V2)/(V3) failures. The clause **(E)**: no isolated counterexample, see Proposition 1.15 (CONJECTURE that it is not needed when (V4) holds) |')

prop = '''
**Proposition 1.15 (what (V1a) can mean in the structured class; K17, 2026-10-27). PROVED for (a); (b) COMPUTED-1, bounded.**
Let X be as in Definition 2.1 (kings and Z-pawns on F_Z, context on files at distance ≥ 2, buffer empty, no officer) and let
Y be a chess position reachable from X by legal moves in which no Z-move has been made.
- **(a)** Then the legal chess moves of the side s to move that are not Z-moves are exactly its context pawn moves (with
  the global e.p. right) if s is not in check at Y, and there are none if s is in check at Y. Whether s is in check is the
  same at every such Y: it is decided at X. In particular there are no pins (no slider exists before the first
  promotion), no checks arise after the root (context pawns never attack F_Z by Lemma 2.2, and kings and Z-pawns have
  not moved), and a king never blocks or captures a context pawn in one move. So (V1a) fails at X iff **(check)** the side
  to move at X is in check from a Z-pawn, or **(E)** fails (the persisting local right of a component is the only other
  difference between chess moves and D-options). *Proof.* A context pawn move is illegal only if it leaves the mover's king
  attacked. With no sliders the only attackers are pawns. Context pawns attack only buffer and context squares
  (Lemma 2.2), so after a context move the attackers of the king are the same Z-pawns as before. If s is in check, a
  context move would have to capture the checking Z-pawn, which lies on F_Z, two files from every context pawn's
  captures, or block, which a pawn check cannot be. En passant is also a context move. The remaining difference between
  D-options and chess moves is the right that persists in a component of the sum while another component is played: that
  is (E). ∎
- **(check) is needed.** Example in the table row of §1.5 (`Ka2 kb4 Pa3 pa4 Pd2 pe3 b -`, cyl:6×6; CHECKED-2, kpsolve and an
  independent solver). The side in check has only Z-moves, so under (V3) it loses in P, while D lets it play in the context.
- **(b) (E).** In the structured class a chess position with a pending right at the root, or one reached later, and ≥ 2
  components, violates (E). Systematic search (K17): contexts on files c, d, f, g of flat:8×6 (F_Z = {a}, buffer b),
  ≤ 5 + 5 pawns, roots with a fresh e.p. right for the side to move (313,476 contexts, 39,696 roots, 39,600 with ≥ 2
  components, so (E) fails at the root); and contexts on c to f of flat:6×6 and cyl:7×6, ≤ 3 + 3 pawns, roots without a
  right (flat:6×6: 1,128 (E)-violating roots; the cyl:7×6 run was not completed). Result: the whole-board D (chess e.p.) and
  the sum D with persisting rights differ in 48 roots (all in flat:8×6, all with (V4) false: opposite threats in
  different components), and never when (V4) holds (2,560 hereditarily sum-safe multi-component roots of the ≤ 4 + 4 run
  alone; o(S) = D_whole in all of them). So no isolated counterexample for (E) was found, and when (V4) holds the sum
  reading and the chess reading agreed on every searched root: CONJECTURE that (E) can be dropped under (V4), in this
  boundary only.
'''
E("proposition 1.15",
 '| (V4) dominance | Proposition 1.12 (cancellation, for every B) and Proposition 1.13 (tempo above B) |',
 '| (V4) dominance | Proposition 1.12 (cancellation, for every B) and Proposition 1.13 (tempo above B) |\n' + prop.rstrip("\n"))
open("../EDITS.md", "w").write("\n".join(edits))
print("ok", len(edits))
