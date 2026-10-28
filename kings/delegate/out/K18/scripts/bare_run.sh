#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
bin/kpp --board cyl:8x6 --ep on --pmodel --promote Q --cap 0 --threads 2 < logs/bare_in.txt > logs/bare_out.txt 2> logs/bare_out.err
