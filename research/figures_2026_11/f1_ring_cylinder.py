"""F1: the ring M_10 on the ten-file cylinder C_10, in perspective (top) and unrolled (bottom).
Run from the repo root:  .venv/bin/python research/figures_2026_11/f1_ring_cylinder.py
Position (files a..j): B4 W2 B6 W2 W3 B6 B7 W3 B7 W5 (paper/ieee/sections/08_star2.tex, 'ten-pawn rings ...')."""
import sys, os
from math import sin, cos, radians
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import build

POS = "B4 W2 B6 W2 W3 B6 B7 W3 B7 W5".split()
FILES = "abcdefghij"
NF, NR = 10, 8
R, S, K = 1.0, 0.19, 0.30
OFF = 18                             # the seam sits 18 degrees right of the front centre, so no file straddles the outline          # radius, rank height (in), tilt
DEG = 360 / NF
LAB = "font=\\sffamily\\fontsize{8}{8}\\selectfont"

def P(phi, z):                       # phi in degrees, 0 = front centre = seam; z in ranks
    return (R * sin(radians(phi)), z * S - R * K * cos(radians(phi)))
def pt(p): return "(%.3f,%.3f)" % p

def pawn(at, white, size, xs):
    x, y = at
    sz = "\\fontsize{%.1f}{%.1f}\\selectfont" % (size, size)
    st = "inner sep=0, transform shape, xscale=%.2f" % xs
    out = []
    if white:
        out.append("\\node[text=white, %s] at (%.3f,%.3f) {\\chessfont%s♟};" % (st, x, y, sz))
        out.append("\\node[text=black, %s] at (%.3f,%.3f) {\\chessfont%s♙};" % (st, x, y, sz))
    else:
        out.append("\\node[text=black, %s] at (%.3f,%.3f) {\\chessfont%s♟};" % (st, x, y, sz))
    return out

def phi_of(f):
    c = f * DEG + DEG / 2 + OFF
    return (c + 180) % 360 - 180
def is_front(f): return cos(radians(phi_of(f))) > -1e-6

def quad(f, r, n=4):
    a, b = f * DEG + OFF, (f + 1) * DEG + OFF
    ph = [a + (b - a) * i / n for i in range(n + 1)]
    lo = [P(p, r) for p in ph]; hi = [P(p, r + 1) for p in reversed(ph)]
    return " -- ".join(pt(q) for q in lo + hi) + " -- cycle"

o = [r"\begin{tikzpicture}[x=1in,y=1in]"]
for f in range(NF):                                  # back half: dashed wireframe, faded pawns
    if not is_front(f):
        for r in range(NR):
            o.append("\\draw[edge!60, line width=0.35pt, dash pattern=on 1.6pt off 1.6pt] %s;" % quad(f, r))
for f, t in enumerate(POS):
    if not is_front(f):
        o += pawn(P(phi_of(f), int(t[1:]) - 0.5), t[0] == "W", 10.5, 0.7)
for f in range(NF):                                  # front half: translucent squares
    if is_front(f):
        for r in range(NR):
            col = "light" if (f + r) % 2 else "dark"
            o.append("\\fill[%s, fill opacity=0.80] %s;" % (col, quad(f, r)))
            o.append("\\draw[edge, line width=0.35pt] %s;" % quad(f, r))
o.append("\\draw[edge, line width=0.7pt] %s -- %s;" % (pt(P(-90, 0)), pt(P(-90, NR))))
o.append("\\draw[edge, line width=0.7pt] %s -- %s;" % (pt(P(90, 0)), pt(P(90, NR))))
o.append("\\draw[edge, line width=0.7pt] %s;" % (" -- ".join(pt(P(p, NR)) for p in range(0, 361, 6))))
o.append("\\draw[edge, line width=0.7pt] %s;" % (" -- ".join(pt(P(p, 0)) for p in range(-90, 91, 6))))
for f, t in enumerate(POS):                          # front pawns
    if is_front(f):
        ph = phi_of(f)
        o += pawn(P(ph, int(t[1:]) - 0.5), t[0] == "W", 12.5, max(0.55, cos(radians(ph))))
