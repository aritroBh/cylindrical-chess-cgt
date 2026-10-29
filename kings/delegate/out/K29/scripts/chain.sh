#!/bin/zsh
# chain.sh SCRIPT ARG...  : run "SCRIPT NAME" for each NAME in the list given after --, sequentially.
S=$1; shift
for n in "$@"; do zsh $S $n; done
