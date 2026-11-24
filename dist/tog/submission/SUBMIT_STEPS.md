# Submission steps

"done" means finished and checked on 2026-11-23. "author" means the author does it by hand.

## Steps

1. done: Named and anonymous PDFs exist; both papers are 10 pages including references, US Letter. Evidence in `pdf_checks.md`.
2. done: Cover letter, ScholarOne fields, upload table and PDF checks written in this folder.
3. author: Create the anonymous code link at https://anonymous.4open.science/. Sign in with GitHub, add the repository `aritroBh/cylindrical-chess-cgt` (the one named in the paper), and give it a project name that does not contain your name. Use the redaction term list so that your name, institution, Prof. Morley's name and the GitHub user name are replaced inside files and file names. The term list exists (`delegate/out/T79/anonymize_terms.txt`; read it first), and `dist/anon/build.py` already builds and checks an anonymous code copy from the repository (`dist/anon/out/`, report `dist/anon/VERIFY.md`, all checks PASS when it was written). Create the anonymous.4open.science mirror either from that checked copy or from the repository with the term list. Only the author can create the link. The repository is public (see item 9 below), so the mirror needs no access grant.
4. author: Open the anonymous link in a private browser window. Search the mirror for aritro, bhattacharjee, uiuc, illinois, urbana, morley and the repository's owner name. Check commit history, `README`, file paths and any logs that may hold `/Users/aritro`. Fix by adding terms and refreshing the mirror.
5. author: Run `sh dist/tog/set_anon_url.sh https://anonymous.4open.science/r/<id>`. The script sets the link in `\anoncodeurl` of `dist/tog/tog.tex` and `dist/tog/supplement.tex` (the named build uses `\codeurl` and is not affected), rebuilds all four PDFs with `dist/tog/rebuild.sh`, checks that both anonymous papers have 10 pages, copies the PDFs to `dist/tog/`, refreshes the hashes in `files_to_upload.md`, and prints PASS or FAIL. It keeps a `.bak` of each edited `.tex` file.
6. author: Check that the new URL appears in both anonymous PDFs (`pdftotext tog_review.pdf - | grep anonymous.4open` and the same for `supplement_review.pdf`); the script does this check and prints it. Rerun the checks in `pdf_checks.md` (pdfinfo, pdffonts, pdfimages, text search, `/URI` list) on the new PDFs.
7. author: Optional but advised by the audit: run `tog_review.pdf` through IEEE PDF eXpress to see whether the AppleSymbols subset fonts are accepted. Not verified.
8. author: Fill in `cover_letter.md`: the anonymous link, the date, and the "Author must confirm" sentence. Decide whether the letter is shown to reviewers; if so, remove name and affiliation from the uploaded copy.
9. author: Log in to ScholarOne for IEEE Transactions on Games (address as shown on the ToG submission page; not verified here). Start a new submission. Choose the full paper type. Paste title, abstract (200 words), index terms, and the AI-use and code statements from `scholarone_fields.md`. Enter author details, ORCID, and answer any funding, prior-publication and conflict questions.
10. author: Upload `tog_review.pdf` as the main document for review and `supplement_review.pdf` as supplementary material. Do not upload `tog.pdf` or `supplement.pdf`.
11. author: In ScholarOne, build the PDF proof and open it. Check that it has 10 pages, the figures show, and the metadata shows no name.
12. author: Submit. Keep the confirmation e-mail and the manuscript ID. Do not post a preprint (arXiv or other) before asking the Editor, since a named preprint can break the double-anonymous review (AUDIT.md section 6).
13. author: After acceptance, switch to the named build, point to github.com/aritroBh/cylindrical-chess-cgt (the repository is already public and is to stay public), and fix the items in AUDIT.md that are still open (review the list; some were fixed by the cut to 10 pages).

## Author must confirm

1. The manuscript is original and not under review elsewhere (cover letter).
2. The 2025 study is unpublished and not public anywhere (paper Section I and the cover letter). No preprint, conference or thesis version exists.
3. There is no funding to declare. The paper's Acknowledgment names none.
4. The AI-use statement meets IEEE's policy (systems, sections, level), and the open models run through OpenCode and Kilo need no names. The wording in the paper is quoted unchanged (checked against `dist/tog/tog.tex` on 2026-11-23).
5. ORCID, e-mail and affiliation for ScholarOne. The paper gives the University of Illinois Urbana-Champaign, Urbana, IL 61801 USA.
6. Name of the manuscript type in ScholarOne (full paper).
7. Whether ScholarOne asks for source files, and any file-size limits (not verified).
8. Whether the cover letter is visible to reviewers; if so, upload it without name and affiliation.
9. The GitHub repository `aritroBh/cylindrical-chess-cgt` is public, and the author has decided to leave it public. It carries the paper's title and the author's name, so a reviewer who searches the title can find it. Its state must match the submitted version at the time of the final version.
10. The date in the cover letter.
11. Figure labels are readable at print size (the audit found 5 to 6.3 pt labels in an earlier build; not re-measured).
12. The index terms are acceptable to ToG (IEEE Thesaurus not checked).
13. The author is reading the AI-written proofs (reading order in `paper/PROOF_READING_ORDER.md`). The paper and Section S17 currently say that no human referee has read them. That wording changes only after the author reports which items were read.
