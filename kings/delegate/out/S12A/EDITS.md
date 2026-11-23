### EDIT 1: T1.11(c) assumes (E)
<<<<<<< OLD
- **(B)** BIG exceeds every tempo count of every such Y.
=======
- **(B)** BIG exceeds every tempo count of every such Y; and
- **(E)** condition (E) of L1.6 in `notes/lemmas.md`: no such Y with two or more components carries a usable e.p.
  right. (Revised after the s12a referee, 2026-11-23: the step "both models give the child" of the proof uses it.
  Whether (c) holds without (E) is OPEN: no counterexample in a small search, COMPUTED-1.)
>>>>>>> NEW

### EDIT 2: threats are inherited by re-split components (the frontier step)
<<<<<<< OLD
  would need a − threat and a race needs both threats. So every opponent move is a pawn move in a live
=======
  would need a − threat and a race needs both threats. (Re-split components inherit "no − threat": if a live
  component W₀ has no − threat and a move in W₀ does not freeze it, none of its new components has a − threat.
  A double step does not change which files are occupied, so W₀ does not split; a move that splits W₀ is a
  capture, which leaves no e.p. right, so while a − threat of one new component is played out the others stay
  as they are, with no passer and no right; the move followed by that sequence would be a − threat of W₀. This is
  not the monotonicity of Definition 1.10, which is about one fixed D-game; under the e.p.-aware test a sibling
  with a usable right could otherwise turn passed early. Revised after the s12a referee, 2026-11-23.) So every
  opponent move is a pawn move in a live
>>>>>>> NEW

### EDIT 3: where the proof uses (E)
<<<<<<< OLD
  - If the child is non-terminal, both models give the child and the induction hypothesis applies.
=======
  - If the child is non-terminal, both models give the child and the induction hypothesis applies. This uses
    (E): F keeps an e.p. right with its component while play goes on elsewhere, and D drops it after one move.
    If Y has two or more components, (E) makes Y's right unusable, so in F it allows no move; and a pawn that
    failed the passed test only by the e.p. clause would make it usable. So the components other than Z have
    the same options in both models and no passer in the child. For the same reason, after the frontier the
    opponent never captures e.p. with a right left from before it, so its moves are moves of D and the tempo
    count bounds them (revised after the s12a referee, 2026-11-23).
>>>>>>> NEW

### EDIT 4: the remark on re-grouping
<<<<<<< OLD
Re-splitting does not change the D-result: it only re-groups the same positions and options, and the D-result
=======
Re-splitting does not change the D-result: it only re-groups the same positions and options (in D an e.p. right
lapses after one move whatever the grouping; it is F that keeps rights per component, and (E) bridges the two;
revised after the s12a referee, 2026-11-23), and the D-result
>>>>>>> NEW

### EDIT 5: T1.14(ii) names where (E) comes from
<<<<<<< OLD
  that pair (it re-groups the same positions and options). By Theorem 1.11(c), with (V4) supplying (HSS) and
=======
  that pair (it re-groups the same positions and options). By Theorem 1.11(c), with (V1a) supplying (E)
  (revised after the s12a referee, 2026-11-23), (V4) supplying (HSS) and
>>>>>>> NEW

### EDIT 6: bridge diagram
<<<<<<< OLD
S  --Thm 1.11(c) (V4)-->  D  --Thm 1.14 (V1-V3)-->  P  --(A_Q)(X)-->  C
=======
S  --Thm 1.11(c) (V4), (E)-->  D  --Thm 1.14 (V1-V3)-->  P  --(A_Q)(X)-->  C
(revised after the s12a referee, 2026-11-23: (E) added to the first arrow)
>>>>>>> NEW

### EDIT 7: status row T1.11(c)
<<<<<<< OLD
| T1.11(c) | PROVED after repair (new in the revision): the hereditary version for cylcgt's re-splitting value | R2 item 2; T30 audit: a move count corrected |
=======
| T1.11(c) | PROVED after repair (new in the revision): the hereditary version for cylcgt's re-splitting value. GAP → PROVED after repair (revised after the s12a referee, 2026-11-23): the proof used condition (E) without assuming it, and is now stated with (E); every use goes through T1.14, whose (V1a) contains (E). Without (E): OPEN (no counterexample in a small search, COMPUTED-1). The frontier step's inheritance of threats by re-split components is now proved | R2 item 2; T30 audit: a move count corrected; s12a referee |
>>>>>>> NEW
