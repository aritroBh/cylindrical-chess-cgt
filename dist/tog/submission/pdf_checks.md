# PDF checks

Run on 2026-11-23 on the PDFs built that day (`pdfinfo` CreationDate of `tog.pdf`: Mon Nov 23 16:44:07 2026 PST). Tools present: `pdfinfo`, `pdffonts`, `pdfimages`, `pdftotext` (poppler, `/opt/homebrew/bin`). The URI scan used `python3` (re, zlib) on the raw file and on all decompressed streams. Checks 1, 2, 4 and 5 were rerun on these PDFs on 2026-11-23 and every value in the tables below matched (supplement 67 pages; file sizes as in the table).

Files: A = `tog.pdf` (named), B = `tog_review.pdf` (anonymous), C = `supplement.pdf` (named), D = `supplement_review.pdf` (anonymous). All in `dist/tog/`.

## Summary

| # | Check | Result |
|---|---|---|
| 1 | pdfinfo: pages, US Letter, version, metadata | PASS |
| 2 | pdffonts: all embedded, no Type 3 | PASS (one caution) |
| 3 | pdfimages: resolution of raster images | PASS (no raster images) |
| 4 | Anonymity text search in B and D | PASS (0 hits for all 7 terms) |
| 5 | /URI targets in B and D | PASS |
| 6 | Anonymous code link present in B and D | FAIL (placeholder text, link not created yet) |

## 1. pdfinfo

| | A tog.pdf | B tog_review.pdf | C supplement.pdf | D supplement_review.pdf |
|---|---|---|---|---|
| Pages | 10 | 10 | 68 | 68 |
| Page size | 612 x 792 pts (letter) | same | same | same |
| PDF version | 1.5 | 1.5 | 1.5 | 1.5 |
| Title | Chess Endgames on a Cylindrical Chessboard: Exact Combinatorial Game Values, Real-Chess Checks, and Tablebases | same | (empty) | (empty) |
| Author | Aritro Bhattacharjee and Thomas Morley | (empty) | (empty) | (empty) |
| Subject | (empty) | (empty) | (empty) | (empty) |
| Keywords | (empty) | (empty) | (empty) | (empty) |
| Creator / Producer | LaTeX with hyperref / xdvipdfmx (0.1) | same | same | same |
| Metadata stream (XMP) | no | no | no | no |
| File size (bytes) | 261005 | 260484 | 614555 | 614283 |

Evidence: `Page size: 612 x 792 pts (letter)` on all four; B `pdfinfo` has no `Author:` line; D has no `Author:` line. Result: PASS. The paper is 10 pages including references, at the ToG limit. Subject and Keywords are empty in all four; ToG does not ask for them in the PDF (not verified), so this is not a failure. The supplements carry no Title field; optional.

## 2. pdffonts

| | A | B | C | D |
|---|---|---|---|---|
| Fonts listed | 57 | 57 | 46 | 46 |
| Not embedded (emb = no) | 0 | 0 | 0 | 0 |
| Type 3 | 0 | 0 | 0 | 0 |
| Types | 25 Type 1C, 19 CID Type 0C, 13 CID TrueType | same | 26 CID Type 0C, 20 CID TrueType | same |

Evidence: `pdffonts` column `emb` is `yes` on every line, and no line says `Type 3`, so there is no page to flag. Result: PASS.

Caution: the 13 (A, B) and 20 (C, D) CID TrueType fonts are subsets of `AppleSymbols`, a macOS system font, used for the chess glyphs. They have `uni = no` (no ToUnicode map), so the chess pieces will not copy out as text. IEEE PDF eXpress normally accepts embedded subsets, but the audit marked this UNKNOWN until the file has been run through PDF eXpress (AUDIT.md, section 4.1). I did not run it. Embedding permission, checked 2026-11-23: the OS/2 table of `/System/Library/Fonts/Apple Symbols.ttf` has `fsType = 0` (installable embedding, no restriction bits), so the font itself permits embedded subsets. The figures can only be regenerated on a Mac (`paper/figures/make_figures.py` asks for this font); the submission needs only the PDFs.

## 3. pdfimages -list

Evidence: `pdfimages -list` printed only the header line for all four files, so there are no raster images. All figures are vector. No image is under 300 dpi. Result: PASS.

Not checked by me: the audit (section 4.2) found board-figure labels at about 5 to 6.3 pt at print size in an earlier 14-page build. The paper has been cut to 10 pages since, and I did not re-measure label sizes. Author must confirm by looking at the figures at print size.

## 4. Anonymity text search (B and D)

Case-insensitive search of `pdftotext` output, plus a raw-bytes search and a search of all decompressed streams (for aritro, bhattach, illinois, morley, uiuc, urbana).

| Term | B tog_review.pdf | D supplement_review.pdf |
|---|---|---|
| aritro | 0 | 0 |
| bhattacharjee | 0 | 0 |
| uiuc | 0 | 0 |
| illinois | 0 | 0 |
| urbana | 0 | 0 |
| morley | 0 | 0 |
| github.com/aritroBh | 0 | 0 |

Evidence: every `grep -ci` count was 0; the stream scan printed no hit. Result: PASS. The self-citation prints as "Anonymous, Title withheld for review, 2025, unpublished manuscript" (B reference [9], D reference [5]), and page 1 shows "Anonymized for review".

Residual risk to judge by hand (not a tool finding): the text says the paper "extends an unpublished 2025 study". If that study is public anywhere, a reviewer can find the author. Author must confirm.

## 5. Hyperlink targets (B and D)

B has 6 `/URI` entries and D has 3:

- http://hgm.nubati.net/rules/Cylinder.html (B, D)
- https://en.wikipedia.org/wiki/Cylinder_chess (B, D)
- https://github.com/LeelaChessZero/lc0 (B)
- https://github.com/official-stockfish/Stockfish (B)
- https://tablebase.lichess.ovh (B)
- https://web.stanford.edu/~wqy/research/Math%20191-%20Chess.pdf (B, D)

Result: PASS. None carries the author's name, institution or repository. The Stanford URL is the personal-page path of a cited third party (Wu, Yu and Landry), not the author. The same links are in the named PDFs.

## 6. Anonymous code link (extra check)

Evidence: B line "at anonymized repository link. The supplementary material gives the full proofs" (Section XIII), D page 1 "The code and data are available at anonymized repository link." Neither has a `/URI` to anonymous.4open.science. Result: FAIL until the author creates the link and rebuilds (steps 3 to 5 in `SUBMIT_STEPS.md`). After the rebuild, rerun checks 1, 2, 4 and 5 and recompute the hashes.