o.append("\\draw[seam, line width=1.6pt] %s -- %s;" % (pt(P(OFF, -0.12)), pt(P(OFF, NR + 0.12))))
for r in range(NR):                                  # rank numbers on the left silhouette
    x, y = P(-90, r + 0.5)
    o.append("\\node[anchor=east, text=black!70, %s, inner sep=2pt] at (%.3f,%.3f) {%d};" % (LAB, x - 0.02, y, r + 1))
for f in range(NF):                                  # file letters: front below, back above
    x, y = P(phi_of(f), 0 if is_front(f) else NR)
    if is_front(f):
        o.append("\\node[anchor=north, text=black!70, %s, inner sep=1.5pt] at (%.3f,%.3f) {%s};" % (LAB, x, y, FILES[f]))
    else:
        o.append("\\node[anchor=south, text=black!50, %s, inner sep=1.5pt] at (%.3f,%.3f) {%s};" % (LAB, x, y, FILES[f]))
o.append("\\draw[-{Latex[length=4pt]}, line width=0.8pt, edge] (%.3f,%.3f) -- (%.3f,%.3f);" % (R + 0.14, 1 * S, R + 0.14, 7.5 * S))
o.append("\\node[rotate=90, font=\\fontsize{8}{8}\\selectfont, text=black!70] at (%.3f,%.3f) {White moves up};" % (R + 0.31, 4.3 * S))
# flat board below
CW = 0.235
cyl_bottom = -R * K - 0.30
x0, y0 = -5 * CW, cyl_bottom - 0.40 - NR * CW
X = lambda f: x0 + f * CW
Y = lambda r: y0 + r * CW
o.append("\\begin{scope}")
o.append("\\clip (%.3f,%.3f) rectangle (%.3f,%.3f);" % (X(-1), Y(0) - 0.01, X(NF + 1), Y(NR) + 0.01))
for f in range(-1, NF + 1):
    ff, ghost = f % NF, (f < 0 or f >= NF)
    for r in range(NR):
        col = "light" if (ff + r) % 2 else "dark"
        o.append("\\fill[%s%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (col, ", fill opacity=0.35" if ghost else "", X(f), Y(r), X(f + 1), Y(r + 1)))
        o.append("\\draw[edge%s, line width=0.3pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % ("!35" if ghost else "", X(f), Y(r), X(f + 1), Y(r + 1)))
    t = POS[ff]
    if ghost: o.append("\\begin{scope}[opacity=0.4]")
    o += pawn((X(f + 0.5), Y(int(t[1:]) - 0.5) + 0.01), t[0] == "W", 12.5, 1.0)
    if ghost: o.append("\\end{scope}")
o.append("\\end{scope}")
o.append("\\draw[edge, line width=0.7pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (X(0), Y(0), X(NF), Y(NR)))
for x in (X(0), X(NF)):
    o.append("\\draw[seam, line width=1.6pt, dash pattern=on 4pt off 2.5pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x, Y(0) - 0.07, x, Y(NR) + 0.07))
for r in range(NR):
    o.append("\\node[anchor=east, text=black!70, %s, inner sep=2pt] at (%.3f,%.3f) {%d};" % (LAB, X(-1), Y(r + 0.5), r + 1))
for f in range(NF):
    o.append("\\node[anchor=north, text=black!70, %s, inner sep=1.5pt] at (%.3f,%.3f) {%s};" % (LAB, X(f + 0.5), Y(0), FILES[f]))
o.append("\\node[seam, anchor=south, %s, inner sep=1pt] at (%.3f,%.3f) {seam: $j$ is next to $a$};" % (LAB, (X(0) + X(NF)) / 2, Y(NR) + 0.09))
o.append("\\node[anchor=north west, font=\\bfseries\\fontsize{8}{8}\\selectfont] at (%.3f,%.3f) {(a)};" % (-R - 0.62, NR * S + R * K + 0.30))
o.append("\\node[anchor=north west, font=\\bfseries\\fontsize{8}{8}\\selectfont] at (%.3f,%.3f) {(b)};" % (-R - 0.62, Y(NR) + 0.27))
o.append(r"\end{tikzpicture}")
build("f1_ring_cylinder", "\n".join(o))
