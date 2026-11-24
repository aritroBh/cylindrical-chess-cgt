// K59: vgsum59.cpp = the K57 referee's vgsum.cpp with memory-only changes (marked K59 MEM): 32-bit edge offsets,
// the forward edge list freed after the reverse lists are built, 32-bit token-game queue, optional --reserve capacity hint, optional --lowmem (moves regenerated
// for the reverse lists instead of stored). No change to the game logic.
// K57 referee: vgsum.cpp. Lines up to build() are copied unchanged from the K56 referee's vg.cpp
// (kings/delegate/out/K56/verify/src/vg.cpp, written from SPEC.md, independent of the K56/K57 investigators' pr56/pr57).
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <sys/resource.h>
using namespace std;

static int W, H, WRAP;
static const uint8_t NONE = 255;

struct Node { uint64_t wp, bp; uint8_t wk, bk, side, ep; };  // side 0 white, 1 black; ep square or NONE

static int sq(int f, int r) { return r * W + f; }
static int fileOf(int s) { return s % W; }
static int rankOf(int s) { return s / W; }
static int stepSq(int s, int df, int dr) {
  int f = fileOf(s) + df, r = rankOf(s) + dr;
  if (r < 0 || r >= H) return -1;
  if (WRAP) f = (f % W + W) % W; else if (f < 0 || f >= W) return -1;
  return sq(f, r);
}
static string sqName(int s) { string t; t += char('a' + fileOf(s)); t += to_string(rankOf(s) + 1); return t; }
static int parseSq(const char *p) { return sq(p[0] - 'a', atoi(p + 1) - 1); }

static uint64_t kingAtt[64], pawnAttBy[2][64];  // pawnAttBy[c][s]: squares a pawn of colour c on s attacks
static void initGeo() {
  for (int s = 0; s < W * H; s++) {
    kingAtt[s] = 0;
    for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
      if (!df && !dr) continue;
      int t = stepSq(s, df, dr); if (t >= 0 && t != s) kingAtt[s] |= 1ULL << t;
    }
    for (int c = 0; c < 2; c++) {
      pawnAttBy[c][s] = 0; int dr = c == 0 ? 1 : -1;
      for (int df = -1; df <= 1; df += 2) { int t = stepSq(s, df, dr); if (t >= 0) pawnAttBy[c][s] |= 1ULL << t; }
    }
  }
}
// is square s attacked by side c on the given board
static bool attacked(const Node &n, int s, int c) {
  int k = c == 0 ? n.wk : n.bk;
  if (kingAtt[k] >> s & 1) return true;
  uint64_t p = c == 0 ? n.wp : n.bp;
  while (p) { int t = __builtin_ctzll(p); p &= p - 1; if (pawnAttBy[c][t] >> s & 1) return true; }
  return false;
}
static bool inCheck(const Node &n) { int c = n.side; return attacked(n, c == 0 ? n.wk : n.bk, 1 - c); }

