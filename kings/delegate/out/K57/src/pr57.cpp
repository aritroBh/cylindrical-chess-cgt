// K57 (copy of K56 pr56.cpp with an --explore mode). K56: the P game of a king-and-pawn group on a cylinder or flat board, with one-sided passes.
// Written for K56 from kings/SPEC.md and LOOPY Definitions 1.2, 1.3, 4.8; no code taken from other solvers.
//
// Rules (P model): chess moves of kings and pawns; the first promotion ends the game as a win for the promoter;
// checkmate loses; stalemate is a draw (in the pass game a side that may pass is never stalemated);
// infinite play is a draw (least fixed point). E.p. as in SPEC.md.
// Pass (a move elsewhere, Definition 1.3 with K40's convention): only the passer may pass; not while in check;
// a pass leaves the board unchanged, gives the move to the other side and clears the e.p. right.
//
// Modes:
//   pr56 --board cyl:10x6 --root "Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5" --shuttle g6 --orient over [--kmax 6] [--sample N seed]
//       builds the component reachable from the four roots (and closed under passes), then
//       (1) Definition 4.8 test (k = 0) and the pass-robust test (unlimited passes) with the smallest number of passes
//           that saves each failing move; (2) --sample: N random nodes with their P values (no passes), for validation.
//   --sum <file>: D-sum results r(G (+) T) for the four roots and both freezes' q (see sum mode below).
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <deque>
#include <algorithm>
#include <random>
#include <sys/resource.h>

using namespace std;
typedef uint64_t u64;

static int W, H, NSQ, WRAP;
static int adjN[64], adjL[64][8];
static u64 kAtt[64];
static u64 pAttBy[2][64];  // squares from which a pawn of colour c attacks s
static inline u64 BIT(int s) { return 1ULL << s; }
static int stepSq(int s, int df, int dr) {
  int f = s % W + df, r = s / W + dr;
  if (r < 0 || r >= H) return -1;
  if (WRAP) f = ((f % W) + W) % W;
  else if (f < 0 || f >= W) return -1;
  return r * W + f;
}
static void initGeom() {
  NSQ = W * H;
  for (int s = 0; s < NSQ; s++) {
    adjN[s] = 0; kAtt[s] = 0;
    for (int df = -1; df <= 1; df++)
      for (int dr = -1; dr <= 1; dr++) {
        if (!df && !dr) continue;
        int t = stepSq(s, df, dr);
        if (t < 0 || t == s) continue;
        if (kAtt[s] & BIT(t)) continue;
        kAtt[s] |= BIT(t); adjL[s][adjN[s]++] = t;
      }
    pAttBy[0][s] = pAttBy[1][s] = 0;
    for (int df = -1; df <= 1; df += 2) {
      int a = stepSq(s, df, -1); if (a >= 0) pAttBy[0][s] |= BIT(a);  // white pawn below attacks s
      int b = stepSq(s, df, +1); if (b >= 0) pAttBy[1][s] |= BIT(b);  // black pawn above attacks s
    }
  }
}
static string sqName(int s) { char b[8]; snprintf(b, 8, "%c%d", 'a' + s % W, s / W + 1); return b; }
static int parseSq(const char *p) { return (atoi(p + 1) - 1) * W + (p[0] - 'a'); }

struct Pos { u64 wp, bp; int wk, bk, stm, ep; };  // stm 0 white 1 black; ep = target square or -1
struct Key { u64 a, b; uint32_t c; bool operator==(const Key &o) const { return a == o.a && b == o.b && c == o.c; } };
static Key keyOf(const Pos &p) { Key k; k.a = p.wp; k.b = p.bp; k.c = p.wk | (p.bk << 6) | (p.stm << 12) | ((p.ep + 1) << 13); return k; }
static Pos posOf(const Key &k) { Pos p; p.wp = k.a; p.bp = k.b; p.wk = k.c & 63; p.bk = (k.c >> 6) & 63; p.stm = (k.c >> 12) & 1; p.ep = (int)((k.c >> 13) & 127) - 1; return p; }

