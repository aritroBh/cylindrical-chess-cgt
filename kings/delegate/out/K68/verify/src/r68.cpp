// r68.cpp -- K68 referee's own solver for the promotion game P of king-and-pawn positions on flat 8x8.
// Written from SPEC rules and the K61 packet section 1, without reading o68.cpp / ax68q.cpp / ax65.cpp.
//
// Layers:   P  = P alone (promotion wins, mate loses, stalemate draws, infinite play draws)
//           S0 = sum rule, nothing beside (no move at all loses, also stalemate)
//           S1 = sum rule beside -1: Black holds one token (a move elsewhere: not in check; clears Black's e.p. right)
// Pawn configurations (white pawns, black pawns, e.p. target) are closed under every pawn move or capture; they form a
// DAG (each pawn move/capture raises a potential), solved from the end; inside one configuration only quiet king moves
// stay, solved by a worklist with predecessors (8 neighbours of the moved king).
//
// Usage: r68 <cmd> [args]   (see main)
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <map>
#include <unordered_map>
#include <algorithm>
#include <set>
typedef uint64_t U64;
using namespace std;

static inline U64 B(int s) { return 1ULL << s; }
static inline int FI(int s) { return s & 7; }
static inline int RA(int s) { return s >> 3; }
static const U64 FA = 0x0101010101010101ULL, FH = FA << 7;
static U64 KATT[64];
static inline U64 wpatt(U64 p) { return ((p & ~FA) << 7) | ((p & ~FH) << 9); }
static inline U64 bpatt(U64 p) { return ((p & ~FH) >> 7) | ((p & ~FA) >> 9); }
static int kdist(int a, int b) { return max(abs(FI(a) - FI(b)), abs(RA(a) - RA(b))); }
static string sqn(int s) { string r; r += char('a' + FI(s)); r += char('1' + RA(s)); return r; }
static int sqp(const char *t) { return (t[0] - 'a') + 8 * (t[1] - '1'); }

struct Cfg { U64 wp, bp; int ep; };  // ep = e.p. target square (the square passed over) or -1
struct CK { bool operator()(const Cfg &a, const Cfg &b) const {
  if (a.wp != b.wp) return a.wp < b.wp; if (a.bp != b.bp) return a.bp < b.bp; return a.ep < b.ep; } };

// a position: side 0 = White, 1 = Black
struct Pos { int wk, bk, stm; Cfg c; int tok; };

enum { UNK = 0, WIN = 1, LOSS = 2, DRAW = 3 };  // from the mover's side

struct Move { int kind; int from, to; };  // kind 0 king, 1 pawn, 2 pass; promo flagged by result
struct Succ { bool promo; bool pass; Pos p; string name; };

static bool incheck(const Pos &p, int side) {
  if (side == 0) return bpatt(p.c.bp) & B(p.wk);
  return wpatt(p.c.wp) & B(p.bk);
}
static bool valid(const Pos &p) {
  if (p.wk == p.bk) return false;
  if (kdist(p.wk, p.bk) < 2) return false;
  U64 occ = p.c.wp | p.c.bp;
  if (occ & (B(p.wk) | B(p.bk))) return false;
  if (incheck(p, 1 - p.stm)) return false;  // side not to move in check
  if (p.c.ep >= 0) { // e.p. only for the side to move right after a double step
    if (p.stm == 1 && RA(p.c.ep) != 2) return false;
    if (p.stm == 0 && RA(p.c.ep) != 5) return false;
  }
  return true;
}

