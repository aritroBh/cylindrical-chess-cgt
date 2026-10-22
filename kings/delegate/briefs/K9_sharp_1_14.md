# K9: a complete proof of the sharp form of Theorem 1.14

**Output directory:** `kings/delegate/out/K9/` (create it). Write only there. Do **not** edit
`kings/theory/LOOPY.md`; propose edits instead (format below).

## Read first

`kings/theory/LOOPY.md`, these parts:
- the status table at the top, including the row "T1.14, sharp form";
- §1.2: Definitions 1.1–1.5 (D-games, play and results, the models C, P, D, S) and the bridge diagram;
- §1.3: Lemma 1.6 (option monotonicity) and Lemma 1.7 (suicide deletion);
- §1.5: Theorem 1.14 with (V1)–(V4) and the proof of (i), and the paragraph **"Sharp form (GAP …)"** right
  after it;
- Theorem 2.4, which the note calls "the version of this statement for Z".

The referee objection behind the GAP is R2 item 6 in `kings/theory/REVIEWS.md`.

## Task

The sharp form says that the hypotheses are needed only along **one** D-winning strategy of the D-winner σ:
- (V2) only at the terminals that strategy reaches;
- (V3) in the strong form: at every node where the loser is to move, **every** legal Z-move of the loser is a
  P-loss for it;
- (V1a) split: the winner's prescribed moves are legal chess moves, and every legal chess move of the loser is
  a D-option.

The conclusion is that σ wins P(X) by following that strategy. It is not a statement that the result is the
normal-play result.

1. **State it** precisely, as a theorem with numbered hypotheses. Fix:
   - what "a D-winning strategy" is in a D-game, which can be loopy, with a finite-time win;
   - which nodes count;
   - how (V1b), no stalemate, enters. Decide whether it is needed only at the loser's nodes of the strategy.
2. **Prove it** completely, step by step:
   - map the strategy to a P-strategy;
   - show that every loser reply in P is a D-option or a Z-move;
   - Z-moves are P-losses by (V3);
   - terminals are P-wins by (V2);
   - stalemate is excluded;
   - the game ends in finitely many moves (why the D-win is reached in finite time even though Z may be
     loopy).
   
   Say where Lemma 1.6 is used: the winner's extra legal moves are irrelevant. Say also where Lemma 1.7 is
   *not* needed, and why the earlier "needed only for terminals" wording was false.
3. **Check the sharpness claims.** For each weakened hypothesis, show by an example that weakening it further
   breaks the statement. Examples from the note are acceptable: §5.4, §5.3 and P4.
4. **Relate it to Theorem 2.4** in one paragraph.

## Deliverables

- `REPORT.md`, starting with a 5-line summary. Then the statement, the proof and the proposed label (PROVED
  after repair, or what remains GAP and why).
- `EDITS.md`: exact edits to `kings/theory/LOOPY.md` in this format, each OLD copied exactly from the file and
  occurring exactly once:

      ### EDIT n: <title>
      <<<<<<< OLD
      <exact text>
      =======
      <replacement>
      >>>>>>> NEW

  Mark every change "(revised after K9, 2026-10-22)". Edit only:
  - the "Sharp form" paragraph;
  - the status row "T1.14, sharp form";
  - the sharp-form clause of the §0 table row T1.14.

  Another task (K7) is editing Definition 2.6, Theorem 2.7, Proposition 2.10 and their rows, so do not touch
  those.
- Check with a short script that every OLD block occurs exactly once in `kings/theory/LOOPY.md`. Run
  `python3 kings/delegate/apply_edits.py kings/theory/LOOPY.md kings/delegate/out/K9/LOOPY_preview.md
  kings/delegate/out/K9/EDITS.md` and report "applied n, rejected 0".

## Rules

- Follow `delegate/COMMON.md`, especially rule 5 (labels, honesty) and rule 7 (shared machine).
- Any computation: one process, under `nice -n 10`, under 3 GB.