// generate legal successors; returns whether a legal promotion exists
static bool gen(const Node &n, vector<Node> &out, vector<string> *names = nullptr) {
  out.clear(); if (names) names->clear(); bool promo = false; int c = n.side;
  uint64_t own = c == 0 ? n.wp : n.bp, opp = c == 0 ? n.bp : n.wp;
  uint64_t occ = n.wp | n.bp | (1ULL << n.wk) | (1ULL << n.bk);
  auto push = [&](Node m, const string &nm) {
    m.side = 1 - c;
    int k = c == 0 ? m.wk : m.bk;
    if (attacked(m, k, 1 - c)) return;  // leaves own king attacked (includes adjacent kings)
    out.push_back(m); if (names) names->push_back(nm);
  };
  // king
  int k = c == 0 ? n.wk : n.bk;
  uint64_t ka = kingAtt[k];
  while (ka) {
    int t = __builtin_ctzll(ka); ka &= ka - 1;
    if (own >> t & 1) continue;
    if (t == (c == 0 ? n.bk : n.wk)) continue;
    Node m = n; m.ep = NONE;
    if (c == 0) { m.wk = t; m.bp &= ~(1ULL << t); } else { m.bk = t; m.wp &= ~(1ULL << t); }
    push(m, string(c == 0 ? "K" : "k") + sqName(k) + sqName(t));
  }
  // pawns
  int dr = c == 0 ? 1 : -1, last = c == 0 ? H - 1 : 0, start = c == 0 ? 1 : H - 2;
  uint64_t p = own;
  while (p) {
    int s = __builtin_ctzll(p); p &= p - 1;
    string pn = string(c == 0 ? "P" : "p") + sqName(s);
    auto mk = [&](int t, bool capt, int capSq, uint8_t ep) {
      Node m = n; m.ep = ep;
      uint64_t &mine = c == 0 ? m.wp : m.bp, &theirs = c == 0 ? m.bp : m.wp;
      mine &= ~(1ULL << s);
      if (capt) theirs &= ~(1ULL << capSq);
      if (rankOf(t) == last) {  // promotion: legal if own king safe afterwards (promoted piece irrelevant here)
        Node chk = m; int kk = c == 0 ? chk.wk : chk.bk;
        if (!attacked(chk, kk, 1 - c)) promo = true;
        return;
      }
      mine |= 1ULL << t;
      push(m, pn + sqName(t));
    };
    int t1 = stepSq(s, 0, dr);
    if (t1 >= 0 && !(occ >> t1 & 1)) {
      mk(t1, false, -1, NONE);
      if (rankOf(s) == start) {
        int t2 = stepSq(s, 0, 2 * dr);
        if (t2 >= 0 && !(occ >> t2 & 1)) mk(t2, false, -1, (uint8_t)t1);
      }
    }
    for (int df = -1; df <= 1; df += 2) {
      int t = stepSq(s, df, dr); if (t < 0) continue;
      if (opp >> t & 1) mk(t, true, t, NONE);
      else if (n.ep != NONE && t == n.ep) mk(t, true, stepSq(t, 0, -dr), NONE);
    }
  }
  return promo;
}

// ---------------- node store ----------------
static vector<Node> nodes;
static vector<uint32_t> tab; static uint64_t tabMask;
static uint64_t hnode(const Node &n) {
  uint64_t h = n.wp * 0x9E3779B97F4A7C15ULL ^ (n.bp + 0x632BE59BD9B4E019ULL) * 0xBF58476D1CE4E5B9ULL;
  h ^= ((uint64_t)n.wk << 24 | (uint64_t)n.bk << 16 | (uint64_t)n.side << 8 | n.ep) * 0x94D049BB133111EBULL;
  h ^= h >> 31; h *= 0xD6E8FEB86659FD93ULL; h ^= h >> 32; return h;
}
static bool eqn(const Node &a, const Node &b) { return a.wp == b.wp && a.bp == b.bp && a.wk == b.wk && a.bk == b.bk && a.side == b.side && a.ep == b.ep; }
static void grow() {
  uint64_t ns = tab.size() * 2; vector<uint32_t> nt(ns, 0xFFFFFFFFu); uint64_t nm = ns - 1;
  for (uint32_t i = 0; i < nodes.size(); i++) { uint64_t h = hnode(nodes[i]) & nm; while (nt[h] != 0xFFFFFFFFu) h = (h + 1) & nm; nt[h] = i; }
  tab.swap(nt); tabMask = nm;
}
static int64_t findNode(const Node &n) {
  uint64_t h = hnode(n) & tabMask;
  while (tab[h] != 0xFFFFFFFFu) { if (eqn(nodes[tab[h]], n)) return tab[h]; h = (h + 1) & tabMask; }
  return -1;
}
static uint32_t addNode(const Node &n) {
  if ((nodes.size() + 1) * 2 > tab.size()) grow();
  uint64_t h = hnode(n) & tabMask;
  while (tab[h] != 0xFFFFFFFFu) { if (eqn(nodes[tab[h]], n)) return tab[h]; h = (h + 1) & tabMask; }
  tab[h] = nodes.size(); nodes.push_back(n); return nodes.size() - 1;
}

