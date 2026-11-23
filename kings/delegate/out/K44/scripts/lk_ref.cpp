// Referee's own implementation of the K20 local king game LK, written from the definition text only.
// Build: c++ -O2 -std=c++17 -o lk lk.cpp
// Usage:
//   lk classify <board> <pairs> <margin|free> [dump=<class>] [ext=<n>]
//   lk root <board> <pairs> <margin|free> "<root text>" [ext]
//   lk sums <board> <pairs> <margin|free> <nsamples> <seed>
// board: flat:6x6 or cyl:6x6 ; pairs: "a2,c4" (white pawn square; black pawn one rank above), "" or "none"
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <set>
#include <string>
#include <vector>
using namespace std;

static const int TP = -1, TM = -2;  // terminal: White has won / Black has won
struct Game {
  int n = 0;
  vector<vector<int>> L, R;
  int add() { L.emplace_back(); R.emplace_back(); return n++; }
};

// ---------------- sum solver ----------------
// outcome: bit0 = White to move result (0 L,1 D,2 W) packed in two arrays
struct SumRes { int nA, nB; vector<uint8_t> w; /* index (a*nB+b)*2+s : 0 L, 1 D, 2 W (White's view) */ };

static void solvePlayer(const Game& A, const Game& B, int player /*0 White,1 Black*/, vector<char>& win) {
  // win[(a*nB+b)*2+s] = player can force a win in finitely many moves with s to move.
  int nA = A.n, nB = B.n;
  size_t NS = (size_t)nA * nB * 2;
  win.assign(NS, 0);
  const vector<vector<int>>& dummy = A.L;
  (void)dummy;
  // option lists by mover
  auto opt = [&](const Game& G, int mover) -> const vector<vector<int>>& { return mover == 0 ? G.L : G.R; };
  // reverse lists: rev[mover][target] = list of sources
  vector<vector<int>> revA[2], revB[2];
  for (int m = 0; m < 2; m++) {
    revA[m].assign(nA, {});
    revB[m].assign(nB, {});
    for (int a = 0; a < nA; a++) for (int t : opt(A, m)[a]) if (t >= 0) revA[m][t].push_back(a);
    for (int b = 0; b < nB; b++) for (int t : opt(B, m)[b]) if (t >= 0) revB[m][t].push_back(b);
  }
  int winT = (player == 0) ? TP : TM;   // terminal that means player wins
  int loseT = (player == 0) ? TM : TP;
  vector<int> cnt(NS, 0);
  vector<size_t> q;
  q.reserve(NS / 4);
  auto id = [&](int a, int b, int s) { return ((size_t)a * nB + b) * 2 + s; };
  for (int a = 0; a < nA; a++)
    for (int b = 0; b < nB; b++)
      for (int s = 0; s < 2; s++) {
        size_t x = id(a, b, s);
        const vector<int>& oa = opt(A, s)[a];
        const vector<int>& ob = opt(B, s)[b];
        if (s == player) {
          bool hasWin = false;
          for (int t : oa) if (t == winT) hasWin = true;
          for (int t : ob) if (t == winT) hasWin = true;
          if (hasWin) { win[x] = 1; q.push_back(x); }
        } else {
          // opponent to move: player wins iff all options are winT or lead to player-wins
          int c = 0; bool bad = false;
          for (int t : oa) { if (t == winT) continue; c++; if (t == loseT) bad = true; }
          for (int t : ob) { if (t == winT) continue; c++; if (t == loseT) bad = true; }
          cnt[x] = bad ? 1000000 : c;
          if (!bad && c == 0) { win[x] = 1; q.push_back(x); }
        }
      }
  size_t head = 0;
  while (head < q.size()) {
    size_t x = q[head++];
    int s = x & 1; size_t ab = x >> 1; int a = ab / nB, b = ab % nB;
    // x has side s to move and is player-win. predecessors have mover m = 1-s, moving to x.
    int m = 1 - s;
    for (int pa : revA[m][a]) {
      size_t p = id(pa, b, m);
      if (win[p]) continue;
      if (m == player) { win[p] = 1; q.push_back(p); }
      else if (--cnt[p] == 0) { win[p] = 1; q.push_back(p); }
    }
    for (int pb : revB[m][b]) {
      size_t p = id(a, pb, m);
      if (win[p]) continue;
      if (m == player) { win[p] = 1; q.push_back(p); }
      else if (--cnt[p] == 0) { win[p] = 1; q.push_back(p); }
    }
  }
}

