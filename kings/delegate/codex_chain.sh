#!/bin/zsh
# Run kings/ Codex briefs one at a time (at most one Codex job from the kings/ session).
# Usage: kings/delegate/codex_chain.sh <pid-to-wait-for | 0> K33:K33_k21_blind.md [K34:<brief> ...]
# Logs: kings/delegate/logs/<K>.log; progress: kings/delegate/logs/codex_chain.out. Stops at a usage-limit error.
ROOT=/Users/aritro/Downloads/Research/Chessendgames
cd $ROOT || exit 1
w=$1; shift
while [[ $w != 0 ]] && kill -0 $w 2>/dev/null; do sleep 30; done
for spec in "$@"; do
  k=${spec%%:*}; b=${spec#*:}
  P="$(cat delegate/COMMON.md; echo; echo ---; echo; cat kings/delegate/briefs/$b)"
  echo "start $k $(date +%H:%M)" >> kings/delegate/logs/codex_chain.out
  codex exec -s workspace-write -c approval_policy=never -C $ROOT "$P" </dev/null > kings/delegate/logs/$k.log 2>&1
  echo "end $k rc=$? $(date +%H:%M)" >> kings/delegate/logs/codex_chain.out
  if grep -q "ERROR: You.ve hit your usage limit" kings/delegate/logs/$k.log; then echo "usage limit at $k; stopping" >> kings/delegate/logs/codex_chain.out; break; fi
done