static Node parsePos(const string &s) {
  Node n{0, 0, 0, 0, 0, NONE}; char buf[16]; const char *p = s.c_str(); int off;
  vector<string> tok;
  while (sscanf(p, "%15s%n", buf, &off) == 1) { tok.push_back(buf); p += off; }
  for (auto &t : tok) {
    if (t == "w") n.side = 0; else if (t == "b") n.side = 1; else if (t == "-") n.ep = NONE;
    else if (t[0] == 'K') n.wk = parseSq(t.c_str() + 1); else if (t[0] == 'k') n.bk = parseSq(t.c_str() + 1);
    else if (t[0] == 'P') n.wp |= 1ULL << parseSq(t.c_str() + 1); else if (t[0] == 'p') n.bp |= 1ULL << parseSq(t.c_str() + 1);
    else if (t[0] >= 'a' && t[0] <= 'j') n.ep = parseSq(t.c_str());
  }
  return n;
}
static string posStr(const Node &n) {
  string s = "K" + sqName(n.wk) + " k" + sqName(n.bk);
  for (int i = 0; i < W * H; i++) if (n.wp >> i & 1) s += " P" + sqName(i);
  for (int i = 0; i < W * H; i++) if (n.bp >> i & 1) s += " p" + sqName(i);
  s += n.side == 0 ? " w " : " b "; s += n.ep == NONE ? "-" : sqName(n.ep); return s;
}

// graph
static vector<uint32_t> off; static vector<uint32_t> succ; static vector<int32_t> passSucc;  // K59 MEM: off 32-bit
static vector<uint8_t> promoF, checkF;
static vector<uint32_t> roff; static vector<uint32_t> rsucc;  // reverse move edges (K59 MEM: 32-bit offsets)
static vector<uint32_t> proff; static vector<uint32_t> prsucc;  // reverse pass edges (K59 MEM: 32-bit offsets)
static uint64_t NEDGES = 0;
static uint64_t RES_N = 0, RES_E = 0; static int LOWMEM = 0;  // K59 MEM: --lowmem  // K59 MEM: optional --reserve <nodes> <edges> (capacity hint only)  // K59 MEM: edge count kept after succ is freed

static long peakMB() { struct rusage ru; getrusage(RUSAGE_SELF, &ru); return ru.ru_maxrss / (1024 * 1024); }

static void build(const vector<Node> &roots) {
  if (RES_N) { nodes.reserve(RES_N); off.reserve(RES_N + 1); passSucc.reserve(RES_N); promoF.reserve(RES_N); checkF.reserve(RES_N); }  // K59 MEM
  if (RES_E) succ.reserve(RES_E);  // K59 MEM
  tab.assign(1 << 20, 0xFFFFFFFFu); tabMask = tab.size() - 1;
  for (auto &r : roots) addNode(r);
  off.push_back(0); vector<Node> out;
  for (uint64_t i = 0; i < nodes.size(); i++) {
    Node n = nodes[i];
    bool pr = gen(n, out); promoF.push_back(pr); bool ch = inCheck(n); checkF.push_back(ch);
    if (LOWMEM) { for (auto &m : out) addNode(m); NEDGES += out.size(); }  // K59 MEM: --lowmem stores no forward edges
    else { for (auto &m : out) succ.push_back(addNode(m)); NEDGES = succ.size(); }
    if (NEDGES > 0xFFFFFFF0ull) { fprintf(stderr, "too many edges for 32-bit offsets\n"); exit(2); }  // K59 MEM
    off.push_back(NEDGES);
    if (!ch) { Node m = n; m.side = 1 - n.side; m.ep = NONE; passSucc.push_back(addNode(m)); } else passSucc.push_back(-1);
  }
  uint64_t N = nodes.size();
  roff.assign(N + 1, 0);
  if (LOWMEM) {  // K59 MEM: regenerate each node's moves (same generator, same order) instead of reading succ
    for (uint64_t u = 0; u < N; u++) { gen(nodes[u], out); for (auto &m : out) { int64_t v = findNode(m); if (v < 0) { fprintf(stderr, "lowmem: child missing\n"); exit(3); } roff[v + 1]++; } }
  } else for (auto v : succ) roff[v + 1]++;
  for (uint64_t i = 0; i < N; i++) roff[i + 1] += roff[i];
  rsucc.resize(NEDGES); { vector<uint32_t> pos(roff.begin(), roff.end() - 1);  // K59 MEM
    if (LOWMEM) { for (uint64_t u = 0; u < N; u++) { gen(nodes[u], out); for (auto &m : out) rsucc[pos[findNode(m)]++] = u; } }
    else for (uint64_t u = 0; u < N; u++) for (uint64_t e = off[u]; e < off[u + 1]; e++) rsucc[pos[succ[e]]++] = u; }
  proff.assign(N + 1, 0);
  for (uint64_t u = 0; u < N; u++) if (passSucc[u] >= 0) proff[passSucc[u] + 1]++;
  for (uint64_t i = 0; i < N; i++) proff[i + 1] += proff[i];
  prsucc.resize(proff[N]); { vector<uint32_t> pos(proff.begin(), proff.end() - 1);  // K59 MEM
    for (uint64_t u = 0; u < N; u++) if (passSucc[u] >= 0) prsucc[pos[passSucc[u]]++] = u; }
  vector<uint32_t>().swap(succ);  // K59 MEM: succ is not used after this point
}


