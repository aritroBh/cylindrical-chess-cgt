# Source me: shared shell variables for the certify workstream.
R=/Users/aritro/Downloads/Research/Chessendgames
EP=/private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt
PY=$R/.venv/bin/python
OUT=$R/realchess/certify/results
LOGS=$R/realchess/certify/logs
# tag|component
CANDS="Wa3b3c2_Bb5b7c6|W: a3 b3 c2 / B: b5 b7 c6
Wa3b2b4_Ba7b6c6|W: a3 b2 b4 / B: a7 b6 c6
Wa3b2c2_Ba4b6c5|W: a3 b2 c2 / B: a4 b6 c5
Wa5b3c4_Ba6b7c7|W: a5 b3 c4 / B: a6 b7 c7
Wa3b2d3_Ba6c7d6|W: a3 b2 d3 / B: a6 c7 d6
Wa2c2_Bb7d7|W: a2 c2 / B: b7 d7"
comp_of() { echo "$CANDS" | grep "^$1|" | cut -d'|' -f2; }
tb() { (cd $R && PYTHONPATH=$R "$PY" "$@"); }          # textbook tree (main checkout cylcgt)
ea() { (cd $EP && PYTHONPATH=$EP:$R "$PY" "$@"); }      # e.p.-aware tree (worktree cylcgt)
