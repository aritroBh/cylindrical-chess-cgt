// K56 referee: one-sided pass games of P for an over group, written from kings/SPEC.md and
// LOOPY Definitions 1.2, 1.5, 4.8 and K56's Definition 1 (PROOF.md). No code from pr56.cpp.
//
// Reading of a pass (the referee's): a pass of X is a move elsewhere (Definition 1.3 with K40's
// convention): allowed only when X is not in check; the board stays; the move goes to the other side;
// any e.p. right is lost. Only X passes. In P a legal promotion wins at once for the promoter,
// a side in check without a move loses, a side not in check without a move (and no pass) draws,
// infinite play draws.
//
// Game P^X_1: states (node, passes left in {0,1}); P^X_0 = layer 0; P^X_inf: one layer.
// Y's winning set = least fixed point (retrograde with counters).
//
// usage: vg --board cyl:8x6 --root "Kf5 kd4 Pb2 ..." --shuttle d5 [--sample N --seed S --samplefile F]
//           [--query "pos w -"]...
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
static vector<uint64_t> off; static vector<uint32_t> succ; static vector<int32_t> passSucc;
static vector<uint8_t> promoF, checkF;
static vector<uint64_t> roff; static vector<uint32_t> rsucc;  // reverse move edges
static vector<uint64_t> proff; static vector<uint32_t> prsucc;  // reverse pass edges

static long peakMB() { struct rusage ru; getrusage(RUSAGE_SELF, &ru); return ru.ru_maxrss / (1024 * 1024); }

static void build(const vector<Node> &roots) {
  tab.assign(1 << 20, 0xFFFFFFFFu); tabMask = tab.size() - 1;
  for (auto &r : roots) addNode(r);
  off.push_back(0); vector<Node> out;
  for (uint64_t i = 0; i < nodes.size(); i++) {
    Node n = nodes[i];
    bool pr = gen(n, out); promoF.push_back(pr); bool ch = inCheck(n); checkF.push_back(ch);
    for (auto &m : out) succ.push_back(addNode(m));
    off.push_back(succ.size());
    if (!ch) { Node m = n; m.side = 1 - n.side; m.ep = NONE; passSucc.push_back(addNode(m)); } else passSucc.push_back(-1);
  }
  uint64_t N = nodes.size();
  roff.assign(N + 1, 0);
  for (auto v : succ) roff[v + 1]++;
  for (uint64_t i = 0; i < N; i++) roff[i + 1] += roff[i];
  rsucc.resize(succ.size()); { vector<uint64_t> pos(roff.begin(), roff.end() - 1);
    for (uint64_t u = 0; u < N; u++) for (uint64_t e = off[u]; e < off[u + 1]; e++) rsucc[pos[succ[e]]++] = u; }
  proff.assign(N + 1, 0);
  for (uint64_t u = 0; u < N; u++) if (passSucc[u] >= 0) proff[passSucc[u] + 1]++;
  for (uint64_t i = 0; i < N; i++) proff[i + 1] += proff[i];
  prsucc.resize(proff[N]); { vector<uint64_t> pos(proff.begin(), proff.end() - 1);
    for (uint64_t u = 0; u < N; u++) if (passSucc[u] >= 0) prsucc[pos[passSucc[u]]++] = u; }
}

