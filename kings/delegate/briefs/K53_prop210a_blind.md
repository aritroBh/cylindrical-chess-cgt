# K53: blind proof of Proposition 2.10(a) (one-move punishments are universal), then comparison

**Output directory:** `kings/delegate/out/K53/` (it exists and holds `blind_packet.md`). Write only there. Do **not**
edit any existing file. Do not run git.

Proposition 2.10(a) is labelled "PROVED after repair". It was false as first stated (four ranks), was repaired to
H ≥ 5, and had an en passant step added after an audit. Its checkers so far are of one vendor, plus one free model.
The paper's supplement states it. You are an independent check; the order of work is fixed.

## Phase 1: prove it blind

Read **only** `kings/delegate/out/K53/blind_packet.md` (Definitions 1.1–1.5, 2.1, 2.5, 2.6, Lemma 2.2 and the statement
of Proposition 2.10(a), without its proof), plus `kings/SPEC.md` and `cylcgt/pawns.py` (`passed`, `ep_capturable`) for
the move rules and the two passed-pawn tests. Do not open `kings/theory/LOOPY.md` until Phase 1 is finished.

Write `PROOF.md`, your own complete proof. Cover explicitly: where a pawn that can promote in one move stands; why no
enemy pawn blocks or guards its path so that it is passed under the textbook test; why it cannot be captured en
passant in a chess-legal position (whose move was last, in the plain form and in the window form of Definition 2.6);
why H ≥ 5 is needed (give the H = 4 counterexample) and whether H = 5 is enough under the e.p.-aware test; why the
conclusion gives (L2) for T = 1, including the e.p. clause of (L2); and what "chess-legal" must mean for the argument
(a stale e.p. right in a component is the known danger). If the statement is false or needs a hypothesis, give the
smallest counterexample.

Then test it: your own short script that enumerates every chess-legal context of at most 3 + 3 pawns on boards of
3–5 files and 5–8 ranks (flat and cylinder), with and without an e.p. right for the side to move, and checks that
whenever no pawn is passed (each test) no pawn of the side s can promote in one move. Report counts and every
disagreement; repeat for H = 4 to show the failures.

## Phase 2: compare

Only after `PROOF.md` is written, read LOOPY's Proposition 2.10 (from "**Proposition 2.10" to the start of part (b)'s
proof, including "A stronger statement needs six ranks"). Write `FINDINGS.md`: a 5-line summary; where your route
differs; each step of LOOPY's proof marked SOUND, GAP (give the missing step) or FALSE (give a counterexample); the
test counts; your recommended label.

## Rules

`delegate/COMMON.md`, rules 5 and 7. Light computation only (minutes, under 1 GB). No file over 50 MB; no installs, no
network. Never use pkill, killall, `kill -- -1` or any pattern kill. Delete binaries at the end. The repository is
public: no personal data, relative paths only.
