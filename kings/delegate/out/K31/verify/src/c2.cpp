#include "mini.h"
int main() {
  LK lk; lk.build(6, 6, false, parsePairs("a2,c4"));
  Sigs S = classify(lk);
  vector<int> nid; Game sub = subgameRoots(lk, nid); IntGame I = buildInt(3);
  Multi M; M.wantDepth = true; M.C = {&sub, &I.g}; M.solve();
  map<string,int> byName; for (int a : S.roots) byName[lk.name(a)] = a;
  for (string nm : {"Kc3 ka4 Pa2 pa3 Pc4 pc5", "Kd3 kb4 Pa2 pa3 Pc4 pc5", "Kc3 kd1 Pa2 pa3 Pc4 pc5"}) {
    int a = byName.count(nm) ? byName[nm] : -1; if (a < 0) { printf("%s not a root\n", nm.c_str()); continue; }
    string lab; for (size_t k = 0; k < S.roots.size(); k++) if (S.roots[k] == a) lab = S.label[k];
    printf("%s  B34 label %s\n", nm.c_str(), lab.c_str());
    for (int s = 0; s < 2; s++) { printf("  %s to move:", s == 0 ? "White" : "Black");
      for (int c = -2; c <= 2; c++) { int r = M.res({nid[a], I.node(c)}, s); printf("  c=%+d %c(%d)", c, "LDW"[r], M.plies({nid[a], I.node(c)}, s)); } printf("\n"); } }
  // check that the line's positions have the claimed plies: print the White-to-move c=0 principal line (winner picks a min-ply move, loser max)
  return 0; }