static SumRes solveSum(const Game& A, const Game& B) {
  vector<char> ww, bb;
  solvePlayer(A, B, 0, ww);
  solvePlayer(A, B, 1, bb);
  SumRes r; r.nA = A.n; r.nB = B.n; r.w.assign(ww.size(), 1);
  for (size_t i = 0; i < ww.size(); i++) {
    if (ww[i] && bb[i]) { fprintf(stderr, "BOTH WIN?!\n"); exit(2); }
    r.w[i] = ww[i] ? 2 : (bb[i] ? 0 : 1);
  }
  return r;
}

// ---------------- battery ----------------
struct Named { string name; int start; };
struct Battery { Game g; vector<Named> games; };

struct Builder {
  Battery bt;
  map<string, int> idx;
  int node() { return bt.g.add(); }
  // add game with explicit nodes: returns start
  int zero() { static int z = -1; (void)z; return -1; }
};

// Build the standard battery B (own definitions, standard CGT meanings).
static Battery buildBattery() {
  Battery bt; Game& g = bt.g;
  auto nd = [&]() { return g.add(); };
  auto L = [&](int x, int t) { g.L[x].push_back(t); };
  auto R = [&](int x, int t) { g.R[x].push_back(t); };
  auto reg = [&](const string& nm, int s) { bt.games.push_back({nm, s}); };
  int zero = nd(); reg("0", zero);
  int star = nd(); L(star, zero); R(star, zero); reg("*", star);
  // integers
  vector<int> pos(4), neg(4); pos[0] = zero; neg[0] = zero;
  for (int i = 1; i <= 3; i++) {
    pos[i] = nd(); L(pos[i], pos[i - 1]);
    neg[i] = nd(); R(neg[i], neg[i - 1]);
    reg("+" + to_string(i), pos[i]); reg("-" + to_string(i), neg[i]);
  }
  int half = nd(); L(half, zero); R(half, pos[1]); reg("1/2", half);
  int mhalf = nd(); L(mhalf, neg[1]); R(mhalf, zero); reg("-1/2", mhalf);
  int up = nd(); L(up, zero); R(up, star); reg("up", up);
  int down = nd(); L(down, star); R(down, zero); reg("down", down);
  int upstar = nd(); L(upstar, zero); L(upstar, star); R(upstar, zero); reg("up*", upstar);
  int downstar = nd(); L(downstar, zero); R(downstar, zero); R(downstar, star); reg("down*", downstar);
  int star2 = nd(); L(star2, zero); L(star2, star); R(star2, zero); R(star2, star); reg("*2", star2);
  int on = nd(); L(on, on); reg("on", on);
  int off = nd(); R(off, off); reg("off", off);
  int dud = nd(); L(dud, dud); R(dud, dud); reg("dud", dud);
  int over = nd(); L(over, zero); R(over, over); reg("over", over);
  int under = nd(); L(under, under); R(under, zero); reg("under", under);
  int tis = nd(), tisn = nd(); L(tis, tisn); R(tisn, tis); reg("tis", tis); reg("tisn", tisn);
  auto two = [&](const string& nm, vector<int> l, vector<int> r) {
    int x = nd(); for (int t : l) L(x, t); for (int t : r) R(x, t); reg(nm, x); return x; };
  two("{+|}", {TP}, {});
  two("{|-}", {}, {TM});
  two("{+|-}", {TP}, {TM});
  two("{+|0}", {TP}, {zero});
  two("{0|-}", {zero}, {TM});
  two("{+|on}", {TP}, {on});
  two("{off|-}", {off}, {TM});
  two("{1|0}", {pos[1]}, {zero});
  two("{0|-1}", {zero}, {neg[1]});
  two("{2|0}", {pos[2]}, {zero});
  two("{0|-2}", {zero}, {neg[2]});
  two("{on|off}", {on}, {off});
  return bt;
}

