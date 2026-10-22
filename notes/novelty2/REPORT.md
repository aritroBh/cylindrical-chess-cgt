# T29: report (agent text) with the verifier's findings

Written by the orchestrating session on 2026-10-22. The subagent could not write report files, so its
final message is reproduced verbatim under "Agent report". An independent Sonnet verifier then tried to refute
it; its verdict, summary and fix list come first and **take precedence over the agent text where they differ**.

## Verifier verdict: ACCEPT_WITH_FIXES

The agent's message holds up. Every literature fact I re-read matched, and every number I recomputed with my own programs matched the paper. The problems are that the report file was never written, and that some claims need small corrections. notes/novelty2/REPORT.md is the old unverified text. It contradicts the message on Muller, on Claim 4 and on Claim 5, so it must be overwritten. The message is also cut off after item 10. Other fixes:
- Claim 5 and the cylinder-values part of Claim 2 miss the project's own unpublished 2025 study (prior_work/main.tex, section 8), which already states the ring rule Ring(n) = mex G(n-3).
- "Only odd ranks" for Elkies 2002 is slightly too strong.
- The agent missed another T15 error: Elkies 1996 constructs tiny-one (p. 144), so it is not an open problem.
- The paper's abstract says K+R can no longer force mate without crediting prior prose.
The agent's labels (NOT FOUND, PRIOR in prose) overstate no novelty. Findings are in /Users/aritro/Downloads/Research/Chessendgames/notes/novelty2/VERIFY_T29.md, with scripts in notes/novelty2/verify_t29/.

### Fixes and problems found by the verifier

- notes/novelty2/REPORT.md is stale (mtime 00:50, written before this run) and was never overwritten. It says Muller claimed a forced bishop-pair mate and that KRK contradicts Muller; the real contradiction is KBBK against the Muller-hosted page. The agent's message is also truncated after item 10 ('24 WebFetch'). Overwrite REPORT.md from the corrected claim table at the end of VERIFY_T29.md.
- Claim 5 is labelled NOT FOUND with no mention of the project's own prior_work/main.tex (section 8, line 219): Ring(n) = mex G(n-3), 'the Grundy value for the ring is always either 0 or 1'. This is unpublished and uses a wrong recurrence, but it is the same ring rule and the paper cites it as Study2025. Correct label: PRIOR (own, unpublished) for the ring formula. The new parts are the 3xn chess derivation, the corrected g and the misere remark. The external-literature result (NOT FOUND) stands.
- Claim 2: 'no CGT value for any cylinder position' ignores the same unpublished 2025 study, which computes cylinder values. Label it RELATED; the n+3 ring-*2 rule remains NOT FOUND.
- Elkies 2002 wording: 'builds *2 only on boards with an odd number of ranks, at least 9' is slightly too strong. The abstract says m >= 9 with no parity condition. Diag. 6A and Diag. 7A/7E (pp. 70-73) are on odd heights, and p. 73 says 'longer boards of odd height >= 9'. Even heights such as 8x8 are said to need more work, not shown impossible.
- A second T15 error was missed: T15 section 4 says Elkies 1996 lists tiny(1) as open. Elkies 1996 constructs tiny-one in Diagram 9 (p. 144, with knights) and p. 148 says tiny-x for integers x >= 0 is already constructed; only 1/8 and the higher ups are asked. The paper's abstract line 'we also find ... Tiny 1' should be qualified as king-and-pawn only in the trebuchet model, or dropped.
- Claim 4 exposure in the paper: the abstract and intro state that K+R can no longer force mate on the cylinder, and that on the torus only two major pieces force mate, without citing Wikipedia, the XBoard/Muller rules page, the Chess Variant Pages or Gik. The prose is prior; only the numbers (2.80%, mate depths, 24 tables) are new. Add a citation or soften.
- Wording nuance: '16,538 ordinary-board draws become cylinder wins' counts (position, side-to-move) pairs: 9,216 white-to-move + 7,322 black-to-move. The same applies to 15,930.
- Claim 1 scope: NOT FOUND is correct, but the paper's *2 holds only in the model (count rule, e.p.-aware test, frozen kings). Real-chess oracle values for positions A and B are still open (14_conclusion.tex item 2). The summary line should say 'in the model'.
- Not independently verified by me: Chess Variant Pages text (all chessvariants.org URLs returned 403; search snippets only), Gik 1983, Winning Ways, Guy's Twopins, Plambeck-Siegel, Borna-Ashrafi. The agent's claim of 24 searches / 42 page requests is unverifiable, but my 4 searches and about 20 fetches found nothing contradicting NOT FOUND. I did not rerun the heavy ring-*2 scans for n>=4 or the seven-pawn census.

