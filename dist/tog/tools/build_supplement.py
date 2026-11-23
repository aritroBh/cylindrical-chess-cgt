"""Assemble supp/*.tex for supplement.tex: the material moved out of the 10-page version (taken verbatim from
the long version, dist/tog/long/ = copy of paper/ieee/sections/) and the full proofs (converted from Markdown
by tools/md2tex.py, or taken from proof.tex). Run from dist/tog: python3 tools/build_supplement.py"""
import os, re, sys
sys.path.insert(0, 'tools')
import md2tex
import clean_notes
R = '../../'
os.makedirs('supp', exist_ok=True)
MAIN_LABELS = set(re.findall(r'\\label\{([^}]+)\}', ''.join(open('sections/' + f).read() for f in os.listdir('sections'))))

# labels of moved items that the main text reuses for something else get an S suffix in the supplement
REN = {'fig:basic': 'fig:basicS', 'fig:ep_test': 'fig:epS', 'sec:basic-inf': 'S-basic-inf'}

def L(f, a, b):
    lines = open('long/' + f + '.tex').read().split('\n')[a - 1:b]
    s = '\n'.join(lines)
    for k, v in REN.items():
        s = re.sub(r'\{%s\}' % re.escape(k), '{%s}' % v, s)
    # labels that the main text still defines are dropped here (references resolve to the main text via xr)
    s = re.sub(r'\\label\{([^}]+)\}', lambda m: '' if m.group(1) in MAIN_LABELS else m.group(0), s)
    s = s.replace('figure*', 'figure').replace('table*', 'table').replace('[!t]', '[!htbp]')
    s = s.replace(r'\columnwidth', r'\linewidth')
    s = s.replace(r'{0.16\textwidth}', r'{0.165\textwidth}').replace(r'height=1.05in', r'height=1.1in')  # labels >= 8 pt
    return s + '\n'

def W(name, *parts):
    open('supp/' + name + '.tex', 'w').write('\n'.join(parts))

def scrub(t):
    return t.replace('/Users/aritro/Downloads/Research/Chessendgames/', '').replace('/Users/aritro/', '~/')

def MD(path, a=None, b=None, cur=None):
    # a hand-edited copy in supp_src/ replaces the automatic clean-up of the working note
    if cur and os.path.exists('supp_src/' + cur):
        lines = open('supp_src/' + cur, encoding='utf-8').read().split('\n')
        return scrub('\n'.join(md2tex.convert(lines))) + '\n'
    lines = open(R + path, encoding='utf-8').read().split('\n')
    if a:
        lines = lines[a - 1:b]
    lines = clean_notes.clean(lines)
    return scrub('\n'.join(md2tex.convert(lines))) + '\n'

NOTE = (r'\noindent\emph{Source.} ' '%s. ' r'The note is typeset here without changes to its mathematics; it keeps its own '
        r'numbering, labels (PROVED, CHECKED-2, COMPUTED-1, CONJECTURE) and file references, which are paths in the '
        r'code repository. Its statements correspond to the main text as follows: %s' '\n\n')

# S1 basic positions -----------------------------------------------------------------------------
W('s01',
  r'\section{Basic Positions and the E.p.-Aware Test}\label{S-basic}',
  r'This section holds the walk-throughs of Section~\ref{sec:basic} and the census statistics of Section~\ref{sec:ep} '
  r'of the main text. Fig.~\ref{fig:basicS} shows the six basic boards; boards (a) and (f) are '
  r'Fig.~\ref{fig:basic}(b) and (c) of the main text.',
  L('02_rules', 52, 91),
  L('02_rules', 98, 105),
  L('03_basic', 3, 52))

