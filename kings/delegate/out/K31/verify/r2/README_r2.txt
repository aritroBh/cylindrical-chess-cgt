Second K31 referee: own sources and logs.
lk3.cpp   LK game (any number of pairs), generic K-component sum solver, battery B34, modes cls / flat1.
lk3b.cpp  includes lk3.cpp; modes prof, profbatch, pairs, pairsbat, allpairs, c2.
sweep.sh, run_sweeps.sh (via heavy.sh), ext.sh   grid sweeps.  summarize.py, cmpall.py, cmproots.py   comparisons.
Build: c++ -O2 -std=c++17 -o bin/lk3 lk3.cpp ; c++ -O2 -std=c++17 -o bin/lk3b lk3b.cpp   (binaries deleted at the end)
Written from the definition text in K20/summary.json only. Did not read or include mini.h, lk.cpp, kg.cpp or tempo.cpp.
