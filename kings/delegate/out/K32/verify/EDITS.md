Replacement edits from the second K32 referee (2026-10-28). They replace the four blocks of `kings/delegate/out/K32/EDITS.md` (and of `verify/EDITS_referee1.md`, the first referee's copy, which has the same four blocks); apply these four INSTEAD of those, not as well.
The mathematics is confirmed and the OLD text is unchanged. The changes are small: (i) "equals a number" is defined where the stops are defined; (ii) a remark in (R2) that equal finite number games are interchangeable in a sum; (iii) the literal count of 1,213 is said to be the λ form only (the ρ form has another 1,213); (iv) "finite" RS for the literal form; (v) the second referee's reproduction is added to the data paragraph; (vi) tags and the list of implementations.

### EDIT Proposition 3.9prime: reserves against Siegel's stops (after Proposition 3.9)
<<<<<<< OLD
(The same table was computed by K21's solver and by the referee's `ref.py`, B = 4: CHECKED-2. For over and under these are also Λ and P, the node 0 inside them having reserves (0, 0).)
=======
(The same table was computed by K21's solver and by the referee's `ref.py`, B = 4: CHECKED-2. For over and under these are also Λ and P, the node 0 inside them having reserves (0, 0).)

**Proposition 3.9′ (reserves and Siegel's stops). PROVED from the two standard facts (R1) and (R2) below, which are KNOWN and were not re-derived here** (new, K32, 2026-10-27; re-derived from (R1) and (R2) by two K32 referees, 2026-10-28, the second of whom also re-ran every check from scratch; revised after the second K32 referee, 2026-10-28: definition of "equals a number", the interchange remark in (R2), the literal counts; answers §8 item 4(d) and corrects the form of the conjecture).
Let y be a node of a finite terminal-free stopper. Its stops LS(y), RS(y) ∈ ℝ ∪ {±∞} are Siegel's [S, ch. VI] (KNOWN; the chapter reference is from memory and was not checked): if y equals a number x (that is, y − x is a second-player win: both players lose moving first) then LS(y) = RS(y) = x; otherwise LS(y) is the maximum of RS(y^L) over the Left options and RS(y) is the minimum of LS(y^R) over the Right options, with max ∅ = −∞ and min ∅ = +∞.
Write y + C for y with C Left tokens, as in the conventions above (C an integer ≥ 0). Two standard facts compare the right stop with the number −C:
- (R1) (KNOWN) If Left wins y + C moving second, then RS(y) ≥ −C.
- (R2) (KNOWN) If RS(y) > −C, then Left wins y + C moving second.

(R1) and (R2) say that RS(y) is the supremum of the numbers x for which Left wins y − x moving second, read at the integers x = −C: (R1) is the case x = −C, and (R2) is the fact that adding a positive number keeps a Left win second (the proof of Lemma 3.8a works for any two components; a finite number game may be replaced by an equal one inside a sum, which is KNOWN). The imported fact is therefore that the recursion above computes this supremum for a stopper (Siegel). It is not re-derived here. The data below test it.

Let u = −RS(y). Then:
- (a) λ(y) < ∞ iff RS(y) > −∞. If RS(y) = +∞, then λ(y) = 0.
- (b) If u is finite, then max(0, ⌈u⌉) ≤ λ(y) ≤ max(0, ⌊u⌋ + 1). So λ(y) = max(0, ⌈u⌉) unless u is an integer ≥ 0, and then λ(y) ∈ {u, u + 1}.
- (c) (mirror) Let v = LS(y). Then ρ(y) < ∞ iff LS(y) < +∞; if LS(y) = −∞ then ρ(y) = 0; and if v is finite, max(0, ⌈v⌉) ≤ ρ(y) ≤ max(0, ⌊v⌋ + 1).
- (d) The conjecture of §8 item 4(d), "λ = ⌈−RS⌉ or one more", is true only after the clamp at 0 in (b). It fails exactly when RS(y) ≥ 2 is finite, because λ ≥ 0: the integer 2 = {1∣} has RS = 2 and λ = 0.
- (e) At an integer boundary the stops do not decide. For RS = LS = 0 all four pairs (λ, ρ) ∈ {0, 1}² occur: 0 gives (0, 0), over and ↑ give (0, 1), under and ↓ give (1, 0), * gives (1, 1). For u = m an integer ≥ 0, λ(y) = m iff Left wins y + m second.
- (f) For a terminal-free stopper S: all reserves are finite on reach(S) iff RS > −∞ and LS < +∞ at every node of reach(S). Then Λ(S) ≤ max(0, ⌊−m⌋ + 1) with m = min RS over reach(S) (Λ(S) = 0 if m = +∞), and P(S) ≤ max(0, ⌊M⌋ + 1) with M = max LS over reach(S) (P(S) = 0 if M = −∞). So the B of Corollary 3.8b can be read off the stops.

*Proof.* (a), (b). Let λ(y) = C < ∞. Left wins y + C second, so RS(y) ≥ −C by (R1), that is C ≥ u. Hence RS(y) > −∞, and since C is an integer ≥ 0, C ≥ max(0, ⌈u⌉).
Conversely let RS(y) > −∞. If RS(y) = +∞, then RS(y) > 0 and (R2) with C = 0 gives λ(y) = 0. If u is finite, put C = max(0, ⌊u⌋ + 1). Then C > u (if C = 0 then ⌊u⌋ ≤ −1, so u < 0), so RS(y) = −u > −C, and (R2) gives λ(y) ≤ C.
If u is not an integer, then ⌈u⌉ = ⌊u⌋ + 1 and the two bounds agree. If u is an integer < 0, both bounds are 0. If u is an integer ≥ 0, the bounds are u and u + 1.
(c) Swap the Left and Right options of y. The mirror game ȳ is a stopper, λ(ȳ) = ρ(y) because the rules are symmetric, and RS(ȳ) = −LS(y) because the recursion is symmetric and the number x goes to −x. Apply (a) and (b) to ȳ.
(d) If RS(y) ≥ 2 is finite, then ⌈−RS⌉ + 1 ≤ −1 < 0 ≤ λ. If RS(y) < 2 then u > −2: for ⌈u⌉ = −1 the set {−1, 0} contains λ = 0 (u < 0), and for ⌈u⌉ ≥ 0, (b) gives ⌈u⌉ ≤ λ ≤ ⌊u⌋ + 1 ≤ ⌈u⌉ + 1.
(e) The last sentence: the set of C with "Left wins y + C second" is upward closed (Lemma 3.8a), so λ(y) ≤ m iff Left wins y + m second, and λ(y) ≥ m by (b). The four pairs, by hand, with ↑ = {0 ∣ *} and * = {0 ∣ 0}. 0: (0, 0) is trivial. over and under: Proposition 3.9. *: in * + 0 Right moves to 0 and Left has no move, so λ ≥ 1; in * + 1 Right's only move leaves 0 + 1, Left plays the token and Right is stuck, so λ(*) = 1; ρ(*) = 1 by symmetry. ↑: in ↑ + 0 Right's only move is to *, Left answers * → 0 and Right is stuck, so λ(↑) = 0; with Left to move at ↑ she plays to 0 and wins, so ρ(↑) ≥ 1, and in ↑ − 1 her only move is to 0 − 1, after which Right moves and she is stuck, so ρ(↑) = 1. ↓ is the mirror image of ↑. The stops of all six games are 0 (KNOWN for the infinitesimals ↑, ↓, *; for over and under the recursion gives LS = RS(0) = 0 and RS = LS; also computed below).
(f) (a) and (c) at every node, and both bounds are monotone in RS(y) and LS(y); Λ(S) and P(S) are the maxima over reach(S). ∎

*Data (K32; `kings/delegate/out/K32/summary.json`, `logs/`, `scripts/`; the first K32 referee's reproduction is in `kings/delegate/out/K32/verify/` (`scripts`, `logs`), the second referee's in `kings/delegate/out/K32/verify/mine/` (report: `kings/delegate/out/K32/VERIFY.md`)).* Two C implementations by K32 (A: token DP and a profile against dyadic numbers on a 1/16 grid; B: a generic sum solver, explicit number games on a 1/32 grid, explicit token chains) agree on λ, ρ, LS, RS at every node of every graph tested, and the stops from Siegel's recursion agree with the supremum of the numbers x with Left winning y − x (moving first, second) in every case (0 mismatches). The corrected relation (b), (c) holds in all of them. Every rooted stopper with at most 4 nodes (3, 43, 4,281 and 2,169,427 isomorphism classes on 1 to 4 nodes, 2,173,754 in all): 0 violations; the literal form for λ fails in 1,213 of them (3 on 3 nodes, 1,210 on 4 nodes), exactly those with finite RS ≥ 2, and the mirror form for ρ fails in another 1,213, exactly those with LS ≤ −2 (2,426 classes in all). 105,000 random stoppers of 5 to 8 nodes (620,000 nodes): 0 violations of (b), (c); the literal form fails only for RS ≥ 2 (8,873 nodes for λ, 8,779 for ρ at LS ≤ −2). The named games: on (0, ∞), off (∞, 0), over (0, 1), under (1, 0), 0 (0, 0), * (1, 1), ↑ (0, 1), ↓ (1, 0), 1 (0, 1), 2 (0, 2), −1 (1, 0), 1/2 (0, 1), ±1 (2, 2), {on∣off} (∞, ∞), and K21's three-node stopper of the tempo-regime counterexample (∞, ∞); stops are the values. The first K32 referee reproduced this with a third C implementation and a Python one, written without reading K32's solvers: the class counts 3, 43, 4,281 (own labelled enumeration, root fixed, canonical under permutations of the other nodes) and 2,169,427 (own enumeration of all 2^32 labelled graphs on 4 nodes, 12,958,975 of them rooted stoppers), the 1,210 literal violations on 4 nodes, and all 48 signatures (λ, ρ, LS, RS) with identical counts; 0 violations of (b), (c) and 0 grid mismatches with the supremum characterisation on every node of every 4-node class (8,677,708 nodes); 0 violations on random stoppers of 4 to 8 nodes, with the literal form failing exactly when RS ≥ 2 or LS ≤ −2; a Python solver with a different data layout agreed on all 5,200 nodes of 1,100 random stoppers of 4 to 6 nodes. CHECKED-2. A second K32 referee wrote a new C checker and a new Python checker from the definitions only (neither K32's solvers nor the first referee's code was read) and reproduced the class counts 3, 43, 4,281 and 2,169,427 (12,958,975 labelled rooted stoppers on 4 nodes), the same 48 signatures with the same counts, the 1,210 literal violations of the λ form on 4 nodes, and 0 violations of (b), (c) at all 8,677,708 nodes of the 4-node classes. A grid of 1/16 with |x| ≤ 9 gives the same result as 1/8 with |x| ≤ 6 on every 4-node class, so the grid is not a cut-off. On 1,100,000 random stoppers of 5 to 8 nodes (7,000,000 nodes) there were 0 violations of (b), (c) and 0 mismatches between Siegel's recursion and the supremum characterisation; the literal form failed exactly when the finite stop was ≥ 2 (ρ: ≤ −2) at every node of every class of at most 4 nodes and in a random run of 100,000 six-node stoppers. The Python program (token DP for λ and ρ, naive fixpoint sweeps, exact fractions) agrees with the C program on every node of 2,100 random stoppers of 2 to 7 nodes (8,850 nodes), and an own Python count gives the class counts 3, 43, 4,281. (R1) and (R2) held at every node tested, the integers x = −C included; they are KNOWN and not proved here. The exhaustive search stops at 4 nodes: 5 nodes were not enumerated (the class counts grow by factors of 14, 100 and 507 from 1 to 4 nodes, so 5 nodes means billions of classes, an extrapolation).
>>>>>>> NEW


### EDIT Section 8 item 4(d): answered
<<<<<<< OLD
(d) the relation between (λ, ρ) and
     Siegel's stops (CONJECTURE, untested: λ(S) = ⌈−RS(S)⌉ or one more, for a terminal-free stopper with finite reserve).
=======
(d) the relation between (λ, ρ) and
     Siegel's stops: ANSWERED (new, K32, 2026-10-27; re-derived by two K32 referees, 2026-10-28; Proposition 3.9′). The conjecture was true only after a clamp at 0: λ(S) = max(0, ⌈−RS(S)⌉) or one more,
     and "one more" only if −RS(S) is an integer ≥ 0; λ(S) = ∞ iff RS(S) = −∞; ρ is the mirror with LS. The literal form fails whenever the finite stop RS(S) ≥ 2 (the integer 2 has λ = 0) and is undefined for infinite RS.
     PROVED from the standard comparison of the stops of a stopper with numbers (KNOWN, not re-derived here); the corrected relation holds on every rooted stopper with at most 4 nodes
     and on random stoppers of 4–8 nodes (CHECKED-2). Still open: a derivation of the comparison itself from the recursive definition of the stops inside this document.
>>>>>>> NEW


### EDIT Status table: new row P3.9prime after the P3.9-P3.10 row
<<<<<<< OLD
the reserve table CHECKED-2 (two solvers), the draw counts COMPUTED-1 |
=======
the reserve table CHECKED-2 (two solvers), the draw counts COMPUTED-1 |
| P3.9′ | Reserves against Siegel's stops: for a node y of a finite terminal-free stopper, λ(y) = ∞ iff RS(y) = −∞, otherwise max(0, ⌈−RS(y)⌉) ≤ λ(y) ≤ max(0, ⌊−RS(y)⌋ + 1) (one more only when −RS(y) is an integer ≥ 0); ρ is the mirror with LS. The conjecture of §8 item 4(d) holds after the clamp at 0 and fails literally for RS ≥ 2 | PROVED from the standard comparison of stops with numbers (new, K32, 2026-10-27; re-derived by two K32 referees, 2026-10-28; the comparison is KNOWN, not re-derived); the corrected relation holds on all 2,173,754 rooted stoppers with at most 4 nodes (both referees re-enumerated them) and on random stoppers of 2–8 nodes, CHECKED-2 (K32's two C solvers and a C and a Python program from each of the two referees; no violation) |
>>>>>>> NEW


### EDIT Referee table: row for P3.9prime after the P3.9, P3.10 row
<<<<<<< OLD
| P3.9, P3.10 | PROVED (new, K21, 2026-10-27; re-derived by the K21 referee); the reserve table CHECKED-2, the draw counts COMPUTED-1 | K21 referee |
=======
| P3.9, P3.10 | PROVED (new, K21, 2026-10-27; re-derived by the K21 referee); the reserve table CHECKED-2, the draw counts COMPUTED-1 | K21 referee |
| P3.9′ | PROVED from the KNOWN comparison of stops with numbers (new, K32, 2026-10-27; revised after the second K32 referee, 2026-10-28): the reduction was re-derived step by step by both K32 referees; the comparison itself, (R1) and (R2), is Siegel's theorem and was not re-derived. The conjecture of §8 item 4(d) is FALSE as worded for RS ≥ 2 and TRUE after the clamp at 0. CHECKED-2, exhaustive to 4 nodes (re-enumerated by both referees: 2,169,427 classes on 4 nodes, 1,210 literal violations) | K32 referees 1 and 2 |
>>>>>>> NEW