// Y's winning set in P^X_K. K = 1: two layers, index l*N + n (l = passes left); K = -1: unlimited (one layer).
static vector<uint8_t> solve(int X, int K) {
  uint64_t N = nodes.size(); int L = K == 1 ? 2 : 1; int Y = 1 - X;
  vector<uint8_t> win(N * L, 0), cnt(N * L, 0); vector<uint64_t> q; q.reserve(1 << 20);
  for (int l = 0; l < L; l++) for (uint64_t n = 0; n < N; n++) {
    uint64_t g = l * N + n; const Node &nd = nodes[n];
    if (nd.side == Y) { if (promoF[n]) { win[g] = 1; q.push_back(g); } }
    else {
      bool passOK = passSucc[n] >= 0 && (K == -1 || l == 1);
      int c = (int)(off[n + 1] - off[n]) + (passOK ? 1 : 0);
      if (promoF[n]) cnt[g] = 255;  // X promotes: never a Y win
      else if (c == 0) { if (checkF[n]) { win[g] = 1; q.push_back(g); } else cnt[g] = 255; /* stalemate: draw */ }
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
    // pass predecessors: u with side X, passSucc[u] = v; pass from layer l+1 (K=1) or same layer (inf)
    uint64_t lp; if (K == -1) lp = 0; else if (l == 0 && L == 2) lp = 1; else continue;
    for (uint64_t e = proff[v]; e < proff[v + 1]; e++) { uint64_t u = prsucc[e]; if (nodes[u].side == X) reach(lp * N + u); }
  }
  return win;
}

int main(int argc, char **argv) {
  string root, shuttle, sampleFile; int nsample = 0; unsigned seed = 1; vector<string> queries;
  for (int i = 1; i < argc; i++) {
    string a = argv[i];
    if (a == "--board") { char kind[8]; sscanf(argv[++i], "%7[a-z]:%dx%d", kind, &W, &H); WRAP = !strcmp(kind, "cyl"); }
    else if (a == "--root") root = argv[++i];
    else if (a == "--shuttle") shuttle = argv[++i];
    else if (a == "--sample") nsample = atoi(argv[++i]);
    else if (a == "--seed") seed = atoi(argv[++i]);
    else if (a == "--samplefile") sampleFile = argv[++i];
    else if (a == "--query") queries.push_back(argv[++i]);
  }
  initGeo();
  Node A = parsePos(root + " b -"); Node B = A; B.bk = parseSq(shuttle.c_str());
  vector<Node> roots; for (Node r : {A, B}) for (int s = 0; s < 2; s++) { r.side = s; roots.push_back(r); }
  build(roots);
  uint64_t N = nodes.size();
  printf("board %s%dx%d root %s shuttle %s: %llu nodes, %llu edges, peak %ld MB after build\n", WRAP ? "cyl:" : "flat:", W, H,
         root.c_str(), shuttle.c_str(), (unsigned long long)N, (unsigned long long)succ.size(), peakMB());
  // Att^B_k : White's winning set with Black passing (X = Black); Att^W_k : Black's (X = White)
  vector<uint8_t> aB1 = solve(1, 1), aBi = solve(1, -1), aW1 = solve(0, 1), aWi = solve(0, -1);
  printf("peak %ld MB after solving\n", peakMB());
  auto get = [&](const vector<uint8_t> &a, const Node &n, int l) -> int {
    int64_t i = findNode(n); if (i < 0) return -1; return a[l * N + i];
  };
  auto pval = [&](const Node &n) -> char { int w = get(aB1, n, 0), b = get(aW1, n, 0); if (w < 0) return '?'; return w ? 'W' : b ? 'L' : 'D'; };
  // validation sample (P values, no passes)
  if (nsample > 0) {
    FILE *f = fopen(sampleFile.c_str(), "w"); srand(seed);
    for (int i = 0; i < nsample; i++) {
      uint64_t n = ((uint64_t)rand() * 2654435761ULL + rand()) % N;
      fprintf(f, "%s | %c\n", posStr(nodes[n]).c_str(), aB1[n] ? 'W' : aW1[n] ? 'L' : 'D');
    }
    fclose(f);
  }
  auto yn = [](int v) { return v < 0 ? "?" : v ? "yes" : "no"; };
  vector<Node> out; vector<string> names;
  for (int ri = 0; ri < 4; ri++) {
    Node r = roots[ri]; gen(r, out, &names);
    printf("root %s (P value %c): %zu moves\n", posStr(r).c_str(), pval(r), out.size());
    for (size_t j = 0; j < out.size(); j++) {
      Node x = out[j]; Node xp = x; xp.side = r.side; xp.ep = NONE;  // x, then a pass of the side to move in x
      bool chk = inCheck(x);
      if (r.side == 1) {  // Black at a root; X = Black
        bool sh = x.bk != r.bk && x.wp == r.wp && x.bp == r.bp && (x.bk == A.bk || x.bk == B.bk);
        if (sh) { printf("   %-8s shuttle\n", names[j].c_str()); continue; }
        printf("   %-8s Att^B_0 %s  Att^B_1 %s  Att^B_inf %s  | N1 %s  V1 %s\n", names[j].c_str(), yn(get(aB1, x, 0)),
               yn(get(aB1, x, 1)), yn(get(aBi, x, 0)), yn(get(aB1, x, 1)), chk ? "no(White in check)" : yn(get(aB1, xp, 1)));
      } else {  // White at a root; X = White
        int l0 = get(aW1, x, 0);
        if (!l0) {
          Node qw = x; qw.side = 0; qw.ep = NONE;
          printf("   %-8s freeze candidate: q Black-to-move all moves lose (Att^B_0) %s, q White-to-move all lose (Att^W_0) %s%s\n",
                 names[j].c_str(), yn(get(aB1, x, 0)), chk ? "illegal(check)" : yn(get(aW1, qw, 0)), "");
          continue;
        }
        printf("   %-8s Att^W_0 %s  Att^W_1 %s  Att^W_inf %s  | Ninf %s  V0 %s\n", names[j].c_str(), yn(l0), yn(get(aW1, x, 1)),
               yn(get(aWi, x, 0)), yn(get(aWi, x, 0)), chk ? "no(Black in check)" : yn(get(aW1, xp, 0)));
      }
    }
  }
  for (auto &qs : queries) {
    Node n = parsePos(qs);
    printf("query %s : P %c  Att^B_0 %s Att^B_1 %s Att^B_inf %s  Att^W_0 %s Att^W_1 %s Att^W_inf %s\n", qs.c_str(), pval(n),
           yn(get(aB1, n, 0)), yn(get(aB1, n, 1)), yn(get(aBi, n, 0)), yn(get(aW1, n, 0)), yn(get(aW1, n, 1)), yn(get(aWi, n, 0)));
  }
  printf("peak %ld MB\n", peakMB());
}
