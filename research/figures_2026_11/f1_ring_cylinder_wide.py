"""F1 wide: M_10 on C_10, perspective cylinder (left) and unrolled board (right); double-column, <= 2.5 in tall.
Run from the repo root:  .venv/bin/python research/figures_2026_11/f1_ring_cylinder_wide.py
Position (files a..j): B4 W2 B6 W2 W3 B6 B7 W3 B7 W5.  The cylinder is rotated (OFF, the angle of the seam j|a)
to maximise the pawns that can be seen: front-wall pawns, plus far-wall pawns visible above the front rim.
Occluded far-wall pawns are not drawn; panel (b) shows all ten."""
import sys, os
from math import sin, cos, radians
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import build

POS = "B4 W2 B6 W2 W3 B6 B7 W3 B7 W5".split()
FILES = "abcdefghij"
NF, NR = 10, 8
R, S, K = 1.2, 0.185, 0.27
DEG = 360 / NF
GLY = 12.5
LAB = "font=\\sffamily\\fontsize{8}{8}\\selectfont"
MARGIN = 0.11     # clearance (in) of a far-wall pawn centre above the front rim

def P(phi, z, off=0):
    return (R * sin(radians(phi)), z * S - R * K * cos(radians(phi)))
def pt(p): return "(%.3f,%.3f)" % p
def phi_of(f, off): return (f * DEG + DEG / 2 + off + 180) % 360 - 180

def status(f, off):
    """'front', 'back-visible' or 'hidden' for the pawn on file f."""
    ph = phi_of(f, off); r = int(POS[f][1:])
    c = cos(radians(ph))
    if c > 0.15: return "front"
    if c > -1e-9: return "hidden"        # on the silhouette
    x, y = P(ph, r - 0.5)
    top_front = NR * S - R * K * abs(c)  # front rim at the same x
    return "back" if y - MARGIN > top_front and y < NR * S + R * K * abs(c) - 0.06 else "hidden"

best = None
for off in range(-60, 61):
    if cos(radians(off)) < 0.6: continue                          # seam must face the viewer
    st = [status(f, off) for f in range(NF)]
    score = (sum(s != "hidden" for s in st), -abs(off))
    if best is None or score > best[0]: best = (score, off, st)
(_, OFF), st = best[0], best[2]
OFF = best[1]
print("OFF", OFF, "visible", sum(s != "hidden" for s in st), "front", st.count("front"), "far", st.count("back"), st)

def quad(f, r, n=4):
    a, b = f * DEG + OFF, (f + 1) * DEG + OFF
    ph = [a + (b - a) * i / n for i in range(n + 1)]
    return " -- ".join(pt(q) for q in [P(p, r) for p in ph] + [P(p, r + 1) for p in reversed(ph)]) + " -- cycle"

def segs(f):
    """angular pieces of file f, split where the wall crosses the silhouette: [(a, b, is_front)]."""
    a, b = f * DEG + OFF, (f + 1) * DEG + OFF
    cuts = [a] + [c for c in range(-720, 721, 180) if a < c + 90 < b for c in [c + 90]] + [b]
    cuts = sorted(set([a, b] + [90 + 180 * k for k in range(-5, 6) if a < 90 + 180 * k < b]))
    return [(u, v, cos(radians((u + v) / 2)) > 0) for u, v in zip(cuts, cuts[1:])]

def quadab(a, b, r, n=4):
    ph = [a + (b - a) * i / n for i in range(n + 1)]
    return " -- ".join(pt(q) for q in [P(p, r) for p in ph] + [P(p, r + 1) for p in reversed(ph)]) + " -- cycle"

def pawn(at, white, size, xs):
    x, y = at
    sz = "\\fontsize{%.1f}{%.1f}\\selectfont" % (size, size)
    stl = "inner sep=0, transform shape, xscale=%.2f" % xs
    if white:
        return ["\\node[text=white, %s] at (%.3f,%.3f) {\\chessfont%s♟};" % (stl, x, y, sz),
                "\\node[text=black, %s] at (%.3f,%.3f) {\\chessfont%s♙};" % (stl, x, y, sz)]
    return ["\\node[text=black, %s] at (%.3f,%.3f) {\\chessfont%s♟};" % (stl, x, y, sz)]

front = lambda f: cos(radians(phi_of(f, OFF))) > -1e-9
o = [r"\begin{tikzpicture}[x=1in,y=1in]"]
# far wall: light squares with dashed edges (hidden below the opaque front wall), visible far pawns
for f in range(NF):
    for a, b, fr in segs(f):
        if not fr:
            for r in range(NR):
                col = "light" if (f + r) % 2 else "dark"
                o.append("\\fill[%s, fill opacity=0.35] %s;" % (col, quadab(a, b, r)))
                o.append("\\draw[edge!60, line width=0.35pt, dash pattern=on 1.6pt off 1.6pt] %s;" % quadab(a, b, r))
for f in range(NF):
    if st[f] == "back":
        o += pawn(P(phi_of(f, OFF), int(POS[f][1:]) - 0.5), POS[f][0] == "W", GLY * 0.85, 0.75)
