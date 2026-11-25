// kref.cpp -- K59 referee's own solver (written from scratch, shares no code with anything in kings/).
// P game of a king-and-pawn group on a flat or cylindrical W x H board, and its sum with a finite D-game T.
//   P:   chess moves (double step from the 2nd rank, e.p., no move into check), promotion = terminal win for the
//        promoter, checkmate = loss, stalemate = draw, infinite play = draw.
//   sum: group (+) T under the sum's rule: a move is a group move or a T move; a side in check may not move in T;
//        a T move clears the e.p. right; promotion or a T terminal ends the play; a side with no move loses.
// Values by retrograde analysis (least fixed point) over all states reachable from the seeds.
// Usage:
//   kref check BOARD "PIECES" Z0 Z1          Definition 4.8 (over orientation: Black shuttles Z0-Z1, White king
//                                            fixed) clause by clause in P, then (B1) beside -1 under the sum's rule.
//   kref sum BOARD "PIECES" Z0 Z1 TFILE      group (+) T against over_D (+) T for every T in TFILE (format name|k|L/R;...)
//   kref val BOARD "PIECES" STM [EP]         P value and move list of one position (sanity tests)
// BOARD: flat:WxH or cyl:WxH.  PIECES: e.g. "Ka4 kc4 Pb2 Pf5 pb6 pf6" (Black king on Z0).
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <fstream>
#include <algorithm>
using namespace std;

static int W, H, CYL;
static int sqof(int r, int f) { return r * W + f; }
static int rk(int s) { return s / W; }
static int fl(int s) { return s % W; }
static bool fadd(int f, int d, int &g) {
  g = f + d;
  if (CYL) { g = ((g % W) + W) % W; return true; }
  return g >= 0 && g < W;
}
static int fdist(int a, int b) { int d = abs(a - b); if (CYL) d = min(d, W - d); return d; }
static bool kadj(int a, int b) { return a != b && abs(rk(a) - rk(b)) <= 1 && fdist(fl(a), fl(b)) <= 1; }
static int kdist(int a, int b) { return max(abs(rk(a) - rk(b)), fdist(fl(a), fl(b))); }

struct Pos { uint64_t wp = 0, bp = 0; int wk = 0, bk = 0, stm = 0, ep = -1, t = 0; };
static inline bool has(uint64_t b, int s) { return (b >> s) & 1; }

static string sqname(int s) { string r; r += char('a' + fl(s)); r += to_string(rk(s) + 1); return r; }
static string show(const Pos &p) {
  string o = "K" + sqname(p.wk) + " k" + sqname(p.bk);
  for (int s = 0; s < W * H; s++) if (has(p.wp, s)) o += " P" + sqname(s);
  for (int s = 0; s < W * H; s++) if (has(p.bp, s)) o += " p" + sqname(s);
  o += p.stm ? " b" : " w";
  o += " " + (p.ep >= 0 ? sqname(p.ep) : string("-"));
  return o;
}
static int parsesq(const string &x) { return sqof(atoi(x.c_str() + 1) - 1, x[0] - 'a'); }

// is square s attacked by side `by` (0 White, 1 Black)?
static bool attacked(const Pos &p, int s, int by) {
  if (kadj(s, by ? p.bk : p.wk)) return true;
  int r = rk(s), f = fl(s), g;
  int pr = by ? r + 1 : r - 1;  // a White pawn attacks upward, so it stands one rank below
  if (pr < 0 || pr >= H) return false;
  uint64_t pw = by ? p.bp : p.wp;
  for (int d = -1; d <= 1; d += 2) if (fadd(f, d, g) && has(pw, sqof(pr, g))) return true;
  return false;
}
static bool incheck(const Pos &p, int side) { return attacked(p, side ? p.bk : p.wk, 1 - side); }
static bool occupied(const Pos &p, int s) { return has(p.wp | p.bp, s) || s == p.wk || s == p.bk; }

// keep the e.p. square only if the side to move has a pawn placed to take on it
static void normep(Pos &p) {
  if (p.ep < 0) return;
  int r = rk(p.ep), f = fl(p.ep), g;
  int pr = p.stm ? r + 1 : r - 1;  // Black (to move) takes downward from r+1
  uint64_t pw = p.stm ? p.bp : p.wp;
  bool ok = false;
  if (pr >= 0 && pr < H)
    for (int d = -1; d <= 1; d += 2) if (fadd(f, d, g) && has(pw, sqof(pr, g))) ok = true;
  if (!ok) p.ep = -1;
}

