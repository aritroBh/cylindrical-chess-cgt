# L14 · Cold referee report on the Lean checks

## Five-line summary

1. **CHECKED-2.** All 20 unflagged census groups match: 231,071 records, 459,443 placements, 6,724 zeros, 4,042 stars and no higher nimber. Allowing a live e.p. right after a double step from an open unflagged predecessor adds 22,290 records.
2. **PROVED / CHECKED-2.** L5 establishes the eighth for every race function in the sum specification. The root and threat checks give a valid counterexample to hereditary sum safety.
3. **CHECKED-2.** The tested wall rings, the named ten- and eleven-file rings and the Möbius controls give the expected heap outcomes. Lean's finite family computations leave the insertion induction and its reduced-graph hypotheses to the supplement.
4. **CHECKED-2.** Independent compulsory-capture play gives the Dawson ring Grundy values through width 20. The Lean Grundy comparison stops at 16. An independent complete one-step cut test passes on the six-file, eight-rank, two-pawn family.
5. **PROVED / CHECKED-2.** The heap agreement test accepts an unknown for a loss, though all stricter replays pass. Wide search gives a wrong winner on a valid 1,005-rank board. The eleven-file, twelve-pawn Lean theorem checks the sum only; a new whole-board check confirms *3.

## E · Census, reviewed first

**CHECKED-2 — agrees on the stated numbers for unflagged starting diagrams.** The default is the count race rule with the e.p.-aware passed test and ordinary kings frozen out. The numerical test is for the component sum with winning components replaced by signed 256. The zero and star columns count symmetry **records**. Multiplicity expands only the placement column. The paper prints the totals, without the following group breakdown, at `dist/tog/sections/06_atlas.tex:3–9` and `dist/tog/sections/08_star2.tex:35–42`. Each tuple below is (records, placements, zeros, stars). Both programs give zero higher nimbers in every row. Reproduce with **E** below.

| Width | Pawns | Independent canonical games | Lean `CensusData.expected` |
|---:|---:|---|---|
| 1 | 2 | 15, 15, 7, 4 | 15, 15, 7, 4 |
| 1 | 3 | 40, 40, 8, 0 | 40, 40, 8, 0 |
| 1 | 4 | 60, 60, 18, 6 | 60, 60, 18, 6 |
| 1 | 5 | 48, 48, 20, 4 | 48, 48, 20, 4 |
| 1 | 6 | 16, 16, 16, 0 | 16, 16, 16, 0 |
| 2 | 2 | 15, 30, 5, 3 | 15, 30, 5, 3 |
| 2 | 3 | 150, 300, 4, 0 | 150, 300, 4, 0 |
| 2 | 4 | 755, 1 495, 70, 37 | 755, 1 495, 70, 37 |
| 2 | 5 | 2 360, 4 720, 90, 30 | 2 360, 4 720, 90, 30 |
| 2 | 6 | 5 188, 10 336, 200, 80 | 5 188, 10 336, 200, 80 |
| 3 | 2 | 0, 0, 0, 0 | 0, 0, 0, 0 |
| 3 | 3 | 70, 110, 4, 0 | 70, 110, 4, 0 |
| 3 | 4 | 1 365, 2 565, 140, 84 | 1 365, 2 565, 140, 84 |
| 3 | 5 | 10 476, 20 402, 222, 98 | 10 476, 20 402, 222, 98 |
| 3 | 6 | 51 089, 100 843, 1 396, 673 | 51 089, 100 843, 1 396, 673 |
| 4 | 2 | 0, 0, 0, 0 | 0, 0, 0, 0 |
| 4 | 3 | 0, 0, 0, 0 | 0, 0, 0, 0 |
| 4 | 4 | 1 035, 2 025, 198, 152 | 1 035, 2 025, 198, 152 |
| 4 | 5 | 16 054, 32 108, 290, 158 | 16 054, 32 108, 290, 158 |
| 4 | 6 | 142 335, 284 330, 4 036, 2 713 | 142 335, 284 330, 4 036, 2 713 |
| **All** | **2–6** | **231071, 459443, 6724, 4042** | **231071, 459443, 6724, 4042** |

**PROVED — root domain.** At fixed colour counts, `lean/CylChess/Census.lean:21–35,47–67` enumerates ordered sublists of distinct squares. It rejects overlap, requires both extreme files, permits internal gaps, and fixes the white-list length before concatenating the sorted armies for lexicographic comparison. Reflection is an involution, so each orbit contributes once and a fixed point has multiplicity one. Filing by exact span removes duplicate translations. The strict order's empty-list case would be unsuitable as a general lexicographic order on unequal-length lists, but all key comparisons here are on equal lengths. A white pawn on rank 7 or black pawn on rank 2 would already be passed on a diagram whose pawns are all on ranks 2–7. The rank restriction in the generator therefore loses no eligible unflagged diagram. Using a four-file flat board even for smaller spans is harmless because no pawn can enter a vacant exterior file.