// Extended battery (own design): games {A|B}, A,B subsets of size<=2 of atoms; each as separate component.
static void buildExt(vector<Battery>& chunks, int chunkSize) {
  // atoms: nodes in a shared base graph
  Game base; vector<pair<string, int>> atoms;
  auto nd = [&]() { return base.add(); };
  int zero = nd(); int star = nd(); base.L[star].push_back(zero); base.R[star].push_back(zero);
  int p1 = nd(); base.L[p1].push_back(zero);
  int m1 = nd(); base.R[m1].push_back(zero);
  int p2 = nd(); base.L[p2].push_back(p1);
  int m2 = nd(); base.R[m2].push_back(m1);
  int on = nd(); base.L[on].push_back(on);
  int off = nd(); base.R[off].push_back(off);
  int dud = nd(); base.L[dud].push_back(dud); base.R[dud].push_back(dud);
  int tis = nd(), tisn = nd(); base.L[tis].push_back(tisn); base.R[tisn].push_back(tis);
  int up = nd(); base.L[up].push_back(zero); base.R[up].push_back(star);
  int down = nd(); base.L[down].push_back(star); base.R[down].push_back(zero);
  int half = nd(); base.L[half].push_back(zero); base.R[half].push_back(p1);
  int over = nd(); base.L[over].push_back(zero); base.R[over].push_back(over);
  atoms = {{"+", TP}, {"-", TM}, {"0", zero}, {"*", star}, {"1", p1}, {"-1", m1}, {"2", p2}, {"-2", m2}, {"on", on}, {"off", off}, {"dud", dud},
           {"tis", tis}, {"tisn", tisn}, {"up", up}, {"down", down}, {"1/2", half}, {"over", over}};
  int na = atoms.size();
  vector<vector<int>> subs;  // subsets of size<=2 as index lists
  subs.push_back({});
  for (int i = 0; i < na; i++) subs.push_back({i});
  for (int i = 0; i < na; i++) for (int j = i + 1; j < na; j++) subs.push_back({i, j});
  auto sname = [&](const vector<int>& s) { string r; for (size_t k = 0; k < s.size(); k++) { if (k) r += ","; r += atoms[s[k]].first; } return r; };
  Battery cur; cur.g = base;
  for (auto& A : subs) for (auto& B : subs) {
    int x = cur.g.add();
    for (int i : A) cur.g.L[x].push_back(atoms[i].second);
    for (int i : B) cur.g.R[x].push_back(atoms[i].second);
    cur.games.push_back({"{" + sname(A) + "|" + sname(B) + "}", x});
    if ((int)cur.games.size() >= chunkSize) { chunks.push_back(cur); cur = Battery(); cur.g = base; }
  }
  if (!cur.games.empty()) chunks.push_back(cur);
}


// Battery of the K20 description: B64 = {A|B}, A,B subsets of {+,-,0}; all {x|y}, x,y in {none,+,-,B64}; plus B34 games.
static void buildExt2(vector<Battery>& chunks, int chunkSize) {
  Game base; int zero = base.add();
  vector<int> t = {TP, TM, zero};
  vector<int> b64;
  for (int a = 0; a < 8; a++) for (int b = 0; b < 8; b++) {
    int x = base.add();
    for (int i = 0; i < 3; i++) { if (a >> i & 1) base.L[x].push_back(t[i]); if (b >> i & 1) base.R[x].push_back(t[i]); }
    b64.push_back(x);
  }
  vector<int> opts = {-100}; opts.push_back(TP); opts.push_back(TM); for (int x : b64) opts.push_back(x);
  Battery cur; cur.g = base;
  for (size_t i = 0; i < b64.size(); i++) cur.games.push_back({"B64#" + to_string(i), b64[i]});
  for (int l : opts) for (int r : opts) {
    int x = cur.g.add();
    if (l != -100) cur.g.L[x].push_back(l);
    if (r != -100) cur.g.R[x].push_back(r);
    cur.games.push_back({"{" + to_string(l) + "|" + to_string(r) + "}", x});
    if ((int)cur.games.size() >= chunkSize) { chunks.push_back(cur); cur = Battery(); cur.g = base; }
  }
  if (!cur.games.empty()) chunks.push_back(cur);
}

