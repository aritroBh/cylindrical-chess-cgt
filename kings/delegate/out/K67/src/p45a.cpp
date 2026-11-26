// K67 copy of K65's p45a.cpp: one change, a memory guard before the table is allocated (marked K67).
// plocal.cpp -- K43: exhaustive table of the promotion model P (real kings, first promotion wins, e.p. on,
// stalemate = draw, infinite play = draw) for every placement of both kings (anywhere on the board) and of up to
// NW white and NB black pawns on F consecutive files (ranks 2..H-1), and the exact over/under group tests of
// LOOPY Definition 4.8 on every placement.  Own move generator, written for K43 from SPEC.md and Definition 1.5.
//
// Method: a layer is a pawn configuration; pawn moves/captures leave the layer for a layer solved earlier
// (fewer pawns, or the same number and more advanced).  Inside a layer only the kings move; counting retrograde
// analysis.  Value codes (mover's view): 0 draw/unresolved, 1 win, 2 loss, 3 illegal.
//
// usage: plocal --kind cyl|flat --W 8 --H 6 --F 4 --off 0 --nw 3 --nb 3 [--kwin] [--mode under|over|both|dud|none]
//               [--dump N seed] [--print-q 30]
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <algorithm>
#include <string>
#include <ctime>
using namespace std;
typedef unsigned __int128 u64;   // K45: square masks are 128 bits so that boards of up to 72 squares fit
typedef uint32_t u32;
#define BIT(s) (((u64)1) << (s))
static inline int ctzM(u64 x) { uint64_t lo = (uint64_t)x; return lo ? __builtin_ctzll(lo) : 64 + __builtin_ctzll((uint64_t)(x >> 64)); }

static int W, H, N, FLAT = 0, F = 4, OFF = 0, NW = 3, NB = 3, PWN, S;
static int nbr[80][8], nnb[80];
static u64 kn[80];
static int psq[40], sqp[80];
static u64 wAttP[40], bAttP[40];
static vector<int> FILES;   // K45: pawn files (any set of files), instead of F consecutive files
static int distT[80][80];

struct Layer { u32 wm, bm; u64 WP, BP, Wat, Bat; };
static vector<Layer> layers;
static vector<int> idxW, idxB;
static vector<int32_t> lid2;
static int nSetB;
static uint8_t* tab = nullptr;

static inline int sq(int f, int r) { return r * W + f; }
static int wrapf(int f) { if (FLAT) return (f < 0 || f >= W) ? -1 : f; return ((f % W) + W) % W; }

static void init_geo() {
  N = W * H; S = 2 * N * N;
  for (int s = 0; s < N; s++) {
    int f = s % W, r = s / W; nnb[s] = 0; kn[s] = 0;
    for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
      if (!df && !dr) continue;
      int g = wrapf(f + df), q = r + dr;
      if (g < 0 || q < 0 || q >= H) continue;
      int t = sq(g, q);
      bool dup = false; for (int i = 0; i < nnb[s]; i++) if (nbr[s][i] == t) dup = true;
      if (!dup && t != s) { nbr[s][nnb[s]++] = t; kn[s] |= BIT(t); }
    }
  }
  for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) {
    int fd = abs(a % W - b % W); if (!FLAT) fd = min(fd, W - fd);
    distT[a][b] = max(fd, abs(a / W - b / W));
  }
  PWN = F * (H - 2);
  memset(sqp, -1, sizeof sqp);
  for (int i = 0; i < PWN; i++) {
    int f = FILES[i / (H - 2)];
    int r = 1 + i % (H - 2);
    psq[i] = sq(f, r); sqp[psq[i]] = i;
    wAttP[i] = bAttP[i] = 0;
    for (int df = -1; df <= 1; df += 2) {
      int g = wrapf(f + df); if (g < 0) continue;
      if (r + 1 < H) wAttP[i] |= BIT(sq(g, r + 1));
      if (r - 1 >= 0) bAttP[i] |= BIT(sq(g, r - 1));
    }
  }
}

static u64 attOf(u32 m, const u64* a) { u64 r = 0; while (m) { int i = __builtin_ctz(m); m &= m - 1; r |= a[i]; } return r; }
static u64 bbOf(u32 m) { u64 r = 0; while (m) { int i = __builtin_ctz(m); m &= m - 1; r |= BIT(psq[i]); } return r; }
static inline int lidOf(u32 wm, u32 bm) { return lid2[(size_t)idxW[wm] * nSetB + idxB[bm]]; }
static inline int sidx(int stm, int wk, int bk) { return (stm * N + wk) * N + bk; }
static inline uint8_t* TP(int lid) { return tab + (size_t)lid * (S / 4); }
static inline int TG(const uint8_t* p, int i) { return (p[i >> 2] >> ((i & 3) * 2)) & 3; }

