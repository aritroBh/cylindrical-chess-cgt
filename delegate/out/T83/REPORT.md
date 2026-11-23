**Text 1 — GAP. Text 2 — SOUND WITH FIXES.**  
**PROVED** — A.11 transfers the winner for each qualifying side to move. The empty-context example in A.13 works exactly as claimed.  
**PROVED** — A.16 proves a promotion-game win by the deadline. Its stronger assertion that the win occurs on a move *after* the reply is false.  
**PROVED** — The Möbius insertion preserves the two first-mover outcomes against every finite nim-heap, given the stated base and small cases.  
**CHECKED-2** — Two independent rules implementations support the Möbius base. Four support the small cases in the original comparison, and the independent referee also confirms them.

## Text 1 — kings appendix

Line references in this section use `s12a_core.tex` in `dist/tog/supp_src/`. Proposed replacements are for that source unless otherwise stated. **PROVED** denotes a deduction from the specified rules, including deductions checked by hand on a displayed board. Computations have separate labels. The chess arguments apply to the games defined at lines 220–225. A.11–A.13 use the chosen textbook, e.p.-aware or e.p.-off setting subject to their stated hypotheses. A.16 concerns legal chess e.p. and first promotion; its certificate does not adjudicate passed pawns.

### A.10 — CORRECT AS IT STANDS

**PROVED — `s12a_core.tex:227–234`.** A first pawn to enter a previously pawn-empty buffer file cannot push there from another file. Both ordinary and e.p. captures require an enemy pawn already on the destination *file*, even when the destination *square* is empty. Kings moving through the buffer do not supply a capturable piece. The empty files therefore persist, keep the two pawn populations apart, and put every context pawn more than one file from every king-group file. The argument works at both ends of an arc, including across the cylinder seam. No replacement.

### A.11 — CORRECT WITH A FIX

**PROVED — `s12a_core.tex:237–251,259–277`.** Fix the actual starter and a winning strategy in the finite pawn game. At the winner's turn a move of that strategy exists, since having no move loses. At the opponent's turn every pawn option either preserves the strategy's win or gives $\sigma$ the terminal award. In both cases (V1) identifies the *successor* as well as the move, including the right. On a passer event (V2) supplies the chess continuation, even if the mover loses the race. Only the opponent can choose a Z-move along this strategy, and then (V3) supplies the continuation. In particular, if the opponent has no pawn move, (V1) still gives it a legal chess move and every such move is a Z-move. This accounts for the normal-play loss without treating it as chess stalemate.

**PROVED — `s12a_core.tex:273–277`.** Each non-event decreases the nonnegative total pawn potential by at least one. A prefix of length $\Phi_W(X)+\Phi_B(X)$ therefore cannot be followed by another non-event, and (V1) rules out stopping there for lack of a move. This is a bound in plies through the first event, not a bound on the subsequent mate. A.2(a) concerns the *pawn-game* successor of a promotion. More strongly, induct along the common prefix: the context starts without a passer, an ordinary chess right belongs to the previous mover, and every non-event preserves the absence of a passer. A.2(c) now excludes even a promoting *context event* from such a parent, since $H\ge5$. A Z-promotion is an event by definition. Thus no comparison of a promoted chess officer with a retained model pawn is needed. The proof needs the two directions of the move correspondence, matching successors, legal-move existence, and the winning continuations. The no-check clauses are sufficient extra hypotheses. No assumption of (E) is used here.

**MINOR · PROVED — `s12a_core.tex:238,248,264,269–270`.** “After which $W$ would end” also admits a no-pawn-move child, whereas the defined context event is the first passer. The proof handles an immobile opponent at its *next* chess turn. Make the event terminology unambiguous. At lines 238–239 replace “a context move after which $W(X)$ would end, that is, some side has a passed pawn among the context pawns” with `a context move that leaves some side with a passed pawn among the context pawns`. In (V2) use `every context move at $Y$ that produces a passed pawn and is adjudicated for $\sigma$ in $W$ leads to a chess position that $\sigma$ wins;`. At 264 and 269–270 replace `If it ends $W$` by `If it produces a passed pawn`. The option-free child otherwise remains covered by line 271.

**MINOR · PROVED — `s12a_core.tex:253–255,274–275`.** The quotation about “either side” predates the current main theorem (`dist/tog/sections/04_kings.tex:49–59`). Replace the main-text lead-in through “Precise form:” with `For the given side to move, the main text identifies the chess result with the outcome of $W(X)$ under (V1)--(V3). Precise form:`. Replace “The play is never stalemate (V1)” with `Before the event, (V1) excludes stalemate; from the event onward the chosen winning continuation excludes it.` In the next sentence use `a context promotion would make a passed pawn in the pawn-game successor by Lemma~A.2(a) and so would itself be an event`.

