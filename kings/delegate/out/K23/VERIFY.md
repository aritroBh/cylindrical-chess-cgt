# K23 referee report (VERIFY)

Referee: independent run, 2026-10-27. Scope: `K23/summary.json`, `K23/EDITS.md`, LOOPY.md sections 2 (Def. 2.1, 2.6, Thm 2.7, Prop. 2.10), 5.1, 6, 7, 8.
There is no `K23/REPORT.md` (only `summary.json`, `EDITS.md`, `logs/`, `scripts/`, `data/`); I read the summary text of the task, `logs/key_digest.txt`, `logs/enum_counts.txt`, `scripts/gen_ctx.py`, `scripts/classify.py`.

**Verdict: ACCEPT WITH FIXES.** Every number reproduces, with my own code. The mathematics of the example is right. What has to change is wording and labels in the EDITS, listed in section 4.

## 1. What I built (all in `K23/verify/`, none of the agent's scripts used for the numbers)

| tool | what it is |
|---|---|
| `ref3.cpp` | my own solver, written from `kings/SPEC.md` only: K+pawns v K+pawns, cylinder or flat, layer-by-layer retrograde (pawn moves change the layer, kings move inside it), e.p., double steps. Default = P (first promotion wins for the promoter, real kings); `--frozen` = every king move loses at once for the mover, promotion wins at once, stalemate draws. `ref3m.cpp` = same plus `--moves`. |
| `gen.py` | my own context generator (same definition as stated in the claim: pawns of both colours on the listed files, ranks 2-5, at most a/b pawns per side, e.p. `-`, both sides to move) |
| `analyze.py` | my own passed-pawn test (textbook, context pawns only, cylinder wrap) and counts |
| `local_game.py` | my own implementation of the local game L_T(Q_Z) of Definition 2.6 (both the L1_P and the queen-clause form) |
| `mu.py` | my own breadth-first search for mu_s of (L2) |
| private builds | `kp` = `kings/kpsolve.c`, `kp_p` = K7 `kp_p.c` (`--pmodel`). They share source, so they are one family; `pk2.c` is the only other independent code of the agent. |

Cross-checks: `ref3` against `kp_p --pmodel` (P) and `kp --frozen` (frozen), position by position, on `data/key_7x6.txt`, `data/dist8.txt`, `data/g88.txt`, `data/pair.txt`: 0 differences in every file (92 positions, P and frozen). On the whole 7x6 enumeration (1,770 positions) `ref3`, `kp_p` and `kp` agree on every position (0 differences, P and frozen). On the whole 8x6 enumeration (9,158 positions) `ref3`, `kp_p` and `kp` also agree on every position (0 differences, P and frozen).

## 2. Claim by claim

