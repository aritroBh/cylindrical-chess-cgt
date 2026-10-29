#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/verify
tag=$(echo $1 | tr ':' '_')_$2$3
rm -rf work/$tag; CHUNK=60000 nice -n 15 python3 scripts/ref_enum2.py gen $1 $2 $3 work/$tag > logs/own2_$tag.txt
TMAX=2 nice -n 15 python3 scripts/ref_enum2.py run $1 $2 $3 work/$tag 2>/dev/null >> logs/own2_$tag.txt
