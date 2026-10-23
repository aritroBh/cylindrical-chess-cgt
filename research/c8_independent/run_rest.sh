#!/bin/zsh
# Orchestrator takeover of T48 (Codex hit its limit at 19:14, Kilo fallback walled): run chunks 1-3 of the
# 9-pawn C8 ring enumeration one at a time after chunk 0 (pid 31645, started by T48) exits.
cd "${0:A:h}"
while kill -0 31645 2>/dev/null; do sleep 60; done
for c in 1 2 3; do
  nice -n 15 ./c8check --enum $c 4 8 9 > out9_$c.txt 2> out9_$c.err &
  echo $! > chunk$c.pid; wait $!
  echo "[$(date +%H:%M)] chunk $c done: $(tail -2 out9_$c.txt | head -1)" >> progress.txt
done
echo "[$(date +%H:%M)] ALL DONE" >> progress.txt
