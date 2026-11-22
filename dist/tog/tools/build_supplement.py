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
  L('05_sums', 136, 142))

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
  L('08_star2', 110, 181))

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
  r'Sections~\ref{S-ringn}--\ref{S-star3}.' + '\n\n' + body)

# S14 n-pawn *2 -----------------------------------------------------------------------------------------
W('s14', r'\section{Full Proof: Rings of Value \texorpdfstring{$\nim{2}$}{*2} with One Pawn per File}\label{S-ringn}',
  NOTE % ('research/ring\\_n\\_proof/PROOF\\_N.md', r'its theorem is the statement of Section~\ref{sec:star2-rings} that the '
          r'two families with $n$ pawns are $\nim{2}$ as whole-board games for every $n\ge10$; $M_{10}$ is the ring of Fig.~\ref{fig:ring}.'),
  MD('research/ring_n_proof/PROOF_N.md', cur='s14_ringn.md'))

# S15 *3 families ---------------------------------------------------------------------------------------
W('s15', r'\section{Full Proofs: The Lemma 3 Write-Up and the \texorpdfstring{$\nim{3}$}{*3} Families}\label{S-star3}',
  r'This section holds four notes. The first writes out Lemma~3 of Section~\ref{S-wall} (its Section 2b), which the '
  r'other proofs cite, and proves a further $\nim{2}$ family with $n+2$ pawns. The second and third prove the whole-board '
  r'$\nim{3}$ with $n+2$ pawns for even $n\ge8$ and odd $n\ge11$; the fourth proves the $\nim{3}$ with $n+1$ pawns for '
  r'every $n\ge12$ (Section~\ref{sec:star2-rings}). Each is typeset without changes to its mathematics.',
  r'\subsection{Note 1: research/ring\_n\_plus\_2\_proof/PROOF.md}', MD('research/ring_n_plus_2_proof/PROOF.md', cur='s15_note1.md'),
  r'\subsection{Note 2: research/ring\_n\_plus\_2\_proof/PROOF\_Q.md (even $n$)}', MD('research/ring_n_plus_2_proof/PROOF_Q.md', cur='s15_note2.md'),
  r'\subsection{Note 3: research/ring\_n\_plus\_2\_proof/PROOF\_odd.md (odd $n$)}', MD('research/ring_n_plus_2_proof/PROOF_odd.md', cur='s15_note3.md'),
  r'\subsection{Note 4: research/star3\_proof/PROOF\_S3T3.md}', MD('research/star3_proof/PROOF_S3T3.md', cur='s15_note4.md'))

# S16 square rule ---------------------------------------------------------------------------------------
W('s16', r'\section{Full Proof: The Square-Rule Passer Test}\label{S-square}',
  NOTE % ('research/v2\\_mechanisms\\_proof/PROOF\\_S.md', r'it proves, for the frozen-king pawn game, the square-rule passer '
          r'test behind the repair in Section~\ref{sec:kings-sweep}.'),
  MD('research/v2_mechanisms_proof/PROOF_S.md', cur='s16_square.md'))
aux = open('build/tog_review.aux').read()
open('supp/mainlabels.tex', 'w').write('\n'.join(l for l in aux.split('\n') if l.startswith('\\newlabel{')) + '\n')
print('ok')
