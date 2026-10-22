# T28 — arXiv / Overleaf package of "Chess Endgames on a Cylindrical Chessboard"

Output directory: `dist/arxiv/`. Nothing outside this directory was written; `paper/` was
not modified.

## 0. Summary (5 lines)

1. `dist/arxiv/src/` is the complete, self-contained arXiv source tree: `main.tex`,
   `macros.tex`, `refs.bib`, `main.bbl`, 17 `sections/*.tex` and the 27 figure PDFs that
   `main.tex` actually includes (364 KiB total; every symlink resolved to a real file).
2. A fresh build (`tectonic -X compile main.tex` in an empty directory) succeeds with
   **0 errors, 0 undefined references/citations, 0 overfull boxes, 0 multiply-defined
   labels**; the resulting PDF is **textually byte-identical to `paper/ieee/main.pdf`**.
3. **The build is 14 pages, not 13.** The brief's "13 pages" is stale: the last
   orchestrator round (`paper/ieee/REVIEW_LOG.md`, 2026-10-22 01:00) grew the paper from
   13 to 14 pages. Dropping the table of contents does *not* restore 13 (tested).
4. **arXiv's default engine (pdfLaTeX) will compile it.** The source is pure ASCII, uses
   no `fontspec`/`unicode-math`, no `\write18`, and every figure is a PDF, so pdfLaTeX
   needs no conversion. It could not be *executed* here (no TeX distribution but tectonic
   is installed); the XeTeX build was executed and is clean apart from 4 harmless
   class-load font warnings.
5. `cylinder-chess-arxiv.zip` (211 KiB) and `cylinder-chess-overleaf.zip` (212 KiB, same
   tree + `latexmkrc` pinning XeLaTeX) are in this directory; both were unzipped into
   empty directories and rebuilt from scratch as a final check.

---

## 1. What was built

```
dist/arxiv/
├── src/                             the arXiv source tree (canonical)
│   ├── main.tex                     7 519 B
│   ├── macros.tex                     937 B
│   ├── refs.bib                     5 461 B
│   ├── main.bbl                     4 510 B
│   ├── sections/*.tex               17 files, 84 545 B
│   └── figures/*.pdf                27 files, 220 KiB
├── latexmkrc                          851 B   (Overleaf only)
├── build.sh                         7 179 B   (rebuild + verify + package, one command)
├── logs/
│   ├── tectonic-build.log           console log of the fresh build
│   ├── main.log                     the LaTeX log of that build
│   ├── main.blg                     the BibTeX log
│   └── main.pdf                     the PDF that build produced
├── cylinder-chess-arxiv.zip         215 643 B
├── cylinder-chess-overleaf.zip      216 256 B
└── REPORT.md                        this file
```

### 1.1 How the file list was derived (not hand-copied)

`build.sh` computes both lists from the sources themselves, so the package can never
drift from `main.tex`:

```bash
# sections: exactly the files main.tex \inputs
grep -oE '\\input\{sections/[^}]+\}' paper/ieee/main.tex \
  | sed -e 's|\\input{sections/||' -e 's|}$||' -e 's|$|.tex|' | sort -u

# figures: exactly the files some .tex \includegraphics's
grep -rhoE '\{figures/[^}]+\}' paper/ieee/main.tex paper/ieee/sections/*.tex \
  | sed 's/{figures\///;s/}//' | sort -u
```

