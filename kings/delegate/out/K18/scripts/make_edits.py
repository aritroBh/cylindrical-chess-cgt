#!/usr/bin/env python3
"""build EDITS.md from the current tables (run from the K18 directory)."""
import json, collections, re, os
LOOPY = "/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md"
text = open(LOOPY).read()
# ---- exact OLD blocks
i0 = text.index("   - The question is untested. Every trébuchet placement checked on the 7×6 cylinder satisfied (L1) for every")
i1 = text.index("2. Do both-sides-shuttle (dud) groups exist without a pawn break")
old1 = text[i0:i1].rstrip("\n")
j0 = text.index("- **K24 re-computation (2026-10-27; scripts and logs in `kings/delegate/out/K24/`")
j1 = text.index("\n---\n\n## References")
old2 = text[j0:j1].rstrip("\n")
assert text.count(old1) == 1 and text.count(old2) == 1
# ---- numbers
def tab(d):
    try: return json.load(open(f"logs/{d}/table.json"))
    except OSError: return []
def matched(t):
    c = collections.Counter()
    for r in t:
        if r["cls"] in ("zero", "neg") and r["A"] != "X":
            c[("pf" if r["promfree"] else "race", "ok" if r["A"] == "L" else "fail")] += 1
    return c
ES, ES7, E3, EP = matched(tab("ES")), matched(tab("ES7")), matched(tab("E3")), matched(tab("EP"))
race_ok = ES[("race", "ok")] + ES7[("race", "ok")] + E3[("race", "ok")]; race_fail = ES[("race", "fail")] + ES7[("race", "fail")] + E3[("race", "fail")]
pf_ok = EP[("pf", "ok")] + E3[("pf", "ok")]; pf_fail = EP[("pf", "fail")] + E3[("pf", "fail")] + ES[("pf", "fail")] + ES7[("pf", "fail")]
nE3 = len({r["s"] for r in tab("E3")}); nE3rows = len(tab("E3"))
# E1 modules
sel = json.load(open("logs/sorties_k_selected.json")); ctxm = json.load(open("logs/ctxmod_contexts.json"))
AB = {"W1(e)+B1(g) zero": (1, 1), "B1(e)+W1(g) zero": (1, 1), "W1(e)": (1, 0), "W1(g)": (1, 0), "B1(e)": (0, 1), "B1(g)": (0, 1), "W1(e)+W1(g)": (2, 0), "B1(e)+B1(g)": (0, 2)}
e1 = collections.Counter(); nE1 = 0
for i, s in enumerate(sel):
    rout = None
    for d in ("logs/E1", "logs/E1b"):
        try: r_ = [l.rstrip() for l in open(f"{d}/out_{i}.txt") if " | " in l]
        except OSError: continue
        if len(r_) == 16: rout = r_; break
    if rout is None: continue
    nE1 += 1
    for j, c in enumerate(ctxm):
        a = rout[2 * j].split(" | ")[1].split(); A = a[0] if a[0] == a[1] else a[0] + a[1]
        if A == "X": continue
        na, nb = AB[c["name"]]; d = na - nb; got = A == "L"
        pred = True if d <= 0 else (s["kvecP"][d] is not None)
        e1[("d<=0" if d <= 0 else "d>0", "pred ok" if pred else "pred not", "punished" if got else "not punished")] += 1
