// K68 copy of kings/delegate/out/K65/verify/src/ax65.cpp (the K65 referee's solver), unchanged except the block
// marked K68: with the environment variable AX68_QUERY=file, after solving P it prints the P value (W/D/L for White)
// of every position listed in that file (lines: WK BK Wpawns Bpawns side, pawns comma-separated or '-'), and exits.
// ax65.cpp -- K65 referee's own solver (written from scratch from kings/theory/LOOPY.md: Definition 4.8, Lemma 4.15
// for (B1), Theorem 4.18 (c) for Aux and the ladders T_N).  Shares no code with aux60, vgsum59, pr57, ref3m, kp_p,
// p45a, r48, kref or pk.
//
// Board: flat:WxH or cyl:WxH (W*H <= 64).  Chess moves of kings and pawns: double step from the second rank, e.p.,
// no move into check, kings never adjacent.  A promotion ends the play: the promoter wins.
// Games (all "does the HERO win?", hero = White unless stated):
//   P      : the group alone; checkmate loses, stalemate is a draw, infinite play a draw.  Solved twice (hero White,
//            hero Black), so P values are W / D / L.
//   sum    : group (+) T for a small D-game T, under the sum's rule: a move is a board move or a T move; no T move
//            while in check; a T move clears the mover's e.p. right; a side with no move at all loses.
//            T = 0      (no T moves)
//            T = -1     Black may once move -1 -> 0                       -> (B1)
//            T = under  White may pass for ever (accepting), Black may once move to 0   -> Aux, a Buchi game:
//                       an infinite play is a White win iff White passed infinitely often
//            T = T_N    ladder: u_j -> u_{j-1} for White (u_0 -> White terminal win), u_j -> z for Black
// Method.  A pawn configuration (White pawn set, Black pawn set) changes only irreversibly (a pawn advances or one
// disappears), and the T-state changes only irreversibly except for the pass under -> under.  So blocks
// (configuration, T-state) are solved one at a time, every move that leaves a block going to a block solved before.
// Inside a block only king moves and the pass remain; the block is solved by the nested fixpoint of a Buchi game
// (nu Y. mu X), which for blocks without accepting moves is the plain attractor (least fixpoint).  The set of
// configurations is the closure of the root configuration under pawn moves and captures with the kings ignored
// (an over-approximation; values of extra positions are never used wrongly, they are values of real positions).
// Positions with an e.p. right are evaluated by one ply over solved values when they are needed.
// Values are stored as one bit per (configuration, side to move, White king square, Black king square) per T-state.
// Memory: the program computes its array sizes before allocating and exits if they exceed the limit (default 2 GB).
//
// Usage: ax65 BOARD "PIECES" Z0 Z1 [--lmax N] [--noladder] [--noaux] [--noP] [--limit BYTES]
//   PIECES with the Black king on Z0 (over orientation: Black shuttles Z0-Z1, White king fixed), e.g.
//   ax65 flat:8x8 "Kc4 ke4 Pb5 Pf2 Pf6 pb6 pf7" e4 e5
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
#include <algorithm>
#include <unordered_set>
#include <sstream>
using namespace std;
typedef uint64_t BB;

static int W, H, CYL, NSQ, HALF, NS, WPC;
static BB KN[64], PA[2][64];  // KN: king neighbours; PA[x][s]: squares from which a pawn of colour x attacks s
static inline bool on(BB b, int s) { return (b >> s) & 1ULL; }
static inline int RK(int s) { return s / W; }
static inline int FL(int s) { return s % W; }
static bool fstep(int f, int d, int &g) { g = f + d; if (CYL) { g = (g + W) % W; return true; } return g >= 0 && g < W; }
static string SN(int s) { string r; r += char('a' + FL(s)); r += to_string(RK(s) + 1); return r; }
static int PS(const string &x) { return (atoi(x.c_str() + 1) - 1) * W + (x[0] - 'a'); }
static inline bool kadj(int a, int b) { return on(KN[a], b); }

static void initBoard() {
  NSQ = W * H; HALF = NSQ * NSQ; NS = 2 * HALF; WPC = (NS + 63) / 64;
  for (int s = 0; s < NSQ; s++) {
    KN[s] = 0; PA[0][s] = PA[1][s] = 0;
    int r = RK(s), f = FL(s), g;
    for (int dr = -1; dr <= 1; dr++) for (int df = -1; df <= 1; df++) {
      if (!dr && !df) continue;
      int r2 = r + dr; if (r2 < 0 || r2 >= H || !fstep(f, df, g)) continue;
      int t = r2 * W + g; if (t != s) KN[s] |= 1ULL << t;
    }
    for (int d = -1; d <= 1; d += 2) {
      if (!fstep(f, d, g)) continue;
      if (r - 1 >= 0) PA[0][s] |= 1ULL << ((r - 1) * W + g);  // White pawn one rank below attacks s
      if (r + 1 < H) PA[1][s] |= 1ULL << ((r + 1) * W + g);   // Black pawn one rank above attacks s
    }
  }
}

