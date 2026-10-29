// usage: pairs <cyl|flat> W H pairs N : all ordered pairs of +-1 roots (own B34 labels): x+y+c vs integer sum, c=-N..N; x+int(+-1)+c
#include "mini.h"
static int intRes(int m, int s) { if (m > 0) return 2; if (m == 0) return s == 0 ? 0 : 2; return 0; }
int main(int argc, char** argv) {
  bool cyl = string(argv[1]) == "cyl"; int W = atoi(argv[2]), H = atoi(argv[3]); auto pairs = parsePairs(argv[4]); int N = atoi(argv[5]);
  LK lk; lk.build(W, H, cyl, pairs);
  Sigs S = classify(lk);
  vector<int> nid; Game sub = subgameRoots(lk, nid);
  vector<int> pm, val; for (size_t k = 0; k < S.roots.size(); k++) if (S.label[k] == "+1" || S.label[k] == "-1") { pm.push_back(nid[S.roots[k]]); val.push_back(S.label[k] == "+1" ? 1 : -1); }
  IntGame I = buildInt(N);
  Multi P; P.C = {&sub, &sub, &I.g}; P.solve();
  long chk = 0, mis = 0; map<string,long> out;
  for (size_t a = 0; a < pm.size(); a++) for (size_t b = 0; b < pm.size(); b++) {
    for (int c = -N; c <= N; c++) for (int s = 0; s < 2; s++) { chk++; if (P.res({pm[a], pm[b], I.node(c)}, s) != intRes(val[a] + val[b] + c, s)) mis++; }
    char key[64]; snprintf(key, sizeof key, "%+d%+d White-first=%d Black-first=%d", val[a], val[b], P.res({pm[a], pm[b], I.node(0)}, 0), P.res({pm[a], pm[b], I.node(0)}, 1)); out[key]++; }
  // x + integer(+-1) + c : use one more LK x int x int
  Multi Q; Q.C = {&sub, &I.g, &I.g}; Q.solve(); long chk2 = 0, mis2 = 0;
  for (size_t a = 0; a < pm.size(); a++) for (int v1 : {1, -1}) for (int c = -N; c <= N; c++) for (int s = 0; s < 2; s++) { chk2++;
    if (Q.res({pm[a], I.node(v1), I.node(c)}, s) != intRes(val[a] + v1 + c, s)) mis2++; }
  printf("%s:%dx%d %s N=%d roots %zu +-1 %zu : x+y+c checked %ld mismatches %ld ; x+int+c checked %ld mismatches %ld\n", argv[1], W, H, argv[4], N, S.roots.size(), pm.size(), chk, mis, chk2, mis2);
  for (auto& kv : out) printf("   %s : %ld ordered pairs\n", kv.first.c_str(), kv.second);
  return 0; }