struct Mv { int kind; int child; int wk, bk, ep; };   // kind 0 in-layer king move, 1 exit (child layer), 2 promotion (mover wins)
// ep: square skipped by a double step that can be captured, or -1.  stm 0 = White.
static int genMoves(int lid, int wk, int bk, int stm, int ep, Mv* out) {
  const Layer& L = layers[lid];
  int n = 0;
  u64 occ = L.WP | L.BP;
  int mk = stm ? bk : wk, ok = stm ? wk : bk;
  u64 myP = stm ? L.BP : L.WP, enP = stm ? L.WP : L.BP;
  u64 enAtt = stm ? L.Wat : L.Bat;
  u32 enM = stm ? L.wm : L.bm;
  const u64* enAP = stm ? wAttP : bAttP;
  u64 c = kn[mk] & ~kn[ok] & ~BIT(ok) & ~myP;
  while (c) {
    int t = ctzM(c); c &= c - 1;
    if ((enP >> t) & 1) {
      int pi = sqp[t];
      u32 nem = enM & ~(1u << pi);
      if ((attOf(nem, enAP) >> t) & 1) continue;
      Mv& m = out[n++]; m.kind = 1; m.ep = -1;
      m.child = stm ? lidOf(nem, L.bm) : lidOf(L.wm, nem);
      if (stm) { m.child = lidOf(nem, L.bm); } else { m.child = lidOf(L.wm, nem); }
      m.wk = stm ? wk : t; m.bk = stm ? t : bk;
    } else {
      if ((enAtt >> t) & 1) continue;
      Mv& m = out[n++]; m.kind = 0; m.child = lid; m.ep = -1; m.wk = stm ? wk : t; m.bk = stm ? t : bk;
    }
  }
  bool inchk = (enAtt >> mk) & 1;
  u32 myM = stm ? L.bm : L.wm;
  int dir = stm ? -1 : 1;
  int last = stm ? 0 : H - 1, second = stm ? H - 2 : 1;
  const u64* myAP = stm ? bAttP : wAttP;
  (void)myAP;
  u32 m2 = myM;
  while (m2) {
    int pi = __builtin_ctz(m2); m2 &= m2 - 1;
    int s = psq[pi], r = s / W, f = s % W;
    int t = s + dir * W;
    if (!((occ >> t) & 1) && t != wk && t != bk) {
      if (!inchk) {
        if (r + dir == last) { Mv& m = out[n++]; m.kind = 2; m.child = -1; m.wk = wk; m.bk = bk; m.ep = -1; }
        else {
          int pj = sqp[t];
          u32 nmm = myM ^ (1u << pi) ^ (1u << pj);
          Mv& m = out[n++]; m.kind = 1; m.ep = -1; m.wk = wk; m.bk = bk;
          m.child = stm ? lidOf(L.wm, nmm) : lidOf(nmm, L.bm);
          if (r == second) {
            int t2 = t + dir * W;
            if (!((occ >> t2) & 1) && t2 != wk && t2 != bk) {
              int pj2 = sqp[t2];
              u32 nm2 = myM ^ (1u << pi) ^ (1u << pj2);
              int epq = -1;
              for (int d = -1; d <= 1; d += 2) {
                int g = wrapf(f + d); if (g < 0) continue;
                if ((enP >> sq(g, r + 2 * dir)) & 1) epq = t;
              }
              Mv& m3 = out[n++]; m3.kind = 1; m3.ep = epq; m3.wk = wk; m3.bk = bk;
              m3.child = stm ? lidOf(L.wm, nm2) : lidOf(nm2, L.bm);
            }
          }
        }
      }
    }
    for (int d = -1; d <= 1; d += 2) {
      int g = wrapf(f + d); if (g < 0) continue;
      int tt = sq(g, r + dir);
      if (r + dir == last) continue;
      if (!((enP >> tt) & 1)) continue;
      int pj = sqp[tt];
      u32 nem = enM & ~(1u << pj);
      if ((attOf(nem, enAP) >> mk) & 1) continue;
      u32 nmm = myM ^ (1u << pi) ^ (1u << pj);
      Mv& m = out[n++]; m.kind = 1; m.ep = -1; m.wk = wk; m.bk = bk;
      m.child = stm ? lidOf(nem, nmm) : lidOf(nmm, nem);
    }
    if (ep >= 0) {
      // the opponent double-stepped over ep; its pawn stands at ep - dir*W ... (opponent moves in direction -dir)
      int land = ep - dir * W;     // landing square of the opponent pawn is one step further along ITS direction = ep + (-dir)*W
      land = ep + (-dir) * W;
      // my pawn must stand beside the landing square, i.e. on the rank of `land`, and capture to ep
      if (s / W == land / W && (s % W != land % W)) {
        int fe = ep % W; bool ok2 = false;
        for (int d = -1; d <= 1; d += 2) { int g = wrapf(fe + d); if (g >= 0 && sq(g, s / W) == s) ok2 = true; }
        if (ok2 && ((enP >> land) & 1) && !((occ >> ep) & 1) && ep != wk && ep != bk) {
          int pl = sqp[land], pe = sqp[ep];
          u32 nem = enM & ~(1u << pl);
          if (!((attOf(nem, enAP) >> mk) & 1)) {
            u32 nmm = myM ^ (1u << pi) ^ (1u << pe);
            Mv& m = out[n++]; m.kind = 1; m.ep = -1; m.wk = wk; m.bk = bk;
            m.child = stm ? lidOf(nem, nmm) : lidOf(nmm, nem);
          }
        }
      }
    }
  }
  return n;
}

