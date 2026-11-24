# R15 consistency audit of the ToG submission package (read-only, 2026-11-23)

Checked state: dist/tog PDFs built 2026-11-23 13:42 (tog_review.pdf sha256 f96336fc..., supplement_review.pdf 20951b09...), repo HEAD fc19cc80, anonymous code copy built from 2be946c1. Working text extractions are in this folder (tog_review.txt, supplement.txt and so on; they are scratch).

Scoreboard: A 25 PASS / 0 FAIL. B 14 PASS / 0 FAIL. C 5 PASS / 2 FAIL (+1 note). D 3 PASS / 1 FAIL. E 8 FAIL (stale or contradictory statements), 9 PASS. F 36 path tokens exist, 8 do not (+18 figure files that are build assets). G 0 identifying hits, 2 internal-note-style notes.

## A. Cross-references from the 10-page paper into the supplement: PASS (25 of 25)

The paper hard-codes "Section S<n>" (there is no \ref to a supplement label; supp/mainlabels.tex only goes the other way). Supplement headings from the printed contents (supplement.pdf): S1 Basic Positions and the E.p.-Aware Test; S2 Kings: Certificates, Loopy Games and the Failure Sweep; S3 Sums: The Puzzles and Condition (E); S4 The Atlas: Details; S5 Elkies' Small Values: Details; S6 The *2 Question: Details and Ring Listings; S7 From the Model to Real Chess: Details; S8 Tablebases: Rules and King and Pawn Against King; S9 Dawson's Chess: Details and Learning; S10 Further Open Problems; S11 Positions with Kings in FEN; S12 Full Proofs: Validity..., Sums, Certificates and Loopy Games; S13 Wall Rings *2 with n+3 pawns; S14 Rings *2 with one pawn per file; S15 Lemma 3 write-up, *3 families, Mobius strip; S16 The Square-Rule Passer Test; S17 Who Wrote and Who Checked the Proofs.

| # | Where (file:line) | Cited | Target heading | Fits |
|---|---|---|---|---|
| 1 | 02_rules.tex:66 (Fig. 2 caption) | S1, values 1, 2, star, up | S1.2, S1.3 | PASS |
| 2 | 02_rules.tex:79 | S1, 4,070 outcome changes | S1 first paragraph holds 18,137 / 231,071 / 4,070 | PASS |
| 3 | 02_rules.tex:108 | S1, derivations of 1, 2, star, up, double-up-star | S1.2, S1.3 | PASS |
| 4 | 04_kings.tex:66 | S12, full proof of Theorem 3 | S12 (core results A.III) | PASS |
| 5 | 04_kings.tex:85 | S12 exact clauses and proof | S12 | PASS |
| 6 | 04_kings.tex:86 | S2, local test for (V2), loopy games | S2 opening sentence names both | PASS |
| 7 | 04_kings.tex:99 | S16, square rule not sound on every board | S16 (counterexample) | PASS |
| 8 | 04_kings.tex:101 | S2, 2,154 / 105 / 2,049 / 92.5% | S2.3 (same numbers) | PASS |
| 9 | 05_sums.tex:17 | S3 shows the puzzles | S3.1 | PASS |
| 10 | 05_sums.tex:66 | S12, proof of Theorem 6 | S12 | PASS |
| 11 | 05_sums.tex:74 | S3, (E) cannot be dropped | S3.2 Condition (E) | PASS |
| 12 | 05_sums.tex:85 | S3, models differ in outcome | S3.3 Two Models | PASS |
| 13 | 06_atlas.tex:14 | S4, highest temperature 3 | S4.1 The Hottest Position | PASS |
| 14 | 06_atlas.tex:24 | S4, examples | S4.2 Cylinder-Only Values | PASS |
| 15 | 07_targets.tex:62 | S5, checks on the mirror image | S5 first paragraph | PASS |
| 16 | 07_targets.tex:70 | S5, textbook 1/8 and up-second fail | S5.2 | PASS |
| 17 | 08_star2.tex:31 | S6, details of candidate | S6.1 | PASS |
| 18 | 08_star2.tex:52 and :58 | S6, positions A and B | S6.2 | PASS |
| 19 | 08_star2.tex:89, :90 | S6, whole-board scan to nine files, five-file counts | S6.3 | PASS |
| 20 | 08_star2.tex:104 | S6, example rings and counts | S6.3 | PASS |
| 21 | 08_star2.tex:129 | S6, no star-four scans | S6.3 (134,920,191) | PASS |
| 22 | 08_star2.tex:135 | S15, insertion proof on the Mobius strip | S15 Notes 5 and 6 | PASS |
| 23 | 09_real.tex:46, :55 | S7, other nimber-2 positions; 6.1e10 states | S7, S7.1 | PASS |
| 24 | 10_tablebases.tex:69 | S8, counts, widths C3 to C10, KPKP | S8 (table, "Other widths", "A pawn each") | PASS |
| 25 | 11_dawson.tex:10, :60; 12_engines.tex:63; 14_conclusion.tex:5, :14; 13_verify.tex:15 | S9 boards (Fig. S7), S9 Plambeck-Siegel, S9.1 learning; S10 "two more problems" (S10 says main text lists four, full list six; main text has four); S2 Conjecture (h about 5-7, S2 line "Real trebuchets seem to need h = 5-7"); S12-S15 full proofs; S11 FEN | all fit | PASS |