struct Mv { Pos q; int term; string name; };  // term: 0 none, 1 mover wins (promotion)
static void gen(const Pos &p, vector<Mv> &out) {
  out.clear();
  int s = p.stm;
  auto push = [&](Pos q, int term, const string &nm) {
    if (incheck(q, s)) return;  // own king may not be left in check (also for a promotion)
    q.stm = 1 - s;
    normep(q);
    out.push_back({q, term, nm});
  };
  char kc = s ? 'k' : 'K', pc = s ? 'p' : 'P';
  int k = s ? p.bk : p.wk;
  for (int dr = -1; dr <= 1; dr++) for (int df = -1; df <= 1; df++) {
    if (!dr && !df) continue;
    int r2 = rk(k) + dr, f2;
    if (r2 < 0 || r2 >= H || !fadd(fl(k), df, f2)) continue;
    int t = sqof(r2, f2);
    if (has(s ? p.bp : p.wp, t) || t == p.wk || t == p.bk) continue;
    Pos q = p; q.ep = -1;
    if (s) { q.bk = t; q.wp &= ~(1ULL << t); } else { q.wk = t; q.bp &= ~(1ULL << t); }
    push(q, 0, string(1, kc) + sqname(k) + sqname(t));
  }
  uint64_t own = s ? p.bp : p.wp, opp = s ? p.wp : p.bp;
  int dir = s ? -1 : 1, last = s ? 0 : H - 1, start = s ? H - 2 : 1;
  for (int a = 0; a < W * H; a++) if (has(own, a)) {
    int r = rk(a), f = fl(a), r1 = r + dir;
    if (r1 < 0 || r1 >= H) continue;
    auto mk = [&](int to, int capsq, int ep) {
      Pos q = p; q.ep = ep;
      if (s) { q.bp &= ~(1ULL << a); if (capsq >= 0) q.wp &= ~(1ULL << capsq); if (rk(to) != last) q.bp |= 1ULL << to; }
      else   { q.wp &= ~(1ULL << a); if (capsq >= 0) q.bp &= ~(1ULL << capsq); if (rk(to) != last) q.wp |= 1ULL << to; }
      push(q, rk(to) == last ? 1 : 0, string(1, pc) + sqname(a) + sqname(to));
    };
    int t1 = sqof(r1, f);
    if (!occupied(p, t1)) {
      mk(t1, -1, -1);
      if (r == start) { int t2 = sqof(r + 2 * dir, f); if (!occupied(p, t2)) mk(t2, -1, t1); }
    }
    for (int d = -1; d <= 1; d += 2) {
      int g; if (!fadd(f, d, g)) continue;
      int t = sqof(r1, g);
      if (has(opp, t)) mk(t, t, -1);
      else if (t == p.ep) mk(t, sqof(r, g), -1);  // e.p.: the pawn taken stands beside, on the mover's rank
    }
  }
}

// ---- finite D-game T ----
struct DG { string name; vector<vector<int>> L, R; };  // option -1 = W terminal, -2 = B terminal
static vector<DG> readT(const char *fn) {
  vector<DG> v; ifstream in(fn); string line;
  while (getline(in, line)) {
    if (line.empty() || line[0] == '#') continue;
    stringstream ss(line); string nm, ks, body;
    getline(ss, nm, '|'); getline(ss, ks, '|'); getline(ss, body);
    int k = atoi(ks.c_str()); DG g; g.name = nm;
    stringstream bs(body); string part;
    for (int i = 0; i < k; i++) {
      getline(bs, part, ';');
      size_t sl = part.find('/');
      auto conv = [](const string &x) { vector<int> o; stringstream xs(x); string tok;
        while (getline(xs, tok, ',')) { if (tok.empty()) continue; o.push_back(tok == "W" ? -1 : tok == "B" ? -2 : atoi(tok.c_str())); } return o; };
      g.L.push_back(conv(part.substr(0, sl))); g.R.push_back(conv(part.substr(sl + 1)));
    }
    v.push_back(g);
  }
  return v;
}

// ---- graph over reachable states ----
static uint64_t mixh(uint64_t x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ULL; x ^= x >> 33; return x; }

