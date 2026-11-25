// pk.cpp -- K63 referee's own P solver (written from LOOPY Definitions 1.1-1.5 / SPEC rules for P; shares no code
// with the investigator's programs or with kref).  Flat 8x8 board only.
// P: chess moves of kings and pawns (no move into check, double steps, e.p.), a promotion is a terminal win for
// the promoter, checkmate a loss, stalemate a draw, infinite play a draw.
// Method: positions are split by pawn configuration (White pawn set, Black pawn set).  Every pawn move and every
// capture changes the configuration irreversibly (a pawn advances, or a pawn disappears), so configurations are
// solved one at a time in an order where every move that leaves a configuration goes to one already solved;
// inside one configuration only king moves remain, solved by retrograde counting (least fixed point).
// A position with an e.p. right is evaluated by one ply over solved values when it is needed.
// Usage:  pk < file     each input line: "PIECES stm [ep]" (e.g. "Ka4 kc4 Pb2 Pf5 pb6 pf6 b -"), blank-separated
//         groups are independent problems; output: the line and its value W / L / D (White's view), and with -m
//         also the value after every legal move.
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <sstream>
#include <iostream>
using namespace std;
typedef uint64_t BB;
static inline int RK(int s) { return s >> 3; }
static inline int FL(int s) { return s & 7; }
static inline bool HAS(BB b, int s) { return (b >> s) & 1ULL; }
static string SQ(int s) { string r; r += char('a' + FL(s)); r += char('1' + RK(s)); return r; }
static int PSQ(const string &x) { return (x[1] - '1') * 8 + (x[0] - 'a'); }
static inline bool kadj(int a, int b) { return a != b && abs(RK(a) - RK(b)) <= 1 && abs(FL(a) - FL(b)) <= 1; }

