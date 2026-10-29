// ownref.cpp (K28) = K27 referee's ownchess.cpp plus the option REFINE (argv[4] = 1): capture refinement of a capped promotion,
//   see FINDINGS.md.  With REFINE = 0 it is ownchess.cpp unchanged.
// ownchess.cpp -- referee's own chess solver, flat 7x6 (or WxH) board, kings + pawns + at most ONE officer (cap 1).
// Written from SPEC.md only; shares no code with kpsolve.c, ref3, pm.py, own.cpp.
// Method: layers = (white pawn set, black pawn set, officer type/colour or none). Pawn moves, captures and promotions
// leave the layer, officer captures leave it too. Inside a layer only king/officer non-capturing moves happen; they are
// solved by counting retrograde analysis. Child layers are solved first (recursion, memoised).
// Cap 1 (SPEC.md): a promotion is *capped* iff the position after it would hold more than 1 officer.
// Bound A: a capped promotion is an immediate White win; bound B: an immediate Black win.
// Usage: ownchess W H BOUND(0=A,1=B)  < positions   -> "<pos> | X" with X in W/D/L from White's point of view, for that bound.
// No en passant: aborts if a pawn ever stands on its second rank (a double step would then be possible).
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <cctype>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>
using std::string; using std::vector;
typedef unsigned long long u64;
static int W = 7, H = 6, N = 42, BOUND = 0, REFINE = 0;
static inline int fl(int s) { return s % W; }
static inline int rk(int s) { return s / W; }
static inline bool kadj(int a, int b) { return a != b && abs(fl(a) - fl(b)) <= 1 && abs(rk(a) - rk(b)) <= 1; }
struct Pos {
  int wk, bk; u64 wp, bp; int ot, oc, os;  // officer type 0..3 = Q R B N (-1 none), colour, square
};
struct Key {
  u64 wp, bp; int ot, oc;
  bool operator<(const Key& o) const {
    if (wp != o.wp) return wp < o.wp; if (bp != o.bp) return bp < o.bp; if (ot != o.ot) return ot < o.ot; return oc < o.oc; }
};
static const int DF[8] = {1, -1, 0, 0, 1, 1, -1, -1}, DR[8] = {0, 0, 1, -1, 1, -1, 1, -1};
static const int KDF[8] = {1, 2, 2, 1, -1, -2, -2, -1}, KDR[8] = {2, 1, -1, -2, -2, -1, 1, 2};
// is square s attacked by colour c in position p? (king of c, pawns of c, officer of c if colour matches)
static bool attacked(const Pos& p, int s, int c) {
  int ck = c == 0 ? p.wk : p.bk;
  if (kadj(ck, s)) return true;
  u64 pp = c == 0 ? p.wp : p.bp;
  int f = fl(s), r = rk(s);
  int pr = c == 0 ? r - 1 : r + 1;
  if (pr >= 0 && pr < H) for (int d = -1; d <= 1; d += 2) { int pf = f + d; if (pf >= 0 && pf < W && (pp >> (pr * W + pf) & 1)) return true; }
  if (p.ot >= 0 && p.oc == c && p.os != s) {
    int o = p.os;
    if (p.ot == 3) {
      int of = fl(o), orr = rk(o);
      for (int i = 0; i < 8; i++) if (of + KDF[i] == f && orr + KDR[i] == r) return true;
    } else {
      u64 occ = p.wp | p.bp | (1ULL << p.wk) | (1ULL << p.bk);
      int lo = p.ot == 2 ? 4 : 0, hi = p.ot == 1 ? 4 : 8;  // dirs 0-3 orthogonal, 4-7 diagonal
      for (int i = lo; i < hi; i++) {
        int x = fl(o) + DF[i], y = rk(o) + DR[i];
        while (x >= 0 && x < W && y >= 0 && y < H) {
          int q = y * W + x;
          if (q == s) return true;
          if (occ >> q & 1) break;
          x += DF[i]; y += DR[i];
        }
      }
    }
  }
  return false;
}
struct Move { Pos to; int promo; bool capped; int rv = -1; };  // promo: 0 none, 1 promotion move; rv: refined value (see refineCapped)
static bool anySecond = false;
// ---- capture refinement.  A capped promotion by the colour whose bound is the generous one (White in A, Black in B) is resolved by the
// opponent's legal captures of the new piece: the promoter's true value is at most (for the promoter) its value after any such
// capture, so the best capture for the opponent gives a valid bound.  Returns the value for the OPPONENT (to move after the
// promotion): 1 win, 2 loss, 0 draw, or -1 if the opponent has no legal capture of the new piece.
struct Layer;
static int layerValue(const Pos& p, int stm);   // defined after the layer code
struct P2 { int wk, bk; u64 wp, bp; int no; int ot[2], oc[2], os[2]; };
static bool attacked2(const P2& p, int s, int c) {
  int ck = c == 0 ? p.wk : p.bk;
  if (kadj(ck, s)) return true;
  u64 pp = c == 0 ? p.wp : p.bp;
  int f = fl(s), r = rk(s), pr = c == 0 ? r - 1 : r + 1;
  if (pr >= 0 && pr < H) for (int d = -1; d <= 1; d += 2) { int pf = f + d; if (pf >= 0 && pf < W && (pp >> (pr * W + pf) & 1)) return true; }
  u64 occ = p.wp | p.bp | (1ULL << p.wk) | (1ULL << p.bk);
  for (int j = 0; j < p.no; j++) occ |= 1ULL << p.os[j];
  for (int j = 0; j < p.no; j++) {
    if (p.oc[j] != c || p.os[j] == s) continue;
    int o = p.os[j];
    if (p.ot[j] == 3) { for (int i = 0; i < 8; i++) if (fl(o) + KDF[i] == f && rk(o) + KDR[i] == r) return true; }
    else {
      int lo = p.ot[j] == 2 ? 4 : 0, hi = p.ot[j] == 1 ? 4 : 8;
      for (int i = lo; i < hi; i++) {
        int x = fl(o) + DF[i], y = rk(o) + DR[i];
        while (x >= 0 && x < W && y >= 0 && y < H) {
          int q = y * W + x;
          if (q == s) return true;
          if (occ >> q & 1) break;
          x += DF[i]; y += DR[i];
        }
      }
    }
  }
  return false;
}
// n: position after the promoting pawn left (and a captured piece, if any, was removed), possibly with one officer left (n.ot >= 0);
// the new piece (type ty, colour c) stands on t.
static int refineCapped(const Pos& n, int c, int ty, int t) {
  int o = 1 - c;
  P2 p; p.wk = n.wk; p.bk = n.bk; p.wp = n.wp; p.bp = n.bp; p.no = 0;
  if (n.ot >= 0) { p.ot[p.no] = n.ot; p.oc[p.no] = n.oc; p.os[p.no] = n.os; p.no++; }
  int newj = p.no; p.ot[p.no] = ty; p.oc[p.no] = c; p.os[p.no] = t; p.no++;
  int cnt = 0, loss = 0, draw = 0;
  auto finish = [&](P2 q) {   // q: position after the opponent's capture; check legality of the capturer's king, then look up
    int ok = o == 0 ? q.wk : q.bk;
    if (attacked2(q, ok, c)) return;
    Pos r; r.wk = q.wk; r.bk = q.bk; r.wp = q.wp; r.bp = q.bp; r.ot = -1; r.oc = 0; r.os = 0;
    if (q.no > 1) { fprintf(stderr, "internal error: refine with two officers left\n"); exit(1); }
    if (q.no == 1) { r.ot = q.ot[0]; r.oc = q.oc[0]; r.os = q.os[0]; }
    int v = layerValue(r, c);   // value for the promoter, to move
    cnt++;
    if (v == 2) loss = 1; else if (v == 0) draw = 1;
  };
  // capture by the opponent's king
  int ko = o == 0 ? p.wk : p.bk, kc = o == 0 ? p.bk : p.wk;
  if (kadj(ko, t) && !kadj(kc, t)) {
    P2 q = p; for (int j = newj; j + 1 < q.no; j++) { q.ot[j] = q.ot[j + 1]; q.oc[j] = q.oc[j + 1]; q.os[j] = q.os[j + 1]; } q.no--;
    if (o == 0) q.wk = t; else q.bk = t;
    finish(q);
  }
  // capture by the opponent's old officer (the new piece is the promoter's, so only an old officer of colour o can capture)
  if (n.ot >= 0 && n.oc == o) {
    int os = n.os; bool reach = false;
    u64 occ = p.wp | p.bp | (1ULL << p.wk) | (1ULL << p.bk) | (1ULL << os) | (1ULL << t);
    if (n.ot == 3) { for (int i = 0; i < 8; i++) if (fl(os) + KDF[i] == fl(t) && rk(os) + KDR[i] == rk(t)) reach = true; }
    else {
      int lo = n.ot == 2 ? 4 : 0, hi = n.ot == 1 ? 4 : 8;
      for (int i = lo; i < hi && !reach; i++) {
        int x = fl(os) + DF[i], y = rk(os) + DR[i];
        while (x >= 0 && x < W && y >= 0 && y < H) {
          int q = y * W + x;
          if (q == t) { reach = true; break; }
          if (occ >> q & 1) break;
          x += DF[i]; y += DR[i];
        }
      }
    }
    if (reach) {
      P2 q = p; q.no = 1; q.ot[0] = n.ot; q.oc[0] = n.oc; q.os[0] = t;   // the old officer now stands on t; the new piece is gone
      finish(q);
    }
  }
  // (an opponent pawn can never capture on the promotion square: it would have to stand beyond the last rank)
  if (!cnt) return -1;
  return loss ? 1 : draw ? 0 : 2;
}
// legal moves of colour c to move
static void gen(const Pos& p, int c, vector<Move>& out) {
  out.clear();
  u64 own = c == 0 ? p.wp : p.bp, opp = c == 0 ? p.bp : p.wp;
  int k = c == 0 ? p.wk : p.bk, ok = c == 0 ? p.bk : p.wk;
  bool ownOff = p.ot >= 0 && p.oc == c, oppOff = p.ot >= 0 && p.oc != c;
  u64 occ = p.wp | p.bp | (1ULL << p.wk) | (1ULL << p.bk) | (p.ot >= 0 ? 1ULL << p.os : 0);
  auto emit = [&](Pos n, int promo, bool capped) {
    if (attacked(n, c == 0 ? n.wk : n.bk, 1 - c)) return;
    out.push_back({n, promo, capped});
  };
  // king
  for (int i = 0; i < 8; i++) {
    int x = fl(k) + DF[i], y = rk(k) + DR[i];
    if (x < 0 || x >= W || y < 0 || y >= H) continue;
    int t = y * W + x;
    if ((own >> t & 1) || t == ok) continue;
    if (ownOff && p.os == t) continue;
    Pos n = p;
    if (opp >> t & 1) { if (c == 0) n.bp &= ~(1ULL << t); else n.wp &= ~(1ULL << t); }
    if (oppOff && p.os == t) { n.ot = -1; n.oc = 0; n.os = 0; }
    if (c == 0) n.wk = t; else n.bk = t;
    emit(n, 0, false);
  }
  // officer
  if (ownOff) {
    int o = p.os;
    auto tryto = [&](int t) -> bool {  // returns true if square t was empty (continue sliding)
      if (t == p.wk || t == p.bk) return false;
      if (own >> t & 1) return false;
      Pos n = p; n.os = t;
      bool cap = false;
      if (opp >> t & 1) { cap = true; if (c == 0) n.bp &= ~(1ULL << t); else n.wp &= ~(1ULL << t); }
      emit(n, 0, false);
      return !cap;
    };
    if (p.ot == 3) {
      for (int i = 0; i < 8; i++) { int x = fl(o) + KDF[i], y = rk(o) + KDR[i]; if (x >= 0 && x < W && y >= 0 && y < H) tryto(y * W + x); }
    } else {
      int lo = p.ot == 2 ? 4 : 0, hi = p.ot == 1 ? 4 : 8;
      for (int i = lo; i < hi; i++) {
        int x = fl(o) + DF[i], y = rk(o) + DR[i];
        while (x >= 0 && x < W && y >= 0 && y < H) { if (!tryto(y * W + x)) break; x += DF[i]; y += DR[i]; }
      }
    }
  }
  // pawns
  int dir = c == 0 ? 1 : -1, last = c == 0 ? H - 1 : 0, second = c == 0 ? 1 : H - 2;
  for (int s = 0; s < N; s++) {
    if (!(own >> s & 1)) continue;
    int f = fl(s), r = rk(s);
    if (r == second) anySecond = true;
    int r1 = r + dir;
    if (r1 < 0 || r1 >= H) continue;
    auto addpawn = [&](int t, bool cap) {
      Pos n = p;
      u64& pp = c == 0 ? n.wp : n.bp;
      u64& qq = c == 0 ? n.bp : n.wp;
      pp &= ~(1ULL << s);
      if (cap) {
        if (opp >> t & 1) qq &= ~(1ULL << t);
        else if (oppOff && p.os == t) { n.ot = -1; n.oc = 0; n.os = 0; }
      }
      if (r1 == last) {
        for (int ty = 0; ty < 4; ty++) {
          Pos m = n;
          bool capped = m.ot >= 0;  // an officer is still on the board after the capture => 2 officers => capped
          m.ot = ty; m.oc = c; m.os = t;
          if (capped) {
            // terminal value, but the move must still be legal (own king not attacked; promoted piece irrelevant to own king)
            // the new piece (never placed in Pos, which holds one officer) can interpose a check: model it as an own pawn blocker on t
            Pos chk = n; if (c == 0) chk.wp |= 1ULL << t; else chk.bp |= 1ULL << t;
            if (attacked(chk, c == 0 ? chk.wk : chk.bk, 1 - c)) continue;
            Move mv_{m, 1, true};
            if (REFINE && c == BOUND) mv_.rv = refineCapped(n, c, ty, t);
            out.push_back(mv_);
          } else emit(m, 1, false);
        }
      } else { if (c == 0) n.wp |= 1ULL << t; else n.bp |= 1ULL << t; emit(n, 0, false); }
    };
    int t = r1 * W + f;
    if (!(occ >> t & 1)) addpawn(t, false);
    for (int d = -1; d <= 1; d += 2) {
      int cf = f + d; if (cf < 0 || cf >= W) continue;
      int q = r1 * W + cf;
      if ((opp >> q & 1) || (oppOff && p.os == q)) addpawn(q, true);
    }
  }
}
// ---- layers
struct Layer { vector<uint8_t> v; };
static std::map<Key, Layer*> memo;
static long long nstates = 0; static long nlayers = 0;
static inline size_t sidx(const Pos& p, int stm) {
  size_t base = (size_t)p.wk * N + p.bk;
  if (p.ot >= 0) base = base * N + p.os;
  return base * 2 + stm;
}
static Key keyOf(const Pos& p) { return Key{p.wp, p.bp, p.ot, p.ot >= 0 ? p.oc : 0}; }
static Layer* solve(const Key& key);
static Layer* getLayer(const Key& k) { auto it = memo.find(k); if (it != memo.end()) return it->second; return solve(k); }
static int layerValue(const Pos& p, int stm) {
  Layer* L = getLayer(keyOf(p));
  uint8_t v = L->v[sidx(p, stm)];
  if (v == 3) { fprintf(stderr, "internal error: illegal capture position\n"); exit(1); }
  return v;
}
// value 0 draw(unresolved), 1 mover wins, 2 mover loses, 3 illegal
static Layer* solve(const Key& key) {
  Layer* L = new Layer();
  bool hasO = key.ot >= 0;
  size_t total = (size_t)N * N * (hasO ? N : 1) * 2;
  L->v.assign(total, 3);
  memo[key] = L;  // safe: child layers never reference this layer (DAG), except in-layer handled locally
  nlayers++;
  // enumerate legal states
  vector<Pos> sts; vector<int> stm_; vector<uint32_t> ids;
  u64 pawns = key.wp | key.bp;
  for (int wk = 0; wk < N; wk++) {
    if (pawns >> wk & 1) continue;
    for (int bk = 0; bk < N; bk++) {
      if (bk == wk || (pawns >> bk & 1) || kadj(wk, bk)) continue;
      for (int os = 0; os < (hasO ? N : 1); os++) {
        if (hasO && (os == wk || os == bk || (pawns >> os & 1))) continue;
        Pos p{wk, bk, key.wp, key.bp, hasO ? key.ot : -1, hasO ? key.oc : 0, hasO ? os : 0};
        for (int stm = 0; stm < 2; stm++) {
          // side not to move must not be in check
          int other = 1 - stm;
          int ok = other == 0 ? wk : bk;
          if (attacked(p, ok, stm)) continue;
          L->v[sidx(p, stm)] = 0;
          sts.push_back(p); stm_.push_back(stm); ids.push_back((uint32_t)sidx(p, stm));
        }
      }
    }
  }
  size_t ns = sts.size();
  nstates += ns;
  // per state: classify moves
  vector<uint32_t> cnt(ns, 0);
  vector<uint32_t> eoff(ns + 1, 0);
  vector<uint32_t> edges;  // in-layer child state ids (index into L->v), flat
  vector<uint8_t> done(ns, 0);
  // map idx -> position in sts
  std::vector<uint32_t> pos_of(total, 0xffffffffu);
  for (size_t i = 0; i < ns; i++) pos_of[ids[i]] = (uint32_t)i;
  vector<Move> mv;
  vector<uint8_t> init(ns, 0);  // 0 undecided, 1 win, 2 loss
  for (size_t i = 0; i < ns; i++) {
    const Pos& p = sts[i]; int c = stm_[i];
    gen(p, c, mv);
    eoff[i] = edges.size();
    if (mv.empty()) {
      bool chk = attacked(p, c == 0 ? p.wk : p.bk, 1 - c);
      init[i] = chk ? 2 : 0; if (!chk) done[i] = 1;  // stalemate = draw (decided)
      cnt[i] = 0;
      continue;
    }
    uint32_t pending = 0; bool win = false;
    for (auto& m : mv) {
      int cv;  // child value from the child mover's (opponent's) view: 1 opp wins, 2 opp loses, 0 draw ; -1 in-layer
      if (m.capped) {
        bool whiteWins = BOUND == 0;
        bool moverWins = (c == 0) == whiteWins;
        cv = moverWins ? 2 : 1;
        if (m.rv >= 0) cv = m.rv;   // refined (REFINE): value for the opponent after his best capture of the new piece
      } else {
        Key ck = keyOf(m.to);
        if (!(ck.wp == key.wp && ck.bp == key.bp && ck.ot == key.ot && ck.oc == key.oc && m.promo == 0)) {
          Layer* cl = getLayer(ck);
          uint8_t v = cl->v[sidx(m.to, 1 - c)];
          if (v == 3) { fprintf(stderr, "internal error: illegal child\n"); exit(1); }
          cv = v == 1 ? 1 : v == 2 ? 2 : 0;
        } else {
          cv = -1;
          edges.push_back((uint32_t)sidx(m.to, 1 - c));
          pending++;
          continue;
        }
      }
      if (cv == 2) win = true;
      else if (cv == 0) pending++;  // draw child: never makes the mover lose
      // cv==1: child is a win for opponent: contributes nothing to pending
    }
    cnt[i] = pending;
    if (win) init[i] = 1;
    else if (pending == 0) init[i] = 2;
    // note: draw-valued out-of-layer children counted in pending but never decremented => state can't be a loss
  }
  eoff[ns] = edges.size();
  // reverse edges (CSR)
  vector<uint32_t> rcount(ns + 1, 0);
  for (size_t i = 0; i < ns; i++) for (uint32_t e = eoff[i]; e < eoff[i + 1]; e++) { uint32_t t = pos_of[edges[e]]; rcount[t + 1]++; }
  for (size_t i = 0; i < ns; i++) rcount[i + 1] += rcount[i];
  vector<uint32_t> rev(edges.size()), fillp(rcount.begin(), rcount.end() - 1);
  for (size_t i = 0; i < ns; i++) for (uint32_t e = eoff[i]; e < eoff[i + 1]; e++) { uint32_t t = pos_of[edges[e]]; rev[fillp[t]++] = (uint32_t)i; }
  // retrograde
  vector<uint32_t> q;
  vector<uint8_t> val(ns, 0);
  for (size_t i = 0; i < ns; i++) if (init[i]) { val[i] = init[i]; q.push_back((uint32_t)i); }
  for (size_t h = 0; h < q.size(); h++) {
    uint32_t t = q[h];
    for (uint32_t e = rcount[t]; e < rcount[t + 1]; e++) {
      uint32_t s = rev[e];
      if (val[s]) continue;
      if (val[t] == 2) { val[s] = 1; q.push_back(s); }
      else if (val[t] == 1) { if (--cnt[s] == 0) { val[s] = 2; q.push_back(s); } }
    }
  }
  for (size_t i = 0; i < ns; i++) L->v[ids[i]] = val[i];
  return L;
}
static bool parsepos(const string& line, Pos& p, int& stm) {
  std::istringstream is(line); vector<string> t; string x; while (is >> x) t.push_back(x);
  if (t.size() < 3) return false;
  p.wk = p.bk = -1; p.wp = p.bp = 0; p.ot = -1; p.oc = 0; p.os = 0;
  for (size_t i = 0; i + 2 < t.size(); i++) {
    char c = t[i][0]; int s = (t[i][2] - '1') * W + (t[i][1] - 'a');
    if (c == 'K') p.wk = s; else if (c == 'k') p.bk = s; else if (c == 'P') p.wp |= 1ULL << s; else if (c == 'p') p.bp |= 1ULL << s;
    else { const char* ty = "QRBN"; const char* tl = strchr(ty, toupper(c)); if (!tl) return false; p.ot = tl - ty; p.oc = isupper(c) ? 0 : 1; p.os = s; }
  }
  stm = t[t.size() - 2] == "b";
  return true;
}
int main(int argc, char** argv) {
  W = atoi(argv[1]); H = atoi(argv[2]); N = W * H; BOUND = atoi(argv[3]); if (argc > 4) REFINE = atoi(argv[4]);
  string line;
  while (std::getline(std::cin, line)) {
    if (line.empty() || line[0] == '#') continue;
    Pos p; int stm;
    if (!parsepos(line, p, stm)) { puts("bad"); continue; }
    Layer* L = getLayer(keyOf(p));
    uint8_t v = L->v[sidx(p, stm)];
    char r;
    if (v == 3) r = 'X'; else if (v == 0) r = 'D'; else r = ((v == 1) == (stm == 0)) ? 'W' : 'L';
    printf("%s | %c\n", line.c_str(), r);
    fflush(stdout);
  }
  fprintf(stderr, "[ownchess bound %c: layers %ld, states %lld, second-rank pawn seen: %d]\n", BOUND ? 'B' : 'A', nlayers, nstates, (int)anySecond);
  return 0;
}