### A.12 — CORRECT WITH A FIX

**PROVED — `s12a_core.tex:280–286`.** (a) Read “equality of move sets” as the correspondence *with matching results*. With stationary kings, a context pawn cannot attack either king's file, uncover a slider, capture a checking Z-pawn, or interpose against a pawn check. (b) The transfer works in P and F with (V2) and (V3) interpreted in the destination game. In F a king move loses by rule, and Z-pawn moves still require (V3). (c) The no-passer restriction is exactly the domain of $W$. (d) Chess and $W$ both expire a right after one ply. (E) belongs to the sum comparison, as specified by A.7. No change to (b) or (d).

**MINOR · PROVED — `s12a_core.tex:280,285`.** At 280 replace `the equality of move sets` with `the move correspondence with matching successors`. At 285 replace the entire last sentence of (c) with `The main theorem explicitly assumes at least five ranks, as required for the use of Lemma~A.2(c).` The current main theorem opens with that assumption.

### A.13 — CORRECT WITH A FIX

**PROVED — `s12a_core.tex:288–292`.** Take $F_Z=\{a,b,c\}$ on the flat board. With no context pawns, $W$ has no move and $S$ is the empty sum $0$; either player starting either pawn game loses. HSS and (E) are vacuous, $N(X)=0$, and the race rule is never invoked. All real moves are Z-moves, so the pre-event reach consists of the starting position alone.

- With Black to move neither king is in check. The white king b6 covers a7 and b7; c7 covers b8. Black therefore has precisely `a5–a4`. White answers `c8=Q#`. The queen checks along c8–b8–a8, b8 remains attacked and a7 and b7 remain covered. The black pawn can neither block nor capture. Thus (V1) holds, (V2) is vacuous and (V3) holds for the sole legal move.
- With White to move the legal moves are `Ka6, Kxa5, Kb5, Kc5, Kc6` and the four promotions on c8. The queen and rook promotions mate. After Black's forced `a4` the same list applies with `Ka5` in place of `Kxa5`. Bishop and knight promotion give no check. At the White-to-move root a mating Z-move violates (V3). White wins the chess game while the empty sum loses for White.

A.11 and A.7 give the corollary for the same starter. **MINOR · PROVED — `s12a_core.tex:289`.** Replace `The main text's ‘‘either side to move’’ assumes the hypotheses for both.` (the source uses TeX quotation marks) with `To infer the full outcome class one must verify the chess hypotheses for both starters.` The main theorem now already says “for each side to move for which this holds”. The example itself needs no repair.

### A.14 — CORRECT WITH A FIX

**PROVED — `s12a_core.tex:295–306`.** Only e is empty at the root. The two legal alternating moves h5–h6 and a7×h6 create a second empty file, a. The listed blockers persist to the indicated positions, so the split is actually reached before adjudication. In the f–h component the successive black pushes keep g3 ahead until f4×g3 removes the last white pawn. In b–d the d-pawn remains blocked by c7 through d6; c7×d6 leaves b2 and the black d6 pawn both passed. This counts as a White threat regardless of who wins the race. The threat sequences need not alternate, unlike the two moves used to reach the split.

**MAJOR · CHECKED-2 — `s12a_core.tex:295–297`.** The self-contained statement specifies e.p. off but leaves the race rule open. Two independent evaluations of $S$ give R with `count` and N with `mover` at $\mathrm{BIG}=256$. One whole-board minimax gives N under both rules (**COMPUTED-1** in this audit). Thus the numerical clause is false as a setting-independent statement. The main paper declares a default count rule at `dist/tog/sections/02_rules.tex:79–81`. Replace `On $\cyl{8}$ with e.p.\ off, let` with `On $\cyl{8}$ with e.p.\ off, the count race rule and $\BIG=256$, let`. E.p. off uses the textbook passed test. The hand proof of (a,b) needs no race verdict. The check also covers `opponent`, for which $S$ is R and $W$ is N.

### A.15 and (C1)–(C3) — CORRECT WITH A FIX

