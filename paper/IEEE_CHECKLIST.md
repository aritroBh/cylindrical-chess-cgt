# IEEE-ready checklist

Target: IEEE Transactions on Games. Updated 2026-11-22. `[x]` done, `[~]` running, `[ ]` open.

## Format and submission
- [x] IEEEtran journal class, abstract under 200 words, index terms
- [x] All 19 references checked against publishers
- [x] Two references added and checked against Crossref (2026-11-23): Thompson 1986 (retrograde analysis) and
  Tomašev et al. 2022 (rule changes to chess with AlphaZero); 20 references in the 10-page version
- [x] 29 referee findings applied; facts match the research reports
- [x] AI-use statement in the Acknowledgment
- [x] Anonymous review build (14 pages) and named build (15 pages)
- [x] arXiv package passes its rule checks
- [x] Full IEEE ToG compliance audit (`delegate/out/ieee_audit/AUDIT.md`)
- [x] Plan to reach the 10-page limit, rest to a supplement (`delegate/out/ieee_audit/PLAN_10_PAGES.md`)
- [x] Audit fixes applied: evidence labels no longer look like citations, abbreviations defined, AI statement names
      systems and sections, review build says "the authors", caption and unit style, build files refreshed
- [x] DOIs added to five references, each checked against Crossref
- [x] Board labels at 8 pt or more in the 10-page version
- [ ] Anonymous code link for reviewers (anonymous.4open.science; the author creates it)
- [x] 10-page version built: 10 pages with references, 4.4 column-inches free (`dist/tog/`, PDFs in `paper/`)
- [x] Supplement built: 87 pages, moved material and the full proofs
- [x] Independent check of the 10-page text: 4 blockers and 9 should-fix items found and applied (`delegate/out/tog_review/REPORT.md`)
- [x] Supplement cleaned: 83 pages, no overfull lines, working-note residue stripped
- [x] Supplement proofs (S12, S14, S15): hand-edited copies in `dist/tog/supp_src/` replace the automatic clean-up;
  80 pages. S16: the square-rule proof was false (counterexample found); it now gives the test, the checks and
  the counterexample
