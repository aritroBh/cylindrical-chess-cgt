#!/bin/zsh
# K59: build the tools from the copies in src/ into bin/ (binaries are deleted at the end).
cd "$(dirname $0)/.."
mkdir -p bin
c++ -O2 -std=c++17 -o bin/vgsum src/vgsum.cpp
c++ -O2 -std=c++17 -o bin/vgsum59 src/vgsum59.cpp
c++ -O2 -std=c++17 -o bin/pr57 src/pr57.cpp
c++ -O2 -std=c++17 -o bin/ref3m src/ref3m.cpp
cc -O2 -o bin/kp_p10 src/kp_p10.c -lpthread -lm
c++ -O2 -std=c++17 -o bin/p45a src/p45a.cpp
c++ -O2 -std=c++17 -o bin/r48 src/r48.cpp
