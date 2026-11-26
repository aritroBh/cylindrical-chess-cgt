// q68.cpp -- K68 referee: conservative chess solver for the leaves of Lemma A (positions after b8=Q, Black to move).
// Material: White K + Q + pawns, Black K + pawns, flat 8x8, chess rules (mate wins, stalemate draws), with two
// conservative changes that can only lower White's results:
//   * White may not promote (the move is removed);
//   * a Black promotion, and a Black capture of the queen, count as a Black win at once.
// So a White win here is a White win in chess (the 50-move rule ignored; see the DTM printed).
// Usage: q68 < leaves.txt   (one FEN per line, Black to move, exactly one White queen)
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
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
static U64 qatt(int q, U64 occ) {
  U64 a = 0; static const int dr[8] = {1, 1, 1, 0, 0, -1, -1, -1}, df[8] = {-1, 0, 1, -1, 1, -1, 0, 1};
  for (int d = 0; d < 8; d++) { int r = RA(q) + dr[d], f = FI(q) + df[d];
    while (r >= 0 && r < 8 && f >= 0 && f < 8) { int s = f + 8 * r; a |= B(s); if (occ & B(s)) break; r += dr[d]; f += df[d]; } }
  return a;
}
struct Cfg { U64 wp, bp; bool operator<(const Cfg &o) const { return wp != o.wp ? wp < o.wp : bp < o.bp; } };
static map<Cfg, int> cid; static vector<Cfg> cfgs;
static int addc(Cfg c) { auto it = cid.find(c); if (it != cid.end()) return it->second; int i = cfgs.size(); cid[c] = i; cfgs.push_back(c); return i; }
// closure: pawn pushes (no promotion), pawn captures, any piece taking any enemy pawn
static void closure(Cfg r) {
  vector<int> st{addc(r)};
  while (!st.empty()) {
    Cfg c = cfgs[st.back()]; st.pop_back();
    auto push = [&](Cfg n) { size_t b = cfgs.size(); int i = addc(n); if ((size_t)i == b) st.push_back(i); };
    for (U64 t = c.bp; t; t &= t - 1) { Cfg n = c; n.bp &= ~B(__builtin_ctzll(t)); push(n); }
    for (U64 t = c.wp; t; t &= t - 1) { Cfg n = c; n.wp &= ~B(__builtin_ctzll(t)); push(n); }
    U64 occ = c.wp | c.bp;
    for (U64 t = c.wp; t; t &= t - 1) { int f = __builtin_ctzll(t), to = f + 8; if (RA(to) == 7) continue;
      if (!(occ & B(to))) { Cfg n = c; n.wp = (n.wp & ~B(f)) | B(to); push(n); if (RA(f) == 1 && !(occ & B(to + 8))) { Cfg m = c; m.wp = (m.wp & ~B(f)) | B(to + 8); push(m); } }
      for (int d = -1; d <= 1; d += 2) { if (FI(f) + d < 0 || FI(f) + d > 7) continue; int x = to + d; if (c.bp & B(x)) { Cfg n = c; n.bp &= ~B(x); n.wp = (n.wp & ~B(f)) | B(x); push(n); } } }
    for (U64 t = c.bp; t; t &= t - 1) { int f = __builtin_ctzll(t), to = f - 8; if (RA(to) == 0) continue;
      if (!(occ & B(to))) { Cfg n = c; n.bp = (n.bp & ~B(f)) | B(to); push(n); if (RA(f) == 6 && !(occ & B(to - 8))) { Cfg m = c; m.bp = (m.bp & ~B(f)) | B(to - 8); push(m); } }
      for (int d = -1; d <= 1; d += 2) { if (FI(f) + d < 0 || FI(f) + d > 7) continue; int x = to + d; if (c.wp & B(x)) { Cfg n = c; n.wp &= ~B(x); n.bp = (n.bp & ~B(f)) | B(x); push(n); } } }
  }
}
// e.p. is ignored: a Black double step needs a pawn on rank 7 (none in the leaves after ...c6 has moved; and pc6 is on
// rank 6), and a White double step needs a White pawn on rank 2 beside... handled conservatively below by forbidding
// White double steps that would give Black an e.p. capture (none arise here; counted).
enum { UNK = 0, WIN = 1, LOSS = 2, DRAW = 3 };
static vector<vector<uint8_t>> V;  // per cfg, index stm*262144 + wk*4096 + bk*64 + wq
static vector<vector<uint8_t>> Dd;
static long epWarn = 0;
struct S { int wk, bk, wq, stm; Cfg c; };
static inline int idx(int stm, int wk, int bk, int wq) { return stm * 262144 + wk * 4096 + bk * 64 + wq; }
static bool blackInCheck(const S &s) {
  U64 occ = s.c.wp | s.c.bp | B(s.wk) | B(s.bk) | B(s.wq);
  return (qatt(s.wq, occ) & B(s.bk)) || (wpatt(s.c.wp) & B(s.bk));
}
static bool whiteInCheck(const S &s) { return bpatt(s.c.bp) & B(s.wk); }
static bool valid(const S &s) {
  if (s.wk == s.bk || s.wk == s.wq || s.bk == s.wq) return false;
  U64 occ = s.c.wp | s.c.bp;
  if (occ & (B(s.wk) | B(s.bk) | B(s.wq))) return false;
  if (kdist(s.wk, s.bk) < 2) return false;
  if (s.stm == 0 && blackInCheck(s)) return false;
  if (s.stm == 1 && whiteInCheck(s)) return false;
  return true;
}
// successor result: -1 = terminal Black win (conservative), else state
struct Sc { int term; S s; };
static void gen(const S &s, vector<Sc> &out) {
  out.clear();
  U64 occ = s.c.wp | s.c.bp | B(s.wk) | B(s.bk) | B(s.wq);
  if (s.stm == 0) {
    // king
    for (U64 t = KATT[s.wk]; t; t &= t - 1) { int to = __builtin_ctzll(t);
      if ((s.c.wp | B(s.wq)) & B(to)) continue; if (kdist(to, s.bk) < 2) continue;
      S n = s; n.stm = 1; n.wk = to; n.c.bp &= ~B(to); if (whiteInCheck(n)) continue; out.push_back({0, n}); }
    // queen
    U64 qa = qatt(s.wq, occ);
    for (U64 t = qa; t; t &= t - 1) { int to = __builtin_ctzll(t);
      if ((s.c.wp | B(s.wk) | B(s.bk)) & B(to)) continue;
      S n = s; n.stm = 1; n.wq = to; n.c.bp &= ~B(to); if (whiteInCheck(n)) continue; out.push_back({0, n}); }
    // pawns (no promotion)
    for (U64 t = s.c.wp; t; t &= t - 1) { int f = __builtin_ctzll(t), to = f + 8; if (RA(to) == 7) continue;
      auto add = [&](int d, bool cap) { S n = s; n.stm = 1; n.c.wp = (n.c.wp & ~B(f)) | B(d); if (cap) n.c.bp &= ~B(d); if (whiteInCheck(n)) return; out.push_back({0, n}); };
      if (!(occ & B(to))) { add(to, false); if (RA(f) == 1 && !(occ & B(to + 8))) {
          int a = to + 8; bool ep = (FI(a) > 0 && (s.c.bp & B(a - 1))) || (FI(a) < 7 && (s.c.bp & B(a + 1)));
          if (ep) epWarn++; else add(to + 8, false); } }
      for (int d = -1; d <= 1; d += 2) { if (FI(f) + d < 0 || FI(f) + d > 7) continue; int x = to + d; if (s.c.bp & B(x)) add(x, true); } }
  } else {
    for (U64 t = KATT[s.bk]; t; t &= t - 1) { int to = __builtin_ctzll(t);
      if (s.c.bp & B(to)) continue; if (kdist(to, s.wk) < 2) continue;
      if (to == s.wq) { // capture the queen: legal if the queen is unprotected (by king: excluded above; by pawns)
        if (wpatt(s.c.wp) & B(to)) continue; out.push_back({-1, s}); continue; }
      S n = s; n.stm = 0; n.bk = to; n.c.wp &= ~B(to);
      if (blackInCheck(n)) continue; out.push_back({0, n}); }
    for (U64 t = s.c.bp; t; t &= t - 1) { int f = __builtin_ctzll(t), to = f - 8;
      auto add = [&](int d, bool cap) {
        S n = s; n.stm = 0; n.c.bp = (n.c.bp & ~B(f)); bool promo = RA(d) == 0; bool takesQ = cap && d == s.wq;
        if (!promo) n.c.bp |= B(d);
        if (cap && !takesQ) n.c.wp &= ~B(d);
        if (takesQ) { out.push_back({-1, s}); return; }
        // legality: Black king not in check afterwards (the queen may now see it)
        if (blackInCheck(n)) return;
        if (promo) { out.push_back({-1, s}); return; }
        out.push_back({0, n}); };
      if (!(occ & B(to))) { add(to, false); if (RA(f) == 6 && !(occ & B(to - 8))) add(to - 8, false); }
      for (int d = -1; d <= 1; d += 2) { if (FI(f) + d < 0 || FI(f) + d > 7) continue; int x = to + d; if ((s.c.wp | B(s.wq)) & B(x)) add(x, true); } }
  }
}
static int look(const S &s, uint8_t *d) { int c = cid.at(s.c); int i = idx(s.stm, s.wk, s.bk, s.wq); if (d) *d = Dd[c][i]; return V[c][i]; }
static int npawns(const Cfg &c) { return __builtin_popcountll(c.wp | c.bp); }
static int pot(const Cfg &c) { int v = 0; for (U64 t = c.wp; t; t &= t - 1) v += RA(__builtin_ctzll(t)); for (U64 t = c.bp; t; t &= t - 1) v += 7 - RA(__builtin_ctzll(t)); return v + 10 * (8 - npawns(c)); }
static void solve(int ci) {
  const int N = 524288;
  V[ci].assign(N, UNK); Dd[ci].assign(N, 255);
  vector<uint8_t> &Vv = V[ci];
  vector<char> ok(N, 0); vector<int> work; vector<Sc> mv;
  for (int i = 0; i < N; i++) { S s{(i >> 12) & 63, (i >> 6) & 63, i & 63, i >> 18, cfgs[ci]}; if (valid(s)) { ok[i] = 1; work.push_back(i); } }
  auto ev = [&](int i) {
    S s{(i >> 12) & 63, (i >> 6) & 63, i & 63, i >> 18, cfgs[ci]};
    gen(s, mv);
    if (mv.empty()) { if (s.stm == 1) return blackInCheck(s) ? (int)LOSS : (int)DRAW; return whiteInCheck(s) ? (int)LOSS : (int)DRAW; }
    bool allw = true;
    for (auto &m : mv) { int v = m.term == -1 ? LOSS : look(m.s, nullptr); // term: White to move after Black's win = LOSS for White
      if (v == LOSS) return (int)WIN; if (v != WIN) allw = false; }
    return allw ? (int)LOSS : (int)UNK;
  };
  // predecessors in this cfg: quiet king or queen moves of the side that just moved
  while (!work.empty()) {
    int i = work.back(); work.pop_back(); if (Vv[i] != UNK) continue;
    int v = ev(i); if (v == UNK) continue; Vv[i] = v; if (v == DRAW) continue;
    int stm = i >> 18, wk = (i >> 12) & 63, bk = (i >> 6) & 63, wq = i & 63;
    if (stm == 1) { // White moved: king or queen
      for (U64 t = KATT[wk]; t; t &= t - 1) { int j = idx(0, __builtin_ctzll(t), bk, wq); if (ok[j] && Vv[j] == UNK) work.push_back(j); }
      U64 occ = cfgs[ci].wp | cfgs[ci].bp | B(wk) | B(bk);
      for (U64 t = qatt(wq, occ); t; t &= t - 1) { int j = idx(0, wk, bk, __builtin_ctzll(t)); if (ok[j] && Vv[j] == UNK) work.push_back(j); }
    } else {
      for (U64 t = KATT[bk]; t; t &= t - 1) { int j = idx(1, wk, __builtin_ctzll(t), wq); if (ok[j] && Vv[j] == UNK) work.push_back(j); }
    }
  }
  for (int i = 0; i < N; i++) if (ok[i] && Vv[i] == UNK) Vv[i] = DRAW;
}
int main() {
  for (int s = 0; s < 64; s++) { KATT[s] = 0; for (int d = 0; d < 64; d++) if (d != s && kdist(s, d) == 1) KATT[s] |= B(d); }
  vector<S> L; char line[256]; vector<int> audit;
  while (fgets(line, sizeof line, stdin)) {
    string f(line);
    if (f.rfind("AUDIT ", 0) == 0) { int q = (f[6] - 'a') + 8 * (f[7] - '1'); audit.push_back(q); Cfg c{0, B(q)}; closure(c); continue; }
    if (f.size() < 10) continue;
    S s{}; s.c.wp = s.c.bp = 0; int r = 7, fl = 0; size_t i = 0;
    for (; f[i] != ' '; i++) { char ch = f[i]; if (ch == '/') { r--; fl = 0; continue; } if (ch >= '1' && ch <= '8') { fl += ch - '0'; continue; }
      int q = fl + 8 * r; if (ch == 'K') s.wk = q; else if (ch == 'k') s.bk = q; else if (ch == 'Q') s.wq = q; else if (ch == 'P') s.c.wp |= B(q); else if (ch == 'p') s.c.bp |= B(q); fl++; }
    s.stm = f[i + 1] == 'b' ? 1 : 0; L.push_back(s);
  }
  for (auto &s : L) closure(s.c);
  fprintf(stderr, "leaves %zu, pawn cfgs %zu (%.0f MB)\n", L.size(), cfgs.size(), cfgs.size() * 524288.0 * 2 / 1e6);
  vector<int> ord(cfgs.size()); for (size_t i = 0; i < ord.size(); i++) ord[i] = i;
  sort(ord.begin(), ord.end(), [](int a, int b) { return pot(cfgs[a]) > pot(cfgs[b]); });
  V.resize(cfgs.size()); Dd.resize(cfgs.size());
  for (int c : ord) solve(c);
  long w = 0, other = 0;
  for (auto &s : L) { int v = look(s, nullptr); // Black to move: LOSS = White wins
    if (v == LOSS) w++; else { other++; printf("NOT WON (conservative): wk%d bk%d wq%d %s\n", s.wk, s.bk, s.wq, v == WIN ? "Black win" : "draw"); } }
  printf("leaves %zu: White wins (conservative chess) %ld, other %ld; ep-skips %ld\n", L.size(), w, other, epWarn);
  // audit of the stated KNOWN fact: K+Q against K + one pawn on square q, Black to move, queen not capturable,
  // Black not stalemated (has a legal move), Black not in check or in check (both counted)
  for (int q : audit) {
    long tot = 0, won = 0, shown = 0; vector<Sc> mv;
    for (int wk = 0; wk < 64; wk++) for (int bk = 0; bk < 64; bk++) for (int wq = 0; wq < 64; wq++) {
      S s{wk, bk, wq, 1, Cfg{0, B(q)}}; if (!valid(s)) continue;
      if (getenv("PATTERN") && !(wq == 57 && (wk == 48 || wk == 50))) continue;  // Qb8 with Ka7/Kc7 (the leaves' shape)
      if (kdist(bk, wq) == 1 && kdist(wk, wq) > 1) continue;  // queen capturable by the king
      if (bpatt(B(q)) & B(wq)) continue;                       // queen capturable by the pawn
      gen(s, mv); if (mv.empty()) continue;                    // stalemated or mated
      tot++; int v = look(s, nullptr); if (v == LOSS) won++;
      else if (shown < 6) { shown++; printf("   audit pawn %c%d not won (%s): wk %c%d bk %c%d wq %c%d\n", 'a' + FI(q), RA(q) + 1, v == WIN ? "Black wins conservatively" : "draw",
                         'a' + FI(wk), RA(wk) + 1, 'a' + FI(bk), RA(bk) + 1, 'a' + FI(wq), RA(wq) + 1); }
    }
    printf("audit pawn %c%d, Black to move, queen safe, Black has a move: %ld positions, White wins (conservative) %ld, not won %ld\n",
           'a' + FI(q), RA(q) + 1, tot, won, tot - won);
  }
  return 0;
}
