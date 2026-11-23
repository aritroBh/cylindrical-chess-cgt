#!/bin/zsh
# K45 implementation B, all layers of a file triple (same search space as implementation A).  Usage: run_ball.sh W files
cd "$(dirname $0)"
W=$1; FL=$2; tag=cyl${W}x6_f${FL//,/_}
[[ -f logs/Ball_$tag.done ]] && exit 0
../../heavy.sh ./bin/b45 --W $W --all $FL > logs/Ball_$tag.out 2> logs/Ball_$tag.err
echo "rc=$?" > logs/Ball_$tag.done