- [x] Last page: both builds at 10 pages; named build ends 747 and 719 pt (about two lines spare), anonymous 748 and 647 pt
- [x] Title: the original title on both versions (author decision)
- [x] Author block: University of Illinois Urbana-Champaign (ORCID optional, add in the submission system)
- [ ] Push to the public repository (on the author's word)
- [x] Second mock review of the 10-page text (`delegate/out/tog_review2/REPORT.md`): 5 blockers and 12 should-fix items.
  Applied: conclusion no longer mixes the 8x8 accuracy with the six-rank square-rule result; the 92.5% now gives its
  pool (2,154 positions, 105 draws); real-king test says queen promotions only; Möbius counts labelled; FEN defined;
  the paper now says AI models wrote the full proofs (label definition, Section XIII, Acknowledgment); supplement S10
  and S6.4 corrected. Not applied: dropping the Wikipedia citation (it is a source of the claim we correct), the
  shorter title (author decision), a new supplement section with the two Section V tables (open)
- [x] King-claim audit by the kings session, 14 fixes applied: the certificate now needs the defender not to be
  stalemated; trébuchet zero stated as 'when alone'; Puzzle 2 on the cylinder is C2; supplement S12 brought up to date
- [x] Long version: broken cross-reference in the conclusion fixed (it printed ??)
- [x] Third referee report (kings session, `paper-referee-2026-11-22.md` in the shared notes): applied the square-rule
  scope (52 repairs hold with frozen kings, 31 with real kings; the rule is not sound on every board), six settings
  not nine in Section VI, the abstract's wording on frozen kings (199 words), a caption label and three stale report
  headers. The sum cross-check was rerun with both sides e.p.-aware: 0 of 2,483,775 pairs differ, so the sentence in
  Section XIII stands and now has a log. Open: further prior-work references (Syzygy, fairy-chess generators, CGSuite) if space allows
- [x] Supplement S3.4 added: the census table by rule and test, and the 19-row table of the real-king sum test; 81 pages
- [x] Submission package (`dist/tog/submission/`): cover letter, ScholarOne fields, upload table, steps for the author.
  PDF checks pass on all four files: US Letter, every font embedded, no Type 3 fonts, no raster images, no author
  name in the anonymous text, metadata or links; abstract 197 words. One fail, the author's: the anonymous code link
  is still the placeholder (`\anoncodeurl`, `tog.tex` line 26 and `supplement.tex` line 27). Not run: IEEE PDF eXpress
- [x] Reviewer's-eye audit by Codex (`delegate/out/T79/REPORT.md`): README now has a setup step; the cross-check runs
  under both passed-pawn tests and all 1,070 single components agree under each; 18 raw CLI transcripts untracked
- [ ] Privacy: two files already on the public repository hold personal material (`kings/delegate/logs/K8.log`,
  `K13b.log`); purge from history and force-push, or make the repository private (author's word)
- [x] Anonymous code copy built by `dist/anon/build.py`: 5,568 files, 77 MB (25 MB zipped), in `dist/anon/out/`
  (not tracked). All 24 checks in `dist/anon/VERIFY.md` pass: no identifier in any file, PDF or archive member; tests,
  `verify_paper`, the cross-check, the tablebase build and the king-and-pawn solver all run from a fresh copy. Files
  over 5 MB and all logs are left out. Still the author's: put the copy in a new repository and create the
  anonymous link

## Results being added
- [x] Twisted tablebases audited: paper numbers stand (`research/mobius_repair/`)
- [x] Old *2 discrepancy explained: sum model vs whole board (`research/star2_frontier_recheck/`)
- [x] Real-king test of the sum theorem (`research/sum_truth_cyl/`): 19 sums, 19 of 38 positions exact and all agree, the rest bounded; in Section V of both versions
- [x] Sum vs whole-board value for the ring families (`research/sum_vs_whole_families/`): equal in all 24 pairs
  solved in both models (n <= 11); confirms the text, no change needed
- [x] How often sum and whole board differ, by race rule (`research/sum_whole_census/`): 599,098 positions; never
  when hereditarily sum-safe, 19.3% of the rest; in Section V of both versions
- [x] New: pawn rings on the Möbius strip (`research/mobius_rings/`, checked by Codex in `research/mobius_rings_check/`):
  least *2 is 6, 8, 6, 8, 8, 8 for n = 3..8; in Section VIII of both versions and Section S6 of the supplement
- [x] Möbius rings on 9 to 11 files and their families (`research/mobius_rings_n/`): least *2 is 10, 10, 11, the same
  as the cylinder; one pawn per file works on 8 files, not on 9, and from 10 to 32 in two families; in Section VIII
  of both versions, supplement S6.4 (82 pages) and the conclusion. The 12-file scan is still running
- [x] Self-contained proofs of the four S results (supplement S12.1, `dist/tog/supp_src/s12a_core.tex`): refereed by
  Codex T81 and the kings session's referee A, fixes applied; the paper's description of the sum model corrected
  (test for a passed pawn before splitting); supplement 95 pages. Kings referee B (sum safety) applied too: a pawn on
  its last rank counts as passed, as in the engine, so no height condition; the long kings note was repaired to match
- [x] Möbius families proved *2 for every width (`research/mobius_rings_proof/`, Codex referee T82 holds with two
  wording fixes, base case recomputed independently): one pawn per file suffices on every strip of 10 or more files,
  label S; in Section VIII of both versions, supplement S6.4 and S15 Note 5; the open question left the conclusion
- [x] New: the pawn game on boards of 5 to 12 ranks (`research/tall_boards/`): no *4 in 1.8 billion positions; *2 with
  four pawns and *3 with six on seven ranks; none on five ranks; in Section VIII of both versions, supplement S6.5
  and the conclusion. To fit, the two-core remark moved to the supplement only and five supplement pointers were shortened
- [x] Engines on sums: the 200-position test was flawed (king group among the pawns in 163; illegal winning moves;
  27 positions Stockfish rejects). Claim withdrawn from Section XII and the introduction of both versions; the
  suite table stands. A clean rerun is open
- [x] Independent Codex check of the height results (T80): the complete scans for 5 and 6 ranks and 3 files on 7
  ranks agree in every nimber count and minimum; the named positions agree; labels raised to C2 for those
- [ ] Seven-pawn *2 in real chess: the 9-man end positions (needs about 26 GB; waits for the author's word)
- [ ] Zero sums with real kings at depth 2 (needs more than 12 GB per run; waits for the author's word)

## Round of 2026-11-23 (Fable plans and reviews; Opus, Sonnet and Haiku agents do the work)

- [ ] R1 (Opus): re-referee appendix S12.1 items A.1 to A.9 after the last-rank convention was adopted
  (`delegate/out/R1_appendix_reread/REPORT.md`)
- [ ] R2 (Sonnet): audit every pointer from the 10-page paper into the supplement (hard-coded S numbers), every
  label, and the submission files against the current PDFs (`delegate/out/R2_xref_audit/REPORT.md`)
- [ ] R3 (Opus): is there a family of *3 rings on the Möbius strip, as on the cylinder? (`research/mobius_star3_family/`)
- [ ] R4 (Haiku): recount the facts in `dist/tog/submission/` (pages, hashes, words in the abstract, references,
  figures, tables) from the built PDFs (`delegate/out/R4_submission_facts/REPORT.md`)
- [ ] 12-file Möbius scan: summarise when all 128 chunks are done (47 done on 2026-11-23, one *2 so far, the
  family member with one pawn per file)

## Figures
- [x] Signature figure: the one-pawn-per-file ring drawn on a cylinder (`research/figures_2026_11/f1_ring_cylinder_wide.pdf`)
- [x] Least pawns in a ring against n (`f2_least_pawns.pdf`)
- [x] Model against real chess, with confidence intervals (`f3_model_vs_chess.pdf`)
- [x] Cylinder ring and least-pawns figures in the 10-page text; model-vs-chess figure in the supplement
