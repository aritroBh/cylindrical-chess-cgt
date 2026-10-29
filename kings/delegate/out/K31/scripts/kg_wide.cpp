// kg.cpp  (K20)  local king-fight games of a king group, D-semantics, signature battery.
//
// Local game LK(Z): board cyl:WxH or flat:WxH. Position = (alive pawn set, white king, black king).
// Pawns never move (frozen/blocked); only kings move; a king may capture an enemy pawn.
// Decisive events end the (sub)game: a king capture that leaves a passed pawn for exactly one side is
// a terminal for that side (+ for White, - for Black). Passed = no enemy pawn on the same or an adjacent
// file ahead (cylinder: cyclic adjacency); no e.p. is possible (no pawn ever moves).
// A player with no legal move loses (normal play).  Sortie: free (whole board) or box (--margin m).
//
// For every pawn configuration and EVERY legal king placement (root) the program computes the outcome
// pair (White to move, Black to move) of  G (+) K  for a battery of small context games K (short and
// loopy), where (+) is the D-sum: a move to a terminal in either coordinate ends the whole play, a
// player with no move in any coordinate loses, infinite play is a draw.  The battery signature of a root
// is compared with the signature of reference games (0, *, integers, on, off, dud, over, under, ...).
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <set>
#include <string>
#include <vector>
using namespace std;
typedef unsigned __int128 u64;

// ---------------------------------------------------------------- generic D-game graphs
struct Graph {
  int n = 0;
  vector<vector<int>> opt[2];  // opt[c][x] : >=0 node, -1 = plus terminal, -2 = minus terminal
  // derived
  vector<int> roff[2], rtgt[2];
  vector<int> nplus[2], nminus[2], deg[2];
  void init(int nn) { n = nn; for (int c = 0; c < 2; c++) opt[c].assign(n, {}); }
  void finish() {
    for (int c = 0; c < 2; c++) {
      vector<int> cntr(n + 1, 0);
      nplus[c].assign(n, 0); nminus[c].assign(n, 0); deg[c].assign(n, 0);
      for (int x = 0; x < n; x++) {
        auto& o = opt[c][x];
        sort(o.begin(), o.end()); o.erase(unique(o.begin(), o.end()), o.end());
        deg[c][x] = (int)o.size();
        for (int t : o) { if (t == -1) nplus[c][x]++; else if (t == -2) nminus[c][x]++; else cntr[t + 1]++; }
      }
      roff[c].assign(n + 1, 0);
      for (int i = 0; i < n; i++) roff[c][i + 1] = roff[c][i] + cntr[i + 1];
      rtgt[c].assign(roff[c][n], 0);
      vector<int> pos(roff[c].begin(), roff[c].end() - 1);
      for (int x = 0; x < n; x++) for (int t : opt[c][x]) if (t >= 0) rtgt[c][pos[t]++] = x;
    }
  }
};

// retrograde on the product G x K. won[state] : player p (0 = White/+, 1 = Black/-) forces a win.
static void retro(const Graph& G, const Graph& K, int p, vector<char>& won, vector<int>& cnt, vector<int>& q) {
  const int n = G.n, m = K.n;
  size_t S = (size_t)n * m * 2;
  won.assign(S, 0); cnt.assign(S, 0); q.clear();
  int twIsPlus = (p == 0);  // p wins by reaching plus terminal if p==0
  for (int x = 0; x < n; x++) for (int k = 0; k < m; k++) for (int s = 0; s < 2; s++) {
    size_t id = ((size_t)x * m + k) * 2 + s;
    int ntw = twIsPlus ? G.nplus[s][x] + K.nplus[s][k] : G.nminus[s][x] + K.nminus[s][k];
    int nop = G.deg[s][x] + K.deg[s][k];
    if (s == p) { if (ntw > 0) { won[id] = 1; q.push_back((int)id); } }
    else { cnt[id] = nop - ntw; if (cnt[id] == 0) { won[id] = 1; q.push_back((int)id); } }
  }
  for (size_t qi = 0; qi < q.size(); qi++) {
    size_t y = q[qi];
    int sp = (int)(y & 1);   // mover at y
    int s = 1 - sp;          // mover at predecessors
    size_t xk = y >> 1;
    int x2 = (int)(xk / m), k2 = (int)(xk % m);
    auto visit = [&](size_t ps) {
      if (won[ps]) return;
      if (s == p) { won[ps] = 1; q.push_back((int)ps); }
      else if (--cnt[ps] == 0) { won[ps] = 1; q.push_back((int)ps); }
    };
    for (int e = G.roff[s][x2]; e < G.roff[s][x2 + 1]; e++) { int x = G.rtgt[s][e]; visit(((size_t)x * m + k2) * 2 + s); }
    for (int e = K.roff[s][k2]; e < K.roff[s][k2 + 1]; e++) { int k = K.rtgt[s][e]; visit(((size_t)x2 * m + k) * 2 + s); }
  }
}

