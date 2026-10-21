#!/bin/zsh
# Launch delegated tasks on external AI CLIs, headless, in the background.
# Usage: delegate/run.sh [TASK ...]           tasks T1..T15, "wave2" (every non-codex task) or "codex" (T1 T8); no args = all
#        TOOL=opencode delegate/run.sh T2    override the tool for the named tasks
#        MODEL=<provider/model> ...          override the model
#        FORCE=1 ...                         relaunch even if the task's previous process is still running
# If a tool dies on a quota / rate-limit / billing / dead-endpoint error, the task is re-run once on
# the free fallback model ($FALLBACK, default omniroute/auto/coding:free) and the output is appended to the log.
# Logs: delegate/logs/<task>.log; PIDs: delegate/logs/<task>.pid
ROOT=/Users/aritro/Downloads/Research/Chessendgames
cd "$ROOT" || exit 1
mkdir -p delegate/logs
setopt NO_HUP NO_CHECK_JOBS

prompt() { cat delegate/COMMON.md; echo; echo "---"; echo; cat "delegate/briefs/$1"; }

# the command for each tool (model $2 optional); the prompt is appended as the last argument
cmd_for() {
  local m=$2
  case $1 in
    codex)        echo codex exec -s workspace-write -c approval_policy=never -C "$ROOT" ${m:+-m $m} ;;
    qwen)         echo qwen --approval-mode yolo ${m:+-m $m} -p ;;
    agy)          echo agy --dangerously-skip-permissions ${m:+--model $m} -p ;;
    opencode)     echo opencode run --auto ${m:+-m $m} ;;
    cursor-agent) echo cursor-agent --force ${m:+--model $m} -p ;;
    muse)         echo muse exec --approval-mode never ${m:+--model $m} ;;
    kilo)         echo kilo run --auto ${m:+-m $m} ;;
    *) echo "unknown tool $1" >&2; return 1 ;;
  esac
}

typeset -A TOOLS MODELS BRIEF
# default tool and model per task (free models where possible; reassigned 2026-10-21 after quota failures)
TOOLS=(T1 codex T2 kilo T3 opencode T4 opencode T5 opencode T6 opencode T7 kilo
       T8 codex T9 opencode T10 opencode T11 opencode T12 kilo T13 opencode T14 kilo T15 kilo T1b opencode T8b opencode)
# free models verified working on 2026-10-21 (aihubmix free tier = 10 tries; opencode deepseek rate-limited)
MODELS=(T1 "" T2 kilo/nvidia/nemotron-3-ultra-550b-a55b:free T3 omniroute/auto/coding:free
        T4 omniroute/auto/coding:free T5 omniroute/auto/best-free T6 opencode/beam-free
        T7 kilo/kilo-auto/free T8 "" T9 omniroute/auto/coding:free T10 omniroute/oc/nemotron-3-ultra-free
        T11 omniroute/auto/best-free T12 kilo/minimax/minimax-m3.1-flash:free T13 opencode/beam-free
        T14 kilo/nvidia/nemotron-3-ultra-550b-a55b:free T15 kilo/kilo-auto/free
        T1b omniroute/auto/coding:free T8b omniroute/oc/nemotron-3-ultra-free)
BRIEF=(T1 T1_codex_independent_verify.md T2 T2_qwen_proof_check.md T3 T3_agy_elkies_targets.md
       T4 T4_opencode_cylinder_ep_aware.md T5 T5_cursor_ml_chesssums.md T6 T6_muse_ml_dawson.md
       T7 T7_kilo_completeness_review.md T8 T8_star2_frontier_search.md T9 T9_mobius_klein.md
       T10 T10_pawn_tablebases_cylinder.md T11 T11_thermography_atomic.md T12 T12_odd_cylinders_opposition.md
       T13 T13_engines_on_chesssums.md T14 T14_dawson_variants.md T15 T15_novelty_literature.md
       T1b T1b_free_independent_verify.md T8b T8b_star2_frontier_search.md)
ALL=(T1 T2 T3 T4 T5 T6 T7 T8 T9 T10 T11 T12 T13 T14 T15)

tasks=()
for a in "$@"; do
  case $a in
    wave2) tasks+=(T2 T3 T4 T5 T6 T7 T9 T10 T11 T12 T13 T14 T15) ;;
    codex) tasks+=(T1 T8) ;;
    *) tasks+=($a) ;;
  esac
done
(( ${#tasks} )) || tasks=($ALL)

for task in $tasks; do
  [[ -n $BRIEF[$task] ]] || { echo "unknown task $task" >&2; continue; }
  if [[ -z $FORCE && -f delegate/logs/$task.pid ]] && ps -p $(<delegate/logs/$task.pid) >/dev/null 2>&1; then
    echo "skip $task: still running (pid $(<delegate/logs/$task.pid)); FORCE=1 to relaunch"; continue
  fi
  tool=${TOOL:-$TOOLS[$task]}
  model=${MODEL:-$MODELS[$task]}
  cmd=($(cmd_for $tool $model)) || continue
  fb=($(cmd_for opencode ${FALLBACK:-omniroute/auto/coding:free}))
  log="delegate/logs/$task.log"; text="$(prompt $BRIEF[$task])"
  (
    $cmd "$text" > "$log" 2>&1 < /dev/null
    if tail -c 2000 "$log" | grep -qiE "usage limit|RESOURCE_EXHAUSTED|Rate limit exceeded|Endpoint is unavailable|billing|quota reached|only try 10 times"; then
      echo "\n=== $(date): $tool failed to start; falling back to $fb" >> "$log"
      $fb "$text" >> "$log" 2>&1 < /dev/null
    fi
  ) &!
  echo $! > "delegate/logs/$task.pid"
  echo "launched $task (pid $!): $tool ${model:-default} (fallback: opencode ${FALLBACK:-omniroute/auto/coding:free})"
done
