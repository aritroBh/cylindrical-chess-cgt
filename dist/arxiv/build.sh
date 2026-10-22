#!/bin/bash
# Rebuild, verify and package the arXiv / Overleaf source of
# "Chess Endgames on a Cylindrical Chessboard" (A. Bhattacharjee).
#
#   ./dist/arxiv/build.sh
#
# Steps
#   1. Rebuild dist/arxiv/src/ from paper/ieee, keeping only what main.tex needs
#      and resolving every symlink into a real file.
#   2. Fresh-build the tree in a throw-away directory with
#      `tectonic -X compile main.tex` (offline: --only-cached).
#   3. Check the build: page count, errors, undefined references/citations,
#      overfull boxes.
#   4. Write dist/arxiv/cylinder-chess-arxiv.zip and
#      dist/arxiv/cylinder-chess-overleaf.zip.
#
# Nothing outside dist/arxiv/ is written to, and paper/ is never modified.
# The only requirement is `tectonic` on PATH (0.16 or later) and `zip`.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PAPER="$ROOT/paper/ieee"
SRC="$HERE/src"
LOGDIR="$HERE/logs"

command -v tectonic >/dev/null 2>&1 || { echo "FATAL: tectonic not found on PATH"; exit 1; }
command -v zip      >/dev/null 2>&1 || { echo "FATAL: zip not found on PATH"; exit 1; }

rm -rf "$LOGDIR"
mkdir -p "$LOGDIR" "$SRC/sections" "$SRC/figures"

# ---------------------------------------------------------------- 1. gather --
# Sections: exactly the files main.tex \inputs.
SECTIONS=$(cd "$PAPER" && grep -oE '\\input\{sections/[^}]+\}' main.tex \
             | sed -e 's|\\input{sections/||' -e 's|}$||' -e 's|$|.tex|' | sort -u)
