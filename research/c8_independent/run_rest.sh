#!/bin/zsh
# Orchestrator takeover of T48 (Codex hit its limit at 19:14, Kilo fallback walled). c8check_gen = c8check with a
# generation stamp in place of the per-class memset (same search; node counts identical on the test positions).
# Chunk 0 is re-run with it as a cross-check of the memset run (out9_0.memset.txt), then chunks 1-3.
cd "${0:A:h}"
for c in 0 1 2 3; do
  start=$(date +%s)
  nice -n 15 ./c8check_gen --enum $c 4 8 9 > out9_$c.txt 2> out9_$c.err &
  echo $! > chunk$c.pid; wait $!
  echo "[$(date +%H:%M)] chunk $c done in $(( $(date +%s) - start )) s: $(head -1 out9_$c.txt | grep -v STAR; grep -c STAR out9_$c.txt) star lines" >> progress.txt
done
echo "[$(date +%H:%M)] ALL DONE" >> progress.txt
