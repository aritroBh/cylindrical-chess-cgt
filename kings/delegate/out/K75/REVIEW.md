# K75 review (coordinator, 2026-11-26)

Question: which of the 48 exact over groups of flat 8×8 keep, in the promotion game P, the results of ω beside
real pawns on one separated file of the same board, and is there a rule in terms of the kings' distances to
that file?

Investigator: `findings.txt`. Referee (K76, independent; third solver p74, own predictor, own recount):
`verify/VERIFY.md`. The note's paragraph "K75" after the K72 paragraph is the referee's text
(`verify/EDITS.md`), with one change by me: the ten K67 groups are now refereed (K77), so the paragraph cites
the census of Corollary 4.17 and not "referee pending". Where `findings.txt` says that K67's search rests on
one program, that is out of date.

| Statement | Label |
|---|---|
| 58 (group, file) pairs; seven groups have no separated file | recomputed by the referee from the group strings |
| Contexts of at most 1 + 1 pawns (43 a pair): 11 pairs (10 groups) agree everywhere; 427 contexts of the other 47 differ; every one has pawns of both colours | CHECKED-2 (pk, ref3m, p74 agree at all 19,952 positions) |
| For the three groups that fail (C) only q = 0_D and root ≤ ω are proved; against that 18 of the 427 are no failure (409 fail; 12 pairs without a failure of a proved statement) | referee's correction of the reading |
| C125_10 h and C145_13 h clean at 2 + 2; C014_01 h clean at 3 + 3 | CHECKED-2 |
| C014_01, C145_13, C145_17, C145_20 on h, C125_20 on a, C125_21 on h clean beside all 729 placements; C125_17, C125_18 on h, C014_06 on g and h clean at 2 + 2; C125_10 h clean up to 3 + 3 | COMPUTED-1 (p74) |
| Every clean pair has d_W ≥ 4 and d_W + d_B ≥ 8; no rule in the two distances is sufficient (12 pairs with d_W = 7, d_B = 5: four clean, eight failing) | a description of the 58 pairs, computed; not a conjecture |
| The investigator's tempo refinement (R1') | has an unlisted exception (C034_01 on g); not used |
| "2 + 2 does not fit for the eight-man pairs" | refuted: p74 with the contexts split into parts runs them |

What it means. Six groups keep the results of ω beside every pawn placement on one file of the same board,
by one program; three of them up to 2 + 2 or 3 + 3 by three. So real examples exist where the abstract theorem
describes the real board, but they are a minority (10 or 11 of 41 groups with a separated file), and whether a
group is one is decided by the group (can a king leave its post, is there something to take), not by distance.
A theorem would need a hypothesis that pins both kings; the note has none.

Process notes. Investigator: one unmeasured direct run of 141 s (killed by itself, own PID); its chain took
freed slots without a gap for two and a half hours and held both for about ten minutes. Referee: one direct
run of 36 s; sizing runs without the watchdog (under 0.06 GB, under a second each).
