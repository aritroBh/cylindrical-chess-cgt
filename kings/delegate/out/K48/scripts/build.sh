#!/bin/zsh
# K48: build the solvers from the K39 / K45 sources (relative paths; run from kings/delegate/out/K48). Binaries go to bin/ and are deleted after the runs.
cd "$(dirname $0)/.."
cc -O2 -o bin/kp39 ../K39/src/kp39.c -lpthread -lm
c++ -O2 -std=c++17 -o bin/own39 ../K39/src/own39.cpp
c++ -O2 -std=c++17 -o bin/own2 ../K39/src/own2.cpp
c++ -O2 -std=c++17 -o bin/rf39 ../K39/verify/rf39.cpp
c++ -O2 -std=c++17 -o bin/r48 src/r48.cpp
c++ -O2 -std=c++17 -o bin/p45a ../K45/src/p45a.cpp
c++ -O2 -std=c++17 -o bin/ref3m ../K23/verify/ref3m.cpp
cc -O2 -o bin/kp_p10 ../K44/scripts/kp_p10.c -lpthread -lm