struct Cfg { BB w, b; bool operator==(const Cfg &o) const { return w == o.w && b == o.b; } };
struct CH { size_t operator()(const Cfg &c) const { return c.w * 0x9E3779B97F4A7C15ULL ^ (c.b + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL; } };

// square s attacked by pawns of colour `by` (0 White) in configuration c
static inline bool pawnatt(const Cfg &c, int s, int by) {
  int r = RK(s), f = FL(s);
  int pr = by ? r + 1 : r - 1;
  if (pr < 0 || pr > 7) return false;
  BB pw = by ? c.b : c.w;
  if (f > 0 && HAS(pw, pr * 8 + f - 1)) return true;
  if (f < 7 && HAS(pw, pr * 8 + f + 1)) return true;
  return false;
}

static unordered_map<Cfg, int, CH> cid;
static vector<Cfg> cfgs;
static vector<vector<int8_t>> val;  // per config: [stm*4096 + wk*64 + bk]: 1 mover wins, 2 mover loses, 3 draw, 4 illegal
static vector<char> solved;

static int key_count(const Cfg &c) { return __builtin_popcountll(c.w) + __builtin_popcountll(c.b); }
static int key_adv(const Cfg &c) {
  int a = 0;
  for (int s = 0; s < 64; s++) { if (HAS(c.w, s)) a += RK(s); if (HAS(c.b, s)) a += 7 - RK(s); }
  return a;
}
// configurations reachable (over-approximation: kings ignored)
static void closure(const vector<Cfg> &start) {
  vector<Cfg> st(start.begin(), start.end());
  auto add = [&](Cfg c) { if (!cid.count(c)) { cid[c] = cfgs.size(); cfgs.push_back(c); st.push_back(c); } };
  for (auto &c : start) if (!cid.count(c)) { cid[c] = cfgs.size(); cfgs.push_back(c); }
  while (!st.empty()) {
    Cfg c = st.back(); st.pop_back();
    BB all = c.w | c.b;
    for (int s = 0; s < 64; s++) {
      if (HAS(c.w, s) || HAS(c.b, s)) {  // a king captures it
        Cfg d = c; d.w &= ~(1ULL << s); d.b &= ~(1ULL << s); add(d);
      }
      for (int col = 0; col < 2; col++) {
        BB own = col ? c.b : c.w, opp = col ? c.w : c.b;
        if (!HAS(own, s)) continue;
        int dir = col ? -8 : 8, r = RK(s), f = FL(s), last = col ? 0 : 7, r1 = r + (col ? -1 : 1);
        if (r1 == last) continue;  // only promotions from here (terminal)
        auto mv = [&](int to, int cap) { Cfg d = c; BB &o = col ? d.b : d.w; BB &e = col ? d.w : d.b;
          o &= ~(1ULL << s); o |= 1ULL << to; if (cap >= 0) e &= ~(1ULL << cap); add(d); };
        if (!HAS(all, s + dir)) { mv(s + dir, -1); if (r == (col ? 6 : 1) && !HAS(all, s + 2 * dir)) mv(s + 2 * dir, -1); }
        for (int df = -1; df <= 1; df += 2) {
          int g = f + df; if (g < 0 || g > 7) continue;
          int t = r1 * 8 + g;
          if (HAS(opp, t)) mv(t, t);
          // e.p.: own pawn on its 5th rank, enemy pawn beside it, square behind empty
          int epr = col ? 3 : 4;
          if (r == epr && HAS(opp, r * 8 + g) && !HAS(all, t)) mv(t, r * 8 + g);
        }
      }
    }
  }
}

static inline int8_t getv(int ci, int stm, int wk, int bk) { return val[ci][stm * 4096 + wk * 64 + bk]; }

// outcome codes for the mover: 1 win, 2 loss, 3 draw
struct Out { int code; };
// one-ply value of a state of configuration c (solved), side stm to move, e.p. square ep (>=0)
static int evalEP(const Cfg &c, int stm, int wk, int bk, int ep);

// enumerate moves of (c, stm, wk, bk, ep): calls fext(code) for moves leaving the configuration (code = outcome for
// the MOVER: 1 win, 2 loss, 3 draw) and fint(idx) for king moves inside it.  Returns number of legal moves.
template <class FE, class FI>
static int moves(const Cfg &c, int stm, int wk, int bk, int ep, FE fext, FI fint) {
  int n = 0;
  int k = stm ? bk : wk, ok = stm ? wk : bk;
  BB own = stm ? c.b : c.w, opp = stm ? c.w : c.b, all = c.w | c.b;
  // king moves
  for (int dr = -1; dr <= 1; dr++) for (int df = -1; df <= 1; df++) {
    if (!dr && !df) continue;
    int r = RK(k) + dr, f = FL(k) + df;
    if (r < 0 || r > 7 || f < 0 || f > 7) continue;
    int t = r * 8 + f;
    if (HAS(own, t) || kadj(t, ok) || t == ok) continue;
    if (HAS(opp, t)) {
      Cfg d = c; (stm ? d.w : d.b) &= ~(1ULL << t);
      if (pawnatt(d, t, 1 - stm)) continue;
      int ci = cid.at(d);
      int nwk = stm ? wk : t, nbk = stm ? t : bk;
      int v = getv(ci, 1 - stm, nwk, nbk);
      n++; fext(v == 1 ? 2 : v == 2 ? 1 : 3);
    } else {
      if (pawnatt(c, t, 1 - stm)) continue;
      int nwk = stm ? wk : t, nbk = stm ? t : bk;
      n++; fint((1 - stm) * 4096 + nwk * 64 + nbk);
    }
  }
  // pawn moves
  int dir = stm ? -8 : 8, last = stm ? 0 : 7;
  for (int s = 0; s < 64; s++) if (HAS(own, s)) {
    int r = RK(s), f = FL(s), r1 = r + (stm ? -1 : 1);
    auto go = [&](int to, int cap, bool dbl) {
      if (to == wk || to == bk) return;
      Cfg d = c; BB &o = stm ? d.b : d.w; BB &e = stm ? d.w : d.b;
      o &= ~(1ULL << s); if (cap >= 0) e &= ~(1ULL << cap);
      bool prom = RK(to) == last;
      if (!prom) o |= 1ULL << to;
      if (pawnatt(d, k, 1 - stm)) return;  // own king left in check
      n++;
      if (prom) { fext(1); return; }
      int ci = cid.at(d);
      int v;
      if (dbl) {
        int e2 = to - dir;  // square passed over
        int pr = RK(to);
        bool epok = false;
        BB ep_takers = stm ? d.w : d.b;
        if (f > 0 && HAS(ep_takers, pr * 8 + f - 1)) epok = true;
        if (f < 7 && HAS(ep_takers, pr * 8 + f + 1)) epok = true;
        v = epok ? evalEP(d, 1 - stm, wk, bk, e2) : getv(ci, 1 - stm, wk, bk);
      } else v = getv(ci, 1 - stm, wk, bk);
      fext(v == 1 ? 2 : v == 2 ? 1 : 3);
    };
    int t1 = s + dir;
    if (!HAS(all, t1) && t1 != wk && t1 != bk) {
      go(t1, -1, false);
      int t2 = s + 2 * dir;
      if (r == (stm ? 6 : 1) && !HAS(all, t2) && t2 != wk && t2 != bk) go(t2, -1, true);
    }
    for (int df = -1; df <= 1; df += 2) {
      int g = f + df; if (g < 0 || g > 7) continue;
      int t = r1 * 8 + g;
      if (HAS(opp, t)) go(t, t, false);
      else if (t == ep) go(t, r * 8 + g, false);
    }
  }
  return n;
}

static bool incheck(const Cfg &c, int stm, int wk, int bk) { int k = stm ? bk : wk; return pawnatt(c, k, 1 - stm); }

static int evalEP(const Cfg &c, int stm, int wk, int bk, int ep) {
  bool win = false, draw = false;
  int n = moves(c, stm, wk, bk, ep,
                [&](int code) { if (code == 1) win = true; else if (code == 3) draw = true; },
                [&](int idx) { int v = val[cid.at(c)][idx]; if (v == 2) win = true; else if (v != 1) draw = true; });
  if (n == 0) return incheck(c, stm, wk, bk) ? 2 : 3;
  return win ? 1 : draw ? 3 : 2;
}

static void solve_cfg(int ci) {
  const Cfg c = cfgs[ci];
  vector<int8_t> &V = val[ci];
  V.assign(8192, 0);
  BB all = c.w | c.b;
  vector<int> cnt(8192, 0);
  vector<vector<int>> pred(8192);
  vector<int> q;
  for (int stm = 0; stm < 2; stm++) for (int wk = 0; wk < 64; wk++) for (int bk = 0; bk < 64; bk++) {
    int idx = stm * 4096 + wk * 64 + bk;
    if (wk == bk || kadj(wk, bk) || HAS(all, wk) || HAS(all, bk) || incheck(c, 1 - stm, wk, bk)) { V[idx] = 4; continue; }
  }
  for (int idx = 0; idx < 8192; idx++) {
    if (V[idx] == 4) continue;
    int stm = idx >> 12, wk = (idx >> 6) & 63, bk = idx & 63;
    bool win = false; int c2 = 0;
    int n = moves(c, stm, wk, bk, -1,
                  [&](int code) { if (code == 1) win = true; else if (code == 3) c2 += 1000000; },
                  [&](int j) { pred[j].push_back(idx); c2++; });
    if (n == 0) { V[idx] = incheck(c, stm, wk, bk) ? 2 : 3; if (V[idx] == 2) q.push_back(idx); continue; }
    if (win) { V[idx] = 1; q.push_back(idx); continue; }
    cnt[idx] = c2;
    if (c2 == 0) { V[idx] = 2; q.push_back(idx); }
  }
  for (size_t h = 0; h < q.size(); h++) {
    int t = q[h];
    for (int s : pred[t]) {
      if (V[s]) continue;
      if (V[t] == 2) { V[s] = 1; q.push_back(s); }
      else if (V[t] == 1) { if (--cnt[s] == 0) { V[s] = 2; q.push_back(s); } }
    }
  }
  for (int idx = 0; idx < 8192; idx++) if (V[idx] == 0) V[idx] = 3;
  solved[ci] = 1;
}

struct In { Cfg c; int stm, wk, bk, ep; string line; };
static In parse(const string &line) {
  In p; p.c = {0, 0}; p.ep = -1; p.line = line;
  stringstream ss(line); string x; vector<string> tok;
  while (ss >> x) tok.push_back(x);
  int i = 0;
  for (; i < (int)tok.size(); i++) {
    const string &t = tok[i];
    if (t.size() == 3 && strchr("KkPp", t[0])) {
      int s = PSQ(t.substr(1));
      if (t[0] == 'K') p.wk = s; else if (t[0] == 'k') p.bk = s; else if (t[0] == 'P') p.c.w |= 1ULL << s; else p.c.b |= 1ULL << s;
    } else break;
  }
  p.stm = tok[i][0] == 'b';
  if (i + 1 < (int)tok.size() && tok[i + 1] != "-") p.ep = PSQ(tok[i + 1]);
  return p;
}

int main(int argc, char **argv) {
  bool showm = argc > 1 && string(argv[1]) == "-m";
  string line; vector<vector<In>> groups(1);
  while (getline(cin, line)) {
    if (line.empty() || line[0] == '#') { if (!groups.back().empty()) groups.push_back({}); continue; }
    groups.back().push_back(parse(line));
  }
  for (auto &g : groups) {
    if (g.empty()) continue;
    cid.clear(); cfgs.clear(); val.clear(); solved.clear();
    vector<Cfg> st; for (auto &p : g) st.push_back(p.c);
    closure(st);
    vector<int> ord(cfgs.size());
    for (size_t i = 0; i < ord.size(); i++) ord[i] = i;
    vector<pair<int,int>> key(cfgs.size());
    for (size_t i = 0; i < cfgs.size(); i++) key[i] = {key_count(cfgs[i]), key_adv(cfgs[i])};
    // solve fewer pawns first; among equal counts, more advanced first
    sort(ord.begin(), ord.end(), [&](int a, int b) { if (key[a].first != key[b].first) return key[a].first < key[b].first; return key[a].second > key[b].second; });
    val.assign(cfgs.size(), {}); solved.assign(cfgs.size(), 0);
    for (int ci : ord) solve_cfg(ci);
    for (auto &p : g) {
      int ci = cid.at(p.c);
      int v;
      if (p.ep >= 0) v = evalEP(p.c, p.stm, p.wk, p.bk, p.ep);
      else v = val[ci][p.stm * 4096 + p.wk * 64 + p.bk];
      char a = v == 4 ? 'X' : v == 3 ? 'D' : (v == 1) == (p.stm == 0) ? 'W' : 'L';
      printf("%-44s %c   (configs %zu)\n", p.line.c_str(), a, cfgs.size());
      if (showm && v != 4) {
        // list moves with values (White's view after the move)
        int stm = p.stm;
        int k = stm ? p.bk : p.wk;
        (void)k;
        // re-run generator, printing outcome codes in order (king moves first, then pawn moves by square)
        vector<string> outv;
        moves(p.c, stm, p.wk, p.bk, p.ep,
              [&](int code) { outv.push_back(code == 3 ? "D" : ((code == 1) == (stm == 0)) ? "W" : "L"); },
              [&](int j) { int w = val[ci][j]; outv.push_back(w == 3 ? "D" : ((w == 2) == (stm == 0)) ? "W" : "L"); });
        printf("      move values in generator order (king moves, then pawns by square): ");
        for (auto &o : outv) printf("%s ", o.c_str());
        printf("\n");
      }
    }
    fflush(stdout);
  }
  return 0;
}
