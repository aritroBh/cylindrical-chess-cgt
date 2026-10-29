// kq.cpp -- K28: layered retrograde solver for kings + pawns + promoted officers on a small FLAT board.
// Written from kings/SPEC.md (not from kpsolve.c). Differences from SPEC.md, all on purpose:
//   * no en passant and no double step (the program aborts if a pawn stands on its own second rank);
//   * the officer cap can be set per colour (--capw, --capb) in addition to the total (--cap);
//   * the promotion set can be set per colour (--promw, --promb).
// With --cap C and the other options at their defaults it computes exactly what `kpsolve --cap C` computes.
// A promotion is *capped* if the position after it holds more than --cap officers, or more than --capw (--capb)
// officers of the mover's colour. A capped promotion ends the game at once: bound A = White wins, bound B = Black wins.
// So A >= true value >= B from White's point of view. Restricting the promotion set or the per-colour cap of a side
// can only make that side weaker, so A and B stay valid bounds for the game in which that side is *not* restricted
// in the direction (A: restrict Black / B: restrict White): see FINDINGS.md.
//
// Method: layers = (white pawns, black pawns, sorted officer codes). Pawn moves and every capture leave the layer;
// inside a layer only king / officer non-capturing moves are made. Child layers are solved first (recursion).
// A layer is solved by counting retrograde analysis: a forward pass classifies every state (win by a move that leaves
// the layer, loss with no move, in-layer move count) and a level-synchronous backward pass over *reverse* moves
// propagates. Stored layers are packed 2 bits per state (0 draw, 1 win for the side to move, 2 loss, 3 illegal).
// Usage: kq [--board flat:7x6] [--cap C] [--capw X] [--capb Y] [--promw QRBN] [--promb QRBN]
//           [--bound A|B|AB] [--threads T] [--moves] [--quiet] < positions
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <thread>
#include <vector>
using namespace std;
typedef unsigned long long u64;
typedef uint32_t u32;
typedef uint8_t u8;

static int W = 7, H = 6, N = 42;
static int TOTCAP = 1, CAPC[2] = {9, 9}, BOUND = 0, NT = 1, WANTMOVES = 0, QUIET = 0;
static vector<int> PROMO[2];
static string CACHE;  // directory for solved layers (one directory per parameter set)
static const char TCH[] = "QRBN";
static inline u64 bit(int s) { return 1ULL << s; }
static inline int fileOf(int s) { return s % W; }
static inline int rankOf(int s) { return s / W; }

// ---------------- geometry ----------------
static u64 KINGM[64], KNIGHTM[64], PAWNFROM[2][64], RAYM[8][64];
static const int DF[8] = {1, -1, 0, 0, 1, 1, -1, -1}, DR[8] = {0, 0, 1, -1, 1, -1, 1, -1};
static const int NDF[8] = {1, 2, -1, -2, 1, 2, -1, -2}, NDR[8] = {2, 1, 2, 1, -2, -1, -2, -1};
static inline bool dpos(int d) { return d == 0 || d == 2 || d == 4 || d == 6; }  // square index grows along the ray

static void initGeom() {
  N = W * H;
  for (int s = 0; s < N; s++) {
    int f = fileOf(s), r = rankOf(s);
    KINGM[s] = KNIGHTM[s] = 0;
    PAWNFROM[0][s] = PAWNFROM[1][s] = 0;
    for (int d = 0; d < 8; d++) {
      int nf = f + DF[d], nr = r + DR[d];
      if (nf >= 0 && nf < W && nr >= 0 && nr < H) KINGM[s] |= bit(nr * W + nf);
      nf = f + NDF[d]; nr = r + NDR[d];
      if (nf >= 0 && nf < W && nr >= 0 && nr < H) KNIGHTM[s] |= bit(nr * W + nf);
      RAYM[d][s] = 0;
      nf = f + DF[d]; nr = r + DR[d];
      while (nf >= 0 && nf < W && nr >= 0 && nr < H) { RAYM[d][s] |= bit(nr * W + nf); nf += DF[d]; nr += DR[d]; }
    }
    for (int df = -1; df <= 1; df += 2) {
      if (f + df < 0 || f + df >= W) continue;
      if (r - 1 >= 0) PAWNFROM[0][s] |= bit((r - 1) * W + f + df);  // a white pawn there attacks s
      if (r + 1 < H) PAWNFROM[1][s] |= bit((r + 1) * W + f + df);   // a black pawn there attacks s
    }
  }
}

