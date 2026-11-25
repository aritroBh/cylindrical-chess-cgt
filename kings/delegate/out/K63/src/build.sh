#!/bin/zsh
# K63: build the tools from the copies in src/ into bin/ (binaries deleted at the end). Run from kings/delegate/out/K63.
cd "$(dirname $0)/.."
mkdir -p bin
cc -O2 -o bin/kpsolve src/kpsolve.c -lpthread -lm
cc -O2 -o bin/kp39 src/kp39.c -lpthread -lm
c++ -O2 -std=c++17 -o bin/own39 src/own39.cpp
c++ -O2 -std=c++17 -o bin/ref3m src/ref3m.cpp
cc -O2 -o bin/kp_p10 src/kp_p10.c -lpthread -lm
c++ -O2 -std=c++17 -o bin/kref src/kref.cpp
c++ -O2 -std=c++17 -o bin/vgsum59 src/vgsum59.cpp
