// K47 implementation A: the K45 group Z_O as a component of a D-sum (LOOPY Definitions 1.2, 1.3, 1.5; K40's
// convention: the component is the P game of the group's pieces, a promotion is a terminal for the promoter,
// a side in check may not move in T, checkmate loses; a side with no move at all loses (N) or draws (C)).
// Written from kings/SPEC.md and LOOPY only.
//
// Usage: za <W> <H> <roots file> <tests file> <conv N|C> [--dump-values]
//   roots file : lines "<pieces> " (no side to move); each root is solved with both sides to move.
//   tests file : one test game per line: "name | m | pos0: L=a,b R=c ; pos1: ..." (start position 0)
// Output: one line per (test, root, side): name root side r(Z+T) and r(over+T), and a MATCH/DIFF flag.
#include <cstdio>
#include <cstdlib>
#include <sys/resource.h>
#include <cstring>
#include <string>
#include <vector>
#include <deque>
#include <unordered_map>
#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>
using namespace std;
typedef unsigned long long u64;
int W, H, NSQ;
static inline int F(int s) { return s % W; }
static inline int R(int s) { return s / W; }
static inline int SQ(int f, int r) { return r * W + ((f % W) + W) % W; }

struct Pl { u64 wp, bp; int wk, bk, ep; };  // ep: target square or -1
struct KH { size_t operator()(const pair<u64, u64>& k) const { return k.first * 0x9E3779B97F4A7C15ULL ^ (k.second + 0x632BE59BD9B4E019ULL + (k.first >> 17)); } };
// K55: pawn bitboards reach bit 49 on cyl:10x6, so the king and e.p. fields start at bit 50 (K47 used bit 48, fine for W <= 9)
static pair<u64, u64> key(const Pl& p) { return {p.wp | ((u64)p.wk << 50) | ((u64)p.bk << 56), p.bp | ((u64)(p.ep + 1) << 50)}; }

bool kingAdj(int a, int b) {
  int df = abs(F(a) - F(b)); df = min(df, W - df); return df <= 1 && abs(R(a) - R(b)) <= 1 && a != b;
}
// is square s attacked by side c (0 white,1 black) pieces in placement p
bool attacked(const Pl& p, int s, int c) {
  int f = F(s), r = R(s);
  if (c == 0) {
    if (kingAdj(p.wk, s)) return true;
    if (r >= 1) { if (p.wp >> SQ(f - 1, r - 1) & 1) return true; if (p.wp >> SQ(f + 1, r - 1) & 1) return true; }
  } else {
    if (kingAdj(p.bk, s)) return true;
    if (r + 1 < H) { if (p.bp >> SQ(f - 1, r + 1) & 1) return true; if (p.bp >> SQ(f + 1, r + 1) & 1) return true; }
  }
  return false;
}
bool inCheck(const Pl& p, int c) { return attacked(p, c == 0 ? p.wk : p.bk, 1 - c); }