struct Cfg { BB p[2]; };
struct CH { size_t operator()(const pair<BB, BB> &x) const { return (x.first * 0x9E3779B97F4A7C15ULL) ^ ((x.second + 0x7F4A7C15ULL) * 0xC2B2AE3D27D4EB4FULL); } };
static vector<Cfg> CF;            // configurations in solve order
static vector<int> SORTED;        // indices of CF sorted by (p0, p1) for lookup
static double LIMIT = 2.0e9;

static int adv(const Cfg &c) { int a = 0; for (int s = 0; s < NSQ; s++) { if (on(c.p[0], s)) a += RK(s); if (on(c.p[1], s)) a += H - 1 - RK(s); } return a; }
static int lastRank(int x) { return x ? 0 : H - 1; }
static int startRank(int x) { return x ? H - 2 : 1; }

static void closure(const Cfg &root) {
  unordered_set<pair<BB, BB>, CH> seen; vector<Cfg> st{root}; seen.insert({root.p[0], root.p[1]}); CF.push_back(root);
  size_t capcfg = (size_t)(LIMIT / (2.0 * WPC * 8 + 120));
  auto add = [&](const Cfg &d) { if (seen.insert({d.p[0], d.p[1]}).second) { CF.push_back(d); st.push_back(d);
      if (CF.size() > capcfg) { printf("ABORT: more than %zu configurations; two value layers would exceed the memory limit\n", capcfg); exit(3); } } };
  while (!st.empty()) {
    Cfg c = st.back(); st.pop_back();
    BB all = c.p[0] | c.p[1];
    for (int x = 0; x < 2; x++) for (int s = 0; s < NSQ; s++) if (on(c.p[x], s)) {
      { Cfg d = c; d.p[x] &= ~(1ULL << s); add(d); }  // a king takes it
      int r = RK(s), r1 = r + (x ? -1 : 1);
      if (r1 < 0 || r1 >= H || r1 == lastRank(x)) continue;  // from here only promotions (terminal)
      int t1 = r1 * W + FL(s);
      auto mv = [&](int to, int cap) { Cfg d = c; d.p[x] &= ~(1ULL << s); d.p[x] |= 1ULL << to; if (cap >= 0) d.p[1 - x] &= ~(1ULL << cap); add(d); };
      if (!on(all, t1)) { mv(t1, -1); if (r == startRank(x)) { int t2 = (r1 + (x ? -1 : 1)) * W + FL(s); if (!on(all, t2)) mv(t2, -1); } }
      for (int d = -1; d <= 1; d += 2) { int g; if (!fstep(FL(s), d, g)) continue; int t = r1 * W + g;
        if (on(c.p[1 - x], t)) mv(t, t);
        else if (r == (x ? 3 : H - 4) && on(c.p[1 - x], r * W + g) && !on(all, t)) mv(t, r * W + g); }
    }
  }
  // solve order: fewer pawns first, then more advanced first (every move leaves to an earlier configuration)
  vector<pair<pair<int, int>, int>> key;
  for (size_t i = 0; i < CF.size(); i++) key.push_back({{__builtin_popcountll(CF[i].p[0]) + __builtin_popcountll(CF[i].p[1]), -adv(CF[i])}, (int)i});
  sort(key.begin(), key.end());
  vector<Cfg> o; for (auto &k : key) o.push_back(CF[k.second]); CF.swap(o);
  SORTED.resize(CF.size()); for (size_t i = 0; i < CF.size(); i++) SORTED[i] = i;
  sort(SORTED.begin(), SORTED.end(), [](int a, int b) { return CF[a].p[0] != CF[b].p[0] ? CF[a].p[0] < CF[b].p[0] : CF[a].p[1] < CF[b].p[1]; });
}
static int cidOf(const Cfg &c) {
  int lo = 0, hi = SORTED.size() - 1;
  while (lo <= hi) { int m = (lo + hi) / 2; const Cfg &d = CF[SORTED[m]];
    if (d.p[0] == c.p[0] && d.p[1] == c.p[1]) return SORTED[m];
    if (d.p[0] < c.p[0] || (d.p[0] == c.p[0] && d.p[1] < c.p[1])) lo = m + 1; else hi = m - 1; }
  fprintf(stderr, "configuration not in closure\n"); exit(2);
}
// per-block memo of successor configuration ids
static int MEMO_CI = -1; static vector<int> MEMO; static vector<int> MEMOST; static int STAMP = 0;
static int succId(int ci, int key, const Cfg &d) {
  if (ci != MEMO_CI) { MEMO_CI = ci; STAMP++; }
  if (MEMOST[key] == STAMP) return MEMO[key];
  MEMOST[key] = STAMP; return MEMO[key] = cidOf(d);
}

