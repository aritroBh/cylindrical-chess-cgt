// rf39.cpp -- K39 referee's own chess solver, written from kings/SPEC.md only (no code read from kpsolve.c, kp39.c,
// own39.cpp, own2.cpp, ownref.cpp or kq3.cpp). Kings + pawns + up to 3 officers (cap and per-colour caps), flat or
// cylinder, double step and en passant, per-colour promotion sets, bound A or B, optional capture refinement.
// Design: lazy recursive layers keyed by (white pawns, black pawns, sorted officer codes); en-passant positions are not
// stored but evaluated on the fly from their moves. A layer is solved by counting retrograde analysis whose predecessors
// are found by un-moving a king or officer of the side that just moved (non-capturing moves are reversible).
// Values per state, from the side to move: 0 draw, 1 win, 2 loss, 3 illegal; stored 2 bits per state.
// Refinement (--refine): a capped promotion by the side the bound favours (A: White, B: Black) is scored as the
// opponent's best legal capture of the new piece (value of the position after it); no such capture: the mover wins.
// Usage: rf39 W H CYL BOUND(A|B) CAP CAPW CAPB PROMW PROMB REFINE(0|1) < positions
//   output: "<pos> | v | mv:v ..." with v from White's view (W/D/L/X).
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <iostream>
#include <sstream>
using namespace std;
typedef unsigned long long u64;

static int W, H, N, CYL, BOUNDA, CAP, CAPC[2], REFINE;
static bool PROM[2][4];
static const char *TY = "QRBN";

static inline int F(int s) { return s % W; }
static inline int R(int s) { return s / W; }
static inline int sq(int x, int y) {
  if (y < 0 || y >= H) return -1;
  if (CYL) { x %= W; if (x < 0) x += W; } else if (x < 0 || x >= W) return -1;
  return y * W + x;
}
static const int KX[8] = {1, 1, 0, -1, -1, -1, 0, 1}, KY[8] = {0, 1, 1, 1, 0, -1, -1, -1};
static const int NX[8] = {1, 2, 2, 1, -1, -2, -2, -1}, NY[8] = {2, 1, -1, -2, -2, -1, 1, 2};
// slider directions: 0..3 orthogonal, 4..7 diagonal
static const int DX[8] = {1, -1, 0, 0, 1, 1, -1, -1}, DY[8] = {0, 0, 1, -1, 1, -1, 1, -1};

struct Pos {
  int k[2];          // king squares, 0 white 1 black
  u64 p[2];          // pawn bitboards
  int no;            // officers
  int ot[4], oc[4], os[4];  // type 0..3 (QRBN), colour, square
  int stm, ep;
};
static inline u64 occ(const Pos& P) {
  u64 o = P.p[0] | P.p[1] | (1ULL << P.k[0]) | (1ULL << P.k[1]);
  for (int i = 0; i < P.no; i++) o |= 1ULL << P.os[i];
  return o;
}
static bool kingNear(int a, int b) {
  for (int d = 0; d < 8; d++) if (sq(F(a) + KX[d], R(a) + KY[d]) == b) return true;
  return false;
}
// squares an officer of type t on o reaches (moves or attacks) given occupancy; dedup
static int targets(int t, int o, u64 oc, int* out) {
  int n = 0;
  auto add = [&](int q) { for (int i = 0; i < n; i++) if (out[i] == q) return; out[n++] = q; };
  if (t == 3) { for (int d = 0; d < 8; d++) { int q = sq(F(o) + NX[d], R(o) + NY[d]); if (q >= 0) add(q); } return n; }
  int lo = (t == 2) ? 4 : 0, hi = (t == 1) ? 4 : 8;
  for (int d = lo; d < hi; d++) {
    int x = F(o), y = R(o);
    for (;;) {
      x += DX[d]; y += DY[d];
      int q = sq(x, y);
      if (q < 0 || q == o) break;
      add(q);
      if (oc >> q & 1) break;
    }
  }
  return n;
}
static bool attacked(const Pos& P, int s, int c) {  // is square s attacked by colour c
  // pawns
  int py = (c == 0) ? R(s) - 1 : R(s) + 1;
  for (int dx = -1; dx <= 1; dx += 2) { int q = sq(F(s) + dx, py); if (q >= 0 && (P.p[c] >> q & 1)) return true; }
  if (kingNear(P.k[c], s)) return true;
  u64 oc = occ(P);
  int buf[64];
  for (int i = 0; i < P.no; i++) if (P.oc[i] == c) {
    int n = targets(P.ot[i], P.os[i], oc, buf);
    for (int j = 0; j < n; j++) if (buf[j] == s) return true;
  }
  return false;
}
static bool legal(const Pos& P) {
  u64 seen = 0;
  auto put = [&](int s) { if (s < 0 || s >= N || (seen >> s & 1)) return false; seen |= 1ULL << s; return true; };
  if (!put(P.k[0]) || !put(P.k[1])) return false;
  for (int i = 0; i < P.no; i++) if (!put(P.os[i])) return false;
  if (P.p[0] & P.p[1]) return false;
  if ((P.p[0] | P.p[1]) & seen) return false;
  u64 r1 = 0, rH = 0;
  for (int x = 0; x < W; x++) { r1 |= 1ULL << x; rH |= 1ULL << ((H - 1) * W + x); }
  if ((P.p[0] | P.p[1]) & (r1 | rH)) return false;
  if (kingNear(P.k[0], P.k[1])) return false;
  if (attacked(P, P.k[1 - P.stm], P.stm)) return false;
  return true;
}