// ---------------- LK ----------------
struct Cfg {
  int W, H; bool cyl;
  vector<pair<int, int>> pairs;  // white pawn (file, rank0)
  int margin; int flo = -1, fhi = -1;                   // -1 free
};
struct LK {
  Cfg c; int NSQ, np;
  vector<int> pf, pr, pcol;  // pawns: file, rank, colour (0 white,1 black)
  vector<int> nodeOf;        // dense index from raw id, -1 if illegal
  vector<int> raw;           // raw id of dense node
  Game g;
  vector<char> inRegion;
  long races = 0; vector<char> raceNode;
  int fileStep(int f, int d) const { int x = f + d; if (c.cyl) return ((x % c.W) + c.W) % c.W; return (x < 0 || x >= c.W) ? -1 : x; }
  int sq(int f, int r) const { return r * c.W + f; }
  bool adj(int a, int b) const {
    int fa = a % c.W, ra = a / c.W, fb = b % c.W, rb = b / c.W;
    int df = abs(fa - fb); if (c.cyl) df = min(df, c.W - df);
    return df <= 1 && abs(ra - rb) <= 1;
  }
  bool nearFile(int f1, int f2) const { int df = abs(f1 - f2); if (c.cyl) df = min(df, c.W - df); return df <= 1; }
  bool passedP(int S, int i) const {  // pawn i in S passed?
    for (int j = 0; j < np; j++) {
      if (!(S >> j & 1) || pcol[j] == pcol[i]) continue;
      if (!nearFile(pf[i], pf[j])) continue;
      if (pcol[i] == 0 && pr[j] > pr[i]) return false;
      if (pcol[i] == 1 && pr[j] < pr[i]) return false;
    }
    return true;
  }
  bool attacked(int S, int s, int byColour) const {  // square s attacked by a pawn of colour byColour in S
    int f = s % c.W, r = s / c.W;
    for (int j = 0; j < np; j++) {
      if (!(S >> j & 1) || pcol[j] != byColour) continue;
      int tr = pr[j] + (byColour == 0 ? 1 : -1);
      if (tr != r) continue;
      for (int d = -1; d <= 1; d += 2) if (fileStep(pf[j], d) == f) return true;
    }
    return false;
  }
  int pawnAt(int S, int s) const {
    for (int j = 0; j < np; j++) if ((S >> j & 1) && sq(pf[j], pr[j]) == s) return j;
    return -1;
  }
  long rawId(int S, int wk, int bk) const { return ((long)S * NSQ + wk) * NSQ + bk; }
  bool legal(int S, int wk, int bk) const {
    if (!inRegion[wk] || !inRegion[bk]) return false;
    if (wk == bk || adj(wk, bk)) return false;
    if (pawnAt(S, wk) >= 0 || pawnAt(S, bk) >= 0) return false;
    if (attacked(S, wk, 1) || attacked(S, bk, 0)) return false;
    return true;
  }
  void build(const Cfg& cf) {
    c = cf; NSQ = c.W * c.H; np = 0;
    for (auto& p : c.pairs) {
      pf.push_back(p.first); pr.push_back(p.second); pcol.push_back(0);
      pf.push_back(p.first); pr.push_back(p.second + 1); pcol.push_back(1);
    }
    np = pf.size();
    inRegion.assign(NSQ, 1);
    if (c.margin >= 0 && c.flo >= 0) { for (int sq2 = 0; sq2 < NSQ; sq2++) inRegion[sq2] = (sq2 % c.W >= c.flo && sq2 % c.W <= c.fhi); }
    else if (c.margin >= 0 && np > 0) {
      set<int> files; for (int f : pf) files.insert(f);
      vector<char> ok(c.W, 0);
      if (!c.cyl) {
        int lo = *files.begin(), hi = *files.rbegin();
        for (int f = max(0, lo - c.margin); f <= min(c.W - 1, hi + c.margin); f++) ok[f] = 1;
      } else {
        // smallest arc covering files: choose the largest gap between consecutive files
        vector<int> fl(files.begin(), files.end());
        int best = -1, bi = 0;
        for (size_t i = 0; i < fl.size(); i++) {
          int nx = fl[(i + 1) % fl.size()]; int gap = ((nx - fl[i]) % c.W + c.W) % c.W; if (fl.size() == 1) gap = c.W;
          if (gap > best) { best = gap; bi = i; }
        }
        int start = fl[(bi + 1) % fl.size()]; int len = c.W - best + 1; if (fl.size() == 1) len = 1;
        len += 2 * c.margin; if (len >= c.W) { for (int f = 0; f < c.W; f++) ok[f] = 1; }
        else for (int k = -c.margin; k < len - c.margin; k++) ok[((start + k) % c.W + c.W) % c.W] = 1;
      }
      for (int s = 0; s < NSQ; s++) inRegion[s] = ok[s % c.W];
    }
    int nS = 1 << np;
    nodeOf.assign((size_t)nS * NSQ * NSQ, -1);
    for (int S = 0; S < nS; S++) for (int wk = 0; wk < NSQ; wk++) for (int bk = 0; bk < NSQ; bk++)
      if (legal(S, wk, bk)) { nodeOf[rawId(S, wk, bk)] = raw.size(); raw.push_back(rawId(S, wk, bk)); }
    for (size_t i = 0; i < raw.size(); i++) g.add();
    raceNode.assign(raw.size(), 0);
    for (size_t i = 0; i < raw.size(); i++) {
      long r = raw[i]; int bk = r % NSQ; int wk = (r / NSQ) % NSQ; int S = r / NSQ / NSQ;
      for (int col = 0; col < 2; col++) {
        int ks = col == 0 ? wk : bk, os = col == 0 ? bk : wk;
        int kf = ks % c.W, kr = ks / c.W;
        for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
          if (!df && !dr) continue;
          int nf = fileStep(kf, df), nr = kr + dr;
          if (nf < 0 || nr < 0 || nr >= c.H) continue;
          int t = sq(nf, nr);
          if (!inRegion[t]) continue;
          int pj = pawnAt(S, t);
          if (pj >= 0 && pcol[pj] == col) continue;
          if (adj(t, os) || t == os) continue;
          int S2 = S; bool cap = false;
          if (pj >= 0) { S2 = S & ~(1 << pj); cap = true; }
          if (attacked(S2, t, 1 - col)) continue;
          vector<int>& out = (col == 0 ? g.L : g.R)[i];
          if (cap) {
            bool wp = false, bp = false;
            for (int j = 0; j < np; j++) if (S2 >> j & 1) { if (passedP(S2, j)) { if (pcol[j] == 0) wp = true; else bp = true; } }
            if (wp && bp) { raceNode[i] = 1; /* treat as race: not needed */ out.push_back(col == 0 ? TP : TM); continue; }
            if (wp) { out.push_back(TP); continue; }
            if (bp) { out.push_back(TM); continue; }
          }
          int nw = col == 0 ? t : wk, nb = col == 0 ? bk : t;
          int id = nodeOf[rawId(S2, nw, nb)];
          if (id < 0) { fprintf(stderr, "illegal target?!\n"); exit(3); }
          out.push_back(id);
        }
      }
    }
  }
  string name(int sqr) const { string s; s += char('a' + sqr % c.W); s += to_string(sqr / c.W + 1); return s; }
  string rootText(int node) const {
    long r = raw[node]; int bk = r % NSQ; int wk = (r / NSQ) % NSQ; int S = r / NSQ / NSQ;
    string s = "K" + name(wk) + " k" + name(bk);
    for (int j = 0; j < np; j++) if (S >> j & 1) s += string(" ") + (pcol[j] == 0 ? "P" : "p") + name(sq(pf[j], pr[j]));
    return s;
  }
  int parseRoot(const string& t) const {
    int S = 0, wk = -1, bk = -1;
    size_t i = 0;
    while (i < t.size()) {
      while (i < t.size() && t[i] == ' ') i++;
      if (i >= t.size()) break;
      char ch = t[i]; int f = t[i + 1] - 'a'; int r = atoi(t.c_str() + i + 2) - 1; i += 2; while (i < t.size() && isdigit(t[i])) i++;
      if (ch == 'K') wk = sq(f, r); else if (ch == 'k') bk = sq(f, r);
      else { for (int j = 0; j < np; j++) if (sq(pf[j], pr[j]) == sq(f, r) && pcol[j] == (ch == 'P' ? 0 : 1)) S |= 1 << j; }
    }
    return nodeOf[rawId(S, wk, bk)];
  }
  int fullS() const { return (1 << np) - 1; }
  vector<int> roots() const {
    vector<int> r; for (size_t i = 0; i < raw.size(); i++) if ((int)(raw[i] / NSQ / NSQ) == fullS()) r.push_back(i); return r;
  }
};