**CHECKED-2 — the missing root qualifier matters.** `Census.lean:61–63` and `lean/CylChess/Game.lean:33–37` always set the root flag to `none`. Main-text §Atlas says “every such position” without stating this restriction. From W a2 b2 / B a4 a7, White can play b2–b4. Both the resulting diagram with a usable e.p. right and the same diagram without the right are open in the default setting. Without the right its value is zero. With it Black can take en passant and wins whoever starts. The Lean specification returns `some false` for White and `some true` for Black moving first. Reproduce with **F**. The census remains appropriate for starting diagrams stipulated to have no right. The separate whole-board scan of 793,299 placements and its birthday bound at `08_star2.tex:40–42` are outside L10.

**CHECKED-2 — size of the omitted subclass.** I extended the audit to roots with an active flag immediately after a legal double step from an open, unflagged predecessor in the census domain, requiring the flagged successor itself to be open. The Python enumerator works backwards from a victim/capturer pair, checks both traversed squares, reconstructs the predecessor and verifies the forward move. A comparison written separately in Lean starts from `Census.records`, plays moves forwards, and quotients double steps from a mirror-symmetric predecessor by the mirror of the flagged file. The flag determines the preceding unflagged diagram uniquely. Both count these **additional** mirror/translation records, using the aware test throughout. No one-file position can have a usable e.p. flag. The restriction on the predecessor is explicit; these numbers need no claim about reachability from the standard chess initial array. Reproduce with **F+**.

| Width | Extra records | Extra zeros | Extra stars | Higher nimbers |
|---:|---:|---:|---:|---:|
| 2 | 544 | 14 | 32 | 0 |
| 3 | 6,548 | 38 | 74 | 0 |
| 4 | 15,198 | 128 | 154 | 0 |
| **Total** | **22,290** | **180** | **260** | **0** |

**CHECKED-2 — independent method.** `census.py` starts from uncoloured square subsets on ranks 2–7 and then assigns colours. It implements steps, double steps, captures, usable e.p., blocker tests, the front-pawn distance and tie against the last mover. It constructs ordinary partizan option trees, re-splits open children, adds the resulting games and uses actual signed-integer game trees as terminals. It compares directly in both directions with zero and star. For the independent all-nimber result it canonicalizes followers, bypasses reversible moves, removes dominated moves and recognizes a nimber by identical option lists containing exactly the lower nimbers. The two zero/star tests agree on every record. This route uses no finite/cofinite heap encoding, no numerical heap cutoff, and no project data as inputs. Only the post-computation comparison reads `CensusData.lean`. The residual 220,305 unflagged records are non-nimbers. Internal gaps matter: even width 3 with four pawns includes 120 reflected records with an empty interior file. Agreement here is on every **group tally**. We did not align two per-position value databases.

**PROVED — why the all-heaps recurrence works.** Write A and B for the two sets of heaps admitting a winning board move. A child contributes the complement of the opponent's winning set. At heap j a side can also win by lowering to any earlier heap where its opponent loses. `lean/CylChess/Heaps.lean:32–46,55–70,75–105` implements union, complement, and exactly that strict-prefix test. Put t equal to the larger exception-bit length. From t on, A and B are constant. Any win at t persists, since either its board option persists or its earlier heap witness persists. Any loss at t makes the opposite side win at every index from t+1. If a side has never lost through t, it won at t and hence never loses later. Thus all future prefix tests are determined at t+1. The returned tail and the finite/cofinite representation are correct for **every** heap, and the extra iterations are sufficient. A double loss can occur at most once because both sides can move back to it at all larger heaps. This rules out a lost mask containing both bits 0 and 1. This is a referee's mathematical argument for the recurrence. A Lean theorem relating `Heaps.sets` to specification outcomes for arbitrary inputs is still missing.

**PROVED — memoization and the final theorem.** `Heaps.lean:72–109` uses the normalized list of components as key for both sides' sets. The environment is fixed for the lifetime of each memo. Integer cancellation and dropping zero in `lean/CylChess/Search.lean:29–36` preserve the ordinary sum. Fuel failure or an unresolved race propagates, and only definite results enter the memo. This can change which calls finish at a specified small fuel. `Census.lean:98–112` counts failures explicitly. Its comment at lines 76–79 describes an “odd” category while the actual final branch includes the ordinary empty lost set. `CensusData.lean:14–30` contains all 20 distinct keys. `Claims/L10_CensusSmall.lean:19` and `L10_CensusBig.lean:11` recompute the groups with compiled code. `L10_Census.lean:15–20` proves only a length and a sum of literals by kernel reduction. A duplicate key could satisfy a length-only check in a modified table. The current table additionally passes a distinct-key and exact-coverage comparison (**L**, **E**). The code uses fuel 400, chunks of 2,000 and an empty memo for each chunk. The three genuinely empty groups are (3,2), (4,2) and (4,3).

