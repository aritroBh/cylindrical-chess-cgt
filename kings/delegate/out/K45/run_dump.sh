#!/bin/zsh
cd "$(dirname $0)"
../../heavy.sh ./bin/p45a --kind cyl --W 10 --H 6 --files 0,2,5 --nw 2 --nb 2 --mode none --dump 1500 7 > logs/dump_a.out 2> logs/dump_a.err
grep '^DUMP' logs/dump_a.out | sed 's/^DUMP //' | sed 's/ | .*//' > logs/dump_pos.txt
../../heavy.sh ./bin/ref3m_k45 --board cyl:10x6 < logs/dump_pos.txt > logs/dump_ref.out 2> logs/dump_ref.err
echo done > logs/dump.done
