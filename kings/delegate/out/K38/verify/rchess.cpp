// rchess.cpp -- K38 referee's own chess solver, written from kings/SPEC.md only (shares no code with kpsolve.c,
// ref3, kq3/ownref or K38's scripts).  Kings + pawns + at most CAP=1 officer (Q, R, B, N), flat or cylinder,
// double step and en passant as in SPEC.md.  A promotion that would create a 2nd officer is *capped*:
// bound A = immediate White win, bound B = immediate Black win.  Method: explicit forward enumeration of every
// position reachable from the input positions, then the least fixed point by repeated sweeps.
// Usage: rchess W H wrap(0/1) BOUND(A|B) [promW] [promB] < positions  -> "<pos> | v" (W/D/L, White's view).
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <unordered_map>
#include <iostream>
#include <sstream>
#include <set>
using namespace std;
typedef uint64_t u64;
static int W, H, WRAP, N;
static char BOUND = 'A';
static string PROM[2] = {"QRBN", "QRBN"};

struct Pos { int wk, bk; u64 wp, bp; int ot, oc, os; int stm; int ep; };  // ot: 0 none, 1 Q, 2 R, 3 B, 4 N; ep: -1 none
struct Key { u64 a, b; bool operator==(const Key& o) const { return a == o.a && b == o.b; } };
struct KH { size_t operator()(const Key& k) const { return k.a * 0x9E3779B97F4A7C15ULL ^ (k.b + 0x632BE59BD9B4E019ULL + (k.a << 6)); } };
static Key key(const Pos& p) {
  Key k; k.a = p.wp | ((u64)p.wk << 42) | ((u64)p.bk << 48) | ((u64)p.stm << 54) | ((u64)p.ot << 55) | ((u64)p.oc << 58);
  k.b = p.bp | ((u64)p.os << 42) | ((u64)(p.ep + 1) << 48); return k;
}
static int fl(int s) { return s % W; }
static int rk(int s) { return s / W; }
static int sq(int f, int r) {
  if (r < 0 || r >= H) return -1;
  if (WRAP) f = ((f % W) + W) % W; else if (f < 0 || f >= W) return -1;
  return r * W + f;
}
static const int KD[8][2] = {{1,0},{-1,0},{0,1},{0,-1},{1,1},{1,-1},{-1,1},{-1,-1}};
static const int ND[8][2] = {{1,2},{2,1},{-1,2},{-2,1},{1,-2},{2,-1},{-1,-2},{-2,-1}};
static bool kadj(int a, int b) { for (auto& d : KD) if (sq(fl(a) + d[0], rk(a) + d[1]) == b) return true; return false; }
static u64 occ(const Pos& p) { u64 o = p.wp | p.bp | (1ULL << p.wk) | (1ULL << p.bk); if (p.ot) o |= 1ULL << p.os; return o; }
// squares an officer of type t on s attacks / may move to (ignoring colour), given occupancy o
static void offTargets(int t, int s, u64 o, vector<int>& out) {
  out.clear();
  if (t == 4) { for (auto& d : ND) { int q = sq(fl(s) + d[0], rk(s) + d[1]); if (q >= 0) out.push_back(q); } }
  else {
    for (int i = 0; i < 8; i++) {
      bool orth = i < 4;
      if (t == 2 && !orth) continue;
      if (t == 3 && orth) continue;
      int f = fl(s), r = rk(s);
      while (true) {
        f += KD[i][0]; r += KD[i][1];
        int q = sq(f, r);
        if (q < 0 || q == s) break;
        out.push_back(q);
        if (o >> q & 1) break;
      }
    }
  }
  set<int> u(out.begin(), out.end()); out.assign(u.begin(), u.end());
}
static bool attacked(const Pos& p, int s, int by) {
  int k = by == 0 ? p.wk : p.bk;
  if (kadj(k, s)) return true;
  u64 pw = by == 0 ? p.wp : p.bp; int d = by == 0 ? -1 : 1;  // a pawn of `by` attacking s stands at rank(s)+d
  for (int df = -1; df <= 1; df += 2) { int q = sq(fl(s) + df, rk(s) + d); if (q >= 0 && (pw >> q & 1)) return true; }
  if (p.ot && p.oc == by) { vector<int> t; offTargets(p.ot, p.os, occ(p), t); for (int q : t) if (q == s) return true; }
  return false;
}
static bool inCheck(const Pos& p, int c) { return attacked(p, c == 0 ? p.wk : p.bk, 1 - c); }
// moves: children; term: +1 mover wins at once (capped promotion favourable to mover), -1 mover loses at once
struct MV { Pos c; int term; };
static void gen(const Pos& p, vector<MV>& out) {
  out.clear();
  int me = p.stm, op = 1 - me;
  u64 o = occ(p);
  u64 myp = me == 0 ? p.wp : p.bp, opp = me == 0 ? p.bp : p.wp;
  bool myOff = p.ot && p.oc == me, opOff = p.ot && p.oc == op;
  auto push = [&](Pos n) { n.stm = op; if (!inCheck(n, me)) out.push_back({n, 0}); };
  auto capAt = [&](Pos& n, int t) {  // remove enemy non-king on t
    if (me == 0) n.bp &= ~(1ULL << t); else n.wp &= ~(1ULL << t);
    if (opOff && p.os == t) { n.ot = 0; n.oc = 0; n.os = 0; }
  };
  auto isEnemy = [&](int t) { return (opp >> t & 1) || (opOff && p.os == t); };
  auto isOwn = [&](int t) { return (myp >> t & 1) || (myOff && p.os == t) || t == (me == 0 ? p.wk : p.bk); };
  int myk = me == 0 ? p.wk : p.bk, ok = me == 0 ? p.bk : p.wk;
  // king
  for (auto& d : KD) {
    int t = sq(fl(myk) + d[0], rk(myk) + d[1]); if (t < 0 || isOwn(t) || t == ok) continue;
    Pos n = p; n.ep = -1; capAt(n, t); if (me == 0) n.wk = t; else n.bk = t; push(n);
  }
  // officer
  if (myOff) {
    vector<int> ts; offTargets(p.ot, p.os, o, ts);
    for (int t : ts) { if (isOwn(t) || t == ok) continue; Pos n = p; n.ep = -1; capAt(n, t); n.os = t; push(n); }
  }
  // pawns
  int dir = me == 0 ? 1 : -1, last = me == 0 ? H - 1 : 0, second = me == 0 ? 1 : H - 2;
  for (int s = 0; s < N; s++) {
    if (!(myp >> s & 1)) continue;
    struct T { int t; bool cap; int capsq; int nep; };
    vector<T> ts;
    int one = sq(fl(s), rk(s) + dir);
    if (one >= 0 && !(o >> one & 1)) {
      ts.push_back({one, false, -1, -1});
      int two = sq(fl(s), rk(s) + 2 * dir);
      if (rk(s) == second && two >= 0 && !(o >> two & 1)) ts.push_back({two, false, -1, rk(two) == last ? -1 : one});
    }
    for (int df = -1; df <= 1; df += 2) {
      int t = sq(fl(s) + df, rk(s) + dir); if (t < 0) continue;
      if (isEnemy(t)) ts.push_back({t, true, t, -1});
      else if (p.ep == t) { int c = sq(fl(t), rk(t) - dir); if (c >= 0 && (opp >> c & 1)) ts.push_back({t, true, c, -1}); }
    }
    for (auto& x : ts) {
      Pos n = p; n.ep = x.nep;
      if (me == 0) n.wp &= ~(1ULL << s); else n.bp &= ~(1ULL << s);
      if (x.cap) capAt(n, x.capsq);
      if (rk(x.t) == last) {
        for (char c : PROM[me]) {
          int ty = c == 'Q' ? 1 : c == 'R' ? 2 : c == 'B' ? 3 : 4;
          if (n.ot) {  // capped: legality with the new piece on t as a blocker (an own pawn-like blocker)
            Pos b = n; if (me == 0) b.wp |= 1ULL << x.t; else b.bp |= 1ULL << x.t; b.stm = op;
            // the blocker must not itself attack: model only blocking; pawn attacks of the blocker point away from own king? use full check
            Pos bb = b; // attacks on own king by enemy pieces only
            if (inCheck(bb, me)) continue;
            int mw = (BOUND == 'A') ? 0 : 1;  // winner of a capped promotion
            out.push_back({n, mw == me ? 1 : -1});
          } else { Pos m = n; m.ot = ty; m.oc = me; m.os = x.t; push(m); }
        }
      } else { if (me == 0) n.wp |= 1ULL << x.t; else n.bp |= 1ULL << x.t; push(n); }
    }
  }
}
static int pq(const char* s) { return (s[1] - '1') * W + (s[0] - 'a'); }
static string nm(int s) { string r; r += char('a' + fl(s)); r += to_string(rk(s) + 1); return r; }
static bool parse(const string& line, Pos& p) {
  istringstream is(line); vector<string> t; string x; while (is >> x) t.push_back(x);
  if (t.size() < 3) return false;
  p = Pos{-1, -1, 0, 0, 0, 0, 0, 0, -1};
  for (size_t i = 0; i + 2 < t.size(); i++) {
    char c = t[i][0]; int s = pq(t[i].c_str() + 1);
    if (c == 'K') p.wk = s; else if (c == 'k') p.bk = s; else if (c == 'P') p.wp |= 1ULL << s; else if (c == 'p') p.bp |= 1ULL << s;
    else { const char* o = "QRBNqrbn"; const char* f = strchr(o, c); if (!f) return false; int i2 = f - o; p.ot = i2 % 4 + 1; p.oc = i2 / 4; p.os = s; }
  }
  p.stm = t[t.size() - 2] == "w" ? 0 : 1;
  p.ep = t.back() == "-" ? -1 : pq(t.back().c_str());
  return true;
}
int main(int argc, char** argv) {
  W = atoi(argv[1]); H = atoi(argv[2]); WRAP = atoi(argv[3]); N = W * H; BOUND = argv[4][0];
  if (argc > 5) PROM[0] = argv[5];
  if (argc > 6) PROM[1] = argv[6];
  vector<string> lines; vector<Pos> roots; string l;
  while (getline(cin, l)) { lines.push_back(l); Pos p; if (l.empty() || l[0] == '#' || !parse(l, p)) continue; roots.push_back(p); }
  unordered_map<Key, int, KH> id; vector<Pos> st; vector<int> off{0}; vector<int> ed;  // ed: child index, or -2 (mover wins), -3 (mover loses)
  for (auto& r : roots) if (!id.count(key(r))) { id[key(r)] = st.size(); st.push_back(r); }
  vector<MV> mv;
  for (size_t i = 0; i < st.size(); i++) {
    Pos p = st[i]; gen(p, mv);
    for (auto& m : mv) {
      if (m.term) { ed.push_back(m.term > 0 ? -2 : -3); continue; }
      Key k = key(m.c); auto it = id.find(k); int j;
      if (it == id.end()) { j = st.size(); id[k] = j; st.push_back(m.c); } else j = it->second;
      ed.push_back(j);
    }
    off.push_back(ed.size());
  }
  size_t n = st.size();
  vector<signed char> v(n, 0);  // +1 win for side to move, -1 loss, 0 unknown/draw
  vector<char> fin(n, 0);
  for (size_t i = 0; i < n; i++) if (off[i] == off[i + 1]) { fin[i] = 1; v[i] = inCheck(st[i], st[i].stm) ? -1 : 0; }
  bool ch = true; int sweeps = 0;
  while (ch) {
    ch = false; sweeps++;
    for (size_t i = 0; i < n; i++) {
      if (fin[i]) continue;
      bool win = false, allw = true;
      for (int e = off[i]; e < off[i + 1]; e++) {
        int c = ed[e];
        if (c == -2) { win = true; break; }
        if (c == -3) continue;
        if (fin[c] && v[c] == -1) { win = true; break; }
        if (!(fin[c] && v[c] == 1)) allw = false;
      }
      if (win) { v[i] = 1; fin[i] = 1; ch = true; } else if (allw) { v[i] = -1; fin[i] = 1; ch = true; }
    }
  }
  fprintf(stderr, "[rchess %dx%d wrap=%d bound %c promW=%s promB=%s: %zu states, %zu edges, %d sweeps]\n", W, H, WRAP, BOUND,
          PROM[0].c_str(), PROM[1].c_str(), n, ed.size(), sweeps);
  for (auto& line : lines) {
    Pos p; if (line.empty() || line[0] == '#' || !parse(line, p)) { cout << line << "\n"; continue; }
    int i = id[key(p)]; int s = fin[i] ? v[i] : 0; if (p.stm == 1) s = -s;
    cout << line << " | " << (s > 0 ? 'W' : s < 0 ? 'L' : 'D');
    // per-move values
    gen(p, mv);
    for (auto& m : mv) {
      int w;
      if (m.term) w = m.term; else { int j = id[key(m.c)]; w = fin[j] ? -v[j] : 0; }
      if (p.stm == 1) w = -w;
      // label: find moved piece
      cout << " ";
      Pos c = m.c; string lab;
      if (p.stm == 0) { if (c.wk != p.wk) lab = "K" + nm(p.wk) + nm(c.wk); } else { if (c.bk != p.bk) lab = "K" + nm(p.bk) + nm(c.bk); }
      if (lab.empty()) lab = m.term ? "capped" : "other";
      cout << lab << ":" << (w > 0 ? 'W' : w < 0 ? 'L' : 'D');
    }
    cout << "\n";
  }
}
