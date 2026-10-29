// Referee 2 (K31 second referee) -- own implementation of the K20 local king game LK, generic sums, battery B34.
// Written from the definition text in K20/summary.json only. Does not include or read mini.h, lk.cpp, kg.cpp, tempo.cpp.
// Build: c++ -O2 -std=c++17 -o bin/lk3 lk3.cpp
#include <algorithm>
#include <array>
#include <climits>
#include <cstdio>
#include <cstdlib>
#include <functional>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
typedef long long ll;
static const int TP = -1, TM = -2;   // terminals: White has won / Black has won
struct Game { vector<vector<int>> L, R; int n = 0; int add() { L.emplace_back(); R.emplace_back(); return n++; } };

struct Board {
  bool cyl; int W, H;
  int sq(int f, int r) const { return r * W + f; }   // r 0-based
  int file(int s) const { return s % W; }
  int rk(int s) const { return s / W; }
  vector<int> nb(int s) const {
    vector<int> v; int f = file(s), r = rk(s);
    for (int dr = -1; dr <= 1; dr++) for (int df = -1; df <= 1; df++) {
      if (!dr && !df) continue; int rr = r + dr; if (rr < 0 || rr >= H) continue;
      int ff = f + df; if (cyl) ff = (ff + W) % W; else if (ff < 0 || ff >= W) continue;
      v.push_back(sq(ff, rr));
    }
    sort(v.begin(), v.end()); v.erase(unique(v.begin(), v.end()), v.end()); return v;
  }
  bool adj(int a, int b) const { for (int t : nb(a)) if (t == b) return true; return false; }
  // squares attacked by a pawn: white pawn at s attacks (f+-1, r+1); black attacks (f+-1, r-1)
  vector<int> att(int s, int color) const {
    vector<int> v; int f = file(s), r = rk(s) + (color == 0 ? 1 : -1); if (r < 0 || r >= H) return v;
    for (int df = -1; df <= 1; df += 2) { int ff = f + df; if (cyl) ff = (ff + W) % W; else if (ff < 0 || ff >= W) continue; v.push_back(sq(ff, r)); }
    return v;
  }
  bool sameOrAdjFile(int f1, int f2) const {
    if (f1 == f2) return true; int d = abs(f1 - f2); if (cyl) d = min(d, W - d); return d <= 1;
  }
};
struct Pawn { int sq, color; };
struct LK {
  Board B; vector<Pawn> P; Game g; vector<array<int, 3>> st; vector<int> idmap; int NSQ; long races = 0;
  int key(int S, int wk, int bk) const { return (S * NSQ + wk) * NSQ + bk; }
  bool attacked(int S, int t, int color_of_king) const {   // t attacked by an enemy pawn in S
    for (size_t i = 0; i < P.size(); i++) if ((S >> i & 1) && P[i].color != color_of_king)
      for (int a : B.att(P[i].sq, P[i].color)) if (a == t) return true;
    return false;
  }
  int pawnAt(int S, int t) const { for (size_t i = 0; i < P.size(); i++) if ((S >> i & 1) && P[i].sq == t) return (int)i; return -1; }
  bool passed(int S, int i) const {
    int f = B.file(P[i].sq), r = B.rk(P[i].sq);
    for (size_t j = 0; j < P.size(); j++) if ((S >> j & 1) && P[j].color != P[i].color) {
      int rj = B.rk(P[j].sq), fj = B.file(P[j].sq);
      bool ahead = P[i].color == 0 ? rj > r : rj < r;
      if (ahead && B.sameOrAdjFile(f, fj)) return false;
    }
    return true;
  }
  bool legal(int S, int wk, int bk) const {
    if (wk == bk || B.adj(wk, bk)) return false;
    if (pawnAt(S, wk) >= 0 || pawnAt(S, bk) >= 0) return false;
    if (attacked(S, wk, 0) || attacked(S, bk, 1)) return false;
    return true;
  }
  // returns option target: node id, or TP/TM; -3 if illegal move
  int step(int S, int wk, int bk, int color, int t, int& S2) const {
    int me = color == 0 ? wk : bk, you = color == 0 ? bk : wk; (void)me;
    int pi = pawnAt(S, t);
    if (pi >= 0 && P[pi].color == color) return -3;                // own pawn
    if (t == you || B.adj(t, you)) return -3;
    S2 = S; if (pi >= 0) S2 = S & ~(1 << pi);
    if (attacked(S2, t, color)) return -3;
    if (pi >= 0) {
      bool wp = false, bp = false;
      for (size_t i = 0; i < P.size(); i++) if (S2 >> i & 1) { if (passed(S2, i)) { if (P[i].color == 0) wp = true; else bp = true; } }
      if (wp && !bp) return TP; if (bp && !wp) return TM;
      if (wp && bp) { return -4; }
    }
    return -5;  // ordinary
  }
  LK(Board b, vector<Pawn> p) : B(b), P(p) {
    NSQ = B.W * B.H; int full = (1 << P.size()) - 1;
    idmap.assign((size_t)(1 << P.size()) * NSQ * NSQ, -1);
    vector<int> q;
    auto get = [&](int S, int wk, int bk) { int& r = idmap[key(S, wk, bk)]; if (r < 0) { r = g.add(); st.push_back({S, wk, bk}); q.push_back(r); } return r; };
    for (int wk = 0; wk < NSQ; wk++) for (int bk = 0; bk < NSQ; bk++) if (legal(full, wk, bk)) get(full, wk, bk);
    for (size_t h = 0; h < q.size(); h++) {
      int id = q[h]; auto [S, wk, bk] = st[id];
      for (int color = 0; color < 2; color++) {
        int me = color == 0 ? wk : bk;
        for (int t : B.nb(me)) {
          int S2; int r = step(S, wk, bk, color, t, S2);
          if (r == -3) continue;
          if (r == -4) { races++; continue; }
          int tgt;
          if (r == TP || r == TM) tgt = r; else tgt = color == 0 ? get(S2, t, bk) : get(S2, wk, t);
          (color == 0 ? g.L : g.R)[id].push_back(tgt);
        }
      }
    }
  }
  int node(int wk, int bk) const { return idmap[key((1 << P.size()) - 1, wk, bk)]; }
};

