// K47 implementation B (written separately from za.cpp, from kings/SPEC.md and LOOPY Definitions 1.2, 1.3, 1.5 and
// K40's sum convention): r(X + T) for X = the K45 group (the P game of its own pieces) and for X = over, T a test game.
// Design: mailbox board with base-5 packed keys; a generic component (options per side, check and promotion flags, the
// e.p.-clearing map); the product states reachable from the start are found first, then the two attractors
// (White forces a win, Black forces a win) are computed separately; everything else is a draw.
// Sum rules: a move is a move in one component; a promotion is a win for the promoter and ends the play; a side in check
// must move in X (checkmate loses); a move elsewhere clears the e.p. right of X (and vice versa for T);
// a side with no move at all loses (conv N) or draws (conv C).
// Usage: zb <W> <H> <roots file> <tests file> <N|C>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <unordered_map>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <cstdint>
using namespace std;

static int BW, BH;
struct Board { char sq[64]; int ep; };   // sq: '.', 'K', 'k', 'P', 'p'; ep = e.p. target square or -1
struct Key2 { uint64_t a, b; bool operator==(const Key2& o) const { return a == o.a && b == o.b; } };
struct KeyHash { size_t operator()(const Key2& k) const { uint64_t h = k.a ^ (k.b * 0xff51afd7ed558ccdULL); h ^= h >> 33; h *= 0xc4ceb9fe1a85ec53ULL; return h ^ (h >> 29); } };
static int code(char c) { return c == '.' ? 0 : c == 'K' ? 1 : c == 'k' ? 2 : c == 'P' ? 3 : 4; }
static Key2 pack(const Board& b) {
  int n = BW * BH, half = n / 2; uint64_t a = 0, c = 0;
  for (int i = half - 1; i >= 0; i--) a = a * 5 + code(b.sq[i]);
  for (int i = n - 1; i >= half; i--) c = c * 5 + code(b.sq[i]);
  c = c * 64 + (b.ep + 1);
  return {a, c};
}
static int at(int f, int r) { return r * BW + ((f % BW) + BW) % BW; }
static int fileOf(int s) { return s % BW; }
static int rankOf(int s) { return s / BW; }
static int findKing(const Board& b, char k) { for (int i = 0; i < BW * BH; i++) if (b.sq[i] == k) return i; return -1; }
// is the king of colour `white` attacked?
static bool kingAttacked(const Board& b, bool white) {
  int k = findKing(b, white ? 'K' : 'k'); int f = fileOf(k), r = rankOf(k);
  char enemyK = white ? 'k' : 'K', enemyP = white ? 'p' : 'P';
  for (int dr = -1; dr <= 1; dr++) for (int df = -1; df <= 1; df++) {
    if (!dr && !df) continue; int rr = r + dr; if (rr < 0 || rr >= BH) continue;
    if (b.sq[at(f + df, rr)] == enemyK) return true; }
  // a black pawn attacks downwards: it attacks the white king from rank r+1; a white pawn attacks a black king from rank r-1
  int pr = white ? r + 1 : r - 1;
  if (pr >= 0 && pr < BH) { if (b.sq[at(f - 1, pr)] == enemyP || b.sq[at(f + 1, pr)] == enemyP) return true; }
  return false;
}
static bool kingsTouch(const Board& b) {
  int a = findKing(b, 'K'), c = findKing(b, 'k');
  int df = abs(fileOf(a) - fileOf(c)); if (BW - df < df) df = BW - df;
  return df <= 1 && abs(rankOf(a) - rankOf(c)) <= 1;
}
// legal moves; promotions are reported by a flag (they end the play), other moves as boards
static void moves(const Board& b, bool white, vector<Board>& res, bool& promotes) {
  res.clear(); promotes = false;
  char K = white ? 'K' : 'k', P = white ? 'P' : 'p', eP = white ? 'p' : 'P';
  int fwd = white ? 1 : -1, lastR = white ? BH - 1 : 0, dblR = white ? 1 : BH - 2;
  auto finish = [&](Board n) { if (kingAttacked(n, white)) return; if (kingsTouch(n)) return; res.push_back(n); };
  for (int s = 0; s < BW * BH; s++) {
    char pc = b.sq[s]; int f = fileOf(s), r = rankOf(s);
    if (pc == K) {
      for (int dr = -1; dr <= 1; dr++) for (int df = -1; df <= 1; df++) {
        if (!dr && !df) continue; int rr = r + dr; if (rr < 0 || rr >= BH) continue;
        int t = at(f + df, rr); char d = b.sq[t];
        if (d != '.' && d != eP) continue;   // own piece or enemy king
        Board n = b; n.ep = -1; n.sq[s] = '.'; n.sq[t] = K; finish(n);
      }
    } else if (pc == P) {
      int r1 = r + fwd;
      auto add = [&](int t, int capSq) {
        Board n = b; n.ep = -1; n.sq[s] = '.'; if (capSq >= 0) n.sq[capSq] = '.';
        if (rankOf(t) == lastR) { if (!kingAttacked(n, white)) promotes = true; return; }
        n.sq[t] = P; finish(n);
      };
      int t1 = at(f, r1);
      if (b.sq[t1] == '.') {
        add(t1, -1);
        if (r == dblR) { int t2 = at(f, r1 + fwd); if (b.sq[t2] == '.') {
          Board n = b; n.ep = t1; n.sq[s] = '.'; n.sq[t2] = P;
          if (!kingAttacked(n, white)) res.push_back(n); } }
      }
      for (int df : {-1, 1}) {
        int t = at(f + df, r1);
        if (b.sq[t] == eP) add(t, t);
        else if (t == b.ep && b.sq[at(f + df, r)] == eP) add(t, at(f + df, r));
      }
    }
  }
}
// generic component
struct Comp {
  vector<vector<int>> opt[2];  // options per side (ids)
  vector<char> check[2], promo[2];
  vector<int> clear;            // e.p. cleared
};
static Comp chessComp(const vector<Board>& roots, vector<int>& rootIds, vector<Board>& nodesOut) {
  Comp C; unordered_map<Key2, int, KeyHash> id; vector<Board>& nodes = nodesOut;
  auto get = [&](const Board& b) { Key2 k = pack(b); auto it = id.find(k); if (it != id.end()) return it->second;
    int n = nodes.size(); id.emplace(k, n); nodes.push_back(b); return n; };
  for (auto& r : roots) rootIds.push_back(get(r));
  vector<Board> mv; bool pr;
  for (size_t i = 0; i < nodes.size(); i++) {
    Board b = nodes[i];
    for (int c = 0; c < 2; c++) {
      bool white = c == 0;
      C.check[c].push_back(kingAttacked(b, white));
      vector<int> o;
      // only generate if the opponent is not in check (otherwise this side is never to move here)
      if (!kingAttacked(b, !white)) { moves(b, white, mv, pr); for (auto& x : mv) o.push_back(get(x)); }
      else pr = false;
      C.promo[c].push_back(pr); C.opt[c].push_back(o);
    }
    Board cb = b; cb.ep = -1; C.clear.push_back(get(cb));
  }
  return C;
}
// test game: options may be -1 (White wins) or -2 (Black wins)
struct Test { string name; int m; vector<vector<int>> o[2]; vector<int> cl; };
static Test readTest(const string& line) {
  Test T; vector<string> f; size_t p = 0, q;
  while ((q = line.find('|', p)) != string::npos) { f.push_back(line.substr(p, q - p)); p = q + 1; }
  f.push_back(line.substr(p));
  T.name = f[0]; T.name.erase(T.name.find_last_not_of(' ') + 1);
  T.m = stoi(f[1]); T.o[0].resize(T.m); T.o[1].resize(T.m); T.cl.resize(T.m);
  for (int i = 0; i < T.m; i++) T.cl[i] = i;
  stringstream ss(f[2]); string part;
  while (getline(ss, part, ';')) {
    stringstream ps(part); string tok; int pos = -1;
    while (ps >> tok) {
      if (tok.back() == ':') { pos = stoi(tok); continue; }
      int side = tok[0] == 'L' ? 0 : tok[0] == 'R' ? 1 : 2;
      string v = tok.substr(2);
      if (side == 2) { T.cl[pos] = stoi(v); continue; }
      stringstream vs(v); string x;
      while (getline(vs, x, ',')) if (!x.empty()) T.o[side][pos].push_back(x == "W" ? -1 : x == "B" ? -2 : stoi(x));
    }
  }
  return T;
}
// r(X + T) for every reachable product state; returns per state: 'W', 'L' (Black wins), 'D', or 0 (unreached)
static char CONVB;
struct Rev { vector<uint32_t> off[2], lst[2], coff, clst; };
static Rev reverseOf(const Comp& X) {
  Rev R; size_t n = X.clear.size();
  for (int c = 0; c < 2; c++) {
    R.off[c].assign(n + 1, 0);
    for (size_t x = 0; x < n; x++) for (int y : X.opt[c][x]) R.off[c][y + 1]++;
    for (size_t x = 0; x < n; x++) R.off[c][x + 1] += R.off[c][x];
    R.lst[c].resize(R.off[c][n]); vector<uint32_t> f(R.off[c].begin(), R.off[c].end() - 1);
    for (size_t x = 0; x < n; x++) for (int y : X.opt[c][x]) R.lst[c][f[y]++] = x;
  }
  R.coff.assign(n + 1, 0); for (size_t x = 0; x < n; x++) R.coff[X.clear[x] + 1]++;
  for (size_t x = 0; x < n; x++) R.coff[x + 1] += R.coff[x];
  R.clst.resize(n); { vector<uint32_t> f(R.coff.begin(), R.coff.end() - 1); for (size_t x = 0; x < n; x++) R.clst[f[X.clear[x]]++] = x; }
  return R;
}
static vector<char> sumSolve(const Comp& X, const Rev& RV, const vector<int>& starts, const Test& T) {
  size_t n = X.clear.size(), m = T.m, S = n * m * 2;
  auto id = [&](size_t x, size_t t, int s) { return ((size_t)s * m + t) * n + x; };  // a different layout from A
  auto dec = [&](size_t i, size_t& x, size_t& t, int& s) { s = i / (m * n); t = (i / n) % m; x = i % n; };
  vector<vector<int>> Tpre[2], Tcl(m);
  for (int c = 0; c < 2; c++) { Tpre[c].resize(m); for (size_t t = 0; t < m; t++) for (int u : T.o[c][t]) if (u >= 0) Tpre[c][u].push_back(t); }
  for (size_t t = 0; t < m; t++) Tcl[T.cl[t]].push_back(t);
  auto succ = [&](size_t x, size_t t, int s, vector<long long>& out) {
    out.clear();
    if (X.promo[s][x]) out.push_back(s == 0 ? -1 : -2);
    for (int y : X.opt[s][x]) out.push_back(id(y, T.cl[t], 1 - s));
    if (!X.check[s][x]) for (int u : T.o[s][t]) out.push_back(u < 0 ? u : (long long)id(X.clear[x], u, 1 - s));
  };
  // predecessors of product state j (one entry per edge)
  auto preds = [&](size_t j, vector<size_t>& out) {
    out.clear(); size_t y, u; int s2; dec(j, y, u, s2); int s = 1 - s2;
    for (uint32_t k = RV.off[s][y]; k < RV.off[s][y + 1]; k++) for (int t : Tcl[u]) out.push_back(id(RV.lst[s][k], t, s));
    if (X.clear[y] == (int)y)  // y carries no e.p. right: a T move may have led here from any x that clears to y
      for (uint32_t k = RV.coff[y]; k < RV.coff[y + 1]; k++) { size_t x = RV.clst[k]; if (X.check[s][x]) continue;
        for (int t : Tpre[s][u]) out.push_back(id(x, t, s)); }
  };
  size_t NW = (S + 63) / 64;
  vector<uint64_t> reach(NW, 0), fr(NW, 0), nx(NW, 0); vector<long long> sc; vector<size_t> pv;
  auto setb = [](vector<uint64_t>& v, size_t i) { v[i >> 6] |= 1ULL << (i & 63); };
  auto getb = [](const vector<uint64_t>& v, size_t i) { return (v[i >> 6] >> (i & 63)) & 1; };
  for (int z : starts) for (int s = 0; s < 2; s++) { setb(reach, id(z, 0, s)); setb(fr, id(z, 0, s)); }
  for (bool more = true; more;) { more = false;
    for (size_t w = 0; w < NW; w++) for (uint64_t bb = fr[w]; bb; bb &= bb - 1) { size_t i = w * 64 + __builtin_ctzll(bb);
      size_t x, t; int s; dec(i, x, t, s); succ(x, t, s, sc);
      for (long long j : sc) if (j >= 0 && !getb(reach, j)) { setb(reach, j); setb(nx, j); more = true; } }
    swap(fr, nx); fill(nx.begin(), nx.end(), 0); }
  vector<char> res(S, 0);
  for (size_t i = 0; i < S; i++) if (getb(reach, i)) res[i] = 'D';
  vector<uint8_t> left(S);
  for (int sig = 0; sig < 2; sig++) {
    long long myT = sig == 0 ? -1 : -2; char mark = sig == 0 ? 'W' : 'L';
    fill(fr.begin(), fr.end(), 0);
    for (size_t i = 0; i < S; i++) { left[i] = 255; if (!getb(reach, i)) continue;
      size_t x, t; int s; dec(i, x, t, s); succ(x, t, s, sc); bool in = false;
      if (s == sig) { for (long long j : sc) if (j == myT) in = true; }
      else {
        bool escape = false; int cnt = 0;
        for (long long j : sc) { if (j == myT) continue; if (j < 0) { escape = true; break; } cnt++; }
        if (escape) continue;
        if (sc.empty()) { if (X.check[s][x] || CONVB == 'N') in = true; else continue; }
        else if (cnt == 0) in = true;
        else { if (cnt > 250) { fprintf(stderr, "deg\n"); exit(1); } left[i] = cnt; }
      }
      if (in) { res[i] = mark; setb(fr, i); }
    }
    for (bool more = true; more;) { more = false;
      for (size_t w = 0; w < NW; w++) for (uint64_t bb = fr[w]; bb; bb &= bb - 1) { size_t j = w * 64 + __builtin_ctzll(bb);
        preds(j, pv);
        for (size_t i : pv) { if (!getb(reach, i) || res[i] == mark) continue;
          int s = i / (m * n);
          if (s == sig) { res[i] = mark; setb(nx, i); more = true; }
          else if (left[i] != 255 && --left[i] == 0) { res[i] = mark; setb(nx, i); more = true; } } }
      swap(fr, nx); fill(nx.begin(), nx.end(), 0); }
  }
  return res;
}
static Board parseBoard(const string& l) {
  Board b; memset(b.sq, '.', sizeof b.sq); b.ep = -1; stringstream ss(l); string t;
  while (ss >> t) { int f = t[1] - 'a', r = stoi(t.substr(2)) - 1; b.sq[at(f, r)] = t[0]; }
  return b;
}
int main(int argc, char** argv) {
  BW = atoi(argv[1]); BH = atoi(argv[2]); CONVB = argv[5][0];
  vector<Board> roots; vector<string> names; { ifstream f(argv[3]); string l; while (getline(f, l)) if (!l.empty() && l[0] != '#') { roots.push_back(parseBoard(l)); names.push_back(l); } }
  vector<int> rid; vector<Board> nodes; Comp X = chessComp(roots, rid, nodes);
  fprintf(stderr, "B: component nodes %zu\n", nodes.size());
  Rev RX = reverseOf(X);
  Comp O; O.opt[0] = {{1}, {}}; O.opt[1] = {{0}, {}}; O.check[0] = O.check[1] = {0, 0}; O.promo[0] = O.promo[1] = {0, 0}; O.clear = {0, 1};
  Rev RO = reverseOf(O);
  ifstream tf(argv[4]); string l;
  while (getline(tf, l)) {
    if (l.empty() || l[0] == '#') continue;
    Test T = readTest(l);
    vector<char> rz = sumSolve(X, RX, rid, T), ro = sumSolve(O, RO, {0}, T);
    size_t n = nodes.size(), m = T.m;
    for (size_t r = 0; r < rid.size(); r++) for (int s = 0; s < 2; s++) {
      char a = rz[((size_t)s * m + 0) * n + rid[r]], b = ro[((size_t)s * m + 0) * 2 + 0];
      printf("%s | %s | %c | Z %c | over %c | %s\n", T.name.c_str(), names[r].c_str(), s ? 'b' : 'w', a, b, a == b ? "MATCH" : "DIFF");
    }
    fflush(stdout);
  }
}
