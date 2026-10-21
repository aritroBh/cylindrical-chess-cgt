# T12: odd-circumference cylinders, king opposition and parity

Output directory: `research/odd_cylinders/`.

**Context:** on a cylinder with an odd number of files, king opposition parity breaks; nobody has studied this. `kings/kpsolve` solves exact king-and-pawn chess on small flat and cylinder boards (see `kings/SPEC.md` and the board-size flags). The loopy-game theory is in `kings/theory/LOOPY.md`.

1. **Trébuchets.** For cylinders C_n × R with n = 3..9 files and R = 5..8 ranks (as feasible), find every mutual zugzwang of type K+P vs K+P.
   - Does the 5.1 trébuchet pattern (king on the far side of the seam) exist for every n?
   - How does the answer depend on the parity of n?
2. **Opposition.** For K+P vs K on C_n, compute win/draw for both sides to move. Compare n odd with n even, and state the rule (e.g. "on odd cylinders the defending king can never take the opposition when ...").
3. **Loopy values.** For bare-king and king-tempo groups, classify which are on, off, dud or 0, following LOOPY.md Theorem 3.4, as a function of n.
4. Label every claim COMPUTED-1, CHECKED-2 or PROVED. Give exact reproduce commands.

Write `research/odd_cylinders/REPORT.md`.