// ---- layers ----
struct Key { u64 a, b; int codes; bool operator==(const Key& o) const { return a == o.a && b == o.b && codes == o.codes; } };
struct KH { size_t operator()(const Key& k) const { return k.a * 0x9E3779B97F4A7C15ULL ^ (k.b + 0x632BE59BD9B4E019ULL) * 31 ^ k.codes; } };
static inline int code(int t, int c) { return t + 4 * c; }
// canonical order: officers sorted by code (stable for equal codes)
static void canon(Pos& P) {
  for (int i = 1; i < P.no; i++) for (int j = i; j > 0 && code(P.ot[j - 1], P.oc[j - 1]) > code(P.ot[j], P.oc[j]); j--) {
    swap(P.ot[j], P.ot[j - 1]); swap(P.oc[j], P.oc[j - 1]); swap(P.os[j], P.os[j - 1]);
  }
}
static Key keyOf(const Pos& P) {
  int cd = P.no;
  for (int i = 0; i < P.no; i++) cd = cd * 8 + code(P.ot[i], P.oc[i]);
  return Key{P.p[0], P.p[1], cd};
}
static u64 lsize(int no) { u64 s = 2ULL * N * N; for (int i = 0; i < no; i++) s *= N; return s; }
static u64 idxOf(const Pos& P) {
  u64 x = 0;
  for (int i = P.no - 1; i >= 0; i--) x = x * N + P.os[i];
  x = (x * N + P.k[1]) * N + P.k[0];
  return x * 2 + P.stm;
}
static void decode(u64 x, Pos& P) {  // P has pawns and officer types set
  P.stm = x & 1; x >>= 1;
  P.k[0] = x % N; x /= N; P.k[1] = x % N; x /= N;
  for (int i = 0; i < P.no; i++) { P.os[i] = x % N; x /= N; }
  P.ep = -1;
}
static unordered_map<Key, vector<uint8_t>, KH> STORE;
static u64 nStates = 0, nLayers = 0;
static inline int getv(const vector<uint8_t>& v, u64 i) { return (v[i >> 2] >> ((i & 3) * 2)) & 3; }
static inline void setv(vector<uint8_t>& v, u64 i, int x) { v[i >> 2] = (v[i >> 2] & ~(3 << ((i & 3) * 2))) | (x << ((i & 3) * 2)); }

