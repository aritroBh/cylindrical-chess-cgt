#!/bin/zsh
# Launch the A8 (kings/) delegated tasks on external AI CLIs, headless, in the background.
# Same conventions as delegate/run.sh (the main session's launcher, which this does not modify):
# each prompt is delegate/COMMON.md followed by a brief in kings/delegate/briefs/; on a quota or
# rate-limit failure the task re-runs once on the free fallback (kilo nemotron-3-ultra free; omniroute is down).
# Usage: kings/delegate/run.sh K1 [K2 ...]     TOOL=<tool> MODEL=<model> to override.
# Logs: kings/delegate/logs/<task>.log; PIDs: kings/delegate/logs/<task>.pid
ROOT=/Users/aritro/Downloads/Research/Chessendgames
cd "$ROOT" || exit 1
mkdir -p kings/delegate/logs
setopt NO_HUP NO_CHECK_JOBS

typeset -A TOOLS MODELS BRIEF
TOOLS=(K1 codex K1a kilo K1b opencode K1c opencode K2 kilo K3 opencode K4 kilo K5 opencode K8 codex K8v kilo K9 kilo K10 opencode K10v codex)
MODELS=(K1 "" K1a kilo/minimax/minimax-m3.1-flash:free K1b omniroute/oc/nemotron-3-ultra-free
        K1c omniroute/auto/best-free K2 kilo/nvidia/nemotron-3-ultra-550b-a55b:free K3 opencode/beam-free
        K4 kilo/nvidia/nemotron-3-ultra-550b-a55b:free K5 opencode/beam-free
        K8 "" K8v kilo/nvidia/nemotron-3-ultra-550b-a55b:free K9 kilo/nvidia/nemotron-3-ultra-550b-a55b:free K10 opencode/beam-free K10v "")
BRIEF=(K1 K1_loopy_revision.md K1a K1a_validity_full.md K1b K1b_certificate_full.md
       K1c K1c_loopy_full.md K2 K2_report_referee.md K3 K3_repair_check.md
       K4 K4_gafni_cylinder.md K5 K5_canonical_check.md
       K8 K8_stalemate_tempo.md K8v K8v_verify.md K9 K9_sharp_1_14.md K10 K10_passer_certificate.md K10v K10v_verify.md)

prompt() { cat delegate/COMMON.md; echo; echo "---"; echo; cat "kings/delegate/briefs/$1"; }
cmd_for() {
  local m=$2
  case $1 in
    codex)    echo codex exec -s workspace-write -c approval_policy=never -C "$ROOT" ${m:+-m $m} ;;
    opencode) echo opencode run --standalone --auto ${m:+-m $m} ;;
    kilo)     echo kilo run --auto ${m:+-m $m} ;;
    qwen)     echo qwen --approval-mode yolo ${m:+-m $m} -p ;;
    agy)      echo agy --dangerously-skip-permissions ${m:+--model $m} -p ;;
    muse)     echo muse exec --approval-mode never ${m:+--model $m} ;;
    *) echo "unknown tool $1" >&2; return 1 ;;
  esac
}

for task in "$@"; do
  [[ -n $BRIEF[$task] ]] || { echo "unknown task $task" >&2; continue; }
  if [[ -f kings/delegate/logs/$task.pid ]] && ps -p $(<kings/delegate/logs/$task.pid) >/dev/null 2>&1; then
    echo "skip $task: still running"; continue
  fi
  tool=${TOOL:-$TOOLS[$task]}; model=${MODEL-$MODELS[$task]}   # MODEL="" means the tool's default
  cmd=($(cmd_for $tool $model)) || continue
  fb=($(cmd_for ${FALLBACK_TOOL:-kilo} ${FALLBACK:-kilo/nvidia/nemotron-3-ultra-550b-a55b:free}))
  log="kings/delegate/logs/$task.log"; text="$(prompt $BRIEF[$task])"
  (
    $cmd "$text" > "$log" 2>&1 < /dev/null
    if tail -c 2000 "$log" | grep -qiE "usage limit|RESOURCE_EXHAUSTED|Rate limit exceeded|Endpoint is unavailable|billing|quota reached|only try 10 times|idle timeout|Too Many Requests"; then
      echo "\n=== $(date): $tool failed; falling back to $fb" >> "$log"
      $fb "$text" >> "$log" 2>&1 < /dev/null
    fi
  ) &!
  echo $! > "kings/delegate/logs/$task.pid"
  echo "launched $task (pid $!): $tool ${model:-default}"
done