**PROVED — weakness in the agreement test.** `lean/CylChess/HeapsAgrees.lean:21–28` compares a Boolean with `reference == some true`. For a predicted loss, both `some false` and `none` pass. On the stuck W a2 / B a3 pair at heap zero, even the reference function that always returns `none` passes. Compare directly with `some (wl.mem j)` or `some (wr.mem j)` to require a definite outcome. `Heaps.lean:18–20` also describes the wrong comparison ranges and file. The actual tests in `HeapsAgrees.lean:30–46` use heaps 0–3 against the specification and 0–7 against the fast search. **L** contains the counterexample and the stricter replay.

## A · Corrections

**PROVED / CHECKED-2 — the eighth says what the paper says.** `dist/tog/sections/07_targets.tex:54–56` matches the unflagged W a2 b2 b3 / B a5 a6 b6, `L5_Eighth.lean:28–33`, on the ordinary 8×8 board. `Claims/Common.lean:7–21` supplies the settings and fuel. `Game.lean:66–73,161–166` uses the canonical dyadic tree and tests both starters against its negative. `Claims/L5_EmptyTable.lean:89–110` changes only the race function. One-sided passed adjudications and move generation stay fixed. Its order on partial answers allows any refinement of unknown and requires a known answer to stay equal. A definite win has a winning witness and a definite loss requires all moves to lose. The pointwise option-list proof and fuel induction at lines 65–86,112–146 therefore lift the empty-table result to **every** position-and-last-mover race function, including partial functions. The final theorem at lines 169–175 depends on the compiled nine-setting empty-table result, not on completeness of a race-key list. The default base separately has `decide +kernel` at lines 156–159. Race-rule names contribute three copies per e.p. treatment after replacement. Our independent search returned two losses for the position plus −1/8 with every race unknown under off, textbook and aware (**A/D**). The two occupied files cannot split into two nonempty blocks, so the whole-board shortcut for a terminal against this small dyadic addend is exact.

**PROVED — open roots.** `Claims/RootsOpen.lean:20–33` uses `decide` for both pass tests on A and B, G and its file mirror in all nine settings, and X on the cylinder in its claimed off/count setting. It does not assert reachability from the ordinary starting array. The comment at lines 14–16 generalizes too far: L10 screens in `Census.records`; L7 controls use `signature`, which lacks the root guard that `starTest` has. The listed controls are concrete positions.

**PROVED / CHECKED-2 — non-HSS witness.** `dist/tog/sections/05_sums.tex:31–35,55–59` explicitly allows either colour in any order and counts a race as both threats. On the eight-file cylinder, off/count, h5–h6 and a7×h6 across the seam leave exactly the b–d and f–h components. In the former d4–d5, c7–c5 makes White alone passed. In the latter f7–f5–f4–f3 by Black makes Black alone passed. The alternative h6–h5–h4, g3×h4 makes both passed. `Claims/L6_NotHSS.lean:37–41,73–94` checks a legal successor and open source at each step, and tests the endpoints separately. All four theorems use kernel `decide`. These witnesses imply failure of the published definition. Lean does not package them as `¬ HSS X` for a general formal predicate. Our board replay reproduced all three endpoint passer pairs and the open entry line (**A/D**). The earlier model-outcome assertions are separate at `L6_SumCounter.lean:20–40`; the whole board also has kernel checks for both starters, while the 256-point sum result uses fast search.

## B · Rings

**PROVED — the intended whole-board game.** `dist/tog/supp/s13.tex:7–23` and `lean/CylChess/SearchWide.lean:64–72` agree on an open root. Each pawn move is adjudicated on the entire successor board, both passers invoke the count race, and a heap move decreases the heap while preserving the entire position, flag included. A player with no available move loses. The specification does not adjudicate a terminal root; the family tests reject such roots. `Rules.lean:181–198,220–230,268–303` flips the destination rank and pawn heading across the Möbius seam, uses the heading for home rank and distance, and tests enemies in mirrored rank coordinates. This agrees with Note 5 lines 31–37. `SearchWide.lean:118–153` partitions the pawns only to change search order. The first pass accepts any immediate win, drops terminal losses, and remembers an undefined race. Its inner `none` means a **known winning move**, distinct from the return value `none` of an exhausted search. Lines 156–198 key definite answers by the whole position (both armies, heading and flag), heap, and mover. The memo is fresh per environment. Neither the ordering hint nor fuel changes a definite truth value. A cached hit at lower fuel need not reproduce a naive fuel failure.

