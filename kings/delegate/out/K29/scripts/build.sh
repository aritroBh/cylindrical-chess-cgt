#!/bin/zsh
# build.sh: private builds of every solver K29 uses (delete bin/ at the end)
R=/Users/aritro/Downloads/Research/Chessendgames
cd $R/kings/delegate/out/K29 && mkdir -p bin
cc -O2 -o bin/kp  $R/kings/kpsolve.c -lpthread                                    # kpsolve (chess, --frozen)
cc -O2 -o bin/kpp $R/kings/delegate/out/K7/scripts/draft/kp_p.c -lpthread          # kp_p, --pmodel
c++ -O2 -std=c++17 -o bin/ref3  $R/kings/delegate/out/K23/verify/ref3.cpp          # independent P / frozen solver
c++ -O2 -std=c++17 -o bin/ref3m $R/kings/delegate/out/K23/verify/ref3m.cpp         # ref3 + --moves
cc -O2 -o bin/grp scripts/grp.c                                                    # K29 screening tool (this directory)
cc -O2 -o bin/grp3 scripts/grp3.c