# S2 kings -----------------------------------------------------------------------------------------
W('s02',
  r'\section{Kings: Certificates, Loopy Games and the Failure Sweep}\label{S-kings}',
  r'This section holds the parts of Section~\ref{sec:kings} of the main text that were moved out: the certificate '
  r'theory, the local test for (V2), the loopy games and the details of the failure sweep. Full proofs are in Section~\ref{S-kingsproof}.',
  r'\subsection{Certificates}',
  L('04_kings', 89, 127),
  L('04_kings', 129, 154),
  r'\subsection{Details of the Failure Sweep}',
  L('04_kings', 158, 168),
  r'Fig.~\ref{fig:f3} shows the agreement rates with Wilson 95\% intervals. The intervals treat positions as '
  r'independent and so are optimistic.',
  r'''\begin{figure}[!htbp]
\centering
\includegraphics{figures/f3_model_vs_chess.pdf}
\caption{Agreement between the model and real chess, with Wilson 95\% intervals. Top: ordinary $8\times8$ board
beside a tr\'ebuchet, $2{,}049$ decisive positions, by race rule (count rule best). Bottom: exact king-and-pawn
results on small boards.}
\label{fig:f3}
\end{figure}
''')


# S3.4 two checks of the sum model: tables copied from research/sum_whole_census/analysis_wall.md (Table 1 of REPORT.md
# and the heredity table) and from research/sum_truth_cyl/REPORT.md, section "12 GB runs"
CENSUS = [  # test, rule, D and N over all positions, D and N over HSS positions, D and N over non-HSS positions
  ('textbook', 'count', 11595, 599098, 0, 539893, 11595, 59205),
  ('textbook', 'mover', 10496, 599098, 0, 539893, 10496, 59205),
  ('textbook', 'opponent', 12104, 599098, 0, 539893, 12104, 59205),
  ('e.p.-aware', 'count', 11300, 599098, 0, 540503, 11300, 58595),
  ('e.p.-aware', 'mover', 9243, 599098, 0, 540503, 9243, 58595),
  ('e.p.-aware', 'opponent', 12100, 599098, 0, 540503, 12100, 58595)]
def n_(x): return '$' + '{:,}'.format(x).replace(',', '{,}') + '$'
def frac(d, n): return n_(d) + ' / ' + n_(n)
census_rows = '\n'.join('%s & %s & %s & %s & %s\\\\' % (t, r, frac(a, b), frac(c, d), frac(e, f))
                        for (t, r, a, b, c, d, e, f) in CENSUS)
H = r'1/2{\pm}1/2'
V = {'0': '0', '1': '1', '-1': '-1', '2': '2', '-2': '-2', 'h': H, 'mh': '-' + H, '3h': r'3/2{\pm}1/2',
     'm3h': r'-3/2{\pm}1/2', 'mhh': '-' + H}
def comp(txt, v): return r'\pos{%s} $(%s)$' % (txt, V[v])
PAIRS = [  # id, comp 1, value, comp 2, value, class, white to move (upper, lower), black to move (upper, lower)
  ('P1', 'W d3 / B d4 d5', '0', 'W f2 f4 / B f5', '1', 'L', 'WD', 'WD'),
  ('P9', 'W d2 d3 / B d4 d5', '0', 'W f2 f3 / B f4 f5', '0', 'P', 'DL', 'WD'),
  ('P21', 'W d2 d4 / B d5', '1', 'W f3 / B f4 f5', '0', 'L', 'WW', 'WW'),
  ('P22', 'W d3 / B d4 d5', '0', 'W f2 / B f4 f5', 'mh', 'N', 'WD', 'LL'),
  ('P26', 'W d2 d3 / B d4 d5', '0', 'W f2 f3 / B f5', 'h', 'N', 'WW', 'DL'),
  ('P29', 'W d2 d3 / B d4', '0', 'W f3 / B f4 f5', '0', 'P', 'DL', 'WD'),
  ('P35', 'W d2 / B d4 d5', 'mh', 'W f2 f3 / B f4 f5', '0', 'N', 'WD', 'LL'),
  ('P40', 'W d2 d3 / B d5', 'h', 'W f3 / B f4 f5', '0', 'N', 'WW', 'DL'),
  ('P48', 'W d2 / B d3 d5', '-1', 'W f2 f3 / B f4', '0', 'R', 'DL', 'DL'),
  ('N0', 'W d2 d4 / B d5', '1', 'W f2 / B f3 f5', '-1', 'P', 'DL', 'WD'),
  ('N1', 'W d2 d4 / B d5', '1', 'W f2 f3 / B f5', 'h', 'L', 'WW', 'WW'),
  ('N2', 'W d2 d4 / B d5', '1', 'W f2 / B f4 f5', 'mh', 'N', 'WW', 'DL'),
  ('N3', 'W d2 / B d3 d5', '-1', 'W f2 f3 / B f5', 'h', 'N', 'WL', 'DL'),
  ('N4', 'W d2 / B d3 d5', '-1', 'W f2 / B f4 f5', 'mh', 'R', 'LL', 'LL'),
  ('N5', 'W d2 d3 / B d5', 'h', 'W f2 / B f4 f5', 'mh', 'P', 'DL', 'WD'),
  ('N6', 'W d2 d3 / B d5', 'h', 'W f2 f3 / B f5', 'h', 'L', 'WW', 'WW'),
  ('N7', 'W d2 / B d4 d5', 'mh', 'W f2 / B f4 f5', 'mh', 'R', 'LL', 'LL'),
  ('N8', 'W d2 d4 / B d5', '1', 'W f2 f4 / B f5', '1', 'L', 'WW', 'WW'),
  ('N9', 'W d2 / B d3 d5', '-1', 'W f2 / B f3 f5', '-1', 'R', 'LL', 'LL')]
