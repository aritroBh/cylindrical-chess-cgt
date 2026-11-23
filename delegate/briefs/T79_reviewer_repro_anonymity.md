# T79 — Reviewer's-eye audit: can a stranger reproduce the repository, and is an anonymised copy really anonymous?

Output directory: `delegate/out/T79/` (create it). Write `REPORT.md` there and any scripts you use. Do not edit
anything else in the repository. Git: read-only commands only (`git ls-files`, `git archive`, `git show`,
`git log`); never commit, add, checkout, reset, stash or push. NEVER use pkill, killall, `kill -- -1` or
`kill $(pgrep ...)`; signal only PIDs you started and recorded yourself. Keep every process under 2 GB and
under 20 minutes; at most 2 processes at once; if `nice` is denied by your sandbox, run without it. Other
people's jobs run on this machine: do not touch any process you did not start.

## Background

The repository backs a paper on chess pawn endgames on a cylindrical board, analysed with combinatorial game
theory. The paper goes to a double-anonymous journal (IEEE Transactions on Games). Reviewers will get an
anonymised copy of the tracked files through anonymous.4open.science, which replaces a list of terms the
author supplies. Two things must hold: the README's commands work from a clean copy, and no identifying
string survives.

## Task 1 — clean-copy reproduction

1. Make a clean export of HEAD's tracked files: `mkdir -p delegate/out/T79/export && git archive HEAD | tar -x -C delegate/out/T79/export`
   (tracked files only; about the size `git ls-files` implies; if the export would exceed 600 MB, export only
   the paths the README's commands need and say so).
2. In the export, follow `README.md` section "Reproduce" (and any "Install"/"Setup" section before it) exactly
   as a stranger would. The README uses `.venv/bin/python`; a clean copy has no `.venv`, so note what the
   README says about creating it. If it gives no instruction, that is finding number one; then create a
   virtual environment inside the export from the repository's own requirements file if one exists (do not
   install anything from the network if the sandbox blocks it; say so) or fall back to the repository's
   existing `/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python` run with the export as the
   working directory.
3. Run each README command once (skip any that the README itself says takes more than 20 minutes; say which).
   Record: command, exit status, wall time, last 10 lines of output, and whether the result matches what the
   README or paper says it should print.
4. List every path the README mentions and whether it exists in the export (tracked) or only in the working
   tree (untracked or ignored).
5. C sources: for each C solver the README tells the reader to build, try the stated build command.

## Task 2 — anonymity of the tracked files

1. Search every tracked file in the export (text files; for PDFs use `pdftotext` and `pdfinfo` if available,
   otherwise `strings`) for identifying strings, case-insensitive. Start from these seeds and add any you
   discover (user names in absolute paths, e-mail addresses, GitHub handles, institution names, mentor names,
   city names tied to the author): `aritro`, `bhattacharjee`, `aritroBh`, `uiuc`, `illinois`, `urbana`,
   `champaign`, `morley`, `/Users/`, `@gmail`, `@illinois`, `cylindrical-chess-cgt`.
2. Report, per term: number of files, number of lines, and the ten files with most hits. Do not print e-mail
   addresses in full in the report; write the local part's first letter and the domain.
3. Produce `delegate/out/T79/anonymize_terms.txt`: the minimal list of literal terms (one per line) whose
   replacement would remove every identifying hit, most specific first. Say which hits no term list can fix
   (for example a PDF with the author's name rendered in it, or PDF metadata) and list those files so they can
   be excluded from the anonymised copy instead.
4. Check the two anonymous PDFs `dist/tog/tog_review.pdf` and `dist/tog/supplement_review.pdf` separately:
   text, metadata (Author, Title, Creator, Producer, custom fields), embedded file names, and hyperlink
   targets. Any hit there is a blocker.

## Report format

`REPORT.md`: a five-line summary first (does the README reproduce from a clean copy: yes / yes with fixes /
no; is the anonymised copy safe with the term list: yes / no, and how many files must be excluded). Then one
table per task, then a numbered list of concrete fixes, each naming the file and the exact change. Label
every statement you verified by running something as RUN, and every statement from reading only as READ.