// ---- generic K-component sum solver -----
struct Sum {
  vector<const Game*> C; int K = 0; vector<size_t> mul; size_t NS = 0; vector<char> win[2];
  void solve() {
    K = C.size(); mul.assign(K, 1); NS = 1; for (int i = 0; i < K; i++) { mul[i] = NS; NS *= C[i]->n; }
    size_t tot = NS * 2;
    vector<vector<vector<int>>> rev(2 * K);
    for (int m = 0; m < 2; m++) for (int i = 0; i < K; i++) {
      auto& rv = rev[m * K + i]; rv.assign(C[i]->n, {});
      const auto& o = m == 0 ? C[i]->L : C[i]->R;
      for (int a = 0; a < C[i]->n; a++) for (int t : o[a]) if (t >= 0) rv[t].push_back(a);
    }
    for (int player = 0; player < 2; player++) {
      auto& Wn = win[player]; Wn.assign(tot, 0);
      int winT = player == 0 ? TP : TM, loseT = player == 0 ? TM : TP;
      vector<int> cnt(tot, 0); vector<size_t> q; vector<int> v(K);
      for (size_t x = 0; x < NS; x++) {
        size_t r = x; for (int i = 0; i < K; i++) { v[i] = r % C[i]->n; r /= C[i]->n; }
        for (int s = 0; s < 2; s++) {
          size_t id = x * 2 + s;
          if (s == player) {
            bool hw = false;
            for (int i = 0; i < K && !hw; i++) for (int t : (s == 0 ? C[i]->L : C[i]->R)[v[i]]) if (t == winT) { hw = true; break; }
            if (hw) { Wn[id] = 1; q.push_back(id); }
          } else {
            int c = 0; bool bad = false;
            for (int i = 0; i < K; i++) for (int t : (s == 0 ? C[i]->L : C[i]->R)[v[i]]) { if (t == winT) continue; c++; if (t == loseT) bad = true; }
            cnt[id] = c;
            if (!bad && c == 0) { Wn[id] = 1; q.push_back(id); }
            if (bad) cnt[id] = INT_MAX / 2;
          }
        }
      }
      for (size_t h = 0; h < q.size(); h++) {
        size_t id = q[h]; int s = id & 1; size_t x = id >> 1; int m = 1 - s;
        size_t r = x; for (int i = 0; i < K; i++) { v[i] = r % C[i]->n; r /= C[i]->n; }
        for (int i = 0; i < K; i++) for (int pa : rev[m * K + i][v[i]]) {
          size_t p = (x - mul[i] * v[i] + mul[i] * pa) * 2 + m;
          if (Wn[p]) continue;
          if (m == player) { Wn[p] = 1; q.push_back(p); }
          else if (--cnt[p] == 0) { Wn[p] = 1; q.push_back(p); }
        }
      }
    }
    for (size_t i = 0; i < tot; i++) if (win[0][i] && win[1][i]) { fprintf(stderr, "BOTH WIN\n"); exit(2); }
  }
  size_t idx(const vector<int>& v, int s) const { size_t x = 0; for (int i = 0; i < K; i++) x += mul[i] * v[i]; return x * 2 + s; }
  int res(const vector<int>& v, int s) const { size_t i = idx(v, s); return win[0][i] ? 2 : (win[1][i] ? 0 : 1); }
};