**PROVED — an out-of-domain counterexample and an overstated test description.** At `SearchWide.lean:76–103`, maximum/minimum enemy ranks per file implement the three strict-ahead tests on the eight-rank boards. The minimum sentinel is 1000. On a valid one-file, 1003-rank flat board with a lone Black pawn at rank 1001, `hasPassed` returns true and `passedF` returns false. `Rules.lean:66–67` imposes no height cap. There is also a genuine **wrong winner at an open root**. On a flat 5-file, 1005-rank board put W a1001 e1001 / B b1002 d1002, heap 0, Black to move. The valid root has no passer. A black capture, e.g. b1002×a1001, immediately produces a black passer. The fast test misses it and allows the other White pawn to capture. At identical fuel 10 the specification returns `some true` and the fast search `some false` (**F**, last output). This disproves unrestricted agreement, including at definite answers. All named ring claims use eight ranks. `SearchWideAgrees.lean:11–15` describes “every position reachable,” whereas lines 59–75 stop at depth two. The `wide`/naive comparison tests open cases only, heaps 0–2, both movers, and can also pass `none == none` (lines 79–88). The slower unpruned comparison is only on wall widths 5–10 and heaps 0–3 (lines 104–108). It shares the pawn rules. Reproduce with **L**.

**PROVED — which generalizations follow.** Each successful `starTest` requires definite matching outputs from both starters for every heap from 0 through 6. `WideCommon.lean:14–25` checks the actual file-list length and pawn count, so an invalid positive-width family returning an empty list cannot pass. `L7b_Mobius.lean:22–25` also checks both. All stated ranges are nonempty, with the correct parity where required. `WideLemmas.lean:24–35` proves for the specification that a loss of the other mover at k supplies a winning heap move at every h>k, with one more unit of fuel. The family results supply losses of `wide`; there is no general Lean implication turning those into `WH` losses. In ordinary game theory a double loss at k also forces N below k because those heap reductions at k all lose. Neither argument supplies induction on board width or establishes a reduced graph's flags, edges and fixed files.

**PROVED — family transcriptions and ranges.** I compared the ordered file words (including repeated pairs, multi-pawn files, and the side of the seam) at `Families.lean:20–99` with S13 lines 32–36, S14 lines 9 and 41–42, and the displayed definitions in S15 Notes 1–6. The claimed inputs match those definitions. `parseFile` at `SearchWide.lean:44–58` would accept arbitrary non-digit characters as ranks, but the concrete words contain only colour switches and valid digits. The following are the actual whole-board searches, all under aware/count with both movers. **S** below reproduces the source ranges. Each row says less than the corresponding all-width theorem.

| Families, source | Target and material | Lean range, inclusive | Comparison with the supplement |
|---|---|---|---|
| S13 odd/even walls, `L7b_Walls:23–24` | *2, n+3 | n=5–61 | Matches the direct width sweep in S13:136–139. The reduced base graphs at 17 and 16 and their insertion are separate facts. |
| N1 P, N3 R, `L7b_Walls:27–32` | *2, n+2 | even 8–60, odd 11–59 | Matches the reported direct width sweeps. N1:35 also reports heap 7. |
| S14 M and O, `L7b_OnePerFile:15–19` | *2, n | even 10–50, odd 11–49 | Covers all S14 small bases. S6:82–84 reports the families through width 60. |
| N2 Q, N3 Qo, `L7b_Star3:17–21` | *3, n+2 | even 8–40, odd 11–39 | Covers Q's direct 8–24; Qo falls short of N3:27's odd sweep through 59. |
| N4 T and S, `L7b_Star3:23–24`, `L7b_S:12–13` | *3, n+1 | even 12–40, odd 13–25 | Covers the bases 20 and 23. N4:25 also reports reduced S signatures through 41. The inserted graph is a different check. |
| N5 F1, F2, F3, `L7b_Mobius:30–34` | *2, n, n, n+1 | m=1–20, 1–20, 0–20 | Widths 10–48 even, 11–49 odd, 7–47 odd. All include m=5, beyond the N5 direct small cases. |
| N6 TT and SS, `L7b_Mobius:36`, `L7b_MobiusSS:9` | *3, n+1 | m=1–14, 0–8 | Widths 12–38 even, 11–27 odd. Both include the bases, TT(5) and SS(6). |

