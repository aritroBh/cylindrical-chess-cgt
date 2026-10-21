#!/bin/zsh
# Launch the delegated tasks on external AI CLIs, headless, in the background.
# Usage: delegate/run.sh [T1 T2 ...]   (no arguments = all tasks)
# Logs: delegate/logs/<task>.log; PIDs: delegate/logs/<task>.pid
ROOT=/Users/aritro/Downloads/Research/Chessendgames
cd "$ROOT" || exit 1
mkdir -p delegate/logs

prompt() { cat delegate/COMMON.md; echo; echo "---"; echo; cat "delegate/briefs/$1"; }

launch() {  # launch <task> <brief> <command...>  (the prompt is appended as the last argument)
  local task=$1 brief=$2; shift 2
  if [[ -n "$SELECT" && " $SELECT " != *" $task "* ]]; then return; fi
  nohup "$@" "$(prompt "$brief")" > "delegate/logs/$task.log" 2>&1 < /dev/null &
  echo $! > "delegate/logs/$task.pid"
  echo "launched $task (pid $!): $1"
}

SELECT="$*"
launch T1 T1_codex_independent_verify.md   codex exec -s workspace-write -c approval_policy=never -C "$ROOT"
launch T2 T2_qwen_proof_check.md           qwen --approval-mode yolo -p
launch T3 T3_agy_elkies_targets.md         agy --dangerously-skip-permissions -p
launch T4 T4_opencode_cylinder_ep_aware.md opencode run --auto
launch T5 T5_cursor_ml_chesssums.md        cursor-agent --force -p
launch T6 T6_muse_ml_dawson.md             muse exec --approval-mode never
launch T7 T7_kilo_completeness_review.md   kilo run --auto