// ---- D-game component ----
struct Opt { int to; bool acc; };   // to >= 0 T-state; -1 White terminal win; -2 Black terminal win
struct TState { vector<Opt> L, R; };
struct Game { bool sum; int hero; vector<TState> T; vector<int> lay; };  // lay[t]: value layer of T-state t
static vector<vector<BB>> LAYER;  // per T-state, bits [ci*WPC + idx/64]
static inline bool getb(int t, int ci, int idx) { return (LAYER[t][(size_t)ci * WPC + (idx >> 6)] >> (idx & 63)) & 1ULL; }
static inline void setb(int t, int ci, int idx) { LAYER[t][(size_t)ci * WPC + (idx >> 6)] |= 1ULL << (idx & 63); }
static inline int IDX(int stm, int wk, int bk) { return stm * HALF + wk * NSQ + bk; }

static bool legalState(const Cfg &c, int stm, int wk, int bk) {
  BB all = c.p[0] | c.p[1];
  if (wk == bk || kadj(wk, bk) || on(all, wk) || on(all, bk)) return false;
  int ko = stm ? wk : bk;  // the side not to move may not be in check
  return !(c.p[stm] & PA[stm][ko]);
}
static inline bool inCheck(const Cfg &c, int stm, int wk, int bk) { int k = stm ? bk : wk; return c.p[1 - stm] & PA[1 - stm][k]; }

static bool heroWins(const Game &G, int ci, int t, int stm, int wk, int bk, int ep);

// Enumerate the moves of state (ci, t, stm, wk, bk, ep).  cb(internalIdx, acc, extHeroWins): internalIdx >= 0 for a
// move that stays in the block (ci, t) (king move without capture, or a T move t -> t), else extHeroWins is the
// solved result.  Returns the number of moves.
template <class F> static int gen(const Game &G, int ci, int t, int stm, int wk, int bk, int ep, F cb) {
  const Cfg &c = CF[ci]; int n = 0;
  int k = stm ? bk : wk, ok = stm ? wk : bk, x = stm, y = 1 - stm;
  BB own = c.p[x], opp = c.p[y], all = own | opp;
  // king moves
  BB tg = KN[k] & ~own & ~KN[ok];
  for (; tg; tg &= tg - 1) {
    int s = __builtin_ctzll(tg); if (s == ok) continue;
    if (on(opp, s)) {
      Cfg d = c; d.p[y] &= ~(1ULL << s);
      if (d.p[y] & PA[y][s]) continue;
      int ci2 = succId(ci, HALF + s, d);
      int nwk = stm ? wk : s, nbk = stm ? s : bk; n++;
      cb(-1, false, heroWins(G, ci2, t, y, nwk, nbk, -1));
    } else {
      if (opp & PA[y][s]) continue;
      int nwk = stm ? wk : s, nbk = stm ? s : bk; n++;
      cb(IDX(y, nwk, nbk), false, false);
    }
  }
  // pawn moves
  int dr = x ? -1 : 1;
  for (BB pw = own; pw; pw &= pw - 1) {
    int s = __builtin_ctzll(pw), r = RK(s), r1 = r + dr;
    if (r1 < 0 || r1 >= H) continue;
    auto go = [&](int to, int cap, bool dbl) {
      Cfg d = c; d.p[x] &= ~(1ULL << s); if (cap >= 0) d.p[y] &= ~(1ULL << cap);
      bool prom = RK(to) == lastRank(x);
      if (!prom) d.p[x] |= 1ULL << to;
      if (d.p[y] & PA[y][k]) return;  // own king left in check
      n++;
      if (prom) { cb(-1, false, stm == G.hero); return; }
      int ci2 = succId(ci, s * NSQ + to, d);
      int e2 = -1;
      if (dbl) { int pass = (r + dr) * W + FL(s); if (d.p[y] & PA[y][pass]) e2 = pass; }
      cb(-1, false, heroWins(G, ci2, t, y, wk, bk, e2));
    };
    int t1 = r1 * W + FL(s);
    if (!on(all, t1) && t1 != wk && t1 != bk) {
      go(t1, -1, false);
      if (r == startRank(x)) { int t2 = (r1 + dr) * W + FL(s); if (!on(all, t2) && t2 != wk && t2 != bk) go(t2, -1, true); }
    }
    for (int d = -1; d <= 1; d += 2) { int g; if (!fstep(FL(s), d, g)) continue; int tt = r1 * W + g;
      if (on(opp, tt)) go(tt, tt, false);
      else if (tt == ep) go(tt, r * W + g, false); }
  }
  // T moves (sum rule): not while in check; they clear the e.p. right
  if (G.sum && !inCheck(c, stm, wk, bk)) {
    const vector<Opt> &op = stm ? G.T[t].R : G.T[t].L;
    for (const Opt &o : op) {
      n++;
      if (o.to == -1) cb(-1, false, G.hero == 0);
      else if (o.to == -2) cb(-1, false, G.hero == 1);
      else if (o.to == t) cb(IDX(y, wk, bk), o.acc, false);
      else cb(-1, false, getb(G.lay[o.to], ci, IDX(y, wk, bk)));
    }
  }
  return n;
}
static bool noMoveHeroWins(const Game &G, const Cfg &c, int stm, int wk, int bk) {
  if (G.sum) return stm != G.hero;                     // a side with no move loses
  return inCheck(c, stm, wk, bk) && stm != G.hero;      // P: checkmate loses, stalemate draws
}
// value of a solved state; a state with a usable e.p. right by one ply
static bool heroWins(const Game &G, int ci, int t, int stm, int wk, int bk, int ep) {
  if (ep < 0) return getb(G.lay[t], ci, IDX(stm, wk, bk));
  bool any = false, all = true;
  int n = gen(G, ci, t, stm, wk, bk, ep, [&](int ii, bool, bool v) { bool w = ii >= 0 ? getb(G.lay[t], ci, ii) : v; if (w) any = true; else all = false; });
  if (n == 0) return noMoveHeroWins(G, CF[ci], stm, wk, bk);
  return stm == G.hero ? any : all;
}

