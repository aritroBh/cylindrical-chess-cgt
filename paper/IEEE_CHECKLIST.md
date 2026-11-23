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

- [x] R1 (Opus): re-referee appendix S12.1 items A.1 to A.9 after the last-rank convention was adopted
  (`delegate/out/R1_appendix_reread/REPORT.md`): sound, four minor wording fixes applied; its own brute force
  (flat boards up to 5 files by 6 ranks, all nine settings, at most 2+2 pawns, and 3+3 in the default setting) finds
  no difference between S and W under the hypotheses, and its split-first control does differ
- [x] R2 (Sonnet): audit every pointer from the 10-page paper into the supplement (hard-coded S numbers), every
  label, and the submission files against the current PDFs (`delegate/out/R2_xref_audit/REPORT.md`): 26 pointer groups checked, no
  broken reference or `??`; findings were stale text in supplement S3, S4 and S10 (frozen long-version lines), in the
  README and in two submission files, one intro claim missing from the body (n+1 pawns on C11), and two vague pointers
- [x] R5 (Sonnet): applied the R1 and R2 fixes (13 edits decided by the main session) and rebuilt; diff reviewed and
  checks rerun by the main session (10 pages with 0.32 in spare, supplement 95, numbers and anonymity pass)
- [x] R3 (Opus): is there a family of *3 rings on the Möbius strip, as on the cylinder? YES: n+1 pawns for n = 9, 11
  and every n >= 12. Families TT (even n >= 12) and SS (odd n >= 11) are the cylinder's T_n and S_n with the seam at
  one particular file; two programs agree to n = 32 and 31. n = 10 with 11 pawns open (12 pawns found).
  (`research/mobius_star3_family/REPORT.md`)
- [x] T87 (Codex): independent checker written; its sandbox refused the priority change, so I ran it (60 s,
  134 MB): both base graphs agree exactly (1305/4018/1212 and 22755/72730/49694, zones, NNNPN), both insertion
  steps are isomorphisms, TT m = 0..4 and SS m = 0..5 as claimed (`delegate/out/T87/run_all.log`). C1 is CHECKED-2
- [x] R13 (Opus): proof note `research/mobius_star3_family/PROOF.md` (96 lines). The plan holds without repair: V and
  Lemmas 2, 3 of Note 5 never use the contents of a file outside the arc, so the zone file across the seam does
  no harm; fallback base m0 = 6 for TT if a referee doubts it
- [x] T88 (Codex): holds with fixes, no blocker; seam argument confirmed; one false sentence corrected; 7 fixes applied
- [x] Supplement S15 Note 6, S6.4 paragraph, S17 row; one clause in Section VIII of the 10-page paper (fits; 0.32 in
  spare) and a sentence in the long version. Supplement 106 pages
- [x] R4 (Haiku): recount the facts in `dist/tog/submission/` (pages, hashes, words in the abstract, references,
  figures, tables) from the built PDFs (`delegate/out/R4_submission_facts/REPORT.md`): all match except one stale page count
  (82, now 95) in `pdf_checks.md`, fixed
- [x] R6 (Opus): a fresh hostile mock review of the anonymous paper and supplement, formed without reading earlier
  reviews (`delegate/out/R6_mock_review3/REPORT.md`): recommends major revision. Its spot checks of the sum-safety
  proof and the ring proofs found them sound. Wording fixes go to R9. For the author to decide: the proofs labelled S
  have been checked only by AI models (M3); Table I corrects an unpublished study reviewers cannot see (M4); the
  supplement names the code package, which can be searched while the repository is public (anonymity)
- [x] R7 (Sonnet): audit the 15-page long version against the 10-page version, statement by statement
  (`delegate/out/R7_long_version_audit/REPORT.md`): the long version's certificate clauses differ from the precise
  ones, one Möbius *3 result is missing, and the conclusion (and supplement S10) wrongly called the least Möbius ring
  for n >= 12 open (it is n, since one pawn per file suffices). Fixes go to R9
- [x] R9 (Sonnet): applied the accepted R6 and R7 fixes to both versions and rebuilt; diff reviewed and builds rerun
  by the main session. 10-page paper: 10 pages (0.32 in spare), supplement 95. The long version's named build is now
  16 pages (anonymous 15); it has no page limit. Not applied: one rewrite in Section IX that pushed the paper to 11
  pages. The agent also corrected the audit: the 10-page paper has 14 sections, so "Sections II--XIII" was right
- [x] R10 (Sonnet): per-result record of who wrote and who checked each S proof, and which programs computed its
  finite parts (`delegate/out/R10_provenance/TABLE.md`). It shows uneven checking: several final texts were never
  re-read after their fixes, and Note 2 of S15 was rewritten by its only other-vendor referee
- [x] T83 (Codex): re-read the FINAL text of appendix A.10 to A.17 and of the Möbius note (S15 Note 5).
  Verdict: appendix GAP (A.16 timing clause false: the reply itself can mate while the projected position is
  live; counterexample checked with python-chess; the promotion-game win stands), Möbius note sound with
  fixes. 1 blocker, 1 major (A.14 needs the race rule), about 25 minor wordings (`delegate/out/T83/`)