struct Graph {
  bool sumrule = false; const DG *T = nullptr;
  vector<uint64_t> kw, kb; vector<uint32_t> ke;  // state words
  vector<uint32_t> tab; uint64_t cap = 0, n = 0;
  vector<uint64_t> off; vector<uint32_t> ed; vector<uint8_t> val;
  static const uint32_t MW = 0xFFFFFFFF, ML = 0xFFFFFFFE, EMPTY = 0xFFFFFFFF;
  uint32_t ex(const Pos &p) { return (uint32_t)p.wk | ((uint32_t)p.bk << 7) | ((uint32_t)p.stm << 14) | ((uint32_t)(p.ep + 1) << 15) | ((uint32_t)p.t << 22); }
  Pos unpack(uint64_t i) { Pos p; p.wp = kw[i]; p.bp = kb[i]; uint32_t e = ke[i];
    p.wk = e & 127; p.bk = (e >> 7) & 127; p.stm = (e >> 14) & 1; p.ep = (int)((e >> 15) & 127) - 1; p.t = e >> 22; return p; }
  uint64_t h(uint64_t a, uint64_t b, uint32_t e) { return mixh(a * 0x9E3779B97F4A7C15ULL ^ mixh(b + e * 0x632BE59BD9B4E019ULL)); }
  void grow() {
    uint64_t nc = cap ? cap * 2 : (1 << 20); vector<uint32_t> nt(nc, EMPTY);
    for (uint64_t i = 0; i < n; i++) { uint64_t j = h(kw[i], kb[i], ke[i]) & (nc - 1); while (nt[j] != EMPTY) j = (j + 1) & (nc - 1); nt[j] = (uint32_t)i; }
    tab.swap(nt); cap = nc;
  }
  uint32_t get(const Pos &p, bool add) {
    if ((n + 1) * 2 > cap) grow();
    uint32_t e = ex(p); uint64_t j = h(p.wp, p.bp, e) & (cap - 1);
    while (tab[j] != EMPTY) { uint32_t i = tab[j]; if (kw[i] == p.wp && kb[i] == p.bp && ke[i] == e) return i; j = (j + 1) & (cap - 1); }
    if (!add) return EMPTY;
    tab[j] = (uint32_t)n; kw.push_back(p.wp); kb.push_back(p.bp); ke.push_back(e); return (uint32_t)n++;
  }
  // moves of a state under this graph's rules: group moves, then T moves (sum rule only)
  void moves(const Pos &p, vector<Mv> &gm, vector<pair<int, Pos>> &out) {  // out: (code, successor); code 0 node, 1 mover wins, 2 mover loses
    out.clear(); gen(p, gm);
    for (auto &m : gm) out.push_back({m.term ? 1 : 0, m.q});
    if (sumrule && T && !incheck(p, p.stm)) {
      const vector<int> &op = p.stm ? T->R[p.t] : T->L[p.t];
      for (int o : op) {
        if (o < 0) { int winner = o == -1 ? 0 : 1; out.push_back({winner == p.stm ? 1 : 2, p}); continue; }
        Pos q = p; q.stm = 1 - p.stm; q.ep = -1; q.t = o; out.push_back({0, q});
      }
    }
  }
  void build(const vector<Pos> &seeds) {
    for (auto &s : seeds) get(s, true);
    off.push_back(0);
    vector<Mv> gm; vector<pair<int, Pos>> mv;
    for (uint64_t i = 0; i < n; i++) {
      Pos p = unpack(i); moves(p, gm, mv);
      for (auto &m : mv) ed.push_back(m.first == 1 ? MW : m.first == 2 ? ML : get(m.second, true));
      off.push_back(ed.size());
    }
  }
  void solve() {  // val: 1 mover wins, 2 mover loses, 3 draw (stalemate in P), 0 unknown -> draw
    val.assign(n, 0);
    for (uint64_t i = 0; i < n; i++) if (off[i] == off[i + 1]) {
      Pos p = unpack(i); val[i] = (sumrule || incheck(p, p.stm)) ? 2 : 3;
    }
    bool ch = true;
    while (ch) {
      ch = false;
      for (uint64_t i = 0; i < n; i++) {
        if (val[i]) continue;
        bool win = false, allw = true;
        for (uint64_t e = off[i]; e < off[i + 1]; e++) {
          uint32_t t = ed[e];
          if (t == MW) { win = true; break; }
          if (t == ML) continue;
          if (val[t] == 2) { win = true; break; }
          if (val[t] != 1) allw = false;
        }
        if (win) { val[i] = 1; ch = true; } else if (allw) { val[i] = 2; ch = true; }
      }
    }
  }
  // absolute value: 'W' White wins, 'L' Black wins, 'D'
  char absval(const Pos &p) { uint32_t i = get(p, false); if (i == EMPTY) { fprintf(stderr, "state not in graph: %s\n", show(p).c_str()); exit(2); }
    int v = val[i]; if (v == 1) return p.stm ? 'L' : 'W'; if (v == 2) return p.stm ? 'W' : 'L'; return 'D'; }
};