Observation: the 10-page paper also says "S1" in the Fig. 2 caption and the supplement's Fig. 2(b),(c) pointers agree. The supplement intro says "numbers starting with S point to this supplement", consistent with the usage.

## B. Numbers: PASS (14 of 14)

Abstract numbers are all words (six pawns, three files, ten files, seven files, one-eighth, 199 words); each matches the contribution list and the body: "six pawns on C3", "ten on C7 to C10", "n pawns on Cn, n>=10" (S, 08_star2.tex ring section), "ten-pawn rings *3 on C7" (eight of them, S6.3), "seven pawns, A and B, three programs" (Table III paragraph, S6.3 "three programs agree"), "1/8, up-second-star C2, Tiny 1 C1" (Table II, Sec. VII), "2.80%" (Sec. X, Table IV, S8), "233-position pilot" (Sec. XII; Table V rows sum 226 + 7 decided = 233; 181 + 52 = 233), "92.5% of 2,049" (IV-B, XIV, S2).

Threshold checks against the supplement (all agree):
- n>=5 for n+3 wall rings: body 08_star2; S6.3 and S13 Theorem 1 (odd n>=5, even n>=6); checked "n<17" and "to n=12": same in S6.3.
- n>=10 (even M_n, odd n>=11 O_n): S14, S6.3, S10, S6.4.
- *3 with n+2 pawns, even n>=8, odd n>=11: S15 Notes 2 and 3 and S6.3.
- *3 with n+1 pawns, n>=12 (S) and C11 (C2): S6.3, S15 Note 4 (even n>=12, odd n>=13).
- Mobius n+1 pawns *3 for n>=11: S15 Note 6, S6.4. Mobius least *2 "6, 8, 6, 8, 8, 8" (n=3..8), cylinder "6, 7, 8, 9, 10, 10", "10, 10, 11" for n=9..11: Table S3 identical.
- Position counts: 5,503,282 roots; two seven-pawn and four eight-pawn positions; 793,299 placements, 292; 6,470 / 3,891; 134,920,191; 599,098 / 540,503 / 19.3% (S3 table: 11,300 of 58,595); 159 = 107 + 18 + 34; 500; 52; 128; 2,154 / 105 / 2,049; 302 / 290 / 283 / 5 / 2; 6.1e10 / 15.6 h; 216 vs 160 zugzwangs; 326,640; 16,538 / 15,930; 607 million; 0.66%; 638 / 109; 31 of 301 / 56 (S9). All identical.
- Arithmetic inside the body: 55,195 x 15 x 3 = 2,483,775; x 2 = 4,967,550 (matches); 599,098 - 540,503 = 58,595 (matches S3).
- Numbers that exist only in the 10-page paper (no supplement counterpart, so nothing to disagree): 233 and Table V, 160 legal-move test positions, 1,070 components, 55,195 / 4,967,550 / 2,483,775, 26,000 ChessSums sums, 4,887, 200 sums / 163 / 13 (200 - 163 = 37 stand clear of the pawns; 13 of those have a model winning move: the sentence is correct but reads as if 13 were all of them). The supplement carries no Stockfish/Lc0 detail.
- dist/tog/check_numbers.py ran: "RESULT: all numbers found". Caution: it reads the long-version sources (../../paper/ieee/sections/{00_abstract,01_intro,08_star2,14_conclusion}.tex), not dist/tog/sections, and tests only that a number occurs somewhere in the PDFs, so it does not prove agreement in context. I did the contextual comparison above by hand.
- Label difference worth knowing: S10 item 3 gives "n+1 on C11 and C12 <C1>" (least number, needs a scan showing no smaller ring), the body gives "n+1 gives *3 on C11 <C2>" (existence). Not a contradiction.