**PROVED — `s12a_core.tex:311–340` and `dist/tog/sections/04_kings.tex:82–86`.** The quoted words match the current paper. They are a fair synopsis with the pointer to S12, but the sentence alone does not define an equivalent operational test. The clock starts *after* the non-promoting Z-reply, with the defender moving first. In (C1) the defender may pass out of check and the punisher's king stays on $F_Z$. In (C2) the defender can also move its king, including capturing a context blocker. In (C3) the selected real strategy must avoid *defender* stalemate over all real responses, using local winning moves with the time left. Seeing one cooperative promotion or one stalemate-free variation does not verify these conditions. Rejecting an immediately capturable new queen strengthens local promotion safety without establishing a chess win.

**MINOR · PROVED — `s12a_core.tex:334–339`.** Replace the explanation from `This is a summary` through `stalemate clause is (C3).` with:

~~~tex
The quoted sentence summarizes (C1)--(C3). The clock counts the
punisher's moves after its reply. Condition (C1) uses the projected board,
a defender allowed to pass out of check, and a punisher whose king stays
on $F_Z$. Condition (C2) lets the defender move its king and context
pawns consecutively in $Q^\circ$, including king captures of blockers.
Condition (C3) requires a choice of guided real strategy that avoids
defender stalemate throughout the window.
~~~

**MINOR · PROVED — `s12a_core.tex:329–331`.** Give the strategy's domain explicitly. In particular, it has no duty to move after a real mate or to find a local move after the deadline. Replace (C3) with:

~~~tex
\item[(C3)] \emph{No stalemate.} There is a strategy for $\bar s$ from
$Q$ in $\mathrm{P}$ with the following property. Until the game ends or
$\bar s$ has made $h$ moves from $Q$, each move it prescribes is a legal
Z-move whose projection is winning in (C1) with the remaining number
of moves. In every such play $s$ is never stalemated before $\bar s$'s
$h$-th move. Call this a guided strategy satisfying (C3).
~~~

### A.16 — GAP / WRONG as to timing; the promotion-game win follows

**BLOCKER · PROVED — `s12a_core.tex:343–344,385–390`.** The proof establishes *local mate implies real mate*. The converse can fail because deleting context pawns can give the defender an escape. In particular the reply $r$ can be real checkmate when $\pi(Q)$ is live. This is the earliest possible failure of “with one of its next $h$ moves”.

On the flat board take $F_Z=\{a,b\}$, buffer c, White **Ka6, b6, b7, d6**, Black **Ka8, a7, e7**, Black to move. The context pawns d6 and e7 block one another's passed test. Black is checked by b7. Its only legal move is $m=\mathrm{Kb8}$; White's legal non-promoting Z-reply is $r=\mathrm{b6{\times}a7\#}$. The a7 pawn checks b8. The white king protects a7 and b7, b7 attacks a8 and c8, and d6 attacks c7. Black cannot answer the pawn check.

Take $h=1$. In $\pi(Q)$ the d6 and e7 pawns disappear. Black is checked and has exactly **Kc7**; it cannot pass. White now promotes **a8=Q** on its first move, proving (C1). In $Q^\circ$ the only black context pawn starts on e7 and cannot promote in one black move, proving (C2). In the real $Q$ Black is checkmated. There is no White turn to guide and no defender stalemate, so (C3) holds. The real game has already ended on $r$. This is a counterexample to the displayed timing conclusion under either passed test and with no e.p. right. It also disproves Step 4's claim that every maximal real play projects to a *completed* local win.

Replace the conclusion from `it plays $r$` through the end of line 344 with:

~~~tex
it plays $r$ and wins by promotion or mate no later than its $h$-th
subsequent move. The reply itself may already mate; otherwise it follows
the guided strategy of (C3) for as long as play continues.}
~~~

**PROVED — `s12a_core.tex:347–373`, invariants and Steps 1–2.** The buffer survives both opening moves. The punisher's context pawns stay put or are captured. The defender's king was safe from them after $m$ and cannot later step into their attack. Before promotion, the only possible check on that king comes from a retained Z-pawn. A legal defender king move projects to a legal step, including a capture that becomes an ordinary step. A Z-pawn move retains its local squares and relevant right. A non-promoting context move is a pass: it clears any retained right and cannot answer a Z-pawn's check. Conversely a permitted punisher move uses only $F_Z$, including both squares of a king step. Its king is safe there from context attacks; any e.p. right it could use is present in both games.