**PROVED — named values and minima.** The file- and rank-lists in `Claims/L7a_NamedRings.lean:22–39,70–85` match the main text at `08_star2.tex:104–110,121–126`, including the nine-pawn flat *3 and the flat seven-rank four-pawn *2 at widths 3, 4 and 5. The named cylinder M10 and O11 have separate sum and whole-board assertions. The six-pawn C3 sum has *2 in the default setting and zero in off/count; line 54 does not test selectively removing either of the two e.p. captures discussed at `supp/s06.tex:93–95`. That is a dependence on two specific legal options, stronger than globally switching e.p. off. A single component in `ring6_shape` would not by itself imply every file is occupied; here the actual pawn lists do.

**PROVED — S6 witnesses and the missing model.** `Claims/L7a_S6Rings.lean:21–56` matches the printed squares for the C4 example and colour-reversed twin, C6 *2, both example values on C7 and C8, C8 wall identity and C11 *3 (`supp/s06.tex:68–95,103–111`). Except for the wall identity these are **sum** checks. Individual named witnesses do not establish the population counts or uniqueness of all C4 seven-pawn solutions. Most importantly, `08_star2.tex:124–125` expressly calls the n+1-pawn C11 result a **whole-board** *3. The comment at `L7a_S6Rings.lean:52–53` mentions both games, yet `c11_twelve_pawn_ring_sum` calls only `sumStar`. The C11 witness is W c4 d6 e3 h3 i2 k2 / B a4 b7 d7 f7 g6 j6. The C11 cylinder does not belong to the T/S family checks (they start at 12/13), and the SS(0) strip has a different topology. **B** and **F** directly test the missing cylinder statement.

**PROVED — L11 exhausts the claimed small sum-model domains.** `RingScan.lean:20–29,40–55,64–85` enumerates all splits into two nonempty armies, excludes overlap and passers, requires every file occupied, and does not quotient rotations. Unknowns enter the failure count and are retained in the candidate list. `Claims/L11_RingMinC3.lean:22–37` shows no higher nimber below six pawns and identifies all six raw six-pawn *2 placements by mutual membership in the dihedral/colour orbit. The orbit list may repeat entries, so mutual membership is appropriate. `L11_RingMinC4.lean:16–18` excludes smaller rings on four files. Together with the two explicit seven-pawn examples it gives the C4 minimum. No separate proof here exhausts seven-pawn C4 rings to classify all minimizers, C5–C9 to certify all the claimed minima, or the Möbius minima in `08_star2.tex:131–135`. The paper also reports sum-model wall computations to n=12 (`08_star2.tex:116–119`), whereas the Lean wall-family sweep uses the whole-board game.

**CHECKED-2 — independent whole-board controls.** **B** plays out the moves from the paper and S13/Note 5 with integer bitboards for the four colour/heading classes. It keeps the e.p. flag across heap moves and resolves both starters separately. In increasing heap order 0–4, N means both starters win, P both lose, L White wins either way and R Black wins either way.

| Position | Independent | Lean or paper comparison |
|---|---|---|
| S13 wall on each cylinder 5 through 10 | NNPNN for each | `wall_rings_star2`, NNPNN |
| M10 and O11 | NNPNN each | `rings_M10_O11_star2_whole`, NNPNN each |
| Six-pawn C3 | aware/count NNPNN, off/count PNNNN | `ring6_star2`, `ring6_ep_off_zero` for S. On three cyclic files any remaining occupied files stay one component. |
| Twelve-pawn C11 whole-board witness | NNNPN | Main text says *3. **F** adds a `Wide.sigString` check separate from the published sum-only theorem. |
| Möbius F1(1) | NNPNN | `F1_star2`, NNPNN |
| Möbius F1(0), F2(0), TT(0) | RNRRR, NNRRR, LLLLL | `Mobius_controls`, identical |
  
**CHECKED-2 — the named component sums.** Our separate sum search (**B**, `sums.py`) re-splits a moved open component, retains the flags in untouched components, adds signed 256 to the net integer at a terminal and plays the heap as another summand. Both movers lose at heap 2 for M10, O11 and the aware C3 example, and at heap 0 for the off/count C3 example. These are direct tests of the sum-model equalities in `L7a_NamedRings.lean:50–62`.

**PROVED — cylinder controls have differing coverage.** `Claims/L7b_Controls.lean:17–31` tests all five characters for R9 and Qo9 (LLLLL), only heap 2 for M8/O9 (N/R), and only heap 3 for T10/S11 (L/R). The latter are sufficient counterexamples to the proposed nimber at each excluded size. No universal claim over the remaining characters is needed or established. **B** verifies that all six control roots are open, with full signatures LLLLL, LLLLL, NNNNN, RRRRR, LLNLL and NNNRR in the stated order. The positive family statements, controls, named-ring values and L11 scans all use compiled `native_decide`.