// generate legal successors. allowPass: Black token pass available
static void gen(const Pos &p, vector<Succ> &out) {
  out.clear();
  int s = p.stm;
  U64 own = s == 0 ? p.c.wp : p.c.bp, opp = s == 0 ? p.c.bp : p.c.wp;
  int mk = s == 0 ? p.wk : p.bk, ok = s == 0 ? p.bk : p.wk;
  U64 oppatt = s == 0 ? bpatt(p.c.bp) : wpatt(p.c.wp);
  // king moves
  for (U64 t = KATT[mk]; t; t &= t - 1) {
    int to = __builtin_ctzll(t);
    if (own & B(to)) continue;
    if (kdist(to, ok) < 2) continue;
    Pos q = p; q.c.ep = -1; q.stm = 1 - s;
    if (s == 0) { q.wk = to; q.c.bp &= ~B(to); } else { q.bk = to; q.c.wp &= ~B(to); }
    // attacked by enemy pawns after the capture (a captured pawn no longer attacks)
    U64 att = s == 0 ? bpatt(q.c.bp) : wpatt(q.c.wp);
    if (att & B(to)) continue;
    (void)oppatt;
    out.push_back({false, false, q, string("K") + ((opp & B(to)) ? "x" : "") + sqn(to)});
  }
  // pawn moves
  int dir = s == 0 ? 8 : -8;
  for (U64 t = own; t; t &= t - 1) {
    int fr = __builtin_ctzll(t);
    int lastr = s == 0 ? 7 : 0, startr = s == 0 ? 1 : 6;
    auto add = [&](int to, bool cap, bool epcap, bool dbl) {
      Pos q = p; q.stm = 1 - s; q.c.ep = -1;
      U64 &mo = s == 0 ? q.c.wp : q.c.bp; U64 &mp = s == 0 ? q.c.bp : q.c.wp;
      mo &= ~B(fr);
      if (cap) mp &= ~B(to);
      if (epcap) mp &= ~B(to - dir);
      bool promo = RA(to) == lastr;
      if (!promo) mo |= B(to);
      if (dbl) {
        // e.p. right only if an enemy pawn can actually capture (stands beside the arrival square)
        int arr = to; U64 adj = 0;
        if (FI(arr) > 0) adj |= B(arr - 1); if (FI(arr) < 7) adj |= B(arr + 1);
        if (adj & mp) q.c.ep = fr + dir;
      }
      if (incheck(q, s)) return;  // own king in check after the move
      string nm = string(sqn(fr)) + (cap || epcap ? "x" : "-") + sqn(to) + (promo ? "=" : "") + (epcap ? "ep" : "");
      out.push_back({promo, false, q, nm});
    };
    int to = fr + dir;
    if (to < 0 || to > 63) continue;
    U64 occ = p.c.wp | p.c.bp | B(p.wk) | B(p.bk);
    if (!(occ & B(to))) {
      add(to, false, false, false);
      if (RA(fr) == startr && !(occ & B(to + dir))) add(to + dir, false, false, true);
    }
    for (int df = -1; df <= 1; df += 2) {
      if (FI(fr) + df < 0 || FI(fr) + df > 7) continue;
      int c = to + df;
      if (opp & B(c)) add(c, true, false, false);
      else if (c == p.c.ep) add(c, false, true, false);
    }
  }
  // token pass (Black only)
  if (s == 1 && p.tok && !incheck(p, 1)) {
    Pos q = p; q.stm = 0; q.tok = 0; q.c.ep = -1;
    out.push_back({false, true, q, "pass"});
  }
}

// ---------------- configuration closure ----------------
static map<Cfg, int, CK> cid;
static vector<Cfg> cfgs;
static int addcfg(const Cfg &c) {
  auto it = cid.find(c); if (it != cid.end()) return it->second;
  int id = cfgs.size(); cid[c] = id; cfgs.push_back(c); return id;
}
static void closure(const Cfg &root) {
  vector<int> st; st.push_back(addcfg(root)); {Cfg c = root; c.ep = -1; st.push_back(addcfg(c));}
  while (!st.empty()) {
    Cfg c = cfgs[st.back()]; st.pop_back();
    for (int s = 0; s < 2; s++) {
      U64 own = s == 0 ? c.wp : c.bp, opp = s == 0 ? c.bp : c.wp;
      int dir = s == 0 ? 8 : -8, lastr = s == 0 ? 7 : 0, startr = s == 0 ? 1 : 6;
      auto push = [&](Cfg n) { size_t before = cfgs.size(); int id = addcfg(n); if ((size_t)id == before) st.push_back(id);
        if (n.ep >= 0) { Cfg m = n; m.ep = -1; size_t b2 = cfgs.size(); int id2 = addcfg(m); if ((size_t)id2 == b2) st.push_back(id2); } };
      // king captures of enemy pawns (either king can take any pawn of the other side)
      for (U64 t = opp; t; t &= t - 1) { int x = __builtin_ctzll(t); Cfg n = c; n.ep = -1;
        if (s == 0) n.bp &= ~B(x); else n.wp &= ~B(x); push(n); }
      for (U64 t = own; t; t &= t - 1) {
        int fr = __builtin_ctzll(t), to = fr + dir;
        if (to < 0 || to > 63) continue;
        U64 occ = c.wp | c.bp;
        auto mk = [&](int dest, bool cap, bool epc, bool dbl) {
          Cfg n = c; n.ep = -1; U64 &mo = s == 0 ? n.wp : n.bp; U64 &mp = s == 0 ? n.bp : n.wp;
          mo &= ~B(fr); if (cap) mp &= ~B(dest); if (epc) mp &= ~B(dest - dir);
          if (RA(dest) == lastr) { push(n); return; }  // promotion: the board without the pawn is never needed, harmless
          mo |= B(dest);
          if (dbl) { U64 adj = 0; if (FI(dest) > 0) adj |= B(dest - 1); if (FI(dest) < 7) adj |= B(dest + 1); if (adj & mp) n.ep = fr + dir; }
          push(n);
        };
        if (!(occ & B(to))) { mk(to, false, false, false); if (RA(fr) == startr && !(occ & B(to + dir))) mk(to + dir, false, false, true); }
        for (int df = -1; df <= 1; df += 2) {
          if (FI(fr) + df < 0 || FI(fr) + df > 7) continue;
          int x = to + df; if (opp & B(x)) mk(x, true, false, false); else if (x == c.ep) mk(x, false, true, false);
        }
      }
    }
  }
}
static int potential(const Cfg &c) {
  int v = 0;
  for (U64 t = c.wp; t; t &= t - 1) v += RA(__builtin_ctzll(t));
  for (U64 t = c.bp; t; t &= t - 1) v += 7 - RA(__builtin_ctzll(t));
  v += 10 * (10 - __builtin_popcountll(c.wp | c.bp));
  return v;
}