for f in range(NF):                                   # front wall, opaque
    for a, b, fr in segs(f):
        if fr:
            for r in range(NR):
                col = "light" if (f + r) % 2 else "dark"
                o.append("\\fill[%s] %s;\\draw[edge, line width=0.35pt] %s;" % (col, quadab(a, b, r), quadab(a, b, r)))
o.append("\\draw[edge, line width=0.7pt] %s -- %s;" % (pt(P(-90, 0)), pt(P(-90, NR))))
o.append("\\draw[edge, line width=0.7pt] %s -- %s;" % (pt(P(90, 0)), pt(P(90, NR))))
o.append("\\draw[edge, line width=0.7pt] %s;" % (" -- ".join(pt(P(p, NR)) for p in range(0, 361, 6))))
o.append("\\draw[edge, line width=0.7pt] %s;" % (" -- ".join(pt(P(p, 0)) for p in range(-90, 91, 6))))
for f in range(NF):
    if st[f] == "front":
        ph = phi_of(f, OFF)
        o += pawn(P(ph, int(POS[f][1:]) - 0.5), POS[f][0] == "W", GLY, max(0.6, cos(radians(ph))))
o.append("\\draw[seam, line width=1.6pt] %s -- %s;" % (pt(P(OFF, -0.1)), pt(P(OFF, NR + 0.1))))
for r in range(NR):
    x, y = P(-90, r + 0.5)
    o.append("\\node[anchor=east, text=black!70, %s, inner sep=2pt] at (%.3f,%.3f) {%d};" % (LAB, x - 0.01, y, r + 1))
for f in range(NF):                                   # file letters: front below the bottom rim, far ones above the top rim
    ph = phi_of(f, OFF)
    if front(f):
        x, y = P(ph, 0)
        o.append("\\node[anchor=north, text=black!70, %s, inner sep=1.5pt] at (%.3f,%.3f) {%s};" % (LAB, x, y, FILES[f]))
cyl_bottom = P(OFF, 0)[1]
o.append("\\node[seam, anchor=north, %s, inner sep=1pt] at (%.3f,%.3f) {seam};" % (LAB, P(OFF, 0)[0], cyl_bottom - 0.17))
top = NR * S + R * K
bottom = cyl_bottom - 0.17 - 0.14
o.append("\\node[anchor=north west, font=\\bfseries\\fontsize{8}{8}\\selectfont] at (%.3f,%.3f) {(a)};" % (-R - 0.38, top))
# arrow between the panels
ax = R + 0.30
o.append("\\draw[-{Latex[length=4pt]}, line width=0.8pt, edge] (%.3f,%.3f) -- (%.3f,%.3f);" % (ax, 1.0 * S, ax, 7.5 * S))
o.append("\\node[rotate=90, font=\\fontsize{8}{8}\\selectfont, text=black!70, inner sep=1pt, fill=white] at (%.3f,%.3f) {White moves up};" % (ax, 4.25 * S))
# flat board, same overall height
H = top - bottom
CW = (H - 0.17) / NR
gx = ax + 0.35 + 0.22 + CW                              # left edge of file a (after the left ghost column)
X = lambda f: gx + f * CW
Y = lambda r: top - NR * CW + r * CW                    # top of the board aligns with the top of panel (a)
o.append("\\begin{scope}")
o.append("\\clip (%.3f,%.3f) rectangle (%.3f,%.3f);" % (X(-1), Y(0) - 0.01, X(NF + 1), Y(NR) + 0.01))
for f in range(-1, NF + 1):
    ff, ghost = f % NF, (f < 0 or f >= NF)
    for r in range(NR):
        col = "light" if (ff + r) % 2 else "dark"
        o.append("\\fill[%s%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (col, ", fill opacity=0.35" if ghost else "", X(f), Y(r), X(f + 1), Y(r + 1)))
        o.append("\\draw[edge%s, line width=0.3pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % ("!35" if ghost else "", X(f), Y(r), X(f + 1), Y(r + 1)))
    if ghost: o.append("\\begin{scope}[opacity=0.4]")
    o += pawn((X(f + 0.5), Y(int(POS[ff][1:]) - 0.5) + 0.01), POS[ff][0] == "W", GLY, 1.0)
    if ghost: o.append("\\end{scope}")
o.append("\\end{scope}")
o.append("\\draw[edge, line width=0.7pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (X(0), Y(0), X(NF), Y(NR)))
for x in (X(0), X(NF)):
    o.append("\\draw[seam, line width=1.6pt, dash pattern=on 4pt off 2.5pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x, Y(0) - 0.05, x, Y(NR) + 0.05))
for r in range(NR):
    o.append("\\node[anchor=east, text=black!70, %s, inner sep=2pt] at (%.3f,%.3f) {%d};" % (LAB, X(-1), Y(r + 0.5), r + 1))
for f in range(NF):
    o.append("\\node[anchor=north, text=black!70, %s, inner sep=1.5pt] at (%.3f,%.3f) {%s};" % (LAB, X(f + 0.5), Y(0), FILES[f]))
o.append("\\node[anchor=north west, font=\\bfseries\\fontsize{8}{8}\\selectfont] at (%.3f,%.3f) {(b)};" % (X(-1) - 0.38, top))
o.append(r"\end{tikzpicture}")
build("f1_ring_cylinder_wide", "\n".join(o))