def side(t):  # first token is the upper bound, second the lower bound, over W > D > L for the mover
    return t[0] if t[0] == t[1] else '[%s,%s]' % (t[1], t[0])
sum_rows = '\n'.join('%s & %s & %s & $\\mathcal{%s}$ & %s & %s\\\\' % (i, comp(a, va), comp(b, vb), c, side(w), side(k))
                     for (i, a, va, b, vb, c, w, k) in PAIRS)
S34 = r"""\subsection{Two Checks of the Sum Model}\label{S-sumchecks}
Both results of this subsection are computed by one program each \lab{C1}; neither is a proof.

\emph{Sum model against the whole board.} We solved every position without a passed pawn that has at most six
pawns on flat boards three to five files wide, counted up to mirror image and colour swap, in the sum model and on the
whole board ($599{,}098$ positions). We compare only the outcome classes. Table~\ref{tab:censusSW} gives, for each
race rule and passed-pawn test, how often they differ, for all positions, for the hereditarily sum-safe (HSS) ones
and for the others. The default setting is the count rule with the e.p.-aware test.

\begin{table}[!htbp]
\centering
\caption{Positions where the outcome class of the sum model differs from that of the whole board, by passed-pawn
test and race rule: number of differing positions / number of positions.}
\label{tab:censusSW}
\footnotesize
\begin{tabular}{@{}llrrr@{}}
\toprule
test & race rule & all & HSS & not HSS\\
\midrule
""" + census_rows + r"""
\bottomrule
\end{tabular}
\end{table}

\emph{Sum model against real kings.} On the cylinder with eight files and six ranks we fixed the anchors
\pos{Pa3 pa4 Kh4 kb3}, put one component on file d and one on file f with file e empty, and solved the sum with real
kings, queen promotions only, en passant on, and play bounded after the first promotion (the solver's cap~1).
For each side to move the solver returns an upper and a lower bound over W $>$ D $>$ L, from White's point of view; a side is
\emph{exact} if the two agree, and \emph{bounded} otherwise, shown as $[$lower,upper$]$. In
Table~\ref{tab:realkingsum} W, D and L are a win, a draw and a loss for White, and the classes
$\mathcal L$, $\mathcal R$, $\mathcal N$, $\mathcal P$ are the model's, read as white to move, black to move: $\mathcal L$ is
W, W; $\mathcal R$ is L, L; $\mathcal N$ is W, L; $\mathcal P$ is L, W. The anchors alone give exactly this
pattern for $\mathcal P$. The nine P pairs have no passed-pawn component and each contains a locked component of
value $0$, so they test the sum only weakly; the ten N pairs have two live non-passer components of nonzero value.
Of the $38$ sides, $19$ are exact and all agree with the model, and the other $19$ are bounds that contain the model's
result. Every sum of class $\mathcal P$ is bounded on both sides. Bounds confirm nothing beyond that
the model is not contradicted, and all $19$ sums share the same anchors, so the king and anchor placement may matter
at the bound level. One run per position, no independent re-run.

\begin{table}[!htbp]
\centering
\caption{Real-king test of $19$ sums on the cylinder with eight files and six ranks. Components with their values,
the model's outcome class of the sum, and the solver's result with white to move and with black to move.}
\label{tab:realkingsum}
\footnotesize
\setlength{\tabcolsep}{4pt}
\begin{tabular}{@{}lllcll@{}}
\toprule
pair & component on d & component on f & model & white to move & black to move\\
\midrule
""" + sum_rows + r"""
\bottomrule
\end{tabular}
\end{table}
"""

