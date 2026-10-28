# T66 referee report: PROOF_N.md

## Five-line verdict

1. **SOUND —** H1–H7 hold for both families, conditional on the cited Lemmas 1–3 and the finite base checks.
2. **PROVED —** The cuts are valid at M: n0=18, c=4 and O: n0=19, c=5; the wall phase and colour reversal are consistent.
3. **COMPUTED-1 —** Independent reduced graphs reproduce 441 M18 nodes and 2,132 O19 nodes, with the claimed zones and NNPNN signatures.
4. **COMPUTED-1 —** Two insertion steps per family preserve every reduced node, K-edge, and T-edge.
5. **COMPUTED-1 —** Direct searches give NNPNN for all eight below-n0 cases, under both heap/EP interpretations.

## Referee review

### H1 — wall, phase, insertion, and O_n colour reversal

**PROVED —** M_n has wall files 0..n-9, with B4 on even files and W2 on odd files. For n>=18, c=4 insertion adds old file 5 (W2) and old file 4 (B4) at new files 5 and 6; the alternating phase continues, and the old tail shifts by two. O_n has wall files 1..n-9, with B7 on odd files and W5 on even files. For n>=19, c=5 insertion adds old file 6 (W5) and old file 5 (B7) at new files 6 and 7, again continuing the phase. Thus ins_4(M_n)=M_(n+2) for n>=18 and ins_5(O_n)=O_(n+2) for n>=19.

**PROVED — Cut bounds.** The required arc has ten files. The M wall has length n-8, so it contains [0,9] at c=4 exactly when n>=18. The O wall has length n-9, so it contains [1,10] at c=5 exactly when n>=19. The family starts below those bounds are handled by the separate direct searches.

**PROVED —** Colour reversal for O_n is colour swap plus rank map r -> 9-r: B7 -> W2, W5 -> B4, and B4 -> W5. It converts the wall to the W2/B4 pattern used by Lemma 2. It preserves legal moves and EP-capturability, swaps White/Black passers, and negates the game. The count race is preserved because White's distance 8-r-[r=2] becomes Black's (9-r)-1-[9-r=7]; ties also exchange the two sides. Since -*2=*2, this transfers the wall argument without asserting that the reversed core is an M_n position.

**PROVED —** The M wall begins at file 0, while file n-1 is the non-wall W5 beside it across the seam. The seam neighbour n-1 is outside the insertion arc, and neither required local window wraps across the seam. The wall lemma is used on central files 1..8 (and near-reply files 3..6), so file 0 is never treated as its moving q. At the start, B4 on file 0 is blocked by W2 on file 1; W5 on file n-1 is blocked by B7 on file n-2.

**PROVED — Exact pattern content.** T50's phrase “a wall file that still holds its starting pawn” is weaker than its local wall argument if read to permit extra pawns. Here every application uses exact one-pawn files: C1 checks the full base arc, and the zone invariant plus insertion preserves that content. The needed stronger condition is established; defining “pattern file” explicitly this way would make the note clearer.

### H2 — wall moves, captures, and en passant

**PROVED —** In an exact B4/W2 wall window, W2's ordinary capture targets are rank 3, empty because its neighbours are B4 on rank 4; B4's capture targets are rank 3, empty because its neighbours are W2 on rank 2. A W2 single step remains blocked by adjacent B4 pawns ahead. After its double step to rank 4, an adjacent B4 can capture it en passant, so the mover's pawn is not passed under the adopted EP-aware test. A B4 step to rank 3 remains blocked by an adjacent W2 on rank 2. If a live flag lets B4 capture a just-moved W2, its other adjacent W2 still blocks the resulting B4. Thus the moving side has no passer after any wall move.

**PROVED —** The B7/W5 wall is the colour/rank mirror. Its ordinary capture targets are rank 6 and empty. A B7 single step to 6 is blocked by adjacent W5 pawns on rank 5; after its double step to 5, those pawns can take en passant. A W5 step to 6 is blocked by adjacent B7 pawns on rank 7. If an eligible EP capture occurs, the other pattern neighbour still blocks the mover's pawn. Lemma 2(a) therefore applies even when a flag protects the pawn of the side not to move; Lemma 2(b)'s no-flag premise holds on the central windows used here.