// ---------------- solving ----------------
// layer: 0 = P alone, 1 = sum rule no token, 2 = sum rule with Black token
static vector<vector<uint8_t>> VAL[3];
static vector<vector<uint8_t>> DTM[3];
static vector<char> solved[3];
static inline int sidx(int stm, int wk, int bk) { return stm * 4096 + wk * 64 + bk; }

static int lookupv(const Pos &q, int layer, uint8_t *d) {
  int L = layer == 0 ? 0 : (q.tok ? 2 : 1);
  auto it = cid.find(q.c);
  if (it == cid.end()) { fprintf(stderr, "missing cfg\n"); exit(2); }
  int c = it->second;
  if (VAL[L][c].empty()) { fprintf(stderr, "cfg not solved\n"); exit(3); }
  int i = sidx(q.stm, q.wk, q.bk);
  if (d) *d = DTM[L][c][i];
  return VAL[L][c][i];
}

static void solvecfg(int c, int L) {
  VAL[L][c].assign(8192, UNK);
  DTM[L][c].assign(8192, 255);
  vector<uint8_t> &V = VAL[L][c];
  vector<int> work;
  vector<Succ> mv;
  vector<char> isvalid(8192, 0);
  for (int i = 0; i < 8192; i++) {
    Pos p{(i >> 6) & 63, i & 63, i >> 12, cfgs[c], L == 2 ? 1 : 0};
    if (L == 2 && p.stm == 0) p.tok = 1;
    if (valid(p)) { isvalid[i] = 1; work.push_back(i); }
  }
  auto evalst = [&](int i) -> int {
    Pos p{(i >> 6) & 63, i & 63, i >> 12, cfgs[c], L == 2 ? 1 : 0};
    gen(p, mv);
    if (mv.empty()) {
      if (incheck(p, p.stm)) return LOSS;
      return L == 0 ? DRAW : LOSS;
    }
    bool allwin = true;
    for (auto &m : mv) {
      if (m.promo) return WIN;
      int v = lookupv(m.p, L, nullptr);
      if (v == LOSS) return WIN;
      if (v != WIN) allwin = false;
    }
    return allwin ? LOSS : UNK;
  };
  while (!work.empty()) {
    int i = work.back(); work.pop_back();
    if (V[i] != UNK) continue;
    int v = evalst(i);
    if (v == UNK) continue;
    V[i] = v;
    if (v == DRAW) continue;
    // predecessors in this cfg: other side's king moved quietly into its square
    int stm = i >> 12, wk = (i >> 6) & 63, bk = i & 63;
    int ps = 1 - stm;
    int moved = ps == 0 ? wk : bk;
    for (U64 t = KATT[moved]; t; t &= t - 1) {
      int fr = __builtin_ctzll(t);
      int j = ps == 0 ? sidx(0, fr, bk) : sidx(1, wk, fr);
      if (isvalid[j] && V[j] == UNK) work.push_back(j);
    }
  }
  for (int i = 0; i < 8192; i++) if (isvalid[i] && V[i] == UNK) V[i] = DRAW;
  // distances (plies to the end with optimal play: win fastest, lose slowest), Bellman relaxation inside the cfg
  vector<uint8_t> &D = DTM[L][c];
  bool ch = true; int rounds = 0;
  while (ch && rounds < 300) {
    ch = false; rounds++;
    for (int i = 0; i < 8192; i++) {
      if (!isvalid[i] || V[i] == DRAW) continue;
      Pos p{(i >> 6) & 63, i & 63, i >> 12, cfgs[c], L == 2 ? 1 : 0};
      gen(p, mv);
      int nd;
      if (mv.empty()) nd = 0;
      else if (V[i] == WIN) {
        nd = 255;
        for (auto &m : mv) { if (m.promo) { nd = 1; break; } uint8_t d; int v = lookupv(m.p, L, &d); if (v == LOSS && d < 255) nd = min(nd, d + 1); }
      } else {
        nd = 0;
        for (auto &m : mv) { uint8_t d; lookupv(m.p, L, &d); if (d == 255) { nd = 255; break; } nd = max(nd, d + 1); }
      }
      if (nd > 254) nd = 255;
      if (nd != D[i]) { D[i] = nd; ch = true; }
    }
  }
}