// outcome codes from White's view: 0 = W, 1 = D, 2 = L ; res[2*x+s] for K root = node 0
static void outcomes(const Graph& G, const Graph& K, vector<uint8_t>& res) {
  vector<char> w0, w1; vector<int> cnt, q;
  retro(G, K, 0, w0, cnt, q);
  retro(G, K, 1, w1, cnt, q);
  res.assign((size_t)G.n * 2, 1);
  for (int x = 0; x < G.n; x++) for (int s = 0; s < 2; s++) {
    size_t id = ((size_t)x * K.n + 0) * 2 + s;
    res[2 * x + s] = w0[id] ? 0 : (w1[id] ? 2 : 1);
  }
}

// ---------------------------------------------------------------- small reference / context games
typedef vector<pair<vector<int>, vector<int>>> Nodes;
static Graph mk(const Nodes& nd) {
  Graph g; g.init((int)nd.size());
  for (int i = 0; i < (int)nd.size(); i++) { g.opt[0][i] = nd[i].first; g.opt[1][i] = nd[i].second; }
  g.finish(); return g;
}
struct Named { string name; Graph g; };
static vector<Named> make_contexts() {
  vector<Named> v;
  auto add = [&](string nm, Nodes nd) { v.push_back({nm, mk(nd)}); };
  const int P = -1, M = -2;
  add("0", {{{}, {}}});
  add("*", {{{1}, {1}}, {{}, {}}});
  for (int n = 1; n <= 3; n++) {
    Nodes a, b;
    for (int i = 0; i <= n; i++) { a.push_back({i < n ? vector<int>{i + 1} : vector<int>{}, {}}); b.push_back({{}, i < n ? vector<int>{i + 1} : vector<int>{}}); }
    add("+" + to_string(n), a); add("-" + to_string(n), b);
  }
  add("1/2", {{{1}, {2}}, {{}, {}}, {{1}, {}}});
  add("-1/2", {{{2}, {1}}, {{}, {}}, {{}, {1}}});
  add("up", {{{1}, {2}}, {{}, {}}, {{1}, {1}}});
  add("down", {{{2}, {1}}, {{}, {}}, {{1}, {1}}});
  add("up*", {{{1, 2}, {1}}, {{}, {}}, {{1}, {1}}});
  add("down*", {{{1}, {1, 2}}, {{}, {}}, {{1}, {1}}});
  add("*2", {{{1, 2}, {1, 2}}, {{}, {}}, {{1}, {1}}});
  add("on", {{{0}, {}}});
  add("off", {{{}, {0}}});
  add("dud", {{{0}, {0}}});
  add("over", {{{1}, {0}}, {{}, {}}});
  add("under", {{{0}, {1}}, {{}, {}}});
  add("tis", {{{1}, {}}, {{}, {0}}});
  add("tisn", {{{}, {1}}, {{0}, {}}});
  add("{+|}", {{{P}, {}}});
  add("{|-}", {{{}, {M}}});
  add("{+|-}", {{{P}, {M}}});
  add("{+|0}", {{{P}, {1}}, {{}, {}}});
  add("{0|-}", {{{1}, {M}}, {{}, {}}});
  add("{1|0}", {{{1}, {2}}, {{2}, {}}, {{}, {}}});
  add("{0|-1}", {{{2}, {1}}, {{}, {2}}, {{}, {}}});
  add("{2|0}", {{{1}, {3}}, {{2}, {}}, {{3}, {}}, {{}, {}}});
  add("{0|-2}", {{{3}, {1}}, {{}, {2}}, {{}, {3}}, {{}, {}}});
  add("{+|on}", {{{P}, {1}}, {{1}, {}}});    // White threat; Black may move to on
  add("{off|-}", {{{1}, {M}}, {{}, {1}}});
  add("{on|off}", {{{1}, {2}}, {{1}, {}}, {{}, {2}}});
  return v;
}

