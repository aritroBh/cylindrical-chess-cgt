// usage: cls <cyl|flat> W H pairs [dump]   -> counts of +1/-1/other classes, optional dump of +-1 roots
#include "mini.h"
int main(int argc, char** argv) {
  bool cyl = string(argv[1]) == "cyl"; int W = atoi(argv[2]), H = atoi(argv[3]); auto pairs = parsePairs(argv[4]);
  bool dump = argc > 5;
  LK lk; lk.build(W, H, cyl, pairs);
  Sigs S = classify(lk);
  map<string,int> cnt; int p = 0, m = 0; long fileBad = 0, parBad = 0;
  for (size_t k = 0; k < S.roots.size(); k++) { cnt[S.label[k]]++; if (S.label[k] == "+1" || S.label[k] == "-1") {
      string nm = lk.name(S.roots[k]);
      if (dump) printf("DUMP %s :: %s\n", S.label[k].c_str(), nm.c_str());
      (S.label[k] == "+1" ? p : m)++;
      // structure: both kings on file W/2, same colour squares
      ll r = lk.raw[S.roots[k]]; int bk = r % lk.NSQ, wk = (r / lk.NSQ) % lk.NSQ;
      if (!(W % 2 == 0 && lk.fileOf(wk) == W / 2 && lk.fileOf(bk) == W / 2)) fileBad++;
      if ((lk.rankOf(wk) - lk.rankOf(bk)) % 2 != 0) parBad++; } }
  printf("%s:%dx%d %s roots %zu races %ld  +1 %d  -1 %d  notW/2file %ld oddrankdiff %ld\n", argv[1], W, H, argv[4], S.roots.size(), lk.races, p, m, fileBad, parBad);
  return 0; }