static void solveall(int L) {
  vector<int> ord(cfgs.size());
  for (size_t i = 0; i < cfgs.size(); i++) ord[i] = i;
  sort(ord.begin(), ord.end(), [](int a, int b) {
    int pa = potential(cfgs[a]), pb = potential(cfgs[b]);
    if (pa != pb) return pa > pb;
    return cfgs[a].ep < cfgs[b].ep;  // ep = -1 (none) first: e.p. cfgs lead to their none cfg
  });
  VAL[L].assign(cfgs.size(), {}); DTM[L].assign(cfgs.size(), {});
  for (int c : ord) solvecfg(c, L);
}

// ---------------- FEN ----------------
static Pos fromfen(const string &fen, int tok = 0) {
  Pos p{}; p.c.wp = p.c.bp = 0; p.c.ep = -1; p.tok = tok;
  int r = 7, f = 0; size_t i = 0;
  for (; i < fen.size() && fen[i] != ' '; i++) {
    char ch = fen[i];
    if (ch == '/') { r--; f = 0; continue; }
    if (ch >= '1' && ch <= '8') { f += ch - '0'; continue; }
    int s = f + 8 * r;
    if (ch == 'K') p.wk = s; else if (ch == 'k') p.bk = s; else if (ch == 'P') p.c.wp |= B(s); else if (ch == 'p') p.c.bp |= B(s);
    else { fprintf(stderr, "bad fen piece\n"); exit(1); }
    f++;
  }
  i++; p.stm = (i < fen.size() && fen[i] == 'b') ? 1 : 0;
  return p;
}
static string tofen(const Pos &p) {
  string s;
  for (int r = 7; r >= 0; r--) {
    int e = 0;
    for (int f = 0; f < 8; f++) {
      int q = f + 8 * r; char ch = 0;
      if (q == p.wk) ch = 'K'; else if (q == p.bk) ch = 'k'; else if (p.c.wp & B(q)) ch = 'P'; else if (p.c.bp & B(q)) ch = 'p';
      if (!ch) { e++; continue; }
      if (e) { s += char('0' + e); e = 0; } s += ch;
    }
    if (e) s += char('0' + e);
    if (r) s += '/';
  }
  s += p.stm ? " b" : " w";
  return s;
}
static const char *vs(int v) { return v == WIN ? "W" : v == LOSS ? "L" : v == DRAW ? "D" : "?"; }
// value from White's side: W / L / D
static string wval(const Pos &p, int L) {
  uint8_t d; int v = lookupv(p, L, &d);
  char buf[32];
  int w = v == DRAW ? DRAW : ((v == WIN) == (p.stm == 0) ? WIN : LOSS);
  snprintf(buf, sizeof buf, "%s%d", vs(w), v == DRAW ? 0 : (int)d);
  return buf;
}