### H3 — both ends of the Lemma-3 arc

**PROVED —** At n=n0+2t, the insertion proof's pattern arc is [c-4,c+5+2t] and its central files are [c-3,c+4+2t]. The left endpoint uses window [j-1,j+3]=[c-4,c]; the right endpoint uses [j-3,j+1]=[c+1+2t,c+5+2t]. Both lie inside the exact pattern arc, including at the wall ends.

**PROVED —** For M18, central endpoints j=1 and j=8 have windows 0..4 and 5..9. For M20, endpoints 1 and 10 have windows 0..4 and 7..11. At the left, W2's single move to rank 3 can be captured by file-0 B4; its double step can be taken there en passant. File-2 W2 remains blocked by file-3 B4. The right endpoint is B4 on file 8 (then 10), with its required left-facing window entirely in the wall.

**PROVED —** For O19, endpoints j=2 and j=9 have windows 1..5 and 6..10. For O21, endpoints 2 and 11 have windows 1..5 and 8..12. The left W5 has B7 neighbours on files 1 and 3; the right B7 has W5 neighbours on files 8 and 10. Its double step is EP-capturable. None of these windows uses non-wall file 0. Lemma 2(b) therefore makes every central move L or P, including both endpoints, at every inducted size.

**COMPUTED-1 —** The independent local scan found no T/K central move. At M18, files 1 and 8 have 441L+441P and 441P moves, respectively. At O19, files 2 and 9 have 2,132P and 4,264P moves. These finite counts are sanity checks; the all-n conclusion follows from the hand window containment and Lemma 2(b).

### H4 — no passer and no initial flag

**PROVED —** The starts have no EP flag because no pawn has moved. In M_n, wall B4 pawns are blocked by adjacent W2 on rank 2, and W2 by adjacent B4 on rank 4. The eight tail pawns are blocked, in order, by: B6_(n-8) <- W2_(n-7), W2_(n-7) <- B6_(n-8), W3_(n-6) <- B6_(n-5), B6_(n-5) <- W3_(n-6), B7_(n-4) <- W3_(n-3), W3_(n-3) <- B7_(n-2), B7_(n-2) <- W5_(n-1), and W5_(n-1) <- B7_(n-2). Each blocker is on the same or an adjacent file and ahead in the blocked pawn's direction.

**PROVED —** In O_n, wall B7 pawns are blocked by adjacent W5 pawns, and W5 by adjacent B7. The non-wall B4 on file 0 is blocked by W2 on file n-1 across the seam. The tail is blocked by B7_(n-8) <- W5_(n-9), W3_(n-7) <- B7_(n-8), B7_(n-6) <- W3_(n-7), B6_(n-5) <- W3_(n-4), W3_(n-4) <- B6_(n-5), W2_(n-3) <- B6_(n-2), B6_(n-2) <- W2_(n-1), and W2_(n-1) <- B4_0 across the seam (also B6_(n-2)). Thus both starts are nonterminal.

**COMPUTED-1 —** Every node in both independently rebuilt base reduced graphs has neither a live EP flag nor a passer. Lemma 3's view correspondence preserves these conditions under insertion.

### H5 — race rule

**PROVED —** Lemma 2(a) does not compare promotion distances: it shows the moving side has no passer after a wall move. Lemma 3 preserves the exact passed-pawn set, colour, rank, and EP protection, so it preserves terminal outcomes under count (and any race rule based only on those data and the side that just moved). The computed value is specifically for count; no other race rule is claimed.

### H6 — invariant and induction

**COMPUTED-1 —** The base changed-file zones are M18: {10,11,12,13,14,15,17} and O19: {0,12,13,14,15,16,17,18}. They are disjoint from arcs 0..9 and 1..10, respectively, so every arc file has exactly its starting one-pawn content in every base node. The general zones M_n={n-8..n-3,n-1} and O_n={0} U {n-7..n-1} map to their n+2 zones. M’s zone lies entirely right of c=4 and shifts by two; O’s file 0 stays fixed while its tail zone lies right of c=5 and shifts by two.