# S3 sums -------------------------------------------------------------------------------------------
W('s03',
  r'\section{Sums: The Puzzles and Condition (E)}\label{S-sums}',
  r'\subsection{The Two Principles and the Puzzles}',
  L('05_sums', 8, 14),
  L('05_sums', 18, 41),
  L('05_sums', 62, 84),
  r'\subsection{Condition (E)}',
  L('05_sums', 126, 134),
  r'\subsection{Two Models}',
  L('05_sums', 136, 142),
  S34)

# S4 atlas ------------------------------------------------------------------------------------------
W('s04', r'\section{The Atlas: Details}\label{S-atlas}',
  L('06_atlas', 11, 63))

# S5 small values -----------------------------------------------------------------------------------
W('s05', r'\section{Elkies\textquotesingle{} Small Values: Details}\label{S-targets}',
  L('07_targets', 62, 90))

# S6 *2 -----------------------------------------------------------------------------------------------
W('s06', r'\section{The \texorpdfstring{$\nim{2}$}{*2} Question: Details and Ring Listings}\label{S-star2}',
  r'\subsection{The Textbook Candidate}', L('08_star2', 30, 44),
  r'\subsection{Census and Seven Pawns}', L('08_star2', 53, 58), L('08_star2', 67, 83),
  r'\subsection{Counts, Five Files and Rings}',
  r'This subsection gives in full what Sections~\ref{sec:star2-five} and~\ref{sec:star2-rings} of the main text summarize, with every listed ring, count and check.',
  L('08_star2', 110, 181),
  r'''\subsection{Rings on the M\"obius Strip}
The strip joins the first and last files with the ranks reversed: square $(n,r)$ is beside $(1,9-r)$. Every pawn
has a direction; white pawns start moving up and black pawns down, and a capture across the seam lands on the
mirrored rank and reverses the direction of the capturing pawn. Double step and promotion follow the direction.
A pawn is passed if no enemy pawn is strictly ahead of it, in its own direction, on its file or a neighboring
file, the seam neighbor being read in mirrored ranks; a pawn that can be taken en passant is not passed. The
whole-board game with the count rule is otherwise that of Section~\ref{sec:star2-rings}. A root ring has a pawn
on every file, no passed pawn and all pawns in their starting directions; rotating the strip does not preserve
this, so rings that differ by a rotation are counted separately.

Table~\ref{tab:mobring} gives the least number of pawns in a root ring $\nim{2}$ and one such ring for each $n$,
in ring notation: one entry per file from the first to the last, the seam lying between the last and the first.
All root rings were scanned for $n=3$ with $3$ to $10$ pawns, $n=4$ with $4$ to $9$, $n=5$ and $6$ with $n$ to
$9$, $n=7$ with $7$ and $8$, and $n=8$ with $8$ (two programs by one AI model agree on every ring). A third
program, written independently from the rules alone, agrees on the eight rings named here, on the number of
root rings, and on the number of $\nim{2}$ rings in every scan below the least, and at the least
for $n=3,4,5,8$ \lab{C2}. Two nine-pawn rings are $\nim{3}$: B67 W4 W2B6 W2B5 W5B7 on five files and
B7 W4 W23 B5 W3B7 W4B7 on six \lab{C2}.

\begin{table}[!htbp]
\centering
\caption{Least number of pawns in a root ring $\nim{2}$ on the M\"obius strip and on the cylinder, with a least ring on the strip.}
\label{tab:mobring}
\begin{tabular}{@{}cccl@{}}
\toprule
$n$ & strip & cylinder & a least ring on the strip\\
\midrule
3 & 6 & 6 & W3B6 W2B7 W4B5\\
4 & 8 & 7 & B5 W23 W2B67 W4B7\\
5 & 6 & 8 & B6 W3 B5 W2 W3B7\\
6 & 8 & 9 & B4 W2 W2 W2B6 B5 W3B7\\
7 & 8 & 10 & B6 W2 W3 B6 B7 W3 W6B7\\
8 & 8 & 10 & B7 W3 W3 B6 W3 B6 B6 W2\\
9 & 10 & 10 & B6 W2 W3 B6 B7 W3 B7 W5 W6B7\\
10 & 10 & 10 & B4 W2 B6 W2 W3 B6 B7 W3 B7 W5\\
11 & 11 & 11 & B4 W2 B6 W2 W3 B6 B7 W3 B7 W5 B7\\
\bottomrule
\end{tabular}
\end{table}

\emph{Nine to eleven files.} For $n=9$, $10$ and $11$ we scanned every root ring with $n$ pawns ($2{,}729{,}517$,
$17{,}146{,}529$ and $109{,}358{,}578$ rings) and, for $n=9$, every root ring with ten pawns ($133{,}597{,}405$ rings).
The two programs agree on every ring \lab{C1}. The independently written program agrees on every $\nim{2}$ and
$\nim{3}$ ring found, and its own scan of the nine-pawn rings on nine files also finds no $\nim{2}$ \lab{C2}. So the
least on nine files is ten pawns. Up to symmetry, ten files have two $\nim{2}$ rings with one pawn per file and
eleven files have one. On nine files one ten-pawn ring is $\nim{3}$: B5 W3 W4 B7 B7 W3 W2 W2B7 B7 \lab{C2}. For
$n=9,10,11$ the strip and the cylinder need the same number of pawns.

\emph{Families.} Three families continue these rings; $(X)^m$ stands for $m$ copies of the block $X$.
\begin{itemize}
\item $(\text{B4 W2})^m$ B6 W2 W3 B6 B7 W3 B7 W5 has $n=2m+8$ files and one pawn per file. It is $\nim{2}$ for
  $m=1,\dots,12$, that is $n=10,\dots,32$.
\item $(\text{B4 W2})^m$ B6 W2 W3 B6 B7 W3 B7 W5 B7 has $n=2m+9$ files and one pawn per file. It is $\nim{2}$ for
  $m=1,\dots,11$, that is $n=11,\dots,31$.
\item B6 W2 W3 B6 B7 W3 $(\text{B7 W5})^m$ W6B7 has $n=2m+7$ files and $n+1$ pawns. It is $\nim{2}$ for
  $m=0,\dots,12$, that is $n=7,\dots,31$.
\end{itemize}
All three families are $\nim{2}$ for every $m$ in these ranges without an upper bound: the first two for every
$m\ge1$ and the third for every $m\ge0$ \lab{S} (Section~\ref{S-star3}, Note~5: a full proof written by one AI model and checked line by line by an AI referee from another vendor). The proof is the insertion
argument of the cylinder (Section~\ref{S-ringn}): two wall files are inserted inside a wall of ten files that does not cross the seam,
and the reduced game does not change. Its base case, the reduced game at $m=5$ ($435$, $417$ and $435$ positions),
was computed by two independently written programs \lab{C2}, which also agree on the members with $m\le13$ solved directly. So one pawn per file
gives a $\nim{2}$ ring on the strip for every $n\ge10$. The members with $m=0$ of the first two
families are not $\nim{2}$, and the eight-file ring of Table~\ref{tab:mobring} is not extended by any block
insertion we tried. Since a ring has at least one pawn per file, the least number of pawns in a ring $\nim{2}$ on the
strip is $n$ for every $n\ge10$. A scan of all root rings with twelve pawns on twelve files was stopped after $50$ of
$128$ parts; the only $\nim{2}$ ring in those parts is the member of the first family.

Rings of value $\nim{3}$ with $n+1$ pawns exist on the strip for every $n\ge11$ \lab{S} (Section~\ref{S-star3}, Note~6). They are the cylinder's two families $T_n$ and $S_n$ of Note~4 with the seam at one particular file; other positions of the seam on the same rings do not give $\nim{3}$. The proof is the same insertion argument, and its base cases were computed by two independently written programs \lab{C2}. On ten files we found a $\nim{3}$ ring only with twelve pawns, and eleven pawns are open.

\subsection{Boards of Other Heights}\label{S-heights}
Everything above is on eight ranks. Here the board has $R$ ranks, $5\le R\le12$: white pawns start on rank $2$,
black pawns on rank $R-1$, and the double step is allowed only from there. We solved single-component positions
without a passed pawn in which every file is occupied (rings, on a cylinder), on ordinary boards of three and four
files and cylinders of three to five files, in increasing number of pawns: about $1.8$ billion positions in all.
Table~\ref{tab:heights} gives the least number of pawns in a $\nim{2}$ and in a $\nim{3}$.

\begin{table}[!htbp]
\centering
\caption{Least number of pawns in a position of value $\nim{2}$ / $\nim{3}$ on a board of $R$ ranks. A dash: every
position of the board was solved and none has the value. ${>}p$: none with up to $p$ pawns; more pawns were not
scanned in full.}
\label{tab:heights}
\small
\begin{tabular}{@{}lcccccccc@{}}
\toprule
board & $R=5$ & $6$ & $7$ & $8$ & $9$ & $10$ & $11$ & $12$\\
\midrule
ordinary, 3 files & -- / -- & 8 / -- & 4 / -- & 10 / -- & 7 / 9 & 7 / 9 & 7 / 9 & 6 / 9\\
ordinary, 4 files & -- / -- & 6 / -- & 4 / 6 & 7 / 9 & 6 / 9 & 8 / 9 & 6 / 8 & 6 / 8\\
$\cyl{3}$ & -- / -- & -- / -- & 4 / -- & 6 / -- & 6 / ${>}12$ & 6 / 10 & 6 / 9 & 6 / 9\\
$\cyl{4}$ & -- / -- & 6 / -- & 6 / ${>}16$ & 7 / ${>}11$ & 6 / ${>}9$ & 7 / ${>}8$ & 6 / ${>}8$ & 6 / ${>}7$\\
$\cyl{5}$ & -- / -- & 8 / -- & 6 / 8 & 8 / ${>}9$ & 6 / 9 & 8 / ${>}8$ & 8 / ${>}7$ & ${>}7$ / ${>}7$\\
\bottomrule
\end{tabular}
\end{table}

No position has a nimber above $\nim{3}$ \lab{C1}. The only nimbers are $0$, $\star$, $\nim{2}$ and $\nim{3}$, with
$831$ positions of value $\nim{2}$ and $77$ of value $\nim{3}$. The least counts are not monotone in the height.
On five ranks no position is $\nim{2}$. On six ranks six pawns are enough, as in \pos{W a2 b2 d2 / B a5 c5 d5} on
four files. On seven ranks four pawns are enough, \pos{W a2 c2 / B c3 b6} on three files, and six pawns make a
$\nim{3}$, \pos{W a2 c2 d3 / B c3 b6 c6} on four files. On the cylinder of three files and nine ranks the position
with all six pawns at home, \pos{W a2 b2 c2 / B a8 b8 c8}, is $\nim{2}$. The column $R=8$ agrees with the counts of
Sections~S6.2 and~S6.3.

The solver was written for this scan. It agrees with our CGT engine on $16{,}000$ random positions, $2{,}000$ for
each height, and on each of the $48$ positions behind a least count in the table \lab{C2}. A third program,
written independently from the rules alone, repeated the complete scans for five ranks, for six ranks and for three
files on seven ranks: $2{,}381{,}595$ positions, with the same number of positions of each nimber and the same least
counts, and no nimber above $\nim{3}$ \lab{C2}. It also showed that the first solver counts $280$ impossible
positions on $\cyl{5}$ with six ranks (twenty pawns, one or two of them white); this changes no entry of the table.
For the other heights, that no smaller position exists and that no $\nim{4}$ occurs rests on the one solver
\lab{C1}. Positions with an empty file, wider boards and more pawns than the table states were not scanned.
''')