// ---------------------------------------------------------------- board and local game
struct Board {
  int W, H, wrap, N;
  vector<vector<int>> kadj;      // king neighbours
  vector<vector<char>> adj;      // adjacent or equal
  int nb(int f, int d) const { int g = f + d; if (wrap) return ((g % W) + W) % W; return (g < 0 || g >= W) ? -1 : g; }
  void init(int w, int h, int wr) {
    W = w; H = h; wrap = wr; N = w * h;
    kadj.assign(N, {}); adj.assign(N, vector<char>(N, 0));
    for (int s = 0; s < N; s++) {
      int f = s % W, r = s / W;
      for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
        if (!df && !dr) continue;
        int g = nb(f, df), q = r + dr;
        if (g < 0 || q < 0 || q >= H) continue;
        int t = q * W + g;
        if (t == s) continue;
        if (find(kadj[s].begin(), kadj[s].end(), t) == kadj[s].end()) kadj[s].push_back(t);
      }
      adj[s][s] = 1; for (int t : kadj[s]) adj[s][t] = 1;
    }
  }
  string sq(int s) const { string t; t += char('a' + s % W); t += to_string(s / W + 1); return t; }
};

struct Pawn { int color, sq; };  // color 0 white, 1 black

struct Config {
  vector<Pawn> pw;
  string name;
};

struct LocalGame {
  const Board& B; vector<Pawn> pw; int np;
  vector<u64> attW, attB;       // squares attacked by white / black pawns, per alive mask
  vector<u64> occW, occB;       // pawn squares per alive mask
  vector<char> okmask;          // non-terminal alive masks
  vector<int> passer;           // per alive mask: bit0 white passer, bit1 black passer
  vector<int> distW, distB;
  u64 allowed;
  vector<int> id;               // id[(pm*N + wk)*N + bk]
  vector<array<int, 3>> nodes;  // pm, wk, bk
  Graph G;
  LocalGame(const Board& b, const vector<Pawn>& p, u64 allow) : B(b), pw(p), np((int)p.size()), allowed(allow) {}
  int pawnAt(int pm, int s) const { for (int i = 0; i < np; i++) if ((pm >> i & 1) && pw[i].sq == s) return i; return -1; }
  void build() {
    int N = B.N; int NM = 1 << np;
    attW.assign(NM, 0); attB.assign(NM, 0); occW.assign(NM, 0); occB.assign(NM, 0); passer.assign(NM, 0);
    distW.assign(NM, 99); distB.assign(NM, 99); okmask.assign(NM, 0);
    for (int pm = 0; pm < NM; pm++) {
      for (int i = 0; i < np; i++) if (pm >> i & 1) {
        int f = pw[i].sq % B.W, r = pw[i].sq / B.W;
        if (pw[i].color == 0) { occW[pm] |= (u64)1 << pw[i].sq; for (int d = -1; d <= 1; d += 2) { int g = B.nb(f, d); if (g >= 0 && r + 1 < B.H) attW[pm] |= (u64)1 << ((r + 1) * B.W + g); } }
        else { occB[pm] |= (u64)1 << pw[i].sq; for (int d = -1; d <= 1; d += 2) { int g = B.nb(f, d); if (g >= 0 && r - 1 >= 0) attB[pm] |= (u64)1 << ((r - 1) * B.W + g); } }
      }
      for (int i = 0; i < np; i++) if (pm >> i & 1) {
        int f = pw[i].sq % B.W, r = pw[i].sq / B.W; bool blocked = false;
        for (int j = 0; j < np; j++) if ((pm >> j & 1) && pw[j].color != pw[i].color) {
          int g = pw[j].sq % B.W, s = pw[j].sq / B.W;
          bool near = (g == f) || (B.nb(f, -1) == g) || (B.nb(f, 1) == g);
          if (!near) continue;
          if (pw[i].color == 0 ? s > r : s < r) blocked = true;
        }
        if (!blocked) {
          passer[pm] |= (pw[i].color == 0 ? 1 : 2);
          // promotion distance in pawn moves (cylcgt convention)
          int hh = B.H;
          if (pw[i].color == 0) distW[pm] = min(distW[pm], hh - 1 - r - (r == 1 ? 1 : 0));
          else distB[pm] = min(distB[pm], r - (r == hh - 2 ? 1 : 0));
        }
      }
      okmask[pm] = (passer[pm] == 0);
    }
    id.assign((size_t)NM * N * N, -1);
    int full = NM - 1;
    if (!okmask[full]) return;
    for (int pm = 0; pm < NM; pm++) {
      if (!okmask[pm]) continue;
      for (int wk = 0; wk < N; wk++) {
        if (!(allowed >> wk & 1)) continue;
        if ((occW[pm] | occB[pm]) >> wk & 1) continue;
        if (attB[pm] >> wk & 1) continue;
        for (int bk = 0; bk < N; bk++) {
          if (!(allowed >> bk & 1)) continue;
          if (B.adj[wk][bk]) continue;
          if ((occW[pm] | occB[pm]) >> bk & 1) continue;
          if (attW[pm] >> bk & 1) continue;
          id[((size_t)pm * N + wk) * N + bk] = (int)nodes.size();
          nodes.push_back({pm, wk, bk});
        }
      }
    }
    G.init((int)nodes.size());
    int nrace = 0;
    for (int i = 0; i < (int)nodes.size(); i++) {
      int pm = nodes[i][0], wk = nodes[i][1], bk = nodes[i][2];
      for (int c = 0; c < 2; c++) {
        int me = c == 0 ? wk : bk, op = c == 0 ? bk : wk;
        for (int t : B.kadj[me]) {
          if (!(allowed >> t & 1)) continue;
          if (B.adj[t][op]) continue;
          u64 own = c == 0 ? occW[pm] : occB[pm];
          u64 enm = c == 0 ? occB[pm] : occW[pm];
          if (own >> t & 1) continue;
          int npm = pm;
          if (enm >> t & 1) npm = pm & ~(1 << pawnAt(pm, t));
          u64 att = c == 0 ? attB[npm] : attW[npm];
          if (att >> t & 1) continue;
          if (!okmask[npm]) {
            int ps = passer[npm];
            int term;
            if (ps == 1) term = -1; else if (ps == 2) term = -2;
            else { // race (cannot happen with a capture-only game; kept for completeness)
              nrace++;
              int dw = distW[npm], db = distB[npm];
              // mover c has just moved; opponent moves next and wins ties
              if (c == 0) term = (db <= dw) ? -2 : -1; else term = (dw <= db) ? -1 : -2;
            }
            G.opt[c][i].push_back(term);
          } else {
            int nw = c == 0 ? t : wk, nbk = c == 0 ? bk : t;
            int to = id[((size_t)npm * B.N + nw) * B.N + nbk];
            if (to < 0) { fprintf(stderr, "internal: invalid target\n"); exit(1); }
            G.opt[c][i].push_back(to);
          }
        }
      }
    }
    G.finish();
    races = nrace;
  }
  int races = 0;
  // is every non-terminal alive subset pawn-frozen (no push, no pawn capture)?
  bool faithful() const {
    int NM = 1 << np;
    // reachable masks from the full one by single captures
    vector<char> reach(NM, 0); reach[NM - 1] = 1;
    for (int pm = NM - 1; pm >= 0; pm--) if (reach[pm] && okmask[pm]) for (int i = 0; i < np; i++) if (pm >> i & 1) reach[pm & ~(1 << i)] = 1;
    for (int pm = 0; pm < NM; pm++) if (reach[pm] && okmask[pm]) {
      for (int i = 0; i < np; i++) if (pm >> i & 1) {
        int f = pw[i].sq % B.W, r = pw[i].sq / B.W; int dr = pw[i].color == 0 ? 1 : -1;
        int fwd = (r + dr) * B.W + f;
        if (pawnAt(pm, fwd) < 0) return false;
        for (int d = -1; d <= 1; d += 2) { int g = B.nb(f, d); if (g < 0) continue; int s2 = (r + dr) * B.W + g; int j = pawnAt(pm, s2); if (j >= 0 && pw[j].color != pw[i].color) return false; }
      }
    }
    return true;
  }
};