// ---- block solver ----
static vector<int> EOFF, ETG, POFF, PSRC, CNT; static vector<char> EACC, LEG, GEX, BEX, TERMG, NM, X, Y;
static long long BUCHI_ITERS = 0;
static void solveBlock(const Game &G, int ci, int t) {
  const Cfg &c = CF[ci];
  EOFF.assign(NS + 1, 0); ETG.clear(); EACC.clear();
  bool anyAcc = false;
  for (int idx = 0; idx < NS; idx++) {
    int stm = idx / HALF, wk = (idx % HALF) / NSQ, bk = idx % NSQ;
    LEG[idx] = legalState(c, stm, wk, bk); GEX[idx] = BEX[idx] = TERMG[idx] = NM[idx] = 0;
    if (LEG[idx]) {
      bool hero = stm == G.hero;
      int n = gen(G, ci, t, stm, wk, bk, -1, [&](int ii, bool acc, bool v) {
        if (ii >= 0) { if (LEG[ii] || true) { ETG.push_back(ii); EACC.push_back(acc); if (acc) anyAcc = true; } }
        else if (hero) { if (v) GEX[idx] = 1; } else { if (!v) BEX[idx] = 1; } });
      if (n == 0) { NM[idx] = 1; TERMG[idx] = noMoveHeroWins(G, c, stm, wk, bk); }
    }
    EOFF[idx + 1] = ETG.size();
  }
  // predecessor lists over non-accepting internal edges
  POFF.assign(NS + 1, 0);
  for (int s = 0; s < NS; s++) for (int e = EOFF[s]; e < EOFF[s + 1]; e++) if (!EACC[e]) POFF[ETG[e] + 1]++;
  for (int s = 0; s < NS; s++) POFF[s + 1] += POFF[s];
  PSRC.assign(POFF[NS], 0); { vector<int> fill(POFF.begin(), POFF.end() - 1);
    for (int s = 0; s < NS; s++) for (int e = EOFF[s]; e < EOFF[s + 1]; e++) if (!EACC[e]) PSRC[fill[ETG[e]]++] = s; }
  for (int s = 0; s < NS; s++) Y[s] = LEG[s];
  vector<int> q; q.reserve(NS);
  while (true) {
    BUCHI_ITERS++;
    q.clear();
    for (int s = 0; s < NS; s++) {
      X[s] = 0; if (!LEG[s]) continue;
      int stm = s / HALF;
      if (stm == G.hero) {
        bool g = GEX[s];
        for (int e = EOFF[s]; e < EOFF[s + 1] && !g; e++) if (EACC[e] && Y[ETG[e]]) g = true;
        if (g) { X[s] = 1; q.push_back(s); }
      } else {
        if (NM[s]) { if (TERMG[s]) { X[s] = 1; q.push_back(s); } continue; }
        CNT[s] = EOFF[s + 1] - EOFF[s];
        if (!BEX[s] && CNT[s] == 0) { X[s] = 1; q.push_back(s); }
      }
    }
    for (size_t h = 0; h < q.size(); h++) {
      int u = q[h];
      for (int e = POFF[u]; e < POFF[u + 1]; e++) {
        int p = PSRC[e]; if (X[p] || !LEG[p]) continue;
        if (p / HALF == G.hero) { X[p] = 1; q.push_back(p); }
        else if (!BEX[p] && --CNT[p] == 0) { X[p] = 1; q.push_back(p); }
      }
    }
    bool changed = false;
    for (int s = 0; s < NS; s++) if (X[s] != Y[s]) { changed = true; Y[s] = X[s]; }
    if (!anyAcc || !changed) break;
  }
  for (int s = 0; s < NS; s++) if (Y[s]) setb(G.lay[t], ci, s);
}
static void allocLayer(int t) { LAYER[t].assign((size_t)CF.size() * WPC, 0ULL); }
static void freeLayer(int t) { vector<BB>().swap(LAYER[t]); }
static void solveLayer(const Game &G, int t) { allocLayer(G.lay[t]); for (size_t ci = 0; ci < CF.size(); ci++) solveBlock(G, ci, t); }