# S7 real chess ---------------------------------------------------------------------------------------
W('s07', r'\section{From the Model to Real Chess: Details}\label{S-real}', L('09_real', 29, 74))

# S8 tablebases ---------------------------------------------------------------------------------------
W('s08', r'\section{Tablebases: Rules and King and Pawn Against King}\label{S-tb}',
  L('10_tablebases', 3, 18), L('10_tablebases', 47, 69), r'\subsection{King and Pawn Against King}', L('10_tablebases', 72, 148))

# S9 Dawson ---------------------------------------------------------------------------------------------
W('s09', r'\section{Dawson\textquotesingle{}s Chess: Details and Learning}\label{S-dawson}',
  L('11_dawson', 7, 24), L('11_dawson', 35, 66), L('11_dawson', 84, 92),
  r'\subsection{Learning Dawson\textquotesingle{}s Chess}', L('12_engines', 75, 78))

# S10 open problems -------------------------------------------------------------------------------------
W('s10', r'\section{Further Open Problems}\label{S-open}',
  r'The main text lists four open problems; this is the full list of six.', L('14_conclusion', 7, 25))

# S11 FEN ---------------------------------------------------------------------------------------------
W('s11', r'\section{Positions with Kings in FEN}\label{S-fen}',
  L('appendix_positions', 1, 7).replace(r'\label{app:positions}', ''),
  L('appendix_table', 3, 55).replace(r'{0.29\textwidth}', r'{0.27\textwidth}'))