static inline u64 rayAtt(int sq, int d, u64 occ) {
  u64 r = RAYM[d][sq], b = r & occ;
  if (!b) return r;
  int bs = dpos(d) ? __builtin_ctzll(b) : 63 - __builtin_clzll(b);
  return r ^ RAYM[d][bs];
}
static inline u64 slideAtt(int sq, u64 occ, int lo, int hi) {
  u64 a = 0;
  for (int d = lo; d < hi; d++) a |= rayAtt(sq, d, occ);
  return a;
}
// officer code = 4 * colour + type, type 0..3 = Q R B N
static inline u64 offAtt(int code, int sq, u64 occ) {
  int t = code & 3;
  if (t == 3) return KNIGHTM[sq];
  return slideAtt(sq, occ, t == 2 ? 4 : 0, t == 1 ? 4 : 8);
}

// ---------------- positions ----------------
struct Pos {
  u64 wp, bp;
  int wk, bk, no, stm;
  int osq[2], oc[2];
};
struct Key {
  u64 wp, bp;
  int no, oc[2];
  bool operator==(const Key& o) const {
    if (wp != o.wp || bp != o.bp || no != o.no) return false;
    for (int j = 0; j < no; j++)
      if (oc[j] != o.oc[j]) return false;
    return true;
  }
};
static inline void canon(Pos& p) {
  if (p.no == 2) {
    bool sw = p.oc[0] > p.oc[1] || (p.oc[0] == p.oc[1] && p.osq[0] > p.osq[1]);
    if (sw) { swap(p.oc[0], p.oc[1]); swap(p.osq[0], p.osq[1]); }
  }
}
static inline Key keyOf(const Pos& p) {
  Key k; k.wp = p.wp; k.bp = p.bp; k.no = p.no; k.oc[0] = p.no > 0 ? p.oc[0] : 0; k.oc[1] = p.no > 1 ? p.oc[1] : 0;
  return k;
}
static inline void canonKey(Key& k) {
  if (k.no == 2 && k.oc[0] > k.oc[1]) swap(k.oc[0], k.oc[1]);
}
static inline u64 occOf(const Pos& p) {
  u64 o = p.wp | p.bp | bit(p.wk) | bit(p.bk);
  for (int j = 0; j < p.no; j++) o |= bit(p.osq[j]);
  return o;
}
static inline size_t posIdx(const Pos& p) {
  size_t i = (size_t)p.stm;
  i = i * N + p.wk;
  i = i * N + p.bk;
  for (int j = 0; j < p.no; j++) i = i * N + p.osq[j];
  return i;
}
static inline size_t layerSize(int no) {
  size_t n = 2;
  for (int i = 0; i < 2 + no; i++) n *= (size_t)N;
  return n;
}
static inline void decode(const Key& k, size_t idx, Pos& p) {
  p.wp = k.wp; p.bp = k.bp; p.no = k.no;
  for (int j = k.no - 1; j >= 0; j--) { p.osq[j] = (int)(idx % N); idx /= N; p.oc[j] = k.oc[j]; }
  if (k.no < 2) { p.osq[1] = 0; p.oc[1] = 0; }
  if (k.no < 1) { p.osq[0] = 0; p.oc[0] = 0; }
  p.bk = (int)(idx % N); idx /= N;
  p.wk = (int)(idx % N); idx /= N;
  p.stm = (int)idx;
}
// is square sq attacked by colour `by`? (occ includes everything)
static inline bool attacked(const Pos& p, int sq, int by, u64 occ) {
  int k = by ? p.bk : p.wk;
  if ((KINGM[k] >> sq) & 1) return true;
  if ((by ? p.bp : p.wp) & PAWNFROM[by][sq]) return true;
  for (int j = 0; j < p.no; j++)
    if ((p.oc[j] >> 2) == by && p.osq[j] != sq && ((offAtt(p.oc[j], p.osq[j], occ) >> sq) & 1)) return true;
  return false;
}
static inline bool inCheck(const Pos& p, int side) { return attacked(p, side ? p.bk : p.wk, 1 - side, occOf(p)); }
static bool legalState(const Pos& p) {
  u64 seen = p.wp | p.bp;
  if (p.wp & p.bp) return false;
  if (((seen >> p.wk) & 1) || ((seen >> p.bk) & 1) || p.wk == p.bk) return false;
  seen |= bit(p.wk) | bit(p.bk);
  for (int j = 0; j < p.no; j++) {
    if ((seen >> p.osq[j]) & 1) return false;
    seen |= bit(p.osq[j]);
  }
  if (p.no == 2 && p.oc[0] == p.oc[1] && p.osq[0] > p.osq[1]) return false;
  if ((KINGM[p.wk] >> p.bk) & 1) return false;
  return !inCheck(p, 1 - p.stm);
}
static void removeOfficerAt(Pos& q, int sq) {
  for (int j = 0; j < q.no; j++)
    if (q.osq[j] == sq) {
      for (int i = j; i + 1 < q.no; i++) { q.osq[i] = q.osq[i + 1]; q.oc[i] = q.oc[i + 1]; }
      q.no--;
      return;
    }
}