For existence, start at the (C1) win and induct on **live projected prefixes** with the remaining deadline. Every legal defender reply preserves a punisher win, and choosing a winning punisher move preserves it with one fewer punisher move. At a live punisher turn a winning move must exist: having no permitted move is a local failure. The lifting argument makes that move legal in the real game. (C3) supplies the *choice among* those moves that avoids stalemate. The choice may depend on the full real history. Fixing the witness $\rho$ in line 347 fixes that real strategy; no step requires all its moves to belong to one preselected local strategy.

**MINOR · PROVED — `s12a_core.tex:347–348,364–367,370–373`.** To avoid projecting a context officer on the very move whose possibility Step 3 is testing, replace `A context-pawn move leaves` with `A non-promoting context-pawn move leaves`. Replace `Hence the projection of the play is a play` with `Hence, up to a possible first context promotion, each nonterminal real prefix projects to a legal prefix`. At 371 replace `its right is the same (I4)` with `every right usable by this local move agrees in the two positions (I4)`: a defender double step off $F_Z$ can leave an unprojected right. Replace `By Step~1 the projected position is one that` with `By (C1) at the root and induction using Step~1 and the previous guided choices, the live projected position is one that`.

**PROVED — `s12a_core.tex:375–383`, Step 3.** A defender Z-promotion would give a local failure. For a first context promotion consider its move directly. Erasing the punisher's turns and the defender's Z-pawn turns leaves the defender king and both sets of surviving context pawns in precisely their replayed positions. A king capture of a deleted Z-pawn is an ordinary king step in $Q^\circ$. No punisher can capture a context pawn along this play, and no defender context pawn can capture e.p. because the punisher only double-steps on $F_Z$. The resulting sequence in $Q^\circ$ ends at promotion in at most $h$ defender moves, contrary to (C2). Replace the opening of Step 3 up to `A promotion of a Z-pawn` with `In the window from $Q$ through $\bar s$'s $h$-th subsequent move, $s$ has at most $h$ turns, since $s$ moves first. A promotion of a Z-pawn`. This counts the window without assuming either game has already won.

**BLOCKER repair continued · PROVED — `s12a_core.tex:385–390`, Step 4.** Replace this step with:

~~~tex
\emph{Step 4: $\bar s$ wins.} If $s$ is already mated at $Q$ or is
mated earlier on the real line, $\bar s$ has won. Otherwise (C3)
excludes real stalemate of $s$ at each of its turns before the deadline.
Step~2 supplies a legal winning move at each live punisher turn, and
Step~3 excludes defender promotion in the window. Thus while the real
line continues its projection is a local prefix with only winning
punisher moves at their remaining budgets. Such a prefix cannot continue
past the $h$-th punisher move without local promotion or mate. A local
punisher promotion is the same legal real promotion. At a local mate
$s$ is in check in the real game by (I3), and any real escape would
project to a legal local escape by Step~1. Hence the real game ends in
a punisher win by the stated deadline.
~~~

### A.17 — CORRECT AS IT STANDS

**PROVED — `s12a_core.tex:393–395`.** A.17 uses only the P-win part of A.16, which survives. A certificate for every legal Z-move at the specified positions gives (V3) in P. The quantifier is substantive: under the stated data a *promoting* Z-move cannot be certified. In chess promotion is not a terminal win. No replacement.

**Numbering only · PROVED — `s12a_core.tex:397–403`.** All named destinations exist in `dist/tog/supp/s12.tex`: the per-position axiom (A_Q) at 484; Definition 1.10 at 532; Theorem 1.11 at 550 with its re-splitting frontier and induction at 595–599; Proposition 1.12 at 607; Theorem 1.14 at 648 with (i),(ii) and its sharp form at 712; Proposition 1.15(a) at 762–765; Lemma 2.2 at 787; Definition 2.6 at 851 with (L1_P),(L2),(L3); Theorem 2.7(a) at 902–905; and “What Theorem 2.7 does not give” at 949. No numbering replacement. This checks the destinations only.

## Text 2 — Möbius note

Line references use `s15_note5.md` in `dist/tog/supp_src/`. The test is e.p.-aware, e.p. is on, and races use count with ties awarded against the mover. The theorem concerns the whole board against a nim-heap.

### Summary and §0 — result and evidence labels

**PROVED — `s15_note5.md:5–13,19–29`.** The three words have the stated widths. The F3 final token puts two pawns on one file. The ranges exclude exactly the two asserted exceptions at $m=0$. The dependence of the hand proof on C1 and C2 is disclosed. The single cut per family suffices. The fixed reduced-graph counts follow for large $m$ because the proof of Lemma 3 actually matches T-moves as well as T-flags; for the shorter stable ranges the displayed computations supply the remaining cases.