// ---- positions and move lists for the checks ----
struct Pos { Cfg c; int wk, bk, stm, ep; };
struct NMv { string name; Pos q; bool prom; };
static string show(const Pos &p) {
  string o = "K" + SN(p.wk) + " k" + SN(p.bk);
  for (int s = 0; s < NSQ; s++) if (on(p.c.p[0], s)) o += " P" + SN(s);
  for (int s = 0; s < NSQ; s++) if (on(p.c.p[1], s)) o += " p" + SN(s);
  o += p.stm ? " b " : " w "; o += p.ep >= 0 ? SN(p.ep) : "-"; return o;
}
static vector<NMv> listMoves(const Pos &p) {
  vector<NMv> out; const Cfg &c = p.c; int stm = p.stm, x = stm, y = 1 - stm;
  int k = stm ? p.bk : p.wk, ok = stm ? p.wk : p.bk; BB own = c.p[x], opp = c.p[y], all = own | opp;
  char kc = stm ? 'k' : 'K', pc = stm ? 'p' : 'P';
  for (BB tg = KN[k] & ~own & ~KN[ok]; tg; tg &= tg - 1) { int s = __builtin_ctzll(tg); if (s == ok) continue;
    Cfg d = c; d.p[y] &= ~(1ULL << s); if (d.p[y] & PA[y][s]) continue;
    Pos q{d, stm ? p.wk : s, stm ? s : p.bk, y, -1}; out.push_back({string(1, kc) + SN(k) + SN(s), q, false}); }
  int dr = x ? -1 : 1;
  for (BB pw = own; pw; pw &= pw - 1) { int s = __builtin_ctzll(pw), r = RK(s), r1 = r + dr; if (r1 < 0 || r1 >= H) continue;
    auto go = [&](int to, int cap, bool dbl) { Cfg d = c; d.p[x] &= ~(1ULL << s); if (cap >= 0) d.p[y] &= ~(1ULL << cap);
      bool prom = RK(to) == lastRank(x); if (!prom) d.p[x] |= 1ULL << to; if (d.p[y] & PA[y][k]) return;
      int e2 = -1; if (dbl) { int pass = (r + dr) * W + FL(s); if (d.p[y] & PA[y][pass]) e2 = pass; }
      out.push_back({string(1, pc) + SN(s) + SN(to), Pos{d, p.wk, p.bk, y, e2}, prom}); };
    int t1 = r1 * W + FL(s);
    if (!on(all, t1) && t1 != p.wk && t1 != p.bk) { go(t1, -1, false);
      if (r == startRank(x)) { int t2 = (r1 + dr) * W + FL(s); if (!on(all, t2) && t2 != p.wk && t2 != p.bk) go(t2, -1, true); } }
    for (int d = -1; d <= 1; d += 2) { int g; if (!fstep(FL(s), d, g)) continue; int tt = r1 * W + g;
      if (on(opp, tt)) go(tt, tt, false); else if (tt == p.ep) go(tt, r * W + g, false); } }
  return out;
}
static bool HW(const Game &G, int t, const Pos &p) { return heroWins(G, cidOf(p.c), t, p.stm, p.wk, p.bk, p.ep); }
// print every move of p in game G at T-state t with "does White win after it" (for explanations)
static void explain(const Game &G, int t, const Pos &p, const char *label) {
  string o = string("   ") + label + " " + show(p) + " :";
  for (auto &m : listMoves(p)) { bool w = m.prom ? (p.stm == 0) : HW(G, t, m.q); o += " " + m.name + "=" + (w ? "W" : "notW"); }
  if (!inCheck(p.c, p.stm, p.wk, p.bk)) for (const Opt &op : (p.stm ? G.T[t].R : G.T[t].L)) {
    Pos q = p; q.stm = 1 - p.stm; q.ep = -1; bool w = op.to == -1 ? true : op.to == -2 ? false : HW(G, op.to, q);
    o += string(" ") + (p.stm ? "T-move" : (op.acc ? "pass" : "T-move")) + "=" + (w ? "W" : "notW"); }
  printf("%s\n", o.c_str());
}

