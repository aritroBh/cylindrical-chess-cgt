// Referee 2: extra modes (profile, sums with contexts, allpairs, line C2). Includes lk3.cpp (same author, this referee).
#include <iostream>
#define main main_base
#include "lk3.cpp"
#undef main
static int pmres(const Sum& S, vector<int> v, int s) { return S.res(v, s); }
// integer sum reference outcome pair: n>0 (W,W); n==0 (L,W); n<0 (L,L)
static pair<int,int> intref(int n) { if (n > 0) return {2, 2}; if (n == 0) return {0, 2}; return {0, 0}; }

int main(int argc, char** argv) {
  string mode = argv[1];
  if (mode == "prof") {   // prof cyl|flat W H pairs N : leads Lw Fw Lb Fb
    int W = atoi(argv[3]), H = atoi(argv[4]); string pairs = argv[5]; int N = atoi(argv[6]);
    Board b = mkBoard(argv[2], W, H); LK lk(b, mkPawns(b, pairs)); Game I = intGame(N);
    Sum S; S.C = {&lk.g, &I}; S.solve();
    map<array<int,4>, int> hist; map<int,int> cl[4];
    int full = (1 << lk.P.size()) - 1;
    for (int x = 0; x < lk.g.n; x++) {
      if (lk.st[x][0] != full) continue;
      int Lw = -1, Fw = -1, Lb = -1, Fb = -1;
      for (int n = 0; n <= N; n++) {
        // White ahead by -n: context -n means Black has n spare moves
        if (S.win[0][S.idx({x, -n + N}, 1)]) Lw = n;   // White wins, Black to move
        if (S.win[0][S.idx({x, -n + N}, 0)]) Fw = n;   // White wins, White to move
        if (S.win[1][S.idx({x, n + N}, 0)]) Lb = n;    // Black wins, White to move
        if (S.win[1][S.idx({x, n + N}, 1)]) Fb = n;    // Black wins, Black to move
      }
      hist[{Lw, Fw, Lb, Fb}]++; cl[0][Lw]++; cl[1][Fw]++; cl[2][Lb]++; cl[3][Fb]++;
    }
    const char* nm[4] = {"Lw", "Fw", "Lb", "Fb"};
    printf("PROF %s %dx%d %s N=%d", argv[2], W, H, pairs.c_str(), N);
    for (int k = 0; k < 4; k++) { printf(" %s{", nm[k]); for (auto& kv : cl[k]) printf("%d:%d ", kv.first, kv.second); printf("}"); }
    printf("\n");
  } else if (mode == "pairs") {   // pairs cyl|flat W H pairs N : x+y+c and x+int+c
    int W = atoi(argv[3]), H = atoi(argv[4]); string pairs = argv[5]; int N = atoi(argv[6]);
    Board b = mkBoard(argv[2], W, H); LK lk(b, mkPawns(b, pairs)); auto B = battery(); auto sg = signatures(lk.g, B);
    Game one = intGame(2); auto so = signatures(one, B); string s1 = so[3], sm = so[1];
    int full = (1 << lk.P.size()) - 1; vector<int> roots, sgn;
    for (int x = 0; x < lk.g.n; x++) { if (lk.st[x][0] != full) continue; if (sg[x] == s1) { roots.push_back(x); sgn.push_back(1); } else if (sg[x] == sm) { roots.push_back(x); sgn.push_back(-1); } }
    Game I = intGame(N + 2);   // integer context game, range -(N+2)..N+2
    Sum S3; S3.C = {&lk.g, &lk.g, &I}; S3.solve();
    long chk = 0, mis = 0; map<string, long> shape;
    for (size_t i = 0; i < roots.size(); i++) for (size_t j = 0; j < roots.size(); j++) for (int c = -N; c <= N; c++) {
      auto ref = intref(sgn[i] + sgn[j] + c);
      int a = S3.res({roots[i], roots[j], c + N + 2}, 0), bb = S3.res({roots[i], roots[j], c + N + 2}, 1);
      chk++; if (a != ref.first || bb != ref.second) mis++;
    }
    // x + integer(+-1) + c : context game covers s + c
    Sum S2; S2.C = {&lk.g, &I}; S2.solve(); long chk2 = 0, mis2 = 0;
    for (size_t i = 0; i < roots.size(); i++) for (int s : {1, -1}) for (int c = -N; c <= N; c++) {
      auto ref = intref(sgn[i] + s + c); int tot = s + c;
      int a = S2.res({roots[i], tot + N + 2}, 0), bb = S2.res({roots[i], tot + N + 2}, 1);
      chk2++; if (a != ref.first || bb != ref.second) mis2++;
    }
    int np = 0, nm = 0; for (int s : sgn) (s > 0 ? np : nm)++;
    printf("PAIRS %s %dx%d %s N=%d roots %d (+1: %d, -1: %d) x+y+c checked %ld mismatches %ld ; x+int+c checked %ld mismatches %ld\n", argv[2], W, H, pairs.c_str(), N, (int)roots.size(), np, nm, chk, mis, chk2, mis2);
  } else if (mode == "profbatch") {   // stdin lines: board W H pairs N ; prints joint histogram lines
    string bd, pr; int W, H, N;
    while (cin >> bd >> W >> H >> pr >> N) {
      Board b = mkBoard(bd, W, H); LK lk(b, mkPawns(b, pr)); Game I = intGame(N);
      Sum S; S.C = {&lk.g, &I}; S.solve(); map<array<int,4>, int> hist; int full = (1 << lk.P.size()) - 1;
      for (int x = 0; x < lk.g.n; x++) {
        if (lk.st[x][0] != full) continue; int Lw = -1, Fw = -1, Lb = -1, Fb = -1;
        for (int n = 0; n <= N; n++) {
          if (S.win[0][S.idx({x, -n + N}, 1)]) Lw = n; if (S.win[0][S.idx({x, -n + N}, 0)]) Fw = n;
          if (S.win[1][S.idx({x, n + N}, 0)]) Lb = n; if (S.win[1][S.idx({x, n + N}, 1)]) Fb = n;
        }
        hist[{Lw, Fw, Lb, Fb}]++;
      }
      for (auto& kv : hist) printf("J %s %dx%d %s %d %d %d %d %d\n", bd.c_str(), W, H, pr.c_str(), kv.first[0], kv.first[1], kv.first[2], kv.first[3], kv.second);
      printf("R %s %dx%d %s races %ld\n", bd.c_str(), W, H, pr.c_str(), lk.races);
    }
  } else if (mode == "c2") {   // c2 cyl|flat W H pairs wkname bkname N : outcome and plies for c=-N..N, both movers
    int W = atoi(argv[3]), H = atoi(argv[4]); string pairs = argv[5]; string wkn = argv[6], bkn = argv[7]; int N = atoi(argv[8]);
    Board b = mkBoard(argv[2], W, H); LK lk(b, mkPawns(b, pairs)); Game I = intGame(N);
    auto sqof = [&](string t) { return b.sq(t[0] - 'a', atoi(t.c_str() + 1) - 1); };
    int x0 = lk.node(sqof(wkn), sqof(bkn)); if (x0 < 0) { printf("illegal root\n"); return 1; }
    size_t nI = I.n; size_t tot = (size_t)lk.g.n * nI * 2;
    auto id = [&](int x, int k, int s) { return ((size_t)x * nI + k) * 2 + s; };
    vector<int> D[2];
    for (int P = 0; P < 2; P++) {
      D[P].assign(tot, -1); int winT = P == 0 ? TP : TM, loseT = P == 0 ? TM : TP;
      for (int round = 0; round < 400; round++) {
        vector<pair<size_t,int>> upd;
        for (int x = 0; x < lk.g.n; x++) for (int k = 0; k < (int)nI; k++) for (int s = 0; s < 2; s++) {
          size_t me = id(x, k, s); if (D[P][me] >= 0) continue;
          const auto& ox = s == 0 ? lk.g.L[x] : lk.g.R[x]; const auto& ok = s == 0 ? I.L[k] : I.R[k];
          if (s == P) {
            int best = INT_MAX;
            for (int t : ox) { if (t == winT) best = min(best, 1); else if (t >= 0) { int d = D[P][id(t, k, 1 - s)]; if (d >= 0) best = min(best, d + 1); } }
            for (int t : ok) { if (t == winT) best = min(best, 1); else if (t >= 0) { int d = D[P][id(x, t, 1 - s)]; if (d >= 0) best = min(best, d + 1); } }
            if (best != INT_MAX) upd.push_back({me, best});
          } else {
            bool ok2 = true; int mx = 0; bool any = false;
            for (int t : ox) { any = true; if (t == loseT) { ok2 = false; break; } if (t == winT) continue; int d = D[P][id(t, k, 1 - s)]; if (d < 0) { ok2 = false; break; } mx = max(mx, d); }
            if (ok2) for (int t : ok) { any = true; if (t == loseT) { ok2 = false; break; } if (t == winT) continue; int d = D[P][id(x, t, 1 - s)]; if (d < 0) { ok2 = false; break; } mx = max(mx, d); }
            if (ok2) upd.push_back({me, any ? mx + 1 : 0});
          }
        }
        if (upd.empty()) break;
        for (auto& u : upd) D[P][u.first] = u.second;
      }
    }
    printf("C2 %s %dx%d %s K%s k%s\n", argv[2], W, H, pairs.c_str(), wkn.c_str(), bkn.c_str());
    for (int s = 0; s < 2; s++) { printf("  %s to move:", s == 0 ? "White" : "Black");
      for (int c = -N; c <= N; c++) { size_t m = id(x0, c + N, s); int w0 = D[0][m], w1 = D[1][m]; if (w0 >= 0 && w1 >= 0) printf(" c=%d BOTH", c); else if (w0 >= 0) printf(" c=%d:W(%d)", c, w0); else if (w1 >= 0) printf(" c=%d:L(%d)", c, w1); else printf(" c=%d:D", c); }
      printf("\n"); }
  } else if (mode == "pairsbat") {   // pairsbat cyl|flat W H pairs : x+y+K for every K of B34 vs integer(sx+sy)+K
    int W = atoi(argv[3]), H = atoi(argv[4]); string pairs = argv[5];
    Board b = mkBoard(argv[2], W, H); LK lk(b, mkPawns(b, pairs)); auto B = battery(); auto sg = signatures(lk.g, B);
    Game one = intGame(2); auto so = signatures(one, B); string s1 = so[3], sm = so[1];
    int full = (1 << lk.P.size()) - 1; vector<int> roots, sgn;
    for (int x = 0; x < lk.g.n; x++) { if (lk.st[x][0] != full) continue; if (sg[x] == s1) { roots.push_back(x); sgn.push_back(1); } else if (sg[x] == sm) { roots.push_back(x); sgn.push_back(-1); } }
    Game I = intGame(2); long chk = 0, mis = 0;
    for (auto& k : B) {
      Sum S; S.C = {&lk.g, &lk.g, &k.g}; S.solve(); Sum R; R.C = {&I, &k.g}; R.solve();
      for (size_t i = 0; i < roots.size(); i++) for (size_t j = 0; j < roots.size(); j++) {
        int t = sgn[i] + sgn[j]; for (int s = 0; s < 2; s++) { chk++; if (S.res({roots[i], roots[j], k.root}, s) != R.res({t + 2, k.root}, s)) mis++; }
      }
    }
    printf("PAIRSBAT %s %dx%d %s roots %zu battery 34: outcomes checked %ld mismatches %ld\n", argv[2], W, H, pairs.c_str(), roots.size(), chk, mis);
  } else if (mode == "allpairs") {   // allpairs cyl|flat W H pairs : all ordered pairs of named roots (battery names) vs reference sums
    int W = atoi(argv[3]), H = atoi(argv[4]); string pairs = argv[5];
    Board b = mkBoard(argv[2], W, H); LK lk(b, mkPawns(b, pairs)); auto B = battery(); auto sg = signatures(lk.g, B);
    map<string, int> name; vector<Game> refg;
    for (size_t k = 0; k < B.size(); k++) { auto s = signatures(B[k].g, B)[B[k].root]; if (!name.count(s)) name[s] = k; }
    int full = (1 << lk.P.size()) - 1; vector<int> nodes, nm;
    for (int x = 0; x < lk.g.n; x++) { if (lk.st[x][0] != full) continue; auto it = name.find(sg[x]); if (it != name.end()) { nodes.push_back(x); nm.push_back(it->second); } }
    Sum S; S.C = {&lk.g, &lk.g}; S.solve();
    // reference sums for each pair of battery games
    map<pair<int,int>, pair<int,int>> refs; long chk = 0, mis = 0;
    for (size_t i = 0; i < nodes.size(); i++) for (size_t j = 0; j < nodes.size(); j++) {
      pair<int,int> key = {nm[i], nm[j]};
      if (!refs.count(key)) { Sum R; R.C = {&B[nm[i]].g, &B[nm[j]].g}; R.solve(); refs[key] = {R.res({B[nm[i]].root, B[nm[j]].root}, 0), R.res({B[nm[i]].root, B[nm[j]].root}, 1)}; }
      auto ref = refs[key]; int a = S.res({nodes[i], nodes[j]}, 0), c = S.res({nodes[i], nodes[j]}, 1); chk++; if (a != ref.first || c != ref.second) mis++;
    }
    printf("ALLPAIRS %s %dx%d %s: roots %d named %zu pairs checked %ld mismatches %ld\n", argv[2], W, H, pairs.c_str(), lk.g.n, nodes.size(), chk, mis);
  }
  return 0;
}
