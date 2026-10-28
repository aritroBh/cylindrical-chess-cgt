# K17 referee report (round 2): is (V1a) needed?

Verdict: ACCEPT_WITH_FIXES. The main claim (the clause "no checks" of (V1a) is needed, by `Ka2 kb4 Pa3 pa4 Pd2 pe3 b -` on cyl:6x6) is
confirmed by an independent solver and my own code. Every count in summary.json and EDITS.md that I re-ran reproduced exactly. The fixes are
labels, one overcounted figure, one stale sentence left in LOOPY, and one wording slip in a proof. No claim was refuted.

Reused from the earlier (stopped) referee: nothing for any number. I looked at its `verify/r66.hits.json`, `verify/r66.in` and
`verify/ecl_f86_*.out` only as a cross-check list, after producing my own. Everything below was produced by code in `verify/mine/`
(`myd.py` = my own pawn game D, written from LOOPY Def. 1.5 and lemmas L1.6, no import of cylcgt, lemmas, K17 or the first referee's code;
`gen_real.py`, `gen_frozen.py`, `mytwin.py`, `myecl.py`, `myenr.py`). Solvers: ref3m (K23's, written from SPEC.md only) for P and for
`--frozen`; kpsolve and kp_p only to compare. The earlier referee's `twincheck.py` was still running as an orphan at 12 GB RSS when I
started; it was gone before I finished (I did not touch it).

## 1. The headline counterexample (CHECKED-2, in fact three solvers)

`printf 'Ka2 kb4 Pa3 pa4 Pd2 pe3 b -\nKa2 kb5 Pa3 pa4 Pd2 pe3 b -\nKa2 kb5 Pa3 pa4 Pd2 pe3 w -\n' | ref3m --board cyl:6x6 --moves`
(ref3m built with `c++ -O2 -std=c++17 -o ref3m kings/delegate/out/K23/verify/ref3m.cpp`; kp_p `--pmodel --moves` gives the same).
- X (Black to move, in check from Pa3): W; Black's legal moves are exactly Kb5, Kc5, Kc4, Ka5 (Kb3, Kxa3 hit Ka2; Kc3 hits Pd2; Ka4 own pawn),
  all four W. So V1b, V3 hold at X, and X is the only chess-reachable position, so V2 holds (all four decisive events are P-wins for White).
- Twin kb5: Black to move L (Black wins), White to move W. My own checker (`mytwin.py`, own D, own reachable set, own V1a/V1b/V2/V3/V4 test
  on ref3m's move lists) reports the twin clean: legal both sides, V1a-V4 at every reachable position, P = D for both sides.
- My own D (`myd.py`): D(White to move) = White, D(Black to move) = Black, i.e. outcome N; `cylcgt` o(S) = N as well. So P(X) = W != D(X) = Black.
- Frozen: ref3m `--frozen` and `kp --frozen` both give `Ka1 kb4 ...` W, twin kb5 L (b) / W (w).
- Deeper example `Kb6 kb3 Pa2 pa3 Pd2 Pe3 pe5 b -`: ref3m X = W; twin kb2: L (b), W (w); my checker: clean; reachable positions 4 (Black to move) and 6 (White to move); D = N in my D and in cylcgt.
  This is CHECKED-2, not "COMPUTED-1 (kpsolve only)" as EDITS.md says.
- The hand reading of the point is right: a Z-pawn check leaves the mover only Z-moves, which V3 makes losing, while D (Z deleted) lets the mover play e3-e2 or exd2 at once.
  Whether X is retrograde-legal (the last White move must have been Pb2xa3 capturing something) was not examined; Theorem 1.14 speaks of "a K+P chess position", and all solvers treat X as legal.

## 2. Counts (all reproduced with my own generator, own D, ref3m)

| claim (EDITS.md / summary.json) | mine |
|---|---|
| real kings, check at root, cyl:6x6 files d,e, <= 2+2: 781 hits | 214 contexts, 141 with D(B first)=Black, 2538 queries, **781** hits; the hit set equals the first referee's list |
| cyl:5x6 file d, <= 3+3: 0 hits | 18 contexts, 6 candidates, **0** |
| flat:6x6 files d,e,f <= 2+2: 3780 | 716 / 514 / 9252 queries, **3780** |
| cyl:7x6 files d,e,f <= 2+2: 3657 | **3657** |
| clean twin (V1-V4 all, P = D both sides, twin kb(r+2) or kb(r)): 257, 1362, 1210 | **257, 1362, 1210**; all hits are HSS-true |
| frozen X: 514/514 flat6x6 and cyl7x6, 411/411 cyl6x6 (d,e, <=3+3), 6/6 cyl5x6; twin-clean 366, 366, 327 | candidates 514, 514, 411, 6 (every X is P = W in ref3m --frozen); clean twins **366, 366, 327, 6** |
| flat:8x6 files c,d,f,g, fresh right, <=3+3: 856 roots, 768 multi, 0 diffs | **856, 768, 0** |
| <=4+4: 97,676 contexts, 10,400 roots, 2,560 HSS multi, 16 diffs, none HSS | **97,676; 10,400; 10,304 multi; 2,656 HSS, 2,560 HSS multi; 16 diffs, 0 HSS** |
| <=5+5: 313,476 contexts, 39,696 roots, 39,600 multi, 48 diffs, none HSS | **313,476; 39,696; 39,600; 48 diffs; 0 HSS** (5,584 HSS roots) |
| o(S) = D_whole on every HSS root | `cylcgt` value vs my D_whole: **0 differences on all 5,584 HSS roots** of the <=5+5 run (so also on the 2,560 of the <=4+4 run) |
| kp --frozen on the 48 diffs: P = D_whole in 32, = D_fix in 16 | ref3m --frozen: **32 and 16** (and 16/0 on the <=4+4 diffs) |
| flat:6x6 files c..f <=3+3, fresh right: 3036 roots, 192 multi, 0 diffs | **3036, 192, 0** |
| flat:6x6 files c..f <=3+3, no right at root: 1,128 (E)-violating roots, 0 diffs | 20,102 contexts; **1,128 only with a loose test** (any later capture of a just-double-stepped pawn counts, the K17 `usable_ep`); with a genuine e.p. capture **752**; D_fix = D_whole at all of them in both readings |

Search boundaries (stated, not hidden): contexts on ranks 2..H-1 only, <= 2/3/4/5 pawns per side, at most 3 context files (4 for the E search), Z = one locked
pair Pa(r)/pa(r+1) with the Black king on b(r+1) and the White king on a/b, the E search on flat:8x6 with a gap file and the right in the root only;
cyl:7x6 B2 and flat:6x6 <=4+4 (no-right roots) were not completed. I found no hidden cut-off beyond these. Negative result on (E): in this boundary there is no
root with (V4) true where the sum reading (D_fix or o(S)) differs from the chess reading, and no isolated (E) counterexample.

## 3. Proposition 1.15 (a): proof checked against Definitions 2.1 and Lemma 2.2

Sound. With no sliders, only pawns and the enemy king attack; kings never touch; context pawns attack buffer and context squares only; a context move
cannot capture or block a pawn check on F_Z; Z-pawns capture only onto buffer files, which are empty. So the non-Z legal moves are all context moves if the mover is
not in check at Y and none otherwise, and the check status is fixed by X. Slips (fix with A3 in `verify/EDITS_referee.md`):
- "two files from every context pawn's captures" is wrong as written (the capture squares are at distance >= 1 from F_Z, not 2); the argument is unaffected.
- "(V1a) fails at X iff ..." should read "at some Y": V1a is a hypothesis over every reachable Y.
- the figure 1,128 (see table).

## 4. EDIT blocks

All five OLD texts occur exactly once in the current LOOPY.md (`verify/mine/chk.py`; LOOPY.md was re-read today). The NEW texts are accurate except:
- **Labels.** "PROVED" appears in the status row and the table row for a statement whose only evidence is a solver run. By LOOPY's own scheme that is CHECKED-2 (now three
  solvers). Change to CHECKED-2 (A1, A2). Prop 1.15 (a) is a hand proof and may stay PROVED.
- **Stale sentence left behind.** LOOPY.md line 660 (sharp form, "(S1)") says no isolated counterexample is known "as for (V1a)". The same X is one: σ = Black (the D-winner)
  is in check, its only legal moves are Z-moves, so (S1) fails and P(X) = W. EDITS.md does not touch it. Proposed edit B1 in `verify/EDITS_referee.md`.
- The deeper example is CHECKED-2 (see section 1), not COMPUTED-1.

## 5. Labels

- (V1a) clause "no checks" is needed: CHECKED-2 (ref3m, kp_p, refp agree on X, twin; own D). Not PROVED.
- The statistics: COMPUTED-1 as counts, but reproduced here by separate code (own generator, D, V-checker, ref3m), so they are CHECKED-2 as counts.
- Prop 1.15 (a): PROVED (hand), minus the wording slips. (b): bounded negative result, CONJECTURE for "(E) not needed under (V4)" is the right label.
- "(S1) is needed": no longer a bare CONJECTURE (B1).

Files: `verify/mine/` (scripts and small json), `verify/EDITS_referee.md`. Binaries and batch files deleted. No git, no installs, no pattern kills; no run exceeded about 1 CPU-minute, so the
heavy lock was not used (both slots were taken by other jobs); peak RSS of my runs 170 MB (ref3m cyl:7x6).