// ---- moves ----
struct Mv { Pos c; bool inl; bool capped; int psq; char name[16]; };
static void sqname(int s, char* b) { b[0] = 'a' + F(s); b[1] = '1' + R(s); b[2] = 0; }
static void removeAt(Pos& P, int s) {  // remove enemy piece (pawn or officer) at s
  P.p[0] &= ~(1ULL << s); P.p[1] &= ~(1ULL << s);
  for (int i = 0; i < P.no; i++) if (P.os[i] == s) {
    for (int j = i; j + 1 < P.no; j++) { P.ot[j] = P.ot[j + 1]; P.oc[j] = P.oc[j + 1]; P.os[j] = P.os[j + 1]; }
    P.no--; return;
  }
}
static int countC(const Pos& P, int c) { int n = 0; for (int i = 0; i < P.no; i++) n += P.oc[i] == c; return n; }
static void gen(const Pos& P, vector<Mv>& out) {
  out.clear();
  int c = P.stm, e = 1 - c;
  u64 oc = occ(P), own = P.p[c] | (1ULL << P.k[c]), enemy = P.p[e] | (1ULL << P.k[e]);
  for (int i = 0; i < P.no; i++) (P.oc[i] == c ? own : enemy) |= 1ULL << P.os[i];
  auto finish = [&](Mv& m) {
    m.c.stm = e;
    if (attacked(m.c, m.c.k[c], e)) return;
    out.push_back(m);
  };
  char a[4], b[4];
  // king
  for (int d = 0; d < 8; d++) {
    int t = sq(F(P.k[c]) + KX[d], R(P.k[c]) + KY[d]);
    if (t < 0 || (own >> t & 1) || t == P.k[e]) continue;
    Mv m; m.c = P; m.c.ep = -1; m.capped = false;
    bool cap = enemy >> t & 1;
    if (cap) removeAt(m.c, t);
    m.c.k[c] = t; m.inl = !cap && P.ep < 0;
    sqname(P.k[c], a); sqname(t, b); snprintf(m.name, 16, "K%s%s", a, b);
    finish(m);
  }
  // officers
  int buf[64];
  for (int i = 0; i < P.no; i++) if (P.oc[i] == c) {
    int n = targets(P.ot[i], P.os[i], oc, buf);
    for (int j = 0; j < n; j++) {
      int t = buf[j];
      if ((own >> t & 1) || t == P.k[e]) continue;
      Mv m; m.c = P; m.c.ep = -1; m.capped = false;
      bool cap = enemy >> t & 1;
      int from = P.os[i];
      m.c.os[i] = t;
      m.inl = !cap && P.ep < 0;
      sqname(from, a); sqname(t, b); snprintf(m.name, 16, "%c%s%s", TY[P.ot[i]], a, b);
      if (cap) {  // rebuild: remove enemy officer/pawn at t, keep ours
        m.c = P; m.c.ep = -1;
        // remove enemy first
        Pos q = P; q.ep = -1;
        q.p[e] &= ~(1ULL << t);
        int moved_t = P.ot[i];
        // rebuild officer list
        Pos r = q; r.no = 0;
        for (int k2 = 0; k2 < P.no; k2++) {
          if (k2 == i) { r.ot[r.no] = moved_t; r.oc[r.no] = c; r.os[r.no] = t; r.no++; }
          else if (P.os[k2] == t) continue;  // captured enemy officer
          else { r.ot[r.no] = P.ot[k2]; r.oc[r.no] = P.oc[k2]; r.os[r.no] = P.os[k2]; r.no++; }
        }
        canon(r); m.c = r;
      }
      finish(m);
    }
  }
  // pawns
  int dy = (c == 0) ? 1 : -1, last = (c == 0) ? H - 1 : 0, second = (c == 0) ? 1 : H - 2;
  for (int s = 0; s < N; s++) if (P.p[c] >> s & 1) {
    auto push = [&](int t, bool capt, int epcap, int epset) {
      sqname(s, a); sqname(t, b);
      if (R(t) == last) {
        for (int ty = 0; ty < 4; ty++) if (PROM[c][ty]) {
          Mv m; m.c = P; m.c.ep = -1; m.inl = false;
          m.c.p[c] &= ~(1ULL << s);
          Pos r = m.c;
          if (capt) { r.p[e] &= ~(1ULL << t); Pos q = r; q.no = 0;
            for (int k2 = 0; k2 < r.no; k2++) if (r.os[k2] != t) { q.ot[q.no] = r.ot[k2]; q.oc[q.no] = r.oc[k2]; q.os[q.no] = r.os[k2]; q.no++; }
            r = q; }
          r.ot[r.no] = ty; r.oc[r.no] = c; r.os[r.no] = t; r.no++;
          canon(r);
          m.c = r; m.psq = t;
          m.capped = (r.no > CAP) || (countC(r, c) > CAPC[c]);
          snprintf(m.name, 16, "P%s%s=%c", a, b, TY[ty]);
          finish(m);
        }
        return;
      }
      Mv m; m.c = P; m.c.ep = epset; m.inl = false; m.capped = false;
      m.c.p[c] &= ~(1ULL << s); m.c.p[c] |= 1ULL << t;
      if (capt) {
        Pos r = m.c; r.p[e] &= ~(1ULL << t); Pos q = r; q.no = 0;
        for (int k2 = 0; k2 < r.no; k2++) if (r.os[k2] != t) { q.ot[q.no] = r.ot[k2]; q.oc[q.no] = r.oc[k2]; q.os[q.no] = r.os[k2]; q.no++; }
        m.c = q;
      }
      if (epcap >= 0) m.c.p[e] &= ~(1ULL << epcap);
      snprintf(m.name, 16, "P%s%s", a, b);
      finish(m);
    };
    int t1 = sq(F(s), R(s) + dy);
    if (t1 >= 0 && !(oc >> t1 & 1)) {
      push(t1, false, -1, -1);
      if (R(s) == second) {
        int t2 = sq(F(s), R(s) + 2 * dy);
        if (t2 >= 0 && !(oc >> t2 & 1)) {
          if (R(t2) == last) push(t2, false, -1, -1);
          else push(t2, false, -1, t1);
        }
      }
    }
    for (int dx = -1; dx <= 1; dx += 2) {
      int t = sq(F(s) + dx, R(s) + dy);
      if (t < 0) continue;
      bool enemyNonKing = (P.p[e] >> t & 1);
      for (int i = 0; i < P.no; i++) if (P.oc[i] == e && P.os[i] == t) enemyNonKing = true;
      if (enemyNonKing) push(t, true, -1, -1);
      else if (t == P.ep && !(oc >> t & 1)) {
        int victim = sq(F(t), R(t) - dy);
        if (victim >= 0 && (P.p[e] >> victim & 1)) push(t, false, victim, -1);
      }
    }
  }
}