static int evalState(int lid, int wk, int bk, int stm, int ep);
// value of the move for the mover: 1 win, 0 draw, 2 loss  (child value seen from the opponent)
static int moveVal(int lid, const Mv& m, int stm, int wk, int bk, int ep) {
  if (m.kind == 2) return 1;
  int cv;
  if (m.kind == 0) cv = TG(TP(lid), sidx(1 - stm, m.wk, m.bk));
  else if (m.ep >= 0) cv = evalState(m.child, m.wk, m.bk, 1 - stm, m.ep);
  else cv = TG(TP(m.child), sidx(1 - stm, m.wk, m.bk));
  if (cv == 3) { fprintf(stderr, "internal: illegal child state\n"); exit(3); }
  return cv == 2 ? 1 : (cv == 1 ? 2 : 0);
}
static int evalState(int lid, int wk, int bk, int stm, int ep) {
  Mv mv[96];
  int n = genMoves(lid, wk, bk, stm, ep, mv);
  const Layer& L = layers[lid];
  if (!n) { bool chk = stm ? ((L.Wat >> bk) & 1) : ((L.Bat >> wk) & 1); return chk ? 2 : 0; }
  bool dr = false;
  for (int i = 0; i < n; i++) {
    int v = moveVal(lid, mv[i], stm, wk, bk, ep);
    if (v == 1) return 1;
    if (v == 0) dr = true;
  }
  return dr ? 0 : 2;
}

static vector<uint8_t> cntA;
static vector<int32_t> queueA;

static vector<uint8_t> scratch;
static void solveLayer(int lid) {
  const Layer& L = layers[lid];
  uint8_t* T = scratch.data();
  memset(T, 3, S);
  u64 occ = L.WP | L.BP;
  int qh = 0, qt = 0;
  Mv mv[96];
  for (int stm = 0; stm < 2; stm++)
    for (int wk = 0; wk < N; wk++) {
      if ((occ >> wk) & 1) continue;
      for (int bk = 0; bk < N; bk++) {
        if (bk == wk || ((occ >> bk) & 1) || ((kn[wk] >> bk) & 1)) continue;
        if (stm == 0 ? ((L.Wat >> bk) & 1) : ((L.Bat >> wk) & 1)) continue;
        int id = sidx(stm, wk, bk);
        T[id] = 0;
      }
    }
  for (int stm = 0; stm < 2; stm++)
    for (int wk = 0; wk < N; wk++)
      for (int bk = 0; bk < N; bk++) {
        int id = sidx(stm, wk, bk);
        if (T[id] != 0) continue;
        int n = genMoves(lid, wk, bk, stm, -1, mv);
        bool win = false; int cnt = 0;
        for (int i = 0; i < n; i++) {
          if (mv[i].kind == 0) { cnt++; continue; }
          int v = moveVal(lid, mv[i], stm, wk, bk, -1);
          if (v == 1) { win = true; break; }
          if (v == 0) cnt++;
        }
        if (win) { T[id] = 1; queueA[qt++] = id; }
        else if (n == 0) {
          bool chk = stm ? ((L.Wat >> bk) & 1) : ((L.Bat >> wk) & 1);
          if (chk) { T[id] = 2; queueA[qt++] = id; }
        } else if (cnt == 0) { T[id] = 2; queueA[qt++] = id; }
        else cntA[id] = (uint8_t)cnt;
      }
  while (qh < qt) {
    int t = queueA[qh++];
    int v = T[t];
    int stm = t / (N * N), rem = t % (N * N), wk = rem / N, bk = rem % N;
    int opp = 1 - stm;
    int vk = opp == 0 ? wk : bk, other = opp == 0 ? bk : wk;
    for (int i = 0; i < nnb[vk]; i++) {
      int u = nbr[vk][i];
      if (u == other || ((kn[other] >> u) & 1)) continue;
      int s = opp == 0 ? sidx(opp, u, bk) : sidx(opp, wk, u);
      if (T[s] != 0) continue;
      if (v == 2) { T[s] = 1; queueA[qt++] = s; }
      else { if (--cntA[s] == 0) { T[s] = 2; queueA[qt++] = s; } }
    }
  }
  uint8_t* P = TP(lid);
  for (int i = 0; i < S; i += 4) P[i >> 2] = (uint8_t)(T[i] | (T[i + 1] << 2) | (T[i + 2] << 4) | (T[i + 3] << 6));
}

// ---------------------------------------------------------------- names / printing
static string sqname(int s) { char b[8]; snprintf(b, 8, "%c%d", 'a' + s % W, s / W + 1); return b; }
static string posStr(int lid, int wk, int bk, int stm, int ep = -1) {
  const Layer& L = layers[lid];
  string r = "K" + sqname(wk) + " k" + sqname(bk);
  u32 m = L.wm; while (m) { int i = __builtin_ctz(m); m &= m - 1; r += " P" + sqname(psq[i]); }
  m = L.bm; while (m) { int i = __builtin_ctz(m); m &= m - 1; r += " p" + sqname(psq[i]); }
  r += stm ? " b " : " w "; r += ep >= 0 ? sqname(ep) : "-";
  return r;
}
static string mvName(int lid, const Mv& m, int stm, int wk, int bk) {
  if (m.kind == 2) return "promo";
  if (m.kind == 0 || (m.wk != wk || m.bk != bk)) return string("K") + sqname(stm ? bk : wk) + sqname(stm ? m.bk : m.wk);
  return "pawn";
}

