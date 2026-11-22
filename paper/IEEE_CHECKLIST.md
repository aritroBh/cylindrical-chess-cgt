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
- [ ] Balance the last page once the two result slots are filled
- [x] Title: the original title on both versions (author decision)
- [x] Author block: University of Illinois Urbana-Champaign (ORCID optional, add in the submission system)
- [ ] Push to the public repository (on the author's word)

## Results being added
- [x] Twisted tablebases audited: paper numbers stand (`research/mobius_repair/`)
- [x] Old *2 discrepancy explained: sum model vs whole board (`research/star2_frontier_recheck/`)
- [~] Real-king test of the sum theorem (`research/sum_truth_cyl/`)
- [~] Sum vs whole-board value for every ring family (`research/sum_vs_whole_families/`)
- [x] How often sum and whole board differ, by race rule (`research/sum_whole_census/`): 599,098 positions; never
  when hereditarily sum-safe, 19.3% of the rest; in Section V of both versions
- [~] New: pawn rings on the Möbius strip, least *2 (`research/mobius_rings/`)
- [ ] Seven-pawn *2 in real chess: the 9-man end positions (waits for memory)

## Figures
- [x] Signature figure: the one-pawn-per-file ring drawn on a cylinder (`research/figures_2026_11/f1_ring_cylinder_wide.pdf`)
- [x] Least pawns in a ring against n (`f2_least_pawns.pdf`)
- [x] Model against real chess, with confidence intervals (`f3_model_vs_chess.pdf`)
- [x] Cylinder ring and least-pawns figures in the 10-page text; model-vs-chess figure in the supplement