## C · Dawson's ring rule

**PROVED / CHECKED-2 — finite form of the claimed normal-play result.** `dist/tog/sections/11_dawson.tex:9–25,34–44` and `lean/CylChess/Dawson.lean:53–100` agree on a full three-rank ring, White forwards and Black backwards, mandatory captures before pushes, no double step, and loss on no move. Reaching the last rank leaves an immobile pawn. The finite absence of any such arrival is checked separately. `key` at lines 122–124 is ternary occupancy plus the turn bit, injective at fixed length. The memo never crosses boards. `mex` at line 210 scans through the list length inclusive; a missing member exists even for a list of repeated values. `gList` at lines 244–257 correctly has no split at n=2 and includes both endpoint and internal removals thereafter.

| Lean theorem(s) · Dawson.lean | What is actually established |
|---|---|
| **PROVED** `g_table`, `g_recurrence`, `ring_win_list`, 327–335 | Kernel computations of the strip table for 0–33, recurrence for 2–71, and recurrence-derived winning ring list for 3–57. Restating the recurrence over the same computed sequence is an arithmetic consistency check. |
| **COMPUTED-1** `ring_outcome`, `ring_win_range`, `ring_structure`, 337–350 | Native pawn-level winner for both starts 3–20; list filter uses White. Structure checks every opening file, every forced capture continuation, exact terminal diagram and next mover. The nonempty-set guard at line 284 matters. |
| **CHECKED-2** `ring_grundy`, 299–306,345–347 | Native macro-Grundy from the root for both starters at 3–16. Separate after-push Grundy comparisons use all files at n≤12 and only files 0,1 at 13–16. The root still traverses all pushes. Paper's finite annotation through 16 is warranted. |
| **PROVED / COMPUTED-1** `strip_check`, `no_promotion`, `ring_naive_kernel`, `strip_naive_kernel`, `naive_native`, 352–368 | Native strip outcomes and macro-Grundy through 15; exhaustive no-promotion through 14 on rings (from 3) and strips (from 1). Naive kernel winners on rings 3–6 and strips 1–6; compiled naive winners on rings 3–8 and strips 1–9. |

**PROVED — qualification on the macro-game interpretation.** `Dawson.lean:193–208,224–234` flattens all compulsory-capture continuations of a push and checks the resulting turn. If the replying side could choose between nonequivalent subgames, granting the initial mover every endpoint as a mex option would need justification. Checking turn parity alone is insufficient to prove impartiality at every quiet position. For instance the quiet one-file diagram with only a White pawn on rank 1 gets macro values 1 and 0 for its two starters (**F**); this is outside the full-start domain. The first-move structure theorem rules out divergent endpoints on the opening push at full roots. Our independent **C** check groups ends by the initiating push, requires that all choices have the same continuation value and hand over the turn, and cuts at physically empty files. It agrees on the bounded roots. No Lean induction establishes the general ring rule or the octal period, and the misère claims belong to a different game.

**CHECKED-2 — recomputation.** Direct pawn-based macro-Grundy values at n=3 through 20, in order, are `1 0 0 0 1 0 0 0 1 0 0 0 0 0 1 0 0 0`. These agree with the paper formula throughout, with Lean's macro-Grundy through 16, and with its full winner/structure through 20. From the independent strip recurrence, the winning widths through 60 are `3 7 11 17 23 27 31 37 41 45 57`. Above 20 this is a recurrence calculation. **C** reproduces both lists. Lean's `ring_win_list` ends at 57; the paper's displayed list has an ellipsis.

## D · The cut map

**PROVED — correct map, finite one-step theorem.** `dist/tog/sections/02_rules.tex:83–97` cuts out an empty cylinder file. `Claims/L9_Cut.lean:63–75` sends the next file to 0, the preceding file to n−2 and preserves ranks, headings, colours and the relabelled flag. On 0≤e,f<n the numerator `f+n-e-1` is nonnegative before the modulus, so natural subtraction loses nothing. The codomain has n−1 files. `step` at lines 112–125 checks validity and normal form on both boards, component counts and sets, passer presence, classification by last mover, individual e.p. capturability, closure of every pawn successor and equality of the two successor sets for each colour. Component sets suffice because components have disjoint, nonempty supports. `allCheck` varies every empty cut and all nine settings. The equality-of-values induction is in the comment (lines 44–52), outside the proof term.

