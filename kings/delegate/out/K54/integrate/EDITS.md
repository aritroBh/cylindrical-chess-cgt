# K54 integration: edits to kings/theory/LOOPY.md

Source: `kings/delegate/out/K54/FINDINGS.md` (Codex, OpenAI, model gpt-6.2-astra). Each correction was checked
by hand in the K54 integration, and the small witnesses were re-run read-only with `cylcgt` / python-chess
(`findings.txt` in this directory). Apply with `kings/delegate/apply_edits.py`, in order.

### EDIT 1 Definition 1.10: height qualifier of the tempo bound
<<<<<<< OLD
    M_W ≤ Σ_white pawns (H − rank) ≤ (H − 2)p for p legal White pawns. That is ≤ 6p, so ≤ 48 on 8 ranks when
    p ≤ 8, and ≤ 6p in general; BIG = 256 exceeds 6p whenever p ≤ 42. The count ignores a final Z-move, so
=======
    M_W ≤ Σ_white pawns (H − rank) ≤ (H − 2)p for p legal White pawns. On H ranks the bound is (H − 2)p. For
    H ≤ 8 this is at most 6p, hence at most 48 for p ≤ 8, and there BIG = 256 exceeds 6p whenever p ≤ 42
    (revised after K54, 2026-11-23: the earlier "≤ 6p in general" is FALSE on boards taller than 8 ranks; on flat
    1×11, `W a2 / B a10`, White alone pushes seven times, a3 to a9, still without a passer. PROVED). The count ignores a final Z-move, so
>>>>>>> NEW

### EDIT 2 Section 1.4: the same height qualifier where BIG is compared with M
<<<<<<< OLD
With BIG = 256 and pawns only, B > M holds as long as p ≤ 42, since M ≤ 6p (and M ≤ 48 on 8 ranks when
p ≤ 8).
=======
With BIG = 256 and pawns only, on boards of at most 8 ranks B > M holds as long as p ≤ 42, since M ≤ 6p there
(and M ≤ 48 on 8 ranks when p ≤ 8); on H ranks M ≤ (H − 2)p (revised after K54, 2026-11-23: Definition 1.10).
>>>>>>> NEW

### EDIT 3 Theorem 1.11(c) frontier: the right inherited from X
<<<<<<< OLD
    have been in the same component and replaced the right, and its component has not been played since. A right
=======
    have been in the same component and replaced the right, and its component has not been played since
    (revised after K54, 2026-11-23, wording: if a surplus right was already supplied at X, apply (E) at X;
    otherwise apply it at the first pre-event position carrying that right; a right surviving a move elsewhere
    already lay in a separate, untouched component there). A right
>>>>>>> NEW

### EDIT 4 Theorem 1.11(c) frontier: K54 read the printed quiet-move proof
<<<<<<< OLD
  re-derived again by the integration referee; Codex has not read this text. PROVED.)
=======
  re-derived again by the integration referee. K54 (Codex, OpenAI, model gpt-6.2-astra, outside the Claude
  family, 2026-11-23) read this printed quiet-move proof and found every step SOUND, under all three race rules
  and through arbitrarily many splits (`kings/delegate/out/K54/FINDINGS.md`; revised after K54, 2026-11-23:
  this replaces "Codex has not read this text"). PROVED.)
>>>>>>> NEW

### EDIT 5 Theorem 1.11(c): the open question about (E), with the K54 census
<<<<<<< OLD
  fails at the root). Both witnesses have a right at the root. Whether (E) can be dropped for a root without a
  right, with (E) failing only later, is OPEN: the flag-free predecessors of both witnesses agree (COMPUTED-1,
  `flagfree_probe.py`).
=======
  fails at the root). Both displayed counterexamples carry an initial right. For right-free, passer-free 3+3
  roots on five files and six or seven ranks, the adopted passed test and all three race rules, the outcome
  equality holds in the later-failure stratum (COMPUTED-1, K54: 48,576 rule/root outcome-pair comparisons at
  3+3 agree, 12,600 of them with a later failure of (E); finite coverage of these board sizes by a first-split
  reduction, PROVED; `kings/delegate/out/K54/FINDINGS.md`, `pawns_check.py`, `height6.txt`, `height7.txt`). Whether
  (E) can be omitted for arbitrary right-free roots remains OPEN (revised after K54, 2026-11-23); the flag-free
  predecessors of both witnesses agree (COMPUTED-1, `flagfree_probe.py`).
>>>>>>> NEW

### EDIT 6 Theorem 1.11(c), alternative bound: a witness for strictness
<<<<<<< OLD
    played one after another after the moves from X to Y, so Σ M ≤ N(X) (PROVED). The converse fails, since a
    stopped count ends at the first passer and N(X) does not. On boards up to 8×8 with no pawn on its own first
