// Referee (K31 verify) own implementation of the K20 local king game LK, sums and battery B34.
// Written from the definition text in K20/summary.json ("definition") only; does not include lk.cpp, kg.cpp or tempo.cpp.
#pragma once
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <map>
#include <set>
#include <string>
#include <vector>
#include <cmath>
using namespace std;
typedef long long ll;
static const int TP = -1, TM = -2;
struct Game { vector<vector<int>> L, R; int n = 0; int add() { L.emplace_back(); R.emplace_back(); return n++; } };

// ---- K-component sum solver with plies-to-end -----
struct Multi {
  vector<const Game*> C; vector<size_t> mul; size_t NS = 0;
  vector<char> win[2]; vector<int> dep[2];
  bool wantDepth = false;
  vector<int> decode(size_t x) const { vector<int> v(C.size()); for (size_t i = 0; i < C.size(); i++) { v[i] = x % C[i]->n; x /= C[i]->n; } return v; }
  size_t idx(const vector<int>& v, int s) const { size_t x = 0; for (size_t i = 0; i < C.size(); i++) x += mul[i] * v[i]; return x * 2 + s; }
  void solvePlayer(int player) {
    size_t K = C.size();
    mul.assign(K, 1); NS = 1; for (size_t i = 0; i < K; i++) { mul[i] = NS; NS *= C[i]->n; }
    size_t tot = NS * 2; auto& W = win[player]; W.assign(tot, 0);
    auto& D = dep[player]; if (wantDepth) D.assign(tot, 0);
    // reverse edges
    vector<vector<int>> rev[2][8];
    for (int m = 0; m < 2; m++) for (size_t i = 0; i < K; i++) {
      rev[m][i].assign(C[i]->n, {});
      const auto& o = m == 0 ? C[i]->L : C[i]->R;
      for (int a = 0; a < C[i]->n; a++) for (int t : o[a]) if (t >= 0) rev[m][i][t].push_back(a);
    }
    int winT = player == 0 ? TP : TM, loseT = player == 0 ? TM : TP;
    vector<int> cnt(tot, 0);
    vector<size_t> q0, q1, q;
    vector<int> v(K);
    for (size_t x = 0; x < NS; x++) {
      size_t r = x; for (size_t i = 0; i < K; i++) { v[i] = r % C[i]->n; r /= C[i]->n; }
      for (int s = 0; s < 2; s++) {
        size_t id = x * 2 + s;
        const auto* o = &(s == 0 ? C[0]->L : C[0]->R);
        if (s == player) {
          bool hw = false;
          for (size_t i = 0; i < K && !hw; i++) { const auto& oo = s == 0 ? C[i]->L : C[i]->R; for (int t : oo[v[i]]) if (t == winT) { hw = true; break; } }
          if (hw) { W[id] = 1; if (wantDepth) D[id] = 1; q1.push_back(id); }
        } else {
          int c = 0; bool bad = false, anyT = false;
          for (size_t i = 0; i < K; i++) { const auto& oo = s == 0 ? C[i]->L : C[i]->R; for (int t : oo[v[i]]) { if (t == winT) { anyT = true; continue; } c++; if (t == loseT) bad = true; } }
          cnt[id] = bad ? 1000000000 : c;
          if (!bad && c == 0) { W[id] = 1; if (wantDepth) D[id] = anyT ? 1 : 0; (anyT ? q1 : q0).push_back(id); }
        }
        (void)o;
      }
    }
    q = q0; q.insert(q.end(), q1.begin(), q1.end());
    size_t head = 0;
    while (head < q.size()) {
      size_t id = q[head++]; int s = id & 1; size_t x = id >> 1; int m = 1 - s;
      size_t r = x; for (size_t i = 0; i < K; i++) { v[i] = r % C[i]->n; r /= C[i]->n; }
      for (size_t i = 0; i < K; i++) for (int pa : rev[m][i][v[i]]) {
        size_t p = (x - mul[i] * v[i] + mul[i] * pa) * 2 + m;
        if (W[p]) continue;
        if (m == player) { W[p] = 1; if (wantDepth) D[p] = D[id] + 1; q.push_back(p); }
        else if (--cnt[p] == 0) { W[p] = 1; if (wantDepth) D[p] = max(D[id] + 1, 1); q.push_back(p); }
      }
    }
  }
  void solve() { solvePlayer(0); solvePlayer(1); for (size_t i = 0; i < win[0].size(); i++) if (win[0][i] && win[1][i]) { fprintf(stderr, "BOTH WIN\n"); exit(2); } }
  int res(const vector<int>& v, int s) const { size_t i = idx(v, s); return win[0][i] ? 2 : (win[1][i] ? 0 : 1); }  // White's view 0 L 1 D 2 W
  int plies(const vector<int>& v, int s) const { size_t i = idx(v, s); return win[0][i] ? dep[0][i] : (win[1][i] ? dep[1][i] : -1); }
};