// subgame reachable from a set of roots; map[root] -> new id
static Game subgame(const Game& g, const vector<int>& roots, vector<int>& newid) {
  newid.assign(g.n, -1); vector<int> order; vector<int> st;
  for (int r : roots) if (newid[r] < 0) { newid[r] = order.size(); order.push_back(r); st.push_back(r); }
  while (!st.empty()) { int x = st.back(); st.pop_back();
    for (int m = 0; m < 2; m++) for (int t : (m ? g.R : g.L)[x]) if (t >= 0 && newid[t] < 0) { newid[t] = order.size(); order.push_back(t); st.push_back(t); } }
  Game h; for (size_t i = 0; i < order.size(); i++) h.add();
  for (size_t i = 0; i < order.size(); i++) { int x = order[i];
    for (int t : g.L[x]) h.L[i].push_back(t >= 0 ? newid[t] : t);
    for (int t : g.R[x]) h.R[i].push_back(t >= 0 ? newid[t] : t); }
  return h;
}


static vector<char> shortNodes(const Game& g) {
  int n = g.n; vector<int> deg(n, 0); vector<vector<int>> rev(n);
  for (int x = 0; x < n; x++) for (int m = 0; m < 2; m++) for (int t : (m ? g.R : g.L)[x]) if (t >= 0) { deg[x]++; rev[t].push_back(x); }
  vector<char> sh(n, 0); vector<int> q;
  for (int x = 0; x < n; x++) if (deg[x] == 0) { sh[x] = 1; q.push_back(x); }
  size_t h = 0; while (h < q.size()) { int x = q[h++]; for (int p : rev[x]) if (--deg[p] == 0 && !sh[p]) { sh[p] = 1; q.push_back(p); } }
  return sh;
}