// ---------------- Lemma A: White's strategy S_A played literally against every Black reply ----------------
struct SAStats {
  long leaves = 0, fails = 0, maxn = 0, blackStalemate = 0, a2fail = 0, earlyC5 = 0, rank7before = 0, rankAtKxb7 = 0;
  long qcapt = 0, chessStale = 0, pawnRankBad = 0;
  map<int, long> promoAt;           // White move number of the promotion
  set<string> leavesChess;          // positions after b8=Q (Black to move), queen written as Q
  map<int, long> pawnRankAtPromo;   // rank (1..8) of Black's c-pawn at the promotion (0 = no pawn)
  vector<string> failMsg;
};
static U64 queenAtt(int q, U64 occ) {
  U64 a = 0; int dr[8] = {1, 1, 1, 0, 0, -1, -1, -1}, df[8] = {-1, 0, 1, -1, 1, -1, 0, 1};
  for (int d = 0; d < 8; d++) { int r = RA(q) + dr[d], f = FI(q) + df[d];
    while (r >= 0 && r < 8 && f >= 0 && f < 8) { int s = f + 8 * r; a |= B(s); if (occ & B(s)) break; r += dr[d]; f += df[d]; } }
  return a;
}
// chess legality after b8=Q: Black to move; queen on qs. Returns number of legal Black moves; sets chk.
static int chessBlackMoves(const Pos &p, int qs, bool &chk) {
  U64 occ = p.c.wp | p.c.bp | B(p.wk) | B(qs);
  U64 wq = queenAtt(qs, occ);  // with the Black king on the board as a blocker: only for the check test
  chk = (wq & B(p.bk)) || (wpatt(p.c.wp) & B(p.bk));
  U64 occNoK = p.c.wp | p.c.bp | B(p.wk) | B(qs);
  int n = 0;
  for (U64 t = KATT[p.bk]; t; t &= t - 1) {
    int to = __builtin_ctzll(t);
    if (p.c.bp & B(to)) continue;
    if (kdist(to, p.wk) < 2) continue;
    U64 wp2 = p.c.wp & ~B(to);
    bool capQ = to == qs;
    if (wpatt(wp2) & B(to)) continue;
    if (!capQ && (queenAtt(qs, (occNoK & ~B(to))) & B(to))) continue;
    n++;
  }
  // Black pawn moves (pins are impossible: the queen pins along lines; check them by the check test after the move)
  for (U64 t = p.c.bp; t; t &= t - 1) {
    int fr = __builtin_ctzll(t), to = fr - 8;
    auto ok = [&](int dest, bool cap) {
      U64 bp2 = (p.c.bp & ~B(fr)) | (RA(dest) == 0 ? 0 : B(dest));
      U64 wp2 = p.c.wp & ~(cap ? B(dest) : 0);
      int q2 = (cap && dest == qs) ? -1 : qs;
      U64 o2 = wp2 | bp2 | B(p.wk) | (q2 >= 0 ? B(q2) : 0) | B(p.bk);
      bool c = (q2 >= 0 && (queenAtt(q2, o2) & B(p.bk))) || (wpatt(wp2) & B(p.bk));
      return !c;
    };
    U64 occ2 = p.c.wp | p.c.bp | B(p.wk) | B(p.bk) | B(qs);
    if (to >= 0 && !(occ2 & B(to)) && ok(to, false)) n++;
    for (int df = -1; df <= 1; df += 2) { if (FI(fr) + df < 0 || FI(fr) + df > 7 || to < 0) continue; int c = to + df;
      if (((p.c.wp | B(qs)) & B(c)) && ok(c, true)) n++; }
  }
  return n;
}
static const int SQ_b6 = 41, SQ_b7 = 49, SQ_b8 = 57, SQ_a7 = 48, SQ_c7 = 50, SQ_a6 = 40, SQ_c5 = 34, SQ_e5 = 36, SQ_d6 = 43;
static bool sa_move(const Pos &p, int n, string &want) {
  int wk = p.wk;
  if (n == 1) { want = "Ke5"; return true; }
  if (n == 2) { want = "Kd6"; return true; }
  if (n == 3) { want = "Kc7"; return true; }
  if ((p.c.bp & B(SQ_b7)) && (wk == SQ_c7 || wk == SQ_b8)) {
    if (p.bk == SQ_a6) { want = wk == SQ_c7 ? "Kb8" : "Kc7"; return true; }
    want = "Kxb7"; return true;
  }
  if (wk == SQ_b7) { want = kdist(p.bk, SQ_c7) == 1 ? "Ka7" : "Kc7"; return true; }
  if (p.c.wp & B(SQ_b7)) { want = "b7-b8="; return true; }
  if ((p.c.wp & B(SQ_b6)) && !(p.c.bp & B(SQ_b7)) && (wk == SQ_a7 || wk == SQ_c7)) { want = "b6-b7"; return true; }
  return false;
}
static void sa_dfs(const Pos &p, int n, int bturns, bool tookb7, SAStats &st, int bound, int layer, string line) {
  // White to move, White's move number n
  string want;
  if (!sa_move(p, n, want)) { st.fails++; if (st.failMsg.size() < 20) st.failMsg.push_back("no rule: " + tofen(p) + " | " + line); return; }
  vector<Succ> mv; gen(p, mv);
  const Succ *m = nullptr;
  for (auto &x : mv) if (x.name == want) m = &x;
  if (!m) { st.fails++; if (st.failMsg.size() < 20) st.failMsg.push_back("illegal " + want + ": " + tofen(p) + " | " + line); return; }
  line += " " + to_string(n) + "." + want;
  if (want == "Kxb7") { int r = RA(p.bk) + 1; if (r > 5) { st.rankAtKxb7++; if (st.failMsg.size() < 20) st.failMsg.push_back("rank>5 at Kxb7: " + line); } }
  if (m->promo) {
    st.leaves++; st.promoAt[n]++; st.maxn = max<long>(st.maxn, n);
    if (n > bound) { st.fails++; if (st.failMsg.size() < 20) st.failMsg.push_back("late promotion: " + line); }
    if (layer == 0) {
      Pos q = m->p;  // Black to move; queen on b8
      bool capt = kdist(q.bk, SQ_b8) == 1 && kdist(q.wk, SQ_b8) > 1;
      if (capt) st.qcapt++;
      bool chk; int nm = chessBlackMoves(q, SQ_b8, chk);
      if (nm == 0 && !chk) st.chessStale++;
      int pr = 0; for (U64 t = q.c.bp; t; t &= t - 1) pr = RA(__builtin_ctzll(t)) + 1;
      st.pawnRankAtPromo[pr]++;
      if (pr != 0 && pr < 4) st.pawnRankBad++;
      string f = tofen(q); // put the queen in
      // rebuild with Q on b8
      string g; int col = 0; size_t i = 0;
      (void)col; (void)i;
      // simple: rank 8 string
      Pos tmp = q; string fen = tofen(tmp);
      size_t sl = fen.find('/');
      string r8;
      { int e = 0; for (int f8 = 0; f8 < 8; f8++) { int s = f8 + 56; char ch = 0;
          if (s == SQ_b8) ch = 'Q'; else if (s == q.wk) ch = 'K'; else if (s == q.bk) ch = 'k';
          if (!ch) { e++; continue; } if (e) { r8 += char('0' + e); e = 0; } r8 += ch; } if (e) r8 += char('0' + e); }
      st.leavesChess.insert(r8 + fen.substr(sl));
    }
    return;
  }
  Pos q = m->p;  // Black to move
  int bt = bturns + 1;
  if (!tookb7 && RA(q.bk) >= 6) { st.rank7before++; }
  vector<Succ> bm; gen(q, bm);
  if (bm.empty()) { st.blackStalemate++; if (layer == 0 || !incheck(q, 1)) { if (layer == 0) { st.fails++; if (st.failMsg.size() < 20) st.failMsg.push_back("Black stalemated in P: " + line); } } return; }
  // Lemma A2: a king move to the rank below (on rank 1: along it)
  bool a2 = false;
  for (auto &x : bm) if (!x.pass && x.name[0] == 'K') { int to = x.p.bk; if ((RA(q.bk) > 0 && RA(to) == RA(q.bk) - 1) || (RA(q.bk) == 0 && RA(to) == 0)) a2 = true; }
  if (!a2) { st.a2fail++; if (st.failMsg.size() < 20) st.failMsg.push_back("A2 fails: " + tofen(q) + " | " + line); }
  bool b7taken = tookb7 || want == "Kxb7";
  for (auto &x : bm) {
    if (x.promo) { st.fails++; if (st.failMsg.size() < 20) st.failMsg.push_back("Black promotes: " + line + " " + x.name); continue; }
    if (x.name == "Kxc5" && bt < 3) st.earlyC5++;
    sa_dfs(x.p, n + 1, bt, b7taken, st, bound, layer, line + " " + x.name);
  }
}
static void run_sa(const vector<string> &fens, int tok, int bound, int layer) {
  SAStats st;
  for (auto &f : fens) { Pos p = fromfen(f); p.tok = tok; sa_dfs(p, 1, 0, false, st, bound, layer, f + ":"); }
  printf("S_A %s token=%d bound=%d: starts %zu, plays %ld, failures %ld, latest promotion at White move %ld\n",
         layer == 0 ? "P" : "sum", tok, bound, fens.size(), st.leaves, st.fails, st.maxn);
  for (auto &kv : st.promoAt) printf("   promotion at move %d: %ld plays\n", kv.first, kv.second);
  printf("   Black stalemated (no board move) %ld; A2 failures %ld; Kxc5 before B3 %ld; Black king on rank 7/8 before Kxb7 %ld; rank>5 at Kxb7 %ld\n",
         st.blackStalemate, st.a2fail, st.earlyC5, st.rank7before, st.rankAtKxb7);
  if (layer == 0) {
    printf("   after b8=Q: queen capturable %ld, chess stalemate %ld, Black pawn rank<4 %ld; distinct leaf positions %zu\n", st.qcapt, st.chessStale, st.pawnRankBad, st.leavesChess.size());
    for (auto &kv : st.pawnRankAtPromo) printf("   Black c-pawn on rank %d at promotion: %ld plays\n", kv.first, kv.second);
  }
  for (auto &s : st.failMsg) printf("   FAIL %s\n", s.c_str());
  if (layer == 0 && getenv("LEAVES")) { FILE *o = fopen(getenv("LEAVES"), "w"); for (auto &s : st.leavesChess) fprintf(o, "%s b - - 0 1\n", s.c_str()); fclose(o); }
}