Result: **17 sections, 27 figures**. Everything else in `paper/ieee` is deliberately
left out: `main_review.tex`, `main_review.*`, `REVIEW_LOG.md`, `REVIEW_FINDINGS.md`,
`REVISION_PLAN.md`, `ORCH_FIXES.md`, `SPEC.md`, `GUIDELINES.md`, `make_figures.py`,
`figures/INDEX.md`, `figures/src/`, `figures/superseded/`, and `figures/CoverPic.png`
(the cover photo is not `\includegraphics`'d anywhere).

### 1.2 Symlinks

`paper/ieee/figures` is a **real directory** at the time of writing (inode
224436109, distinct from `paper/figures`' 224401986) — the symlink that
`paper/ieee/GUIDELINES.md` §F warns about has been replaced. `build.sh` nevertheless
copies with `cp -L`, so any symlink is dereferenced on the way in, and it aborts if
`find src -type l` is non-empty. The shipped tree contains **0 symlinks**; the zip
contains only regular files.

### 1.3 Every shipped file is byte-identical to `paper/ieee`

```
same: main.tex   same: macros.tex   same: refs.bib   same: main.bbl
(sections checked: 17/17 identical)
(figures checked:  27/27 identical)
```

Reproduce:

```bash
cd /Users/aritro/Downloads/Research/Chessendgames
for f in main.tex macros.tex refs.bib main.bbl; do
  diff -q paper/ieee/$f dist/arxiv/src/$f; done
for f in dist/arxiv/src/sections/*.tex; do
  diff -q paper/ieee/sections/$(basename $f) $f; done
for f in dist/arxiv/src/figures/*.pdf; do
  diff -q paper/ieee/figures/$(basename $f) $f; done
```

---

## 2. The fresh build

### 2.1 Command

```bash
cd /Users/aritro/Downloads/Research/Chessendgames
./dist/arxiv/build.sh            # rebuild src/ from paper/ieee, verify, package
```

The build itself, run in a throw-away directory containing only the package files:

```bash
mkdir /tmp/fresh && cp -R dist/arxiv/src/. /tmp/fresh/ && cd /tmp/fresh
tectonic -X compile --only-cached -k --keep-logs main.tex
```

`--only-cached` forces tectonic to work **offline** from its local bundle; the whole
build ran in ~3 s with no network access.

Console log (`dist/arxiv/logs/tectonic-build.log`), in full:

```
note: "version 2" Tectonic command-line interface activated
note: using only cached resource files
note: Running TeX ...
warning: sections/02_rules:1: Underfull \vbox (badness 4940) has occurred while \output is active
note: Running BibTeX on main.aux ...
note: Rerunning TeX because bibtex was run ...
note: Rerunning TeX because "main.aux" changed ...
note: Running xdvipdfmx ...
note: Writing `main.log` (17.9248046875 KiB)
note: Writing `main.out` (2.9443359375 KiB)
note: Writing `main.blg` (373 B)
note: Writing `main.pdf` (325.033203125 KiB)
note: Writing `main.toc` (4.505859375 KiB)
note: Writing `main.bbl` (4.404296875 KiB)
note: Writing `main.aux` (27.109375 KiB)
```

### 2.2 Check results

| check | value | how measured |
|---|---|---|
| pages | **14** | `pdfinfo main.pdf \| grep Pages` |
| TeX errors (`!`, `Emergency stop`, `Fatal error`) | **0** | `grep -cE '^! \|Emergency stop\|Fatal error' main.log` |
| undefined references / citations | **0** | `grep -cE 'LaTeX Warning: (Reference\|Citation).*undefined\|There were undefined' main.log` |
| overfull boxes | **0** | `grep -cE 'Overfull \\\\[hv]box' main.log` |
| underfull boxes (in `main.log`) | **0** | same with `Underfull` (the one warning below is console-only; `main.log` has no `Underfull` line, and neither does `paper/ieee/main.log`) |
| multiply-defined labels | **0** | `grep -c 'multiply defined' main.log` |
| LaTeX font warnings | **5** (4 shape + 1 summary) | `grep -c 'LaTeX Font Warning' main.log` |
| bibitems in `main.bbl` | **16** | `grep -c '\\bibitem' main.bbl` |
| figures (numbered) | **10** (Fig. 1–10) | `newlabel{fig:...}` in `main.aux` |
| tables (numbered) | **8** (Table I–VIII) | `newlabel{tab:...}` in `main.aux` |
| underfull `\vbox` warning | 1, badness 4940, in `sections/02_rules` | engine console output |

The single underfull-`\vbox` warning is a column-height artefact on the page that
carries Section II; it is present in the paper's own build too and is cosmetic (it does
not set an overfull box and shifts no text).

### 2.3 The PDF is the paper

The freshly built PDF is **textually identical** to the checked-in `paper/ieee/main.pdf`,
page for page:

```bash
cd /tmp/fresh && pdftotext main.pdf fresh.txt
pdftotext /Users/aritro/Downloads/Research/Chessendgames/paper/ieee/main.pdf ref.txt
diff fresh.txt ref.txt          # no output -> identical
```

`pdfinfo` agrees on every field (Title, Author, 14 pages, 612×792 pts letter, PDF 1.5),
and `pdffonts` gives **byte-identical font lists** for both. So the package reproduces
the paper exactly; it does not merely compile.

### 2.4 The page count is 14, not 13 — why

This is the one requirement in the brief that the current sources do not meet, and the
cause is upstream of this task:

* `paper/ieee/REVIEW_LOG.md:326` (round before the last) records "Both builds: 13 pages".
* `paper/ieee/REVIEW_LOG.md:336` (orchestrator, 2026-10-22 01:00) records
  "**Layout:** both builds are now **14 pages** (the review build's limit)." That round
  added the 21 five-file ★2 positions in §VIII-D, the "Other widths" paragraph and
  Table VI in §X-A, and the `\IEEEtriggeratref{11}` that balances the reference columns
  onto page 14.
* `paper/ieee/main.pdf` (built 2026-10-22 00:56, i.e. after that round) is 14 pages, and
  `paper/ieee/main_review.pdf` is 14 pages too.

So the "13 pages" in the brief predates the final revision round. Two further checks
rule out packaging as the cause:

* Removing the table of contents entirely (`\@starttoc{toc}` commented out in a
  throw-away copy) still gives **14 pages** — the TOC is not what makes the difference.
* The build reads the same `sections/*.tex` as the paper, byte for byte (§1.3).

**Nothing in the package can be trimmed to recover the 13th page without editing the
paper's content, which is outside this task's scope.** If 13 pages is required, the
content decision (what to cut) has to be taken by the orchestrator; `build.sh` will then
rebuild the package automatically.

> Note for the IEEE submission, not for arXiv: IEEE ToG wants 10 pages, needs a written
> justification above 12, and charges $200/page beyond 10 (`paper/ieee/GUIDELINES.md` A).
> 14 pages is over both thresholds. arXiv itself has no page limit.

---

## 3. arXiv rule check (`paper/ieee/GUIDELINES.md` §F)

`build.sh` runs all of these automatically; the last run reported:

| rule | result | evidence |
|---|---|---|
| no `\write18` | **ok** | `grep -rqE '\\write18' src/*.tex src/sections/*.tex` → 0 hits (no `pgfplots` externalization, no `minted`) |
| relative paths only | **ok** | no `/Users/`, `/home/`, `/tmp/` or `C:\` in any `.tex`/`.bib`; every `\includegraphics` is `figures/<name>.pdf` |
| file names: letters, digits, `_ + - . , =` only | **ok** | `find src \| sed 's|.*/||' \| grep -E '[^A-Za-z0-9_+,=.-]'` → empty. All names match `[A-Za-z0-9_]+\.(tex|bib|bbl|pdf)`; no spaces, no uppercase-only collisions, no case-only duplicates |
| no hidden files | **ok** | `find src -name '.*' -mindepth 1` → empty |
| no `.aux`/`.log`/`.out`/`.toc`/`.blg`/`.synctex` | **ok** | none in the package. (The compiled `main.pdf` is **not** shipped — arXiv rejects a PDF of the paper; the `.pdf` files inside `figures/` are the figure artwork, which must be PDF/PNG/JPG) |
| no unused figures | **ok** | 27 files, 27 `\includegraphics` targets; the 8 unused figure PDFs in `paper/ieee/figures` and the cover photo are excluded |
| `main.bbl` present | **ok** | 4 510 B, named after `main.tex` |
| `main.bbl` current | **ok** | re-running BibTeX on `main.aux` reproduces it **byte for byte** (`diff` of the regenerated and shipped `.bbl` is empty); all 16 `\cite` keys are in `refs.bib` and in `main.bbl`; the one unused `refs.bib` entry (`Maeser2002`) correctly produces no `\bibitem` |
| total size < 10 MB | **ok** | 364 KiB unpacked, 211 KiB zipped |
| all figures PDF/PNG/JPG | **ok** | 27 × `.pdf`; no EPS/PS, so no conversion is needed |
| relative paths, no driver options to `hyperref` | **ok** | `\usepackage[hidelinks]{hyperref}` only — no `driver=` option |
| PDF bookmarks | **ok** | `main.out` contains `\BOOKMARK` entries for the 6 top-level sections; no `bookmarks=false` needed |
| no `\today` | **ok** | not used |
| bibliography | **ok** | `main.bbl` shipped; `refs.bib` also shipped (arXiv has been able to run BibTeX itself since Nov 2025 — if it does, it regenerates the identical file) |

**One action item, flagged in `main.tex:26-27` and not fixable from inside the package:**
`main.tex:29` currently reads `\submittedfalse`, so the built PDF carries **no** IEEE
preprint notice. `GUIDELINES.md` §F requires the notice
("This work has been submitted to the IEEE for possible publication…") on any preprint
posted *after* submission to the IEEE. If the paper has already been submitted, change
`\submittedfalse` → `\submittedtrue` in `paper/ieee/main.tex` and re-run
`./dist/arxiv/build.sh`; the package then ships the notice. `GUIDELINES.md` §F also says
to **ask the IEEE EiC before posting**, because some IEEE venues reject papers that
already have an arXiv preprint.

---

## 4. Fonts and packages the build needs

### 4.1 Class and packages (all resolved from the LaTeX log)

* Class: `IEEEtran` v1.8b (2015/08/26), `[journal]` option.
* Explicitly loaded: `cite`, `amsmath`, `amssymb`, `amsthm`, `graphicx`, `booktabs`,
  `array`, `subfig` (with `caption=false, font=footnotesize, labelformat=simple,
  justification=centering`), `url`, `hyperref` (with `hidelinks`), `fontenc` (T1).
* Pulled in by the above: `amsbsy`, `amsfonts`, `amsopn`, `amstext`, `auxhook`,
  `bigintcalc`, `bitset`, `caption3`, `etexcmds`, `gettitlestring`, `graphics`,
  `hycolor`, `iftex`, `infwarerr`, `intcalc`, `keyval`, `kvdefinekeys`, `kvoptions`,
  `kvsetkeys`, `l3backend`, `letltxmacro`, `ltxcmds`, `nameref`, `pdfescape`,
  `pdftexcmds`, `puenc`, `refcount`, `rerunfilecheck`, `stringenc`, `trig`,
  `uniquecounter`.
* Font definition files actually read: `t1ptm.fd`, `t1phv.fd`, `t1pcr.fd`, `ts1cmr.fd`,
  `umsa.fd`, `umsb.fd` (and under XeTeX also `xetex.def`, `hxetex.def`,
  `l3backend-xetex.def`).
* Nothing else: no `fontspec`, no `unicode-math`, no `babel`, no `inputenc`, no
  `minted`, no `pgfplots`, no `shellesc`.

All of these are in the TeX Live base/`latex-recommended` collection; arXiv's TeX Live
2025 has every one of them. None is in a collection arXiv omits.

### 4.2 Fonts in the output PDF

Split by origin (`pdffonts main.pdf`):

| origin | fonts |
|---|---|
| LaTeX text (psnfss via `t1ptm/t1phv/t1pcr.fd`) | **NimbusRomNo9L** Regular/Bold/Italic/BoldItalic (Times), **NimbusSanL** Regular/Italic (Helvetica), **NimbusMonL** Regular/Oblique (Courier) |
| LaTeX math (Computer Modern) | CMR 6/7/8/10, CMMI 6/7/8/10, CMSY 7/8/10, CMEX 10, CMBX 8/10, CMSS 8/10, MSBM 10 |
| inside the 27 figure PDFs (matplotlib) | TeX Gyre Heros, TeX Gyre Termes, TeX Gyre Termes Math, Apple Symbols |

The figure fonts are **already embedded in the figure PDFs** (they are produced by
`make_figures.py` with matplotlib), so arXiv does not need them installed. The LaTeX-side
fonts — Nimbus Roman (the URW Times clone) and the Computer Modern math set — are in
every TeX Live.

### 4.3 The four font warnings, explained

```
LaTeX Font Warning: Font shape `TU/ptm/m/n' undefined
(Font)              using `TU/lmr/m/n' instead on input line 503.
   (and TU/ptm/bx/n, TU/ptm/m/it, TU/ptm/bx/it)
LaTeX Font Warning: Some font shapes were not available, defaults substituted.
```

Cause, from `IEEEtran.cls` itself:

* `IEEEtran.cls:495` does `\renewcommand{\rmdefault}{ptm}` (and 494/497 set
  `\sfdefault{phv}`, `\ttdefault{pcr}`), then `IEEEtran.cls:502` does
  `\normalfont\selectfont`. That is the *class-load* moment, and it happens **before**
  the document's `\usepackage[T1]{fontenc}` (`main.tex:3`) has run. Under XeTeX the
  default encoding is `TU`, so LaTeX looks for `TUptm.fd` — which does not exist — and
  substitutes Latin Modern for that instant.
* `main.tex:3` then switches the encoding to `T1`; the log shows
  `LaTeX Font Info: Trying to load font information for T1+ptm` → `(t1ptm.fd` →
  the real Times. `pdffonts` confirms the body text is NimbusRomNo9L, and the rendered
  page 1 is visibly Times.

So the warnings are **class-load artefacts, not a font loss**. They are also
**XeTeX-only**: under pdfLaTeX the class-load check asks for `OT1+ptm`, and
`ot1ptm.fd` ships with psnfss in TeX Live, so a pdfLaTeX build of the same source
produces **no font warnings at all**.

### 4.4 Things that might fail on arXiv's TeX Live, and the verdict

| risk | verdict |
|---|---|
| non-ASCII characters without `inputenc` | **none.** Every `.tex` and `.bib` file in the package is pure ASCII (checked byte-wise: 0 lines with bytes ≥ 0x80). All diacritics are written as LaTeX escapes (`tr\'ebuchet`, `\'e`) |
| figures needing conversion | **none.** All 27 are PDF; pdfLaTeX embeds PDF natively, no `epstopdf`/`img2pdf` step, no shell escape |
| `\write18` / shell escape | **none used** |
| hyperref driver options | **none passed** (only `hidelinks`); `main.out` shows the bookmarks build, so `bookmarks=false` is not needed |
| `subfig` `labelformat=simple` | needs `subfig` ≥ 1.5 (2019-06-01); TeX Live 2025 has 1.5 |
| fonts | `t1ptm.fd`, `t1phv.fd`, `t1pcr.fd` (psnfss) and the CM math set are in base TeX Live; the figure fonts are embedded in the figure files |
| `main.bbl` | present, current, and byte-reproducible by BibTeX |
| arXiv's "no PDF" rule | the *paper's* PDF is not in the package; only figure PDFs are, as required |
| page count | arXiv imposes no page limit |

**Verdict: arXiv will compile the package.** The default engine is pdfLaTeX, and this
source is pdfLaTeX-clean; XeLaTeX also works (proven by the tectonic build, which is
XeTeX-based), with 5 cosmetic font warnings instead of 0.

---

## 5. The pdfLaTeX verdict, stated precisely

**The pdfLaTeX build was not executed.** This machine has no TeX distribution other than
`tectonic` (0.16.9): `pdflatex`, `xelatex`, `lualatex`, `latexmk`, `bibtex` and `tlmgr`
are all absent, and the task brief forbids installing anything. A filesystem-wide search
found no `pdftex`/`pdflatex` binary either. So the claim below is an **exhaustive
source-level analysis** (COMPUTED-1), not a completed run.

The analysis was done file by file against the actual package:

1. **Engine-specific packages: none.** `fontspec`, `unicode-math`, `luatexja`,
   `babel`, `ifthen` engine branches, `minted`, `pgfplots`: all absent.
2. **Input encoding: not needed.** Pure ASCII, so pdLaTeX's default `OT1` + the
   document's `T1` switch suffice. No `inputenc` is loaded and none is needed.
3. **Graphics: no conversion.** Every `\includegraphics` targets a `.pdf`; pdLaTeX
   includes PDF directly.
4. **Class:** `IEEEtran` 1.8b with the `journal` option — the single most widely used
   LaTeX class; `IEEEtran.cls` and `IEEEtran.bst` are in TeX Live.
5. **Packages:** `cite`, `amsmath`, `amssymb`, `amsthm`, `graphicx`, `booktabs`,
   `array`, `subfig`, `url`, `hyperref` — all in TeX Live base/`latex-recommended`.
6. **Fonts:** `t1ptm.fd` / `ot1ptm.fd` / `t1phv.fd` / `t1pcr.fd` from psnfss, plus the
   CM math set — all in TeX Live. Under pdLaTeX the IEEEtran class-load check finds
   `ot1ptm.fd` and emits **no** font warnings (XeTeX emits 4, for the reason given in
   §4.3).
7. **No shell escape, no absolute paths, no hidden files, no auxiliary files** (§3).

**Conclusion (reasoned verdict, not an executed run):** arXiv's default pdfLaTeX
processor will compile this package, and will do so with a *cleaner* log than the
tectonic build. The one thing that cannot be ruled out without running it is a
TeX Live-version-specific interaction, and nothing in the source is version-sensitive
(the newest construct used is `subfig`'s `labelformat=simple`, from 2019).

**If you want XeLaTeX on arXiv instead:** the paper builds under it as-is; select the
compiler in the submission's processing options if the form offers that choice.

**If the four XeTeX font warnings ever bother you:** the one-line fix is to add to
`main.tex` (after `\documentclass`)

```latex
\usepackage{fontspec}
\setmainfont{TeX Gyre Termes}
\setsansfont{TeX Gyre Heros}
\setmonofont{TeX Gyre Cursor}
```

which makes the XeTeX build font-correct without relying on the T1 fallback. This was
**not** applied: it would change the paper's source, and the current XeTeX build is
already font-correct in the output (NimbusRomNo9L = Times).

---

## 6. The two archives

### 6.1 `cylinder-chess-arxiv.zip` (215 643 B)

* 48 files + 2 directory entries, **no wrapper directory** — `main.tex` sits at the
  archive root, which is where arXiv compiles from.
* Contents: `main.tex`, `macros.tex`, `refs.bib`, `main.bbl`, `sections/` (17 `.tex`),
  `figures/` (27 `.pdf`).
* Built with `zip -X -r` (no extra file attributes, no symlinks, no hidden files).

### 6.2 `cylinder-chess-overleaf.zip` (216 256 B)

Identical tree, plus:

* **`latexmkrc`** (851 B), which pins the project to XeLaTeX:

  ```perl
  $pdf_mode = 3;                        # 3 = xelatex
  $xelatex  = 'xelatex -no-shell-escape %O %o';
  $bibtex   = 'bibtex %O %B';
  $max_repeat = 6;
  ```

* **one added comment line** at the top of `main.tex`:
  `%!TEX TS-program = xelatex`. This is the standard, engine-agnostic way to ask for
  XeLaTeX, and it wins over a project setting that would otherwise override
  `latexmkrc`. It is a comment: it changes nothing in the output.

  The arXiv zip does **not** carry this line, because arXiv's default pdfLaTeX is the
  better engine for this document (§4.3, §5).

* On Overleaf, also set **Menu → Settings → Compiler → XeLaTeX**: Overleaf's own
  compiler setting can take precedence over `latexmkrc`, and the magic comment is the
  belt to that pair of braces.

### 6.3 Both zips were rebuilt from scratch

```bash
mkdir -p /tmp/zc /tmp/zo
cd /tmp/zc && unzip -q .../cylinder-chess-arxiv.zip     && tectonic -X compile --only-cached main.tex
cd /tmp/zo && unzip -q .../cylinder-chess-overleaf.zip  && tectonic -X compile --only-cached main.tex
```

Both produce a **14-page** PDF whose extracted text is identical to
`paper/ieee/main.pdf`:

```
ARXIV ZIP -> pages: 14
OVERLEAF ZIP -> pages: 14
ARXIV ZIP PDF TEXT == paper/ieee/main.pdf TEXT
OVERLEAF-ZIP PDF TEXT == paper/ieee/main.pdf TEXT
```

---

## 7. Uploading to arXiv

1. **Get the endorsement first.** Since 2025-12-10 (math) and 2026-01-21 (all
   sections), an institutional e-mail alone no longer qualifies: a first math.CO paper
   needs a **personal endorser** (`GUIDELINES.md` §F, XEND). Get one from a
   math.CO author; a cs.GT-only endorsement will not cover math.CO.
2. **Decide about the IEEE submission first.** `GUIDELINES.md` §F: ask the IEEE EiC
   before posting, because some IEEE venues reject papers that already have an arXiv
   preprint. And if the paper has already been submitted to the IEEE, the preprint must
   carry the IEEE notice — set `\submittedtrue` in `paper/ieee/main.tex:29` and re-run
   `./dist/arxiv/build.sh` before uploading.
3. **Upload the ZIP, not the PDF.** arXiv rejects a PDF produced from TeX
   (`GUIDELINES.md` §F, XSUB). Upload `dist/arxiv/cylinder-chess-arxiv.zip` as a single
   archive.
4. **Metadata** (arXiv's "prep" page):
   * *Title:* `Chess Endgames on a Cylindrical Chessboard: Exact Combinatorial Game
     Values, Real-Chess Checks, and Tablebases`
   * *Authors:* `Aritro Bhattacharjee` (one author; arXiv wants the plain name)
   * *Abstract:* the text of `sections/00_abstract.tex` between `\begin{abstract}` and
     `\end{abstract}`, **without** the words "Abstract" and with `~` and `\emph` removed.
     The current abstract is already compliant: **1 124 characters** (limit 1 920),
     197 words, no `~`, no `\emph`, no LaTeX commands at all.
   * *Comments:* `14 pages, 10 figures, 8 tables. Code and data:
     https://github.com/aritroBh/cylindrical-chess-cgt . Submitted to IEEE Transactions
     on Games.` (report the real page count — 14; see §2.4.)
   * *MSC class:* **91A46** (combinatorial games).
   * *Categories:* primary **math.CO**, cross-list **cs.GT**.
   * *License:* the arXiv non-exclusive license 1.0 (keeps copyright transferable to
     IEEE; CC0 does not — `GUIDELINES.md` §F, XLIC).
5. **Processing options.** Leave the compiler at the default (pdfLaTeX) unless you
   have a reason not to; the source is pdfLaTeX-clean. If the form offers TeX Live
   2025 explicitly, take it.
6. **After upload, check arXiv's own PDF page by page** (`GUIDELINES.md` §F): it must be
   14 pages, the table of contents must be present, the reference columns must be
   balanced on page 14, and the figures must be readable in greyscale.
7. **AI disclosure.** The paper's Acknowledgment already names the systems used
   (Claude Opus 5.5, Codex, Nemotron 3 Ultra, MiniMax M3.1 Flash, and the routed models)
   and arXiv's moderation policy asks for significant generative-AI use to be reported;
   the Acknowledgment is the place. Check that every `\cite` resolves and that there is
   no leftover `TODO`/`VERIFY` in the sources before submitting
   (`GUIDELINES.md` §F, XMOD). *(Spot check done here: all 16 `\cite` keys are in
   `refs.bib` and `main.bbl`; no `TODO`/`FIXME`/`XXX`/`placeholder` string occurs in any
   shipped file — the only `verify` hits are the paper's own `\label{sec:verify}` and
   `\input{sections/13_verify}`, the "Verification and Reproducibility" section.)*
8. **Submission rate.** `GUIDELINES.md` §F (XRATE, a secondary source) mentions a cap
   of 2 new submissions per month from 2026-10-01; if that is in force, plan the
   arXiv posting around it. The same source describes a one-year ban for clear
   evidence of unchecked AI output (invented references, leftover placeholders) — the
   checks in step 7 are the precaution against that.
9. **Fixing a mistake afterwards:** replace the arXiv version (`v1` → `v2`), never
   submit a new paper (`GUIDELINES.md` §F, XSUB).
10. **Overleaf** (if the author wants a web copy): upload
    `dist/arxiv/cylinder-chess-overleaf.zip` to a new Overleaf project, set the
    compiler to XeLaTeX, and compile. The project root must contain `main.tex` and
    `latexmkrc`.

---

## 8. Command index (every number above, reproduced)

```bash
cd /Users/aritro/Downloads/Research/Chessendgames

# 0. full rebuild + verification + packaging (writes only into dist/arxiv/)
./dist/arxiv/build.sh

# 1. page count, errors, undefined refs, overfull boxes
mkdir /tmp/fresh && cp -R dist/arxiv/src/. /tmp/fresh/ && cd /tmp/fresh
tectonic -X compile --only-cached -k --keep-logs main.tex
pdfinfo main.pdf | grep Pages
grep -cE '^! |Emergency stop|Fatal error'            main.log
grep -cE 'LaTeX Warning: (Reference|Citation).*undefined' main.log
grep -cE 'Overfull \\[hv]box'                        main.log
grep -c 'LaTeX Font Warning'                          main.log

# 2. the PDF is the paper
pdftotext main.pdf fresh.txt
pdftotext ../../../paper/ieee/main.pdf ref.txt && diff fresh.txt ref.txt

# 3. fonts and packages actually used
pdffonts main.pdf
grep -oE 'Package: [A-Za-z0-9]+ ' main.log | sed 's/Package: //;s/ $//' | sort -u

# 4. arXiv rule checks
grep -rqE '\\write18' dist/arxiv/src/*.tex dist/arxiv/src/sections/*.tex   # -> no hits
find dist/arxiv/src -name '.*' -mindepth 1                                # -> empty
find dist/arxiv/src \( -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.toc' \)  # -> empty
find dist/arxiv/src -mindepth 1 | sed 's|.*/||' | LC_ALL=C grep -E '[^A-Za-z0-9_+,=.-]'  # -> empty
du -sk dist/arxiv/src                                                        # -> 364
unzip -Z1 dist/arxiv/cylinder-chess-arxiv.zip | wc -l                       # -> 50
```

## 9. Honest summary of what is and is not established

* **PROVED** — the package is complete and self-contained: the 17 sections and 27
  figures are exactly the sets `main.tex` needs, derived mechanically; every file is
  byte-identical to `paper/ieee`; no symlink survives; nothing outside the package is
  read at build time.
* **PROVED** — a fresh, offline build with `tectonic -X compile main.tex` succeeds with
  0 errors, 0 undefined references/citations, 0 overfull boxes, 0 multiply-defined
  labels, and the output PDF is textually identical to `paper/ieee/main.pdf`.
* **PROVED** — both zips, unzipped into empty directories, rebuild to the same 14-page
  PDF.
* **PROVED** — every arXiv rule checked in §3 passes; the source is pure ASCII; all
  figures are PDF; `main.bbl` is present, current and byte-reproducible.
* **COMPUTED-1** — the pdfLaTeX verdict (§5). It is an exhaustive source-level
  analysis of a real package, but the compile was not executed because no pdfLaTeX
  exists on this machine and installing is forbidden by the brief. The XeTeX build *was*
  executed, and the document is font-correct in its output despite the 4 class-load
  warnings.
* **Negative result, reported plainly** — the package is **14 pages**, not the 13 the
  brief asked for. The cause is the last content revision of the paper, not the
  packaging; the package reproduces the paper exactly. Recovering 13 pages requires
  cutting paper content, which is an orchestrator decision outside this task.
* **Not done / out of scope** — the IEEE preprint notice is **not** in the build
  (`\submittedfalse` in `paper/ieee/main.tex:29`); if the paper has already been
  submitted to the IEEE, that switch must be flipped and the package rebuilt. The
  arXiv posting itself was not performed (no network; endorsement required first).
* **No novelty is claimed** for any of the above; this is packaging and verification
  work.