- [x] Apply the T83 fixes to `s12a_core.tex` and `s15_note5.md` (Sonnet), review, rebuild (supplement 95 pages)
- [ ] Kings session: same timing clause in LOOPY Theorem 2.7 (line 1008); sync `s12_kings.md` after its commit
- [ ] Free coding tools as extra referees of final texts (asked by the author on 2026-11-23). Working: Codex,
  Kilo (nemotron-3-ultra, flint, openrouter/free, ling), OpenCode (beam-free). Not working today: agy (quota,
  about 76 h), Cursor (out of usage), muse (billing), qwen (no login), OmniRoute free routes (upstream
  unavailable or limit reached).
  - [x] T84k (Kilo nemotron-3-ultra): no report. It spent 30 minutes debugging its own solver and then hit Kilo's
    free limit. Not counted.
  - [x] T84o (OpenCode beam-free): S14 and Note 4 final texts sound, two minor wordings (one applied). Its own
    solver, which I reran, rebuilds the base graphs of M_18 and T_20 exactly and the smallest members' signatures
    (`delegate/out/T84_opencode/`). The Codex read T84 follows T88
  - [x] T85 (OpenCode beam-free): S12.1 A.1 to A.9, sum safety. Verdict SOUND WITH FIXES. Its own solver:
    11,577 positions under the hypotheses (3 to 5 files, 5 or 6 ranks, at most 4 pawns, e.p.-aware), 0 mismatches
    between W and S; 4,641 more with the opponent race rule, 0. Its one major point (older e.p. rights kept in a
    sum) is already handled by the proof (Lemma A.4(a) drops the unusable right at each step); one sentence added
    to say so. A claim that Reach(X) is alternating play is wrong (line 111: any order). (`delegate/out/T85_opencode/`)
  - [x] T85k (Kilo flint): exited without a report (the model stopped after reading); not counted
  - [x] T86 (Kilo openrouter/free): exited without a report; rerun as T86o on OpenCode beam-free: Notes 1 and 3
    sound with fixes. It read the proofs and recomputed only structural facts (pawn counts, insertion of the
    roots, cuts, zones), not the graphs. Accepted: Note 3's scope sentence contradicted the status line I had
    updated (fix: both now record the Codex referee T63); an undefined family letter in Note 1; a missing pointer
    for Q_n. Not accepted: its weaker wording for T63 (Codex did check the hand proof) and a point about program
    D that the note already discloses (`delegate/out/T86_opencode/`)
- [x] T84 (Codex): re-read the FINAL text of S14 and S15 Note 4: both SOUND WITH FIXES, no blocker; theorems stand.
  Corrected: M_10's reduced graph is an exception to the stable counts (465 nodes, not 441); a claim about failing
  control cuts for O; a colour-reversal argument that assumed its conclusion; "=" should be the restricted outcome
  test (and Codex shows it does give equality with the nimber); who computed what. Its own program recomputed all
  four base graphs (441, 2,132, 1,305, 40,445 nodes), the fixed-cut steps and every small width
  (`delegate/out/T84/`). Fixes applied (Sonnet), reviewed, two leftover sentences reconciled; rebuilt
- [x] R11 (Opus): independent referee of the FINAL text of S15 Note 2 (the *3 with n+2 pawns, even n): sound with
  fixes, all minor; its own engine reproduced the base graph (7,968 nodes) and the small widths
  (`delegate/out/R11_note2_referee/`). Fixes applied (Sonnet), reviewed, rebuilt
- [ ] Kings session asked for the checker record of its theorems and an other-vendor check of Theorem 3.4
- [x] R12a: wording the record does not support: Section XIII now "programs ran the ring base cases" (a longer
  wording costs a page in the named build), acknowledgment "wrote and checked the proofs", Note 3's status line
  (Codex T63 on record), label on the theorem of S13 ("given the computed facts C1 and C2")
- [x] R12b: supplement Section S17 "Who Wrote and Who Checked the Proofs" (two tables, what the checks found,
  limits), drafted by a Sonnet agent from the provenance record, reviewed and corrected. Supplement 99 pages
- [x] Kings Theorem 2.7 repair (commit 39e19a98) ported into `s12_kings.md` (5 of 7 edits; the copy has no status rows)
- [x] Appendix remark "(E) cannot be dropped": `W a4 b3 e2 / B a5 b4 e4` after a2-a4 on the flat 5x7 board, W = N,
  S = R, HSS holds; hand proof, engine and a separate minimax agree in all six settings (found by Codex K52)
- [x] Kings K51/K52 repairs (commit 62ae99cc) ported into `s12_kings.md` by a Sonnet agent: 22 passages applied, 7
  status rows not in the copy; S17 row and the copy's first line updated. Supplement 101 pages
- [x] Kings K54 (Codex read of the printed new proof of 1.11(c) and of the repaired 2.7): every step sound, wording
  fixes only; S17 updated
- [x] K54 wording edits (kings commit 5a7e0978) ported: 7 of 11, the rest are status rows the copy does not have
- [x] R8 (Haiku): bibliography consistency check of both .bib files and the rendered reference list: 20 references,
  numbered in order of first citation, no missing key, no broken entry, both .bib files identical. No change made: the
  DOIs it called duplicated are printed from the note field (the style does not print the doi field)
- [x] 12-file Möbius scan: stopped on purpose at 50 of 128 chunks (one *2, the family member). It no longer decides
  anything: one pawn per file is proved to suffice for n >= 10, so the least is n. Resumable (`logs/restart_notes.log`)

## Figures
- [x] Signature figure: the one-pawn-per-file ring drawn on a cylinder (`research/figures_2026_11/f1_ring_cylinder_wide.pdf`)
- [x] Least pawns in a ring against n (`f2_least_pawns.pdf`)
- [x] Model against real chess, with confidence intervals (`f3_model_vs_chess.pdf`)
- [x] Cylinder ring and least-pawns figures in the 10-page text; model-vs-chess figure in the supplement