int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage: ax65 BOARD \"PIECES\" Z0 Z1 [--lmax N] [--noladder] [--noaux] [--noP] [--limit BYTES]\n"); return 2; }
  string b = argv[1]; CYL = b.rfind("cyl:", 0) == 0; sscanf(b.c_str() + b.find(':') + 1, "%dx%d", &W, &H);
  if (W * H > 64) { fprintf(stderr, "board too big\n"); return 2; }
  initBoard();
  int lmax = 8; bool doLadder = true, doAux = true, doP = true;
  for (int i = 5; i < argc; i++) { string a = argv[i];
    if (a == "--lmax") lmax = atoi(argv[++i]); else if (a == "--noladder") doLadder = false; else if (a == "--noaux") doAux = false;
    else if (a == "--noP") doP = false; else if (a == "--limit") LIMIT = atof(argv[++i]); }
  Pos base{}; base.ep = -1; { stringstream ss(argv[2]); string x;
    while (ss >> x) { int s = PS(x.substr(1)); if (x[0] == 'K') base.wk = s; else if (x[0] == 'k') base.bk = s; else if (x[0] == 'P') base.c.p[0] |= 1ULL << s; else if (x[0] == 'p') base.c.p[1] |= 1ULL << s; } }
  int z[2] = {PS(argv[3]), PS(argv[4])};
  if (base.bk != z[0]) { fprintf(stderr, "Black king must stand on Z0\n"); return 2; }
  printf("ax65 %s  %s  shuttle %s-%s\n", argv[1], argv[2], argv[3], argv[4]);
  closure(base.c);
  double layerB = (double)CF.size() * WPC * 8;
  int maxLayers = doLadder ? 4 : 2;
  double need = maxLayers * layerB + CF.size() * 64.0 + 40e6;
  printf("configurations %zu, states per layer %.0f, bytes per layer %.0f, peak layers %d, estimated peak %.0f bytes\n", CF.size(), (double)CF.size() * NS, layerB, maxLayers, need);
  if (need > LIMIT) { printf("ABORT: estimated memory %.0f exceeds the limit %.0f\n", need, LIMIT); return 3; }
  fflush(stdout);
  MEMO.assign(HALF + NSQ, 0); MEMOST.assign(HALF + NSQ, 0);
  EOFF.reserve(NS + 1); LEG.assign(NS, 0); GEX.assign(NS, 0); BEX.assign(NS, 0); TERMG.assign(NS, 0); NM.assign(NS, 0); X.assign(NS, 0); Y.assign(NS, 0); CNT.assign(NS, 0);
  Pos root[2][2];
  for (int a = 0; a < 2; a++) for (int s = 0; s < 2; s++) { root[a][s] = base; root[a][s].bk = z[a]; root[a][s].stm = s; }
  int fails = 0;
  auto FAIL = [&](const string &m) { printf("FAIL %s\n", m.c_str()); fails++; };
  BB all0 = base.c.p[0] | base.c.p[1];
  for (int a = 0; a < 2; a++) {
    if (on(all0, z[a]) || z[a] == base.wk) FAIL("z square occupied");
    for (int s = 0; s < 2; s++) { if (!legalState(base.c, s, base.wk, z[a])) FAIL("root " + SN(z[a]) + " illegal"); if (inCheck(base.c, s, base.wk, z[a])) FAIL("king in check at root " + SN(z[a])); }
  }
  if (!kadj(z[0], z[1])) FAIL("z not adjacent");
  vector<pair<Pos, string>> bad;  // non-shuttle Black root moves
  // ---------------- Definition 4.8 in P ----------------
  Game PW{false, 0, {TState{}}, {0}}, PB{false, 1, {TState{}}, {1}};
  LAYER.assign(4, {});
  for (int a = 0; a < 2; a++) for (auto &m : listMoves(root[a][1])) {
    bool shut = m.name[0] == 'k' && m.q.bk == z[1 - a] && m.q.c.p[0] == base.c.p[0];
    if (!shut) bad.push_back({m.q, m.name + "@" + SN(z[a])});
  }
  if (doP) {
    // PW in layer 0 (hero White), PB in layer 1 (hero Black)
    solveLayer(PW, 0); solveLayer(PB, 0);
    auto PV = [&](const Pos &p) -> char { bool w = HW(PW, 0, p), l = HW(PB, 0, p); return w ? 'W' : l ? 'L' : 'D'; };
    // ---- K68 query block ----
    if (getenv("AX68_QUERY")) {
      FILE *f = fopen(getenv("AX68_QUERY"), "r"); char buf[512];
      while (f && fgets(buf, sizeof buf, f)) {
        if (buf[0] == '#' || buf[0] == '\n') continue;
        char wk[8], bk[8], wp[128], bp[128], sd[8];
        if (sscanf(buf, "%7s %7s %127s %127s %7s", wk, bk, wp, bp, sd) != 5) continue;
        Pos q{}; q.ep = -1; q.wk = PS(wk); q.bk = PS(bk); q.stm = sd[0] == 'b';
        for (int x = 0; x < 2; x++) { string l = x ? bp : wp; if (l == "-") continue; stringstream ss(l); string t;
          while (getline(ss, t, ',')) q.c.p[x] |= 1ULL << PS(t); }
        if (!legalState(q.c, q.stm, q.wk, q.bk)) { printf("%s %s %s %s %s : illegal\n", wk, bk, wp, bp, sd); continue; }
        printf("%s %s %s %s %s : %c\n", wk, bk, wp, bp, sd, PV(q));
      }
      printf("done\n"); return 0;
    }
    // ---- end K68 ----
    for (int a = 0; a < 2; a++) {
      Pos p = root[a][1]; auto mv = listMoves(p); bool shut = false;
      printf("root %s : P=%c, %zu moves\n", show(p).c_str(), PV(p), mv.size());
      for (auto &m : mv) {
        bool isS = m.name[0] == 'k' && m.q.bk == z[1 - a] && m.q.c.p[0] == base.c.p[0];
        char v = m.prom ? 'L' : PV(m.q);
        printf("   %-7s P(after)=%c%s%s\n", m.name.c_str(), v, isS ? "  shuttle" : "", inCheck(m.q.c, 0, m.q.wk, m.q.bk) ? "  check" : "");
        if (isS) { shut = true; continue; }
        if (v != 'W') FAIL("(O1) " + m.name + " at " + SN(z[a]));
      }
      if (!shut) FAIL("(O1) shuttle illegal at " + SN(z[a]));
      p = root[a][0]; mv = listMoves(p); int nf = 0;
      printf("root %s : P=%c, %zu moves\n", show(p).c_str(), PV(p), mv.size());
      for (auto &m : mv) {
        char v = m.prom ? 'W' : PV(m.q); bool fr = v != 'L';
        printf("   %-7s P(after)=%c%s%s\n", m.name.c_str(), v, m.prom ? " promotion" : "", fr ? "  FREEZE" : "");
        if (!fr) continue; nf++;
        if (m.prom) { FAIL("freeze is a promotion"); continue; }
        Pos q = m.q;
        printf("   freeze %s at %s -> q = %s\n", m.name.c_str(), SN(z[a]).c_str(), show(q).c_str());
        if (inCheck(q.c, 1, q.wk, q.bk)) FAIL("freezing move gives check (" + m.name + ")");
        for (int withRight = 1; withRight >= 0; withRight--) {
          Pos qq = q; if (!withRight) qq.ep = -1; else if (q.ep < 0) continue;
          auto mq = listMoves(qq); bool ok = !mq.empty(); string ls;
          for (auto &mm : mq) { char vv = mm.prom ? 'L' : PV(mm.q); ls += " " + mm.name + "=" + vv; if (vv != 'W') ok = false; }
          printf("      q Black to move%s: every move loses at once: %s  [%s ]\n", withRight ? " with the right" : "", ok ? "yes" : "NO", ls.c_str());
          if (!ok) FAIL("(O3) at q after " + m.name);
        }
        Pos qw = q; qw.stm = 0; qw.ep = -1;
        if (!legalState(qw.c, 0, qw.wk, qw.bk)) { FAIL("(O4) q with White to move illegal"); continue; }
        auto mw = listMoves(qw); bool ok = !mw.empty(); string ls;
        for (auto &mm : mw) { char vv = mm.prom ? 'W' : PV(mm.q); ls += " " + mm.name + "=" + vv; if (vv != 'L') ok = false; }
        printf("      q White to move: every move loses at once: %s  [%s ]\n", ok ? "yes" : "NO", ls.c_str());
        if (!ok) FAIL("(O4) at q after " + m.name);
      }
      if (!nf) FAIL("(O2) no freeze at " + SN(z[a]));
    }
    printf("DEFINITION 4.8 (over): %s (%d failures)\n", fails ? "NOT exact" : "exact", fails);
    freeLayer(0); freeLayer(1);
  }
  fflush(stdout);
  // ---------------- sums ----------------
  // T-states: 0 = zero (no moves); 1 = -1 (Black -> 0); 2 = under (White pass, accepting; Black -> 0)
  Game S{true, 0, {}, {0, 1, 2}};
  S.T.resize(3); S.T[1].R = {{0, false}}; S.T[2].L = {{2, true}}; S.T[2].R = {{0, false}};
  solveLayer(S, 0);
  solveLayer(S, 1);
  int nB1fail = 0;
  vector<int> b1(bad.size());
  for (size_t i = 0; i < bad.size(); i++) { b1[i] = HW(S, 1, bad[i].first);
    printf("B1 %-12s x_m = %s : beside -1 %s ; beside 0 %s\n", bad[i].second.c_str(), show(bad[i].first).c_str(), b1[i] ? "WHITE WIN" : "not a White win", HW(S, 0, bad[i].first) ? "W" : "not W");
    if (!b1[i]) nB1fail++; }
  printf("(B1): %zu non-shuttle Black root moves, %d not a White win beside -1\n", bad.size(), nB1fail);
  for (size_t i = 0; i < bad.size(); i++) if (!b1[i]) {
    printf("explain (B1) at %s: beside -1, White to move, then Black to move after each White move\n", bad[i].second.c_str());
    explain(S, 1, bad[i].first, "x_m beside -1, White to move:");
    for (auto &m : listMoves(bad[i].first)) if (!m.prom) explain(S, 1, m.q, ("after " + m.name + ", beside -1:").c_str());
    Pos xb = bad[i].first; xb.stm = 1; xb.ep = -1; explain(S, 0, xb, "x_m board, Black to move, beside 0:");
    explain(S, 0, bad[i].first, "x_m beside 0, White to move:");
  }
  freeLayer(1); fflush(stdout);
  vector<int> aux(bad.size(), -1);
  if (doAux) {
    solveLayer(S, 2);
    for (size_t i = 0; i < bad.size(); i++) { aux[i] = HW(S, 2, bad[i].first);
      printf("AUX %-12s : White %s Aux(x_m)%s\n", bad[i].second.c_str(), aux[i] ? "WINS" : "does NOT win", (aux[i] && !b1[i]) ? "  (only by passing: (B1) fails here)" : (!aux[i] && b1[i]) ? "  INCONSISTENT with (B1) => Aux" : ""); }
    for (size_t i = 0; i < bad.size(); i++) if (!b1[i]) {
      printf("explain Aux at %s\n", bad[i].second.c_str());
      explain(S, 2, bad[i].first, "x_m in Aux, White to move:");
      Pos xb = bad[i].first; xb.stm = 1; xb.ep = -1; explain(S, 2, xb, "after the pass, Black to move:");
      for (auto &m : listMoves(xb)) if (!m.prom) explain(S, 2, m.q, ("after pass " + m.name + ", White to move:").c_str());
    }
    printf("Buchi outer iterations so far %lld\n", BUCHI_ITERS); fflush(stdout);
  }
  if (doLadder) {
    // ladder layers: T-state 1 = previous L_{j-1}, T-state 2 = current L_j (moved between iterations); under kept in 3
    if (doAux) LAYER[3].swap(LAYER[2]);
    Game Lg{true, 0, {}, {0, 1, 2}}; Lg.T.resize(3);
    vector<int> firstFail(bad.size(), -1); int rootFail[2] = {-1, -1};
    for (int j = 0; j <= lmax; j++) {
      Lg.T[2].L = {{j == 0 ? -1 : 1, false}}; Lg.T[2].R = {{0, false}};
      solveLayer(Lg, 2);
      string line = "T_" + to_string(j) + ":";
      for (size_t i = 0; i < bad.size(); i++) { bool w = HW(Lg, 2, bad[i].first); if (!w && firstFail[i] < 0) firstFail[i] = j; line += " " + bad[i].second + "=" + (w ? "W" : "notW"); }
      for (int a = 0; a < 2; a++) { bool w = HW(Lg, 2, root[a][1]); if (!w && rootFail[a] < 0) rootFail[a] = j; line += " root" + SN(z[a]) + "(Black to move)=" + (w ? "W" : "notW"); }
      printf("%s\n", line.c_str()); fflush(stdout);
      bool stable = j > 0 && LAYER[1] == LAYER[2];
      if (stable) {
        printf("ladder layers stable from T_%d on (layer T_%d equals T_%d bit for bit)\n", j - 1, j, j - 1);
        if (doAux) printf("stable ladder layer equals the Aux layer: %s\n", LAYER[2] == LAYER[3] ? "yes" : "NO");
        break;
      }
      LAYER[1].swap(LAYER[2]); freeLayer(2);
    }
    for (size_t i = 0; i < bad.size(); i++) printf("LADDER %-12s : %s\n", bad[i].second.c_str(), firstFail[i] < 0 ? "White wins beside every T_N computed" : ("first T_N not won: N = " + to_string(firstFail[i])).c_str());
  }
  printf("done\n");
  return 0;
}