**MINOR · COMPUTED-1 — `s15_note5.md:11–12,17,26–28`.** The end of line 12 attributes precise increases in full-search nodes to discarded block moves. Graph isomorphism does not count the descendants visited by a particular minimax implementation, and the earlier node series is for M1 over finite ranges. Replace its last sentence with `In the sampled stable ranges M1's full-search counts increase by 1251, 1239 and 719 per width increment of two files for F1, F2 and F3 respectively. Lemma 3 explains why inserting central wall pawns adds no reduced nodes.` At 11 replace `The seam changes the dynamics only at the block's outer end` with `In F1 and F2 the seam changes move classes at the end of the block next to it`; F3's seam is in the fixed part. At 13 replace `ending at the seam` with `starting at file 0 beside the seam`.

**MINOR · PROVED (counting the documented implementations) — `s15_note5.md:17,26–28`.** Calling the referee “a fourth implementation” is ambiguous immediately after listing R and three earlier rules solvers. U uses R's move generator and adjudicator. Replace the final clause of line 17 with `R, M1, M2 and K are the four rules implementations in the original small-case comparison. U shares R's rules. The independent referee supplies a fifth rules implementation and the second computation of the C1 graph statistics.` The C2 row's “CHECKED-4” is honest for the named original comparison, conservative overall. Replace `M1, M2 to $m=12$` in that row with `M1 and M2 through $m=12$ for F1 and F3 and $m=11$ for F2`, as line 115 correctly specifies. D compares two rules implementations, R/U and M2. At line 27 replace the parenthesis after `COMPUTED-1 (R)` with `(extra evidence; for $m\ge5$ the induction uses only the family's fixed admissible cut)`. Lemma 3 does not apply *directly* to every tested cut. For an intact periodic block, inserting its period at different internal cuts gives the same extended word on each node.

### §1 — rules, patterns and symmetries

**PROVED — `s15_note5.md:33–41`.** The phase repair is present. Requiring the original colour, rank and direction *on each file of one alternating wall* excludes two separately phased walls meeting at the cut. The two old files survive insertion; the new files carry copies in the unique continuing phase. The seam remains the same adjacency at the ends of the chart. Rank reflection with colour and direction reversal preserves the home double step, seam target and flag privileges. It also preserves the two race distances after exchanging players and preserves the tie instruction. Horizontal reflection exchanges the two permissible orientations of the lemma windows.

**MINOR · PROVED — `s15_note5.md:33,37`.** Specify what rank is mirrored in a capture and when the full game's flag lapses. At line 33 replace `a capture across the seam lands on the mirrored rank $9-r$ and flips $d$` with `a pawn on rank $r$ capturing across the seam lands on chart rank $9-(r+d)$ and flips $d$`. After the race definition add `A front pawn has no pawn of either colour ahead on its own file in its direction. The minimum over no eligible passed pawn is $+\infty$.` At 37 add `Here $X$ denotes the mover and $Y$ the opponent. In both the full and reduced sums, a heap move keeps the pawn position and its flag; only the eligible colour may use the flag, and the next pawn-component move clears the old flag whichever colour moves.` This resolves the apparent tension with “next move only” in §1. The family base graphs are flag-free.

### §2 — seam table

**MINOR · COMPUTED-1 — `s15_note5.md:45–53`.** The table promises *every* move on four files but gives examples. F1 omits both pushes from file 1, for instance. The F3 row compresses **three** K-moves into “K, K”. The two individual seam explanations in F1 and F2 check out: the F1 capture from 0 reverses direction and creates a Black passer; in F2 the pawn on 18 is seen from 0 on rank 2, behind the White capturer on rank 3. Replace line 45 with `The table gives selected root moves from files $n-2,n-1,0,1$ at $m=5$, with their classes on both surfaces.` Replace the F3 move and class cells with `$B6\to5$ on 0; $W2\to3$ and $W2\to4$ on 1 | K, K, K | K, K, K`. Replace “All other listed moves” with `All remaining legal root moves on the four files $n-2,n-1,0,1$`. Replace the final sentence of line 53 with `For F1 at $m=5$ the reduced graph has 435 nodes on the strip and 441 on the cylinder.` This removes an ambiguous family and an unsupported inference of node count from the zone alone.

### §3 — V and Lemmas 1–3

**PROVED — `s15_note5.md:59–61`, V.** At a cut edge the copy supplies the original neighbour's contents. At a seam endpoint the *other* neighbour is still mirrored. A potential flagged double-stepper is up on 4 or down on 5; none of the four pattern tokens has that rank/direction combination. Hence neither copy can duplicate a flagged pawn, and eligibility of old capturers is preserved. Each new pawn has an enemy strictly ahead, and the old passers retain their direction and their own-file contents. This preserves front-pawn eligibility, both race minima, and the winner for the same mover, even at a terminal child. **MINOR** at 59–61: replace `is blocked by both neighbours` with `has an enemy strictly ahead on both neighbouring files and so is not passed`; the pawns may still push. Replace `the same pawns with the same squares` with `their images with the same ranks, directions and own-file contents`. File coordinates to the right shift by two. “Same view” is with files and rights transported by this relabelling.

**PROVED — `s15_note5.md:63–65`, Lemma 1.** The non-terminal-root repair is present. A terminal award includes the mover for a tied race. An L-option loses immediately and a P-option leaves an immediate winning terminal reply for the opponent regardless of the heap. T remains an immediate win. The remaining K- and heap options therefore preserve both first-mover win tests by induction. Finiteness follows, for example, by ordering positions lexicographically by pawn count, remaining directional pawn steps and heap size: a capture strictly reduces the first coordinate, a push reduces the second, and a heap move reduces the third. No global monotonicity of chart rank is needed. **MINOR** at 65: replace `their values are those of the reduced game` with `their outcomes for the player to move agree with those in the reduced game`. The lemma proves an outcome equivalence for the specified tests.

**PROVED — `s15_note5.md:67–69`, Lemma 2.** In an E wall the only moves from the middle file are W2–3, W2–4, or B4–3, as appropriate. The neighbouring files have empty capture squares and the wrong colour/direction for the needed enemy up-stepper on 4. A single push leaves an enemy ahead. A double push is e.p.-capturable, and expiry of an old enemy flag cannot release another friendly passer. For (b), a new enemy passer makes the move L. Otherwise the neighbour captures on rank 3, e.p. in the double-step case. It now has no enemy ahead; on the far side of its vacated file the only exposed opposing pawn still has the blocker on $j+3$. No other opposing pawn loses a blocker; the captured pawn was the only possible new flag beneficiary. Thus the reply wins without a race. Reflection and colour reversal give the other window and O wall. All edges actually traversed in these computations are chart edges. No replacement.

**PROVED — `s15_note5.md:71–73`, Lemma 3.** The old central sources $c-3,\ldots,c+4$ and their enlarged range through $c+6$ have a valid five-file window, so none supplies T or K. A far first move can touch the fringe but leaves $c-2,\ldots,c+3$ alone. A seam capture changes only the two board endpoints, both far. Insertion therefore commutes with the move including a fresh flag. In a non-terminal child a near reply cannot award its mover a passer by Lemma 2(a); this use allows the first mover's flag. Every remaining reply corresponds in both directions, even across the seam or e.p., and leaves the cut pair intact. V3 then preserves the existence of a winning terminal reply. This proves preservation of P, hence of K and its children, as well as T. The endpoint case $c-4=0$ is included. No replacement.

### §4 — invariant and step

**PROVED — `s15_note5.md:77–91`.** For $m\ge5$ the arc $0,\ldots,9$ lies in the F1/F2 block and before its zone; the F3 arc $6,\ldots,15$ lies in the block and after its zone. The left endpoint 0 is permitted; no internal edge of the arc crosses the seam. Inserting one period at the stated cut gives the next family root. At each reachable node the invariant supplies the *exact start contents*, including directions and phase, on the entire arc. Lemma 3 gives every K-child in both directions, not just an embedding. Following paths from the two roots proves surjectivity; deleting the inserted files recovers the preimage. Flags stay absent and the added files agree with the extended start. This closes the induction without an assumption about unseen widths. The invariant only needs agreement outside the stated zone.

**MINOR · PROVED — `s15_note5.md:81,85,87–89`.** Define the computed term when it first occurs, e.g. at line 12 after “zone”: `(the union of files whose contents differ from the root at some K-reachable node)`. At line 85 the image of $Z_m$ means the *image of its old file indices*; for F1/F2 the displayed reason $2m\ge5$ starts at $m=3$, not $m=2$. Qualify the first cell of that row with `for the indicated cuts when $m\ge3$`. The proof uses only $m\ge5$. At 87 replace the parenthetical hand example with `(for the finite base and smaller roots see §5; for larger roots V3 and insertion preserve the absence of passers, and the starts carry no right by definition)`. The existing illustrative blocker on file $2m-1$ exists only for positive $m$.

### §5 — finite inputs and reproducibility of the wording

**CHECKED-2 — `s15_note5.md:95–105`, C1.** The grouped $2..13$ row and the explicit line for $m=5$ together give all the inputs. The two independently written graph computations agree as follows. The signature is in increasing heap size $0,\ldots,4$; N means the starter wins and P means the second player wins.

| Family at $m=5$ | Nodes | K-edges | T-moves | Flagged nodes | Nodes with passer | Zone | Signature |
|---|---:|---:|---:|---:|---:|---|---|
| F1 | 435 | 1118 | 404 | 0 | 0 | 10–15 | NNPNN |
| F2 | 417 | 1082 | 356 | 0 | 0 | 10–15 | NNPNN |
| F3 | 435 | 1112 | 428 | 0 | 0 | 0–5 | NNPNN |

**CHECKED-2 (at least two; four in the named original comparison, plus the independent referee) — `s15_note5.md:107–115`, C2.** Against heaps $0,\ldots,3$, F1 and F2 each have NNPN at $m=1,2,3,4$, and F3 has NNPN at $m=0,1,2,3,4$. F1(0) gives RNRR, F2(0) gives NNRR, with R a Black win for either starter. They are outside the theorem. R, M1, M2 and K agree in the recorded comparison. U contributes a full-game algorithm on shared rules for $m\le2$. The referee's separate full-game implementation covers all the required small cases. Independent agreement on signatures does not by itself reproduce C1's graph counts; the referee separately did the reduced traversal.

**MINOR · PROVED — `s15_note5.md:103,107–115,121`.** The admissible-cut list is attributed to logs absent from the note. Replace `The Lemma-3-admissible cuts are listed in the logs` and its parenthesis with `For $m\ge5$ the block contains the required ten-file arc for $4\le c\le2m-6$ in F1/F2 and $10\le c\le2m$ in F3; all of these arcs avoid the zone.` The C2 display still uses `rgraph/unreduced/mob1/mob2/check` after §0 renamed the programs. Its “all” obscures where U stopped. Replace lines 107–115 with:

> **C2.** In a separate invocation per ring, R, M1, M2 and K gave the following signatures for heaps 0 through 3. F1(0) gave RNRR and F2(0) gave NNRR. F1 and F2 gave NNPN for $m=1,\ldots,6$, and F3 gave NNPN for $m=0,\ldots,6$. U also agreed for $m=0,1,2$. The earlier M1/M2 runs extend through $m=12$ for F1 and F3 and $m=11$ for F2. K was used up to width 21.

At line 121 replace `Seam table` by `Selected seam moves` to match §2. The cylinder control at 105 points to a real item, C1M at `dist/tog/supp/s14.tex:28,78`. C3, D, the cylinder control and the randomized L2/L3 tests are supplementary checks; no theorem step assumes their sampled regularity.

### §6 — theorem

**PROVED given C1 and C2 — `s15_note5.md:125–127`.** For $m\ge5$ the rooted reduced-game isomorphism preserves move ownership, K-children and winning T-options, so it preserves both starters' outcomes at every heap size. C1 supplies N,N,P for 0,1,2, and Lemma 1 transfers these to the whole board. From *every* heap larger than 2, either starter may reduce the heap to 2 and leave the opponent a P-position. C2 supplies the identical small-width starting outcomes. These are exactly the outcomes of $\star2+\star h$; the displayed theorem already restricts the meaning of equality accordingly. No replacement.

### §7 and §8 — scope and self-check

**PROVED — `s15_note5.md:131–133`.** Only C1 is a finite premise of the induction for $m\ge5$; C2 handles the smaller widths. Other race rules, arbitrary addends and component-sum values are outside the theorem. At 132, **MINOR**, replace `Section S13 / Note 1 of Section S15 2b` with `Section S13 and §2b of Note 1 in Section S15`. That §2b exists at `dist/tog/supp/s15.tex:65`.

**MINOR · PROVED — `s15_note5.md:137–139`.** The C1 provenance at 137 is consistent with the two graph computations. Its 3,000 random positions included subsets with seam captures, e.p. and moving reversed pawns. Replace `on 3000 random positions with seam captures, e.p. and reversed pawns` with `on 3000 random positions, including examples with each of those features as reported in §5`. At 138 the left-file description incorrectly includes file 2. For $c=4$, the right-extending windows for centres 1 and 2 are $0..4$ and $1..5$. Replace the sentence starting `File 0 is a pattern file` with `File 0 is far in the first-move comparison. It is also the outer file of the five-file window for the central pawn on file 1. That pawn reads file 0 across the chart edge 1–0; no argument requires the view centred on 0 to be free of a seam. The central pawn on file 2 can use files 1 through 5.` Replace the last sentence at 138 with `Alternatively, in F1 and F2 one may take $c=5$ and start at $m=6$: the §5 row supplies the base graph there, the arc $1..10$ avoids its zone, and the finite signature check covers $m=5$.` At 139 replace the final sentence with `A seam-crossing e.p. capture in this comparison involves only far files. The transfer uses V1 and the same skipped-square and flag rule on both boards.` Transfer between widths under one rule cannot validate a different rule.

## Reproduction and limits

Run from the repository root. These commands use the existing environment, keep bytecode off, and run the requested checks sequentially. The first command was run in this audit. It asserts the legal chess lines and all three race settings above. The two versions of $S$ are the project's CGT engine and a separate outcome minimax; the whole-board result in this check is from the latter. The counterexample also has the direct hand verification above.

~~~sh
PYTHONPATH=. .venv/bin/python -B delegate/out/T83/check.py
~~~

For the note's published finite numbers, the following are exact reproduction commands using the existing checkers. There was no numerical discrepancy warranting a fresh Möbius computation. The C1 counts, seam table and C2 rows were compared with the existing output in `research/mobius_rings_proof/logs/` and `delegate/out/T82/`. The independent program's `reduced` and `full` commands calculate different objects.

~~~sh
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1
p=research/mobius_rings_proof
for f in F1 F2 F3; do .venv/bin/python -B "$p/verify.py" "$f" 5 5; done
.venv/bin/python -B delegate/out/T82/referee.py reduced 5 5
.venv/bin/python -B "$p/base.py"
.venv/bin/python -B delegate/out/T82/referee.py full 0 4
for f in F1 F2 F3; do .venv/bin/python -B "$p/seam_moves.py" "$f" 5; done
~~~

For the ancillary all-cuts data, cylinder control, random checks and the node-increment series, the corresponding existing evidence can be inspected without launching scans:

~~~sh
cat research/mobius_rings_n/logs/famconfirm.log
cat research/mobius_rings_proof/logs/verify_F{1,2,3}.log
cat research/mobius_rings_proof/logs/verify_F1_cylinder_control.log
cat research/mobius_rings_proof/logs/difftest{,_cover}_7_3000.log
cat research/mobius_rings_proof/logs/lemma_test_3_3000.log
sed -n '58,65p' research/mobius_rings_n/REPORT.md
~~~

To regenerate those ancillary data when needed, run the following from the root, one invocation at a time. The earlier M1/M2 family driver uses paths relative to its own directory. The referee's two archived full-game ranges concern heaps 0 through 3.

~~~sh
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1
p=research/mobius_rings_proof
for f in F1 F2 F3; do .venv/bin/python -B "$p/verify.py" "$f" 0 13; done
.venv/bin/python -B "$p/verify.py" F1 5 7 --cyl
.venv/bin/python -B "$p/difftest.py" 7 3000
.venv/bin/python -B "$p/difftest_cover.py" 7 3000
.venv/bin/python -B "$p/lemma_test.py" 3 3000
(cd research/mobius_rings_n && ../../.venv/bin/python -B famconfirm.py)
.venv/bin/python -B delegate/out/T82/referee.py full 0 7
.venv/bin/python -B delegate/out/T82/referee.py full 8 13
~~~

For the exact source wording and the numbered destinations:

~~~sh
nl -ba dist/tog/supp_src/s12a_core.tex
nl -ba dist/tog/supp_src/s15_note5.md
nl -ba dist/tog/sections/04_kings.tex | sed -n '45,85p'
rg -n '^\\textbf\{(Definition 1\.10|Theorem 1\.11|Proposition 1\.12|Theorem 1\.14|Proposition 1\.15|Lemma 2\.2|Definition 2\.6|Theorem 2\.7|What Theorem 2\.7 does not give)' dist/tog/supp/s12.tex
~~~

I accepted A.1–A.9 as directed and checked their uses here. I did not audit the proofs of the longer S12 items, rerun any Möbius searches, audit the independent authorship of the historical solvers, or inspect a rendered PDF. The implementation counts above use the documented provenance and the archived outputs. No tablebase, network service or chess engine evaluation was used. The report and its runnable check are the only deliverables.
