# W1 supplement and submission fixes (2026-11-23)

All edits by Python exact-string replacement with count assertions (/tmp/t1.py ... t4.py). Nothing committed or staged. No PDF copied out of dist/tog/build/.

## Task 1: S15 headings (dist/tog/tools/build_supplement.py, lines 380-385)
Each \subsection title is now descriptive; the path moved to the first line under it as `\noindent\emph{File in the code repository:} \texttt{<path>}.\par`.
- Note 1: Rings of value *2 with n+2 pawns, even n>=8, and the full proof of Lemma 3 (matches note: P_n, even n>=8, section 2b writes out Lemma 3)
- Note 2: Rings of value *3 with n+2 pawns, even n>=8 (matches)
- Note 3: Rings of value *2 and *3 with n+2 pawns, odd n>=11 (matches)
- Note 4: Rings of value *3 with n+1 pawns, n>=12 (matches: even n>=12, odd n>=13)
- Note 5: DEVIATION. The note proves F1 (n pawns), F2 (n pawns) and F3 (n+1 pawns), so "one pawn per file" is false for F3. Heading used: "The Moebius strip: rings of value *2 with n or n+1 pawns". (Section S17's table, supp_src/s17_provenance.tex:107, still says "one pawn per file"; left alone, you may want to align it.)
- Note 6: The Moebius strip: rings of value *3 with n+1 pawns, n>=11 (matches)
References by old path titles: none found (grep in sections, supp_src, tools, tog.tex). Other text refers to "Note k of Section S15" only.

## Task 2
(a) notes/lemmas.md: NOT included, nothing changed in dist/anon/build.py or the supplement. grep hits (case-insensitive): line 3 "Written 2026-10-15 to 16 by Claude (Opus) for the continuation of ..."; lines 36, 354, 409, 537 name "Codex" (e.g. "Codex's independent crosscheck/minimax.py"). Other terms: 0 hits (aritro, bhattacharjee, uiuc, illinois, urbana, morley, /Users/, @, session). Note also that dist/anon/build.py has `notes/` in EXCLUDE_PREFIXES (a hard exclusion), so adding a whitelist entry alone would not include it. Options for you: edit lines 3, 36, 354, 409, 537 of notes/lemmas.md (agent names are not identifying per the R15 audit) and then allow notes/lemmas.md in build.py, or change the ~20 supplement mentions.
(b) In supp_src/s12_kings.md, first mention of each program got "(not in the code copy; available on request)": kp_p (line 73, merged into the existing parenthesis: "(not in the code copy; available on request; its flag is `--pmodel`; ..."), refp.py (639), pk2.c (1240), pyp.py (1520), dsum.py (1701, its first mention; the audit listed 1863 as first), sumsolve.c (1863). Descriptions kept.
(c) `kings/kpsolve --frozen` (line 638) -> "`kings/kpsolve.c` with `--frozen`"; `kings/kpsolve` (743) -> `kings/kpsolve.c`.

## Task 3: revision-history phrasing, all in supp_src/s12_kings.md (36 edits, 0 remaining "2026-11-23" or "revised")
Format: line (old numbering) before -> after.
- 1: "the new proof of its move-count step, revised 2026-11-23, was re-derived" -> "... step was re-derived"
- 1: "Theorem 1.14 (the statement, the sharp form and the revisions of 2026-11-23)" -> "(the statement and the sharp form)"
- 27: "(revised 2026-11-23: the earlier "defined on every board height" was too wide;" -> "(the earlier ..."
- 185: "(revised 2026-11-23: the earlier "<= 6p in general" is false" -> "(the earlier ..."
- 190: "needs this reading; revised 2026-11-23: the new frontier step also projects" -> "needs this reading; the frontier step also projects"
- 198: "Pawn threats tau_P (revised 2026-11-23)." -> "Pawn threats tau_P."
- 248: "(the frontier step re-proved, revised 2026-11-23)" -> "(the frontier step re-proved)"
- 256: "(revised 2026-11-23: this is what the program ..." -> "(this is what the program ..."
- 262: "(E) cannot be dropped (revised 2026-11-23)." -> "(E) cannot be dropped."
- 283-284: "remains OPEN (revised 2026-11-23); the flag-free" -> "remains OPEN; the flag-free"
- 293: "(revised 2026-11-23: "a multiset of frozen integers +-B" missed the spent stacks)" -> "("a multiset ..." would miss the spent stacks)"
- 298: "Frontier (re-proved, revised 2026-11-23)." -> "Frontier (re-proved)."
- 305: "A model of another vendor (2026-11-23) then read" -> "A model of another vendor then read"
- 307: "in the text (revised 2026-11-23). PROVED.)" -> "in the text. PROVED.)"
- 314: "(revised 2026-11-23, wording: if a surplus right" -> "(in words: if a surplus right"
- 358: "(revised 2026-11-23: the earlier justification ..." -> "(the earlier justification ..."
- 377: "(revised 2026-11-23: an earlier clause, ..." -> "(an earlier clause, ..."
- 382: "(Revised 2026-11-23. An earlier text bounded" -> "(An earlier text bounded"
- 392: "... uniform statement (revised 2026-11-23)." -> "... uniform statement."
- 413: "(revised 2026-11-23: this said "the either-player tau", which differs" -> "(this is not "the either-player tau", which differs"
- 454: "M <= (H - 2)p (revised 2026-11-23)." -> "M <= (H - 2)p."
- 478: "(Definition 1.10; revised 2026-11-23: tau_P, as in" -> "(Definition 1.10: tau_P, as in"
- 488: "(Revised 2026-11-23: if the convention already credits" -> "(If the convention already credits"
- 503: "(Revised 2026-11-23: this used to be called a tautology; (A_Q)(X) is only" -> "(This is not a tautology: (A_Q)(X) is only"
- 523: "so the two entries agree (revised 2026-11-23)." -> "so the two entries agree."
- 639: "Theorem 1.11(c), revised 2026-11-23)" -> "Theorem 1.11(c))"
- 680: "gives o(S) != D; revised 2026-11-23);" -> "gives o(S) != D);"
- 839-840: " (earlier wording: "s queens on its T-th move")" -> deleted (pure change-log; no mathematics lost). DOUBT: you may prefer to keep it.
- 864: "(Revised 2026-11-23 after a re-read by a model of another vendor: the earlier wording" -> "(A re-read by a model of another vendor showed that the earlier wording"
- 912: "(revised 2026-11-23: the earlier "pi(R) is unchanged ..." -> "(the earlier ..."
- 960-961: "(Step 6) (revised 2026-11-23)." -> "(Step 6)."
- 962: "Step 6: s wins in time. (revised 2026-11-23) A mate" -> "... A mate"
- 985: "PROVED. (revised 2026-11-23)" -> "PROVED."
- 1668: "exists (revised 2026-11-23, after a re-read by" -> "exists (after a re-read by"
- 1959: "need never pass; revised 2026-11-23: "never passes" was too strong," -> "need never pass: "never passes" is too strong,"
- 1964: "exists" (revised 2026-11-23)." -> "exists"."
Left unchanged and listed (in doubt):
- s12_kings.md: "the earlier proof of Theorem 1.11(c)" (line 1) and "An earlier proof charged every later opponent move ..." (~300): they describe a gap that was fixed, no date; kept as mathematics.
- s15_note1/3.md "repaired definition of pattern file", s15_note1.md:109 "The only repairs are precisions": statements about a definition differing from S13; kept.
- s16_square.md:1 and :17 "the repair of the main text": a different sense (the sweep), kept.
- s17_provenance.tex: line 1 (TeX comment with date, not printed), line 33 "it now holds per side to move, and the text was corrected", line 44 "Drafts by Claude (Opus) in 2026-10, revised by free models" (printed p. 104; a provenance date, you may want "October 2026"), lines 45, 51, 98 "repairs"/"repaired". Section S17 untouched, as instructed.

## Task 4: dist/tog/submission/
- AI-use: scholarone_fields.md (named and review versions) and cover_letter.md now read "wrote and checked the proofs of Sections S12-S15" (the paper, tog.tex:139-153, with the dash style of the two md files). "Author must confirm" item 4 gets "(checked against tog.tex on 2026-11-23)". The review version still says "the authors" (paper does too).
- SUBMIT_STEPS.md: dated 2026-11-23; step 3 says the term list exists, dist/anon/build.py builds and checks the anonymous copy (dist/anon/out, VERIFY.md), the author creates the mirror from that copy or from the repository, only the author can create the link; old steps 5-8 replaced by step 5 (`sh dist/tog/set_anon_url.sh <URL>`) and step 6 (URL check in both anonymous PDFs, rerun pdf_checks); steps renumbered 1-13; "not verified" about copying PDFs removed.
- Repository public (author's decision): SUBMIT_STEPS step 3, step 13 (was 15), item 9; scholarone_fields.md "After acceptance" paragraph. The warning that a reviewer who searches the title can find it is kept (item 9, scholarone_fields).
- pdf_checks.md: provenance sentence now "Run on 2026-11-23 on the PDFs built at 13:42 (CreationDate 13:42:08-13:42:20 PST)", supplement 106 pages. Reran checks 1, 2, 4, 5 on current dist/tog PDFs (pdfinfo, 57/57/46/46 fonts all emb=yes, no Type 3, 0 images, 0 hits for aritro/bhattach/uiuc/illinois/urbana/morley in B and D by text, raw bytes and decompressed streams, same 6 and 3 /URIs): no value changed. Reference "steps 1 to 4" -> "steps 3 to 5".
- files_to_upload.md Sources row: lists tog.tex (lines 42, 45, 47, 109-113, 147), macros.tex:13, supplement.tex:34, 36, 79 (verified by grep; sections/, refs.bib, supp/, tog_review.tex, supplement_review.tex have no hit).
- cover_letter.md: "Date: 23 November 2026 (draft date; Author must confirm ...)".
- SUBMIT_STEPS "Author must confirm" item 13 added (author reading AI-written proofs, paper/PROOF_READING_ORDER.md; wording changes only after the author reports which were read).

## Task 5
- dist/tog/rebuild.sh: faithful copy of the scratchpad script; only change: R computed as `$(cd "$(dirname "$0")/../.." && pwd)`. POSIX sh (`sh -n` passes). Not run.
- dist/tog/set_anon_url.sh [--dry-run] URL: refuses unless URL matches the regex; edits the one `\newcommand{\anoncodeurl}{...}` in tog.tex and supplement.tex (fails unless exactly one each; writes .bak), runs rebuild.sh, checks with pdftotext (whitespace removed) that the URL is in build/tog_review.pdf and build/supplement_review.pdf and that "anonymous.4open.science" is not in build/tog.pdf, prints PASS or FAIL.
Test output (only these two kinds of run):
```
$ sh set_anon_url.sh https://example.com/x
REFUSED: URL must match ^https://anonymous\.4open\.science/r/[A-Za-z0-9._-]+/?$ (got: 'https://example.com/x')   rc=2
$ sh set_anon_url.sh "https://anonymous.4open.science/r/a;b"   -> REFUSED, rc=2
$ sh set_anon_url.sh --dry-run https://anonymous.4open.science/r/test-id_1.x
tog.tex: \newcommand{\anoncodeurl}{\url{https://anonymous.4open.science/r/test-id_1.x}}
supplement.tex: \newcommand{\anoncodeurl}{\url{https://anonymous.4open.science/r/test-id_1.x}}
DRY RUN: edited temporary copies in /var/folders/.../tmp.xxxx (originals untouched, nothing built)   rc=0
```
md5 of tog.tex and supplement.tex unchanged; no .bak files created; \anoncodeurl untouched. The PASS/FAIL path and the idempotent second run (macro body already `\url{...}`; the regex allows one nested brace level) were not exercised.

## Task 6: build
`python3 tools/build_supplement.py` -> ok (regenerated supp/s12.tex, supp/s15.tex). tectonic on supplement_review.tex and supplement.tex: rc 0, both 106 pages (the same as the current PDFs; size of build/supplement.pdf 830457 vs 830013 bytes). Overfull boxes: 1 (2.4 pt, paragraph at line 569), none over 5 pt. Undefined references: 0 (only a font-shape warning). pdftotext of the new build shows the six new S15 headings with "File in the code repository" lines, and no "2026-11-23". Output PDFs stay in dist/tog/build/; dist/tog/*.pdf, paper/*.pdf are untouched, so the hashes in files_to_upload.md still describe the old PDFs and need rebuild.sh before submission.

## git status --short dist/tog dist/anon | head -40
 M dist/tog/submission/SUBMIT_STEPS.md
 M dist/tog/submission/cover_letter.md
 M dist/tog/submission/files_to_upload.md
 M dist/tog/submission/pdf_checks.md
 M dist/tog/submission/scholarone_fields.md
 M dist/tog/supp/s12.tex
 M dist/tog/supp/s15.tex
 M dist/tog/supp_src/s12_kings.md
 M dist/tog/tools/build_supplement.py
?? dist/tog/rebuild.sh
?? dist/tog/set_anon_url.sh