static int valueOf(const Pos& Q);  // value of a legal position from its side to move (0 D, 1 W, 2 L)
static int moveVal(const Pos& P, const Mv& m) {  // value of move m for the mover P.stm
  int c = P.stm;
  if (m.capped) {
    bool favoured = (BOUNDA && c == 0) || (!BOUNDA && c == 1);
    if (!favoured) return 2;
    if (!REFINE) return 1;
    vector<Mv> rs; gen(m.c, rs);
    int best = 1; bool any = false;  // from mover c's view; opponent picks the worst for c
    for (auto& r : rs) {
      // capture of the new piece: the moved piece lands on psq
      bool hits = false;
      if (r.c.no < m.c.no) {  // an officer disappeared and the capturer (colour 1-c) now stands on psq
        bool still = false; for (int i = 0; i < r.c.no; i++) if (r.c.os[i] == m.psq && r.c.oc[i] == 1 - c) still = true;
        if (r.c.k[1 - c] == m.psq || (r.c.p[1 - c] >> m.psq & 1) || still) hits = true;
      }
      if (!hits) continue;
      any = true;
      int v = valueOf(r.c);  // r.c.stm == c
      int vc = v;  // already from c's view
      auto rank = [](int x) { return x == 2 ? 0 : (x == 0 ? 1 : 2); };
      if (rank(vc) < rank(best)) best = vc;
    }
    (void)any;
    return best;
  }
  int v = valueOf(m.c);
  return v == 1 ? 2 : (v == 2 ? 1 : 0);
}
static void solveLayer(const Key& K, const Pos& tmpl);
static int valueOf(const Pos& Q) {
  if (Q.ep >= 0) {
    vector<Mv> ms; gen(Q, ms);
    if (ms.empty()) return attacked(Q, Q.k[Q.stm], 1 - Q.stm) ? 2 : 0;
    bool allL = true;
    for (auto& m : ms) { int v = moveVal(Q, m); if (v == 1) return 1; if (v != 2) allL = false; }
    return allL ? 2 : 0;
  }
  Key K = keyOf(Q);
  auto it = STORE.find(K);
  if (it == STORE.end()) { solveLayer(K, Q); it = STORE.find(K); }
  int v = getv(it->second, idxOf(Q));
  if (v == 3) { fprintf(stderr, "lookup of illegal state\n"); exit(3); }
  return v;
}

