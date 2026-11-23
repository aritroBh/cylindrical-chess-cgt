# Files to upload

Hashes and sizes are from the build of 2026-11-23. Both anonymous builds still print the placeholder "anonymized repository link" instead of an anonymous.4open.science URL, so they are NOT final. After the link is put in and both anonymous PDFs are rebuilt, recompute the hashes with `shasum -a 256` and update this table. See `SUBMIT_STEPS.md`.

Root: `dist/tog/`

| ScholarOne slot | File (full path) | Bytes | Pages | SHA-256 | Status |
|---|---|---|---|---|---|
| Main document for review | `dist/tog/tog_review.pdf` | 260516 | 10 | `4f3aec370d5cd42cda70c5fa68c550ec6efe97a538b5d1c6bb7f0793505eded4` | Placeholder link; rebuild first |
| Supplementary material | `dist/tog/supplement_review.pdf` | 795758 | 101 | `6562b48d8639801c302eee2d53bca624a7756f75a3ddb8e98e2544e2eb1af29c` | Placeholder link; rebuild first |
| Sources (only if asked) | LaTeX sources of the anonymous build: `tog_review.tex`, `tog.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/` | not computed | n/a | not computed | Author must confirm that ScholarOne asks for sources at review stage (not verified). If sent, they must be anonymous: `tog.tex` contains the author name and the GitHub URL inside the `\else` branches, so do not send sources for review without stripping them. |
| Cover letter | `dist/tog/submission/cover_letter.md` (paste text, or export to PDF) | n/a | 1 | n/a | Needs the anonymous link and author checks |

Do not upload (named versions, kept for after acceptance):

| File | Bytes | Pages | SHA-256 |
|---|---|---|---|
| `dist/tog/tog.pdf` | 261096 | 10 | `d97ad95b87440d2600d0500440fa6e5af24063a08eb0cef497014a4df3cafd5c` |
| `dist/tog/supplement.pdf` | 796041 | 101 | `f347ceea3e32bdd296a7ebffc8a7cb2f015d778c1b3c781d07c8ba36464a26bc` |

Maximum upload size per file in ScholarOne for ToG: not verified.