m0 = e1[("d<=0", "pred ok", "punished")]; m0f = e1[("d<=0", "pred ok", "not punished")]
p_ok = e1[("d>0", "pred ok", "punished")]; p_okf = e1[("d>0", "pred ok", "not punished")]
q_n = e1[("d>0", "pred not", "not punished")]; q_p = e1[("d>0", "pred not", "punished")]
S = json.load(open("summary.json")) if os.path.exists("summary.json") else {}
P4 = json.load(open("logs/p4_check.json")); p4tot = f"{P4['ES']['matched_legal'] + P4['EP']['matched_legal'] + P4['E3']['matched_legal']:,}"
new1 = f"""   - **K18 tested the question (2026-10-27; scripts, logs and `summary.json` in `kings/delegate/out/K18/`).** Model P (first
     promotion wins, real kings), `cyl:7×6` and `cyl:8×6`, F_Z = {{a, b, c}}, s = White (Black sorties are colour-flipped), unless
     stated. *Plain* is the local game of Definition 2.6 with no passes for s (a stalemate of s is then a failure for s̄);
     *pass* is Definition 2.6 as it stands (k = ∞); *budget k* gives s at most k passes. A *plain-only sortie* is a White move m at
     a root Y such that some admissible reply r wins the plain game and no admissible reply wins the pass game. An *outright
     escape* is a White move at Y that neither game punishes and that no immediate promotion by s̄ punishes. Result: the question
     can be tested; the conjecture is **false as stated** (explicit counterexamples below, COMPUTED-1); a promotion-free form is
     supported by every test (no counterexample) and is **PROVED** under the extra hypotheses of Proposition 8.1.
     - **Groups with a plain-only sortie and no outright escape exist in large numbers (COMPUTED-1; CHECKED-2 for the local
       values).** Solver: `scripts/lg.cpp` (dense retrograde tables over all pawn configurations with ≤ 2 + 2 or ≤ 3 + 2 pawns
       on F_Z at ranks 2 to H − 1, all king placements, e.p. rights carried exactly; budgets k = 0, …, 6 and ∞; the queen clause
       as a switch), written from Definition 2.6 and `kings/SPEC.md`. Second implementation, written separately:
       `scripts/lg2.py` (explicit reachable graph and fixed point) and `scripts/lg2k.py` (budgets). Both give the (L1) list
       T = 6, 6, 6, 7, 7 and the (L1_P) list 6, 6, 5, 6, 6 of §5.1 after Kxa4, and the facts of §5.5 (mirrored to a White
       sortie: Kd3 and Kd2 are plain-only with T = 6, Kd4 is won in both games with T = 5, Kc2 in neither). They agree on
       140 random positions (80 on `cyl:8×6`, 60 on `cyl:7×6`, 40 of them with an e.p. right, 42 with a finite value; 0
       mismatches). The budget values k = 1, …, 6 come from `lg.cpp` alone (COMPUTED-1): the cross-check with `lg2k.py` had finished 1 of 60 values (no mismatch) when it was cut off by the machine load. The search lists, for every root Y with both kings on F_Z, White to move, no passer by the root rule of
       Appendix A and no immediate promotion for White, every White move and the least T over the admissible replies in each
       game. Mirror classes of roots with at least one plain-only sortie and no outright escape (queen clause; without it):
       `cyl:8×6`, 3 files, ≤ 2 + 2 pawns: 941 (1257); `cyl:7×6` the same, 941 (1257); `cyl:8×6`, 4 files: 6602 (6864);
       `cyl:7×6`, 4 files: 6598 (6860); 3 files, ≤ 3 + 2 pawns: 1075 and 1075 (1391 and 1390); `flat:6×6`, 3 files: 960
       (1056). On `cyl:8×6` with 3 files and the queen clause the 941 groups have 1372 plain-only king sorties (and 492
       plain-only pawn sorties); 19 of the groups have one pawn a side. So Z_on's escape Kc5 was not essential: the
       question has non-degenerate test cases. Reproduce: `bin/lg --board cyl:8x6 --fz 0:3 --maxw 2 --maxb 2 --kmax 6 --search`
       (`c++ -O2 -std=c++17 -o bin/lg scripts/lg.cpp`), then `scripts/parse_search.py`.
     - **The local game is a lower bound of the real one (CHECKED-2: the local solver and the full-board P solver agree).** For
       the 232,343 distinct positions after a White move at those roots (`cyl:8×6`, 3 files, ≤ 2 + 2): whenever the plain
       local game is won, `kpsolve --pmodel` (K7's `kp_p.c`) says Black wins P: 108,710 of 108,710 (queen-clause version
       100,625 of 100,625); for the pass game 95,658 of 95,666, the 8 exceptions being draws by stalemate of White (the
       pass game cannot stalemate s). All 4,593 punished White moves of the 941 groups (1,864 plain-only, 2,726 punished in both
       games, 3 only with passes: two of them also Black wins in P, one drawn) are Black wins in bare P except that one
       stalemate draw. Reproduce: `scripts/bare_noesc.py`, `scripts/cmp_bare.py`.
     - **Most plain-only sorties are not tempo-sensitive (COMPUTED-1).** The failure at k = ∞ only says that s can pass forever.
       Of the 1372 plain-only king sorties, 953 are won for every budget k ≤ 6, usually with T_k = T_0 + k (s̄ absorbs each pass
       with one extra move); 327 are won only for k = 0; 61 are won for a prefix k ≤ 1, …, 4; 27 have a parity pattern (won for even k
       only, 15, or for k = 0 and odd k, 12); 4 are other. A real context gives s only finitely many spare moves, so a sortie of the
       first kind stays punished beside any finite context, at a longer time T_k (the point of (L2) with T_k, and of
       Proposition 8.1 below); the genuinely tempo-sensitive cases are the other 419 (1372 − 953).
     - **Context experiments (COMPUTED-1, `scripts/ctx_exp2.py`, `kpp --pmodel --cap 0`).** Contexts G: pawns of both colours on
       the context files e, f, g (`cyl:8×6`: all {4160} with at most 2 + 2 pawns and a legal pawn move for each side) or e, f
       (`cyl:7×6`: 716). The class of G is its `kpsolve --frozen` value with the kings on a1 and c6, (White to move, Black to move):
       zero = (L, W), negative = (L, L), positive = (W, W), fuzzy = (W, L). "Second-player win for the punisher" means zero or
       negative. Tempo matching predicts that Y·m + G, Black to move, is a Black win for these classes. A sortie is *illegal*
       beside G if a context pawn attacks its square (such cases are not counted). Tested: (ES) the 25 plain-only king sorties of
       the 19 groups with one pawn a side against 125 contexts (all 123 with one pawn a side, and the two zero contexts with 1 + 2
       and 2 + 1 pawns); (ES7) the same on `cyl:7×6` (25 sorties, 59 contexts); (E3) {nE3} of 12 planned sorties of the stratified sample (the other six were not finished), 2 + 2 and
       1 + 2 groups, with k* from 0 to 6, against 159 contexts (all 59 zero, 60 negative, 20 positive, 20 fuzzy of the
       `cyl:8×6` family). Reproduce: `scripts/contexts.py cyl:8x6 4,5,6 2 2 logs/ctx8x6_efg_22`, `bin/kp --board cyl:8x6 --frozen --ep on
       --promote Q --cap 0 < logs/ctx8x6_efg_22_frozen_in.txt`, `scripts/select_k.py`, `scripts/ctx_exp2.py make cyl:8x6 <contexts>
       <sorties.json> <dir>`, `bin/kpp --board cyl:8x6 --ep on --pmodel --promote Q --cap 0 < <dir>/in_i.txt`, `scripts/ctx_exp2.py collect …`,
       `scripts/analyze_E.py <dir> <sorties.json>`.
       - **Counterexamples to the unrestricted conjecture (COMPUTED-1, exact: both bounds agree).** In {race_fail} of the {race_ok + race_fail}
         legal zero or negative contexts of these three runs the sortie is not punished; in the others it is. The smallest:
         Y = `Ka1 Pa2 kc1 pa3`, m = Ka1–h1 (plain-only, T = 4), context G = `Pe2 Pg2 pf4` (frozen value zero). `Ka1 kc6 Pe2 Pg2 pf4
         w -` is a Black win and `… b -` a White win in `--frozen`, but `Kh1 Pa2 kc1 pa3 Pe2 Pg2 pf4 b -` is a White win in P (exact; all
         six Black moves lose), and `Ka1 Pa2 kc1 pa3 Pe2 Pg2 pf4 w -` is a White win in P, so beside this zero the group is not 0. The same for the
         negative context `Pe2 pg3` (a race). Reproduce: `bin/kpp --board cyl:8x6 --ep on --pmodel --promote Q --cap 0 --moves
         < logs/cx_small.txt` (5.5 s; output in `logs/cx_small_out.txt`). **Chess** (`kpsolve --cap 1 --promote Q`, exact
         bounds A ≥ value ≥ B from White's side; `bin/kp --board cyl:8x6 --ep on --promote Q --cap 1 < logs/C2_in.txt`, 586 s): for
         29 non-punished sorties of ES the lower bound B is D or W in 20, so Black cannot win chess either (this includes the two
         examples above); in 3 Black wins chess exactly (P and chess differ); 6 are undecided (bounds W or D against L). The 12
         controls (punished in P): 11 Black wins in chess exactly, 1 undecided. In all {race_fail} failures the sortie king stands within 2 steps of a
         context pawn after m, while T ≥ 4, so it can capture the pawn that makes G a second-player win (CONJECTURE for the
         mechanism; not traced move by move). None of the {race_fail} contexts is promotion-free.
       - **Promotion-free matched contexts: no counterexample (COMPUTED-1).** G is *promotion-free* if no sequence of legal pawn moves of
         the context alone (both colours, any order) promotes. Of the 4160 contexts only 5 zero and 45 fuzzy ones are promotion-free
         (shared one-move gaps such as `Pe2 Pg2 pe4 pg4`, whose value is * + * = 0); no negative or positive one is. All {pf_ok} legal
         cases with these shared-gap contexts are punished (25 sorties of the one-pawn groups against the 5 zero contexts, 123
         legal; the 5 contexts against the {nE3} E3 sorties, {E3[('pf','ok')]} legal), and so are {m0} cases with the reservoir contexts described next in
         which s has no more spare moves than s̄: {pf_ok + m0} of {pf_ok + m0} in all. The reservoir contexts are the blocked modules `Pe2 Pe4 pe5` (one private spare move for White, file e or g) and
         `Pe2 pe5 pe3` (one for Black), combined on the files e and g so that s has a spare moves and s̄ has b ({nE1} of 32 sorties, 8
         contexts each: Δ = a − b ∈ {{−2, −1, 0, 1, 2}}). Here the refined prediction is: punished iff Δ ≤ 0 or the P-variant local
         game with Δ passes is won. Δ ≤ 0: {m0} of {m0 + m0f} punished. Δ > 0 predicted punished: {p_ok} of {p_ok + p_okf} punished. Δ > 0
         predicted not punished: {q_n} not punished (draw or White win, as predicted), {q_p} punished anyway; these are not contradictions,
         because the local game confines s̄'s king to F_Z and the real s̄ may raid the reservoir. The harness therefore has power.
     - **Verdict on open question 1.** (a) The conjecture as worded is **false** in P: a context can be a second-player win for the
       punisher in the frozen convention and the plain-only sortie still wins, (COMPUTED-1; in chess too for 20 of the 29 cases of ES, where Black cannot win). In every failure s's king stands within 2 steps of
       a pawn of G after the sortie and T ≥ 4 (the mechanism, that the king captures the pawn that makes G a second-player win, is a
       CONJECTURE). (b) For promotion-free contexts that are second-player wins, with
       or without a surplus for s̄, all tests agree with tempo matching: CONJECTURE, supported by {pf_ok + m0} of {pf_ok + m0} cases.
       (c) With the hypotheses of Proposition 8.1 it is a theorem, but those hypotheses are very restrictive: in none
       of the tested cases does it hold: (P3) fails in all {p4tot} matched sortie–context pairs on `cyl:8×6` (ES, EP, E3) and in all
       256 sortie–context pairs with the reservoir contexts (`scripts/p4_check.py`, with R from `scripts/analysis_R.py`; the
       sortie king can reach the context files within T ≥ 3 moves). It is a proved sufficient condition, not the
       explanation of the data. (d) The k = ∞ criterion is too
       strong for finite contexts: 953 of the 1372 plain-only king sorties are won for every budget tried.
       Boundary: ≤ 2 + 2 pawns (≤ 3 + 2 in the group search only) on 3 or 4 files of `cyl:7×6` and `cyl:8×6` (and `flat:6×6` for the group
       search), contexts of at most 2 + 2 pawns on the context files (at most 3 pawns for the modules), model P; chess was run
       only for the 41 positions above (a promotion in chess is not an immediate win), and not for the promotion-free tests.
     - **Proposition 8.1 (tempo pairing). PROVED (one derivation, K18; not re-derived by a second model).** Let Q (s to move) be as in
       Theorem 2.7(b), with no e.p. right at Q, context G on the context files. Assume:
       - (P1) s̄ wins the plain local game L_T^0(Q_Z) (s may not pass; stalemate of s is a failure for s̄; the (L1_P) version is
         enough for P);
       - (P2) there is a set 𝒢 of context positions with s to move that contains the context of Q, contains no promotion move in its play
         (neither side promotes in any play of 𝒢 under the pairing below), and is closed under pairing: after any legal
         context-pawn move of s from a position of 𝒢 (e.p. captures included) s̄ has a legal context-pawn move to a position
         of 𝒢. (𝒢 = the positions at which s̄ wins the frozen game with s to move, when G is promotion-free.)
         Let X be the set of squares on which a context pawn stands in some position of 𝒢-play;
       - (P3) let R be the set of squares on which s's king can stand in lines of L_T^0(Q_Z) where s̄ plays its winning strategy;
         then R contains no square of X or of its king-neighbourhood.
       Then s̄ wins P from Q.
       - *Proof.* s̄ plays: to a local move of s (a king move or a Z-pawn move) the reply of its winning strategy σ of L_T^0(Q_Z);
         to a context-pawn move of s the pairing reply of (P2). Local part: delete the context pairs from a real play. By the
         arguments of Steps 1 to 6 of Theorem 2.7 (a context pair changes only the context and the side to move twice, and a
         pending e.p. right on F_Z that s lets lapse only removes an option of s) what is left is a play of L_T^0(Q_Z) in which s̄
         follows σ, with no passes of s, so it ends within T moves of s̄ by a promotion by s̄ or a mate of s. A promotion by s̄ is a
         legal real move (Step 2), a mate in the projection is a mate in the real game because a context pawn never attacks
         s's king (P4: the king stays outside the king-neighbourhood of X). Every real legal local move of s is a legal local
         move and conversely, for the states of the lines (the destination of a king move lies in R, outside the neighbourhood of X,
         so no context pawn attacks or occupies it; Z-pawn moves are the same). Hence s is never stalemated in the real play:
         it has a local move whenever it has one in the plain game, and the plain win means that s is never stalemated there. So
         neither (L3) nor (L3_F) has to be assumed. Pairing replies exist and are legal: the context
         pawns move on squares of X, which by (P3) are never occupied by s's king, s̄'s king stays on F_Z (a buffer file separates
         it from the context), and a context pawn move gives no check to a king on F_Z (Lemma 2.2). A real context move of s is a
         move of the abstract pawn game (the king stands outside X), so it is covered by (P2). No promotion occurs in the context: none in
         𝒢-play, and s's king cannot capture or block a context pawn by (P3). The number of context pairs is finite (pawns only advance or are captured), so the play ends. ∎
       - *What it does not say.* (P3) is a hypothesis on the sortie king; without it the statement is false (the
         counterexamples above). (P2) can be certified by `kpsolve --frozen` (zero or negative) and a search for promotions.
       - A finite-budget form (s has at most k more spare moves than s̄, and s̄ wins the local game with k passes) is the natural
         generalisation; it is a CONJECTURE here, supported by the Δ > 0 cases above.
"""
new2 = old2 + f"""
- **K18 re-computation (2026-10-27; scripts, logs and `summary.json` in `kings/delegate/out/K18/`).** For open question 1. New
  implementations, written from Definition 2.6 and `kings/SPEC.md`: `scripts/lg.cpp` (the local game of Definition 2.6, all
  pawn configurations of ≤ 2 + 2 or ≤ 3 + 2 pawns on F_Z at once, pass budgets 0 to 6 and ∞, queen clause and the mate rule
  as in K7), `scripts/lg2.py` and `scripts/lg2k.py` (a second, independent solver, with budgets). They agree with §5.1, §5.5 and with
  each other (140 random positions, 0 mismatches). The full-board checks use private builds of `kings/kpsolve.c` and of K7's
  `kp_p.c` (`--pmodel`): the plain local game is a lower bound of bare P at 108,710 of 108,710 positions. The group search, the
  finite-budget classes, the context experiments and Proposition 8.1 are recorded in §8, open question 1.
  One bug found on the way (fixed, all numbers above are after the fix): a configuration in which a White and a Black pawn
  share a square was treated as a root; the bare P check (`X`, illegal) exposed it."""
open("EDITS.md", "w").write(f"""### EDIT section 8 open question 1 (K18)
<<<<<<< OLD
{old1}
=======
{new1.rstrip()}
>>>>>>> NEW

### EDIT appendix A K18 (K18)
<<<<<<< OLD
{old2}
=======
{new2}
>>>>>>> NEW
""")
print("EDITS.md written; E1 sorties", nE1, "E3 sorties", nE3, "race ok/fail", race_ok, race_fail, "pf", pf_ok, pf_fail, "e1", dict(e1))