static Cfg parseCfg(const string& board, const string& pairs, const string& margin) {
  Cfg c; c.cyl = board.substr(0, 3) == "cyl"; size_t x = board.find('x');
  c.W = atoi(board.c_str() + board.find(':') + 1); c.H = atoi(board.c_str() + x + 1);
  if (pairs != "none" && pairs != "") {
    size_t i = 0;
    while (i < pairs.size()) {
      size_t j = pairs.find(',', i); if (j == string::npos) j = pairs.size();
      string p = pairs.substr(i, j - i); c.pairs.push_back({p[0] - 'a', atoi(p.c_str() + 1) - 1}); i = j + 1;
    }
  }
  c.margin = margin == "free" ? -1 : atoi(margin.c_str());
  c.flo = -1; c.fhi = -1;
  if (margin.size() > 1 && margin[0] == 'F') { sscanf(margin.c_str() + 1, "%d-%d", &c.flo, &c.fhi); c.margin = 0; }
  return c;
}

// signature of every root against a battery: returns for each root a vector<uint8_t> of outcomes (2 per game)
static void signatures(const LK& lk, const Battery& bt, const vector<int>& roots, vector<vector<uint8_t>>& sig) {
  SumRes sr = solveSum(lk.g, bt.g);
  for (size_t k = 0; k < roots.size(); k++) {
    for (auto& nm : bt.games) {
      size_t id = ((size_t)roots[k] * sr.nB + nm.start) * 2;
      sig[k].push_back(sr.w[id]); sig[k].push_back(sr.w[id + 1]);
    }
  }
}
static vector<uint8_t> refSig(const Game& H, int hstart, const Battery& bt) {
  SumRes sr = solveSum(H, bt.g);
  vector<uint8_t> s;
  for (auto& nm : bt.games) { size_t id = ((size_t)hstart * sr.nB + nm.start) * 2; s.push_back(sr.w[id]); s.push_back(sr.w[id + 1]); }
  return s;
}

