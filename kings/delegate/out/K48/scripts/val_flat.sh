#!/bin/zsh
# K48: r48 (flat option added to r45) against ref3m on random flat positions (P model); r48 on cyl:8x6 for the K45 group (must equal r45).
cd "$(dirname $0)/.."
scripts/hrun.sh val_r48_flat8 2400 in/rnd_flat8.txt bin/r48 val pln:8x6
scripts/hrun.sh val_ref3m_flat8 2400 in/rnd_flat8.txt bin/ref3m --board pln:8x6
scripts/hrun.sh val_r48_flat10 2400 in/rnd_flat10.txt bin/r48 val pln:10x6
scripts/hrun.sh val_ref3m_flat10 2400 in/rnd_flat10.txt bin/ref3m --board pln:10x6
scripts/hrun.sh grp_r48_cyl8 1200 /dev/null bin/r48 group cyl:8x6 over "Pb2 Pb4 Pe2 pa4 pb5 pe5" d4 d5 f5
echo done > logs/val_flat.done
