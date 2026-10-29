// usage: prof <cyl|flat> W H pairs N   : lead profile Lw Fw Lb Fb of every root (see K31 tempo.cpp header for the definition)
#include "mini.h"
int main(int argc, char** argv) {
  bool cyl = string(argv[1]) == "cyl"; int W = atoi(argv[2]), H = atoi(argv[3]); auto pairs = parsePairs(argv[4]); int N = atoi(argv[5]);
  LK lk; lk.build(W, H, cyl, pairs);
  vector<int> roots = lk.roots(); IntGame I = buildInt(N);
  vector<int> nid; bool closed = true;
  for (int rt : roots) for (int m = 0; m < 2; m++) for (int t : (m == 0 ? lk.g.L : lk.g.R)[rt]) if (t >= 0 && lk.raw[t] / lk.NSQ / lk.NSQ != lk.full) closed = false;
  Game sub; if (closed) sub = subgameRoots(lk, nid);
  const Game* G = closed ? &sub : &lk.g;
  if (!closed) { nid.assign(lk.g.n, 0); for (int i = 0; i < lk.g.n; i++) nid[i] = i; }
  Multi M; M.C = {G, &I.g}; M.solve();
  for (size_t k = 0; k < roots.size(); k++) (void)k;
  map<array<int,4>, long> hist; map<int,long> vals[4];
  for (size_t k = 0; k < roots.size(); k++) {
    int Lw = -1, Fw = -1, Lb = -1, Fb = -1;
    for (int n = 0; n <= N; n++) {
      if (M.res({nid[roots[k]], I.node(-n)}, 1) == 2) Lw = n;
      if (M.res({nid[roots[k]], I.node(-n)}, 0) == 2) Fw = n;
      if (M.res({nid[roots[k]], I.node(n)}, 0) == 0) Lb = n;
      if (M.res({nid[roots[k]], I.node(n)}, 1) == 0) Fb = n; }
    hist[{Lw, Fw, Lb, Fb}]++; vals[0][Lw]++; vals[1][Fw]++; vals[2][Lb]++; vals[3][Fb]++; }
  printf("%s:%dx%d %s N=%d roots %zu\n", argv[1], W, H, argv[4], N, roots.size());
  const char* nm[4] = {"Lw", "Fw", "Lb", "Fb"};
  for (int i = 0; i < 4; i++) { printf(" %s {", nm[i]); for (auto& kv : vals[i]) printf(" %d:%ld", kv.first, kv.second); printf(" }\n"); }
  return 0; }