int main(int argc, char** argv) {
  if (argc < 5) { fprintf(stderr, "usage\n"); return 1; }
  string mode = argv[1];
  Cfg cf = parseCfg(argv[2], argv[3], argv[4]);
  LK lk; lk.build(cf);
  {
    vector<int> rs = lk.roots(); vector<char> seen(lk.raw.size(), 0); vector<int> st = rs; for (int r : rs) seen[r] = 1;
    while (!st.empty()) { int x = st.back(); st.pop_back(); if (lk.raceNode[x]) lk.races++;
      for (int m = 0; m < 2; m++) for (int t : (m ? lk.g.R : lk.g.L)[x]) if (t >= 0 && !seen[t]) { seen[t] = 1; st.push_back(t); } }
  }
  Battery B = buildBattery();
  if (mode == "classify") {
    string dump; int ext = 0;
    for (int i = 5; i < argc; i++) { string a = argv[i]; if (a.rfind("dump=", 0) == 0) dump = a.substr(5); if (a.rfind("ext=", 0) == 0) ext = atoi(a.c_str() + 4); }
    vector<int> roots = lk.roots();
    vector<vector<uint8_t>> sig(roots.size());
    signatures(lk, B, roots, sig);
    // reference signatures: reference games are the registered games themselves
    map<vector<uint8_t>, string> refs;
    SumRes self = solveSum(B.g, B.g);
    (void)self;
    for (auto& nm : B.games) {
      vector<uint8_t> s = refSig(B.g, nm.start, B);
      if (!refs.count(s)) refs[s] = nm.name; else refs[s] += "=" + nm.name;
    }
    map<string, long> cls; map<string, vector<string>> ex;
    vector<string> label(roots.size());
    for (size_t k = 0; k < roots.size(); k++) {
      auto it = refs.find(sig[k]);
      string l;
      if (it != refs.end()) l = it->second;
      else {
        // decisive-or-loopy: a root is "decisive" if some context gives a forced decisive result; keep unclassified
        l = "other";
      }
      label[k] = l; cls[l]++; if (ex[l].size() < 3) ex[l].push_back(lk.rootText(roots[k]));
    }
    { vector<char> sh = shortNodes(lk.g); long ns = 0; for (int r : roots) if (sh[r]) { ns++; if (ns <= 3) printf("SHORT root %s\n", lk.rootText(r).c_str()); } printf("short roots: %ld of %zu\n", ns, roots.size()); }
    { set<vector<uint8_t>> od; for (size_t k = 0; k < roots.size(); k++) if (label[k] == "other") od.insert(sig[k]); printf("distinct other signatures: %zu\n", od.size()); if (getenv("DUMPSIG")) for (auto& sg : od) { printf("SIG "); for (auto v : sg) printf("%d", v); printf("\n"); } }
    printf("board %s pairs %s margin %s : legal nodes %zu roots %zu races %ld\n", argv[2], argv[3], argv[4], lk.raw.size(), roots.size(), lk.races);
    for (auto& kv : cls) {
      printf("  %-28s %8ld   e.g.", kv.first.c_str(), kv.second);
      for (auto& e : ex[kv.first]) printf(" [%s]", e.c_str());
      printf("\n");
    }
    if (!dump.empty())
      for (size_t k = 0; k < roots.size(); k++) if (label[k] == dump) printf("DUMP %s :: %s\n", dump.c_str(), lk.rootText(roots[k]).c_str());
    if (ext > 0) {
      // Extended battery: re-test every root whose B34 label is a given name against the extended battery of its reference
      vector<Battery> chunks; if (getenv("EXT2")) buildExt2(chunks, 600); else buildExt(chunks, 400);
      // reference game for a label = the game of that name in B
      map<string, int> bstart; for (auto& nm : B.games) bstart[nm.name] = nm.start;
      map<string, pair<long, long>> agree;  // label -> (agree, disagree)
      vector<char> okAll(roots.size(), 1);
      for (auto& ch : chunks) {
        vector<vector<uint8_t>> s2(roots.size());
        signatures(lk, ch, roots, s2);
        map<string, vector<uint8_t>> rs;
        for (auto& kv : bstart) rs[kv.first] = refSig(B.g, kv.second, ch);
        for (size_t k = 0; k < roots.size(); k++) {
          string l = label[k]; size_t p = l.find('='); if (p != string::npos) l = l.substr(0, p);
          if (!rs.count(l)) continue;
          if (rs[l] != s2[k]) okAll[k] = 0;
        }
      }
      for (size_t k = 0; k < roots.size(); k++) {
        string l = label[k]; size_t p = l.find('='); if (p != string::npos) l = l.substr(0, p);
        if (!bstart.count(l)) continue;
        if (okAll[k]) agree[l].first++; else agree[l].second++;
      }
      printf("EXT battery (%zu games in %zu chunks):\n", chunks.size() * 0 + 0, chunks.size());
      for (auto& kv : agree) printf("  %-20s agree %ld disagree %ld\n", kv.first.c_str(), kv.second.first, kv.second.second);
    }
  }

  else if (mode == "allpairs") {
    vector<int> roots = lk.roots();
    vector<vector<uint8_t>> sig(roots.size());
    signatures(lk, B, roots, sig);
    map<vector<uint8_t>, string> refs; map<string,int> bstart;
    for (auto& nm : B.games) { vector<uint8_t> sg = refSig(B.g, nm.start, B); if (!refs.count(sg)) refs[sg] = nm.name; bstart[nm.name] = nm.start; }
    vector<string> label(roots.size());
    for (size_t k = 0; k < roots.size(); k++) { auto it = refs.find(sig[k]); label[k] = it == refs.end() ? "" : it->second; }
    vector<int> nid; Game sub = subgame(lk.g, roots, nid);
    SumRes sr = solveSum(sub, sub);
    SumRes rr = solveSum(B.g, B.g);
    long checked = 0, mism = 0; map<string, long> perPair; vector<string> exm;
    int incl = argc > 5 ? atoi(argv[5]) : 0;  // if 1, skip classes dud/on/off in the first operand
    for (size_t i = 0; i < roots.size(); i++) { if (label[i].empty()) continue;
      for (size_t j = 0; j < roots.size(); j++) { if (label[j].empty()) continue;
        size_t a = (size_t)nid[roots[i]] * sr.nB + nid[roots[j]]; size_t ra = ((size_t)bstart[label[i]] * rr.nB + bstart[label[j]]) * 2;
        checked++;
        if (sr.w[a * 2] != rr.w[ra] || sr.w[a * 2 + 1] != rr.w[ra + 1]) { mism++; perPair[label[i] + " + " + label[j]]++; if (exm.size() < 4) exm.push_back(lk.rootText(roots[i]) + " + " + lk.rootText(roots[j])); }
      } }
    printf("allpairs %s %s %s: roots %zu named %ld subgame %d: pairs checked %ld mismatches %ld\n", argv[2], argv[3], argv[4], roots.size(), (long)count_if(label.begin(), label.end(), [](const string& x){return !x.empty();}), sub.n, checked, mism);
    for (auto& kv : perPair) printf("   MISMATCH %s : %ld\n", kv.first.c_str(), kv.second);
    for (auto& e : exm) printf("   e.g. %s\n", e.c_str());
    (void)incl;
  }

  else if (mode == "pred") {
    SumRes rr = solveSum(B.g, B.g); map<string,int> st; for (auto& nm : B.games) st[nm.name] = nm.start;
    static const char* O = "LDW";
    const char* Gs[] = {"+1", "{1|0}", "-1", "{0|-1}"}; const char* Hs[] = {"0", "+1", "-1", "*", "*2", "+2", "-2"};
    for (auto g : Gs) for (auto h : Hs) { size_t a = ((size_t)st[g] * rr.nB + st[h]) * 2; printf("PRED %s | %s | %c %c\n", g, h, O[rr.w[a]], O[rr.w[a + 1]]); }
  }
  else if (mode == "root") {
    int node = lk.parseRoot(argv[5]);
    if (node < 0) { printf("illegal root\n"); return 0; }
    vector<int> roots = {node};
    vector<vector<uint8_t>> sig(1);
    signatures(lk, B, roots, sig);
    static const char* O = "LDW";
    printf("root %s  nodes %zu\n", lk.rootText(node).c_str(), lk.raw.size());
    map<vector<uint8_t>, string> refs;
    for (auto& nm : B.games) { vector<uint8_t> s = refSig(B.g, nm.start, B); refs[s] += (refs.count(s) ? "=" : "") + nm.name; }
    for (size_t i = 0; i < B.games.size(); i++) printf("  +%-8s (%c,%c)\n", B.games[i].name.c_str(), O[sig[0][2 * i]], O[sig[0][2 * i + 1]]);
    auto it = refs.find(sig[0]);
    printf("B34 NAME: %s\n", it == refs.end() ? "(none)" : it->second.c_str());
    if (argc > 6) {
      vector<Battery> chunks; buildExt(chunks, 400);
      if (it != refs.end()) {
        string l = it->second; size_t p = l.find('='); if (p != string::npos) l = l.substr(0, p);
        int bs = -1; for (auto& nm : B.games) if (nm.name == l) bs = nm.start;
        long ag = 0, dis = 0; vector<string> bad;
        for (auto& ch : chunks) {
          vector<vector<uint8_t>> s2(1); signatures(lk, ch, roots, s2);
          vector<uint8_t> rs = refSig(B.g, bs, ch);
          for (size_t i = 0; i < ch.games.size(); i++) {
            bool eq = rs[2 * i] == s2[0][2 * i] && rs[2 * i + 1] == s2[0][2 * i + 1];
            if (eq) ag++; else { dis++; if (bad.size() < 5) bad.push_back(ch.games[i].name); }
          }
        }
        printf("EXT (%ld games) vs reference %s: agree %ld disagree %ld", ag + dis, l.c_str(), ag, dis);
        for (auto& b : bad) printf(" [%s]", b.c_str());
        printf("\n");
      }
    }
  }
  return 0;
}