// ---- integers ----
struct IntGame { Game g; int N; int node(int k) const { return k + N; } };
static IntGame buildInt(int N) { IntGame I; I.N = N; for (int k = -N; k <= N; k++) I.g.add();
  for (int k = 1; k <= N; k++) I.g.L[k + N].push_back(k - 1 + N);
  for (int k = -1; k >= -N; k--) I.g.R[k + N].push_back(k + 1 + N); return I; }

// ---- battery B34 (standard CGT meanings) ----
struct Named { string name; int start; };
struct Battery { Game g; vector<Named> games; };
static Battery buildBattery() {
  Battery B; Game& g = B.g; auto nd = [&]() { return g.add(); };
  auto L = [&](int x, int t) { g.L[x].push_back(t); }; auto R = [&](int x, int t) { g.R[x].push_back(t); };
  auto reg = [&](string nm, int s) { B.games.push_back({nm, s}); };
  int zero = nd(); reg("0", zero);
  int star = nd(); L(star, zero); R(star, zero); reg("*", star);
  int pos[4], neg[4]; pos[0] = neg[0] = zero;
  for (int i = 1; i <= 3; i++) { pos[i] = nd(); L(pos[i], pos[i-1]); neg[i] = nd(); R(neg[i], neg[i-1]); reg("+" + to_string(i), pos[i]); reg("-" + to_string(i), neg[i]); }
  int half = nd(); L(half, zero); R(half, pos[1]); reg("1/2", half);
  int mhalf = nd(); L(mhalf, neg[1]); R(mhalf, zero); reg("-1/2", mhalf);
  int up = nd(); L(up, zero); R(up, star); reg("up", up);
  int down = nd(); L(down, star); R(down, zero); reg("down", down);
  int ups = nd(); L(ups, zero); L(ups, star); R(ups, zero); reg("up*", ups);
  int dns = nd(); L(dns, zero); R(dns, zero); R(dns, star); reg("down*", dns);
  int s2 = nd(); L(s2, zero); L(s2, star); R(s2, zero); R(s2, star); reg("*2", s2);
  int on = nd(); L(on, on); reg("on", on);
  int off = nd(); R(off, off); reg("off", off);
  int dud = nd(); L(dud, dud); R(dud, dud); reg("dud", dud);
  int over = nd(); L(over, zero); R(over, over); reg("over", over);
  int under = nd(); L(under, under); R(under, zero); reg("under", under);
  int tis = nd(), tisn = nd(); L(tis, tisn); R(tisn, tis); reg("tis", tis); reg("tisn", tisn);
  auto two = [&](string nm, vector<int> l, vector<int> r) { int x = nd(); for (int t : l) L(x, t); for (int t : r) R(x, t); reg(nm, x); };
  two("{+|}", {TP}, {}); two("{|-}", {}, {TM}); two("{+|-}", {TP}, {TM}); two("{+|0}", {TP}, {zero}); two("{0|-}", {zero}, {TM});
  two("{+|on}", {TP}, {on}); two("{off|-}", {off}, {TM}); two("{1|0}", {pos[1]}, {zero}); two("{0|-1}", {zero}, {neg[1]});
  two("{2|0}", {pos[2]}, {zero}); two("{0|-2}", {zero}, {neg[2]}); two("{on|off}", {on}, {off});
  return B;
}

