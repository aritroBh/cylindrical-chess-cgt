"""F2: least number of pawns in a ring of value *2 (and *3) on C_n.  Run from repo root:
    .venv/bin/python research/figures_2026_11/f2_least_pawns.py
Data (paper/ieee/sections/08_star2.tex lines 136-146, 14_conclusion.tex line 13, 01_intro.tex lines 46-48):
  *2: n+3 for n=3..7 (6..10) [C2], ten for n=7..10 [C2], n for n>=10 [S whole-board; C2 witnesses n=10,11].
  *3: ten on C7, C8 (nothing smaller; C1), n+2=12 on C10, n+1=12 on C11, 13 on C12 [C1]; at most n+1 for n>=13 [S].
  No *3 ring is known on C3..C6 or C9 (C9: none with 9 or 10 pawns), so nothing is plotted there."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import build

N = list(range(3, 21))
def least2(n):
    return n + 3 if n <= 7 else (10 if n <= 10 else n)
two = [(n, least2(n)) for n in N]
two_comp = [p for p in two if p[0] <= 11]       # computed (C1/C2) or explicit C2 witness
two_proved = [p for p in two if p[0] >= 12]     # proved for all n (S)
three_comp = [(7, 10), (8, 10), (10, 12), (11, 12), (12, 13)]  # exact minima; none known for n<=6, 9
overlap = [p for p in two_comp if p in three_comp or p[0] in (7, 8)]  # *2 points sharing a place with a *3 square, redrawn on top
three_ub = [(n, n + 1) for n in range(13, 21)]
co = lambda pts: " ".join("(%d,%d)" % p for p in pts)

body = r"""
\begin{tikzpicture}\begin{axis}[width=7.0cm, height=5.6cm, scale only axis,
  xmin=2.5, xmax=20.5, ymin=5, ymax=22, xtick={4,6,...,20}, ytick={6,8,...,22},
  xlabel={files $n$ of the cylinder $C_n$}, ylabel={least pawns in a ring},
  ymajorgrids, grid style={gray!25}, axis line style={edge}, tick style={edge}, major tick length=2pt,
  every axis label/.append style={font=\fontsize{8}{9.6}\selectfont},
  legend style={at={(0.02,0.98)}, anchor=north west, draw=none, fill=white, fill opacity=0.85, text opacity=1,
    inner sep=1pt, row sep=-1pt, font=\fontsize{8}{9}\selectfont, legend cell align=left},
  legend image post style={xscale=0.8}]
\addplot[black!60, line width=0.4pt, dash pattern=on 2pt off 2pt] coordinates {(3,3) (20,20)};
\addlegendentry{$n$ pawns (one per file)}
\addplot[forget plot, const plot mark mid, edge, line width=0.8pt] coordinates {%s};
\addplot[only marks, mark=*, mark size=2.0pt, fill=dark, draw=edge] coordinates {%s};
\addlegendentry{$\star2$, computed}
\addplot[only marks, mark=o, mark size=2.2pt, draw=edge, fill=white, line width=0.7pt] coordinates {%s};
\addlegendentry{$\star2$, proved for all $n$}
\addplot[only marks, mark=square*, mark size=2.9pt, fill=seam, draw=edge] coordinates {%s};
\addlegendentry{$\star3$, computed}
\addplot[forget plot, only marks, mark=*, mark size=2.0pt, fill=dark, draw=edge] coordinates {%s};
\addplot[only marks, mark=triangle, mark size=2.6pt, draw=seam, fill=white, line width=0.8pt, mark options={rotate=180}] coordinates {%s};
\addlegendentry{$\star3$, at most $n+1$ (proved)}
\end{axis}\end{tikzpicture}
""" % (co(two), co(two_comp), co(two_proved), co(three_comp), co(overlap), co(three_ub))
build("f2_least_pawns", body)