// ---- reference games ----
static Game intGame(int N) { Game g; for (int k = -N; k <= N; k++) g.add(); for (int k = 1; k <= N; k++) g.L[k + N].push_back(k - 1 + N); for (int k = -1; k >= -N; k--) g.R[k + N].push_back(k + 1 + N); return g; }
struct Named { string name; Game g; int root; };
static vector<Named> battery() {
  vector<Named> B;
  auto mk = [&](string nm, function<int(Game&)> f) { Named x; x.name = nm; x.root = f(x.g); B.push_back(x); };
  mk("0", [](Game& g) { return g.add(); });
  mk("*", [](Game& g) { int z = g.add(), a = g.add(); g.L[a].push_back(z); g.R[a].push_back(z); return a; });
  for (int k : {1, 2, 3}) for (int sg : {1, -1}) { string nm = (sg > 0 ? "+" : "-") + to_string(k);
    mk(nm, [&](Game& g) { Game I = intGame(k); g = I; return sg * k + k; }); }
  mk("1/2", [](Game& g) { int z = g.add(), o = g.add(), h = g.add(); g.L[o].push_back(z); g.L[h].push_back(z); g.R[h].push_back(o); return h; });
  mk("-1/2", [](Game& g) { int z = g.add(), o = g.add(), h = g.add(); g.R[o].push_back(z); g.L[h].push_back(o); g.R[h].push_back(z); return h; });
  auto starbase = [](Game& g, int& z, int& s) { z = g.add(); s = g.add(); g.L[s].push_back(z); g.R[s].push_back(z); };
  mk("up", [&](Game& g) { int z, s; starbase(g, z, s); int u = g.add(); g.L[u].push_back(z); g.R[u].push_back(s); return u; });
  mk("down", [&](Game& g) { int z, s; starbase(g, z, s); int u = g.add(); g.L[u].push_back(s); g.R[u].push_back(z); return u; });
  mk("up*", [&](Game& g) { int z, s; starbase(g, z, s); int u = g.add(); g.L[u].push_back(z); g.L[u].push_back(s); g.R[u].push_back(z); return u; });
  mk("down*", [&](Game& g) { int z, s; starbase(g, z, s); int u = g.add(); g.L[u].push_back(z); g.R[u].push_back(z); g.R[u].push_back(s); return u; });
  mk("*2", [&](Game& g) { int z, s; starbase(g, z, s); int u = g.add(); g.L[u] = {z, s}; g.R[u] = {z, s}; return u; });
  mk("on", [](Game& g) { int o = g.add(); g.L[o].push_back(o); return o; });
  mk("off", [](Game& g) { int o = g.add(); g.R[o].push_back(o); return o; });
  mk("dud", [](Game& g) { int o = g.add(); g.L[o].push_back(o); g.R[o].push_back(o); return o; });
  mk("over", [](Game& g) { int z = g.add(), o = g.add(); g.L[o].push_back(z); g.R[o].push_back(o); return o; });
  mk("under", [](Game& g) { int z = g.add(), o = g.add(); g.L[o].push_back(o); g.R[o].push_back(z); return o; });
  mk("tis", [](Game& g) { int t = g.add(), n = g.add(); g.L[t].push_back(n); g.R[n].push_back(t); return t; });
  mk("tisn", [](Game& g) { int t = g.add(), n = g.add(); g.L[t].push_back(n); g.R[n].push_back(t); return n; });
  mk("{+|}", [](Game& g) { int a = g.add(); g.L[a].push_back(TP); return a; });
  mk("{|-}", [](Game& g) { int a = g.add(); g.R[a].push_back(TM); return a; });
  mk("{+|-}", [](Game& g) { int a = g.add(); g.L[a].push_back(TP); g.R[a].push_back(TM); return a; });
  mk("{+|0}", [](Game& g) { int z = g.add(), a = g.add(); g.L[a].push_back(TP); g.R[a].push_back(z); return a; });
  mk("{0|-}", [](Game& g) { int z = g.add(), a = g.add(); g.L[a].push_back(z); g.R[a].push_back(TM); return a; });
  mk("{+|on}", [](Game& g) { int o = g.add(), a = g.add(); g.L[o].push_back(o); g.L[a].push_back(TP); g.R[a].push_back(o); return a; });
  mk("{off|-}", [](Game& g) { int o = g.add(), a = g.add(); g.R[o].push_back(o); g.L[a].push_back(o); g.R[a].push_back(TM); return a; });
  mk("{1|0}", [](Game& g) { Game I = intGame(1); g = I; int a = g.add(); g.L[a].push_back(1 + 1); g.R[a].push_back(0 + 1); return a; });
  mk("{0|-1}", [](Game& g) { Game I = intGame(1); g = I; int a = g.add(); g.L[a].push_back(0 + 1); g.R[a].push_back(-1 + 1); return a; });
  mk("{2|0}", [](Game& g) { Game I = intGame(2); g = I; int a = g.add(); g.L[a].push_back(2 + 2); g.R[a].push_back(0 + 2); return a; });
  mk("{0|-2}", [](Game& g) { Game I = intGame(2); g = I; int a = g.add(); g.L[a].push_back(0 + 2); g.R[a].push_back(-2 + 2); return a; });
  mk("{on|off}", [](Game& g) { int on = g.add(), off = g.add(), a = g.add(); g.L[on].push_back(on); g.R[off].push_back(off); g.L[a].push_back(on); g.R[a].push_back(off); return a; });
  return B;
}
// signature of every node of A against the battery: string of 2*34 digits
static vector<string> signatures(const Game& A, const vector<Named>& B) {
  vector<string> sig(A.n);
  for (auto& k : B) {
    Sum S; S.C = {&A, &k.g}; S.solve();
    for (int x = 0; x < A.n; x++) { vector<int> v = {x, k.root}; sig[x] += char('0' + S.res(v, 0)); sig[x] += char('0' + S.res(v, 1)); }
  }
  return sig;
}
static Board mkBoard(string bd, int W, int H) { Board b; b.cyl = bd == "cyl"; b.W = W; b.H = H; return b; }
static vector<Pawn> mkPawns(const Board& b, string pairs) {  // pairs "a3,c4" ; file letter, white pawn rank
  vector<Pawn> P; stringstream ss(pairs); string tok;
  while (getline(ss, tok, ',')) { int f = tok[0] - 'a', r = atoi(tok.c_str() + 1); P.push_back({b.sq(f, r - 1), 0}); P.push_back({b.sq(f, r), 1}); }
  return P;
}
static string sqname(const Board& b, int s) { return string(1, 'a' + b.file(s)) + to_string(b.rk(s) + 1); }

