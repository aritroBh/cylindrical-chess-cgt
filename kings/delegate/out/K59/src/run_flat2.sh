#!/bin/zsh
# K59: full checks of the further flat 8x7 hits F2 to F5 (classes 1,2,5 and 1,4,5 of the p45a search).
cd "$(dirname $0)/.."
src/run_group.sh F2 8 7 "Ka4 kc4 Pb2 Pf5 pb6 pf6" c5
src/run_group.sh F3 8 7 "Ke4 kc4 Pb2 Pb5 Pf5 pb6 pf6" c5
src/run_group.sh F4 8 7 "Kc4 ke4 Pb5 Pf2 Pf5 pb6 pf6" e5
src/run_group.sh F5 8 7 "Ka4 kc4 Pb2 Pe5 Pf4 pb6 pe6 pf5" c5
