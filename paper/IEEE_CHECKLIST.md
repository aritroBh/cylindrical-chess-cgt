# IEEE-ready checklist

Target: IEEE Transactions on Games. Updated 2026-11-22. `[x]` done, `[~]` running, `[ ]` open.

## Format and submission
- [x] IEEEtran journal class, abstract under 200 words, index terms
- [x] All 19 references checked against publishers
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
- [ ] Balance the last page (named build is now nearly level: 747 and 719 pt; anonymous 748 and 624 pt); redo after the Möbius text is final
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
- [x] Supplement S3.4 added: the census table by rule and test, and the 19-row table of the real-king sum test; 81 pages
- [x] Submission package (`dist/tog/submission/`): cover letter, ScholarOne fields, upload table, steps for the author.
  PDF checks pass on all four files: US Letter, every font embedded, no Type 3 fonts, no raster images, no author
  name in the anonymous text, metadata or links; abstract 197 words. One fail, the author's: the anonymous code link
  is still the placeholder (`\anoncodeurl`, `tog.tex` line 26 and `supplement.tex` line 27). Not run: IEEE PDF eXpress
- [~] Reviewer's-eye audit by Codex: README reproduces from a clean copy; term list for the anonymous copy (`delegate/out/T79/`)

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
- [~] Möbius rings on 9 to 12 files and their families (`research/mobius_rings_n/`)
- [~] New: the pawn game on boards of 5 to 12 ranks; least pawns for *2 and *3 by height, search for a *4 (`research/tall_boards/`)
- [ ] Seven-pawn *2 in real chess: the 9-man end positions (needs about 26 GB; waits for the author's word)
- [ ] Zero sums with real kings at depth 2 (needs more than 12 GB per run; waits for the author's word)

## Figures
- [x] Signature figure: the one-pawn-per-file ring drawn on a cylinder (`research/figures_2026_11/f1_ring_cylinder_wide.pdf`)
- [x] Least pawns in a ring against n (`f2_least_pawns.pdf`)
- [x] Model against real chess, with confidence intervals (`f3_model_vs_chess.pdf`)
- [x] Cylinder ring and least-pawns figures in the 10-page text; model-vs-chess figure in the supplement