int main(int argc, char** argv) {
  string mode = argv[1];
  if (mode == "cls") {   // cls cyl|flat W H pairs [dump]
    int W = atoi(argv[3]), H = atoi(argv[4]); string pairs = argv[5]; bool dump = argc > 6;
    Board b = mkBoard(argv[2], W, H); LK lk(b, mkPawns(b, pairs));
    auto B = battery(); auto sigR = signatures(lk.g, B);
    // reference signatures: of the games themselves (use root node of each, as part of a game with all battery games)
    map<string, string> name;
    for (auto& k : B) { vector<Named> single = {}; Game A = k.g; auto s = signatures(A, B); name[s[k.root]] = k.name; }
    map<string, int> cnt; int p1 = 0, m1 = 0, unnamed = 0; long off = 0, even = 0, tot1 = 0;
    for (int x = 0; x < lk.g.n; x++) {
      if (lk.st[x][0] != (1 << lk.P.size()) - 1) continue;
      auto it = name.find(sigR[x]); string nm = it == name.end() ? "?" : it->second; cnt[nm]++;
      if (dump && string(argv[6]) == "all") printf("NAME K%s k%s %s\n", sqname(b, lk.st[x][1]).c_str(), sqname(b, lk.st[x][2]).c_str(), nm.c_str());
      if (nm == "+1" || nm == "-1") {
        (nm == "+1" ? p1 : m1)++; tot1++;
        int wk = lk.st[x][1], bk = lk.st[x][2];
        bool onfile = b.file(wk) * 2 == W && b.file(bk) * 2 == W; if (!onfile) off++;
        if ((b.rk(wk) - b.rk(bk)) % 2 != 0) even++;
        if (dump) printf("ROOT %s %d %d %s %s K%s k%s\n", argv[2], W, H, pairs.c_str(), nm.c_str(), sqname(b, wk).c_str(), sqname(b, bk).c_str());
      }
    }
    int roots = 0; for (auto& kv : cnt) roots += kv.second;
    printf("CLS %s %dx%d %s roots %d p1 %d m1 %d notW/2 %ld oddrankdiff %ld races %ld |", argv[2], W, H, pairs.c_str(), roots, p1, m1, off, even, lk.races);
    for (auto& kv : cnt) printf(" %s=%d", kv.first.c_str(), kv.second); printf("\n");
    (void)unnamed;
  } else if (mode == "flat1") {  // flat1 W H : all single pairs on all files, ranks 2..H-2, count +-1 roots
    int W = atoi(argv[2]), H = atoi(argv[3]); Board b = mkBoard("flat", W, H); auto B = battery();
    Game one = intGame(2); auto sone = signatures(one, B); string s1 = sone[1 + 2], sm = sone[-1 + 2];
    int cases = 0, bad = 0; long roots = 0;
    for (int f = 0; f < W; f++) for (int r = 2; r <= H - 2; r++) {
      string pr = string(1, 'a' + f) + to_string(r); LK lk(b, mkPawns(b, pr)); auto sg = signatures(lk.g, B); cases++;
      int c = 0; for (int x = 0; x < lk.g.n; x++) { if (sg[x] == s1 || sg[x] == sm) c++; } roots += lk.g.n; if (c) { bad++; printf("FLAT +-1 found %dx%d %s: %d\n", W, H, pr.c_str(), c); }
    }
    printf("FLAT1 %dx%d cases %d with_pm1 %d roots %ld\n", W, H, cases, bad, roots);
  }
  return 0;
}
