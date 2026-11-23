Note 1 (dist/tog/supp_src/s15_note1.md): SOUND WITH FIXES; Note 3 (dist/tog/supp_src/s15_note3.md): SOUND WITH FIXES

## 5-line summary
1. Both notes' insertion proofs (Lemma 3, §2b) follow from S13 Lemmas 1-3; the repaired "pattern file" definition and the H1-H8 hypotheses are stated and, on inspection, sufficient for the claimed families.
2. Note 1's P_n = *2 (even n>=8) and Note 3's R_n = *2, Qo_n = *3 (odd n>=11) are conditional on the cited finite checks C1'/C2' and C1/C2; the hand parts are not independently proved here.
3. One computed-fact label in each note is slightly loose (B is not an independent program; D is a copy of Note 1's D), and Note 3's refereeing statements contradict each other.
4. Independent stdlib-only checks reproduced the structural facts H5/zone/cut/pawn counts for both families (delegate/out/T86_opencode/check_small.py): all agree.
5. Full node counts, pump isomorphisms, Lemma 2/3 stress tests and race-rule sensitivity were not re-run; they rest on the cited (external) programs.

## Findings

### Note 1: dist/tog/supp_src/s15_note1.md
- dist/tog/supp_src/s15_note1.md:119, MINOR. Undefined symbol: "families of Section S13 (O, E, F)" references F, which S13 does not define (only O_n and E_n). Replacement: "families of Section S13 (O_n, E_n)".
- dist/tog/supp_src/s15_note1.md:16, MINOR. Program identifiers (rg.c, reduced_cyl.py, check3/eng.py, verify_logic/engine.py, verify_compute/myeng.py) are not present in dist/tog/supp/ or dist/tog/supp_src/; they live under research/ring_n_plus_2_proof/. Replacement: prefix each with "research/ring_n_plus_2_proof/" or add a source-location appendix.
- dist/tog/supp_src/s15_note1.md:30, MINOR. C1' is labelled CHECKED-2 on (A, B, C, D, E), but B is cylcgt's own rebuild, not an independent implementation; the honest count of independent programs is four (A, C, D, E). Replacement: "CHECKED-2 (A, C, D, E; B is a cylcgt rebuild, not independent)".
- dist/tog/supp_src/s15_note1.md:10, MINOR. Process claim "two adversarial AI reviewers ... found no mathematical defect" and "refereed by one AI referee ... found it sound" is unverifiable from the repository; leave as caveat or move to an audit log. Replacement: "AI review reports are available on request; no human referee has checked the note."

### Note 3: dist/tog/supp_src/s15_note3.md
- dist/tog/supp_src/s15_note3.md:9, MAJOR. "A model of another vendor then refereed the note and found the proof sound for the family as defined here" contradicts Scope (line 11), which says the odd hand part "has not been refereed by a model of another vendor". Replacement (line 9): "A model of another vendor then refereed the computational parts and the families as defined here, recomputed the two signatures for every odd n=11..23 and the base graphs at n=19; it did not independently check the new odd-specific hand text (H1-H3)."
- dist/tog/supp_src/s15_note3.md:11, MINOR. Scope's "has not been refereed" should be aligned with the replacement above. Replacement: "The hand text specific to the odd families (H1-H3) has not been refereed independently of the computations it cites; only the shared Lemma 3 text of Note 1, §2b was refereed for P_n."
- dist/tog/supp_src/s15_note3.md:14, MINOR. D is described as independently written but is a byte-identical copy of Note 1's D (verify_logic/engine.py); the independent count should not include D as a fresh implementation. Replacement: "D = verify_logicOdd/engineD.py (a copy of verify_logic/engine.py, program D of Note 1; not an independent implementation)".
- dist/tog/supp_src/s15_note3.md:45, MINOR. Undefined cross-reference: "phase and ends differ from E_n, P_n, Q_n" names Q_n, which is defined in Note 2, not in this note or S13. Replacement: "differ from E_n (S13), P_n (Note 1) and Q_n (Note 2)".
- dist/tog/supp_src/s15_note3.md:14, MINOR. Program identifiers are not present in dist/tog/supp/ or dist/tog/supp_src/ (they live under research/ring_n_plus_2_proof/). Replacement: prefix each with "research/ring_n_plus_2_proof/".

## Computed facts and label honesty

Note 1 depends on:
- C1' (R_18: 813 nodes, 1643 K-edges, 1372 T-edges, no flag, zone {0,2,3,4,5,6}, G+*2 P): labelled CHECKED-2 on A,B,C,D,E. Honest count of independent programs: 4 (A,C,D,E); B is a cylcgt rebuild. Verdict: label slightly loose.
- C2' (P_n+*2 P for n=8,10,12,14,16): CHECKED-2 on A,C,D,E. Honest: 4 independent programs. Verdict: honest.
- S1 (813 nodes/zone for n=14..60, pump 18->60): CHECKED-2 on A,C,E (D to 36/44). Honest.
- S2 (signature NNPNNNNN for n=8..60): CHECKED-2 on A,C,E. Honest.
- S3 (cylcgt canonical value *2 for n=8..20): COMPUTED-1. Honest, with the stated caveat that the whole-board route only reached n<=10.
- S4 (Lemma 2/3 tests, 0 failures): CHECKED-2 on C,D,E. Honest.
- S5 (192/813 nodes split, 58/240 captures): CHECKED-2 on C,E. Honest.
- S6 (race-rule sensitivity): COMPUTED-1 (E). Honest.

Note 3 depends on:
- C1R/C1Q (R_19: 429 nodes/805 K/653 T, zone {12..16,18}, NNPN; Qo_19: 1287/2996/1959, zone {0,1,12..16,18}, NNNP): CHECKED-2 on A,B,E and rebuilt by C,D,O. B is a cylcgt rebuild, not independent beyond n<=21; D is a copy of Note 1's D. Honest count of independent implementations: A,C,E,O (4), with B,D as rebuilds/checks. Verdict: label slightly loose but disclosed.
- C2 (signatures for n=11,13,15,17): CHECKED-2 on A,E (also C,D,O). Honest.
- C3 (n=9 LLLL): CHECKED-2 on A,C,D,E,O. Honest.
- S1 (pump 19->59): COMPUTED-1 (A) beyond 33, CHECKED-2 to 33. Honest.
- S2 (signatures to 59): COMPUTED-1 (A) beyond 25. Honest.
- S3 (Lemma 2/3 on nodes): CHECKED-2 on E,D,O. Honest.
- S4 (cylcgt rebuild n=11..21): CHECKED-2 on A,B. Honest.
- S5 (differential tests): CHECKED-2. Honest.
- S6 (raw-flag equivalence): CHECKED-2 on O and a pawns.py rebuild. Honest.

## Independent recompute (this audit)
Program: delegate/out/T86_opencode/check_small.py (stdlib only; no repository code imported). Recomputed:
- Pawn counts n+2 for P_n (n=8..20), R_n and Qo_n (n=11..19): all agree.
- ins_12(start_18) == start_20 (Note 1 H5): agree.
- ins_6(R_19) == R_21 and ins_6(Qo_19) == Qo_21 (Note 3 H5): agree.
- Cut admissibility n0=18 (arc 8..17) and n0=19 (arc 2..11): agree.
- Zone sets P_18 {0,2,3,4,5,6}, R_19 {12,13,14,15,16,18}, Qo_19 {0,1,12,13,14,15,16,18}: agree with the notes.
Result: agreement on all checked structural facts. No discrepancy found.

## What was not checked
- No independent reimplementation of the chess rules or of the reduced-game solvers was attempted; all node counts, edge counts, pump steps, Lemma 2/3 stress tests, race-rule sensitivity and tablebase claims are taken from the cited programs.
- The hand proofs of S13 Lemmas 1-2 and Note 1 §2b were read but not re-derived; Lemma 3 (iii) was checked against the stated view lemma V only.
- The real-chess/tablebase and component-sum claims cited in RESULTS.md were not part of this audit.
- No human referee or non-Claude implementation was available; the notes' own AI-review process claims were not verified.