// ---------------------------------------------------------------- tests
static bool KWIN = false; static u64 kwinMask = ~(u64)0;
struct Cnt { long long placements = 0, f1 = 0, f2 = 0, f3 = 0, f3one = 0, f3val = 0, f4 = 0, noFreezeAtLeastOne = 0, promoFreeze = 0,
  failChk = 0, failNoMove = 0, failLeak = 0, someZero = 0, half = 0, lemmaChecked = 0, lemmaNoShuttle = 0, lemmaLegalOther = 0, lemmaViol = 0, f2v = 0, f3v = 0, f3vFail = 0, f3vPromo = 0, f3vExact = 0, f4kingfreeze = 0, f2all = 0; };
static Cnt cnt_[2];
static long long badHist[2][10], badHist1[2][3];
static vector<string> hits_[2], loose_[2], half_[2], near1_[2];
static int PRINTQ = 30;

// does every legal move of `stm` at (lid,wk,bk,ep) lose at once? returns number of moves, allLose via ref
static int allLose(int lid, int wk, int bk, int stm, int ep, bool& all) {
  Mv mv[96]; int n = genMoves(lid, wk, bk, stm, ep, mv); all = true;
  for (int i = 0; i < n; i++) if (moveVal(lid, mv[i], stm, wk, bk, ep) != 2) { all = false; break; }
  return n;
}


#include <map>
static bool DIAG = false;
static map<string, long long> diag, halfClass;
static string classOf(int lid, const Mv& m, int stm, int wk, int bk) {
  if (m.kind == 2) return "promo";
  if (m.kind == 0) return "Kstep";
  if (m.wk != wk || m.bk != bk) return "Kcap";
  const Layer& A = layers[lid]; const Layer& B = layers[m.child];
  u32 enA = stm ? A.wm : A.bm, enB = stm ? B.wm : B.bm;
  if (__builtin_popcount(enA) != __builtin_popcount(enB)) return "Pcap";
  u32 mA = stm ? A.bm : A.wm, mB = stm ? B.bm : B.wm;
  u32 gone = mA & ~mB, came = mB & ~mA; int a = __builtin_ctz(gone), b = __builtin_ctz(came);
  int dr = abs(psq[a] / W - psq[b] / W);
  return dr == 2 ? "Pdbl" : "Ppush";
}