// ===================== K57 referee additions (below this line) =====================
// (1) tok(X, sumrule): Y's winning set in G (+) (k tokens of X), k in {0,1}, layer l = tokens left.
//     sumrule = 1: a side with no legal move and no token loses (Definition 1.3); = 0: stalemate draws (P).
//     With X = Black, k = 1, sumrule = 1, layer 1 at x is exactly r(x (+) (-1), White to move) = W.
// (2) sum(T): r(G (+) T) for a finite D-game T read from a file (Definition 1.3 with K40's convention:
//     promotion = win for the promoter, a side in check may not move in T, a T-move clears the e.p. right,
//     a side with no move anywhere loses, a move to a terminal ends the play, infinite play draws).
static vector<uint8_t> tok(int X, bool sumrule) {
  uint64_t N = nodes.size(); int Y = 1 - X;
  vector<uint8_t> win(N * 2, 0), cnt(N * 2, 0); vector<uint32_t> q;  // K59 MEM: q 32-bit (2N < 2^32)
  for (int l = 0; l < 2; l++) for (uint64_t n = 0; n < N; n++) {
    uint64_t g = l * N + n; const Node &nd = nodes[n];
    if (nd.side == Y) { if (promoF[n]) { win[g] = 1; q.push_back(g); } }
    else {
      bool passOK = passSucc[n] >= 0 && l == 1;
      int c = (int)(off[n + 1] - off[n]) + (passOK ? 1 : 0);
      if (promoF[n]) cnt[g] = 255;
      else if (c == 0) { if (checkF[n] || sumrule) { win[g] = 1; q.push_back(g); } else cnt[g] = 255; }
      else cnt[g] = c;
    }
  }
  auto reach = [&](uint64_t u) {
    if (win[u]) return;
    uint64_t n = u % N;
    if (nodes[n].side == Y) { win[u] = 1; q.push_back(u); }
    else if (cnt[u] != 255) { if (--cnt[u] == 0) { win[u] = 1; q.push_back(u); } }
  };
  for (uint64_t h = 0; h < q.size(); h++) {
    uint64_t g = q[h], v = g % N, l = g / N;
    for (uint64_t e = roff[v]; e < roff[v + 1]; e++) reach(l * N + rsucc[e]);
    if (l == 0) for (uint64_t e = proff[v]; e < proff[v + 1]; e++) { uint64_t u = prsucc[e]; if (nodes[u].side == X) reach(N + u); }
  }
  return win;
}

// D-game T: positions 0..k-1; opt[s][t] = list of targets, -1 = White-win terminal, -2 = Black-win terminal.
struct DG { string name; int k; vector<vector<int>> opt[2]; };
static vector<DG> readT(const char *fn) {
  vector<DG> out; FILE *f = fopen(fn, "r"); char line[4096];
  while (fgets(line, sizeof line, f)) {
    string s(line); while (!s.empty() && (s.back() == '\n' || s.back() == '\r')) s.pop_back();
    if (s.empty() || s[0] == '#') continue;
    // format: name|k|L0/R0;L1/R1;...  options comma separated, W = White-win terminal, B = Black-win terminal, empty allowed
    size_t a = s.find('|'), b = s.find('|', a + 1);
    DG d; d.name = s.substr(0, a); d.k = atoi(s.substr(a + 1, b - a - 1).c_str());
    d.opt[0].assign(d.k, {}); d.opt[1].assign(d.k, {});
    string rest = s.substr(b + 1); int t = 0; size_t p = 0;
    while (t < d.k) {
      size_t e = rest.find(';', p); string part = rest.substr(p, e == string::npos ? string::npos : e - p);
      size_t sl = part.find('/');
      for (int side = 0; side < 2; side++) {
        string lst = side == 0 ? part.substr(0, sl) : part.substr(sl + 1); size_t q = 0;
        while (q < lst.size()) {
          size_t c = lst.find(',', q); string tk = lst.substr(q, c == string::npos ? string::npos : c - q);
          if (!tk.empty()) d.opt[side][t].push_back(tk == "W" ? -1 : tk == "B" ? -2 : atoi(tk.c_str()));
          if (c == string::npos) break; q = c + 1;
        }
      }
      t++; if (e == string::npos) break; p = e + 1;
    }
    out.push_back(d);
  }
  fclose(f); return out;
}