static const char *ROOTS[2] ={"8/1p6/1Pp5/2P5/1k1K4/8/2P5/8", "8/1p6/1Pp5/1kP5/3K4/8/2P5/8"};

int main(int argc, char **argv) {
  for (int s = 0; s < 64; s++) { KATT[s] = 0; for (int d = 0; d < 64; d++) if (d != s && kdist(s, d) == 1) KATT[s] |= B(d); }
  // closure from the root material (both roots have the same pawns)
  Pos r0 = fromfen(string(ROOTS[0]) + " w");
  closure(r0.c);
  fprintf(stderr, "cfgs %zu\n", cfgs.size());
  string cmd = argc > 1 ? argv[1] : "query";
  int layers = (cmd == "query" || cmd == "lemmaB" || cmd == "group" || cmd == "dump") ? 3 : 3;
  for (int L = 0; L < layers; L++) solveall(L);
  fprintf(stderr, "solved\n");
  if (cmd == "query") {  // lines: FEN-with-side [tok]  -> values in P, S0, S1 and every move
    char line[512];
    while (fgets(line, sizeof line, stdin)) {
      string s(line); while (!s.empty() && (s.back() == '\n' || s.back() == '\r')) s.pop_back();
      if (s.empty() || s[0] == '#') continue;
      Pos p = fromfen(s);
      if (!valid(p)) { printf("%s INVALID\n", s.c_str()); continue; }
      Pos p1 = p; p1.tok = 1;
      printf("%s  P=%s S0=%s S1=%s\n", s.c_str(), wval(p, 0).c_str(), wval(p, 1).c_str(), wval(p1, 2).c_str());
      vector<Succ> mv; gen(p, mv);
      for (auto &m : mv) {
        if (m.promo) { printf("   %-10s promotes\n", m.name.c_str()); continue; }
        Pos q1 = m.p; q1.tok = 1;
        printf("   %-10s -> %s  P=%s S0=%s S1(after, Black token)=%s\n", m.name.c_str(), tofen(m.p).c_str(), wval(m.p, 0).c_str(), wval(m.p, 1).c_str(), wval(q1, 2).c_str());
      }
    }
  }
  if (cmd == "lemmaB") {  // all 162 positions
    const char *gs[3] = {"c2", "c3", "c4"};
    int cnt = 0, nw = 0;
    for (int g = 0; g < 3; g++) for (int wk = 0; wk < 64; wk++) {
      Pos p{}; p.c.wp = B(sqp(gs[g])); p.c.bp = B(sqp("b7")) | B(sqp("c6")); p.c.ep = -1; p.bk = sqp("b6"); p.wk = wk; p.stm = 0; p.tok = 0;
      if (!valid(p)) continue;
      cnt++;
      string v = wval(p, 0);
      if (v[0] == 'L') nw++;
      printf("lemmaB %s K%s %s  P=%s S0=%s\n", gs[g], sqn(wk).c_str(), tofen(p).c_str(), v.c_str(), wval(p, 1).c_str());
    }
    printf("lemmaB total %d, Black wins in P %d\n", cnt, nw);
  }
  if (cmd == "strat") {
    vector<string> A = {
      "8/1p6/1Pp5/2P5/3K4/k7/2P5/8 w", "8/1p6/1Pp5/2P5/k2K4/8/2P5/8 w", "8/1p6/1Pp5/k1P5/3K4/8/2P5/8 w", "8/1p6/kPp5/2P5/3K4/8/2P5/8 w",
      "8/1p6/1Pp5/2P5/2PK4/k7/8/8 w", "8/1p6/1Pp5/2P5/k1PK4/8/8/8 w", "8/1p6/1Pp5/k1P5/2PK4/8/8/8 w", "8/1p6/1Pp5/2P5/2PK4/1k6/8/8 w",
      "8/1p6/1Pp5/2P5/k2K4/2P5/8/8 w", "8/1p6/1Pp5/k1P5/3K4/2P5/8/8 w", "8/1p6/kPp5/2P5/3K4/2P5/8/8 w"};
    vector<string> X(A.begin(), A.begin() + 4);
    run_sa(A, 0, 8, 0);       // P alone, 11 starts, by move 8
    run_sa(X, 1, 9, 2);       // beside -1 (sum rule, Black token), the four boards x_m, by move 9
    run_sa(A, 1, 9, 2);       // beside -1, all 11 starts (more than claimed)
    run_sa(X, 1, 8, 2);       // is the bound 9 needed?
  }
  if (cmd == "needed") {  // Lemma C reduction: White king move at R1,R2,Q1,Q2; ...Kxc5; any White move; ...Kxb6
    const char *F4[4] = {"8/1p6/1Pp5/2P5/1k1K4/8/2P5/8 w", "8/1p6/1Pp5/1kP5/3K4/8/2P5/8 w", "8/1p6/1Pp5/2P5/1kPK4/8/8/8 w", "8/1p6/1Pp5/1kP5/3K4/2P5/8/8 w"};
    const char *NM[4] = {"R1", "R2", "Q1", "Q2"};
    set<string> need; map<string, string> from;
    vector<Succ> a, b, c, d;
    for (int k = 0; k < 4; k++) {
      Pos p = fromfen(F4[k]); gen(p, a);
      for (auto &m1 : a) {
        if (m1.name[0] != 'K') continue;
        gen(m1.p, b); const Succ *kx = nullptr; for (auto &x : b) if (x.name == "Kxc5") kx = &x;
        if (!kx) { printf("%s %s: Kxc5 ILLEGAL\n", NM[k], m1.name.c_str()); continue; }
        gen(kx->p, c);
        printf("%s %s Kxc5: value P=%s; White replies %zu\n", NM[k], m1.name.c_str(), wval(kx->p, 0).c_str(), c.size());
        for (auto &m2 : c) {
          if (m2.promo) { printf("   promotion?!\n"); continue; }
          gen(m2.p, d); const Succ *kb = nullptr; for (auto &x : d) if (x.name == "Kxb6") kb = &x;
          if (!kb) { printf("   after %s: Kxb6 ILLEGAL (%s)\n", m2.name.c_str(), tofen(m2.p).c_str()); continue; }
          string f = tofen(kb->p); need.insert(f); from[f] += string(" ") + NM[k] + ":" + m1.name + "/" + m2.name;
        }
      }
    }
    int bw = 0;
    for (auto &f : need) { Pos p = fromfen(f); string v = wval(p, 0); if (v[0] == 'L') bw++; printf("need %s P=%s via%s\n", f.c_str(), v.c_str(), from[f].c_str()); }
    printf("needed Lemma B positions: %zu, Black wins: %d\n", need.size(), bw);
  }
  return 0;
}