static void board(const char *b) {
  string s(b); CYL = s.rfind("cyl:", 0) == 0;
  if (!CYL && s.rfind("flat:", 0) != 0) { fprintf(stderr, "board must be flat:WxH or cyl:WxH\n"); exit(2); }
  sscanf(s.c_str() + s.find(':') + 1, "%dx%d", &W, &H);
  if (W * H > 64 || W > 16 || H < 5) { fprintf(stderr, "board too big\n"); exit(2); }
}
static Pos parsepieces(const string &ps) {
  Pos p; stringstream ss(ps); string x;
  while (ss >> x) { int s = parsesq(x.substr(1));
    if (x[0] == 'K') p.wk = s; else if (x[0] == 'k') p.bk = s; else if (x[0] == 'P') p.wp |= 1ULL << s; else if (x[0] == 'p') p.bp |= 1ULL << s; }
  return p;
}

static char absP(Graph &g, const Pos &p) { return g.absval(p); }
static const char *nm(char v) { return v == 'W' ? "W" : v == 'L' ? "L" : "D"; }

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: see source\n"); return 2; }
  string cmd = argv[1]; board(argv[2]);
  if (cmd == "val") {
    Pos p = parsepieces(argv[3]); p.stm = argv[4][0] == 'b'; if (argc > 5) p.ep = parsesq(argv[5]); normep(p);
    Graph g; g.build({p}); g.solve();
    printf("nodes %llu edges %zu\n%s : %s\n", (unsigned long long)g.n, g.ed.size(), show(p).c_str(), nm(absP(g, p)));
    vector<Mv> mv; gen(p, mv);
    for (auto &m : mv) printf("   %-8s %s\n", m.name.c_str(), m.term ? "promotion (mover wins)" : nm(absP(g, m.q)));
    if (mv.empty()) printf("   no move (%s)\n", incheck(p, p.stm) ? "checkmate" : "stalemate");
    return 0;
  }
  Pos base = parsepieces(argv[3]); int z[2] = {parsesq(argv[4]), parsesq(argv[5])}; int b0 = base.wk;
  if (base.bk != z[0]) { fprintf(stderr, "Black king must stand on Z0\n"); return 2; }
  int fails = 0;
  auto FAIL = [&](const string &m) { printf("FAIL %s\n", m.c_str()); fails++; };
  // geometry K1, K2 (over orientation: Black shuttles on z, White king on b0)
  Pos root[2][2];  // [a][stm]
  for (int a = 0; a < 2; a++) for (int s = 0; s < 2; s++) { Pos p = base; p.bk = z[a]; p.stm = s; p.ep = -1; root[a][s] = p; }
  printf("board %s%dx%d  pieces %s  shuttle %s-%s\n", CYL ? "cyl:" : "flat:", W, H, argv[3], sqname(z[0]).c_str(), sqname(z[1]).c_str());
  for (int a = 0; a < 2; a++) {
    if (occupied(base, z[a]) && z[a] != base.bk) FAIL("z square occupied");
    Pos p = root[a][0];
    if (attacked(p, z[a], 0)) FAIL("K1/K2: White attacks " + sqname(z[a]));
    if (attacked(p, b0, 1)) FAIL("K1/K2: Black attacks " + sqname(b0) + " with z=" + sqname(z[a]));
    if (kdist(b0, z[a]) < 2) FAIL("K2");
  }
  if (!kadj(z[0], z[1])) FAIL("z not adjacent");
  // P graph: seeds = the four roots, every position one move after a root, and those boards with the other side to move
  vector<Pos> seeds; vector<Mv> mv;
  for (int a = 0; a < 2; a++) for (int s = 0; s < 2; s++) {
    seeds.push_back(root[a][s]); gen(root[a][s], mv);
    for (auto &m : mv) if (!m.term) { seeds.push_back(m.q); Pos q = m.q; q.stm = 1 - q.stm; q.ep = -1; if (!incheck(q, 1 - q.stm)) seeds.push_back(q); }
  }
  Graph P; P.build(seeds); P.solve();
  printf("P graph: %llu nodes, %zu edges\n", (unsigned long long)P.n, P.ed.size());
  vector<pair<Pos, string>> qlist;  // (freeze result, label)
  vector<pair<Pos, string>> b1list; // non-shuttle Black root moves (position after)
  for (int a = 0; a < 2; a++) {
    // (O1) Black to move at root a
    Pos p = root[a][1]; gen(p, mv);
    printf("root %s : P=%s, %zu moves\n", show(p).c_str(), nm(absP(P, p)), mv.size());
    bool shut = false;
    for (auto &m : mv) {
      bool isshut = m.q.bk == z[1 - a] && m.name[0] == 'k' && __builtin_popcountll(m.q.wp) == __builtin_popcountll(p.wp);
      char v = m.term ? 'L' : absP(P, m.q);
      printf("   %-8s -> %s  P(after)=%s%s%s\n", m.name.c_str(), show(m.q).c_str(), nm(v), isshut ? "  shuttle" : "", incheck(m.q, 0) ? "  check" : "");
      if (isshut) { shut = true; continue; }
      if (v != 'W') FAIL("(O1) Black move " + m.name + " does not lose at once");
      b1list.push_back({m.q, m.name + " at " + sqname(z[a])});
    }
    if (!shut) FAIL("(O1) shuttle illegal");
    // (O2) White to move at root a
    p = root[a][0]; gen(p, mv);
    printf("root %s : P=%s, %zu moves\n", show(p).c_str(), nm(absP(P, p)), mv.size());
    int nf = 0;
    for (auto &m : mv) {
      char v = m.term ? 'W' : absP(P, m.q);
      bool fr = v != 'L';
      printf("   %-8s -> %s  P(after)=%s%s\n", m.name.c_str(), show(m.q).c_str(), m.term ? "promotion" : nm(v), fr ? "  FREEZE" : "");
      if (!fr) continue;
      nf++;
      if (m.term) { FAIL("freeze is a promotion"); continue; }
      qlist.push_back({m.q, m.name + " at " + sqname(z[a])});
    }
    if (!nf) FAIL("(O2) no freeze");
  }
  for (auto &qq : qlist) {
    Pos q = qq.first;  // Black to move, with the right if any (normalised: kept only if usable)
    printf("freeze %s\n", qq.second.c_str());
    gen(q, mv);
    printf("   q Black to move %s : P=%s, %zu moves\n", show(q).c_str(), nm(absP(P, q)), mv.size());
    if (mv.empty()) FAIL("(O3) Black has no move at q");
    for (auto &m : mv) { char v = m.term ? 'L' : absP(P, m.q); printf("      %-8s P(after)=%s\n", m.name.c_str(), m.term ? "promotion" : nm(v)); if (v != 'W') FAIL("(O3) " + m.name); }
    Pos q2 = q; q2.ep = -1;
    if (q.ep >= 0 || true) {  // also without the right (Lemma 4.15 talks of both)
      gen(q2, mv); bool allw = !mv.empty();
      for (auto &m : mv) if ((m.term ? 'L' : absP(P, m.q)) != 'W') allw = false;
      printf("   q Black to move without the right: every move loses at once: %s\n", allw ? "yes" : "NO");
    }
    Pos qw = q; qw.stm = 0; qw.ep = -1;
    if (incheck(qw, 1)) { FAIL("(O4) q with White to move illegal (Black in check)"); continue; }
    gen(qw, mv);
    printf("   q White to move %s : P=%s, %zu moves\n", show(qw).c_str(), nm(absP(P, qw)), mv.size());
    if (mv.empty()) FAIL("(O4) White has no move at q");
    for (auto &m : mv) { char v = m.term ? 'W' : absP(P, m.q); printf("      %-8s P(after)=%s\n", m.name.c_str(), m.term ? "promotion" : nm(v)); if (v != 'L') FAIL("(O4) " + m.name); }
  }
  printf("DEFINITION 4.8 (over): %s (%d failures)\n", fails ? "NOT exact" : "exact", fails);
  if (cmd == "check") {
    // tempo-exact (T2) first alternative is not needed; only (B1) here
    DG m1; m1.name = "-1"; m1.L = {{}, {}}; m1.R = {{1}, {}};
    Graph S; S.sumrule = true; S.T = &m1;
    vector<Pos> sd; for (auto &b : b1list) { Pos q = b.first; q.t = 0; sd.push_back(q); }
    S.build(sd); S.solve();
    printf("(B1) graph (group (+) -1, sum rule): %llu nodes, %zu edges\n", (unsigned long long)S.n, S.ed.size());
    int bad = 0;
    for (auto &b : b1list) { Pos q = b.first; q.t = 0; char v = S.absval(q);
      // also: the same position beside 0 (no token), sum rule, for information
      printf("   B1 %-14s -> %s : beside -1 %s\n", b.second.c_str(), show(q).c_str(), nm(v)); if (v != 'W') bad++; }
    printf("(B1): %zu non-shuttle Black root moves, %d not a White win beside -1\n", b1list.size(), bad);
    return 0;
  }
  if (cmd == "sum") {
    vector<DG> Ts = readT(argv[6]);
    // results to compare: roots (both sides) vs omega; q (Black to move with and without right, White to move) vs 0_D
    vector<pair<Pos, int>> cmpos;  // (position, 0 = root/omega, 1 = q/0_D)
    for (int a = 0; a < 2; a++) for (int s = 0; s < 2; s++) cmpos.push_back({root[a][s], 0});
    for (auto &qq : qlist) { Pos q = qq.first; cmpos.push_back({q, 1}); Pos q2 = q; q2.ep = -1; if (q.ep >= 0) cmpos.push_back({q2, 1}); Pos qw = q2; qw.stm = 0; cmpos.push_back({qw, 1}); }
    long nres = 0, ndiff = 0, nodes = 0;
    for (auto &T : Ts) {
      int k = T.L.size();
      // over_D (+) T by plain retrograde: o in {0 = omega, 1 = 0_D}
      vector<int> ov(2 * k * 2, 0);  // index (o*k+t)*2+s ; 1 mover wins, 2 mover loses
      auto idx = [&](int o, int t, int s) { return (o * k + t) * 2 + s; };
      bool ch = true;
      while (ch) { ch = false;
        for (int o = 0; o < 2; o++) for (int t = 0; t < k; t++) for (int s = 0; s < 2; s++) {
          int &v = ov[idx(o, t, s)]; if (v) continue;
          vector<int> succ; bool win = false; int nmv = 0;  // succ: index or -1 mover wins, -2 mover loses
          if (o == 0) { nmv++; int so = s == 0 ? 1 : 0; int r = ov[idx(so, t, 1 - s)]; if (r == 2) win = true; succ.push_back(idx(so, t, 1 - s)); }
          for (int x : (s ? T.R[t] : T.L[t])) { nmv++;
            if (x < 0) { int winner = x == -1 ? 0 : 1; if (winner == s) win = true; else succ.push_back(-2); }
            else { succ.push_back(idx(o, x, 1 - s)); if (ov[idx(o, x, 1 - s)] == 2) win = true; } }
          bool allw = true; for (int x : succ) if (x >= 0 && ov[x] != 1) allw = false;
          if (win) { v = 1; ch = true; } else if (allw) { v = 2; ch = true; }  // nmv == 0 -> allw -> loss
          (void)nmv;
        } }
      Graph G; G.sumrule = true; G.T = &T;
      vector<Pos> sd; for (auto &c : cmpos) for (int t = 0; t < k; t++) { Pos p = c.first; p.t = t; sd.push_back(p); }
      G.build(sd); G.solve(); nodes += G.n;
      for (auto &c : cmpos) for (int t = 0; t < k; t++) {
        Pos p = c.first; p.t = t; char gv = G.absval(p);
        int r = ov[idx(c.second, t, p.stm)]; char oval = r == 1 ? (p.stm ? 'L' : 'W') : r == 2 ? (p.stm ? 'W' : 'L') : 'D';
        nres++;
        if (gv != oval) { ndiff++; printf("DIFF %s t=%d %s group %c over %c\n", T.name.c_str(), t, show(p).c_str(), gv, oval); }
      }
    }
    printf("SUM: %zu games, %ld results compared, %ld differ from over (product nodes in all %ld)\n", Ts.size(), nres, ndiff, nodes);
  }
  return 0;
}
