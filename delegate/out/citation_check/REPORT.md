# Citation check of paper/ieee/refs.bib (2026-10-27)

Method (after github.com/PHY041/claude-skill-citation-checker, applied by hand, not by running its script): each entry looked up in
two or more independent sources (Crossref, OpenAlex, Semantic Scholar, arXiv, the publisher's or series' page, GitHub releases,
the live URL); every field compared; each \cite site read against the source. Five Claude Sonnet agents, one per batch.

| key | verdict | note |
|---|---|---|
| Elkies1996 | VERIFIED | all fields confirmed |
| Elkies2002 | VERIFIED | all fields confirmed |
| Maeser2002 | VERIFIED | correct, but not cited anywhere, so not printed |
| DrummondCole2005 | VERIFIED | all fields confirmed |
| Study2025 | SKIPPED | the author's own unpublished manuscript; cited consistently |
| WinningWays | VERIFIED | all fields confirmed |
| ONAG | VERIFIED | all fields confirmed |
| Siegel2013 | VERIFIED | all fields confirmed |
| GuySmith1956 | VERIFIED | all fields confirmed |
| PlambeckSiegel2008 | VERIFIED | all fields confirmed |
| Dawson1935 | VERIFIED | all fields confirmed |
| Pritchard | VERIFIED | all fields confirmed |
| WuYuLandry2010 | FIX (fixed) | institution 'Stanford Univ.' unsupported (Math 191 course paper); now @misc with the author's own URL |
| Stockfish | VERIFIED | all fields confirmed |
| Lc0 | VERIFIED | all fields confirmed |
| LichessTB | VERIFIED | all fields confirmed |
| PyTorch | FIX (fixed) | pages 8024--8035 -> 8026--8037 (NeurIPS proceedings metadata) |
| WikiCylinder | VERIFIED | all fields confirmed |
| HGMCylinder | FIX (fixed) | page has no date: year field dropped |

## Evidence