// ---------------- move generation ----------------
struct MoveInfo {
  const Pos* pos;
  int kind;    // 0 normal, 1 terminal (capped promotion)
  int winner;  // for kind 1
  bool inl;    // stays in the layer
  char piece;
  int from, to, promo;
};
static inline int ownCount(const Pos& p, int c) {
  int n = 0;
  for (int j = 0; j < p.no; j++) n += (p.oc[j] >> 2) == c;
  return n;
}

template <class F>
static void genMoves(const Pos& p, F&& f) {
  const int us = p.stm, them = 1 - us;
  const u64 ownP = us ? p.bp : p.wp, oppP = us ? p.wp : p.bp;
  u64 ownO = 0, oppO = 0;
  for (int j = 0; j < p.no; j++) ((p.oc[j] >> 2) == us ? ownO : oppO) |= bit(p.osq[j]);
  const int ok = us ? p.bk : p.wk, ek = us ? p.wk : p.bk;
  const u64 occ0 = p.wp | p.bp | ownO | oppO | bit(ok) | bit(ek);
  const u64 ownAll = ownP | ownO | bit(ok);
  // king
  u64 km = KINGM[ok] & ~ownAll & ~bit(ek) & ~KINGM[ek];
  while (km) {
    int n = __builtin_ctzll(km); km &= km - 1;
    Pos q = p;
    if (us) q.bk = n; else q.wk = n;
    bool cap = false;
    if ((oppP >> n) & 1) { if (us) q.wp &= ~bit(n); else q.bp &= ~bit(n); cap = true; }
    else if ((oppO >> n) & 1) { removeOfficerAt(q, n); cap = true; }
    if (attacked(q, n, them, occOf(q))) continue;
    q.stm = them;
    MoveInfo mi{&q, 0, 0, !cap, 'K', ok, n, 0};
    f(mi);
  }
  // officers
  for (int j = 0; j < p.no; j++) {
    if ((p.oc[j] >> 2) != us) continue;
    int from = p.osq[j], code = p.oc[j];
    u64 dest = offAtt(code, from, occ0) & ~ownAll & ~bit(ek);
    while (dest) {
      int s = __builtin_ctzll(dest); dest &= dest - 1;
      Pos q = p;
      bool cap = false;
      if ((oppP >> s) & 1) { if (us) q.wp &= ~bit(s); else q.bp &= ~bit(s); cap = true; }
      else if ((oppO >> s) & 1) { removeOfficerAt(q, s); cap = true; }
      for (int i = 0; i < q.no; i++)
        if (q.osq[i] == from && (q.oc[i] >> 2) == us) { q.osq[i] = s; break; }
      canon(q);
      if (attacked(q, ok, them, occOf(q))) continue;
      q.stm = them;
      MoveInfo mi{&q, 0, 0, !cap, TCH[code & 3], from, s, 0};
      f(mi);
    }
  }
  // pawns
  const int dir = us ? -W : W, last = us ? 0 : H - 1;
  u64 pp = ownP;
  while (pp) {
    int s = __builtin_ctzll(pp); pp &= pp - 1;
    int t = s + dir, f0 = fileOf(s);
    for (int mode = -2; mode <= 1; mode++) {  // -2: push, -1/+1: capture to file f0+mode (0 skipped)
      int to, capsq = -1;
      if (mode == -2) {
        if ((occ0 >> t) & 1) continue;
        to = t;
      } else if (mode == 0) continue;
      else {
        int nf = f0 + mode;
        if (nf < 0 || nf >= W) continue;
        to = rankOf(t) * W + nf;
        if (!(((oppP | oppO) >> to) & 1)) continue;
        capsq = to;
      }
      Pos q = p;
      if (us) q.bp &= ~bit(s); else q.wp &= ~bit(s);
      if (capsq >= 0) {
        if ((oppP >> capsq) & 1) { if (us) q.wp &= ~bit(capsq); else q.bp &= ~bit(capsq); }
        else removeOfficerAt(q, capsq);
      }
      if (rankOf(to) == last) {
        Pos r = q;
        r.osq[r.no] = to; r.oc[r.no] = us * 4; r.no++;
        if (attacked(r, ok, them, occOf(r))) continue;
        for (int t2 : PROMO[us]) {
          Pos s2 = q;
          s2.osq[s2.no] = to; s2.oc[s2.no] = us * 4 + t2; s2.no++;
          canon(s2);
          s2.stm = them;
          bool capped = s2.no > TOTCAP || ownCount(s2, us) > CAPC[us];
          MoveInfo mi{&s2, capped ? 1 : 0, capped ? (BOUND == 0 ? 0 : 1) : 0, false, 'P', s, to, t2 + 1};
          f(mi);
        }
      } else {
        if (us) q.bp |= bit(to); else q.wp |= bit(to);
        if (attacked(q, ok, them, occOf(q))) continue;
        q.stm = them;
        MoveInfo mi{&q, 0, 0, false, 'P', s, to, 0};
        f(mi);
      }
    }
  }
}