# S12 kings and sums theory -----------------------------------------------------------------------------
W('s12', r'\section{Full Proofs: Validity of the Convention, Sums, Certificates and Loopy Games}\label{S-kingsproof}',
  scrub(open('supp_src/s12a_core.tex', encoding='utf-8').read().replace(
      r'\subsection*{The Four Main Results, Self-Contained}',
      r'\subsection{The Four Main Results, Self-Contained}\label{S-core}')),
  r'\subsection{The Longer Treatment}\label{S-kingslong}',
  NOTE % (r'kings/theory/LOOPY.md, Sections 1--3 (the theory note on frozen king groups)',
          r'Theorem~\ref{thm:validity} (validity) and Corollary~\ref{cor:v4} are Theorem~1.14 there, (V4) being part (ii); '
          r'Theorem~\ref{thm:hss} (sum safety) rests on Theorem~1.11 and Theorem~1.14(ii); the certificate theorem of '
          r'Section~\ref{S-kings} is Theorem~2.7; the horizon-1 proposition is Proposition~2.10(a); the theorem on '
          r'outcomes with spare moves is Theorem~3.4.'),
  MD('kings/theory/LOOPY.md', 225, 2213, cur='s12_kings.md'))

# S13 wall rings n+3 ------------------------------------------------------------------------------------
pt = open(R + 'research/ring_family_proof/proof.tex').read()
body = pt[pt.index('\n\\begin{wallproof}') + len('\n\\begin{wallproof}'):pt.index('\n\\end{wallproof}')]
body = body.replace(r'\subsection*', r'\subsection')
# proof.tex numbers its own theorem and lemmas (Lemma 1-3, cited by S14 and S15); keep that numbering
for env in ('theorem', 'lemma'):
    body = body.replace(r'\begin{%s}' % env, r'\begin{w%s}' % env).replace(r'\end{%s}' % env, r'\end{w%s}' % env)