**PROVED — range and hypotheses.** `L9_Cut.lean:82–104,183–207` fills all normal-direction placements up to the pawn cap, excluding White on rank 1 and Black on the last rank, including the empty board, terminal positions, and every normalized usable e.p. right. There is no alternating-history or root-openness hypothesis. The eleven (files,ranks,pawn cap) triples are (3,5,6), (3,8,4), (4,5,4), (4,6,4), (4,8,3), (5,5,4), (5,6,3), (5,8,3), (6,8,2), (7,5,3), (8,5,2). All are native checks. The supplementary brute enumeration at lines 139–154,183–185 tests only the **unflagged** generator on three tiny board sizes. `fam_nonvacuous` tests the specified single family. The four `cut_value_*` at lines 158–169,205–207 add only 0, *1, *2, 1, −1, for both movers, with BIG=20 and a definite-result guard. None asserts equal values for arbitrary n, pawn count, test game or arbitrary coordinate-dependent race assignments.

**CHECKED-2 — independent brute-force instance.** For (6,8,2) each cut has 2,456 unflagged fillings and another 16 distinct usable flags, hence 2,472 with e.p. enabled. Our enumeration chooses up to two coloured squares, then generates flags forwards from legal double steps. The comparison relabels by rotating a list of surviving files, checks both moves and passer-square sets, closure, the component partition with its flag and all three race verdicts. Every cut and setting passed. The size at cut 0 agrees with a direct Lean evaluation and with `lean/notes/L8_L9.md:80`. Reproduce with **A/D** and **L**.

## Trust, strengthened tests and scope of the verdict

**COMPUTED-1 — definite-answer replay of the agreement suites.** **L** returned true for all four strengthened `HeapsAgrees` predicates and the strengthened `wide_agrees_spec`. Thus the permissive predicates did not mask an unknown on these actual comparisons. There are 1,620 initial diagrams, 14,580 (diagram, board, setting) triples across the three topologies, 3,378 open flat/cylinder cases and 5,010 open cases including the strip. Of the 3,378, **2,658 fail the project's own `Position.valid`**, leaving 720 valid flat/cylinder test cases. The same 2,658 fail among the 5,010. The cause is `SearchAgrees.lean:38–46`, which allows Black to start on rank 5 of a five-rank board; `Rules.lean:394–400` excludes that on flat boards and cylinders. The strip validity predicate differs. Testing extra invalid roots still exercises code, but these counts should not be described as counts of distinct legal chess placements. The additional genuine census samples use the default setting. The stricter tests exercise the same pawn rules as their references, unlike the independent census.

**CHECKED-2 — two corrections to the authors' notes.** The missing C11 whole-board assertion is numerically supported: **B** and **F** give NNNPN on the twelve-pawn cylinder in the default setting. This checks both starters and the distinguishing heap 3. It remains absent from the tracked claim theorem. Also, `lean/notes/L7_L10.md:55` says the six-pawn C3 ring fails to be zero under mover/off. The same note at line 170 reports the opposite. Both new computations give **PNNNN for mover/off** and **NNPNN for opponent/off**, heaps 0–4. The latter statement in the note is correct. Its formal off/count claim is unaffected. On C3 no nonempty position can split into multiple occupied-file runs, so the whole-board heap comparison also tests the intended sum value.

**PROVED — trust boundary.** The source scan **S** found no handwritten `sorry`, `admit`, `axiom`, `unsafe`, `partial`, `implemented_by` or `@[extern]` in the audited claim import chain. The executable `lean/MoveList.lean:104` has a partial I/O loop, which these claims do not import. Compiled computation does introduce native axioms. For example **L** prints `census_big._native.native_decide.ax_1_1` together with `propext`, `Classical.choice` and `Quot.sound`. `census_totals`, `roots_open_X` and `fh_black_threat` print no axioms; `eighth_empty_table_default_kernel` prints only `propext`. The universal eighth inherits the native axiom for its nine-setting base. The larger-heap specification lemma uses `propext` and `Quot.sound` and no native decision. The report's **PROVED** labels cover the stated mathematical or proof-term implication. **COMPUTED-1** denotes a single numerical route and **CHECKED-2** agreement with a separately implemented route.

**PROVED — three documentation limits.** Read after forming the verdicts, `lean/notes/L7_L10.md:97–102` identifies the finite widths accurately, but “the finite part” is too broad if it includes the graph isomorphism hypotheses used by insertion; the Lean base outcomes establish only part of the finite premises. Lines 3–5 give stale import guidance: `lean/CylChess.lean` imports `Claims.Axioms_L7_L10` transitively bringing in the new claims. `lean/notes/L8_L9.md:39–45,95–110` distinguishes the finite Dawson and one-step cut checks from the general proofs. Its statement around line 106 should attribute winning widths beyond 20 to the recurrence; the structural pawn check also ends at 20. A secondary transcription slip in `Claims/L7b_Star3.lean:11` lists Qo's base as 22 and 19 in one sentence. Note 3's odd base is 19.