// reverse in-layer moves: calls f(Pos s) for every placement s with t = s + one non-capturing king/officer move
template <class F>
static void genPreds(const Pos& t, F&& f) {
  const int mover = 1 - t.stm;
  const u64 occ = occOf(t);
  const int k = mover ? t.bk : t.wk, ek = mover ? t.wk : t.bk;
  u64 km = KINGM[k] & ~occ & ~KINGM[ek];
  while (km) {
    int n = __builtin_ctzll(km); km &= km - 1;
    Pos s = t;
    if (mover) s.bk = n; else s.wk = n;
    s.stm = mover;
    f(s);
  }
  for (int j = 0; j < t.no; j++) {
    if ((t.oc[j] >> 2) != mover) continue;
    u64 m = offAtt(t.oc[j], t.osq[j], occ) & ~occ;
    while (m) {
      int o = __builtin_ctzll(m); m &= m - 1;
      Pos s = t;
      s.osq[j] = o;
      canon(s);
      s.stm = mover;
      f(s);
    }
  }
}

// ---------------- layers ----------------
struct Layer {
  Key key;
  size_t n;
  vector<u8> pk;  // 2 bits per state
};
static inline int get2(const Layer* L, size_t i) { return (L->pk[i >> 2] >> ((i & 3) * 2)) & 3; }

