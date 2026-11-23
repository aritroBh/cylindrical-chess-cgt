# R4: submission facts recounted from the built PDFs (2026-11-23, Haiku agent; saved by the main session)

One mismatch, fixed: `dist/tog/submission/pdf_checks.md` line 22 said the supplement has 82 pages; it has 95.

| Fact | Measured | Stated | Result |
|---|---|---|---|
| `dist/tog/tog.pdf` | 260856 bytes, 10 pages, SHA-256 136f4064...ee99a7 | files_to_upload.md:18 | MATCH |
| `dist/tog/tog_review.pdf` | 260294 bytes, 10 pages, 8e8de9f3...6181f8 | files_to_upload.md:9 | MATCH |
| `dist/tog/supplement.pdf` | 759840 bytes, 95 pages, eab609b6...e5aa3e | files_to_upload.md:19 | MATCH |
| `dist/tog/supplement_review.pdf` | 759580 bytes, 95 pages, 5af51453...c9c47d | files_to_upload.md:10 | MATCH |
| three copies under `paper/` | byte-identical to the files above | n/a | MATCH |
| abstract | 199 words | scholarone_fields.md:9, 11 | MATCH |
| references | 20 (`\bibitem` in `build/tog.bbl`) | scholarone_fields.md:32 | MATCH |
| figures, tables | 7 and 5 (environments and captions) | scholarone_fields.md:30 | MATCH |
| anonymity grep on both anonymous PDFs | 0 and 0 | n/a | PASS |
| PDF metadata, anonymous PDFs | no Author field; Title on the paper only | n/a | PASS |
| fonts, anonymous PDFs | all embedded, no Type 3 | pdf_checks.md | PASS |
| supplement page count in cover_letter.md:11, scholarone_fields.md:33 and 57 | 95 | 95 | MATCH |
| supplement page count in pdf_checks.md:22 | 95 | 82 | MISMATCH, fixed |
