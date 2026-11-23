# K50: a checker that certifies the frozen-king model for an 8×8 position

The paper's engine-on-sums test was withdrawn: 163 of its 200 positions put the king group on a file with component
pawns (`research/engine_baselines/REPORT.md`, "Embedding flaw"). To rebuild the test set, the paper side needs a program
that takes an ordinary 8×8 K+P position (a trébuchet-type king group plus pawn components; FEN in) and says whether the
frozen-king model is certified for it.

Read LOOPY §1.5 ((V1)–(V4) and why each is needed), Definition 2.1, Lemma 2.2, Theorem 1.14 with its sharp form,
Theorem 2.7 with (L1)–(L3) and the certificate LC_T, Proposition 2.11 and Corollary 2.11a ((H1)–(H5)), Proposition 2.10,
and K29 (which groups act as 0 beside small contexts).

1. Write `kings/embed_check.py` (pure Python, standard library; flat 8×8 by default, `--board cyl:8x8` optional):
   FEN in, JSON out. It must:
   - find the king group Z (both kings, the pawns on their files), F_Z, the buffer files and the context;
   - check separation (Definition 2.1): buffer pawn-free, context at distance ≥ 2, no officer, nobody in check;
   - check each of (V1), (V2), (V3) by the sufficient conditions LOOPY proves (Lemma 2.2 and the e.p. condition for
     (V1); Corollary 2.11a's (H1)–(H5) for (V2); the certificate of Theorem 2.7 with (L1)–(L3) for (V3)), and report
     per clause CERTIFIED, FAILS (with the witness move or pawn) or UNDECIDED (the sufficient condition does not apply);
   - say what the certificate proves: the result in the promotion game P, and chess only with (A_Q) at the root;
   - report how many files remain for the pawn components.
   Never report CERTIFIED for something LOOPY does not prove; UNDECIDED is the honest default.
2. Tests: (a) every position of the 23 separated and a sample of the 163 mixed ChessSums positions
   (`engine/runs/chesssums/`, `research/engine_baselines/`): the mixed ones must fail separation; (b) on 6-rank boards
   small enough to solve, compare the verdict with kp_p --pmodel / `kpsolve --frozen`: no CERTIFIED position may
   disagree with the solver; report the count of CERTIFIED, FAILS, UNDECIDED.
3. For eight files, tabulate for each known group (the two trébuchets of the paper's Fig. (a), (b); Z_T; K29's four
   classes where they fit) how many context files remain and which context sizes are covered by a proof or by K29.
4. Output: the program, `kings/delegate/out/K50/findings.txt` with usage and the test results, and a short usage note the
   paper side can follow. No heavy runs (each test under a CPU-minute, under 1 GB).