static u64 keyHash(const Key& k) {
  u64 h = k.wp * 0x9E3779B97F4A7C15ULL ^ (k.bp + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL;
  h ^= (u64)(k.no + 1) * 0x165667B19E3779F9ULL;
  for (int j = 0; j < k.no; j++) h = (h ^ (u64)(k.oc[j] + 31 * j + 1)) * 0x100000001B3ULL;
  return h ^ (h >> 29);
}
static vector<Layer*> TAB;
static size_t TABN = 0;
static Layer* findLayer(const Key& k) {
  size_t m = TAB.size() - 1, i = keyHash(k) & m;
  while (TAB[i]) {
    if (TAB[i]->key == k) return TAB[i];
    i = (i + 1) & m;
  }
  return nullptr;
}
static void insertLayer(Layer* L) {
  if (2 * (TABN + 1) > TAB.size()) {
    vector<Layer*> old;
    old.swap(TAB);
    TAB.assign(old.size() * 2, nullptr);
    TABN = 0;
    for (Layer* x : old) if (x) insertLayer(x);
  }
  size_t m = TAB.size() - 1, i = keyHash(L->key) & m;
  while (TAB[i]) i = (i + 1) & m;
  TAB[i] = L;
  TABN++;
}
static void resetTables() {
  for (Layer* x : TAB) delete x;
  TAB.assign(1 << 12, nullptr);
  TABN = 0;
}

template <class F>
static void parFor(size_t n, size_t chunk, F&& fn) {
  int nt = n >= 65536 ? NT : 1;
  atomic<size_t> next{0};
  auto work = [&](int tid) {
    for (;;) {
      size_t lo = next.fetch_add(chunk);
      if (lo >= n) break;
      fn(lo, min(n, lo + chunk), tid);
    }
  };
  if (nt == 1) { work(0); return; }
  vector<thread> th;
  for (int t = 1; t < nt; t++) th.emplace_back(work, t);
  work(0);
  for (auto& x : th) x.join();
}

// value of a child position for the side to move in it: 1 win, 2 loss, 0 draw. The layer must exist.
static inline int childValue(const MoveInfo& mi) {
  if (mi.kind == 1) return mi.winner == mi.pos->stm ? 1 : 2;
  Key k = keyOf(*mi.pos);
  Layer* L = findLayer(k);
  if (!L) { fprintf(stderr, "kq: internal error: child layer missing\n"); exit(3); }
  return get2(L, posIdx(*mi.pos));
}

// over-approximate the layers reachable from a layer key by one pawn move, capture or promotion
static void childKeys(const Key& k, vector<Key>& out) {
  auto push = [&](u64 wp, u64 bp, vector<int>& offs) {
    Key q; q.wp = wp; q.bp = bp; q.no = (int)offs.size(); q.oc[0] = q.oc[1] = 0;
    for (size_t j = 0; j < offs.size(); j++) q.oc[j] = offs[j];
    canonKey(q);
    out.push_back(q);
  };
  vector<int> offs;
  for (int j = 0; j < k.no; j++) offs.push_back(k.oc[j]);
  // captures by kings and officers: any pawn, any officer
  for (int c = 0; c < 2; c++) {
    u64 pw = c ? k.bp : k.wp;
    while (pw) {
      int s = __builtin_ctzll(pw); pw &= pw - 1;
      push(c ? k.wp : k.wp & ~bit(s), c ? k.bp & ~bit(s) : k.bp, offs);
    }
  }
  for (int j = 0; j < k.no; j++) {
    vector<int> o2;
    for (int i = 0; i < k.no; i++) if (i != j) o2.push_back(k.oc[i]);
    push(k.wp, k.bp, o2);
  }
  // pawn moves and pawn captures
  for (int c = 0; c < 2; c++) {
    u64 own = c ? k.bp : k.wp, opp = c ? k.wp : k.bp;
    int dir = c ? -W : W, last = c ? 0 : H - 1;
    u64 pw = own;
    while (pw) {
      int s = __builtin_ctzll(pw); pw &= pw - 1;
      int t = s + dir;
      for (int mode = -2; mode <= 1; mode++) {
        if (mode == 0) continue;
        int to;
        bool capPawn = false;
        vector<int> capOff;  // candidate captured-officer indices
        if (mode == -2) {
          if (((k.wp | k.bp) >> t) & 1) continue;
          to = t;
        } else {
          int nf = fileOf(s) + mode;
          if (nf < 0 || nf >= W) continue;
          to = rankOf(t) * W + nf;
          if ((opp >> to) & 1) capPawn = true;
          for (int j = 0; j < k.no; j++) if ((k.oc[j] >> 2) != c) capOff.push_back(j);
          if (!capPawn && capOff.empty()) continue;
        }
        // build the variants: capture a pawn on `to`, or capture officer j, or no capture
        vector<int> variants;  // -2 none, -1 pawn, j officer
        if (mode == -2) variants.push_back(-2);
        else {
          if (capPawn) variants.push_back(-1);
          for (int j : capOff) variants.push_back(j);
        }
        for (int v : variants) {
          u64 nown = own & ~bit(s), nopp = opp;
          vector<int> o2;
          for (int j = 0; j < k.no; j++) if (j != v) o2.push_back(k.oc[j]);
          if (v == -1) nopp &= ~bit(to);
          if (rankOf(to) == last) {
            for (int t2 : PROMO[c]) {
              vector<int> o3 = o2;
              o3.push_back(c * 4 + t2);
              int tot = (int)o3.size(), mine = 0;
              for (int x : o3) mine += (x >> 2) == c;
              if (tot > TOTCAP || mine > CAPC[c]) continue;
              push(c ? nopp : nown, c ? nown : nopp, o3);
            }
          } else {
            nown |= bit(to);
            push(c ? nopp : nown, c ? nown : nopp, o2);
          }
        }
      }
    }
  }
  sort(out.begin(), out.end(), [](const Key& a, const Key& b) {
    if (a.wp != b.wp) return a.wp < b.wp;
    if (a.bp != b.bp) return a.bp < b.bp;
    if (a.no != b.no) return a.no < b.no;
    if (a.oc[0] != b.oc[0]) return a.oc[0] < b.oc[0];
    return a.oc[1] < b.oc[1];
  });
  out.erase(unique(out.begin(), out.end()), out.end());
}

static size_t nLayers = 0, nSlots = 0;
static chrono::steady_clock::time_point T0;
static double secs() { return chrono::duration<double>(chrono::steady_clock::now() - T0).count(); }

static string cacheName(const Key& k) {
  char b[256];
  snprintf(b, sizeof b, "%s/L_%llx_%llx_%d_%d_%d.bin", CACHE.c_str(), k.wp, k.bp, k.no, k.oc[0], k.oc[1]);
  return b;
}
static Layer* loadCached(const Key& k) {
  if (CACHE.empty()) return nullptr;
  FILE* f = fopen(cacheName(k).c_str(), "rb");
  if (!f) return nullptr;
  size_t n = layerSize(k.no);
  Layer* nl = new Layer;
  nl->key = k; nl->n = n; nl->pk.assign((n + 3) / 4, 0);
  u64 hdr[5];
  bool ok = fread(hdr, 8, 5, f) == 5 && hdr[0] == k.wp && hdr[1] == k.bp && hdr[2] == (u64)k.no && hdr[3] == (u64)k.oc[0] && hdr[4] == (u64)k.oc[1] &&
            fread(nl->pk.data(), 1, nl->pk.size(), f) == nl->pk.size();
  fclose(f);
  if (!ok) { delete nl; return nullptr; }
  return nl;
}
static void saveCached(const Layer* L) {
  if (CACHE.empty()) return;
  string fn = cacheName(L->key), tmp = fn + ".tmp";
  FILE* f = fopen(tmp.c_str(), "wb");
  if (!f) return;
  u64 hdr[5] = {L->key.wp, L->key.bp, (u64)L->key.no, (u64)L->key.oc[0], (u64)L->key.oc[1]};
  bool ok = fwrite(hdr, 8, 5, f) == 5 && fwrite(L->pk.data(), 1, L->pk.size(), f) == L->pk.size();
  ok = (fclose(f) == 0) && ok;
  if (ok) rename(tmp.c_str(), fn.c_str()); else remove(tmp.c_str());
}

static Layer* getLayer(const Key& k) {
  Layer* L = findLayer(k);
  if (L) return L;
  if ((L = loadCached(k))) { insertLayer(L); nLayers++; nSlots += L->n; return L; }
  vector<Key> ck;
  childKeys(k, ck);
  for (const Key& c : ck)
    if (!(c == k)) getLayer(c);
  // pawn sets that cannot occur at all (a pawn on its own last rank or a second-rank pawn) are rejected
  if (!QUIET && k.no == 2) fprintf(stderr, "[%.0fs] layer wp=%llx bp=%llx off=%d,%d\n", secs(), k.wp, k.bp, k.oc[0], k.oc[1]);
  size_t n = layerSize(k.no);
  vector<u8> val(n, 0), cnt(n, 0);
  // forward pass
  parFor(n, 4096, [&](size_t lo, size_t hi, int) {
    Pos p;
    for (size_t idx = lo; idx < hi; idx++) {
      decode(k, idx, p);
      if (!legalState(p)) { val[idx] = 3; continue; }
      int m = 0, c = 0;
      bool win = false, draw = false;
      genMoves(p, [&](const MoveInfo& mi) {
        m++;
        if (win) return;
        if (mi.inl) { c++; return; }
        int v = childValue(mi);
        if (v == 2) win = true;
        else if (v == 0) draw = true;
      });
      if (m == 0) { val[idx] = inCheck(p, p.stm) ? 2 : 0; continue; }
      if (win) val[idx] = 1;
      else if (c == 0 && !draw) val[idx] = 2;
      else cnt[idx] = (u8)(c + (draw ? 1 : 0));
    }
  });
  // backward pass
  vector<u32> cur;
  for (size_t i = 0; i < n; i++)
    if (val[i] == 1 || val[i] == 2) cur.push_back((u32)i);
  while (!cur.empty()) {
    vector<vector<u32>> nxt((size_t)NT);
    parFor(cur.size(), 2048, [&](size_t lo, size_t hi, int tid) {
      Pos t;
      for (size_t i = lo; i < hi; i++) {
        u32 ti = cur[i];
        decode(k, ti, t);
        int v = val[ti];
        genPreds(t, [&](Pos& s) {
          size_t si = posIdx(s);
          if (__atomic_load_n(&val[si], __ATOMIC_RELAXED) != 0) return;
          if (v == 2) {
            u8 e = 0;
            if (__atomic_compare_exchange_n(&val[si], &e, (u8)1, false, __ATOMIC_RELAXED, __ATOMIC_RELAXED)) nxt[(size_t)tid].push_back((u32)si);
          } else {
            if (__atomic_fetch_sub(&cnt[si], (u8)1, __ATOMIC_RELAXED) == 1) {
              u8 e = 0;
              if (__atomic_compare_exchange_n(&val[si], &e, (u8)2, false, __ATOMIC_RELAXED, __ATOMIC_RELAXED)) nxt[(size_t)tid].push_back((u32)si);
            }
          }
        });
      }
    });
    cur.clear();
    for (auto& v : nxt) cur.insert(cur.end(), v.begin(), v.end());
  }
  Layer* nl = new Layer;
  nl->key = k;
  nl->n = n;
  nl->pk.assign((n + 3) / 4, 0);
  for (size_t i = 0; i < n; i++) nl->pk[i >> 2] |= (u8)(val[i] << ((i & 3) * 2));
  insertLayer(nl);
  nLayers++;
  nSlots += n;
  saveCached(nl);
  return nl;
}

// ---------------- input / output ----------------
static int parseSquare(const char* s, int* sq) {
  if (s[0] < 'a' || s[0] >= 'a' + W) return 0;
  char* end;
  long r = strtol(s + 1, &end, 10);
  if (end == s + 1 || *end || r < 1 || r > H) return 0;
  *sq = (int)(r - 1) * W + (s[0] - 'a');
  return 1;
}
static string sqName(int s) { string r; r += (char)('a' + fileOf(s)); r += to_string(rankOf(s) + 1); return r; }

static int parsePos(const char* line, Pos* p) {
  char buf[512];
  snprintf(buf, sizeof buf, "%s", line);
  memset(p, 0, sizeof *p);
  p->wk = p->bk = -1;
  p->stm = -1;
  int nwk = 0, nbk = 0, epSeen = 0;
  for (char* t = strtok(buf, " \t\r\n"); t; t = strtok(NULL, " \t\r\n")) {
    if (p->stm < 0 && (!strcmp(t, "w") || !strcmp(t, "b"))) { p->stm = t[0] == 'b'; continue; }
    if (p->stm >= 0 && !epSeen) { epSeen = 1; if (strcmp(t, "-")) return 0; continue; }
    int s;
    if (!parseSquare(t + 1, &s)) return 0;
    char c = t[0];
    int colour = isupper((unsigned char)c) ? 0 : 1, r = rankOf(s);
    switch (toupper((unsigned char)c)) {
      case 'K': if (colour == 0) { p->wk = s; nwk++; } else { p->bk = s; nbk++; } break;
      case 'P':
        if (r == 0 || r == H - 1) return 0;
        if (r == (colour == 0 ? 1 : H - 2)) { fprintf(stderr, "kq: pawn on its second rank (double step not implemented): %s\n", line); exit(4); }
        if (colour == 0) p->wp |= bit(s); else p->bp |= bit(s);
        break;
      case 'Q': case 'R': case 'B': case 'N': {
        if (p->no >= 2) return 0;
        const char* q = strchr(TCH, toupper((unsigned char)c));
        p->osq[p->no] = s; p->oc[p->no] = (int)(q - TCH) + 4 * colour; p->no++;
        break;
      }
      default: return 0;
    }
  }
  if (nwk != 1 || nbk != 1 || p->stm < 0 || !epSeen) return 0;
  canon(*p);
  return legalState(*p);
}
static char wpov(int v, int stm) {
  if (v == 0) return 'D';
  if (v == 3) return 'X';
  return (v == 1) == (stm == 0) ? 'W' : 'L';
}
static string moveText(const MoveInfo& mi) {
  string s;
  s += mi.piece;
  s += sqName(mi.from) + sqName(mi.to);
  if (mi.promo) { s += '='; s += TCH[mi.promo - 1]; }
  return s;
}

int main(int argc, char** argv) {
  string bounds = "A", promw = "QRBN", promb = "QRBN";
  for (int i = 1; i < argc; i++) {
    string a = argv[i];
    auto nx = [&]() -> const char* { if (i + 1 >= argc) { fprintf(stderr, "kq: missing value for %s\n", a.c_str()); exit(2); } return argv[++i]; };
    if (a == "--board") { char kind[8]; if (sscanf(nx(), "%7[a-z]:%dx%d", kind, &W, &H) != 3 || strcmp(kind, "flat")) { fprintf(stderr, "kq: only flat boards\n"); return 2; } }
    else if (a == "--cap") TOTCAP = atoi(nx());
    else if (a == "--capw") CAPC[0] = atoi(nx());
    else if (a == "--capb") CAPC[1] = atoi(nx());
    else if (a == "--promw") promw = nx();
    else if (a == "--promb") promb = nx();
    else if (a == "--bound") bounds = nx();
    else if (a == "--threads") NT = atoi(nx());
    else if (a == "--cache") CACHE = nx();
    else if (a == "--moves") WANTMOVES = 1;
    else if (a == "--quiet") QUIET = 1;
    else { fprintf(stderr, "usage: kq [--board flat:7x6] [--cap C] [--capw X] [--capb Y] [--promw QRBN] [--promb QRBN] [--bound A|B|AB] [--threads T] [--moves] [--quiet]\n"); return 2; }
  }
  if (W < 2 || W > 8 || H < 4 || H > 8 || TOTCAP < 0 || TOTCAP > 2 || NT < 1) { fprintf(stderr, "kq: bad parameters (cap must be 0..2)\n"); return 2; }
  for (char c : promw) { const char* q = strchr(TCH, toupper((unsigned char)c)); if (!q) return 2; PROMO[0].push_back((int)(q - TCH)); }
  for (char c : promb) { const char* q = strchr(TCH, toupper((unsigned char)c)); if (!q) return 2; PROMO[1].push_back((int)(q - TCH)); }
  initGeom();
  vector<string> lines;
  vector<Pos> ps;
  vector<int> ok;
  char buf[1024];
  while (fgets(buf, sizeof buf, stdin)) {
    string s = buf;
    while (!s.empty() && (s.back() == '\n' || s.back() == '\r')) s.pop_back();
    lines.push_back(s);
    size_t q = s.find_first_not_of(' ');
    Pos p;
    if (q == string::npos || s[q] == '#') { ok.push_back(-1); ps.push_back(p); }
    else { int r = parsePos(s.c_str(), &p); ok.push_back(r); ps.push_back(p); }
  }
  size_t n = lines.size();
  vector<string> res[2], mv[2];
  for (int b = 0; b < 2; b++) { res[b].assign(n, ""); mv[b].assign(n, ""); }
  T0 = chrono::steady_clock::now();
  int nb = bounds == "AB" ? 2 : 1;
  for (int bi = 0; bi < nb; bi++) {
    int bound = bounds == "AB" ? bi : (bounds == "B" ? 1 : 0);
    BOUND = bound;
    resetTables();
    nLayers = nSlots = 0;
    for (size_t i = 0; i < n; i++) {
      if (ok[i] < 0) continue;
      if (!ok[i]) { res[bi][i] = "X"; continue; }
      const Pos& p = ps[i];
      Key k = keyOf(p);
      Layer* L = getLayer(k);
      res[bi][i] = string(1, wpov(get2(L, posIdx(p)), p.stm));
      if (WANTMOVES) {
        string s;
        genMoves(p, [&](const MoveInfo& mi) {
          Key ck;
          int v;
          if (mi.kind == 1) v = mi.winner == mi.pos->stm ? 1 : 2;
          else { ck = keyOf(*mi.pos); Layer* CL = getLayer(ck); v = get2(CL, posIdx(*mi.pos)); }
          if (!s.empty()) s += " ";
          s += moveText(mi) + ":" + wpov(v, mi.pos->stm);
        });
        mv[bi][i] = s;
      }
    }
    if (!QUIET) fprintf(stderr, "[kq bound %c cap=%d capw=%d capb=%d promw=%s promb=%s: %zu layers, %zu slots, %.1fs]\n", bound ? 'B' : 'A', TOTCAP, CAPC[0], CAPC[1], promw.c_str(), promb.c_str(), nLayers, nSlots, secs());
  }
  for (size_t i = 0; i < n; i++) {
    if (ok[i] < 0) { printf("%s\n", lines[i].c_str()); continue; }
    printf("%s | %s", lines[i].c_str(), res[0][i].c_str());
    if (nb == 2) printf(" %s", res[1][i].c_str());
    if (WANTMOVES) { printf(" | %s", mv[0][i].c_str()); if (nb == 2) printf(" | B: %s", mv[1][i].c_str()); }
    printf("\n");
  }
  return 0;
}