// moves of side c from p. Returns placements (ep set as appropriate) and a flag for promotion moves (terminal win).
void gen(const Pl& p, int c, vector<Pl>& out, bool& promo) {
  out.clear(); promo = false;
  u64 own = c == 0 ? p.wp : p.bp, opp = c == 0 ? p.bp : p.wp;
  int ok = c == 0 ? p.wk : p.bk, xk = c == 0 ? p.bk : p.wk;
  u64 occ = p.wp | p.bp | (1ULL << p.wk) | (1ULL << p.bk);
  auto legalAfter = [&](Pl q) { q.ep = -1; return !inCheck(q, c); };
  // king
  for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
    if (!df && !dr) continue;
    int r = R(ok) + dr; if (r < 0 || r >= H) continue;
    int t = SQ(F(ok) + df, r);
    if (own >> t & 1) continue; if (t == xk) continue;
    Pl q = p; q.ep = -1;
    if (c == 0) { q.wk = t; q.bp &= ~(1ULL << t); } else { q.bk = t; q.wp &= ~(1ULL << t); }
    if (kingAdj(q.wk, q.bk)) continue;
    if (!legalAfter(q)) continue;
    out.push_back(q);
  }
  int dir = c == 0 ? 1 : -1, last = c == 0 ? H - 1 : 0, start = c == 0 ? 1 : H - 2;
  for (u64 b = own; b; b &= b - 1) {
    int s = __builtin_ctzll(b), f = F(s), r = R(s), r1 = r + dir;
    auto push = [&](int t, int capsq, int newep) {
      Pl q = p; q.ep = -1;
      u64& mine = c == 0 ? q.wp : q.bp; u64& theirs = c == 0 ? q.bp : q.wp;
      mine &= ~(1ULL << s); if (capsq >= 0) theirs &= ~(1ULL << capsq);
      if (R(t) == last) { // promotion: legal iff own king not attacked after
        if (!inCheck(q, c)) promo = true; return; }
      mine |= 1ULL << t; q.ep = newep;
      if (inCheck(q, c)) return;
      out.push_back(q);
    };
    int t = SQ(f, r1);
    if (!(occ >> t & 1)) {
      push(t, -1, -1);
      if (r == start) { int t2 = SQ(f, r1 + dir); if (!(occ >> t2 & 1)) push(t2, -1, t); }
    }
    for (int df = -1; df <= 1; df += 2) {
      int tc = SQ(f + df, r1);
      if (opp >> tc & 1) push(tc, tc, -1);
      else if (p.ep == tc) { // en passant: captured pawn is behind the target
        int cap = SQ(f + df, r);
        if (opp >> cap & 1) push(tc, cap, -1);
      }
    }
  }
}
Pl parse(const string& line) {
  Pl p{0, 0, -1, -1, -1}; istringstream is(line); string t;
  while (is >> t) { int s = (t[1] - 'a') + (atoi(t.c_str() + 2) - 1) * W;
    if (t[0] == 'K') p.wk = s; else if (t[0] == 'k') p.bk = s; else if (t[0] == 'P') p.wp |= 1ULL << s; else if (t[0] == 'p') p.bp |= 1ULL << s; }
  return p;
}
// --- the component graph ---
vector<Pl> nodes; unordered_map<pair<u64, u64>, int, KH> idx;
// per node and side: valid (side may be to move), check flag, promo flag, successor list
vector<uint8_t> valid[2], chk[2], prom[2];
vector<int> sOff[2], sLst[2]; vector<int> clr;  // clr: node with ep cleared
int getId(const Pl& p, deque<int>& q) {
  auto k = key(p); auto it = idx.find(k); if (it != idx.end()) return it->second;
  int id = nodes.size(); nodes.push_back(p); idx[k] = id; q.push_back(id); return id;
}
void build(const vector<Pl>& roots) {
  deque<int> q; for (auto& r : roots) getId(r, q);
  vector<vector<int>> succ[2]; vector<Pl> mv; bool pr;
  vector<int> clrv;
  size_t done = 0;
  while (done < nodes.size()) {
    int id = done++; Pl p = nodes[id];
    for (int c = 0; c < 2; c++) {
      // side c may move from p iff opponent not in check and ep (if any) was made by the opponent
      bool v = !inCheck(p, 1 - c);
      if (p.ep >= 0) { bool madeByWhite = R(p.ep) == 2; if ((c == 0) == madeByWhite) v = false; }
      valid[c].push_back(v); chk[c].push_back(inCheck(p, c));
      vector<int> s;
      pr = false;
      if (v) { gen(p, c, mv, pr); for (auto& x : mv) s.push_back(getId(x, q)); }
      prom[c].push_back(pr);
      succ[c].push_back(s);
    }
    Pl pc = p; pc.ep = -1; clrv.push_back(getId(pc, q));
  }
  clr = clrv;
  for (int c = 0; c < 2; c++) {
    sOff[c].assign(nodes.size() + 1, 0);
    for (size_t i = 0; i < nodes.size(); i++) sOff[c][i + 1] = sOff[c][i] + succ[c][i].size();
    sLst[c].resize(sOff[c].back());
    for (size_t i = 0; i < nodes.size(); i++) copy(succ[c][i].begin(), succ[c][i].end(), sLst[c].begin() + sOff[c][i]);
    vector<vector<int>>().swap(succ[c]);
  }
}
// --- test games ---
// options: >= 0 a position, -1 the terminal "White has won", -2 "Black has won". Cl: the position with the e.p. right cleared.
struct TG { string name; int m; vector<vector<int>> L, Rr; vector<int> Cl; };
TG parseT(const string& line) {
  // name | m | 0: L=1,2 R=3 ; 1: L= R=
  TG g; size_t a = line.find('|'), b = line.find('|', a + 1);
  g.name = line.substr(0, a); while (!g.name.empty() && g.name.back() == ' ') g.name.pop_back();
  g.m = atoi(line.substr(a + 1, b - a - 1).c_str()); g.L.resize(g.m); g.Rr.resize(g.m); g.Cl.resize(g.m); for (int i = 0; i < g.m; i++) g.Cl[i] = i;
  string rest = line.substr(b + 1); stringstream ss(rest); string part;
  while (getline(ss, part, ';')) {
    int i; char buf1[4096], buf2[4096];
    string P = part; size_t c = P.find(':'); if (c == string::npos) continue; i = atoi(P.substr(0, c).c_str());
    size_t l = P.find("L="), r = P.find("R="), cp = P.find("C=");
    string ls = P.substr(l + 2, r - l - 2), rs = P.substr(r + 2, cp == string::npos ? string::npos : cp - r - 2);
    if (cp != string::npos) g.Cl[i] = atoi(P.substr(cp + 2).c_str());
    auto rd = [](string s, vector<int>& v) { for (char& ch : s) if (ch == ',') ch = ' '; stringstream q(s); string x;
      while (q >> x) v.push_back(x == "W" ? -1 : x == "B" ? -2 : atoi(x.c_str())); };
    rd(ls, g.L[i]); rd(rs, g.Rr[i]); (void)buf1; (void)buf2;
  }
  return g;
}
// D-sum solver over component graph x test game. Result per state: 0 draw, 1 win for side to move, 2 loss for side to move.
// State index: ((z*m + t)*2 + s).
// Packed state byte: bits 6-7 value (0 undecided or draw, 1 win for side to move, 2 loss, 3 unreachable), bits 0-5 counter.
vector<uint8_t> st;
vector<uint8_t> hasEp;  // K55: e.p. flag per node, so that the node list can be freed after the build
char CONV = 'N';
vector<int> pOff[2], pLst[2], cOff, cLst; bool revBuilt = false;
void buildRev() {
  size_t N = clr.size();
  for (int c = 0; c < 2; c++) {
    pOff[c].assign(N + 1, 0);
    for (size_t z = 0; z < N; z++) for (int k = sOff[c][z]; k < sOff[c][z + 1]; k++) pOff[c][sLst[c][k] + 1]++;
    for (size_t z = 0; z < N; z++) pOff[c][z + 1] += pOff[c][z];
    pLst[c].resize(pOff[c][N]); vector<int> fill(pOff[c].begin(), pOff[c].end() - 1);
    for (size_t z = 0; z < N; z++) for (int k = sOff[c][z]; k < sOff[c][z + 1]; k++) pLst[c][fill[sLst[c][k]]++] = z;
  }
  cOff.assign(N + 1, 0); cLst.resize(N);
  for (size_t z = 0; z < N; z++) cOff[clr[z] + 1]++;
  for (size_t z = 0; z < N; z++) cOff[z + 1] += cOff[z];
  { vector<int> fill(cOff.begin(), cOff.end() - 1); for (size_t z = 0; z < N; z++) cLst[fill[clr[z]]++] = z; }
  revBuilt = true;
}
static inline uint8_t V(size_t i) { return st[i] >> 6; }
void solveSum(const TG& T) {
  if (!revBuilt) buildRev();
  size_t N = clr.size(), m = T.m, S = N * m * 2;
  st.assign(S, 0);
  vector<u64> cur((S + 63) / 64, 0), nxt((S + 63) / 64, 0);
  vector<vector<int>> Tpred[2]; Tpred[0].resize(m); Tpred[1].resize(m);
  for (size_t t = 0; t < m; t++) { for (int x : T.L[t]) if (x >= 0) Tpred[0][x].push_back(t); for (int x : T.Rr[t]) if (x >= 0) Tpred[1][x].push_back(t); }
  vector<vector<int>> TclPre(m); for (size_t t = 0; t < m; t++) TclPre[T.Cl[t]].push_back(t);
  vector<int> tN[2], tWin[2], tSui[2];
  for (int c = 0; c < 2; c++) { tN[c].assign(m, 0); tWin[c].assign(m, 0); tSui[c].assign(m, 0);
    for (size_t t = 0; t < m; t++) for (int x : (c == 0 ? T.L[t] : T.Rr[t])) {
      if (x >= 0) tN[c][t]++; else if ((x == -1) == (c == 0)) tWin[c][t] = 1; else tSui[c][t]++; } }
  auto I = [&](size_t z, size_t t, int s) { return (z * m + t) * 2 + s; };
  for (size_t z = 0; z < N; z++) for (size_t t = 0; t < m; t++) for (int s = 0; s < 2; s++) {
    size_t i = I(z, t, s);
    if (!valid[s][z]) { st[i] = 3 << 6; continue; }
    bool canT = !chk[s][z];
    if (prom[s][z] || (canT && tWin[s][t])) { st[i] = 1 << 6; cur[i >> 6] |= 1ULL << (i & 63); continue; }
    int n = sOff[s][z + 1] - sOff[s][z];
    if (canT) n += tN[s][t];
    bool hasMove = n > 0 || (canT && tSui[s][t] > 0);
    if (n == 0) { if (hasMove || chk[s][z] || CONV == 'N') { st[i] = 2 << 6; cur[i >> 6] |= 1ULL << (i & 63); } else st[i] = 0; continue; }
    if (n > 63) { fprintf(stderr, "degree overflow\n"); exit(1); }
    st[i] = n;
  }
  for (bool any = true; any;) {
    any = false;
    for (size_t w = 0; w < cur.size(); w++) for (u64 b = cur[w]; b; b &= b - 1) {
      size_t i = w * 64 + __builtin_ctzll(b);
      int s = i & 1; size_t zt = i >> 1, z = zt / m, t = zt % m; int ps = 1 - s; uint8_t v = V(i);
      auto relax = [&](size_t j) {
        uint8_t x = st[j]; if ((x >> 6) != 0 || (x & 63) == 0) return;
        if (v == 2) { st[j] = 1 << 6; nxt[j >> 6] |= 1ULL << (j & 63); any = true; }
        else if ((x & 63) == 1) { st[j] = 2 << 6; nxt[j >> 6] |= 1ULL << (j & 63); any = true; }
        else st[j] = x - 1;
      };
      for (int k = pOff[ps][z]; k < pOff[ps][z + 1]; k++) for (int t0 : TclPre[t]) relax(I(pLst[ps][k], t0, ps));
      if (!hasEp[z])
        for (int k = cOff[z]; k < cOff[z + 1]; k++) { size_t z0 = cLst[k]; if (chk[ps][z0]) continue;
          for (int t0 : Tpred[ps][t]) relax(I(z0, t0, ps)); }
    }
    swap(cur, nxt); fill(nxt.begin(), nxt.end(), 0);
  }
}
// over + T, solved directly on the small product (over has positions omega=0, zero=1)
vector<uint8_t> solveOver(const TG& T) {
  TG O; O.m = 2; O.L = {{1}, {}}; O.Rr = {{0}, {}};
  size_t m = T.m, S = 2 * m * 2; vector<uint8_t> v(S, 0), c(S, 0);
  auto I = [&](size_t o, size_t t, int s) { return (o * m + t) * 2 + s; };
  // simple fixpoint (tiny)
  for (bool ch = true; ch;) { ch = false;
    for (size_t o = 0; o < 2; o++) for (size_t t = 0; t < m; t++) for (int s = 0; s < 2; s++) {
      size_t i = I(o, t, s); if (v[i]) continue;
      vector<size_t> opts; for (int x : (s == 0 ? O.L[o] : O.Rr[o])) opts.push_back(I(x, T.Cl[t], 1 - s));
      bool ownT = false; int sui = 0;
      for (int x : (s == 0 ? T.L[t] : T.Rr[t])) { if (x >= 0) opts.push_back(I(o, x, 1 - s)); else if ((x == -1) == (s == 0)) ownT = true; else sui++; }
      uint8_t nv = 0;
      if (ownT) nv = 1;
      else if (opts.empty()) nv = sui ? 2 : (CONV == 'N' ? 2 : 0);
      else { bool any = false, all = true; for (auto j : opts) { if (v[j] == 2) any = true; if (v[j] != 1) all = false; }
        if (any) nv = 1; else if (all) nv = 2; }
      if (nv) { v[i] = nv; ch = true; }
    } }
  return v;
}
int main(int argc, char** argv) {
  if (argc < 6) { fprintf(stderr, "usage\n"); return 1; }
  W = atoi(argv[1]); H = atoi(argv[2]); NSQ = W * H; CONV = argv[5][0];
  bool dump = argc > 6 && !strcmp(argv[6], "--dump-values");
  vector<Pl> roots; vector<string> rootNames; { ifstream f(argv[3]); string l; while (getline(f, l)) if (!l.empty() && l[0] != '#') { roots.push_back(parse(l)); rootNames.push_back(l); } }
  vector<TG> tests; { ifstream f(argv[4]); string l; while (getline(f, l)) if (!l.empty() && l[0] != '#') tests.push_back(parseT(l)); }
  build(roots);
  fprintf(stderr, "component nodes %zu, edges W %zu B %zu\n", nodes.size(), sLst[0].size(), sLst[1].size());
  // K55: root ids first, then free the hash map (it is not used after the build), to save memory on cyl:10x6
  vector<int> rootId; for (auto& r : roots) rootId.push_back(idx[key(r)]);
  { unordered_map<pair<u64, u64>, int, KH> e; idx.swap(e); }
  hasEp.resize(nodes.size()); for (size_t z = 0; z < nodes.size(); z++) hasEp[z] = nodes[z].ep >= 0;
  if (!dump) { vector<Pl> e; nodes.swap(e); }  // K55: memory on cyl:10x6
  const char* RS = "DWLX";
  for (auto& T : tests) {
    solveSum(T); vector<uint8_t> ov = solveOver(T);
    for (size_t r = 0; r < roots.size(); r++) for (int s = 0; s < 2; s++) {
      int z = rootId[r];
      uint8_t a = V(((size_t)z * T.m + 0) * 2 + s), b = ov[(0 * T.m + 0) * 2 + s];
      // print from White's view: W white wins, L black wins
      auto wv = [&](uint8_t x) { if (x == 0) return 'D'; if (x == 3) return 'X'; bool moverWins = x == 1; return ((s == 0) == moverWins) ? 'W' : 'L'; };
      printf("%s | %s | %c | Z %c | over %c | %s\n", T.name.c_str(), rootNames[r].c_str(), s ? 'b' : 'w', wv(a), wv(b), wv(a) == wv(b) ? "MATCH" : "DIFF");
    }
    if (dump) { // dump the T-component values of every node (for cross-checks): z t s val
      // every 97th node, both sides, as a position line "pieces stm ep | White-view result" (t = start of T)
      for (size_t z = 0; z < nodes.size(); z += 97) for (int s = 0; s < 2; s++) {
        uint8_t x = V(((size_t)z * T.m) * 2 + s); if (x == 3) continue;
        const Pl& p = nodes[z]; string str;
        auto sq = [&](int q) { return string(1, char('a' + F(q))) + char('1' + R(q)); };
        str += "K" + sq(p.wk) + " k" + sq(p.bk);
        for (u64 b = p.wp; b; b &= b - 1) str += " P" + sq(__builtin_ctzll(b));
        for (u64 b = p.bp; b; b &= b - 1) str += " p" + sq(__builtin_ctzll(b));
        str += s ? " b " : " w "; str += p.ep < 0 ? string("-") : sq(p.ep);
        char wv = x == 0 ? 'D' : (((s == 0) == (x == 1)) ? 'W' : 'L');
        printf("V %s | %c\n", str.c_str(), wv); } }
    fflush(stdout);
  }
  (void)RS;
  { struct rusage ru; getrusage(RUSAGE_SELF, &ru); fprintf(stderr, "K55 peak rss %ld bytes\n", (long)ru.ru_maxrss); }
}
