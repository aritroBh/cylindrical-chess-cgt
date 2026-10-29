// own39.cpp (K39) = K28's ownref.cpp (the K27 referee's ownchess.cpp plus the capture refinement), extended by K39 with
//   * the cylinder (option CYL: files wrap for kings, knights, sliders and pawn captures; a ray stops at its own square;
//     the two rank rays that meet the same square give one move),
//   * the double step and en passant (an e.p. right is recorded only when an enemy pawn attacks the skipped square,
//     as kpsolve does; values do not depend on that choice),
//   * a move list per input position (MOVES = 1).
// It still shares no code with kpsolve.c (written from SPEC.md; kpsolve was read only for the output format of --moves).
// Model: chess, kings + pawns + at most ONE officer (cap 1). A promotion is *capped* iff the position after it would hold
// more than 1 officer. Bound A: a capped promotion is an immediate White win; bound B: an immediate Black win.
// REFINE = 1: a capped promotion by the side the bound favours (White in A, Black in B) is scored as the value after the
// opponent's best legal capture of the new piece (no capture: the capped terminal stands). Sound for that side only.
// Usage: own39 W H CYL BOUND(0=A,1=B) REFINE MOVES < positions
//   -> "<pos> | X" (X in W/D/L/X, White's view, for that bound) [" | mv:v mv:v ..."]
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
static int W = 7, H = 6, N = 42, CYL = 0, BOUND = 0, REFINE = 0, MOVES = 0;
static inline int fl(int s) { return s % W; }
static inline int rk(int s) { return s / W; }
// square at file x, rank y, or -1 when off the board (files wrap on the cylinder)
static inline int sqat(int x, int y) {
  if (y < 0 || y >= H) return -1;
  if (CYL) x = ((x % W) + W) % W; else if (x < 0 || x >= W) return -1;
  return y * W + x;
}
static inline bool kadj(int a, int b) {
  if (a == b) return false;
  int df = abs(fl(a) - fl(b)); if (CYL && W - df < df) df = W - df;
  return df <= 1 && abs(rk(a) - rk(b)) <= 1;
}
struct Pos {
  int wk, bk; u64 wp, bp; int ot, oc, os; int ep;  // officer type 0..3 = Q R B N (-1 none), colour, square; e.p. target or -1
};
struct Key {
  u64 wp, bp; int ot, oc, ep;
  bool operator<(const Key& o) const {
    if (wp != o.wp) return wp < o.wp; if (bp != o.bp) return bp < o.bp; if (ot != o.ot) return ot < o.ot;
    if (oc != o.oc) return oc < o.oc; return ep < o.ep; }
  bool operator==(const Key& o) const { return wp == o.wp && bp == o.bp && ot == o.ot && oc == o.oc && ep == o.ep; }
};
static const int DF[8] = {1, -1, 0, 0, 1, 1, -1, -1}, DR[8] = {0, 0, 1, -1, 1, -1, 1, -1};
static const int KDF[8] = {1, 2, 2, 1, -1, -2, -2, -1}, KDR[8] = {2, 1, -1, -2, -2, -1, 1, 2};
// does an officer of type ty on o attack (reach) square s, with occupancy occ (o itself need not be in occ)?
static bool offReach(int ty, int o, int s, u64 occ) {
  if (ty == 3) { for (int i = 0; i < 8; i++) if (sqat(fl(o) + KDF[i], rk(o) + KDR[i]) == s) return true; return false; }
  int lo = ty == 2 ? 4 : 0, hi = ty == 1 ? 4 : 8;  // dirs 0-3 orthogonal, 4-7 diagonal
  for (int i = lo; i < hi; i++) {
    int x = fl(o), y = rk(o);
    for (;;) {
      x += DF[i]; y += DR[i];
      int q = sqat(x, y);
      if (q < 0 || q == o) break;
      if (q == s) return true;
      if (occ >> q & 1) break;
    }
  }
  return false;
}
// is a pawn of colour c attacking s (pawn set pp)?
static bool pawnAtt(u64 pp, int s, int c) {
  int pr = c == 0 ? rk(s) - 1 : rk(s) + 1;
  for (int d = -1; d <= 1; d += 2) { int q = sqat(fl(s) + d, pr); if (q >= 0 && (pp >> q & 1)) return true; }
  return false;
}
// is square s attacked by colour c in position p?
static bool attacked(const Pos& p, int s, int c) {
  int ck = c == 0 ? p.wk : p.bk;
  if (kadj(ck, s)) return true;
  if (pawnAtt(c == 0 ? p.wp : p.bp, s, c)) return true;
  if (p.ot >= 0 && p.oc == c && p.os != s) {
    u64 occ = p.wp | p.bp | (1ULL << p.wk) | (1ULL << p.bk);
    if (offReach(p.ot, p.os, s, occ)) return true;
  }
  return false;
}
struct Move { Pos to; int promo; bool capped; int rv = -1; int pc, from, dest, pty; };  // pc: piece letter; pty promo type or -1
// ---- capture refinement (see the header). Returns the value for the OPPONENT (to move after the promotion):
// 1 win, 2 loss, 0 draw, or -1 if the opponent has no legal capture of the new piece.
static int layerValue(const Pos& p, int stm);
struct P2 { int wk, bk; u64 wp, bp; int no; int ot[2], oc[2], os[2]; };
static bool attacked2(const P2& p, int s, int c) {
  int ck = c == 0 ? p.wk : p.bk;
  if (kadj(ck, s)) return true;
  if (pawnAtt(c == 0 ? p.wp : p.bp, s, c)) return true;
  u64 occ = p.wp | p.bp | (1ULL << p.wk) | (1ULL << p.bk);
  for (int j = 0; j < p.no; j++) occ |= 1ULL << p.os[j];
  for (int j = 0; j < p.no; j++) {
    if (p.oc[j] != c || p.os[j] == s) continue;
    if (offReach(p.ot[j], p.os[j], s, occ)) return true;
  }
  return false;
}
// n: position after the promoting pawn left (a captured piece removed), possibly with one officer left (n.ot >= 0);
// the new piece (type ty, colour c) stands on t.
static int refineCapped(const Pos& n, int c, int ty, int t) {
  int o = 1 - c;
  P2 p; p.wk = n.wk; p.bk = n.bk; p.wp = n.wp; p.bp = n.bp; p.no = 0;
  if (n.ot >= 0) { p.ot[p.no] = n.ot; p.oc[p.no] = n.oc; p.os[p.no] = n.os; p.no++; }
  int newj = p.no; p.ot[p.no] = ty; p.oc[p.no] = c; p.os[p.no] = t; p.no++;
  int cnt = 0, loss = 0, draw = 0;
  auto finish = [&](P2 q) {
    int ok = o == 0 ? q.wk : q.bk;
    if (attacked2(q, ok, c)) return;
    Pos r; r.wk = q.wk; r.bk = q.bk; r.wp = q.wp; r.bp = q.bp; r.ot = -1; r.oc = 0; r.os = 0; r.ep = -1;
    if (q.no > 1) { fprintf(stderr, "internal error: refine with two officers left\n"); exit(1); }
    if (q.no == 1) { r.ot = q.ot[0]; r.oc = q.oc[0]; r.os = q.os[0]; }
    int v = layerValue(r, c);   // value for the promoter, to move
    cnt++;
    if (v == 2) loss = 1; else if (v == 0) draw = 1;
  };
  int ko = o == 0 ? p.wk : p.bk, kc = o == 0 ? p.bk : p.wk;
  if (kadj(ko, t) && !kadj(kc, t)) {
    P2 q = p; for (int j = newj; j + 1 < q.no; j++) { q.ot[j] = q.ot[j + 1]; q.oc[j] = q.oc[j + 1]; q.os[j] = q.os[j + 1]; } q.no--;
    if (o == 0) q.wk = t; else q.bk = t;
    finish(q);
  }
  if (n.ot >= 0 && n.oc == o) {
    u64 occ = p.wp | p.bp | (1ULL << p.wk) | (1ULL << p.bk) | (1ULL << n.os) | (1ULL << t);
    if (offReach(n.ot, n.os, t, occ)) {
      P2 q = p; q.no = 1; q.ot[0] = n.ot; q.oc[0] = n.oc; q.os[0] = t;
      finish(q);
    }
  }
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
  auto emit = [&](Pos n, int promo, bool capped, int pc, int from, int dest, int pty) {
    n.ep = n.ep;  // set by the caller
    if (attacked(n, c == 0 ? n.wk : n.bk, 1 - c)) return;
    Move m; m.to = n; m.promo = promo; m.capped = capped; m.pc = pc; m.from = from; m.dest = dest; m.pty = pty;
    out.push_back(m);
  };
  // king
  u64 kseen = 0;
  for (int i = 0; i < 8; i++) {
    int t = sqat(fl(k) + DF[i], rk(k) + DR[i]);
    if (t < 0 || t == k || (kseen >> t & 1)) continue;
    kseen |= 1ULL << t;
    if ((own >> t & 1) || t == ok) continue;
    if (ownOff && p.os == t) continue;
    Pos n = p; n.ep = -1;
    if (opp >> t & 1) { if (c == 0) n.bp &= ~(1ULL << t); else n.wp &= ~(1ULL << t); }
    if (oppOff && p.os == t) { n.ot = -1; n.oc = 0; n.os = 0; }
    if (c == 0) n.wk = t; else n.bk = t;
    emit(n, 0, false, 'K', k, t, -1);
  }
  // officer: collect the destination set first (on the cylinder two rays can reach the same square)
  if (ownOff) {
    int o = p.os; u64 dest = 0;
    if (p.ot == 3) {
      for (int i = 0; i < 8; i++) { int t = sqat(fl(o) + KDF[i], rk(o) + KDR[i]); if (t >= 0 && t != o) dest |= 1ULL << t; }
    } else {
      int lo = p.ot == 2 ? 4 : 0, hi = p.ot == 1 ? 4 : 8;
      for (int i = lo; i < hi; i++) {
        int x = fl(o), y = rk(o);
        for (;;) {
          x += DF[i]; y += DR[i];
          int q = sqat(x, y);
          if (q < 0 || q == o) break;
          dest |= 1ULL << q;
          if (occ >> q & 1) break;
        }
      }
    }
    dest &= ~(own | (1ULL << p.wk) | (1ULL << p.bk));
    for (int t = 0; t < N; t++) {
      if (!(dest >> t & 1)) continue;
      Pos n = p; n.ep = -1; n.os = t;
      if (opp >> t & 1) { if (c == 0) n.bp &= ~(1ULL << t); else n.wp &= ~(1ULL << t); }
      emit(n, 0, false, "QRBN"[p.ot], o, t, -1);
    }
  }
  // pawns
  int dir = c == 0 ? 1 : -1, last = c == 0 ? H - 1 : 0, second = c == 0 ? 1 : H - 2;
  for (int s = 0; s < N; s++) {
    if (!(own >> s & 1)) continue;
    int f = fl(s), r = rk(s);
    int r1 = r + dir;
    if (r1 < 0 || r1 >= H) continue;
    // capsq: square of the captured piece (-1 none); epcap: the captured pawn stands on capsq, not on t
    auto addpawn = [&](int t, int capsq) {
      Pos n = p; n.ep = -1;
      u64& pp = c == 0 ? n.wp : n.bp;
      u64& qq = c == 0 ? n.bp : n.wp;
      pp &= ~(1ULL << s);
      if (capsq >= 0) {
        if (opp >> capsq & 1) qq &= ~(1ULL << capsq);
        else if (oppOff && p.os == capsq) { n.ot = -1; n.oc = 0; n.os = 0; }
      }
      if (r1 == last) {
        for (int ty = 0; ty < 4; ty++) {
          Pos m = n;
          bool capped = m.ot >= 0;  // an officer is still on the board => 2 officers => capped
          m.ot = ty; m.oc = c; m.os = t;
          if (capped) {
            // legality: the new piece can block a check on its square; model it as an own pawn there
            Pos chk = n; if (c == 0) chk.wp |= 1ULL << t; else chk.bp |= 1ULL << t;
            if (attacked(chk, c == 0 ? chk.wk : chk.bk, 1 - c)) continue;
            Move mv_; mv_.to = m; mv_.promo = 1; mv_.capped = true; mv_.pc = 'P'; mv_.from = s; mv_.dest = t; mv_.pty = ty;
            if (REFINE && c == BOUND) mv_.rv = refineCapped(n, c, ty, t);
            out.push_back(mv_);
          } else emit(m, 1, false, 'P', s, t, ty);
        }
      } else { if (c == 0) n.wp |= 1ULL << t; else n.bp |= 1ULL << t; emit(n, 0, false, 'P', s, t, -1); }
    };
    int t = sqat(f, r1);
    if (!(occ >> t & 1)) {
      addpawn(t, -1);
      if (r == second) {
        int t2 = sqat(f, r1 + dir);
        if (t2 >= 0 && rk(t2) != last && !(occ >> t2 & 1)) {
          Pos n = p; n.ep = -1;
          if (c == 0) n.wp = (n.wp & ~(1ULL << s)) | (1ULL << t2); else n.bp = (n.bp & ~(1ULL << s)) | (1ULL << t2);
          if (pawnAtt(opp, t, 1 - c)) n.ep = t;   // an enemy pawn attacks the skipped square
          emit(n, 0, false, 'P', s, t2, -1);
        }
      }
    }
    u64 cseen = 0;
    for (int d = -1; d <= 1; d += 2) {
      int q = sqat(f + d, r1);
      if (q < 0 || (cseen >> q & 1)) continue;
      cseen |= 1ULL << q;
      if ((opp >> q & 1) || (oppOff && p.os == q)) addpawn(q, q);
      else if (p.ep == q && !(occ >> q & 1)) {
        int vs = sqat(fl(q), r);  // the pawn that double-stepped stands beside s
        if (opp >> vs & 1) addpawn(q, vs);
      }
    }
  }
}
// ---- layers
// values packed 2 bits per state (K39: memory)
struct Layer {
  vector<uint8_t> v;
  inline uint8_t get(size_t i) const { return (v[i >> 2] >> ((i & 3) * 2)) & 3; }
  inline void set(size_t i, uint8_t x) { uint8_t& b = v[i >> 2]; int sh = (i & 3) * 2; b = (uint8_t)((b & ~(3 << sh)) | (x << sh)); }
};
static std::map<Key, Layer*> memo;
static long long nstates = 0; static long nlayers = 0;
static inline size_t sidx(const Pos& p, int stm) {
  size_t base = (size_t)p.wk * N + p.bk;
  if (p.ot >= 0) base = base * N + p.os;
  return base * 2 + stm;
}
static Key keyOf(const Pos& p) { return Key{p.wp, p.bp, p.ot, p.ot >= 0 ? p.oc : 0, p.ep}; }
static Layer* solve(const Key& key);
static Layer* getLayer(const Key& k) { auto it = memo.find(k); if (it != memo.end()) return it->second; return solve(k); }
static int layerValue(const Pos& p, int stm) {
  Layer* L = getLayer(keyOf(p));
  uint8_t v = L->get(sidx(p, stm));
  if (v == 3) { fprintf(stderr, "internal error: illegal lookup\n"); exit(1); }
  return v;
}
// value of a move for the opponent (to move after it): 1 opp wins, 2 opp loses, 0 draw; -1 = in-layer (not looked up)
static int moveValue(const Move& m, int c, const Key* self) {
  if (m.capped) {
    bool whiteWins = BOUND == 0;
    bool moverWins = (c == 0) == whiteWins;
    int cv = moverWins ? 2 : 1;
    if (m.rv >= 0) cv = m.rv;
    return cv;
  }
  Key ck = keyOf(m.to);
  if (self && ck == *self) return -1;
  Layer* cl = getLayer(ck);
  uint8_t v = cl->get(sidx(m.to, 1 - c));
  if (v == 3) { fprintf(stderr, "internal error: illegal child\n"); exit(1); }
  return v == 1 ? 1 : v == 2 ? 2 : 0;
}
// value 0 draw(unresolved), 1 mover wins, 2 mover loses, 3 illegal
static Layer* solve(const Key& key) {
  Layer* L = new Layer();
  bool hasO = key.ot >= 0;
  size_t total = (size_t)N * N * (hasO ? N : 1) * 2;
  L->v.assign((total + 3) / 4, 0xFF);
  memo[key] = L;  // child layers never reference this layer (DAG); in-layer moves are handled here
  nlayers++;
  // with an e.p. right only the capturing side is to move: the side whose pawns did not double-step
  int epStm = -1;
  if (key.ep >= 0) epStm = rk(key.ep) == 2 ? 1 : 0;
  vector<Pos> sts; vector<int> stm_; vector<uint32_t> ids;
  u64 pawns = key.wp | key.bp;
  for (int wk = 0; wk < N; wk++) {
    if (pawns >> wk & 1) continue;
    for (int bk = 0; bk < N; bk++) {
      if (bk == wk || (pawns >> bk & 1) || kadj(wk, bk)) continue;
      for (int os = 0; os < (hasO ? N : 1); os++) {
        if (hasO && (os == wk || os == bk || (pawns >> os & 1))) continue;
        Pos p{wk, bk, key.wp, key.bp, hasO ? key.ot : -1, hasO ? key.oc : 0, hasO ? os : 0, key.ep};
        for (int stm = 0; stm < 2; stm++) {
          if (epStm >= 0 && stm != epStm) continue;
          int other = 1 - stm;
          int okk = other == 0 ? wk : bk;
          if (attacked(p, okk, stm)) continue;
          L->set(sidx(p, stm), 0);
          sts.push_back(p); stm_.push_back(stm); ids.push_back((uint32_t)sidx(p, stm));
        }
      }
    }
  }
  size_t ns = sts.size();
  nstates += ns;
  vector<uint32_t> cnt(ns, 0), eoff(ns + 1, 0), edges;
  std::vector<uint32_t> pos_of(total, 0xffffffffu);
  for (size_t i = 0; i < ns; i++) pos_of[ids[i]] = (uint32_t)i;
  vector<Move> mv;
  vector<uint8_t> init(ns, 0);
  for (size_t i = 0; i < ns; i++) {
    const Pos& p = sts[i]; int c = stm_[i];
    gen(p, c, mv);
    eoff[i] = edges.size();
    if (mv.empty()) {
      bool chk = attacked(p, c == 0 ? p.wk : p.bk, 1 - c);
      init[i] = chk ? 2 : 0;  // stalemate = draw
      cnt[i] = 0;
      continue;
    }
    uint32_t pending = 0; bool win = false;
    for (auto& m : mv) {
      int cv = moveValue(m, c, &key);
      if (cv < 0) { edges.push_back((uint32_t)sidx(m.to, 1 - c)); pending++; continue; }
      if (cv == 2) win = true;
      else if (cv == 0) pending++;  // a drawn exit is never decremented: the state cannot be lost
    }
    cnt[i] = pending;
    if (win) init[i] = 1;
    else if (pending == 0) init[i] = 2;
  }
  eoff[ns] = edges.size();
  vector<uint32_t> rcount(ns + 1, 0);
  for (size_t i = 0; i < ns; i++) for (uint32_t e = eoff[i]; e < eoff[i + 1]; e++) { uint32_t t = pos_of[edges[e]]; rcount[t + 1]++; }
  for (size_t i = 0; i < ns; i++) rcount[i + 1] += rcount[i];
  vector<uint32_t> rev(edges.size()), fillp(rcount.begin(), rcount.end() - 1);
  for (size_t i = 0; i < ns; i++) for (uint32_t e = eoff[i]; e < eoff[i + 1]; e++) { uint32_t t = pos_of[edges[e]]; rev[fillp[t]++] = (uint32_t)i; }
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
  for (size_t i = 0; i < ns; i++) L->set(ids[i], val[i]);
  L->v.shrink_to_fit();
  return L;
}
static int sqparse(const string& t, size_t off) {
  if (t.size() < off + 2) return -1;
  int f = t[off] - 'a', r = atoi(t.c_str() + off + 1) - 1;
  if (f < 0 || f >= W || r < 0 || r >= H) return -1;
  return r * W + f;
}
static bool parsepos(const string& line, Pos& p, int& stm) {
  std::istringstream is(line); vector<string> t; string x; while (is >> x) t.push_back(x);
  if (t.size() < 4) return false;
  p.wk = p.bk = -1; p.wp = p.bp = 0; p.ot = -1; p.oc = 0; p.os = 0; p.ep = -1;
  for (size_t i = 0; i + 2 < t.size(); i++) {
    char c = t[i][0]; int s = sqparse(t[i], 1); if (s < 0) return false;
    if (c == 'K') p.wk = s; else if (c == 'k') p.bk = s; else if (c == 'P') p.wp |= 1ULL << s; else if (c == 'p') p.bp |= 1ULL << s;
    else { const char* ty = "QRBN"; const char* tl = strchr(ty, toupper(c)); if (!tl) return false; p.ot = tl - ty; p.oc = isupper(c) ? 0 : 1; p.os = s; }
  }
  stm = t[t.size() - 2] == "b";
  if (t.back() != "-") {
    int e = sqparse(t.back(), 0); if (e < 0) return false;
    // keep the right only if a pawn of the side to move attacks the skipped square (canonical form, as kpsolve)
    if (pawnAtt(stm == 0 ? p.wp : p.bp, e, stm)) p.ep = e;
  }
  return true;
}
static string sqn(int s) { char b[8]; snprintf(b, sizeof b, "%c%d", 'a' + fl(s), rk(s) + 1); return b; }
int main(int argc, char** argv) {
  if (argc < 7) { fprintf(stderr, "usage: own39 W H CYL BOUND REFINE MOVES < positions\n"); return 2; }
  W = atoi(argv[1]); H = atoi(argv[2]); N = W * H; CYL = atoi(argv[3]); BOUND = atoi(argv[4]); REFINE = atoi(argv[5]); MOVES = atoi(argv[6]);
  if (N > 64 || H < 5) { fprintf(stderr, "own39: need W*H <= 64 and H >= 5\n"); return 2; }
  string line;
  vector<Move> mv;
  while (std::getline(std::cin, line)) {
    if (line.empty() || line[0] == '#') { puts(line.c_str()); continue; }
    Pos p; int stm;
    if (!parsepos(line, p, stm)) { printf("%s | bad\n", line.c_str()); continue; }
    Layer* L = getLayer(keyOf(p));
    uint8_t v = L->get(sidx(p, stm));
    char r;
    if (v == 3) r = 'X'; else if (v == 0) r = 'D'; else r = ((v == 1) == (stm == 0)) ? 'W' : 'L';
    printf("%s | %c", line.c_str(), r);
    if (MOVES && v != 3) {
      gen(p, stm, mv);
      printf(" |");
      for (auto& m : mv) {
        int cv = moveValue(m, stm, nullptr);  // for the opponent
        char c = cv == 0 ? 'D' : ((cv == 1) == (stm == 1)) ? 'W' : 'L';
        printf(" %c%s%s", m.pc, sqn(m.from).c_str(), sqn(m.dest).c_str());
        if (m.pty >= 0) printf("=%c", "QRBN"[m.pty]);
        printf(":%c", c);
      }
    }
    printf("\n");
    fflush(stdout);
  }
  fprintf(stderr, "[own39 %s %dx%d bound %c refine %d: layers %ld, states %lld]\n", CYL ? "cyl" : "flat", W, H, BOUND ? 'B' : 'A', REFINE, nlayers, nstates);
  return 0;
}