// returns value per state (n * k + t): 'W', 'L', 'D'
static vector<char> sumSolve(const DG &T) {
  uint64_t N = nodes.size(); int k = T.k; uint64_t S = N * k;
  vector<vector<int>> rT[2]; rT[0].assign(k, {}); rT[1].assign(k, {});  // rT[s][t'] = t with t' in opt[s][t]
  for (int s = 0; s < 2; s++) for (int t = 0; t < k; t++) for (int o : T.opt[s][t]) if (o >= 0) rT[s][o].push_back(t);
  vector<char> val(S, 'D');
  for (int Y = 0; Y < 2; Y++) {  // Y = colour whose win set is computed
    int X = 1 - Y; int ytm = Y == 0 ? -1 : -2, xtm = Y == 0 ? -2 : -1;
    vector<uint8_t> win(S, 0); vector<uint16_t> cnt(S, 0); vector<uint64_t> q;
    const uint16_t NEVER = 65535;
    for (uint64_t n = 0; n < N; n++) for (int t = 0; t < k; t++) {
      uint64_t g = n * k + t; int s = nodes[n].side;
      bool tOK = !checkF[n];
      if (s == Y) {
        bool w = promoF[n];
        if (tOK) for (int o : T.opt[s][t]) if (o == ytm) w = true;
        if (w) { win[g] = 1; q.push_back(g); }
      } else {
        bool never = promoF[n]; int c = (int)(off[n + 1] - off[n]);
        if (tOK) for (int o : T.opt[s][t]) { if (o == xtm) never = true; else if (o >= 0) c++; }
        if (never) cnt[g] = NEVER;
        else if (c == 0) { win[g] = 1; q.push_back(g); }  // no move (or only moves to Y's terminal): Y wins
        else cnt[g] = c;
      }
    }
    auto reach = [&](uint64_t u) {
      if (win[u]) return;
      if (nodes[u / k].side == Y) { win[u] = 1; q.push_back(u); }
      else if (cnt[u] != NEVER) { if (--cnt[u] == 0) { win[u] = 1; q.push_back(u); } }
    };
    for (uint64_t h = 0; h < q.size(); h++) {
      uint64_t g = q[h], v = g / k; int t = g % k;
      for (uint64_t e = roff[v]; e < roff[v + 1]; e++) reach((uint64_t)rsucc[e] * k + t);
      int ps = 1 - nodes[v].side;  // side that made the T-move into (v, t)
      for (uint64_t e = proff[v]; e < proff[v + 1]; e++) {
        uint64_t u = prsucc[e]; if (nodes[u].side != ps) continue;
        for (int t0 : rT[ps][t]) reach(u * k + t0);
      }
    }
    for (uint64_t g = 0; g < S; g++) if (win[g]) val[g] = Y == 0 ? 'W' : 'L';
  }
  return val;
}