## C. Bibliography: 5 PASS, 2 FAIL

PASS: every \cite key in sections/*.tex resolves (20 distinct keys, all defined in refs.bib; PyTorch is defined but cited only in the supplement). PASS: 20 entries printed, [1] to [20] in order of first citation. PASS: no author reveal in the anonymous build: tog_review.pdf [9] reads `Anonymous, "Title withheld for review," 2025, unpublished manuscript.` (supplement_review.pdf [5] identical); the named build prints [9] as `A. Bhattacharjee, "Analysis of chess endgames on a cylindrical chessboard," 2025, unpublished manuscript.`; pdfauthor is empty in the review build. PASS: IEEEtran style is consistent (abbreviated journals, "vol., no., pp.", @electronic entries as "Author. (Year) Title. Org. Accessed: date. [Online]. Available: URL"). PASS: DOIs print once.

FAIL 1, [15] (HGMCylinder, refs.bib:195-201): no year (already flagged in delegate/out/ieee_audit/AUDIT.md line 336, still open). Printed: `H. G. Muller. Cylinder chess. XBoard variant rules. Accessed: Oct. 22, 2026. [Online]. Available: http://hgm.nubati.net/rules/Cylinder.html`. Corrected entry (year taken from the page's last update, to be confirmed by the author; if none is shown use "n.d."):
```
@electronic{HGMCylinder,
  author       = {H. G. Muller},
  title        = {Cylinder chess},
  organization = {{XBoard} variant rules},
  year         = {n.d.},
  url          = {http://hgm.nubati.net/rules/Cylinder.html},
  note         = {Accessed: Oct. 22, 2026}
}
```
FAIL 2, [10] (WuYuLandry2010, refs.bib:133-140): a course paper with no institution; IEEE style wants the school. Corrected: `howpublished = {Undergraduate course paper (Math 191), Stanford Univ., Stanford, CA, USA}` (the host is already in the URL, so this does not reveal the author).

Note (not counted): [8] Drummond-Cole (Integers, vol. 5, no. 1, 2005, Art. no. G6) has no pages, DOI or URL; "Art. no." is acceptable IEEE style for an e-journal, and I could not re-verify "no. 1" offline. [7] Dawson lists no editor and [1] Pritchard no pages (both fine for books). The two near-duplicate fields `note = {doi: ...}` and `doi = {...}` in refs.bib print one DOI; harmless.

## D. Abstract, index terms, front and back matter: 3 PASS, 1 FAIL

- PASS: abstract is 199 words (python count of sections/00_abstract.tex and of the pdftotext abstract in both PDFs; one word of headroom under 200; hyphenated words counted as one).
- PASS: Index Terms present: "Chess, combinatorial game theory, endgame tablebases, game solving, nimbers" (5 terms).
- PASS: tog_review.pdf has no biography and an Acknowledgment that names only the Lichess, Stockfish and Lc0 maintainers and the AI vendors (no person). The named build alone names "Prof. T. Morley" (tog.tex:147, \else branch).
- FAIL: the AI-use statement is not identical. Paper (sections in tog.tex:149-154, named build): "...wrote and ran, under the author's direction, the software ... Sections II-XIII and the scripts that draw the figures, wrote and checked the proofs of Sections S12-S15, and helped draft and edit the text of all sections." scholarone_fields.md ("AI-use statement" section) and cover_letter.md (AI use paragraph, which says "The Acknowledgment of the paper states:") both read "...wrote the full proofs of Sections S12-S15..." (the words "and checked" and "full" differ). Fix: copy the paper wording verbatim into both files (review version: "authors"/"are responsible"; named: "author"/"is responsible"). Also a point for the author: the review build says "The authors" for a single author (tog.tex:150-156); scholarone_fields.md records this on purpose.

## E. Submission folder: 8 FAIL, 9 PASS

PASS (verified today): all four hashes, sizes and page counts in files_to_upload.md match (tog_review.pdf 260599 B, 10 p, f96336fc...; supplement_review.pdf 829690 B, 106 p, 20951b09...; tog.pdf 261176 B, 10 p, 049403d7...; supplement.pdf 830013 B, 106 p, bde29999...). pdf_checks.md: pdfinfo (letter, author empty in B and D, named author in A), font counts (57 / 57 / 46 / 46, none unembedded, no Type 3), /URI lists (6 in B, 3 in D, as listed), 0 hits for the seven terms, placeholder link still printed (check 6 FAIL is still true). SUBMIT_STEPS line numbers tog.tex:26 and supplement.tex:27 are right. scholarone_fields.md counts (7 figures, 5 tables, 20 references, 199 words, 106 pages) are right. "Both anonymous builds still print the placeholder" is true (tog_review.pdf Sec. XIII, supplement_review.pdf p. 1).

FAIL (stale or contradicting the current state):
1. SUBMIT_STEPS.md step 3: "anonymize_terms.txt ... was not ready ... check that the file exists". Today delegate/out/T79/anonymize_terms.txt EXISTS (645 bytes; contents not read) and dist/anon/build.py uses it (T79 path, line 25).
2. SUBMIT_STEPS.md steps 3 to 4 never mention dist/anon: an anonymous code copy now exists (dist/anon/out/cylinder-chess-review, 5,676 files, 77.3 MB, plus cylinder-chess-review.zip, 26.0 MB; dist/anon/VERIFY.md written 13:44, all checks PASS, identifier scan 0 hits). The 4open.science mirror step is therefore not the only route; the copy was built from 2be946c1, HEAD is now fc19cc80 (6 later commits, none touching dist/tog PDFs), so rerun `python3 dist/anon/build.py` only if code or the PDFs change. The copy contains the two review PDFs, whose bytes equal dist/tog's today.
3. SUBMIT_STEPS.md step 6 "copy the PDFs to dist/tog/ if they are not written there (how they got there: not verified)". Today: sbuild.sh writes only to dist/tog/build (every tectonic call uses --outdir build; no cp anywhere in sbuild.sh or tools/). dist/tog/*.pdf are byte-identical to build/*.pdf (same sha256) but were copied 14 s later by hand (build/tog_review.pdf 13:42:08, dist/tog/tog_review.pdf 13:42:22). The author must run `cp build/tog.pdf build/tog_review.pdf build/supplement.pdf build/supplement_review.pdf .` after a rebuild, or upload from build/.
4. SUBMIT_STEPS.md "Author must confirm" item 9 says the GitHub repository "is public now (made public after the audit)", while scholarone_fields.md says "the audit found it private on 2026-11-22 ... its present state is not verified", and step 15 says "make that repository public" after acceptance. Three files, two answers; no network here, so I cannot say which is true. The author must check once and edit all three.
5. SUBMIT_STEPS.md "Author must confirm" item 4 "The wording in the paper is quoted unchanged": false (see D; cover_letter.md and scholarone_fields.md drop "and checked").
6. pdf_checks.md first paragraph: "Page counts ... refreshed on 2026-11-23 (supplement 95 pages)": the supplement has 106 pages (its own table says 106). Also "Run on 2026-11-22 on the PDFs built at 17:58" is stale: the PDFs were rebuilt 2026-11-23 13:42 and the table's sizes already are the new ones. I re-ran checks 1, 2, 4, 5 today on the current files and all PASS, so the verdicts stand but the provenance sentence is wrong. SUBMIT_STEPS step 1 "checked on 2026-11-22" has the same issue.
7. files_to_upload.md "Sources" row: says only tog.tex holds the author name and GitHub URL. Also holding identifying text: tog.tex (named e-mail, affiliation, "Prof. T. Morley", pdfauthor), macros.tex:13 (\repourl = the GitHub URL, unconditional and used by 13_verify.tex:3 as fallback), supplement.tex:34-36 and :79 (GitHub URL, "A. Bhattacharjee", "Aritro Bhattacharjee"). Sending sources for review needs all of these stripped, not just tog.tex.
8. cover_letter.md "Date: 22 November 2026" (today is 2026-11-23; already marked "Author must confirm").

Still true, not verified by anyone (no change): PDF eXpress acceptance of the AppleSymbols subset fonts (SUBMIT_STEPS step 9; the fsType = 0 embedding check in pdf_checks.md is the only new fact); ScholarOne field names and upload limits; label sizes at print size; IEEE Thesaurus acceptance of the index terms.

## F. Paths cited in the supplement vs dist/anon/out/cylinder-chess-review

Scope: dist/tog/supp/s*.tex and supp_src/*. Machine list with first location: delegate/out/R15_consistency/paths.json. Bare names (for example pawns.py) were matched by file name anywhere in the copy, so a reviewer finds them only if they search; many exist in several folders (rg.c in research/odd_n_plus_2, research/ring_family_proof, research/star4_rings/two_core; graph.py, pump_verify.py, reduced_cyl.py in research/ring_family_proof and ring_n_plus_2_proof; independent.py in ring_n_check, ring_n_plus_2_check, star3_check).

Exist in the copy (36 tokens):
- Full paths: RESULTS.md, cylcgt/pawns.py, engine/suite/, kings/SPEC.md, kings/kpsolve.c, kings/theory/LOOPY.md, lemmas/common.py, research/mobius_rings_proof/PROOF.md, research/mobius_star3_family/PROOF.md, research/ring_family_proof/proof.tex, research/ring_n_plus_2_proof/PROOF.md, PROOF_Q.md, PROOF_odd.md, research/ring_n_proof/PROOF_N.md, research/star3_proof/PROOF_S3T3.md, research/v2_mechanisms/cc.py, research/v2_mechanisms/pawngame.py.
- Partial paths and bare names found by name: check3/eng.py, odd/base_cases.py, odd/check_odd.py, verify_compute/myeng.py, verify_computeOdd/oddeng.py, verify_computeOdd/run_b.py, verify_logic/engine.py, verify_logicOdd/engineD.py, verify_logicOdd/t_random.py, base_cases.py, check_odd.py, graph.py, independent.py, oddeng.py, pawns.py, pump_verify.py, reduced_cyl.py, rg.c, run_a.py.

Do NOT exist in the copy (a reviewer following them finds nothing):
- notes/lemmas.md (20 mentions, S12: "the whole-board convention game W(X) ... (notes/lemmas.md)", supp/s12.tex:502; VERIFY.md lists it as tracked but excluded).
- dsum.py (S12, supp/s12.tex:1379), sumsolve.c (:1465): only in kings/delegate/out/K21/scripts/ in the repository.
- kp_p.c (:1129): only in kings/delegate/out/K7/scripts/. pk2.c (:1129): kings/delegate/out/K23/scripts/. pyp.py (:1250): kings/delegate/out/K16/scripts/. refp.py (:800): kings/delegate/out/K17/scripts/.
- kings/kpsolve (supp/s12.tex:799, and the "kpsolve --frozen" use): the compiled binary name; the source kings/kpsolve.c exists, so say "build kpsolve from kings/kpsolve.c".
- 18 figures/*.pdf names (supp/s01 to s09 \includegraphics) are supplement build assets in dist/tog/figures, not repository paths a reader is told to open; they are in the PDF already. Not a defect.
Each of the K-folder scripts lives under kings/delegate/out, which the anonymous build excludes on purpose (logs and agent transcripts). Fix options: copy the six scripts into kings/ in the copy, or replace the file names in S12 by "the checker programs described here" and drop notes/lemmas.md in favour of "Section S12, A.I".

Supplement headings that are just a file path (supp/s15.tex) and proposed descriptive headings (from each note's own first lines; keep the path in a "Source." line as S13, S14 and S12.2 already do):
- :3 "Note 1: research/ring_n_plus_2_proof/PROOF.md" -> "Note 1: Rings of value *2 with n+2 pawns for even n>=8 (family P_n)"
- :126 "Note 2: research/ring_n_plus_2_proof/PROOF_Q.md (even n)" -> "Note 2: Rings of value *3 with n+2 pawns for even n>=8 (family Q)"
- :184 "Note 3: research/ring_n_plus_2_proof/PROOF_odd.md (odd n)" -> "Note 3: Rings of value *2 and *3 with n+2 pawns for odd n>=11 (families R_n and Qo_n)"
- :275 "Note 4: research/star3_proof/PROOF_S3T3.md" -> "Note 4: Rings of value *3 with n+1 pawns for even n>=12 and odd n>=13 (families T_n and S_n)"
- :364 "Note 5: research/mobius_rings_proof/PROOF.md (Mobius strip)" -> "Note 5: Mobius-strip rings of value *2 (families F1, F2, F3), insertion proof across the seam"
- :504 "Note 6: research/mobius_star3_family/PROOF.md (Mobius strip, *3 with n+1 pawns)" -> "Note 6: Mobius-strip rings of value *3 with n+1 pawns for n>=11 (families TT and SS)"
No other heading is only a path. The S12, S13 and S14 "Source." lines (kings/theory/LOOPY.md, research/ring_family_proof/proof.tex, research/ring_n_proof/PROOF_N.md) all exist in the copy. The supplement text "file references, which are paths in the code repository" (s12:430, s14:2) is only partly true for a reviewer, given the missing items above.

## G. Leftovers in the two anonymous PDFs: no identifying hit

Counts per term (pdftotext -layout, case-insensitive, math-italic letters normalised): aritro 0, bhattacharjee 0, uiuc 0, illinois 0, urbana 0, morley 0, /Users/ 0, "main session" 0, "Codex job" 0, K[0-9][0-9] 0; also e-mail "@" 0, "sonu" 0, "/ANON" 0.
- github.com: tog_review p. 10, refs [19] (github.com/official-stockfish/Stockfish) and [20] (github.com/LeelaChessZero/lc0): third-party, not identifying. supplement_review: 0.
- T[0-9][0-9]: supplement_review pp. 77, 80, 81, 85, 87, 89, 90, 92 (16 lines): "T18", "T19", "T20", "T12", "T10" are theorem and family labels in the proof tables (for example "T18 P_n = *2 for even n >= 18 ... PROVED given L1-L3", "T20: 1305 nodes", math symbol T_n), not job tags. Not identifying; no change needed.
- R[0-9][0-9]: pp. 76, 77, 80, 81, 87 (40 lines): "R18", "R22" are the reduced game R_n of the proofs. Not job tags.
- "delegate": p. 99, "FBoard delegates ..." (a verb about a checker program). Reads fine; not an internal note.
- "2026-1": 36 lines, supplement_review pp. 23, 24, 27, 29-34, 36, 37, 41-43, 58, 66, 104, e.g. p. 29 "(revised 2026-11-23)", p. 23 "the revisions of 2026-11-23", p. 104 "in 2026-10". They do not identify the author but read like internal change-log notes ("revised ... : the earlier wording ..."). Suggest replacing the dates by "in the final version" or deleting the revision remarks.
- Provenance (S17, pp. 103-105, plus p. 23 and p. 29) names "Claude Opus agent", "Sonnet agents", "Codex", "OpenCode", "NVIDIA (Nemotron) and MiniMax", "Kilo": tool and vendor names, consistent with the paper's AI statement; not identifying. The paper's own statement names only "open models run through the OpenCode and Kilo tools", while S17 names the vendors (informational).
- p. 106: web.stanford.edu/~wqy/... is the cited third-party URL ([10] in the paper).
- tog_review.pdf: 0 hits for every term other than the two Stockfish/Lc0 URLs; Title metadata is the paper title; Author metadata empty.