### Claims the verifier recomputed

- **agrees.** Claim: Dawson g(n) (A002187): period 34, last exception n=51, cylinder first-player wins at n=3,7,11,17,23,27,31,37,41,45,57 (g(n-3)=0)
  Recomputed: Octal-game 0.137 from its code; the paper's formula matches it for n<=400. First 40 terms equal OEIS A002187. g(n)!=g(n+34) exactly for n=14,16,31,34,51. Zeros of g give the same n list as the paper.
- **agrees.** Claim: Ring rule: the 3xn cylinder (Dawson's chess) is a first-player win iff g(n-3)=0 (the report calls this a one-line reduction)
  Recomputed: Brute-force game search on the real 3xn game (forced captures, no double step, no promotion). Cylinder n=3..12 and flat n=1..12 all agree with the rule and with g(n)!=0.
- **agrees.** Claim: Cylinder KPK: 16,538 flat draws become cylinder wins, 15,930 flat wins become draws; counts 163,328/124,960/168,024/97,604 flat and 160,656/126,736/165,984/92,760 cylinder; Ka6 Pa5 vs Ka8 flips from draw to win; mutual zugzwangs 160 and 216
  Recomputed: Own C solver with all four promotions gives exactly these counts. 16,538 = 9,216 white-to-move + 7,322 black-to-move; 15,930 = 5,126 + 10,804. Ka6 Pa5 vs Ka8 is a draw on the flat board and a win on the cylinder (25 plies white to move, 26 black to move). Zugzwangs are 160 flat and 216 cylinder.
- **agrees.** Claim: Claim 4: KQK still forces mate on the cylinder, KRK does not (2.80%, mate in 3); KBBK with opposite-coloured bishops wins 100% in 14, contradicting the Muller-hosted page
  Recomputed: Own solvers: KQK cylinder 100% / 10 moves (flat 10); KRK cylinder 2.8015% / 3 (flat 100% / 16); KBBK flat 99.9792% / 19 and cylinder 100% / 14. The Muller-hosted page says two bishops cannot force mate; the quote is confirmed.
- **agrees.** Claim: Elkies page claims: 1996 pp. 139 and 148 (*2 only on files of 6 and 7 ranks; 8x8 or larger asked as open); 2002 pp. 61-78, abstract p. 61, Diag. 6A '9 rows by 12 files' p. 70, even ranks need more work; Drummond-Cole Integers 5 #G06 Fig. 11 pp. 11-12; Nowakowski GONC5 p. 140 B3
  Recomputed: Re-read the MSRI and arXiv PDFs with pdftotext. All page numbers and quotes match. Drummond-Cole's Fig. 11 is a legal 8x8 position with Q, R, B, N and pawns. Nowakowski p. 140 B3 says 'sufficiently large chessboards'.
- **agrees.** Claim: OEIS and Muller-page quotes; Wikipedia (K+R cannot mate on the cylinder, no citation; K+Q cannot mate on a torus, citing Gik 1983)
  Recomputed: OEIS A002187 wording confirmed. Muller-hosted quote confirmed, with no author line. The Wikipedia statements are confirmed, but the Gik citation is attached to the K+Q sentence only. The Chess Variant Pages text returned 403, so I only have search-snippet corroboration.
- **agrees.** Claim: Paper's *2 values: C3 ring, C4 ring, positions A and B are *2; the a2 c2 / b7 d7 candidate is {2+-1 | -2+-1} under the e.p.-aware test
  Recomputed: Repo cylcgt engine reproduces all of these (COMPUTED-1 only, not independent). I did not rerun the C5/C6 ring counts or the seven-pawn census (shared machine).

## Agent report (verbatim)

Only the first 10 lines are the summary. The rest is the evidence, because the Write tool refused to create the report file. `notes/novelty2/REPORT.md` is therefore unchanged and still holds the old, unverified text, including the "H.G. Muller" sentence. Whoever picks this up should write the file from this message. I did not work around the refusal with Bash.

1. **Claim 1 (K+P \*2 on the 8x8 board, seven pawns plus T): NOT FOUND.** No earlier king-and-pawn \*2 on an 8-rank board turned up. The labels here are the brief's verdicts, not CHECKED-2 and the like; those apply to computations.
2. **Closest work on Claim 1 (RELATED):**
   - Elkies 2002 builds \*2 only on boards with an odd number of ranks, at least 9 (abstract, MSRI p. 61; Diag. 6A is "9 rows by 12 files", p. 70). He says an even-rank board like the 8x8 would need more work (pp. 70-71).
   - Drummond-Cole 2005 (Integers 5, #G06, Fig. 11, pp. 11-12) has a legal 8x8 position of value \*2, but it needs bishops, a knight and other pieces.
   - Nowakowski's 2017 problem list (GONC 5, Problem B3, p. 140) still states Elkies' \*k conjecture only for "sufficiently large chessboards".
3. **Correction to the brief:** Elkies 1996 does list \*2, but only on files of 6 and 7 ranks (MSRI pp. 139 and 148). It asks about \*2 on 8x8 or larger boards as an open problem (p. 148). So the brief's "lists no \*2" should read "no \*2 on an 8-rank board". The paper's wording "Elkies' higher nimbers need larger boards" is accurate.
4. **Claim 2 (first ring \*2 on Cn has n+3 pawns): NOT FOUND.** I found no CGT value for any cylinder position. The only nearby statement is the Chess Variant Pages remark that a cylinder has no edge pawns.
5. **Claim 3 (cylinder KPK, 16,538 draws become wins): NOT FOUND** as numbers or as a tablebase. The classic rook-pawn draw becoming a win is not mentioned in anything I could read. RELATED: the "no edge pawns" remark above.
6. **Claim 4: PRIOR in prose, NOT FOUND as numbers.**
   - Wikipedia "Cylinder chess" (no citation), the Chess Variant Pages (static mirror, rewritten 2019 by Greg Strong) and the rules page on hgm.nubati.net (same text on gnu.org XBoard) all say a lone rook cannot mate on a cylinder.
   - The Chess Variant Pages say a queen can still mate, as can a bishop pair.
   - Wikipedia says K+Q cannot mate on a torus but K+2R can, citing Gik 1983. I did not see Gik, so that is second-hand.
   - The paper's percentages and mate depths are NOT FOUND elsewhere.
7. **The Muller claim:** I found nothing saying a bishop pair mates on the cylinder. The Muller-hosted page says the opposite, in a sentence I can quote: "Two Knights and Bishops in any combination cannot do that either." The page has no author line; Wikipedia cites it for "piece values according to H. G. Muller". The paper's KBBK row (opposite-colour bishops win 100%, mate in 14) therefore contradicts that page and agrees with the Chess Variant Pages. KBNK and KNNK agree with both.
8. **Claim 5 (3xn cylinder Dawson's chess): NOT FOUND, and a one-line reduction.**
   - Nothing on a cylinder or ring version in the Ferguson note, Plambeck-Siegel (text searched), Borna and Ashrafi Payaman 2013 (abstract only), OEIS A002187 or Guy's "Twopins" (OCR of a scan, moderate confidence).
   - OEIS confirms the paper's "period 34, last exception 51".
   - Winning Ways was not read.
9. **Errors in earlier notes.** `notes/novelty_check/REPORT.md` (T15) has:
   - Two paraphrases presented as Elkies 1996 quotes (the \*2 and 1/8 questions); the real p. 148 text differs.
   - Drummond-Cole described as "likely the same construction as Elkies 2002".
   - Elkies 2002 given as "pp. 1-21, 2000" (correct: pp. 61-78, 2002).
   - The Muller claim recorded as "KBBK is a forced mate". `notes/lit_cylinder.md` has Muller's actual claim right.
10. **Limits and effort.** There was no Google Scholar, MathSciNet or citation-graph access, so "NOT FOUND" means "not found by the 24 searches". 42 page requests were used (24 WebFetch, 18 curl; the cap was 60). Downloaded PDFs and pages are in the session scratchpad only. No project files were written, and no heavy processes were run.

## Evidence and locators

**Elkies 2002.** Printed MSRI pages (PDF page + 57):
- p. 61: abstract, "m >= 9".
- pp. 62-63: section 2 has two composed 8x8 positions with values 0 and \*. Footnote 2 says they are not pawn endgames.
- p. 64: the pawns game has no double step and no en passant.
- p. 71: any pawn game of length n embeds in a board of at least n+6 files with odd height greater than 5.
- pp. 71-73: Diag. 7A and the \*2 component [1000] on files a-d. It needs four extra immobile a-file pawns (p. 72). The board is 9x12, inferred from "replaced the component [5] of Diag. 6A". The conclusion on p. 73 says odd height at least 9.
- p. 76: [1000] is the shortest word with value \*2.

**Elkies 1996.** Printed pages (PDF page + 134):
- p. 139: a file with both pawns on their initial squares has value \* at width 5 and \*2 at width 6.
- p. 140: Diagram 4 is analysed with an en passant trade.
- p. 148: the open problems. The en passant item asks for a "more systematic CGT-style treatment of en passant". The paper's e.p.-aware passed-pawn test answers that, so it is worth citing.

**Unsolved problems lists, Problem B3 "Chess".** Same wording in all three: GONC 3 p. 476, GONC 4 p. 291, GONC 5 p. 140.

**Wu, Yü, Landry 2010.** The abstract lists the values they found, and \*2 is not among them. A text search for "\*2" and "nimber" finds nothing.

**URLs that gave readable text:**
- Wikipedia: `https://en.wikipedia.org/w/index.php?title=Cylinder_chess&action=raw`
- `https://static.chessvariants.org/boardrules.dir/cylindrical.html` (the `.org` and `.com` hosts return 403)
- `http://hgm.nubati.net/rules/Cylinder.html`
- `https://www.gnu.org/software/xboard/whats_new/rules/Cylinder.html`
- `https://mayhematics.com/v/cylin.htm` (Jelliss; rules and problems only)
- `https://library.slmath.org/books/Book29/files/elkies.pdf`
- `https://library.slmath.org/books/Book42/files/elkies.pdf`
- `https://library.slmath.org/books/Book70/files/1005.pdf` (GONC 5; GONC 4 is Book63, GONC 3 is Book56)
- `https://math.colgate.edu/~integers/fg6/fg6.pdf` (the emis mirror returned 503)
- `https://www.math.ucla.edu/~tom/papers/unpublished/DawsonChess.pdf`
- `https://arxiv.org/pdf/math/0609825`
- `https://oeis.org/A002187`

**Suggested wording, not applied (I did not edit `paper/`):**
- State Claim 1 as "to our knowledge, in the model".
- Cite the Chess Variant Pages, Wikipedia and the Muller-hosted page for the KRK/KQK folklore, and say the paper's KBBK result corrects the Muller page.
- Credit Gik 1983 (via Wikipedia) for torus K+Q.
- Make the indexing explicit where the Dawson section says "strips of at most 32 files". Plambeck-Siegel's quotient is Q33(0.07), 0.137 on n files has the normal-play values of 0.07 on n-1 pins, and I did not check this further.

**Possible mismatch with the paper (not in the brief):** the brief names `06_atlas.tex`, but the n+3 ring rule is in `08_star2.tex` (the Counts and Five Files subsection). The atlas file only supports it indirectly.