int main(int argc, char **argv) {
  string root, shuttle, tfile; vector<string> queries;
  for (int i = 1; i < argc; i++) {
    string a = argv[i];
    if (a == "--board") { char kind[8]; sscanf(argv[++i], "%7[a-z]:%dx%d", kind, &W, &H); WRAP = !strcmp(kind, "cyl"); }
    else if (a == "--root") root = argv[++i];
    else if (a == "--shuttle") shuttle = argv[++i];
    else if (a == "--query") queries.push_back(argv[++i]);
    else if (a == "--tests") tfile = argv[++i];
    else if (a == "--lowmem") LOWMEM = 1;  // K59 MEM
    else if (a == "--reserve") { RES_N = atoll(argv[++i]); RES_E = atoll(argv[++i]); }  // K59 MEM
  }
  initGeo();
  Node A = parsePos(root + " b -"); Node B = A; B.bk = parseSq(shuttle.c_str());
  vector<Node> roots; for (Node r : {A, B}) for (int s = 0; s < 2; s++) { r.side = s; roots.push_back(r); }
  build(roots);
  uint64_t N = nodes.size();
  printf("nodes %llu edges %llu peak %ld MB\n", (unsigned long long)N, (unsigned long long)NEDGES, peakMB());
  vector<uint8_t> pB = tok(1, false), pW = tok(0, false);  // P (stalemate draw), layer 0
  vector<uint8_t> sB = tok(1, true);                       // sum rule, X = Black, 1 token: (B1)
  vector<uint8_t> pB1 = tok(1, false);                     // pass game, 1 Black pass, stalemate draw
  auto idx = [&](const Node &n) { return findNode(n); };
  auto P = [&](const Node &n) -> char { int64_t i = idx(n); if (i < 0) return '?'; return pB[i] ? 'W' : pW[i] ? 'L' : 'D'; };
  // labelled states for the sum test: roots, q's (from the P freezes), positions after Black's non-shuttle root moves
  vector<pair<string, int64_t>> lab;
  vector<Node> out; vector<string> names;
  for (int ri = 0; ri < 4; ri++) {
    Node r = roots[ri]; gen(r, out, &names);
    string rn = string(ri < 2 ? "rootA" : "rootB") + (r.side ? "_b" : "_w");
    lab.push_back({rn, idx(r)});
    printf("%s %s P=%c moves=%zu promo=%d check=%d\n", rn.c_str(), posStr(r).c_str(), P(r), out.size(), (int)promoF[idx(r)], (int)checkF[idx(r)]);
    for (size_t j = 0; j < out.size(); j++) {
      Node x = out[j]; int64_t xi = idx(x);
      if (r.side == 1) {
        bool sh = x.wp == r.wp && x.bp == r.bp && (x.bk == A.bk || x.bk == B.bk);
        if (sh) { printf("   %-8s shuttle -> %s\n", names[j].c_str(), posStr(x).c_str()); continue; }
        printf("   %-8s -> %s  P(after)=%c  B1(sum rule, -1)=%s  [pass game 1 pass, stalemate draw: %s]  check=%d\n", names[j].c_str(),
               posStr(x).c_str(), P(x), sB[N + xi] ? "W" : "not W", pB1[N + xi] ? "W" : "not W", (int)checkF[xi]);
        lab.push_back({rn + "_" + names[j], xi});
      } else {
        char v = P(x);
        printf("   %-8s -> %s  P(after)=%c%s\n", names[j].c_str(), posStr(x).c_str(), v, v != 'L' ? "  FREEZE" : "");
        if (v != 'L') {
          Node qw = x; qw.side = 0; qw.ep = NONE;
          lab.push_back({rn + "_q_" + names[j] + "_b", xi});
          lab.push_back({rn + "_q_" + names[j] + "_w", idx(qw)});
          if (x.ep != NONE) { Node qb = x; qb.ep = NONE; lab.push_back({rn + "_q_" + names[j] + "_bnoep", idx(qb)}); }
        }
      }
    }
  }
  for (auto &qs : queries) {
    Node n = parsePos(qs); int64_t i = idx(n);
    if (i < 0) { printf("query %s : not reachable\n", qs.c_str()); continue; }
    printf("query %s : P=%c  sum-rule with one Black token: %s (layer1) / %s (layer0)\n", qs.c_str(), P(n), sB[N + i] ? "W" : "not W",
           sB[i] ? "W" : "not W");
  }
  printf("peak %ld MB after token games\n", peakMB());
  if (!tfile.empty()) {
    vector<DG> Ts = readT(tfile.c_str());
    for (auto &T : Ts) {
      vector<char> v = sumSolve(T);
      for (auto &l : lab) {
        if (l.second < 0) { printf("SUM %s %s missing\n", T.name.c_str(), l.first.c_str()); continue; }
        printf("SUM %s %s %d ", T.name.c_str(), l.first.c_str(), (int)nodes[l.second].side);
        for (int t = 0; t < T.k; t++) putchar(v[l.second * T.k + t]);
        putchar('\n');
      }
      fflush(stdout);
    }
    printf("peak %ld MB after sums\n", peakMB());
  }
}
