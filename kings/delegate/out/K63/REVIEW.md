# K63 review (2026-11-24)

Item: the 2 + 2 over group F2 (White Ka4, Pb2, Pf5; Black king c4/c5, pb6, pf6) on the ordinary 8×8 board, in chess
and beside other pawns. Brief: `kings/delegate/briefs/K63_brief.md`. Investigator: `findings.txt`, `EDITS.md`
(superseded). Referee, independent: `verify/VERIFY.md`, `verify/EDITS.md` (the edit installed in
`kings/theory/LOOPY.md`, Corollary 4.17's paragraph).

## Result

- **Chess (KNOWN, Syzygy tablebases through the Lichess API, 60 requests, 2026-11-24).** F2 and F1 are not exact over
  groups in chess: the c4 root with Black to move, the c5 root with White to move and the position after b2–b3 with
  Black to move are draws. Only the c4 root keeps its structure: b2–b4 is White's only non-losing move and the
  position after it is a mutual zugzwang. F3 and F4 keep the other root instead (the freeze b2–b3 or f2–f3 wins and
  its position is a mutual zugzwang). The 50-move rule changes nothing. The investigator's cap-1 tables agree with
  the tablebase at all 111 exact values, and all 47 open bound pairs contain the tablebase value.
- **P contexts (CHECKED-2, three programs on the P values, three on the predictions).** Beside the 283 contexts of at
  most 2 + 2 pawns on file h the P result equals the D-sum prediction in 271. The 12 failures have a White pawn on h2
  blocked by a Black pawn; all 40 differing results favour Black. So F2 is not over beside P contexts.
- **Flat 8×8 against flat 8×7, mirror:** confirmed.

## Corrections by the referee (all used)

- "Whether F2 is exact in chess is open" is settled: it is not.
- The mechanism sentence: the king walk to h2 wins only the position after b2–b3 and the c5 root with Black to move;
  elsewhere the difference follows because that freeze now loses.
- Definition 2.1: d and e are group files (the group's files form an arc a to f), g is the buffer, h the only context
  file.
- The partial 2 + 2 count on files g, h (1,146 of 4,579 contexts, not a sample) is left out of the note.

## Not checked

The count of positions whose P value differs between the two boards (39,859 of 883,243; COMPUTED-1); the direct sums
by vgsum59 beside the contexts (COMPUTED-1); most touching-file contexts (seven re-solved); F5 and the 2 + 2 contexts
on d, e in any model.

## Process notes

- Memory rule broken by the investigator: three context runs on files g, h reached 4.9, 5.2 and 6.2 GB (limit 3 GB)
  before it stopped them; they had been started as a chain without a watchdog. Later runs and all referee runs were
  under a 2.2 GB watchdog (referee's peak 1.61 GB).
- The tablebase cache is packed as `verify/logs/tbcache.tar.xz`; the request ledger is `verify/tb_ledger.jsonl`.
- Five empty run markers (`logs/*.done`) were removed before the commit.
