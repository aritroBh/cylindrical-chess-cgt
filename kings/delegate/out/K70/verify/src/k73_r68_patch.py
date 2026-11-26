"""K73: patch a scratch copy of the K68 referee's solver r68.cpp with a 'pval' query (FEN with side and e.p. field).

Usage (from the project root; SCR is a scratch directory outside the repository):
  .venv/bin/python -B -I kings/delegate/out/K70/verify/src/k73_r68_patch.py kings/delegate/out/K68/verify/src/r68.cpp SCR/r68.cpp
  c++ -O2 -std=c++17 -o SCR/r68 SCR/r68.cpp
  .venv/bin/python -B -I kings/delegate/out/K70/verify/src/k73_check.py --dump SCR
  (cat SCR/positions_B_D.txt; awk '{print $1"_"$2, $3, $4, $5}' SCR/starts.txt; cat SCR/blockade.txt) | SCR/r68 pval > SCR/r68_vals.out
  .venv/bin/python -B -I kings/delegate/out/K70/verify/src/k73_cmp.py SCR/r68_vals.out
Nothing else in r68 is changed: the solver, its move generator and its configuration closure are K68's.
"""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src).read()
a = """  i++; p.stm = (i < fen.size() && fen[i] == 'b') ? 1 : 0;
  return p;"""
assert s.count(a) == 1
s = s.replace(a, """  i++; p.stm = (i < fen.size() && fen[i] == 'b') ? 1 : 0;
  i += 2; if (i + 1 < fen.size() && fen[i] >= 'a' && fen[i] <= 'h') p.c.ep = sqp(fen.c_str() + i);  // K73: e.p. field
  return p;""")
b = '  if (cmd == "lemmaB") {'
assert s.count(b) == 1
s = s.replace(b, r'''  if (cmd == "pval") {  // K73: lines "label <board> <w|b> <ep|->" -> label, FEN, value in P (White's view)
    char line[512];
    while (fgets(line, sizeof line, stdin)) {
      string s(line); while (!s.empty() && (s.back() == '\n' || s.back() == '\r')) s.pop_back();
      if (s.empty()) continue;
      size_t sp = s.find(' '); string lab = s.substr(0, sp), fen = s.substr(sp + 1);
      Pos p = fromfen(fen);
      if (!valid(p)) { printf("%s %s INVALID\n", lab.c_str(), fen.c_str()); continue; }
      if (cid.find(p.c) == cid.end()) { printf("%s %s MISSINGCFG\n", lab.c_str(), fen.c_str()); continue; }
      printf("%s %s %s\n", lab.c_str(), fen.c_str(), wval(p, 0).c_str());
    }
  }
''' + b)
open(dst, "w").write(s)
print("patched", dst)