# Figures: exactly the files some .tex \includegraphics's.
FIGURES=$(cd "$PAPER" && grep -rhoE '\{figures/[^}]+\}' main.tex sections/*.tex \
             | sed 's/{figures\///;s/}//' | sort -u)

echo "== 1. collecting source =========================================="
rm -f "$SRC"/*.tex "$SRC"/*.bib "$SRC"/*.bbl
rm -rf "$SRC/sections" "$SRC/figures"
mkdir -p "$SRC/sections" "$SRC/figures"

# cp -L resolves symlinks into real files (paper/ieee/figures was a symlink in
# an earlier revision; it is a real directory now, but keep -L anyway).
cp -L "$PAPER/main.tex" "$PAPER/macros.tex" "$PAPER/refs.bib" "$PAPER/main.bbl" "$SRC/"
for s in $SECTIONS; do cp -L "$PAPER/sections/$s" "$SRC/sections/$s"; done
for f in $FIGURES; do cp -L "$PAPER/figures/$f" "$SRC/figures/$f"; done

echo "   main.tex, macros.tex, refs.bib, main.bbl"
echo "   sections: $(echo "$SECTIONS" | wc -w | tr -d ' ') files"
echo "   figures : $(echo "$FIGURES" | wc -w | tr -d ' ') files"
if find "$SRC" -type l | grep -q .; then
  echo "FATAL: symlinks survived into src/"; exit 1
fi

# ---------------------------------------------------------------- 2. build --
echo
echo "== 2. fresh build in a throw-away directory ======================="
TMP=$(mktemp -d "${TMPDIR:-/tmp}/cylchess-arxiv.XXXXXX")
trap 'rm -rf "$TMP"' EXIT
cp -R "$SRC/." "$TMP/"
( cd "$TMP" && tectonic -X compile --only-cached -k --keep-logs main.tex ) \
    > "$LOGDIR/tectonic-build.log" 2>&1 || {
      echo "FATAL: tectonic failed; see $LOGDIR/tectonic-build.log"; exit 1; }
cp "$TMP/main.log" "$LOGDIR/main.log"
cp "$TMP/main.blg" "$LOGDIR/main.blg"
cp "$TMP/main.pdf" "$LOGDIR/main.pdf"

# ---------------------------------------------------------------- 3. check --
echo
echo "== 3. checks ======================================================"
PAGES=$( (command -v pdfinfo >/dev/null 2>&1 && pdfinfo "$TMP/main.pdf" | awk '/^Pages:/{print $2}') || echo "")
[ -n "$PAGES" ] || PAGES=$(grep -oE 'Output written on main\.pdf \(([0-9]+) pages' "$TMP/main.log" | grep -oE '[0-9]+' | head -1)
NERR=$(grep -cE '^! |^!$|Emergency stop|Fatal error' "$TMP/main.log" || true)
NUNDEF=$(grep -cE 'LaTeX Warning: (Reference|Citation).*undefined|There were undefined references|There were undefined citations' "$TMP/main.log" || true)
NOVER=$(grep -cE 'Overfull \\\\[hv]box' "$TMP/main.log" || true)
NUNDER=$(grep -cE 'Underfull \\\\[hv]box' "$TMP/main.log" || true)
NREDEF=$(grep -cE 'multiply defined' "$TMP/main.log" || true)
NBIB=$(grep -c '\\bibitem' "$TMP/main.bbl" || true)

echo "   pages (pdfinfo)        : $PAGES"
echo "   errors                 : $NERR"
echo "   undefined refs/cites   : $NUNDEF"
echo "   overfull boxes         : $NOVER"
echo "   underfull boxes        : $NUNDER"
echo "   multiply defined lbls  : $NREDEF"
echo "   bibitems in main.bbl   : $NBIB"
echo "   LaTeX font warnings    : $(grep -c 'LaTeX Font Warning' "$TMP/main.log" || true)"

# ------------------------------------------------------- 3b. arXiv rule check --
echo
echo "   -- arXiv rule check (paper/ieee/GUIDELINES.md section F) --"
fail=0
if grep -rqE '\\write18' "$SRC"/*.tex "$SRC"/sections/*.tex; then
  echo "   FAIL: \\write18 present"; fail=1
else echo "   ok  : no \\write18"; fi
if grep -rqE '(/Users/|/home/|/tmp/|[A-Za-z]:\\\\)' "$SRC"/*.tex "$SRC"/sections/*.tex "$SRC"/refs.bib; then
  echo "   FAIL: absolute path present"; fail=1
else echo "   ok  : relative paths only"; fi
if find "$SRC" -name '.*' -mindepth 1 | grep -q .; then
  echo "   FAIL: hidden file present"; fail=1
else echo "   ok  : no hidden files"; fi
if find "$SRC" \( -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.toc' -o -name '*.blg' -o -name '*.synctex*' \) | grep -q .; then
  echo "   FAIL: auxiliary file present"; fail=1
else echo "   ok  : no .aux/.log/.out/.toc/.blg"; fi
badnames=$(find "$SRC" -mindepth 1 | sed 's|.*/||' | LC_ALL=C grep -E '[^A-Za-z0-9_+,=.-]' || true)
if [ -n "$badnames" ]; then
  echo "   FAIL: bad file name(s):"; echo "$badnames" | sed 's/^/          /'; fail=1
else echo "   ok  : file names use only a-z A-Z 0-9 _ + - . , ="; fi
if [ -s "$SRC/main.bbl" ]; then echo "   ok  : main.bbl present ($(wc -c < "$SRC/main.bbl" | tr -d ' ') bytes)"; else echo "   FAIL: main.bbl missing"; fail=1; fi
SZ=$(du -sk "$SRC" | awk '{print $1}')
if [ "$SZ" -lt 10240 ]; then echo "   ok  : size ${SZ} KiB < 10 MB"; else echo "   FAIL: size ${SZ} KiB >= 10 MB"; fail=1; fi
if find "$SRC" -name '*.eps' -o -name '*.ps' | grep -q .; then
  echo "   FAIL: EPS/PS figure present (arXiv wants PDF/PNG/JPG)"; fail=1
else echo "   ok  : all figures are PDF"; fi

# ---------------------------------------------------------------- 4. zips --
echo
echo "== 4. packaging =================================================="
rm -f "$HERE/cylinder-chess-arxiv.zip" "$HERE/cylinder-chess-overleaf.zip"
( cd "$SRC" && zip -q -X -r "$HERE/cylinder-chess-arxiv.zip" . -x '.*' )
# Overleaf variant: same tree plus latexmkrc and a %!TEX engine line.
OVL=$(mktemp -d "${TMPDIR:-/tmp}/cylchess-ovl.XXXXXX")
cp -R "$SRC/." "$OVL/"
cp "$HERE/latexmkrc" "$OVL/latexmkrc"
{ printf '%%!TEX TS-program = xelatex\n'; cat "$SRC/main.tex"; } > "$OVL/main.tex"
( cd "$OVL" && zip -q -X -r "$HERE/cylinder-chess-overleaf.zip" . -x '.*' )
rm -rf "$OVL"
echo "   cylinder-chess-arxiv.zip      $(du -k "$HERE/cylinder-chess-arxiv.zip" | awk '{print $1}') KiB"
echo "   cylinder-chess-overleaf.zip   $(du -k "$HERE/cylinder-chess-overleaf.zip" | awk '{print $1}') KiB"

echo
echo "== done =========================================================="
if [ "$fail" -ne 0 ]; then echo "RESULT: arXiv rule check FAILED"; exit 1; fi
echo "RESULT: all arXiv rule checks passed"
exit 0