// ---------------------------------------------------------------- loopiness (reaches a cycle?)
static vector<char> reaches_cycle(const Graph& G) {
  int n = G.n; vector<int> idx(n, -1), low(n, 0), comp(n, -1); vector<char> on(n, 0), cyc(n, 0);
  vector<int> st; int counter = 0, ncomp = 0;
  vector<int> csize;
  auto succ = [&](int x, vector<int>& out) { out.clear(); for (int c = 0; c < 2; c++) for (int t : G.opt[c][x]) if (t >= 0) out.push_back(t); sort(out.begin(), out.end()); out.erase(unique(out.begin(), out.end()), out.end()); };
  struct Fr { int x; vector<int> s; size_t i; };
  for (int r = 0; r < n; r++) if (idx[r] < 0) {
    vector<Fr> cs; cs.push_back({r, {}, 0}); succ(r, cs.back().s); idx[r] = low[r] = counter++; st.push_back(r); on[r] = 1;
    while (!cs.empty()) {
      Fr& f = cs.back();
      if (f.i < f.s.size()) {
        int y = f.s[f.i++];
        if (idx[y] < 0) { idx[y] = low[y] = counter++; st.push_back(y); on[y] = 1; cs.push_back({y, {}, 0}); succ(y, cs.back().s); }
        else if (on[y]) low[f.x] = min(low[f.x], idx[y]);
      } else {
        int x = f.x;
        if (low[x] == idx[x]) { int sz = 0; for (;;) { int y = st.back(); st.pop_back(); on[y] = 0; comp[y] = ncomp; sz++; if (y == x) break; } csize.push_back(sz); ncomp++; }
        int px = x; cs.pop_back();
        if (!cs.empty()) low[cs.back().x] = min(low[cs.back().x], low[px]);
      }
    }
  }
  // self loops cannot occur (a move changes the position). node reaches a cycle iff it reaches a comp with size>1.
  // Tarjan emits components in reverse topological order: successors have smaller comp ids.
  vector<char> cc(ncomp, 0);
  for (int c = 0; c < ncomp; c++) if (csize[c] > 1) cc[c] = 1;
  vector<vector<int>> cs2(ncomp);
  vector<int> o;
  for (int x = 0; x < n; x++) { succ(x, o); for (int y : o) if (comp[y] != comp[x]) cs2[comp[x]].push_back(comp[y]); }
  for (int c = 0; c < ncomp; c++) { if (!cc[c]) for (int d : cs2[c]) if (cc[d]) { cc[c] = 1; break; } }
  for (int x = 0; x < n; x++) cyc[x] = cc[comp[x]];
  return cyc;
}


