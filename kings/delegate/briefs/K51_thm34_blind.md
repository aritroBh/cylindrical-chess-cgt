# K51: blind proof of Theorem 3.4 (outcome rules with passes), then comparison

**Output directory:** `kings/delegate/out/K51/` (it exists and holds `blind_packet.md`). Write only there. Do **not**
edit any existing file. Do not run git.

Theorem 3.4 is labelled PROVED. Its proof was written by a free external model and read by reviewers of one vendor
only. The paper's supplement states it. You are an independent check from outside that vendor; the order of work is
fixed.

## Phase 1: prove it blind

Read **only** `kings/delegate/out/K51/blind_packet.md`: Definitions 1.1–1.4, Definition 3.1 (the reservoirs on_D, off_D,
dud_D) and the statement of Theorem 3.4, without its proof. Do not open `kings/theory/LOOPY.md`, `notes/` or the
paper until Phase 1 is finished.

Write `PROOF.md`, your own complete proof of (a), (b) and (c). Cover explicitly: the state space (position, side to
move, pass moves); why a pass is never a winning move for the side that would otherwise be to move (or when it is);
well-foundedness of the recursions for Λ and Ρ and for Ρ′; why (a) has draws and (b), (c) have none; the listed
consequences (no zugzwang in (a); every position drawn if G has no terminals; White never in zugzwang in (b)); and the
role of each convention in Definitions 1.2 and 1.3 (a player with no move, infinite play, decisive terminals). If the
statement is false or needs a hypothesis, give the smallest counterexample as an explicit game.

Then test the statement by computation: your own short program (any language, standard library) that enumerates small
short D-games (say up to 5 or 6 positions, with ⊕ and ⊖ terminals), computes r on G ⊞ dud_D, G ⊞ on_D and G ⊞ off_D
directly from Definitions 1.2 and 1.3 (least fixed points), and compares with the recursions of the statement. Report
the counts and every disagreement.

## Phase 2: compare

Only after `PROOF.md` is written, read LOOPY's proof of Theorem 3.4 (from "**Theorem 3.4" to the start of the next
numbered result). Write `FINDINGS.md`: a 5-line summary; where your route differs; each step of LOOPY's proof marked
SOUND, GAP (give the missing step) or FALSE (give a counterexample); the test counts; your recommended label.

## Rules

`delegate/COMMON.md`, rules 5 and 7. Light computation only (minutes, under 1 GB). No file over 50 MB; no installs, no
network. Never use pkill, killall, `kill -- -1` or any pattern kill. Delete binaries at the end. The repository is
public: no personal data, relative paths only.