**PROVED —** If the invariant holds at n, each reduced node is nonterminal and flag-free, and its ten-file arc is exact pattern. Lemma 3 maps the K-children and T-options; insertion maps the start and changed zone. Induction on reduced-graph distance then gives the inserted graph at n+2. Its K-nodes remain flag-free and agree with the new start outside the shifted zone. This proves the induction for every even n>=18 in M and every odd n>=19 in O. The finite graph comparisons below check the first two steps; they do not replace this hand induction.

### H7 — meaning of the *2 value

**COMPUTED-1 —** Both base reduced graphs have signature NNPNN for heaps h=0,1,2,3,4. Thus G+*2 is P and the other four tested sums are N. Lemma 1 transfers these outcomes to the whole-board game.

**PROVED —** For any 5<=h<256, the heap move *h -> *2 reaches the P-position G+*2, so G+*h is N. This agrees with *2+*h, which is N for h!=2 and P for h=2. This proves equivalence against nim heaps in the stated range, not against arbitrary game addends.

## Independent finite checks

**COMPUTED-1 —** The checker in independent.py is a standalone standard-library implementation of cylindrical pawn moves, live en-passant rights, EP-aware passer detection, the count race, whole-board minimax, and K/T reduced graphs. It imports no myeng.py, rg, or cylcgt code.

**COMPUTED-1 — Base graphs.** The single reproduce command below emits each entry.

| Family/base | Nodes | K-edges | T-edges | Changed zone | No flag / no passer | Signature h=0..4 |
|---|---:|---:|---:|---|---|---|
| M18 | 441 | 1,128 | 428 | {10..15,17} | yes / yes | NNPNN |
| O19 | 2,132 | 6,352 | 2,680 | {0,12..18} | yes / yes | NNPNN |

**COMPUTED-1 — Insertion checks.** Each row is a bijection on nodes preserving the complete K- and T-edge sets.

| Family | Step | Nodes both sides | K-edges both sides | T-edges both sides | Signature both sides |
|---|---|---:|---:|---:|---|
| M | 18->20 | 441 | 1,128 | 428 | NNPNN |
| M | 20->22 | 441 | 1,128 | 428 | NNPNN |
| O | 19->21 | 2,132 | 6,352 | 2,680 | NNPNN |
| O | 21->23 | 2,132 | 6,352 | 2,680 | NNPNN |

**COMPUTED-1 — Direct base cases.** Recursive whole-board minimax searched the original pawn game plus heaps h=0..4, with no reduced-game poison pruning. expire expires a pending EP right on a heap move; keep preserves it. State counts are memoized (position, side, heap) states for each run.

| Family | n | expire signature / states | keep signature / states |
|---|---:|---:|---:|
| M | 10 | NNPNN / 55,990 | NNPNN / 55,990 |
| M | 12 | NNPNN / 147,595 | NNPNN / 147,595 |
| M | 14 | NNPNN / 265,319 | NNPNN / 265,319 |
| M | 16 | NNPNN / 405,443 | NNPNN / 405,443 |
| O | 11 | NNPNN / 318,016 | NNPNN / 318,016 |
| O | 13 | NNPNN / 741,189 | NNPNN / 741,189 |
| O | 15 | NNPNN / 1,433,359 | NNPNN / 1,433,359 |
| O | 17 | NNPNN / 2,689,761 | NNPNN / 2,689,761 |

## Limits and reproduction

**PROVED —** The all-size theorem is conditional on the cited reduction, wall, and insertion lemmas (T50 Lemmas 1–3 and the written-out reply correspondence in PROOF.md §2b). This review checked their hypotheses for these families and independently recomputed the requested finite data. The computed base facts remain finite computer checks; no claim is made for the component-sum model, other race rules, or arbitrary game addends.

**COMPUTED-1 —** Exact reproduce command from the project root; it writes only the log in this task directory:

~~~sh
env PYTHONPATH=. .venv/bin/python -u research/ring_n_check/independent.py > research/ring_n_check/independent.log 2>&1
~~~

**COMPUTED-1 —** The environment denied nice -n 15 with “operation not permitted”; the successful run used one process at a time without priority adjustment. The prior-report reference to research/ring_n_plus_2_check/Q/ has a lowercase directory here (q/) and no REPORT.md; the top-level referee report contains its Q-family review. This did not affect the checks above.