static void testUnder(int lid, int sh) {
  const Layer& L = layers[lid];
  Cnt& C = cnt_[sh];
  int fr = 1 - sh;
  u64 occ = L.WP | L.BP;
  u64 shAtt = sh ? L.Wat : L.Bat, frAtt = sh ? L.Bat : L.Wat;
  u64 allsq = BIT(N) - 1;
  u64 safeSh = allsq & ~occ & ~shAtt & kwinMask, safeFr = allsq & ~occ & ~frAtt & kwinMask;
  Mv mv[96];
  for (u64 a = safeSh; a; a &= a - 1) {
    int u = ctzM(a);
    for (u64 b = kn[u] & safeSh; b; b &= b - 1) {
      int v = ctzM(b);
      if (v < u) continue;
      u64 comp = safeFr & ~kn[u] & ~kn[v] & ~BIT(u) & ~BIT(v);
      for (u64 c = comp; c; c &= c - 1) {
        int t = ctzM(c);
        C.placements++;
        int z[2] = {u, v};
        // U1 at both shuttler roots
        bool ok = true;
        for (int aa = 0; aa < 2 && ok; aa++) {
          int wk = sh ? t : z[aa], bk = sh ? z[aa] : t;
          int n = genMoves(lid, wk, bk, sh, -1, mv);
          int nsh = 0;
          for (int i = 0; i < n && ok; i++) {
            if (mv[i].kind == 0 && (sh ? mv[i].bk : mv[i].wk) == z[1 - aa]) { nsh++; continue; }
            if (moveVal(lid, mv[i], sh, wk, bk, -1) != 2) ok = false;
          }
          if (nsh != 1) ok = false;
        }
        if (!ok) continue;
        C.f1++;
        // U2 at both freezer roots
        struct Fz { int lid, wk, bk, ep; bool kingmove; };
        vector<Fz> fz[2];
        bool promo = false, nofz = false;
        for (int aa = 0; aa < 2; aa++) {
          int wk = sh ? t : z[aa], bk = sh ? z[aa] : t;
          int n = genMoves(lid, wk, bk, fr, -1, mv);
          for (int i = 0; i < n; i++) {
            if (mv[i].kind == 2) { promo = true; continue; }
            if (moveVal(lid, mv[i], fr, wk, bk, -1) == 2) continue;   // loses at once
            fz[aa].push_back({mv[i].kind == 0 ? lid : mv[i].child, mv[i].wk, mv[i].bk, mv[i].ep, mv[i].kind != 1 || mv[i].wk != wk || mv[i].bk != bk});
          }
          if (fz[aa].empty()) nofz = true;
        }
        {   // K26 referee style counts (promotion freezes count as value L): placements with U1, >= 1 non-losing move at both roots, U3 over the non-promotion freezes
          bool bothv = true; bool anyPromoV = false;
          for (int aa = 0; aa < 2; aa++) {
            int wk = sh ? t : z[aa], bk = sh ? z[aa] : t; Mv m9[96]; int n9 = genMoves(lid, wk, bk, fr, -1, m9); bool pr = false;
            for (int i = 0; i < n9; i++) if (m9[i].kind == 2) pr = true;
            if (pr) anyPromoV = true;
            if (fz[aa].empty() && !pr) bothv = false;
          }
          if (bothv) {
            bool u3v = true, u4v = true;
            for (int aa = 0; aa < 2; aa++) for (auto& f : fz[aa]) {
              bool all; int n = allLose(f.lid, f.wk, f.bk, sh, f.ep, all); if (n < 1 || !all) u3v = false;
              const Layer& Q = layers[f.lid];
              bool shAtt = (sh == 0) ? (((Q.Bat >> f.wk) & 1) != 0) : (((Q.Wat >> f.bk) & 1) != 0);
              if (shAtt) u4v = false; else { bool all4; int n4 = allLose(f.lid, f.wk, f.bk, fr, -1, all4); if (n4 < 1 || !all4) u4v = false; }
            }
            C.f2v++;
            if (u3v) { C.f3v++; if (!u4v) C.f3vFail++; else if (anyPromoV) C.f3vPromo++; else C.f3vExact++; }
          }
        }
        if (promo) { C.promoFreeze++; }
        if (nofz) { C.noFreezeAtLeastOne++; continue; }
        if (promo) continue;
        C.f2++;
        // U3 for every freeze
        bool u3 = true;
        for (int aa = 0; aa < 2 && u3; aa++)
          for (auto& f : fz[aa]) {
            bool all; int n = allLose(f.lid, f.wk, f.bk, sh, f.ep, all);
            if (n < 1 || !all) { u3 = false; break; }
          }
        if (!u3) continue;
        C.f3++;
        if (DIAG) {
          for (int aa = 0; aa < 2; aa++) for (auto& f : fz[aa]) {
            int wk0 = sh ? t : z[aa], bk0 = sh ? z[aa] : t;
            // class of the freeze: recompute from the root move list
            Mv m0[96]; int n0 = genMoves(lid, wk0, bk0, fr, -1, m0); string fc = "?";
            for (int i = 0; i < n0; i++) if (m0[i].kind != 2 && (m0[i].kind == 0 ? lid : m0[i].child) == f.lid && m0[i].wk == f.wk && m0[i].bk == f.bk && m0[i].ep == f.ep && moveVal(lid, m0[i], fr, wk0, bk0, -1) != 2) { fc = classOf(lid, m0[i], fr, wk0, bk0); break; }
            const Layer& Q = layers[f.lid];
            bool shAtt = (sh == 0) ? (((Q.Bat >> f.wk) & 1) != 0) : (((Q.Wat >> f.bk) & 1) != 0);
            if (shAtt) { diag["freeze=" + fc + " : q illegal for freezer (check)"]++; continue; }
            Mv m1[96]; int n1 = genMoves(f.lid, f.wk, f.bk, fr, -1, m1);
            string sig; int nl = 0;
            for (int i = 0; i < n1; i++) { int v = moveVal(f.lid, m1[i], fr, f.wk, f.bk, -1); if (v != 2) { nl++; string c = classOf(f.lid, m1[i], fr, f.wk, f.bk) + (v == 1 ? "!" : "="); if (sig.find(c) == string::npos) sig += c + ","; } }
            diag["freeze=" + fc + " : nonlosing at q = " + (nl ? sig : "none")]++;
          }
        }
        if (fz[0].size() == 1 && fz[1].size() == 1) C.f3one++;
        // U4
        bool u4 = true; int why = 0; bool rootOK[2] = {true, true}; int nzero = 0;
        for (int aa = 0; aa < 2; aa++)
          for (auto& f : fz[aa]) {
            const Layer& Q = layers[f.lid];
            // after flipping the side to move to the freezer, the side NOT to move is the shuttler: its king must not be attacked by the freezer's pawns
            bool shAttacked = (sh == 0) ? (((Q.Bat >> f.wk) & 1) != 0) : (((Q.Wat >> f.bk) & 1) != 0);
            if (shAttacked) { rootOK[aa] = false; if (u4) why = 1; u4 = false; continue; }
            bool all; int n = allLose(f.lid, f.wk, f.bk, fr, -1, all);
            if (n < 1) { rootOK[aa] = false; if (u4) why = 2; u4 = false; continue; }
            if (!all) { rootOK[aa] = false; if (u4) why = 3; u4 = false; continue; }
            nzero++;
          }
        string ps = posStr(lid, sh ? t : u, sh ? u : t, sh) + "  shuttle " + sqname(u) + sqname(v);
        if (nzero > 0) C.someZero++;
        { int totfz = (int)fz[0].size() + (int)fz[1].size(); int bad = totfz - nzero; badHist[sh][min(bad, 9)]++; if (totfz == 2) { badHist1[sh][bad]++; if (bad == 1 && (int)near1_[sh].size() < 200) near1_[sh].push_back(posStr(lid, sh ? t : u, sh ? u : t, sh) + "  shuttle " + sqname(u) + sqname(v) + (rootOK[0] ? "  zero-root=" : "  zero-root=") + sqname(rootOK[0] ? u : v)); } }
        // Lemma 4.10 check (mechanics): for every freeze m at root aa whose q is a mutual zugzwang (rootOK) and whose shuttle is legal in q:
        //   (i) the shuttle loses at once (U3); (ii) if m is legal at the other root it is not a freeze there (it loses at once)
        for (int aa = 0; aa < 2; aa++) {
          if (!rootOK[aa]) continue;
          for (auto& f : fz[aa]) {
            // shuttle legal in q?
            Mv q1[96]; int n1 = genMoves(f.lid, f.wk, f.bk, sh, f.ep, q1); bool shl = false;
            for (int i = 0; i < n1; i++) if (q1[i].kind == 0 && (sh ? q1[i].bk : q1[i].wk) == z[1 - aa]) shl = true;
            if (!shl) { C.lemmaNoShuttle++; continue; }
            C.lemmaChecked++;
            // is the same move legal at the other root?  look for a freezer move with the same child layer, ep and king squares
            int wk1 = sh ? t : z[1 - aa], bk1 = sh ? z[1 - aa] : t;
            Mv r1[96]; int nr = genMoves(lid, wk1, bk1, fr, -1, r1);
            for (int i = 0; i < nr; i++) {
              if (r1[i].kind == 2) continue;
              int ch = r1[i].kind == 0 ? lid : r1[i].child;
              if (ch == f.lid && r1[i].ep == f.ep && (sh ? (r1[i].wk == f.wk) : (r1[i].bk == f.bk))) {
                C.lemmaLegalOther++;
                if (moveVal(lid, r1[i], fr, wk1, bk1, -1) != 2) C.lemmaViol++;
              }
            }
          }
        }
        if (rootOK[0] != rootOK[1]) {
          C.half++;
          int ra = rootOK[0] ? 0 : 1; string fcl;
          for (auto& f : fz[ra]) {
            int wk0 = sh ? t : z[ra], bk0 = sh ? z[ra] : t; Mv m0[96]; int n0 = genMoves(lid, wk0, bk0, fr, -1, m0);
            for (int i = 0; i < n0; i++) if (m0[i].kind != 2 && (m0[i].kind == 0 ? lid : m0[i].child) == f.lid && m0[i].wk == f.wk && m0[i].bk == f.bk && m0[i].ep == f.ep && moveVal(lid, m0[i], fr, wk0, bk0, -1) != 2) fcl += classOf(lid, m0[i], fr, wk0, bk0) + " ";
          }
          halfClass[fcl]++;
          if ((int)half_[sh].size() < PRINTQ) half_[sh].push_back(ps + (rootOK[0] ? "  rootOK=z0=" : "  rootOK=z1=") + sqname(rootOK[0] ? u : v) + "  freezes: " + fcl);
        }
        if (!u4) {
          if (why == 1) C.failChk++; else if (why == 2) C.failNoMove++; else C.failLeak++;
          if ((int)loose_[sh].size() < PRINTQ) loose_[sh].push_back(ps);
          continue;
        }
        C.f4++;
        hits_[sh].push_back(ps);
      }
    }
  }
}

