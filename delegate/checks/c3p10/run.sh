#!/bin/zsh
cd "${0:A:h}/../../.."
ulimit -s 65520 2>/dev/null
xargs -P 3 -L 1 zsh -c 'nice -n 15 .venv/bin/python delegate/checks/c3p10/check.py $0 $1 $2 2>delegate/checks/c3p10/r$0_s$1_$2.err' < delegate/checks/c3p10/jobs.txt
echo done > delegate/checks/c3p10/ALL_DONE