=======
    played one after another after the moves from X to Y, so Σ M ≤ N(X) (PROVED). The converse fails. The
    different stopping rules alone give only this weak inequality, so a witness is needed (revised after K54,
    2026-11-23: the earlier justification "since a stopped count ends at the first passer and N(X) does not" had
    this gap). On flat 2×7, e.p. off, `W a2 / B b3`, B = 2: every first move is terminal, so both stopped maxima
    are 1 and (B) holds; after a2×b3, b3–b4 is legal in continuing play, so N(X) ≥ 2 = B (PROVED). On boards up to 8×8 with no pawn on its own first
>>>>>>> NEW

### EDIT 7 Theorem 2.7, Step 1: a context move is a pass, which also clears a projected right
<<<<<<< OLD
  - *A context-pawn move.* It changes only context pawns, so π(R) is unchanged except for the side to move; an
=======
  - *A context-pawn move.* It changes only context pawns, so in π(R) the projected pieces stay fixed, the turn
    changes, and any previous projected right expires, exactly as in a pass of rule 2 (revised after K54,
    2026-11-23: the earlier "π(R) is unchanged except for the side to move" was literally false when π(R) carried
    an e.p. right. Example: F_Z = {a, b, c}, `W Ka6 Pb7 Pa2 / B Kc4 Pb4 Pe7`, Black to move; after Kc5 and the
    admissible reply a2–a4, Black's e7–e6 clears the usable right on a3, in projection too, and White promotes
    b8=Q safely on its next move against every local reply. PROVED; the move facts COMPUTED-1, python-chess); an
>>>>>>> NEW

### EDIT 8 Status row T1.11(c): the open question about (E)
<<<<<<< OLD
whether (E) can be dropped at roots without a right is OPEN.
=======
whether (E) can be omitted for arbitrary right-free roots remains OPEN; for right-free, passer-free 3+3 roots on five files and six or seven ranks, the adopted passed test and all three race rules, the outcome equality holds in the later-failure stratum (COMPUTED-1, K54, 2026-11-23: 48,576 comparisons agree, 12,600 with a later failure of (E); finite coverage by a first-split reduction, PROVED).
>>>>>>> NEW

### EDIT 9 Status row T1.11(c): K54 read the printed frontier proof
<<<<<<< OLD
Codex has not read the frontier text now printed | R2 item 2; T30 audit: a move count corrected; s12a referee; K52 (Codex) |
=======
K54 (Codex, OpenAI, model gpt-6.2-astra, outside the Claude family, 2026-11-23) read the printed quiet-move proof and found every step SOUND; its wording corrections (the height qualifier in Definition 1.10, a witness for the strictness of B > N(X), the right inherited from X) are made in the text (revised after K54, 2026-11-23; this replaces "Codex has not read the frontier text now printed") | R2 item 2; T30 audit: a move count corrected; s12a referee; K52 (Codex); K54 (Codex) |
>>>>>>> NEW

### EDIT 10 Status row T2.7: K54 read the corrected Steps 5 and 6
<<<<<<< OLD
the statement of (a) and Steps 5 and 6 of the proof are corrected (revised after T83, 2026-11-23) | R1 item 3, R3 items 2 and 3; K3; K7; T83 |
=======
the statement of (a) and Steps 5 and 6 of the proof are corrected (revised after T83, 2026-11-23). K54 (Codex, OpenAI, model gpt-6.2-astra, outside the Claude family, 2026-11-23) read the printed proof with the corrected Steps 5 and 6 and found every step SOUND, and the two reply-mate examples correct; one wording correction, in Step 1: a context move projects to a pass, which also clears a previous projected e.p. right (revised after K54, 2026-11-23) | R1 item 3, R3 items 2 and 3; K3; K7; T83; K54 |
>>>>>>> NEW

### EDIT 11 Status after review: the K54 read
<<<<<<< OLD
after T83, 2026-11-23). **Caveat for the K9 repair (sharp
=======
after T83, 2026-11-23). K54 (Codex, OpenAI, model gpt-6.2-astra, outside the Claude family, 2026-11-23) then
read the printed quiet-move proof of Theorem 1.11(c) and the corrected Steps 5 and 6 of Theorem 2.7 and found
every step SOUND. Its wording corrections (the height qualifier in Definition 1.10, a witness for the strictness
of B > N(X), the expiry of a projected e.p. right in Step 1 of Theorem 2.7) are made in the text (revised after
K54, 2026-11-23). **Caveat for the K9 repair (sharp
>>>>>>> NEW
