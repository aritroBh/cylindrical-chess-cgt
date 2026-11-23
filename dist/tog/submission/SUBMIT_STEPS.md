# Submission steps

"done" means finished and checked on 2026-11-22. "author" means the author does it by hand.

## Steps

1. done: Named and anonymous PDFs exist; both papers are 10 pages including references, US Letter. Evidence in `pdf_checks.md`.
2. done: Cover letter, ScholarOne fields, upload table and PDF checks written in this folder.
3. author: Create the anonymous code link at https://anonymous.4open.science/. Sign in with GitHub, add the repository `aritroBh/cylindrical-chess-cgt` (the one named in the paper), and give it a project name that does not contain your name. Use the redaction term list so that your name, institution, Prof. Morley's name and the GitHub user name are replaced inside files and file names. Another job is preparing that list in `delegate/out/T79/anonymize_terms.txt`; it was not ready when this package was written, so check that the file exists and read it first. Check that the repository is public at the time (anonymous.4open.science mirrors a GitHub repository, so a private one may need access granted; not verified).
4. author: Open the anonymous link in a private browser window. Search the mirror for aritro, bhattacharjee, uiuc, illinois, urbana, morley and the repository's owner name. Check commit history, `README`, file paths and any logs that may hold `/Users/aritro`. Fix by adding terms and refreshing the mirror.
5. author: Put the URL in both anonymous builds. Edit `\newcommand{\anoncodeurl}{anonymized repository link}` at `dist/tog/tog.tex` line 26 and `dist/tog/supplement.tex` line 27, replacing the text with `\url{https://anonymous.4open.science/r/<id>}`. Keep the edit inside the macro so the named build is not affected (the named build uses `\codeurl`).
6. author: Rebuild with `dist/tog/sbuild.sh` (builds the anonymous paper, the supplement sources, both supplements and the named paper), and copy the PDFs to `dist/tog/` if they are not written there (how they got there: not verified). Confirm the anonymous paper is still 10 pages.
7. author: Rerun the checks in `pdf_checks.md` (pdfinfo, pdffonts, pdfimages, text search, `/URI` list) and check that the new URI appears in both anonymous PDFs.
8. author: Recompute SHA-256 and sizes (`shasum -a 256`, `ls -l`) and update `files_to_upload.md`.
9. author: Optional but advised by the audit: run `tog_review.pdf` through IEEE PDF eXpress to see whether the AppleSymbols subset fonts are accepted. Not verified.
10. author: Fill in `cover_letter.md`: the anonymous link, the date, and the "Author must confirm" sentence. Decide whether the letter is shown to reviewers; if so, remove name and affiliation from the uploaded copy.
11. author: Log in to ScholarOne for IEEE Transactions on Games (address as shown on the ToG submission page; not verified here). Start a new submission. Choose the full paper type. Paste title, abstract (199 words), index terms, and the AI-use and code statements from `scholarone_fields.md`. Enter author details, ORCID, and answer any funding, prior-publication and conflict questions.
12. author: Upload `tog_review.pdf` as the main document for review and `supplement_review.pdf` as supplementary material. Do not upload `tog.pdf` or `supplement.pdf`.
13. author: In ScholarOne, build the PDF proof and open it. Check that it has 10 pages, the figures show, and the metadata shows no name.
14. author: Submit. Keep the confirmation e-mail and the manuscript ID. Do not post a preprint (arXiv or other) before asking the Editor, since a named preprint can break the double-anonymous review (AUDIT.md section 6).
15. author: After acceptance, switch to the named build, point to github.com/aritroBh/cylindrical-chess-cgt, make that repository public, and fix the items in AUDIT.md that are still open (review the list; some were fixed by the cut to 10 pages).

## Author must confirm

1. The manuscript is original and not under review elsewhere (cover letter).
2. The 2025 study is unpublished and not public anywhere (paper Section I and the cover letter). No preprint, conference or thesis version exists.
3. There is no funding to declare. The paper's Acknowledgment names none.
4. The AI-use statement meets IEEE's policy (systems, sections, level), and the open models run through OpenCode and Kilo need no names. The wording in the paper is quoted unchanged.
5. ORCID, e-mail and affiliation for ScholarOne. The paper gives the University of Illinois Urbana-Champaign, Urbana, IL 61801 USA.
6. Name of the manuscript type in ScholarOne (full paper).
7. Whether ScholarOne asks for source files, and any file-size limits (not verified).
8. Whether the cover letter is visible to reviewers; if so, upload it without name and affiliation.
9. The GitHub repository `aritroBh/cylindrical-chess-cgt` is public now (made public after the audit) and carries the paper's title and the author's name, so a reviewer who searches the title can find it. Decide whether to rename it or make it private during review; its state must match the submitted version at the time of the final version.
10. The date in the cover letter.
11. Figure labels are readable at print size (the audit found 5 to 6.3 pt labels in an earlier build; not re-measured).
12. The index terms are acceptable to ToG (IEEE Thesaurus not checked).