// exact dud (both kings shuttle, every other move of the mover loses at once, all 8 roots)
static long long dudCount = 0, dudPlace = 0; static vector<string> dudHits;
static void testDud(int lid) {
  const Layer& L = layers[lid];
  u64 occ = L.WP | L.BP;
  u64 allsq = BIT(N) - 1;
  u64 safeW = allsq & ~occ & ~L.Bat & kwinMask, safeB = allsq & ~occ & ~L.Wat & kwinMask;
  Mv mv[96];
  for (u64 a = safeW; a; a &= a - 1) {
    int u = ctzM(a);
    for (u64 b = kn[u] & safeW; b; b &= b - 1) {
      int v = ctzM(b); if (v < u) continue;
      u64 compB = safeB & ~kn[u] & ~kn[v] & ~BIT(u) & ~BIT(v);
      for (u64 a2 = compB; a2; a2 &= a2 - 1) {
        int x = ctzM(a2);
        for (u64 b2 = kn[x] & compB; b2; b2 &= b2 - 1) {
          int y = ctzM(b2); if (y < x) continue;
          if (distT[x][u] < 2 || distT[x][v] < 2 || distT[y][u] < 2 || distT[y][v] < 2) continue;
          dudPlace++;
          int zw[2] = {u, v}, zb[2] = {x, y};
          bool ok = true;
          for (int i = 0; i < 2 && ok; i++) for (int j = 0; j < 2 && ok; j++) for (int stm = 0; stm < 2 && ok; stm++) {
            int wk = zw[i], bk = zb[j];
            int n = genMoves(lid, wk, bk, stm, -1, mv); int nsh = 0;
            for (int k = 0; k < n && ok; k++) {
              if (mv[k].kind == 0 && (stm ? (mv[k].bk == zb[1 - j]) : (mv[k].wk == zw[1 - i]))) { nsh++; continue; }
              if (moveVal(lid, mv[k], stm, wk, bk, -1) != 2) ok = false;
            }
            if (nsh != 1) ok = false;
          }
          if (ok) { dudCount++; dudHits.push_back(posStr(lid, u, x, 0) + " wz " + sqname(u) + sqname(v) + " bz " + sqname(x) + sqname(y)); }
        }
      }
    }
  }
}

