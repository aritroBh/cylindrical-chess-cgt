# K58 review (2026-11-23)

A blind proof by Codex (model gpt-6.2-astra) of Proposition 4.14 and Lemma 4.15. The packet
(`kings/delegate/briefs/K58_over_lemma_blind.md`) gave the definitions and the two statements only; Codex was told
not to open `kings/theory/` or other output folders. Its raw transcript is not committed.

- Both statements: proved, under the ten readings R1 to R10 of the packet, all of which it accepted as stated.
- It confirms that nothing beyond Definition 4.8 is needed on White's side or at the q's.
- (B1) cannot simply be dropped: `check.py` evaluates an abstract exact shuttle game without (B1) that loses beside
  \* where over wins (COMPUTED-1; no board placement is given for it; on the board the 3 + 3 group of K47 plays this
  role).
- Its own weakest step: the moment White must make a real board move after a bad Black move, charged to Black's one
  spare move.

The proof route is the same in outline as K57's (White answers Black's first pass by freezing; after a deviation the
punisher answers on the board), reached independently. No change to the statements was needed.
