#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/verify
echo $$ > logs/queue4.pid
while [[ ! -f logs/queue1.done ]]; do sleep 20; done
/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh scripts/runone2.sh flat:7x7 2 2 > /dev/null 2>&1
echo finished > logs/queue4.done