W('s13', r'\section{Full Proof: Wall Rings of Value \texorpdfstring{$\nim{2}$}{*2} with \texorpdfstring{$n+3$}{n+3} Pawns}\label{S-wall}',
  r'\noindent\emph{Source.} research/ring\_family\_proof/proof.tex, typeset unchanged. It proves the $n+3$-pawn ring '
  r'$\nim{2}$ on every $\cyl{n}$, $n\ge5$, of Section~\ref{sec:star2-rings}, and its Lemmas 1--3 are used in '
  r'Sections~\ref{S-ringn}--\ref{S-star3}.' + '\n\n' + body + '\n\n'
  + pt[pt.index(r'\paragraph{The five poisoned wall moves'):pt.index(r'\paragraph{Remarks.}')])

# S14 n-pawn *2 -----------------------------------------------------------------------------------------
W('s14', r'\section{Full Proof: Rings of Value \texorpdfstring{$\nim{2}$}{*2} with One Pawn per File}\label{S-ringn}',
  NOTE % ('research/ring\\_n\\_proof/PROOF\\_N.md', r'its theorem is the statement of Section~\ref{sec:star2-rings} that the '
          r'two families with $n$ pawns are $\nim{2}$ as whole-board games for every $n\ge10$; $M_{10}$ is the ring of Fig.~\ref{fig:ring}.'),
  MD('research/ring_n_proof/PROOF_N.md', cur='s14_ringn.md'))

