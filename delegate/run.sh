#!/bin/zsh
# Launch the delegated tasks on external AI CLIs, headless, in the background.
# Usage: delegate/run.sh [T1 T2 ...]                (no tasks = all, each on its default tool)
#        TOOL=opencode delegate/run.sh T2 T3 T6     (run the named tasks on another tool)
#        MODEL=<provider/model> ...                  (optional model override where the tool supports it)
# Logs: delegate/logs/<task>.log; PIDs: delegate/logs/<task>.pid
ROOT=/Users/aritro/Downloads/Research/Chessendgames
cd "$ROOT" || exit 1
mkdir -p delegate/logs

prompt() { cat delegate/COMMON.md; echo; echo "---"; echo; cat "delegate/briefs/$1"; }

# the command for each tool; the prompt is appended as the last argument
cmd_for() {
  case $1 in
    codex)        echo codex exec -s workspace-write -c approval_policy=never -C "$ROOT" ${MODEL:+-m $MODEL} ;;
    qwen)         echo qwen --approval-mode yolo ${MODEL:+-m $MODEL} -p ;;
    agy)          echo agy --dangerously-skip-permissions ${MODEL:+--model $MODEL} -p ;;
    opencode)     echo opencode run --auto ${MODEL:+-m $MODEL} ;;
    cursor-agent) echo cursor-agent --force ${MODEL:+--model $MODEL} -p ;;
    muse)         echo muse exec --approval-mode never ${MODEL:+--model $MODEL} ;;
    kilo)         echo kilo run --auto ${MODEL:+-m $MODEL} ;;
    *) echo "unknown tool $1" >&2; return 1 ;;
  esac
}

typeset -A DEFAULT BRIEF
DEFAULT=(T1 codex T2 qwen T3 agy T4 opencode T5 cursor-agent T6 muse T7 kilo)
BRIEF=(T1 T1_codex_independent_verify.md T2 T2_qwen_proof_check.md T3 T3_agy_elkies_targets.md
       T4 T4_opencode_cylinder_ep_aware.md T5 T5_cursor_ml_chesssums.md T6 T6_muse_ml_dawson.md
       T7 T7_kilo_completeness_review.md)

tasks=("$@")
(( ${#tasks} )) || tasks=(T1 T2 T3 T4 T5 T6 T7)
for task in $tasks; do
  tool=${TOOL:-$DEFAULT[$task]}
  cmd=($(cmd_for $tool)) || continue
  nohup $cmd "$(prompt $BRIEF[$task])" > "delegate/logs/$task.log" 2>&1 < /dev/null &
  echo $! > "delegate/logs/$task.pid"
  echo "launched $task (pid $!): $tool"
done