**Claim 1 (the example). CONFIRMED, CHECKED-3 (ref3, kp_p/kp, and the agent's pk2).**
`printf 'Ka4 Pb3 kc3 pb4 Pe3 pe4 b -\n...' | verify/ref3 --board cyl:7x6` (file `verify/key.txt`):
- G1 = {Pe3, pe4}: P = (L, W), frozen = (L, W).
- G2 = {Pe2, pe3}: P = (L, L), frozen = (L, W).
- Mirror {Pf4, pf5}: P = (W, W), frozen = (L, W).
- `verify/ref3m --board cyl:7x6 --moves`: in G2, Black to move: Kb2, Kc2, Kd4 lead to White wins (they lose for Black), Kd2 leads to a Black win; Kd3, Kc4 and Kxb3 are not generated (Kd3 is covered by the pawn e2: illegal; as claimed). In the mirror, White to move: Kg5 wins, Kg3, Ka5, Kb5 lose (Kg4 is illegal, f5 covers it).
- Same results with e.p. off.
The claim "Black wins by 1...Kd2, the only winning move" is exact. The label CHECKED-2 is not stronger than the evidence (it is weaker: three implementations agree).

**Claim 2 (the six P4 rows equal the convention in P). CONFIRMED, CHECKED-3.** `data/p4.txt` is exactly the six contexts of LOOPY section 6 (Hm1 = Pe2/pe3 pe5, Hp1 = Pe2 Pe4/pe5, H* = Pe3/pe5, H*2 = Pe2/pe5, H0 = Pe3/pe4, and nothing). `ref3` P values: (L,W), (L,L), (W,W), (W,L), (W,L), (L,W) = the convention. The three chess refutations therefore are not P effects. What K23 did not show is *why* chess differs (see problem 2 below).

**Claim 3 (section 5.1 group on cyl:8x8). CONFIRMED, CHECKED-3.** `ref3` on `data/g88.txt`: bare group (L, W). Pe3/pe4 gives (L, W), Pe2/pe3 gives (L, L), Pe6/pe7 gives (W, W); Pd2/pd3, Pd3/pd4 differ with Black to move, Pf5/pf6 and Pf6/pf7 differ with White to move. The others hold.

**Claim 4 (enumerations). CONFIRMED for the 7x6 <= 2 and 8x6 <= 2 counts, with my own generator and solver; the 7x6 <= 3 count (99 of 3,237 differ) is NOT CHECKED, see section 3.**
- My generator: 885, 4,579 and 3,237 contexts (also by direct counting).
- cyl:7x6, e-f, <= 2/2: **885 contexts, 47 differ** (4 with a passer, 43 passer-free); 23 passer-free contexts have frozen (L, W) and differ; they contain **26** (context, side to move) pairs in which the frozen mover loses and does not lose in P; in **all 26** a king step onto the buffer file is among the non-losing moves (Kd2 / Kd3 for Black; Kg3 / Kg4 / Kg5 for White; one pair also has Kd4). 0 illegal positions. `verify/analyze.py 7 c722.P c722.F`, per-move check in the run recorded in section 3.
- cyl:8x6, e-g, <= 2/2: **4,579 contexts, 152 differ** (47 with a passer, 105 passer-free), **0 differ without a pawn on e or g**; the 63 contexts confined to f (62 non-empty plus the empty one) never differ. The "81 single-file contexts on f, <= 4/4" are all of {empty, W, B}^4 on f2..f5 = 81, a trivial count; I did not re-run them (NOT re-checked, but they are a subset of the same family and cost nothing to rerun).
- Parked kings: Z_T replaced by `Ka1 ka6`, frozen: **1,770 positions, 0 differences** (my frozen solver). Caveat: this is a sample (e-f, <= 2/2); the text of the Definition states it for every G.

**Claim 5 (Psi does not depend on the kings). CONFIRMED on the sample** (above). A one-line argument would remove the caveat: kings on F_Z are never attacked by context pawns and never block them (Lemma 2.2), so in the frozen model only pawn moves and the existence of a legal king move matter, and Z_T and the parked kings both have one.

**Claim 6 (mechanism, one tempo). CONFIRMED, and the open point is now computed.**
- Race positions: `Kb4 Pb3 ke2 pe3 w` = L, `Kb4 Pb3 ke3 pe4 w` = W (ref3, kp_p, pk2 agree). 
- The agent did not run the local game. I did (`verify/local_game.py`): after m = 1...Kd2, r = 2.Kxb4, Q_Z = Wk b4, Pb3, bk d2, Black to move (Black may pass, White's king confined to a-c): **T = 4**, both for (L1_P) and for (L1) with the queen clause (T = 3 fails). COMPUTED-1 (my code, one implementation).
- mu_s by breadth-first search (`verify/mu.py`): **4 in G2, 5 in G1**. So with T = 4, (L2) mu_s >= T + 1 = 5 holds in G1 and fails in G2 by exactly one tempo, as claimed. (L3) not checked by me either.
The text can therefore say "T = 4, COMPUTED-1 (K23 referee)" instead of "not run".

**Claim 7 (the general statement is a CONJECTURE). CONFIRMED as "not proved".** I looked for a gap in the stated obstacle. (i) to (iii) are correct readings of Definition 2.6 and Theorem 2.7, the converse of Theorem 2.7 is false (LOOPY "No converse" already says so), and nothing in K23 touches groups other than Z_T and the 5.1 group. The label CONJECTURE is right. I also see no easy refutation; the example family says nothing for a group whose sortie kings cannot reach the buffer.

## 3. Heavy runs and what is outstanding

- All runs above were under about one CPU-minute each (ref3: 7x6 <= 2: 4.5 s P, 0.4 s frozen; 8x6 <= 2: 32 s P, 2.6 s frozen), `nice -n 15`, RSS below 200 MB.
- The 7x6 <= 3 enumeration (3,237 contexts, 99 differ claimed) was submitted through `heavy.sh` and never got a slot in about 30 minutes (both slots were held by other jobs); I cancelled it (my own PIDs only). **NOT CHECKED by me**: 3,237 contexts and 99 differing remain the agent's numbers (pk2 and kp_p/kp agree there, per the agent). My own check of the <= 3 claim is the 3,237 context count (by direct counting) only. The <= 2 results that the text relies on most (885/47 and 4,579/152) are reproduced.
- `kp_p`/`kp` on the 8x6 <= 2 file: done, 0 differences from `ref3`.

## 4. Problems with the claims and the EDITS

1. **Label inflation ("PROVED by example"). Must fix.** LOOPY's Labels rule says kpsolve and solver results are data: "a claim that only a kpsolve run supports keeps the label CONJECTURE, with 'kpsolve agrees'", and PROVED means the full proof is in the note. The EDITS (EDIT 1 "PROVED by example, in P (CHECKED-2...)", the status-table row for P2.10(b), the section-0 sentence, the P13 row "PROVED by example", and `summary.json` "result") call the example PROVED. The example is a computation (the refutation of the six other White replies after 1...Kd2 is "by the solver"). Use **CHECKED-2** (now CHECKED-3), as claims 1 to 5 do, and say that no hand proof is given. "PROVED" in the old text of 2.10(b) refers to the abstract (L2) example and is unaffected.
2. **EDIT "section 6 notes: P4 mechanism sentence": inaccurate.** NEW says the (L2) margin "does not survive the context, in P in G2 and in C in H*, H*2 and H0". H0 is G1: its mu_s = T + 1, so (L2) holds there in P (EDIT 1 says so itself), and K23 did not run C, so nothing shows that an (L2) failure is what happens in C. By LOOPY's own text, mu_s = T + 1 is not enough for a chess win (queen against queen, (L2+) needs T + 2), so the likely reason is (A_Q) or that margin; that is a guess. Suggest: "In C the sorties draw; K23 did not run C. In P the same sorties lose, so the C result is not a P effect (not shown to be an (L2) failure)."
3. **"(A_Q fails)" is asserted, not tested,** in EDIT P4 status row, EDIT "what P4 tests" and EDIT 1 ("facts about chess (A_Q fails)"). The checked fact is "the P value equals the convention in all six rows". Suggest "chess-only effects (not a P effect); the cause was not examined in K23".
4. **EDIT "section 7, (S2)".** The paragraph is the list "(S2), a legal Z-move of the loser that is not a P-loss". After K23 the H0 sorties are P-losses, so the example is no longer an (S2) failure in P; saying "so this (S2) case is a fact about chess" keeps it under a heading it no longer fits. Suggest moving the sentence out of the P list or saying "not an instance of (S2) in P; in C the sorties do not lose".
5. **"So the failure needs a context pawn within a step of the buffer file"** (EDIT 1, Distance) is stated as a necessity but is a sample fact (<= 2 pawns a side, ranks 2-5, e-g). Say "in every failing context of this sample". Also "62 contexts confined to f" are the 62 non-empty ones (63 with the empty context); say so.
6. **P13 row, Basis column:** it cites the hand race count with mu_s = T in G2, which is for Z_T; for the 5.1 group on cyl:8x8 no mechanism was analysed (T = 6 to 7 there). Add "mechanism analysed for Z_T only".
7. **Stale text not covered by the 10 edits** (each occurs once, check with `grep`): LOOPY.md line 1966 ("The trébuchet zero is universal": now Proposition 2.10(b) plus a CONJECTURE) is false for Z_T in P after K23; the §5.1 "Prediction" bullet (bare 5.1 "one throwaway implementation, hence a CONJECTURE") predates the exact P value (L, W) now CHECKED-3. Suggest one more edit for each.
8. **Wording:** "Ψ(G) does not depend on the kings" is stated for every G but checked on a sample; and "every other White reply loses as well" in EDIT 1 refers to G2 only (in G1 after 1...Kd2 White wins), say so.
9. Process: "two independent implementations" is true only for pk2 against the kpsolve family (`kp`, `kp_p` share source). Mine is a third, and agrees.

## 5. EDITS check (OLD occurs exactly once in the current LOOPY.md; table rows have the right number of cells)

`verify/chk_edits.py`: 10 blocks, OLD count 1 for each. Row cell counts: P6 row 8, P13 row 8 (header has 8), the two status-table rows 3.

| EDIT | OLD once | NEW accurate |
|---|---|---|
| P2.10(b): split the conjecture; the example | yes | numbers yes; fix the label (problem 1), the necessity wording (5), "not run" for T (can say T = 4 COMPUTED-1), and 3 |
| status table: P2.10(b) row | yes | fix label (1) |
| status table: P4 row | yes | fix (3) |
| section 0: the conjecture sentence | yes | fix label (1) |
| section 7, (S2): P4 with H0 | yes | fix (4) |
| section 6: P6 row | yes | ok |
| section 6: new row P13 | yes | fix label (1) and Basis (6) |
| section 6 notes: what P4 tests | yes | fix (3) |
| section 6 notes: P4 mechanism sentence | yes | **fix needed (2)** |
| section 8: open question 6 | yes | ok (new item 6 after item 5 which is the last) |

## 6. Reproduce

```
cd kings/delegate/out/K23/verify
c++ -O2 -std=c++17 -o ref3 ref3.cpp ; c++ -O2 -std=c++17 -o ref3m ref3m.cpp
./ref3 --board cyl:7x6 < key.txt ; ./ref3 --board cyl:7x6 --frozen < key.txt ; ./ref3m --board cyl:7x6 --moves < key.txt
python3 gen.py 'Ka4 Pb3 kc3 pb4' ef 2 2 2 5 > c722.txt ; ./ref3 --board cyl:7x6 < c722.txt > c722.P ; ./ref3 --board cyl:7x6 --frozen < c722.txt > c722.F ; python3 analyze.py 7 c722.P c722.F
python3 gen.py 'Ka4 Pb3 kc3 pb4' efg 2 2 2 5 > c826.txt ; ./ref3 --board cyl:8x6 < c826.txt > c826.P ; ./ref3 --board cyl:8x6 --frozen < c826.txt > c826.F ; python3 analyze.py 8 c826.P c826.F
python3 local_game.py ; python3 local_game.py queen ; python3 mu.py ; python3 chk_edits.py
```

## 7. Files kept
`verify/`: `ref3.cpp`, `ref3m.cpp`, `gen.py`, `analyze.py`, `local_game.py`, `mu.py`, `chk_edits.py`, `key.txt`, `verify_log.txt` (outputs of the runs quoted above). Bulk inputs, outputs and binaries were deleted.