// ---- LK ----
struct LK {
  int W, H; bool cyl; int np = 0, NSQ = 0;
  vector<int> pf, pr, pc;     // pawn file, rank (1-based), colour
  vector<int> nodeOf, raw; Game g;
  int full = 0;
  int fs(int f, int d) const { int x = f + d; if (cyl) return ((x % W) + W) % W; return (x < 0 || x >= W) ? -1 : x; }
  int sq(int f, int r) const { return (r - 1) * W + f; }       // r 1-based
  int fileOf(int s) const { return s % W; } int rankOf(int s) const { return s / W + 1; }
  bool nearF(int a, int b) const { int d = abs(a - b); if (cyl) d = min(d, W - d); return d <= 1; }
  bool adj(int a, int b) const { return nearF(fileOf(a), fileOf(b)) && abs(rankOf(a) - rankOf(b)) <= 1; }
  bool passed(int S, int i) const {
    for (int j = 0; j < np; j++) { if (!(S >> j & 1) || pc[j] == pc[i] || !nearF(pf[i], pf[j])) continue;
      if (pc[i] == 0 && pr[j] > pr[i]) return false; if (pc[i] == 1 && pr[j] < pr[i]) return false; }
    return true; }
  bool attacked(int S, int s, int by) const {
    int f = fileOf(s), r = rankOf(s);
    for (int j = 0; j < np; j++) { if (!(S >> j & 1) || pc[j] != by) continue;
      if (pr[j] + (by == 0 ? 1 : -1) != r) continue;
      for (int d : {-1, 1}) if (fs(pf[j], d) == f) return true; }
    return false; }
  int pawnAt(int S, int s) const { for (int j = 0; j < np; j++) if ((S >> j & 1) && sq(pf[j], pr[j]) == s) return j; return -1; }
  bool legal(int S, int wk, int bk) const {
    if (wk == bk || adj(wk, bk)) return false;
    if (pawnAt(S, wk) >= 0 || pawnAt(S, bk) >= 0) return false;
    if (attacked(S, wk, 1) || attacked(S, bk, 0)) return false;
    return true; }
  ll rid(int S, int wk, int bk) const { return ((ll)S * NSQ + wk) * NSQ + bk; }
  long races = 0;
  // pairs: (file, rank of white pawn); black pawn on rank+1 same file
  void build(int W_, int H_, bool cyl_, const vector<pair<int,int>>& pairs) {
    W = W_; H = H_; cyl = cyl_; NSQ = W * H;
    for (auto& p : pairs) { pf.push_back(p.first); pr.push_back(p.second); pc.push_back(0); pf.push_back(p.first); pr.push_back(p.second + 1); pc.push_back(1); }
    np = pf.size(); full = (1 << np) - 1;
    nodeOf.assign((size_t)(1 << np) * NSQ * NSQ, -1);
    for (int S = 0; S < (1 << np); S++) for (int wk = 0; wk < NSQ; wk++) for (int bk = 0; bk < NSQ; bk++)
      if (legal(S, wk, bk)) { nodeOf[rid(S, wk, bk)] = raw.size(); raw.push_back(rid(S, wk, bk)); }
    for (size_t i = 0; i < raw.size(); i++) g.add();
    for (size_t i = 0; i < raw.size(); i++) {
      ll r = raw[i]; int bk = r % NSQ, wk = (r / NSQ) % NSQ, S = r / NSQ / NSQ;
      for (int col = 0; col < 2; col++) {
        int ks = col == 0 ? wk : bk, os = col == 0 ? bk : wk; int kf = fileOf(ks), kr = rankOf(ks);
        for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
          if (!df && !dr) continue;
          int nf = fs(kf, df), nr = kr + dr; if (nf < 0 || nr < 1 || nr > H) continue;
          int t = sq(nf, nr);
          int pj = pawnAt(S, t);
          if (pj >= 0 && pc[pj] == col) continue;
          if (t == os || adj(t, os)) continue;
          int S2 = S; if (pj >= 0) S2 = S & ~(1 << pj);
          if (attacked(S2, t, 1 - col)) continue;
          auto& opt = col == 0 ? g.L[i] : g.R[i];
          if (pj >= 0) {
            bool pw = false, pb = false;
            for (int j = 0; j < np; j++) if (S2 >> j & 1) { if (passed(S2, j)) (pc[j] == 0 ? pw : pb) = true; }
            if (pw && pb) { races++; }
            if (pw != pb) { opt.push_back(pw ? TP : TM); continue; }
          }
          int nw = col == 0 ? sq(nf, nr) : wk, nb = col == 0 ? bk : sq(nf, nr);
          int nn = nodeOf[rid(S2, nw, nb)];
          if (nn < 0) { fprintf(stderr, "illegal target?\n"); exit(3); }
          opt.push_back(nn);
        }
      }
    }
  }
  vector<int> roots() const { vector<int> r; for (size_t i = 0; i < raw.size(); i++) if (raw[i] / NSQ / NSQ == full) r.push_back(i); return r; }
  string name(int node) const {
    ll r = raw[node]; int bk = r % NSQ, wk = (r / NSQ) % NSQ, S = r / NSQ / NSQ; char b[100];
    string s; snprintf(b, sizeof b, "K%c%d k%c%d", 'a' + fileOf(wk), rankOf(wk), 'a' + fileOf(bk), rankOf(bk)); s = b;
    for (int j = 0; j < np; j++) if (S >> j & 1) { snprintf(b, sizeof b, " %c%c%d", pc[j] == 0 ? 'P' : 'p', 'a' + pf[j], pr[j]); s += b; }
    return s; }
};

