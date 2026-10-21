# T6 (muse): ML on Dawson's chess (plan item C3)

Output directory: `ml/dawson/`. Use `.venv-ml/bin/python` (MLX preferred, or PyTorch with MPS).

Background: `dawson/REPORT.md`.
- Normal-play Dawson's chess on 3×n equals octal game 0.137. Its Grundy values g(n) for n <= 300 are in `dawson/` (period 34, last exception n = 51).
- On the cylinder the first player wins iff g(n-3) = 0.

1. Write a small exact environment for 3×n Dawson's chess (flat and ring), or reuse `dawson/` code read-only. Positions are sums of strips.
2. Train a value network, supervised, to predict the outcome (first-player win or loss) of sums of strips.
   - Train on totals up to 30 files.
   - Test on totals of 31-80 files.
   - Report accuracy against total length, and whether the net learns the XOR-of-Grundy rule (probe its features against g(n)).
3. Optional, if time remains: a small AlphaZero-style self-play loop (MCTS plus the net). Compare its play against the exact solver on held-out positions.
4. Write `ml/dawson/REPORT.md`, with the tables and exact commands.
