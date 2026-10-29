#!/bin/zsh
# chainA.sh: suite_val (cap-1 validation + five children at cap 1), then suite_rows (restricted-bound check of rows 1-4).  ONE heavy.sh job.
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K28
zsh scripts/suite_val.sh
zsh scripts/suite_rows.sh
