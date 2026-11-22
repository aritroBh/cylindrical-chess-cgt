# DOI check for paper/ieee/refs.bib (Crossref only)

Output: `delegate/out/ieee_audit/refs_with_doi.bib` (copy of `paper/ieee/refs.bib`; only `doi` fields added and the trailing commas they need).
Rule: a DOI is added only when the Crossref title, first-author surname and year all match the bib entry.
Fetches: 25 Crossref requests in total (no mailto, no personal data). Six candidate fetches were first sent with a stray newline in the DOI (`%0A`); they were repeated with clean URLs and only the clean results are used here.

| key | DOI added | Crossref title / first author / year seen | URL fetched |
|---|---|---|---|
| Elkies1996 | none | "On Numbers and Endgames: Combinatorial Game Theory in Chess Endgames"; Elkies; 1997 (issued 1997-02-06). **Year differs from bib (1996).** | https://api.crossref.org/works/10.1017/9781009701839.014 |
| Elkies2002 | 10.1017/9781316135167.007 | "Higher Nimbers in Pawn Endgames on Large Chessboards"; Elkies; 2002 | https://api.crossref.org/works/10.1017/9781316135167.007 |
| WinningWays | none | "Winning Ways for Your Mathematical Plays"; Berlekamp; 2018 (Taylor & Francis record 10.1201/9780429487330). **Year and publisher differ from bib (2001-2004, A K Peters, 2nd ed.).** | https://api.crossref.org/works?query.bibliographic=Winning+Ways+for+Your+Mathematical+Plays&rows=3 |
| ONAG | none | No matching title (results: "On Games and Numbers", "Numbers Games", not this book) | https://api.crossref.org/works?query.bibliographic=On+Numbers+and+Games&rows=3 |
| Siegel2013 | 10.1090/gsm/146 | "Combinatorial Game Theory"; Siegel; 2013 | https://api.crossref.org/works/10.1090/gsm/146 |
| DrummondCole2005 | none | No matching title in the query results | https://api.crossref.org/works?query.bibliographic=Positions+of+value+2+in+generalized+Domineering+and+chess&rows=3 |
| GuySmith1956 | 10.1017/S0305004100031509 | "The G-values of various games" (G in italics in Crossref); Guy; 1956 | https://api.crossref.org/works/10.1017/S0305004100031509 |
| PlambeckSiegel2008 | 10.1016/j.jcta.2007.07.008 | "Misère quotients for impartial games"; Plambeck; 2008 | https://api.crossref.org/works/10.1016/j.jcta.2007.07.008 |
| Dawson1935 | none | No matching title (Dover 1973 reprint of a 1935 item, not in Crossref) | https://api.crossref.org/works?query.bibliographic=Caissa%27s+Wild+Roses&rows=3 |
| Pritchard | none | No matching title | https://api.crossref.org/works?query.bibliographic=The+Classified+Encyclopedia+of+Chess+Variants&rows=3 |
| Maeser2002 | 10.1017/9781316135167.012 | "Global Threats in Combinatorial Games: A Computation Model with Applications to Chess Endgames"; Mäser; 2002 | https://api.crossref.org/works/10.1017/9781316135167.012 |
| WuYuLandry2010 | none | No matching title (course paper, no DOI) | https://api.crossref.org/works?query.bibliographic=A+combinatorial+game+theoretic+analysis+of+chess+endgames&rows=3 |
| Stockfish | none | No matching title (software release) | https://api.crossref.org/works?query.bibliographic=Stockfish+19&rows=3 |
| Lc0 | none | No matching title (software release) | https://api.crossref.org/works?query.bibliographic=Leela+Chess+Zero&rows=3 |
| LichessTB | none | No matching title (web API) | https://api.crossref.org/works?query.bibliographic=Lichess+tablebase+API+Syzygy&rows=3 |
| PyTorch | none | No matching title | https://api.crossref.org/works?query.bibliographic=PyTorch%3A+An+imperative+style%2C+high-performance+deep+learning+library&rows=3 |
| Study2025 | none | No query sent: the entry is the authors' unpublished manuscript, and its title is withheld for review; sending it to Crossref would disclose it | none |
| WikiCylinder | none | No matching title (Wikipedia page) | https://api.crossref.org/works?query.bibliographic=Cylinder+chess&rows=3 |
| HGMCylinder | none | No matching title (web page) | https://api.crossref.org/works?query.bibliographic=Cylinder+Chess+XBoard+variant+rules&rows=3 |

## Mismatches between Crossref and the bib
- **Elkies1996**: Crossref year 1997 (published 1997-02-06) against bib year 1996. The DOI was not added. Decide whether the bib year is right, or whether the DOI should be added with the year checked by hand.
- **WinningWays**: Crossref's only exact-title record is a 2018 Taylor & Francis entry, against the bib's 2001-2004 A K Peters edition. The DOI was not added.
- All other added DOIs match title, first author and year. The Mäser/"M{\"a}ser" and Guy/Plambeck entries agree once LaTeX accents are decoded.

Not changed: `paper/ieee/refs.bib` (read only) and every field other than the five added `doi` fields.