# S15 *3 families ---------------------------------------------------------------------------------------
W('s15', r'\section{Full Proofs: The Lemma 3 Write-Up, the \texorpdfstring{$\nim{3}$}{*3} Families and the M\"obius Strip}\label{S-star3}',
  r'This section holds six notes. The first writes out Lemma~3 of Section~\ref{S-wall} (its Section 2b), which the '
  r'other proofs cite, and proves a further $\nim{2}$ family with $n+2$ pawns. The second and third prove the whole-board '
  r'$\nim{3}$ with $n+2$ pawns for even $n\ge8$ and odd $n\ge11$; the fourth proves the $\nim{3}$ with $n+1$ pawns for '
  r'every $n\ge12$ (Section~\ref{sec:star2-rings}); the fifth carries the insertion argument over to the M\"obius strip (Section~\ref{S-star2}); the sixth proves the $\nim{3}$ with $n+1$ pawns on the M\"obius strip for every $n\ge11$. Each is typeset without changes to its mathematics.',
  r'\subsection{Note 1: research/ring\_n\_plus\_2\_proof/PROOF.md}', MD('research/ring_n_plus_2_proof/PROOF.md', cur='s15_note1.md'),
  r'\subsection{Note 2: research/ring\_n\_plus\_2\_proof/PROOF\_Q.md (even $n$)}', MD('research/ring_n_plus_2_proof/PROOF_Q.md', cur='s15_note2.md'),
  r'\subsection{Note 3: research/ring\_n\_plus\_2\_proof/PROOF\_odd.md (odd $n$)}', MD('research/ring_n_plus_2_proof/PROOF_odd.md', cur='s15_note3.md'),
  r'\subsection{Note 4: research/star3\_proof/PROOF\_S3T3.md}', MD('research/star3_proof/PROOF_S3T3.md', cur='s15_note4.md'),
  r'\subsection{Note 5: research/mobius\_rings\_proof/PROOF.md (M\"obius strip)}', MD('research/mobius_rings_proof/PROOF.md', cur='s15_note5.md'),
  r'\subsection{Note 6: research/mobius\_star3\_family/PROOF.md (M\"obius strip, $\nim{3}$ with $n+1$ pawns)}', MD('research/mobius_star3_family/PROOF.md', cur='s15_note6.md'))

# S16 square rule ---------------------------------------------------------------------------------------
W('s16', r'\section{The Square-Rule Passer Test: Definition, Checks and a Counterexample}\label{S-square}',
  MD('research/v2_mechanisms_proof/PROOF_S.md', cur='s16_square.md'),
  # S17 who wrote and who checked: kept in the S16 file because supplement.tex inputs only supp/s01 .. supp/s16
  scrub(open('supp_src/s17_provenance.tex', encoding='utf-8').read()))
aux = open('build/tog_review.aux').read()
open('supp/mainlabels.tex', 'w').write('\n'.join(l for l in aux.split('\n') if l.startswith('\\newlabel{')) + '\n')
print('ok')