// signatures of roots against battery; labels via reference signatures of the battery games themselves
struct Sigs {
  vector<int> roots; vector<string> label; Battery B;
};
static string sigKey(const vector<uint8_t>& s) { return string(s.begin(), s.end()); }
static Sigs classify(const LK& lk) {
  Sigs S; S.B = buildBattery(); S.roots = lk.roots();
  Multi M; M.C = {&lk.g, &S.B.g}; M.solve();
  Multi R; R.C = {&S.B.g, &S.B.g}; R.solve();
  map<string, string> ref;
  for (auto& nm : S.B.games) { vector<uint8_t> s; for (auto& b : S.B.games) for (int t = 0; t < 2; t++) s.push_back(R.res({nm.start, b.start}, t));
    string k = sigKey(s); if (!ref.count(k)) ref[k] = nm.name; else ref[k] += "=" + nm.name; }
  for (int a : S.roots) { vector<uint8_t> s; for (auto& b : S.B.games) for (int t = 0; t < 2; t++) s.push_back(M.res({a, b.start}, t));
    auto it = ref.find(sigKey(s)); string l = it == ref.end() ? "other" : it->second; size_t p = l.find('='); if (p != string::npos) l = l.substr(0, p); S.label.push_back(l); }
  return S;
}
// parse "a3" -> (file, rank)
static vector<pair<int,int>> parsePairs(const string& s) {
  vector<pair<int,int>> v; size_t i = 0;
  while (i < s.size()) { if (s[i] == ',') { i++; continue; } int f = s[i] - 'a'; i++; int r = 0; while (i < s.size() && isdigit(s[i])) r = r * 10 + s[i++] - '0'; v.push_back({f, r}); }
  return v; }

// subgame of full-pawn-set nodes only (closed under moves: captures with no decisive event would leave S, so assert none)
static Game subgameRoots(const LK& lk, vector<int>& nid) {
  vector<int> roots = lk.roots(); nid.assign(lk.g.n, -1); for (size_t k = 0; k < roots.size(); k++) nid[roots[k]] = k;
  Game s; for (size_t k = 0; k < roots.size(); k++) s.add();
  for (size_t k = 0; k < roots.size(); k++) for (int m = 0; m < 2; m++) for (int t : (m == 0 ? lk.g.L : lk.g.R)[roots[k]]) {
    if (t < 0) (m == 0 ? s.L : s.R)[k].push_back(t);
    else if (nid[t] >= 0) (m == 0 ? s.L : s.R)[k].push_back(nid[t]);
    else { fprintf(stderr, "non-decisive capture leaves full set (use full game)\n"); exit(4); } }
  return s; }
