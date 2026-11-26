# K68 review (orchestrator), 2026-11-25

**Installed:** Proposition 4.25 in `kings/theory/LOOPY.md`, from the referee's replacement edit
(`verify/EDITS.md`), with one wording fix of mine: Lemma B is stated for the White king squares not next to b6
(54 for each pawn square), as in the programs; the referee's sentence had dropped that condition.

**What the proposition says.** On flat 8×8, `Kd4 kb4/kb5 Pb6 Pc2 Pc5 pb7 pc6` (C125_05 of the K65 census) is an
exact over group and has the results of ω beside every finite D-game. Label: PROVED, given one CHECKED-2 lemma.

| part | label | source |
|---|---|---|
| K1, K2, (O0), (O1), (O2), (O3), (B1) at all six bad moves | PROVED (hand) | PROOF.md §2–4 with repairs G0, G1 |
| (O4); the freezes are the only non-losing root moves | PROVED given Lemma B | PROOF.md Lemma C with repair G2 |
| Lemma B (two pawns against one; 162 positions, 42 used) | CHECKED-2 | o68, ax68q (K68); r68 (referee) |
| chess values at the roots and q's | KNOWN (Syzygy cache of K65) | `verify/logs/tb_k68.out` |
| hand reduction in chess to 460 positions after b8=Q | PROVED given COMPUTED-1 | q68 (referee) |

**Referee (independent agent, own solver r68 written before reading the investigator's programs).** Every hand step
re-derived; five repairs (G0–G4, `verify/VERIFY.md` §4), none changing a statement in P. One real error, in the chess
section: the cited fact "a queen beats a pawn three or more moves from promotion" is false as stated (87
counterexamples with the pawn on c4 in the referee's conservative solver); withdrawn. White's strategy was played
against every Black reply: 298,179 plays in P (promotion by move 8), 131,902 beside −1 (by move 9, attained).

**PROOF.md** is the investigator's text with a header note pointing to the repairs; the repaired sentences are in
`verify/VERIFY.md` §4 and are not merged into the text.

**Open.** Lemma B by hand. The referee did not get it: no single Black first move wins throughout, and the hard
cases (pawn c2 with the White king on b3, c3, d3; pawn c4 with the king on c3) involve stalemate defences. K70 (a
blind attempt by another vendor's model) is running.

**Process notes.** The investigator ran a few two-second solver runs at 0.55–0.73 GB, over the 0.5 GB toy limit of
its brief and far under the 2 GB rule. The referee's runs: 10 s, 25 MB and 6 s, 55 MB. No binaries in the folder.
