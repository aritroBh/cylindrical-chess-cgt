// K55 referee: own solver for r(G (+) T), G = a king-and-pawn group on cyl:Wx6 played as the P game of its own pieces,
// T = a small (possibly loopy) game. Written for this check from the model statement only (no code of za, zb, rz).
// Model: files wrap, ranks do not; kings may not stand next to each other or on an attacked square; pawns step,
// double-step from their first rank, capture diagonally (with wrap) and en passant; a legal promotion is a terminal
// win for the promoter; a side in check may not move in T; a move in T clears the e.p. right; a side with no legal
// move loses. Infinite play is a draw. Values by repeated sweeps to the least fixed point (no counters, no queue).
// Squares are file-major: s = f*H + r.
// Usage: rv55 W H roots.txt tests.txt [moves]      (roots: "Kg4 kf6 Pb3 ..." lines; both sides to move)
//        rv55 W H roots.txt tests.txt dump K       (print the T-start value of every K-th node: "pieces stm ep | W/L/D")
// tests: lines "name<TAB>n<TAB>L0<TAB>R0<TAB>L1<TAB>R1 ..."; a list is "-" or comma-separated node numbers.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <unordered_map>
#include <sys/resource.h>
using namespace std;
typedef uint64_t u64;
static int W, H;
static inline int SQ(int f, int r) { f %= W; if (f < 0) f += W; return f * H + r; }
static inline int FL(int s) { return s / H; }
static inline int RK(int s) { return s % H; }
struct P { u64 w, b; int wk, bk, ep; };
struct Key { u64 w, b; uint32_t m; bool operator==(const Key& o) const { return w == o.w && b == o.b && m == o.m; } };
struct KeyH { size_t operator()(const Key& k) const { u64 h = k.w * 0xff51afd7ed558ccdULL; h ^= (k.b + 0x9e3779b97f4a7c15ULL) * 0xc4ceb9fe1a85ec53ULL; h ^= (u64)k.m * 0x2545F4914F6CDD1DULL; h ^= h >> 31; return h; } };
static Key key(const P& p) { return {p.w, p.b, (uint32_t)(p.wk | (p.bk << 7) | ((p.ep + 1) << 14))}; }
static bool near(int a, int b) { int df = abs(FL(a) - FL(b)); if (W - df < df) df = W - df; return a != b && df <= 1 && abs(RK(a) - RK(b)) <= 1; }
// does colour c (0 White, 1 Black) attack square s
static bool att(const P& p, int s, int c) {
  int f = FL(s), r = RK(s);
  if (c == 0) { if (near(p.wk, s)) return true; if (r - 1 >= 0 && ((p.w >> SQ(f - 1, r - 1)) & 1 || (p.w >> SQ(f + 1, r - 1)) & 1)) return true; }
  else { if (near(p.bk, s)) return true; if (r + 1 < H && ((p.b >> SQ(f - 1, r + 1)) & 1 || (p.b >> SQ(f + 1, r + 1)) & 1)) return true; }
  return false;
}
static bool inchk(const P& p, int c) { return att(p, c == 0 ? p.wk : p.bk, 1 - c); }
struct Mv { P to; int from, dest; };
// legal moves of colour c; promo set if some legal promotion exists (promotions are not listed)
static void moves(const P& p, int c, vector<Mv>& out, bool& promo) {
  out.clear(); promo = false;
  u64 occ = p.w | p.b | (1ULL << p.wk) | (1ULL << p.bk);
  u64 mine = c ? p.b : p.w, theirs = c ? p.w : p.b;
  int k = c ? p.bk : p.wk, ek = c ? p.wk : p.bk;
  for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
    if (!df && !dr) continue; int r = RK(k) + dr; if (r < 0 || r >= H) continue; int t = SQ(FL(k) + df, r);
    if ((mine >> t) & 1) continue; if (near(t, ek) || t == ek) continue;
    P q = p; q.ep = -1; if (c) { q.bk = t; q.w &= ~(1ULL << t); } else { q.wk = t; q.b &= ~(1ULL << t); }
    if (inchk(q, c)) continue; out.push_back({q, k, t});
  }
  int fw = c ? -1 : 1, first = c ? H - 2 : 1, lastr = c ? 0 : H - 1;
  for (int s = 0; s < W * H; s++) {
    if (!((mine >> s) & 1)) continue; int f = FL(s), r = RK(s), r1 = r + fw; if (r1 < 0 || r1 >= H) continue;
    auto tryit = [&](int t, int capsq, int newep) {
      P q = p; q.ep = -1; u64& my = c ? q.b : q.w; u64& th = c ? q.w : q.b; my &= ~(1ULL << s); if (capsq >= 0) th &= ~(1ULL << capsq);
      if (RK(t) == lastr) { if (!inchk(q, c)) promo = true; return; }
      my |= 1ULL << t; q.ep = newep; if (inchk(q, c)) return; out.push_back({q, s, t});
    };
    int t1 = SQ(f, r1);
    if (!((occ >> t1) & 1)) { tryit(t1, -1, -1);
      if (r == first) { int r2 = r1 + fw; if (r2 >= 0 && r2 < H) { int t2 = SQ(f, r2); if (!((occ >> t2) & 1)) tryit(t2, -1, t1); } } }
    for (int d = -1; d <= 1; d += 2) { int tc = SQ(f + d, r1);
      if ((theirs >> tc) & 1) tryit(tc, tc, -1);
      else if (p.ep == tc) { int v = SQ(f + d, r); if ((theirs >> v) & 1) tryit(tc, v, -1); } }
  }
}
static P parse(const char* line) { P p{0, 0, -1, -1, -1}; char b[16]; int n; const char* c = line;
  while (sscanf(c, "%15s%n", b, &n) == 1) { c += n; if (strlen(b) < 3) continue; int s = SQ(b[1] - 'a', atoi(b + 2) - 1);
    if (b[0] == 'K') p.wk = s; else if (b[0] == 'k') p.bk = s; else if (b[0] == 'P') p.w |= 1ULL << s; else if (b[0] == 'p') p.b |= 1ULL << s; }
  return p; }