**COMPUTED-1 — work not repeated.** I did not rebuild the original Lean modules, align every independent game value with a Lean per-position trace, audit the insertion proofs line by line, reconstruct their reduced graphs, or rerun every L11 ring scan and every L7 family width. I reviewed the named statements and their definitions and imported the existing Lean artifacts for the referee probes. The historical atlas, textbook census, whole-board census, real kings and misère Dawson are separate from this task. The additional computations here assess a pawn model, without a novelty claim.

## Reproduction from the repository root

Set the following variables once in the shell. All paths below are repository-relative. The scripts use the standard library. Run each command block sequentially.

```sh
d=delegate/out/L14_codex
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1
```

**E · Independent census, all 20 groups, any nimber.** The comparison asserts every row, the residual non-nimber count, the complete key set and zero failures in the reference. The six final output lines for width 4 and six pawns are disjoint partitions by lowest rank on the first file. As an additional positive control the same canonicalizer recovers *2 on the paper's seven-pawn flat position A.

```sh
nice -n 15 .venv/bin/python "$d/census.py" --self-check
sh "$d/full.sh" > "$d/full.out"
nice -n 15 .venv/bin/python "$d/compare.py"
```

**A/D, B, C · Independent computations.** The first command gives the eighth, all threat lines and the complete selected cut instance. The second gives the whole-board signatures (including the C11 witness and all settings for the six-pawn ring). The third evaluates the component-sum witnesses against their target heaps, including M10 and O11. The fourth gives the two Dawson lists.

```sh
nice -n 15 .venv/bin/python "$d/other.py"
nice -n 15 .venv/bin/python "$d/boards.py"
nice -n 15 .venv/bin/python "$d/sums.py"
nice -n 15 .venv/bin/python "$d/dawson.py"
```

**F · Flagged-root witness and model comparisons.** The first invocation finds the example by search. The second compares it on the Lean model, evaluates the omitted C11 whole-board signature, the contradictory C3 note entries, a quiet Dawson position with different values from its two possible starters, and the open tall-board counterexample to fast-search correctness.

```sh
nice -n 15 .venv/bin/python "$d/flag.py"
(cd lean && nice -n 15 lake env lean -j1 -M 2200 "../$d/Extra.lean")
```

**F+ · Additional live-right records.** Python prints width, material, records, zeros, stars and higher nimbers. The awk command totals those rows by width. Lean prints width, records, zeros, stars, higher nimbers and failures. `FlagCount.lean` is an external audit probe; it was never an input to the independent canonicalizer.

```sh
for n in 2 3 4; do nice -n 15 .venv/bin/python "$d/flag.py" "$n"; done > "$d/flagged.out"
awk '/^live roots/{for(i=5;i<=8;i++) a[$3,i]+=$i} END{for(w=2;w<=4;w++) print w,a[w,5],a[w,6],a[w,7],a[w,8]}' "$d/flagged.out"
(cd lean && nice -n 15 lake env lean -j1 -M 2200 "../$d/FlagCount.lean")
```

**L · Agreement, coverage, cut-family size, axiom and tall-board probes.** Outputs in order are the always-unknown reference counterexample, tall sentinel witness, exact group-key comparison, number of groups, sample sizes, invalid case counts, the three cut-family sizes, the named axiom lists and five strict agreement results.

```sh
(cd lean && nice -n 15 lake env lean -j1 -M 2200 "../$d/Audit.lean")
```

**S · Read the bounded source assertions and screen for trust escapes.** These commands reproduce the theorem names, literal domains and numbers quoted from the project. Numeric searches reproduced independently are listed above.

```sh
rg -n '\b(sorry|sorryAx|admit|axiom|unsafe|partial|implemented_by|extern)\b' lean -g '*.lean'
rg -n '^import .*MoveList' lean/CylChess lean/CylChess.lean
rg -n -A4 '^theorem' lean/CylChess/Claims/{L5_EmptyTable,RootsOpen,L6_NotHSS,L7*,L9_Cut,L10*,L11*}.lean lean/CylChess/{Dawson,WideLemmas,SearchWideAgrees,HeapsAgrees}.lean
rg -n 'C1|C2|controls|signature|first ring|every' dist/tog/supp/{s06,s13,s14}.tex dist/tog/supp_src/s15_note*.md
```

The shell already ran at niceness 20. Here `nice -n 15` reported a priority-setting error and the child retained niceness 20, verifiable with `nice -n 15 .venv/bin/python -c 'import os; print(os.getpriority(os.PRIO_PROCESS, 0))'`. All game jobs ran serially with respect to other heavy jobs started by this review.
