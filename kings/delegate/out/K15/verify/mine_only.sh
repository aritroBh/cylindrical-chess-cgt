#!/bin/zsh
# usage: mine_only.sh NAME "<args>" [nopass]  -> runs/NAME.my.json, runs/NAME.dud
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/verify
NAME=$1; MA=$2; NP=$3; NPM=""; [[ -n "$NP" ]] && NPM="--nopass"
/usr/bin/time -l nice -n 15 bin/mysolve ${=MA} ${=NPM} --dudout runs/${NAME}.dud > runs/${NAME}.my.json 2> runs/${NAME}.my.err
tail -3 runs/${NAME}.my.err | head -1