// full product outcome: res[((size_t)x*K.n + k)*2 + s]
static void product_full(const Graph& G, const Graph& K, vector<uint8_t>& res) {
  vector<char> w0, w1; vector<int> cnt, q;
  retro(G, K, 0, w0, cnt, q);
  retro(G, K, 1, w1, cnt, q);
  size_t S = (size_t)G.n * K.n * 2; res.assign(S, 1);
  for (size_t i = 0; i < S; i++) res[i] = w0[i] ? 0 : (w1[i] ? 2 : 1);
}
// extended battery: all level-1 games (options from {+,-,0}) and all level-2 games with at most one option per side
static vector<Graph> big_battery() {
  vector<Graph> v;
  const int P = -1, M = -2;
  // level-1 options of a game: bitmask over {P,M,Z}
  auto opts1 = [&](int mask, int Z) { vector<int> o; if (mask & 1) o.push_back(P); if (mask & 2) o.push_back(M); if (mask & 4) o.push_back(Z); return o; };
  for (int a = 0; a < 8; a++) for (int b = 0; b < 8; b++) {
    Nodes nd(2); nd[0] = {opts1(a, 1), opts1(b, 1)}; nd[1] = {{}, {}}; v.push_back(mk(nd));
  }
  // level 2: option ids: 0 none, 1 = P, 2 = M, 3.. = level-1 game index (a*8+b) + 3
  for (int l = 0; l < 3 + 64; l++) for (int r = 0; r < 3 + 64; r++) {
    Nodes nd(2); nd[1] = {{}, {}};
    auto add = [&](int id, vector<int>& out) {
      if (id == 0) return;
      if (id == 1) { out.push_back(P); return; }
      if (id == 2) { out.push_back(M); return; }
      int g = id - 3, a = g / 8, b = g % 8;
      int idx = (int)nd.size();
      nd.push_back({opts1(a, 1), opts1(b, 1)});
      out.push_back(idx);
    };
    vector<int> lo, ro; add(l, lo); add(r, ro);
    nd[0] = {lo, ro};
    v.push_back(mk(nd));
  }
  return v;
}


// stopper test: no infinite ALTERNATING play from (x, s).  Build the state graph on (x, mover) and look for cycles.
static vector<char> stopper_flags(const Graph& G) {
  Graph H; H.init(2 * G.n);
  for (int x = 0; x < G.n; x++) for (int s = 0; s < 2; s++) for (int t : G.opt[s][x]) if (t >= 0) H.opt[0][2 * x + s].push_back(2 * t + 1 - s);
  H.finish();
  auto cyc = reaches_cycle(H);
  vector<char> st(G.n, 0);
  for (int x = 0; x < G.n; x++) st[x] = (!cyc[2 * x] && !cyc[2 * x + 1]) ? 1 : 0;
  return st;
}