static bool attackedBy(int s, int c, u64 wp, u64 bp, int wk, int bk) {
  if (c == 0) return (kAtt[s] & BIT(wk)) || (pAttBy[0][s] & wp);
  return (kAtt[s] & BIT(bk)) || (pAttBy[1][s] & bp);
}
static bool inCheck(const Pos &p) {
  return p.stm == 0 ? attackedBy(p.wk, 1, p.wp, p.bp, p.wk, p.bk) : attackedBy(p.bk, 0, p.wp, p.bp, p.wk, p.bk);
}
struct Mv { Pos to; bool promo; string name; };
// legal moves of the side to move; promotions are listed with promo = true (terminal win for the mover)
static void gen(const Pos &p, vector<Mv> &out, bool names) {
  out.clear();
  int c = p.stm;
  u64 occ = p.wp | p.bp | BIT(p.wk) | BIT(p.bk);
  u64 own = c == 0 ? p.wp : p.bp, opp = c == 0 ? p.bp : p.wp;
  auto push = [&](Pos q, bool promo, int from, int to, char pc) {
    // legality: own king not attacked after the move
    int myk = c == 0 ? q.wk : q.bk;
    if (attackedBy(myk, 1 - c, q.wp, q.bp, q.wk, q.bk)) return;
    q.stm = 1 - c;
    Mv m; m.to = q; m.promo = promo;
    if (names) m.name = string(1, pc) + sqName(from) + sqName(to) + (promo ? "=" : "");
    out.push_back(m);
  };
  // king
  int ks = c == 0 ? p.wk : p.bk;
  for (int i = 0; i < adjN[ks]; i++) {
    int t = adjL[ks][i];
    if (own & BIT(t)) continue;
    if (t == p.wk || t == p.bk) continue;
    Pos q = p; q.ep = -1;
    if (c == 0) { q.wk = t; q.bp &= ~BIT(t); } else { q.bk = t; q.wp &= ~BIT(t); }
    push(q, false, ks, t, c == 0 ? 'K' : 'k');
  }
  // pawns
  int dir = c == 0 ? 1 : -1, lastR = c == 0 ? H - 1 : 0, startR = c == 0 ? 1 : H - 2;
  for (u64 m = own; m; m &= m - 1) {
    int s = __builtin_ctzll(m), r = s / W;
    char pc = c == 0 ? 'P' : 'p';
    int t = stepSq(s, 0, dir);
    if (t >= 0 && !(occ & BIT(t))) {
      Pos q = p; q.ep = -1;
      if (c == 0) q.wp = (q.wp & ~BIT(s)) | (t / W == lastR ? 0 : BIT(t)); else q.bp = (q.bp & ~BIT(s)) | (t / W == lastR ? 0 : BIT(t));
      push(q, t / W == lastR, s, t, pc);
      if (r == startR) {
        int t2 = stepSq(t, 0, dir);
        if (t2 >= 0 && !(occ & BIT(t2))) {
          Pos q2 = p; q2.ep = -1;
          bool promo2 = t2 / W == lastR;
          if (c == 0) q2.wp = (q2.wp & ~BIT(s)) | (promo2 ? 0 : BIT(t2)); else q2.bp = (q2.bp & ~BIT(s)) | (promo2 ? 0 : BIT(t2));
          if (!promo2) {
            // keep the e.p. target only if an enemy pawn stands beside t2 (it could capture)
            bool cap = false;
            for (int df = -1; df <= 1; df += 2) { int a = stepSq(t2, df, 0); if (a >= 0 && (opp & BIT(a))) cap = true; }
            if (cap) q2.ep = t;
          }
          push(q2, promo2, s, t2, pc);
        }
      }
    }
    for (int df = -1; df <= 1; df += 2) {
      int x = stepSq(s, df, dir);
      if (x < 0) continue;
      if (opp & BIT(x)) {
        Pos q = p; q.ep = -1;
        bool pr = x / W == lastR;
        if (c == 0) { q.bp &= ~BIT(x); q.wp = (q.wp & ~BIT(s)) | (pr ? 0 : BIT(x)); }
        else { q.wp &= ~BIT(x); q.bp = (q.bp & ~BIT(s)) | (pr ? 0 : BIT(x)); }
        push(q, pr, s, x, pc);
      } else if (x == p.ep) {
        int victim = stepSq(x, 0, -dir);
        Pos q = p; q.ep = -1;
        if (c == 0) { q.bp &= ~BIT(victim); q.wp = (q.wp & ~BIT(s)) | BIT(x); }
        else { q.wp &= ~BIT(victim); q.bp = (q.bp & ~BIT(s)) | BIT(x); }
        push(q, false, s, x, pc);
      }
    }
  }
}
static string fen(const Pos &p) {
  string s = "K" + sqName(p.wk) + " k" + sqName(p.bk);
  for (u64 m = p.wp; m; m &= m - 1) s += " P" + sqName(__builtin_ctzll(m));
  for (u64 m = p.bp; m; m &= m - 1) s += " p" + sqName(__builtin_ctzll(m));
  s += p.stm == 0 ? " w " : " b ";
  s += p.ep >= 0 ? sqName(p.ep) : "-";
  return s;
}
static Pos parsePos(const string &txt, int stm) {
  Pos p; p.wp = p.bp = 0; p.wk = p.bk = -1; p.stm = stm; p.ep = -1;
  char buf[4096]; strncpy(buf, txt.c_str(), 4095); buf[4095] = 0;
  for (char *t = strtok(buf, " "); t; t = strtok(NULL, " ")) {
    if (t[0] == 'K') p.wk = parseSq(t + 1);
    else if (t[0] == 'k') p.bk = parseSq(t + 1);
    else if (t[0] == 'P') p.wp |= BIT(parseSq(t + 1));
    else if (t[0] == 'p') p.bp |= BIT(parseSq(t + 1));
  }
  return p;
}