static string nm(int s) { char b[8]; snprintf(b, 8, "%c%d", 'a' + FL(s), RK(s) + 1); return b; }
static string show(const P& p) { string o = "K" + nm(p.wk) + " k" + nm(p.bk);
  for (int s = 0; s < W * H; s++) if ((p.w >> s) & 1) o += " P" + nm(s);
  for (int s = 0; s < W * H; s++) if ((p.b >> s) & 1) o += " p" + nm(s); return o; }
struct TG { string name; int n; vector<vector<int>> L, R; };
static vector<int> lst(const string& s) { vector<int> v; if (s == "-") return v; size_t a = 0; while (a < s.size()) { size_t e = s.find(',', a); if (e == string::npos) e = s.size(); v.push_back(atoi(s.substr(a, e - a).c_str())); a = e + 1; } return v; }
int main(int argc, char** argv) {
  W = atoi(argv[1]); H = atoi(argv[2]); bool wantMoves = argc > 5 && !strcmp(argv[5], "moves"); int dumpK = (argc > 6 && !strcmp(argv[5], "dump")) ? atoi(argv[6]) : 0;
  vector<P> nodes; unordered_map<Key, int, KeyH> id; vector<int> roots; vector<string> rootStr;
  auto get = [&](const P& p) { Key k = key(p); auto it = id.find(k); if (it != id.end()) return it->second; int i = nodes.size(); id.emplace(k, i); nodes.push_back(p); return i; };
  { FILE* f = fopen(argv[3], "r"); char line[512]; while (fgets(line, sizeof line, f)) { if (line[0] == '#' || line[0] == '\n') continue; line[strcspn(line, "\n")] = 0; roots.push_back(get(parse(line))); rootStr.push_back(line); } fclose(f); }
  vector<uint8_t> ok[2], chk[2], pro[2]; vector<int> clr; vector<int64_t> off[2]; vector<int32_t> to[2];
  off[0].push_back(0); off[1].push_back(0);
  vector<Mv> mv;
  for (size_t i = 0; i < nodes.size(); i++) {
    P p = nodes[i];
    for (int c = 0; c < 2; c++) {
      bool v = !inchk(p, 1 - c);
      if (p.ep >= 0) { bool whiteMade = RK(p.ep) == 2; if (whiteMade == (c == 0)) v = false; }
      bool pr = false; ok[c].push_back(v); chk[c].push_back(inchk(p, c));
      if (v) { moves(p, c, mv, pr); for (auto& m : mv) to[c].push_back(get(m.to)); }
      pro[c].push_back(pr); off[c].push_back(to[c].size());
    }
    P q = p; q.ep = -1; clr.push_back(get(q));
  }
  size_t N = nodes.size();
  fprintf(stderr, "group nodes %zu, edges %zu + %zu\n", N, to[0].size(), to[1].size());
  { unordered_map<Key, int, KeyH> e; id.swap(e); }
  vector<TG> tests; { FILE* f = fopen(argv[4], "r"); static char line[1 << 20];
    while (fgets(line, sizeof line, f)) { if (line[0] == '#' || line[0] == '\n') continue; line[strcspn(line, "\n")] = 0;
      vector<string> tok; char* s = strtok(line, "\t"); while (s) { tok.push_back(s); s = strtok(NULL, "\t"); }
      TG g; g.name = tok[0]; g.n = atoi(tok[1].c_str()); g.L.resize(g.n); g.R.resize(g.n);
      for (int i = 0; i < g.n; i++) { g.L[i] = lst(tok[2 + 2 * i]); g.R[i] = lst(tok[3 + 2 * i]); }
      tests.push_back(g); } fclose(f); }
  for (auto& T : tests) {
    int m = T.n; size_t S = N * m * 2; vector<uint8_t> val(S, 0); // 0 open, 1 White wins, 2 Black wins
    auto I = [&](size_t z, int t, int s) { return (z * m + t) * 2 + s; };
    int sweeps = 0;
    for (bool ch = true; ch; sweeps++) { ch = false;
      for (size_t zz = 0; zz < N; zz++) { size_t z = (sweeps & 1) ? zz : N - 1 - zz;
        for (int t = 0; t < m; t++) for (int s = 0; s < 2; s++) {
          if (!ok[s][z]) continue; size_t i = I(z, t, s); if (val[i]) continue;
          uint8_t me = s == 0 ? 1 : 2, opp = 3 - me;
          if (pro[s][z]) { val[i] = me; ch = true; continue; }
          bool win = false, allLose = true;
          for (int64_t e = off[s][z]; e < off[s][z + 1] && !win; e++) { uint8_t x = val[I(to[s][e], t, 1 - s)]; if (x == me) win = true; else if (x != opp) allLose = false; }
          if (!win && !chk[s][z]) for (int t2 : (s == 0 ? T.L[t] : T.R[t])) { uint8_t x = val[I(clr[z], t2, 1 - s)]; if (x == me) { win = true; break; } else if (x != opp) allLose = false; }
          if (win) { val[i] = me; ch = true; } else if (allLose) { val[i] = opp; ch = true; }
        } } }
    auto ch = [](uint8_t x) { return x == 1 ? 'W' : x == 2 ? 'L' : 'D'; };
    printf("%s", T.name.c_str());
    for (size_t r = 0; r < roots.size(); r++) printf(" | %c%c", ch(val[I(roots[r], 0, 0)]), ch(val[I(roots[r], 0, 1)]));
    printf("   (sweeps %d)\n", sweeps);
    if (wantMoves) for (size_t r = 0; r < roots.size(); r++) for (int s = 0; s < 2; s++) { size_t z = roots[r];
      printf("  %s %s to move: %c ;", rootStr[r].c_str(), s ? "b" : "w", ch(val[I(z, 0, s)]));
      bool pr; moves(nodes[z], s, mv, pr); if (pr) printf(" [promotion]");
      for (auto& x : mv) { int j = -1; for (int64_t e = off[s][z]; e < off[s][z + 1]; e++) if (!memcmp(&nodes[to[s][e]], &x.to, sizeof(P))) j = to[s][e];
        // find id by scanning the successor list (positions compare by value)
        if (j < 0) for (int64_t e = off[s][z]; e < off[s][z + 1]; e++) { const P& a = nodes[to[s][e]]; if (a.w == x.to.w && a.b == x.to.b && a.wk == x.to.wk && a.bk == x.to.bk && a.ep == x.to.ep) j = to[s][e]; }
        printf(" %s-%s:%c", nm(x.from).c_str(), nm(x.dest).c_str(), j < 0 ? '?' : ch(val[I(j, 0, 1 - s)])); }
      if (!chk[s][z]) for (int t2 : (s == 0 ? T.L[0] : T.R[0])) printf(" T0->%d:%c", t2, ch(val[I(clr[z], t2, 1 - s)]));
      printf("\n"); }
    if (dumpK) for (size_t z = 0; z < N; z += dumpK) for (int s = 0; s < 2; s++) { if (!ok[s][z]) continue;
      printf("V %s %c %s | %c\n", show(nodes[z]).c_str(), s ? 'b' : 'w', nodes[z].ep < 0 ? "-" : nm(nodes[z].ep).c_str(), ch(val[I(z, 0, s)])); }
    fflush(stdout);
  }
  struct rusage ru; getrusage(RUSAGE_SELF, &ru); fprintf(stderr, "peak rss %ld bytes\n", (long)ru.ru_maxrss);
}