// ---------------------------------------------------------------- main
static const char* OC = "WDL";
int main(int argc, char** argv) {
  string board = "cyl:6x6"; int margin = -1; int maxpairs = 2; string only; int rmin = 2; int verbose = 0; int maxex = 6;
  string rootsOut; int doExt = 0, doPairs = 0; string shortOut;
  for (int i = 1; i < argc; i++) {
    string a = argv[i];
    if (a == "--board") board = argv[++i];
    else if (a == "--margin") margin = atoi(argv[++i]);
    else if (a == "--maxpairs") maxpairs = atoi(argv[++i]);
    else if (a == "--only") only = argv[++i];     // e.g. "b2,d3" : pairs given as file+white rank
    else if (a == "--verbose") verbose = 1;
    else if (a == "--maxex") maxex = atoi(argv[++i]);
    else if (a == "--roots") rootsOut = argv[++i];
    else if (a == "--ext") doExt = 1;
    else if (a == "--short") shortOut = argv[++i];
    else if (a == "--pairs") doPairs = 1;
  }
  int wrap = board.substr(0, 3) == "cyl";
  int W = atoi(strchr(board.c_str(), 0x3a) + 1); int H = atoi(strchr(board.c_str(), 0x78) + 1);
  Board B; B.init(W, H, wrap);
  auto ctx = make_contexts();
  int NC = (int)ctx.size();
  // references = the first 'nref' contexts that are plain values (all contexts are also references)
  Graph zero = ctx[0].g;
  // signatures of references
  vector<string> refsig(NC);
  for (int j = 0; j < NC; j++) {
    string sg;
    for (int k = 0; k < NC; k++) { vector<uint8_t> r; outcomes(ctx[j].g, ctx[k].g, r); sg += char('0' + r[0]); sg += char('0' + r[1]); }
    refsig[j] = sg;
  }
  map<string, vector<string>> refnames;
  for (int j = 0; j < NC; j++) refnames[refsig[j]].push_back(ctx[j].name);
  printf("# board %s margin %d  contexts %d  distinct reference signatures %zu\n", board.c_str(), margin, NC, refnames.size());
  for (auto& kv : refnames) { printf("# REF"); for (auto& s : kv.second) printf(" %s", s.c_str()); printf("\n"); }
  // enumerate configurations
  vector<vector<array<int, 2>>> cfgs;  // list of pairs (file, white rank 1-based)
  cfgs.push_back({});
  vector<array<int, 2>> singles;
  for (int f = 0; f < W; f++) for (int r = 2; r <= H - 2; r++) singles.push_back({f, r});
  auto canon = [&](vector<array<int, 2>> c) {
    // canonical under file rotation (cyl) and file reflection
    vector<vector<array<int, 2>>> forms;
    for (int refl = 0; refl < 2; refl++) {
      for (int sh = 0; sh < (wrap ? W : 1); sh++) {
        vector<array<int, 2>> d;
        for (auto& p : c) { int f = refl ? W - 1 - p[0] : p[0]; f = wrap ? (f + sh) % W : f; d.push_back({f, p[1]}); }
        sort(d.begin(), d.end()); forms.push_back(d);
      }
    }
    return *min_element(forms.begin(), forms.end());
  };
  set<vector<array<int, 2>>> seen;
  seen.insert({});
  if (maxpairs >= 1) for (auto& s : singles) { auto c = canon({s}); if (seen.insert(c).second) cfgs.push_back(c); }
  if (maxpairs >= 2) for (auto& s : singles) for (auto& t : singles) {
    if (s[0] >= t[0]) continue;
    int d = t[0] - s[0]; if (wrap) d = min(d, W - d);
    if (d > 3) continue;
    auto c = canon({s, t}); if (seen.insert(c).second) cfgs.push_back(c);
  }
  // file-ordered second loop above misses cyclic wrap pairs only if canonical dedupe fails; fine (rotation-invariant).
  map<string, long> totalClass;
  long totalRoots = 0, totalShort = 0;
  FILE* rf = rootsOut.empty() ? nullptr : fopen(rootsOut.c_str(), "w");
  for (auto& c : cfgs) {
    string cname; vector<Pawn> pws;
    for (auto& p : c) {
      cname += string(1, char('a' + p[0])) + to_string(p[1]) + " ";
      pws.push_back({0, (p[1] - 1) * W + p[0]}); pws.push_back({1, p[1] * W + p[0]});
    }
    if (cname.empty()) cname = "none ";
    if (!only.empty()) { string on2 = cname; on2.pop_back(); string want = only; for (char& ch : want) if (ch == ',') ch = ' '; if (on2 != want) continue; }
    u64 allowed = (B.N == 64) ? ~0ULL : (((u64)1 << B.N) - 1);
    if (margin >= 0 && !c.empty()) {
      int lo = 99, hi = -1; for (auto& p : c) { lo = min(lo, p[0]); hi = max(hi, p[0]); }
      // arc of files [lo-margin, hi+margin]; on a cylinder use the minimal arc (c is canonical, files sorted)
      u64 m = 0;
      for (int f = lo - margin; f <= hi + margin; f++) { int g = wrap ? ((f % W) + W) % W : f; if (g < 0 || g >= W) continue; for (int r = 0; r < H; r++) m |= (u64)1 << (r * W + g); }
      allowed = m;
    }
    LocalGame LG(B, pws, allowed);
    LG.build();
    if (LG.G.n == 0) { printf("CONFIG %s: no legal root\n", cname.c_str()); continue; }
    bool faith = LG.faithful();
    auto cyc = reaches_cycle(LG.G);
    auto stp = stopper_flags(LG.G);
    int n = LG.G.n;
    vector<string> sig(n);
    for (int k = 0; k < NC; k++) {
      vector<uint8_t> r; outcomes(LG.G, ctx[k].g, r);
      for (int x = 0; x < n; x++) { sig[x] += char('0' + r[2 * x]); sig[x] += char('0' + r[2 * x + 1]); }
    }
    long nshort = 0; for (int x = 0; x < n; x++) if (!cyc[x]) nshort++;
    printf("CONFIG %s: nodes %d  faithful %d  short-roots %ld  races %d\n", cname.c_str(), n, faith ? 1 : 0, nshort, LG.races);
    map<string, vector<int>> cls;
    for (int x = 0; x < n; x++) cls[sig[x]].push_back(x);
    auto idxOf = [&](const char* nm) { for (int j = 0; j < NC; j++) if (ctx[j].name == nm) return j; return 0; };
    int iOn = idxOf("on"), iOff = idxOf("off"), iDud = idxOf("dud"), iP1 = idxOf("+1"), iM1 = idxOf("-1");
    auto pr = [&](const string& sg, int j) { string r; r += '('; r += OC[sg[2 * j] - '0']; r += ','; r += OC[sg[2 * j + 1] - '0']; r += ')'; return r; };
    vector<pair<long, string>> order;
    for (auto& kv : cls) order.push_back({-(long)kv.second.size(), kv.first});
    sort(order.begin(), order.end());
    for (auto& o : order) {
      const string& sg = o.second; auto& xs = cls[sg];
      string nm; auto it = refnames.find(sg); if (it != refnames.end()) { for (auto& s2 : it->second) nm += s2 + "="; nm.pop_back(); } else nm = "UNMATCHED";
      long nsh = 0, nstp = 0; for (int x : xs) { if (!cyc[x]) nsh++; if (stp[x]) nstp++; }
      printf("  CLASS %-14s roots %6zu short %5ld stopper %5ld | alone%s on%s off%s dud%s +1%s -1%s |", nm.c_str(), xs.size(), nsh, nstp, pr(sg, 0).c_str(), pr(sg, iOn).c_str(), pr(sg, iOff).c_str(), pr(sg, iDud).c_str(), pr(sg, iP1).c_str(), pr(sg, iM1).c_str());
      int shown = 0;
      bool listAll = (nm == "UNMATCHED") || xs.size() <= 3;
      for (int x : xs) {
        if (!listAll && shown >= maxex) break;
        int pm = LG.nodes[x][0], wk = LG.nodes[x][1], bk = LG.nodes[x][2];
        string pos = "K" + B.sq(wk) + " k" + B.sq(bk);
        for (int i2 = 0; i2 < LG.np; i2++) if (pm >> i2 & 1) pos += string(" ") + (LG.pw[i2].color == 0 ? "P" : "p") + B.sq(LG.pw[i2].sq);
        printf(" [%s]", pos.c_str()); shown++;
        if (shown >= 40) break;
      }
      printf("\n");
      totalClass[nm] += (long)xs.size();
    }
    if (rf) for (int x = 0; x < n; x++) {
      int pm = LG.nodes[x][0], wk = LG.nodes[x][1], bk = LG.nodes[x][2];
      string pos = "K" + B.sq(wk) + " k" + B.sq(bk);
      for (int i2 = 0; i2 < LG.np; i2++) if (pm >> i2 & 1) pos += string(" ") + (LG.pw[i2].color == 0 ? "P" : "p") + B.sq(LG.pw[i2].sq);
      string nm; auto it = refnames.find(sig[x]); if (it != refnames.end()) nm = it->second[0]; else nm = "UNMATCHED";
      fprintf(rf, "%s|%s|%s|%d|%s\n", cname.c_str(), pos.c_str(), nm.c_str(), (cyc[x] ? 0 : 1) + 2 * (int)stp[x], sig[x].c_str());
    }

    if (doExt || doPairs) {
      set<string> valueNames = {"0", "*", "+1", "-1", "tis", "tisn", "{1|0}", "{0|-1}", "{on|off}", "on", "off", "dud"};
      vector<int> memberRoots; vector<int> memberRef;
      for (int x = 0; x < n; x++) { auto it = refnames.find(sig[x]); if (it == refnames.end()) continue; int j = -1; for (int t = 0; t < NC; t++) if (ctx[t].name == it->second[0]) j = t; if (valueNames.count(it->second[0])) { memberRoots.push_back(x); memberRef.push_back(j); } }
      if (doExt) {
        auto bb = big_battery();
        // signature of each reference on the big battery, and of each member root
        vector<string> refbig(NC), rootbig(n);
        for (int j = 0; j < NC; j++) if (valueNames.count(ctx[j].name)) for (auto& K : bb) { vector<uint8_t> r; outcomes(ctx[j].g, K, r); refbig[j] += char('0' + r[0]); refbig[j] += char('0' + r[1]); }
        for (auto& K : bb) { vector<uint8_t> r; outcomes(LG.G, K, r); for (int x : memberRoots) { rootbig[x] += char('0' + r[2 * x]); rootbig[x] += char('0' + r[2 * x + 1]); } }
        map<string, array<long, 2>> stat;
        for (size_t t = 0; t < memberRoots.size(); t++) { int x = memberRoots[t]; bool ok = rootbig[x] == refbig[memberRef[t]]; stat[ctx[memberRef[t]].name][ok ? 0 : 1]++; }
        printf("  EXT %zu contexts:", bb.size());
        for (auto& kv : stat) printf(" %s agree=%ld disagree=%ld;", kv.first.c_str(), kv.second[0], kv.second[1]);
        printf("\n");
      }
      if (doPairs && n <= 4200) {
        vector<uint8_t> pf; product_full(LG.G, LG.G, pf);
        // predicted: outcome of ref_a (+) ref_b
        map<pair<int, int>, array<uint8_t, 2>> pred;
        map<string, array<long, 2>> stat;
        long checked = 0, bad = 0; string firstbad;
        for (size_t t = 0; t < memberRoots.size(); t++) for (size_t u = 0; u < memberRoots.size(); u++) {
          int ja = memberRef[t], jb = memberRef[u];
          auto key = make_pair(ja, jb);
          if (!pred.count(key)) { vector<uint8_t> r; product_full(ctx[ja].g, ctx[jb].g, r); pred[key] = {r[0], r[1]}; }
          int x = memberRoots[t], y = memberRoots[u];
          size_t id = ((size_t)x * n + y) * 2;
          bool ok = pf[id] == pred[key][0] && pf[id + 1] == pred[key][1];
          checked++; string kn = ctx[ja].name + "+" + ctx[jb].name; stat[kn][ok ? 0 : 1]++;
          if (!ok) { bad++; }
        }
        printf("  PAIRS checked %ld mismatches %ld |", checked, bad);
        for (auto& kv : stat) if (kv.second[1] > 0 || kv.first.find("+1") != string::npos || kv.first.find("-1") != string::npos) printf(" %s ok=%ld bad=%ld;", kv.first.c_str(), kv.second[0], kv.second[1]);
        printf("\n");
      }
    }

    if (!shortOut.empty()) {
      FILE* sf = fopen(shortOut.c_str(), "a");
      for (int x = 0; x < n; x++) if (!cyc[x]) {
        // dump the reachable subgraph (acyclic) of x
        vector<int> order, seenv; vector<int> stk{x}; map<int, int> ix; ix[x] = 0; order.push_back(x);
        for (size_t qi = 0; qi < order.size(); qi++) for (int c2 = 0; c2 < 2; c2++) for (int t : LG.G.opt[c2][order[qi]]) if (t >= 0 && !ix.count(t)) { ix[t] = (int)order.size(); order.push_back(t); }
        int pm = LG.nodes[x][0], wk = LG.nodes[x][1], bk = LG.nodes[x][2];
        string pos = "K" + B.sq(wk) + " k" + B.sq(bk);
        for (int i2 = 0; i2 < LG.np; i2++) if (pm >> i2 & 1) pos += string(" ") + (LG.pw[i2].color == 0 ? "P" : "p") + B.sq(LG.pw[i2].sq);
        fprintf(sf, "%s|%s|", cname.c_str(), pos.c_str());
        for (size_t k = 0; k < order.size(); k++) {
          for (int c2 = 0; c2 < 2; c2++) { fprintf(sf, "%s", c2 ? "/" : ""); bool first = true; for (int t : LG.G.opt[c2][order[k]]) { fprintf(sf, "%s%s", first ? "" : ",", t == -1 ? "P" : t == -2 ? "M" : to_string(ix[t]).c_str()); first = false; } }
          fprintf(sf, ";");
        }
        fprintf(sf, "\n");
      }
      fclose(sf);
    }
    totalRoots += n; totalShort += nshort;
  }
  printf("TOTAL roots %ld short %ld\n", totalRoots, totalShort);
  for (auto& kv : totalClass) printf("TOTALCLASS %s %ld\n", kv.first.c_str(), kv.second);
  if (rf) fclose(rf);
  return 0;
}