// ---------- node table ----------
static vector<Key> keys;
static vector<uint32_t> table;
static u64 tmask;
static inline u64 hashKey(const Key &k) {
  u64 h = k.a * 0x9E3779B97F4A7C15ULL ^ (k.b + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL ^ (u64)k.c * 0x165667B19E3779F9ULL;
  return h ^ (h >> 29);
}
static void rehash(size_t sz) {
  table.assign(sz, 0xFFFFFFFFu); tmask = sz - 1;
  for (uint32_t i = 0; i < keys.size(); i++) {
    u64 h = hashKey(keys[i]) & tmask;
    while (table[h] != 0xFFFFFFFFu) h = (h + 1) & tmask;
    table[h] = i;
  }
}
static int64_t findKey(const Key &k) {
  u64 h = hashKey(k) & tmask;
  while (table[h] != 0xFFFFFFFFu) { if (keys[table[h]] == k) return table[h]; h = (h + 1) & tmask; }
  return -1;
}
static uint32_t insertKey(const Key &k) {
  u64 h = hashKey(k) & tmask;
  while (table[h] != 0xFFFFFFFFu) { if (keys[table[h]] == k) return table[h]; h = (h + 1) & tmask; }
  uint32_t id = keys.size(); keys.push_back(k); table[h] = id;
  if (keys.size() * 2 > table.size()) rehash(table.size() * 2);
  return id;
}

// graph
static vector<uint32_t> off;     // successor offsets (edges < 2^32)
static vector<uint32_t> succ;    // successors (non-terminal legal moves)
static vector<uint8_t> stmv, chk, promoAv;  // side to move, in check, mover has a legal promotion
static vector<uint32_t> passT;   // pass target or NONE (in check)
static const uint32_t NONE = 0xFFFFFFFFu;
static vector<uint32_t> poff; static vector<uint32_t> pred;   // reverse of succ
static vector<uint32_t> qoff; static vector<uint32_t> qpred;  // reverse of pass edges

static size_t resNodes = 0, resEdges = 0;
static void build(const vector<Pos> &roots) {
  keys.reserve(resNodes); succ.reserve(resEdges); off.reserve(resNodes + 1);
  rehash(1 << 20);
  for (auto &r : roots) insertKey(keyOf(r));
  vector<Mv> mv;
  off.push_back(0);
  for (size_t i = 0; i < keys.size(); i++) {
    Pos p = posOf(keys[i]);
    gen(p, mv, false);
    bool pr = false;
    for (auto &m : mv) { if (m.promo) { pr = true; continue; } uint32_t id = insertKey(keyOf(m.to)); succ.push_back(id); }
    off.push_back(succ.size());
    stmv.push_back(p.stm);
    bool ic = inCheck(p);
    chk.push_back(ic);
    promoAv.push_back(pr);
    if (!ic) { Pos q = p; q.stm = 1 - p.stm; q.ep = -1; passT.push_back(insertKey(keyOf(q))); }
    else passT.push_back(NONE);
  }
  size_t n = keys.size();
  // reverse CSR
  poff.assign(n + 1, 0);
  for (auto t : succ) poff[t + 1]++;
  for (size_t i = 0; i < n; i++) poff[i + 1] += poff[i];
  pred.resize(succ.size());
  { vector<uint32_t> fill(poff.begin(), poff.end() - 1);
    for (size_t i = 0; i < n; i++) for (uint64_t e = off[i]; e < off[i + 1]; e++) pred[fill[succ[e]]++] = i; }
  qoff.assign(n + 1, 0);
  for (size_t i = 0; i < n; i++) if (passT[i] != NONE) qoff[passT[i] + 1]++;
  for (size_t i = 0; i < n; i++) qoff[i + 1] += qoff[i];
  qpred.resize(qoff[n]);
  { vector<uint32_t> fill(qoff.begin(), qoff.end() - 1);
    for (size_t i = 0; i < n; i++) if (passT[i] != NONE) qpred[fill[passT[i]]++] = i; }
}

// Winner Y's attractor. passer: -1 none, else colour that may pass. passMode: 0 none, 1 pass edges to the previous layer
// (prev), 2 pass edges inside the same game (unlimited passes).
static vector<uint8_t> attractor(int Y, int passer, int passMode, const vector<uint8_t> *prev) {
  size_t n = keys.size();
  vector<uint8_t> win(n, 0);
  vector<uint32_t> cnt(n, 0);
  deque<uint32_t> q;
  const uint32_t NEVER = 0xFFFFFFFFu;
  for (size_t i = 0; i < n; i++) {
    int s = stmv[i];
    bool canPass = passMode && s == passer && passT[i] != NONE;
    if (s == Y) {
      if (promoAv[i]) { win[i] = 1; q.push_back(i); continue; }
      if (canPass && passMode == 1 && (*prev)[passT[i]]) { win[i] = 1; q.push_back(i); continue; }
      cnt[i] = 1;  // needs one winning option
    } else {
      if (promoAv[i]) { cnt[i] = NEVER; continue; }
      uint32_t opts = off[i + 1] - off[i];
      if (canPass) {
        if (passMode == 1) { if (!(*prev)[passT[i]]) { cnt[i] = NEVER; continue; } }
        else opts++;
      }
      if (opts == 0 && !(canPass && passMode == 1)) {
        if (chk[i]) { win[i] = 1; q.push_back(i); } else cnt[i] = NEVER;  // mate / stalemate (draw)
        continue;
      }
      if (opts == 0) { win[i] = 1; q.push_back(i); continue; }  // only option is a pass into a win
      cnt[i] = opts;
    }
  }
  auto touch = [&](uint32_t u) {
    if (win[u] || cnt[u] == NEVER) return;
    if (stmv[u] == Y) { win[u] = 1; q.push_back(u); }
    else if (--cnt[u] == 0) { win[u] = 1; q.push_back(u); }
  };
  while (!q.empty()) {
    uint32_t v = q.front(); q.pop_front();
    for (uint64_t e = poff[v]; e < poff[v + 1]; e++) touch(pred[e]);
    if (passMode == 2)
      for (uint64_t e = qoff[v]; e < qoff[v + 1]; e++) { uint32_t u = qpred[e]; if (stmv[u] == passer) touch(u); }
  }
  return win;
}

static long peakMB() { struct rusage ru; getrusage(RUSAGE_SELF, &ru); return ru.ru_maxrss / (1024 * 1024); }  // macOS: bytes

// ---------- sum mode: G (+) T, T a finite D-game ----------
// T file, one game per line (the K47/K55 format): "name | n | 0: L=1,2 R=W ; 1: L= R= ; ..."; W = White's terminal (+), B = Black's (-).
struct TGame { string name; int n; vector<vector<int>> L, R; };  // option -1 = (+), -2 = (-)
static vector<TGame> readTests(const char *fn) {
  vector<TGame> out; FILE *f = fopen(fn, "r"); if (!f) { perror(fn); exit(1); }
  static char line[1 << 20];
  while (fgets(line, sizeof line, f)) {
    string L(line);
    size_t p1 = L.find('|'), p2 = L.find('|', p1 + 1);
    if (p1 == string::npos || p2 == string::npos) continue;
    TGame g; g.name = L.substr(0, p1); while (!g.name.empty() && g.name.back() == ' ') g.name.pop_back();
    g.n = atoi(L.c_str() + p1 + 1); g.L.resize(g.n); g.R.resize(g.n);
    string rest = L.substr(p2 + 1);
    size_t pos = 0;
    while (pos < rest.size()) {
      size_t e = rest.find(';', pos); if (e == string::npos) e = rest.size();
      string item = rest.substr(pos, e - pos); pos = e + 1;
      int i; if (sscanf(item.c_str(), " %d:", &i) != 1) continue;
      auto grab = [&](const char *tag, vector<int> &v) {
        size_t q = item.find(tag); if (q == string::npos) return; q += 2;
        string tok; while (q < item.size() && item[q] != ' ' && item[q] != '\n') tok += item[q++];
        size_t a = 0; while (a < tok.size()) { size_t c = tok.find(',', a); if (c == string::npos) c = tok.size(); string t = tok.substr(a, c - a); a = c + 1;
          if (t.empty()) continue; if (t == "W") v.push_back(-1); else if (t == "B") v.push_back(-2); else v.push_back(atoi(t.c_str())); }
      };
      grab("L=", g.L[i]); grab("R=", g.R[i]);
    }
    out.push_back(g);
  }
  fclose(f); return out;
}
// D-sum G (+) T (Definition 1.3, K40's convention): a G move or a T move; a promotion in G or a move to a terminal of T ends
// the play (terminal W/B wins for that colour, whoever moves into it); a side in check may not move in T; a T move
// clears the e.p. right in G; a side with no move loses; infinite play is a draw. Returns r at (probe node, T node 0).
static void sumSolve(const TGame &T, const vector<uint32_t> &probe, vector<char> &res) {
  size_t n = stmv.size(), m = T.n, N = n * m;
  if (N >= 0xFFFFFFF0ull) { fprintf(stderr, "sum too large\n"); exit(4); }
  vector<vector<pair<int, int>>> tpred(m);  // (t, side) with t' an option of side at t (with multiplicity)
  for (int t = 0; t < (int)m; t++) { for (int o : T.L[t]) if (o >= 0) tpred[o].push_back({t, 0}); for (int o : T.R[t]) if (o >= 0) tpred[o].push_back({t, 1}); }
  vector<uint8_t> val(N, 0);  // bit0 White wins, bit1 Black wins
  vector<uint8_t> cnt(N);
  vector<uint32_t> q;
  const uint8_t NEVER = 255;
  for (int Y = 0; Y < 2; Y++) {
    q.clear();
    const uint8_t WINBIT = 1 << Y;
    auto mark = [&](size_t id) { val[id] |= WINBIT; q.push_back((uint32_t)id); };
    for (size_t g = 0; g < n; g++) {
      int s = stmv[g];
      bool tmoves = passT[g] != NONE;
      int myTerm = s == 0 ? -1 : -2, oppTerm = s == 0 ? -2 : -1;
      for (size_t t = 0; t < m; t++) {
        size_t id = g * m + t;
        const vector<int> &TO = s == 0 ? T.L[t] : T.R[t];
        if (s == Y) {
          bool w = promoAv[g];
          if (tmoves) for (int o : TO) if (o == myTerm) w = true;
          if (w) mark(id); else cnt[id] = 1;
        } else {
          bool never = promoAv[g];
          uint32_t opts = off[g + 1] - off[g];
          if (tmoves) for (int o : TO) { if (o == myTerm) never = true; else if (o != oppTerm) opts++; }
          if (never) { cnt[id] = NEVER; continue; }
          if (opts == 0) { mark(id); continue; }  // no option, or only moves into the opponent's terminal
          if (opts >= NEVER) { fprintf(stderr, "too many options\n"); exit(5); }
          cnt[id] = opts;
        }
      }
    }
    auto touch = [&](size_t u) {
      if ((val[u] & WINBIT) || cnt[u] == NEVER) return;
      if (stmv[u / m] == Y) mark(u);
      else if (--cnt[u] == 0) mark(u);
    };
    for (size_t h = 0; h < q.size(); h++) {
      size_t v = q[h], g = v / m, t = v % m;
      for (uint64_t e = poff[g]; e < poff[g + 1]; e++) touch((size_t)pred[e] * m + t);
      for (uint64_t e = qoff[g]; e < qoff[g + 1]; e++) {
        uint32_t gu = qpred[e];
        for (auto &pt : tpred[t]) if (pt.second == stmv[gu]) touch((size_t)gu * m + pt.first);
      }
    }
  }
  res.clear();
  for (auto g : probe) { uint8_t v = val[(size_t)g * m + 0]; res.push_back(v == 1 ? 'W' : v == 2 ? 'L' : v == 0 ? 'D' : '?'); }
}

int main(int argc, char **argv) {
  string board = "cyl:8x6", root, shuttle, orient = "over", sumFile, probeFile, exploreFile;
  int kmax = 6, sampleN = 0, seed = 1;
  for (int i = 1; i < argc; i++) {
    string a = argv[i];
    if (a == "--board") board = argv[++i];
    else if (a == "--root") root = argv[++i];
    else if (a == "--shuttle") shuttle = argv[++i];
    else if (a == "--orient") orient = argv[++i];
    else if (a == "--kmax") kmax = atoi(argv[++i]);
    else if (a == "--sample") { sampleN = atoi(argv[++i]); seed = atoi(argv[++i]); }
    else if (a == "--sum") sumFile = argv[++i];
    else if (a == "--probe") probeFile = argv[++i];
    else if (a == "--explore") exploreFile = argv[++i];
    else if (a == "--reserve") { resNodes = atoll(argv[++i]); resEdges = atoll(argv[++i]); }
  }
  char kind[8] = {0}; if (sscanf(board.c_str(), "%7[a-z]:%dx%d", kind, &W, &H) != 3) { fprintf(stderr, "bad --board\n"); return 1; }
  WRAP = !strcmp(kind, "cyl");
  if (!WRAP && strcmp(kind, "flat")) { fprintf(stderr, "board kind must be cyl or flat\n"); return 1; }
  initGeom();
  if (NSQ > 64) { fprintf(stderr, "board too large\n"); return 1; }
  if (orient != "over") { fprintf(stderr, "only --orient over is implemented (Black shuttles, White freezes)\n"); return 1; }
  // roots: A = given (Black king on its square), B = Black king on the shuttle square
  Pos A0 = parsePos(root, 0); int za = A0.bk, zb = parseSq(shuttle.c_str());
  Pos B0 = A0; B0.bk = zb;
  vector<Pos> roots;
  for (int z = 0; z < 2; z++) for (int s = 0; s < 2; s++) { Pos p = z ? B0 : A0; p.stm = s; roots.push_back(p); }
  build(roots);
  size_t n = keys.size();
  printf("board %s root %s shuttle %s-%s: %zu nodes, %zu edges, peak %ld MB after build\n", board.c_str(), root.c_str(),
         sqName(za).c_str(), sqName(zb).c_str(), n, succ.size(), peakMB());
  fflush(stdout);

  if (!sumFile.empty()) {
    // probes: the four roots (A_w, A_b, B_w, B_b), then the positions of --probe (one per line, "pieces w|b ep")
    vector<uint32_t> probe; vector<string> pname;
    for (int z = 0; z < 2; z++) for (int s = 0; s < 2; s++) { Pos p = z ? B0 : A0; p.stm = s; int64_t i = findKey(keyOf(p)); probe.push_back(i); pname.push_back(string(z ? "B_" : "A_") + "wb"[s]); }
    if (!probeFile.empty()) {
      FILE *f = fopen(probeFile.c_str(), "r"); char line[1024];
      while (fgets(line, sizeof line, f)) {
        string L(line); while (!L.empty() && (L.back() == '\n' || L.back() == ' ')) L.pop_back(); if (L.empty()) continue;
        size_t a = L.rfind(' '), b2 = L.rfind(' ', a - 1);
        int stm = L[b2 + 1] == 'w' ? 0 : 1; string eps = L.substr(a + 1);
        Pos p = parsePos(L.substr(0, b2), stm); p.ep = eps == "-" ? -1 : parseSq(eps.c_str());
        int64_t i = findKey(keyOf(p)); if (i < 0) { fprintf(stderr, "probe not in component: %s\n", L.c_str()); return 3; }
        probe.push_back(i); pname.push_back(L);
      }
      fclose(f);
    }
    vector<Key>().swap(keys); vector<uint32_t>().swap(table); vector<uint8_t>().swap(chk);
    vector<TGame> tests = readTests(sumFile.c_str());
    printf("SUMHEAD"); for (auto &x : pname) printf(" | %s", x.c_str()); printf("\n");
    for (auto &T : tests) {
      vector<char> r; sumSolve(T, probe, r);
      printf("SUM %s |", T.name.c_str()); for (char c : r) printf(" %c", c); printf("\n");
      fflush(stdout);
    }
    printf("peak %ld MB\n", peakMB());
    return 0;
  }
  // plain P values
  vector<uint8_t> Pw = attractor(0, -1, 0, nullptr), Pb = attractor(1, -1, 0, nullptr);
  auto pval = [&](uint32_t i) { return Pw[i] ? 'W' : Pb[i] ? 'L' : 'D'; };
  if (sampleN) {
    mt19937_64 rng(seed);
    for (int k = 0; k < sampleN; k++) { uint32_t i = rng() % n; printf("SAMPLE %s | %c\n", fen(posOf(keys[i])).c_str(), pval(i)); }
  }
  // layers: WinW[k] = White wins with at most k Black passes; WinB[k] = Black wins with at most k White passes; index kmax+1 = unlimited
  vector<vector<uint8_t>> WinW, WinB;
  WinW.push_back(Pw); WinB.push_back(Pb);
  for (int k = 1; k <= kmax; k++) { WinW.push_back(attractor(0, 1, 1, &WinW[k - 1])); WinB.push_back(attractor(1, 0, 1, &WinB[k - 1])); }
  WinW.push_back(attractor(0, 1, 2, nullptr)); WinB.push_back(attractor(1, 0, 2, nullptr));
  // the mover's own result in the pass game (for the report): X wins with unlimited X passes
  vector<uint8_t> XW_b = attractor(1, 1, 2, nullptr), XW_w = attractor(0, 0, 2, nullptr);  // Black wins passing; White wins passing
  int INF = kmax + 1;
  printf("peak %ld MB after layers\n", peakMB());
  auto idx = [&](const Pos &p) { int64_t i = findKey(keyOf(p)); if (i < 0) { fprintf(stderr, "missing node %s\n", fen(p).c_str()); exit(3); } return (uint32_t)i; };
  // a move by X loses for X: target in Y's set. smallest k that saves it
  auto saveK = [&](uint32_t t, int X) -> string {
    const vector<vector<uint8_t>> &L = X == 1 ? WinW : WinB;
    for (int k = 0; k <= kmax; k++) if (!L[k][t]) return to_string(k);
    if (!L[INF][t]) {
      const vector<uint8_t> &xw = X == 1 ? XW_b : XW_w;
      return string("none<=") + to_string(kmax) + ",unlimited:" + (xw[t] ? "mover-wins" : "draw");
    }
    return "-";
  };
  vector<Mv> mv, mv2;
  if (!exploreFile.empty()) {
    // for each position: its values, and for each legal move the values after it.
    // Pw/Pb: White/Black wins in P; W1/Wi: White wins with Black allowed 1 / unlimited passes; B1/Bi: Black wins with White
    // allowed 1 / unlimited passes; XWb: Black wins with Black passing at will; XWw: White wins with White passing at will.
    FILE *f = fopen(exploreFile.c_str(), "r"); char line[1024];
    auto desc = [&](uint32_t t) {
      string r; r += Pw[t] ? "P=W" : Pb[t] ? "P=L" : "P=D";
      r += string(" W1=") + (WinW[1][t] ? "y" : "n") + " Wi=" + (WinW[INF][t] ? "y" : "n") + " B1=" + (WinB[1][t] ? "y" : "n") + " Bi=" + (WinB[INF][t] ? "y" : "n");
      r += string(" XWb=") + (XW_b[t] ? "y" : "n") + " XWw=" + (XW_w[t] ? "y" : "n");
      return r; };
    while (fgets(line, sizeof line, f)) {
      string L(line); while (!L.empty() && (L.back() == '\n' || L.back() == ' ')) L.pop_back(); if (L.empty() || L[0] == '#') continue;
      size_t a = L.rfind(' '), b2 = L.rfind(' ', a - 1);
      int stm = L[b2 + 1] == 'w' ? 0 : 1; string eps = L.substr(a + 1);
      Pos p = parsePos(L.substr(0, b2), stm); p.ep = eps == "-" ? -1 : parseSq(eps.c_str());
      uint32_t i = idx(p);
      printf("EXPLORE %s | %s%s\n", fen(p).c_str(), desc(i).c_str(), inCheck(p) ? " CHECK" : "");
      gen(p, mv, true);
      for (auto &m : mv) {
        if (m.promo) { printf("   %-9s PROMOTION\n", m.name.c_str()); continue; }
        uint32_t t = idx(m.to);
        printf("   %-9s -> %s | %s%s\n", m.name.c_str(), fen(m.to).c_str(), desc(t).c_str(), inCheck(m.to) ? " CHECK" : "");
      }
    }
    fclose(f);
    printf("peak %ld MB\n", peakMB());
    return 0;
  }
  bool def48 = true, robust = true, budget = true;  // budget: the criterion of K56's Definition (tempo-exact), see PROOF.md
  int nfail = 0, nbfail = 0;
  vector<Pos> qlist;
  for (int z = 0; z < 2; z++) {
    Pos R = z ? B0 : A0; string rn = string("root k") + sqName(R.bk);
    for (int s = 0; s < 2; s++) {
      Pos p = R; p.stm = s;
      if (inCheck(p)) { printf("%s %c: side to move in check\n", rn.c_str(), "wb"[s]); robust = def48 = false; }
    }
    // Black to move
    { Pos p = R; p.stm = 1; gen(p, mv, true);
      int sh = 0;
      printf("%s b (P value %c): %zu moves\n", rn.c_str(), pval(idx(p)), mv.size());
      for (auto &m : mv) {
        bool isSh = m.name[0] == 'k' && m.to.bk == (z ? za : zb);
        if (isSh) { sh++; printf("   %-9s shuttle\n", m.name.c_str()); continue; }
        if (m.promo) { printf("   %-9s PROMOTION\n", m.name.c_str()); def48 = robust = false; continue; }
        uint32_t t = idx(m.to); string k = saveK(t, 1);
        bool l0 = WinW[0][t], li = WinW[INF][t];
        if (!l0) def48 = false;
        if (!li) { robust = false; nfail++; }
        bool bn = WinW[1][t], bv = passT[t] != NONE && WinW[1][passT[t]];
        if (!(bn || bv)) { budget = false; nbfail++; }
        printf("   %-9s loses at once %s, loses vs free passes %s, smallest number of passes that saves it: %s; budget test: (N1) %s (V1) %s\n", m.name.c_str(), l0 ? "yes" : "NO", li ? "yes" : "NO", k.c_str(), bn ? "yes" : "no", bv ? "yes" : "no");
      }
      if (sh != 1) { printf("   shuttle not legal\n"); def48 = robust = false; }
    }
    // White to move
    { Pos p = R; p.stm = 0; gen(p, mv, true);
      int nfz = 0, nfzr = 0;
      printf("%s w (P value %c): %zu moves\n", rn.c_str(), pval(idx(p)), mv.size());
      for (auto &m : mv) {
        if (m.promo) { printf("   %-9s PROMOTION\n", m.name.c_str()); def48 = robust = false; continue; }
        uint32_t t = idx(m.to);
        bool l0 = WinB[0][t], li = WinB[INF][t];
        bool bv0 = passT[t] != NONE && WinB[0][passT[t]];
        if (li) { printf("   %-9s loses vs free passes (and at once: %s); budget test: (Ninf) yes (V0) %s\n", m.name.c_str(), l0 ? "yes" : "NO", bv0 ? "yes" : "no"); if (!l0) def48 = false; continue; }
        if (l0) {  // loses at once in P but not against free passes: a failure of a non-freeze move
          robust = false; nfail++;
          if (!bv0) { budget = false; nbfail++; }
          printf("   %-9s loses at once yes, loses vs free passes NO, smallest number of passes that saves it: %s; budget test: (Ninf) no (V0) %s\n", m.name.c_str(), saveK(t, 0).c_str(), bv0 ? "yes" : "no");
          continue;
        }
        // candidate freeze: test q
        Pos qb = m.to, qbn = m.to, qw = m.to; qbn.ep = -1; qw.ep = -1; qw.stm = 0;
        bool ok48 = !l0, okr = true, chkq = inCheck(qb) || inCheck(qw);
        string why;
        if (chkq) { ok48 = okr = false; why += " check-in-q"; }
        for (int v = 0; v < 3; v++) {
          if (v == 1 && qb.ep < 0) continue;  // same position as v == 0
          Pos qq = v == 0 ? qb : v == 1 ? qbn : qw; int X = qq.stm;
          gen(qq, mv2, true);
          if (mv2.empty()) { ok48 = okr = false; why += " no-move"; }
          for (auto &m2 : mv2) {
            if (m2.promo) { ok48 = okr = false; why += " " + m2.name; continue; }
            uint32_t t2 = idx(m2.to);
            const vector<vector<uint8_t>> &L = X == 1 ? WinW : WinB;
            if (!L[0][t2]) ok48 = false;
            if (!L[INF][t2]) { okr = false; nfail++; why += string(" [q ") + "wb"[X] + (v == 0 && qb.ep >= 0 ? " with e.p. flag" : "") + ": " + m2.name + " not lost vs free passes; saved by " + saveK(t2, X) + " passes]"; }
          }
        }
        if (ok48) nfz++;
        if (okr) nfzr++;
        printf("   %-9s candidate freeze (does not lose at once%s): q is a P-zero (Def 4.8) %s, pass-robust zero %s%s\n", m.name.c_str(), "", ok48 ? "yes" : "no", okr ? "yes" : "NO", why.c_str());
        if (!okr) robust = false;
        if (!ok48 && !l0) def48 = false;
        printf("      q = %s ; q with White to move: %s\n", fen(qb).c_str(), fen(qw).c_str());
      }
      if (nfz == 0) def48 = false;
      if (nfzr == 0) robust = false;
    }
  }
  if (!def48) budget = false;
  printf("RESULT %s %s shuttle %s: Definition 4.8 exact: %s; pass-robust exact: %s; failing moves (pass-robust): %d; tempo-exact (budget test): %s, failing root moves %d\n", board.c_str(), root.c_str(),
         shuttle.c_str(), def48 ? "yes" : "NO", robust ? "yes" : "NO", nfail, budget ? "yes" : "NO", nbfail);
  printf("peak %ld MB\n", peakMB());
  return 0;
}