// ---------------------------------------------------------------- main
int main(int argc, char** argv) {
  string mode = "both"; int dumpN = 0; unsigned seed = 1; bool kind_cyl = true;
  for (int i = 1; i < argc; i++) {
    string a = argv[i];
    auto nx = [&]() { return string(argv[++i]); };
    if (a == "--kind") kind_cyl = (nx() == "cyl");
    else if (a == "--W") W = atoi(nx().c_str());
    else if (a == "--H") H = atoi(nx().c_str());
    else if (a == "--F") F = atoi(nx().c_str());
    else if (a == "--off") OFF = atoi(nx().c_str());
    else if (a == "--files") { string t = nx(); FILES.clear(); size_t p = 0; while (p < t.size()) { size_t q = t.find(',', p); if (q == string::npos) q = t.size(); FILES.push_back(atoi(t.substr(p, q - p).c_str())); p = q + 1; } F = FILES.size(); }
    else if (a == "--nw") NW = atoi(nx().c_str());
    else if (a == "--nb") NB = atoi(nx().c_str());
    else if (a == "--mode") mode = nx();
    else if (a == "--kwin") KWIN = true;
    else if (a == "--dump") { dumpN = atoi(nx().c_str()); seed = atoi(nx().c_str()); }
    else if (a == "--diag") DIAG = true;
    else if (a == "--print-q") PRINTQ = atoi(nx().c_str());
    else { fprintf(stderr, "bad arg %s\n", a.c_str()); return 1; }
  }
  FLAT = !kind_cyl;
  if (FILES.empty()) { for (int i = 0; i < F; i++) FILES.push_back(OFF + i); }
  init_geo();
  if (KWIN) { kwinMask = 0; for (int s = 0; s < N; s++) { int f = s % W; bool in = false; for (int i = 0; i < F; i++) { int g = OFF + i; if (!FLAT) g %= W; if (g == f) in = true; } if (in) kwinMask |= BIT(s); } }
  // pawn mask sets
  auto build = [&](int lim, vector<int>& idx, vector<u32>& list) {
    idx.assign((size_t)1 << PWN, -1);
    for (u32 m = 0; m < ((u32)1 << PWN); m++) if (__builtin_popcount(m) <= lim) { idx[m] = list.size(); list.push_back(m); }
  };
  vector<u32> ws, bs; build(NW, idxW, ws); build(NB, idxB, bs); nSetB = bs.size();
  // layers, sorted by (count asc, advancement desc)
  struct Tmp { u32 wm, bm; int cnt, adv; };
  vector<Tmp> tl;
  for (u32 w : ws) for (u32 b : bs) {
    if (w & b) continue;
    int adv = 0; u32 m = w; while (m) { int i = __builtin_ctz(m); m &= m - 1; adv += psq[i] / W - 1; }
    m = b; while (m) { int i = __builtin_ctz(m); m &= m - 1; adv += (H - 2) - psq[i] / W; }
    tl.push_back({w, b, __builtin_popcount(w) + __builtin_popcount(b), adv});
  }
  sort(tl.begin(), tl.end(), [](const Tmp& a, const Tmp& b) { if (a.cnt != b.cnt) return a.cnt < b.cnt; if (a.adv != b.adv) return a.adv > b.adv; if (a.wm != b.wm) return a.wm < b.wm; return a.bm < b.bm; });
  lid2.assign(ws.size() * nSetB, -1);
  layers.resize(tl.size());
  for (size_t i = 0; i < tl.size(); i++) {
    Layer& L = layers[i]; L.wm = tl[i].wm; L.bm = tl[i].bm; L.WP = bbOf(L.wm); L.BP = bbOf(L.bm);
    L.Wat = attOf(L.wm, wAttP); L.Bat = attOf(L.bm, bAttP);
    lid2[(size_t)idxW[L.wm] * nSetB + idxB[L.bm]] = i;
  }
  fprintf(stderr, "board %s:%dx%d window F=%d off=%d pawns<=%d+%d layers=%zu states/layer=%d table=%.2f GB\n", FLAT ? "flat" : "cyl", W, H, F, OFF, NW, NB, layers.size(), S, (double)layers.size() * S / 4e9);
  { double need = (double)layers.size() * (S / 4) + 7.0 * S * 4;   // K67: size before allocating (table + per-layer work arrays), exit over 2 GB
    if (need > 2.0e9) { fprintf(stderr, "K67 memory guard: estimated %.2f GB > 2.0 GB, not allocating\n", need / 1e9); return 3; } }
  tab = (uint8_t*)malloc((size_t)layers.size() * (S / 4));
  if (!tab) { fprintf(stderr, "alloc failed\n"); return 2; }
  cntA.assign(S, 0); queueA.assign(S, 0); scratch.assign(S, 0);
  time_t t0 = time(0);
  for (size_t i = 0; i < layers.size(); i++) {
    solveLayer(i);
    for (int sh = 0; sh < 2; sh++) {
      if (!(mode == "both" || (mode == "under" && sh == 0) || (mode == "over" && sh == 1))) continue;
      Cnt b4 = cnt_[sh]; testUnder(i, sh); const Cnt& c = cnt_[sh];
      bool blocked = layers[i].wm && __builtin_popcount(layers[i].wm) == __builtin_popcount(layers[i].bm);
      { u32 m = layers[i].wm; while (m) { int k = __builtin_ctz(m); m &= m - 1; int t = psq[k] + W; if (!(t < N && sqp[t] >= 0 && ((layers[i].bm >> sqp[t]) & 1))) blocked = false; } }
      if (c.f1 - b4.f1 > 0 || blocked) {
        string key; { u32 m = layers[i].wm; while (m) { int k = __builtin_ctz(m); m &= m - 1; key += "P" + sqname(psq[k]); } m = layers[i].bm; while (m) { int k = __builtin_ctz(m); m &= m - 1; key += "p" + sqname(psq[k]); } }
        printf("LAYER %s sh=%d%s pl=%lld f1=%lld nofz=%lld promo=%lld f2=%lld f3=%lld f4=%lld\n", key.c_str(), sh, blocked ? " B" : "", c.placements - b4.placements, c.f1 - b4.f1, c.noFreezeAtLeastOne - b4.noFreezeAtLeastOne, c.promoFreeze - b4.promoFreeze, c.f2 - b4.f2, c.f3 - b4.f3, c.f4 - b4.f4);
      }
    }
    if (mode == "dud") testDud(i);
    if ((i & 8191) == 8191) fprintf(stderr, "[%5lds] layer %zu/%zu  F3 %lld/%lld  F4 %lld/%lld\n", (long)(time(0) - t0), i + 1, layers.size(), cnt_[0].f3, cnt_[1].f3, cnt_[0].f4, cnt_[1].f4);
  }
  for (int sh = 0; sh < 2; sh++) {
    if (!(mode == "both" || (mode == "under" && sh == 0) || (mode == "over" && sh == 1))) continue;
    Cnt& C = cnt_[sh];
    printf("RESULT %s shuttler=%s placements=%lld F1(U1 at both shuttler roots)=%lld noFreeze=%lld promoFreeze=%lld F2(U2)=%lld F3(U3 loose)=%lld F3one=%lld F4(exact U4)=%lld failChk=%lld failNoMove=%lld failLeak=%lld someZero=%lld halfExact=%lld lemma410(checked=%lld noShuttle=%lld legalAtOther=%lld violations=%lld) refstyle(U1+U2=%lld U3=%lld failU4=%lld promoU4ok=%lld exact=%lld)\n",
           FLAT ? "flat" : "cyl", sh ? "black(over)" : "white(under)", C.placements, C.f1, C.noFreezeAtLeastOne, C.promoFreeze, C.f2, C.f3, C.f3one, C.f4, C.failChk, C.failNoMove, C.failLeak, C.someZero, C.half, C.lemmaChecked, C.lemmaNoShuttle, C.lemmaLegalOther, C.lemmaViol, C.f2v, C.f3v, C.f3vFail, C.f3vPromo, C.f3vExact);
    for (auto& s : hits_[sh]) printf("HIT sh=%d %s\n", sh, s.c_str());
    for (auto& s : loose_[sh]) printf("LOOSE sh=%d %s\n", sh, s.c_str());
    for (auto& s : half_[sh]) printf("HALF sh=%d %s\n", sh, s.c_str());
    for (auto& s : near1_[sh]) printf("NEAR1 sh=%d %s\n", sh, s.c_str());
  }
  for (auto& kv : halfClass) printf("HALFCLASS %lld %s\n", kv.second, kv.first.c_str());
  for (auto& kv : diag) printf("DIAG %lld %s\n", kv.second, kv.first.c_str());
  for (int sh = 0; sh < 2; sh++) { printf("BADHIST sh=%d (non-zero freezes among all freezes of the two roots, F3 placements; last bin = 9 or more):", sh); for (int i = 0; i < 10; i++) printf(" %lld", badHist[sh][i]); printf("\n"); printf("BADHIST1 sh=%d (placements with exactly one freeze at each root: 0, 1, 2 non-zero freezes): %lld %lld %lld\n", sh, badHist1[sh][0], badHist1[sh][1], badHist1[sh][2]); }
  if (mode == "dud") { printf("DUD placements=%lld exact=%lld\n", dudPlace, dudCount); for (auto& s : dudHits) printf("DUDHIT %s\n", s.c_str()); }
  if (dumpN) {
    srand(seed);
    for (int k = 0; k < dumpN; k++) {
      int lid = rand() % layers.size(); int stm = rand() % 2, wk = rand() % N, bk = rand() % N;
      int v = TG(TP(lid), sidx(stm, wk, bk));
      if (v == 3) { k--; continue; }
      // White's point of view
      char c = v == 0 ? 'D' : ((v == 1) == (stm == 0) ? 'W' : 'L');
      printf("DUMP %s | %c\n", posStr(lid, wk, bk, stm).c_str(), c);
    }
  }
  free(tab);
  return 0;
}