- **Elkies1996**: https://arxiv.org/abs/math/9905198 https://api.crossref.org/works/10.1017/9781009701839.014 https://api.crossref.org/works?query.bibliographic=On+numbers+and+endgames+Combinatorial+game+theory+in+chess+endgames+Elkies&rows=3 https://library.slmath.org/books/Book29/contents.html https://library.slmath.org/books/Book29/files/elkies.pdf
- **Elkies2002**: https://arxiv.org/abs/math/0011253 https://api.crossref.org/works/10.1017/9781316135167.007 https://api.openalex.org/works?search=Higher+nimbers+in+pawn+endgames+on+large+chessboards https://library.slmath.org/books/Book42/contents.html
- **Maeser2002**: https://library.slmath.org/books/Book42/contents.html https://library.slmath.org/books/Book42/files/maeser.pdf https://api.crossref.org/works/10.1017/9781316135167.012 https://www.cambridge.org/core/product/identifier/9781316135167%23c11/type/book_part https://www.cambridge.org/core/books/abs/more-games-of-no-chance/global-threats-in-combinatorial-games-a-computation-model-with-applications-to-chess-endgames/E82EA22695E73EBBA7ABF563D6BB5094
- **DrummondCole2005**: https://zenodo.org/records/7727217/files/fg6.pdf https://zenodo.org/records/7727217 https://api.zbmath.org/v1/document/_search?search_string=ti:Positions%20of%20value%20*2%20generalized%20Domineering (zbMATH id 2214427) https://api.openalex.org/works?search=Positions+of+value+2+in+generalized+Domineering+and+chess https://arxiv.org/pdf/1506.03949 (reference [10])
- **Study2025**: 
- **WinningWays**: https://api.crossref.org/works?query.bibliographic=Winning+Ways+for+Your+Mathematical+Plays+Berlekamp+Conway+Guy&rows=5 https://api.openalex.org/works?search=Winning+Ways+for+Your+Mathematical+Plays&per-page=5 https://openlibrary.org/search.json?q=winning+ways+for+your+mathematical+plays&fields=title,author_name,first_publish_year,publish_year,publisher,edition_count,isbn&limit=5 https://celebratio.org/Berlekamp_ER/bibf/266/909/ https://math.berkeley.edu/~berlek/pubs/books.html
- **ONAG**: https://api.crossref.org/works?query.bibliographic=On+Numbers+and+Games+Conway&rows=5 https://openlibrary.org/search.json?q=on+numbers+and+games+conway&fields=title,author_name,first_publish_year,publish_year,publisher,publish_place,edition_count,isbn&limit=5 https://en.wikipedia.org/wiki/On_Numbers_and_Games https://www.routledge.com/On-Numbers-and-Games/Conway/p/book/9781568811277
- **Siegel2013**: https://api.crossref.org/works?query.bibliographic=Combinatorial+Game+Theory+Siegel+Graduate+Studies+in+Mathematics&rows=5 https://api.crossref.org/works/10.1090/gsm/146 https://api.crossref.org/works?query.bibliographic=Siegel+Combinatorial+Game+Theory+loopy+games&filter=prefix:10.1090,type:book-chapter&rows=15&select=title,page,DOI https://openlibrary.org/search.json?q=combinatorial+game+theory+siegel&fields=title,author_name,first_publish_year,publish_year,publisher,publish_place,edition_count,isbn&limit=5
- **GuySmith1956**: https://api.crossref.org/works/10.1017/S0305004100031509 https://api.openalex.org/works?search=The+G-values+of+various+games&per-page=5 https://www.cambridge.org/core/product/identifier/S0305004100031509/type/journal_article https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/abs/gvalues-of-various-games/B5C925C1BCF73C0DB7F35EEA160EBB4B https://oeis.org/A002187
- **PlambeckSiegel2008**: https://api.crossref.org/works?query.bibliographic=Misere+quotients+for+impartial+games+Plambeck+Siegel&rows=3 https://api.openalex.org/works?search=Mis%C3%A8re+quotients+for+impartial+games&per-page=3 https://arxiv.org/abs/math/0609825 https://arxiv.org/pdf/math/0609825
- **Dawson1935**: https://openlibrary.org/isbn/9780486229102.json https://en.wikipedia.org/wiki/Thomas_Rayner_Dawson https://arxiv.org/pdf/math/0609825 https://en.wikipedia.org/wiki/Dawson%27s_Chess https://api.crossref.org/works?query.bibliographic=Caissa%27s+Wild+Roses+Dawson+Five+Classics+of+Fairy+Chess&rows=3
- **Pritchard**: https://openlibrary.org/search.json?q=classified+encyclopedia+of+chess+variants&fields=title,author_name,publisher,first_publish_year,publish_year,isbn,edition_count https://openlibrary.org/isbn/9780955516801.json https://www.chesshistory.com/winter/extra/variants.html https://en.wikipedia.org/wiki/David_Pritchard_(chess_player) https://en.wikipedia.org/wiki/The_Chess_Variant_Pages
- **WuYuLandry2010**: https://academic.timwylie.com/19CSCI4341F/chess_endgames_wqy.pdf https://academic.timwylie.com/19CSCI4341F/ https://academic.timwylie.com/ http://web.stanford.edu/~wqy/research/Math%20191-%20Chess.pdf http://web.stanford.edu/~wqy/Research.html
- **Stockfish**: https://api.github.com/repos/official-stockfish/Stockfish/releases?per_page=5 https://github.com/official-stockfish/Stockfish/releases/tag/sf_19 https://stockfishchess.org/blog/ https://stockfishchess.org/download/ https://api.github.com/repos/official-stockfish/Stockfish/git/ref/tags/sf_19
- **Lc0**: https://api.github.com/repos/LeelaChessZero/lc0/releases?per_page=8 https://github.com/LeelaChessZero/lc0/releases/tag/v0.32.1 https://api.github.com/repos/LeelaChessZero/lc0/releases/tags/v0.32.1 https://api.github.com/repos/LeelaChessZero/lc0/git/ref/tags/v0.32.1 https://raw.githubusercontent.com/LeelaChessZero/lc0/v0.32.1/src/main.cc
- **LichessTB**: https://tablebase.lichess.ovh/ https://tablebase.lichess.ovh/tables/standard/ https://tablebase.lichess.ovh/standard?fen=8/8/8/8/8/4k3/4p3/4K3_w_-_-_0_1 https://tablebase.lichess.ovh/standard?fen=8/8/8/8/3k4/p7/PPPPP3/K7_w_-_-_0_1 https://github.com/lichess-org/lila-tablebase
- **PyTorch**: https://papers.nips.cc/paper_files/paper/2019/hash/bdbca288fee7f92f2bfa9f7012727740-Abstract.html https://papers.nips.cc/paper_files/paper/2019/file/bdbca288fee7f92f2bfa9f7012727740-Bibtex.bib https://proceedings.neurips.cc/paper_files/paper/2019/file/bdbca288fee7f92f2bfa9f7012727740-Metadata.json https://proceedings.neurips.cc/paper_files/paper/2019/file/bdbca288fee7f92f2bfa9f7012727740-Paper.pdf https://arxiv.org/abs/1912.01703
- **WikiCylinder**: https://en.wikipedia.org/wiki/Cylinder_chess https://en.wikipedia.org/api/rest_v1/page/summary/Cylinder_chess https://en.wikipedia.org/w/index.php?title=Cylinder_chess&action=history&limit=5
- **HGMCylinder**: http://hgm.nubati.net/rules/Cylinder.html http://hgm.nubati.net/rules/ http://hgm.nubati.net/ https://en.wikipedia.org/wiki/Cylinder_chess
