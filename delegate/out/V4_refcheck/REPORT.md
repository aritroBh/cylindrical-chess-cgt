# V4: reference list checked with two outside tools (2026-11-25)

Input: `dist/tog/refs.bib` (21 entries; identical to `paper/ieee/refs.bib`) and the reference list of the anonymous 10-page PDF (20 printed references; PyTorch is in the file but cited nowhere in the 10-page paper).

Tools, each run in a sandbox that could read only the input files:
- `academic-refchecker` 3.1.12 (markrussinovich/refchecker), no LLM, on the `.bib` file. Raw output: `refchecker_stdout.txt`, `refchecker_report.json`.
- `hallucinator` 0.2.2 (gianlucasb/hallucinator), Python bindings, on the PDF. Raw output: `hallucinator_stdout.txt`.
- `opendraft` was not run: it writes drafts from a topic and has no mode that checks an existing paper.

## Result: no invented reference, nothing to change

Every flag was checked by hand.

| Entry | Flag | Finding |
|---|---|---|
| Elkies 1996 | year 1996 against 1999 | 1996 is the book (Games of No Chance); 1999 is the arXiv copy. Correct as cited |
| Winning Ways, ONAG | year 2001 against 1983, 1978 | The second editions (2001) are cited. Correct |
| Siegel 2013 | venue missing; DOI 10.1090/gsm/146 "not valid" | The series is given; the DOI resolves at the publisher (the publisher's site refuses scripts) |
| Drummond-Cole 2005 | not found | Integers is not in the databases. The article is listed in volume 5 on the journal's own site |
| Guy and Smith 1956 | DOI "not valid" (one tool) | doi.org resolves it; the other tool verified the entry |
| Dawson 1935, Pritchard | not found | Books outside the databases |
| Wu, Yu, Landry 2010 | "non-existent web page" | The tool sent the LaTeX-escaped URL. The plain URL answers 403 to scripts, as does the whole site; the Internet Archive holds a copy from 2026-04-16. To do by a person: open the link once in a browser |
| Thompson 1986 | venue ICCA J. against ICGA Journal | The journal was the ICCA Journal in 1986. Correct |
| Tomašev 2022 | first author "Tomaev" | The tool dropped the accented letter; the file has `Toma{\v{s}}ev` |
| Study 2025 | not found | The authors' own unpublished study |
| Stockfish, Lc0, Lichess tablebase, Wikipedia, H. G. Muller | skipped or not found | Web pages; all five links answer 200 |