static void solveLayer(const Key& K, const Pos& tmpl) {
  u64 S = lsize(tmpl.no);
  vector<uint8_t> val(S, 3), cnt(S, 0), nodraw(S, 1);
  vector<u64> q; q.reserve(1 << 16);
  vector<Mv> ms;
  Pos P = tmpl;
  for (u64 x = 0; x < S; x++) {
    decode(x, P);
    if (!legal(P)) continue;
    gen(P, ms);
    if (ms.empty()) { val[x] = attacked(P, P.k[P.stm], 1 - P.stm) ? 2 : 0; if (val[x]) q.push_back(x); continue; }
    int c = 0; bool win = false, draw = false;
    for (auto& m : ms) {
      if (m.inl) { c++; continue; }
      int v = moveVal(P, m);
      if (v == 1) { win = true; break; }
      if (v == 0) draw = true;
    }
    if (win) { val[x] = 1; q.push_back(x); continue; }
    val[x] = 0; cnt[x] = c; nodraw[x] = !draw;
    if (c == 0 && !draw) { val[x] = 2; q.push_back(x); }
  }
  // mark undecided: value 0 with cnt>0 (or with a draw exit). Use a separate decided flag.
  vector<uint8_t> dec(S, 0);
  for (u64 x : q) dec[x] = 1;
  for (size_t h = 0; h < q.size(); h++) {
    u64 x = q[h];
    decode(x, P);
    int v = val[x];  // for P.stm
    int mover = 1 - P.stm;  // the side that moved into P
    // un-move each king/officer of 'mover' to an empty square
    u64 oc = occ(P);
    auto tryPred = [&](Pos& Sp) {
      Sp.stm = mover;
      if (!legal(Sp)) return;
      u64 y = idxOf(Sp);
      if (dec[y] || val[y] == 3) return;
      if (v == 2) { val[y] = 1; dec[y] = 1; q.push_back(y); }
      else if (v == 1) {
        if (--cnt[y] == 0 && nodraw[y]) { val[y] = 2; dec[y] = 1; q.push_back(y); }
      }
    };
    if (v == 0) continue;
    // king of mover
    int kt = P.k[mover];
    for (int d = 0; d < 8; d++) {
      int s = sq(F(kt) + KX[d], R(kt) + KY[d]);
      if (s < 0 || (oc >> s & 1)) continue;
      Pos Sp = P; Sp.k[mover] = s; tryPred(Sp);
    }
    int buf[64], buf2[64];
    for (int i = 0; i < P.no; i++) if (P.oc[i] == mover) {
      int t = P.os[i];
      int n = targets(P.ot[i], t, oc, buf);
      for (int j = 0; j < n; j++) {
        int s = buf[j];
        if (oc >> s & 1) continue;
        Pos Sp = P; Sp.os[i] = s;
        // verify forward s -> t in Sp
        int n2 = targets(P.ot[i], s, occ(Sp), buf2); bool ok = false;
        for (int k2 = 0; k2 < n2; k2++) if (buf2[k2] == t) ok = true;
        if (!ok) continue;
        tryPred(Sp);
      }
    }
  }
  vector<uint8_t> packed((S + 3) / 4, 0);
  for (u64 x = 0; x < S; x++) setv(packed, x, val[x]);
  STORE[K] = std::move(packed);
  nLayers++; nStates += S;
}

static bool parse(const string& line, Pos& P) {
  istringstream is(line); string tok; vector<string> t;
  while (is >> tok) t.push_back(tok);
  if (t.size() < 2) return false;
  P.no = 0; P.p[0] = P.p[1] = 0; P.k[0] = P.k[1] = -1;
  size_t n = t.size();
  for (size_t i = 0; i + 2 < n; i++) {
    string& s = t[i]; char ch = s[0]; int x = s[1] - 'a', y = atoi(s.c_str() + 2) - 1; int q = y * W + x;
    int col = isupper(ch) ? 0 : 1; char u = toupper(ch);
    if (u == 'K') P.k[col] = q; else if (u == 'P') P.p[col] |= 1ULL << q;
    else { int ty = strchr(TY, u) - TY; P.ot[P.no] = ty; P.oc[P.no] = col; P.os[P.no] = q; P.no++; }
  }
  P.stm = t[n - 2] == "w" ? 0 : 1;
  P.ep = t[n - 1] == "-" ? -1 : (atoi(t[n - 1].c_str() + 1) - 1) * W + (t[n - 1][0] - 'a');
  canon(P);
  return true;
}
static char wv(int v, int stm) { if (v == 0) return 'D'; bool whiteWins = (v == 1) == (stm == 0); return whiteWins ? 'W' : 'L'; }

int main(int argc, char** argv) {
  if (argc < 11) { fprintf(stderr, "usage\n"); return 1; }
  W = atoi(argv[1]); H = atoi(argv[2]); N = W * H; CYL = atoi(argv[3]); BOUNDA = argv[4][0] == 'A';
  CAP = atoi(argv[5]); CAPC[0] = atoi(argv[6]); CAPC[1] = atoi(argv[7]);
  for (int c = 0; c < 2; c++) for (int t = 0; t < 4; t++) PROM[c][t] = strchr(argv[8 + c], TY[t]) != nullptr;
  REFINE = atoi(argv[10]);
  string line;
  while (getline(cin, line)) {
    if (line.empty() || line[0] == '#') { cout << line << "\n"; continue; }
    Pos P; parse(line, P);
    if (!legal(P)) { cout << line << " | X\n"; continue; }
    int v = valueOf(P);
    cout << line << " | " << wv(v, P.stm) << " |";
    vector<Mv> ms; gen(P, ms);
    for (auto& m : ms) { int mv = moveVal(P, m); cout << " " << m.name << ":" << wv(mv, P.stm); }
    cout << "\n"; cout.flush();
  }
  fprintf(stderr, "layers %llu states %llu\n", nLayers, nStates);
  return 0;
}
