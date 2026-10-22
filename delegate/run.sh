#!/bin/zsh
# Launch delegated tasks on external AI CLIs, headless, in the background.
# Usage: delegate/run.sh [TASK ...]           tasks T1..T23, groups "wave2", "codex" (T1 T8), "paper" (T16),
#        "review" (T17 T18), "revise" (T19), "research3" (T20-T23); no args = T1..T15
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
       T8 codex T9 opencode T10 opencode T11 opencode T12 kilo T13 opencode T14 kilo T15 kilo T1b opencode T8b opencode
       T16 codex T17 opencode T18 opencode T19 codex T20 codex T21 opencode T22 opencode T23 opencode T22b opencode T21b opencode T24 opencode T25 kilo T26 kilo T27 opencode)
# free models verified working on 2026-10-21 (aihubmix free tier = 10 tries; opencode deepseek rate-limited)
MODELS=(T1 "" T2 kilo/nvidia/nemotron-3-ultra-550b-a55b:free T3 omniroute/auto/coding:free
        T4 omniroute/auto/coding:free T5 omniroute/auto/best-free T6 opencode/beam-free
        T7 kilo/kilo-auto/free T8 "" T9 omniroute/auto/coding:free T10 omniroute/oc/nemotron-3-ultra-free
        T11 omniroute/auto/best-free T12 kilo/minimax/minimax-m3.1-flash:free T13 opencode/beam-free
        T14 kilo/nvidia/nemotron-3-ultra-550b-a55b:free T15 kilo/kilo-auto/free
        T1b omniroute/auto/coding:free T8b omniroute/oc/nemotron-3-ultra-free
        T16 "" T17 omniroute/auto/best-free T18 opencode/beam-free T19 "" T20 ""
        T21 omniroute/auto/coding:free T22 omniroute/oc/nemotron-3-ultra-free T23 omniroute/auto/coding:free T22b omniroute/auto/coding:free T21b omniroute/auto/best-free T24 omniroute/auto/coding:free T25 kilo/minimax/minimax-m3.1-flash:free T26 kilo/minimax/minimax-m3.1-flash:free T27 omniroute/auto/coding:free)
BRIEF=(T1 T1_codex_independent_verify.md T2 T2_qwen_proof_check.md T3 T3_agy_elkies_targets.md
       T4 T4_opencode_cylinder_ep_aware.md T5 T5_cursor_ml_chesssums.md T6 T6_muse_ml_dawson.md
       T7 T7_kilo_completeness_review.md T8 T8_star2_frontier_search.md T9 T9_mobius_klein.md
       T10 T10_pawn_tablebases_cylinder.md T11 T11_thermography_atomic.md T12 T12_odd_cylinders_opposition.md
       T13 T13_engines_on_chesssums.md T14 T14_dawson_variants.md T15 T15_novelty_literature.md
       T1b T1b_free_independent_verify.md T8b T8b_star2_frontier_search.md
       T16 T16_ieee_paper_draft.md T17 T17_ieee_factcheck.md T18 T18_ieee_style_review.md T19 T19_ieee_revise.md
       T20 T20_star2_real_oracle.md T21 T21_width5_census.md T22 T22_seven_pawn_independent.md T23 T23_kpkp_cylinder.md T22b T22b_seven_pawn_resume.md T21b T21b_width5_finish.md T24 T24_star3_hunt.md T25 T25_odd_cylinders_verify.md T26 T26_ring_pattern.md T27 T27_textbook_star3.md)
ALL=(T1 T2 T3 T4 T5 T6 T7 T8 T9 T10 T11 T12 T13 T14 T15)

tasks=()
for a in "$@"; do
  case $a in
    wave2) tasks+=(T2 T3 T4 T5 T6 T7 T9 T10 T11 T12 T13 T14 T15) ;;
    codex) tasks+=(T1 T8) ;;
    paper) tasks+=(T16) ;;              # then: review (after T16 lands), then revise
    review) tasks+=(T17 T18) ;;
    revise) tasks+=(T19) ;;
    research3) tasks+=(T20 T21 T22 T23) ;;
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
