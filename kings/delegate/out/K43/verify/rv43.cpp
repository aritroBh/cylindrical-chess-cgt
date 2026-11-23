// rv43.cpp -- K43 referee: own table solver of model P (kings/SPEC.md rules, first promotion wins for the promoter,
// e.p. on, stalemate and infinite play draw) and an own implementation of the exact under/over test of LOOPY Definition 4.8.
// Written from SPEC.md and LOOPY Definition 4.8 only; no code from the K43 investigator.
// Usage: rv43 --board cyl:7x6 --files 0-3 --maxw 3 --maxb 3 [--list N]       (test mode)
//        rv43 --board cyl:7x6 --files 0-3 --maxw 3 --maxb 3 --eval < positions (prints "pos | V", White's view, for the side to move)
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>
using namespace std;
typedef uint64_t u64;
static int W, H, N, WRAP;
static int NB[80][8], NNB[80];
static u64 ATT[2][80]; // ATT[c][s]: squares from which a pawn of colour c attacks s
static int DIST[80][80];
static int sq(int f, int r) { if (r < 0 || r >= H) return -1; if (WRAP) f = (f % W + W) % W; else if (f < 0 || f >= W) return -1; return r * W + f; }
static int fileOf(int s) { return s % W; }
static int rankOf(int s) { return s / W; }

struct LKH { size_t operator()(const pair<u64,u64>& k) const { return k.first * 0x9E3779B97F4A7C15ULL ^ (k.second + 0x1234567ULL) * 0xC2B2AE3D27D4EB4FULL; } };
static unordered_map<pair<u64,u64>, int, LKH> ids;
static vector<vector<uint8_t>> tabs; // packed 2 bits; 0 draw, 1 mover wins, 2 mover loses, 3 illegal
static vector<char> state; // 0 new, 1 solving, 2 solved
static long nSolved = 0;

static inline int idxOf(int stm, int wk, int bk) { return (stm * N + wk) * N + bk; }
static inline int tget(int id, int i) { return (tabs[id][i >> 2] >> ((i & 3) * 2)) & 3; }

static int solveLayer(u64 wp, u64 bp);
static int layerId(u64 wp, u64 bp) {
  auto it = ids.find({wp, bp});
  int id;
  if (it == ids.end()) { id = (int)tabs.size(); ids[{wp, bp}] = id; tabs.emplace_back(); state.push_back(0); }
  else id = it->second;
  if (state[id] == 2) return id;
  if (state[id] == 1) { fprintf(stderr, "cycle\n"); exit(1); }
  solveLayer(wp, bp);
  return id;
}

struct Pos { u64 wp, bp; int wk, bk, stm, ep; };
// move kinds
enum { PROMO = 0, KMOVE = 1, OTHER = 2 };
struct Mv { int kind; Pos c; };

static bool attackedBy(int s, int c, u64 pawns) { return (ATT[c][s] & pawns) != 0; }
static bool legalPos(const Pos& p) {
  u64 occ = p.wp | p.bp;
  if (p.wp & p.bp) return false;
  if ((occ >> p.wk) & 1) return false;
  if ((occ >> p.bk) & 1) return false;
  if (p.wk == p.bk || DIST[p.wk][p.bk] < 2) return false;
  // side not to move not in check
  if (p.stm == 0) { if (attackedBy(p.bk, 0, p.wp)) return false; }
  else { if (attackedBy(p.wk, 1, p.bp)) return false; }
  return true;
}
static bool inCheck(const Pos& p) { return p.stm == 0 ? attackedBy(p.wk, 1, p.bp) : attackedBy(p.bk, 0, p.wp); }

static void genMoves(const Pos& p, vector<Mv>& out) {
  out.clear();
  int us = p.stm, them = 1 - us;
  u64 own = us == 0 ? p.wp : p.bp, opp = us == 0 ? p.bp : p.wp;
  int ok = us == 0 ? p.wk : p.bk, ek = us == 0 ? p.bk : p.wk;
  u64 occ = p.wp | p.bp | (1ULL << p.wk) | (1ULL << p.bk);
  // king
  for (int i = 0; i < NNB[ok]; i++) {
    int t = NB[ok][i];
    if ((own >> t) & 1) continue;
    if (DIST[t][ek] < 2) continue;
    u64 opp2 = opp & ~(1ULL << t);
    if (ATT[them][t] & opp2) continue;
    Mv m; m.c = p; m.c.stm = them; m.c.ep = -1;
    if (us == 0) m.c.wk = t; else m.c.bk = t;
    if ((opp >> t) & 1) { m.kind = OTHER; if (us == 0) m.c.bp = opp2; else m.c.wp = opp2; }
    else m.kind = KMOVE;
    out.push_back(m);
  }
  // pawns
  int dir = us == 0 ? 1 : -1, last = us == 0 ? H - 1 : 0, second = us == 0 ? 1 : H - 2;
  for (u64 b = own; b; b &= b - 1) {
    int s = __builtin_ctzll(b), f = fileOf(s), r = rankOf(s);
    auto add = [&](int to, u64 capMask, int epsq) {
      u64 nown = (own & ~(1ULL << s));
      u64 nopp = opp & ~capMask;
      bool promo = rankOf(to) == last;
      if (!promo) nown |= 1ULL << to;
      // legality: own king not attacked by enemy pawns afterwards
      if (ATT[them][ok] & nopp) return;
      Mv m; m.c = p; m.c.stm = them; m.c.ep = epsq;
      if (us == 0) { m.c.wp = nown; m.c.bp = nopp; } else { m.c.bp = nown; m.c.wp = nopp; }
      m.kind = promo ? PROMO : OTHER;
      out.push_back(m);
    };
    int t1 = sq(f, r + dir);
    if (t1 >= 0 && !((occ >> t1) & 1)) {
      add(t1, 0, -1);
      if (r == second) {
        int t2 = sq(f, r + 2 * dir);
        if (t2 >= 0 && !((occ >> t2) & 1)) add(t2, 0, rankOf(t2) == last ? -1 : t1);
      }
    }
    for (int df = -1; df <= 1; df += 2) {
      int t = sq(f + df, r + dir);
      if (t < 0) continue;
      if ((opp >> t) & 1) add(t, 1ULL << t, -1);
      else if (t == p.ep) { int cs = sq(f + df, r); add(t, 1ULL << cs, -1); }
    }
  }
}

static int valueOf(const Pos& p);
// 1-ply evaluation (used for e.p.-flagged positions and for checks); nmoves returned
static int evalNode(const Pos& p, int* nmoves) {
  vector<Mv> ms; genMoves(p, ms);
  if (nmoves) *nmoves = (int)ms.size();
  if (ms.empty()) return inCheck(p) ? 2 : 0;
  bool draw = false;
  for (auto& m : ms) {
    if (m.kind == PROMO) return 1;
    int v = valueOf(m.c);
    if (v == 2) return 1;
    if (v == 0) draw = true;
  }
  return draw ? 0 : 2;
}
static int valueOf(const Pos& p) {
  if (p.ep >= 0) return evalNode(p, nullptr);
  int id = layerId(p.wp, p.bp);
  return tget(id, idxOf(p.stm, p.wk, p.bk));
}

static int solveLayer(u64 wp, u64 bp) {
  int id = ids[{wp, bp}];
  state[id] = 1;
  int NS = 2 * N * N;
  vector<uint8_t> val(NS, 3), cnt(NS, 0), dex(NS, 0);
  vector<int> succ; succ.reserve(NS * 4);
  vector<int> sstart(NS + 1, 0);
  vector<Mv> ms;
  vector<int> queue; queue.reserve(NS);
  for (int i = 0; i < NS; i++) {
    sstart[i] = (int)succ.size();
    int stm = i / (N * N), wk = (i / N) % N, bk = i % N;
    Pos p{wp, bp, wk, bk, stm, -1};
    if (!legalPos(p)) continue;
    genMoves(p, ms);
    bool win = false, dr = false; int nin = 0;
    for (auto& m : ms) {
      if (m.kind == PROMO) { win = true; continue; }
      if (m.kind == KMOVE) { succ.push_back(idxOf(m.c.stm, m.c.wk, m.c.bk)); nin++; continue; }
      int v = valueOf(m.c);
      if (v == 2) win = true; else if (v == 0) dr = true;
    }
    if (win) val[i] = 1;
    else if (nin == 0) val[i] = ms.empty() ? (inCheck(p) ? 2 : 0) : (dr ? 0 : 2);
    else { val[i] = 4; cnt[i] = nin; dex[i] = dr; }
    if (val[i] == 1 || val[i] == 2) queue.push_back(i);
  }
  sstart[NS] = (int)succ.size();
  // reverse edges
  vector<int> pstart(NS + 1, 0), pred(succ.size());
  for (int x : succ) pstart[x + 1]++;
  for (int i = 0; i < NS; i++) pstart[i + 1] += pstart[i];
  vector<int> fill(pstart.begin(), pstart.end() - 1);
  for (int i = 0; i < NS; i++) for (int k = sstart[i]; k < sstart[i + 1]; k++) pred[fill[succ[k]]++] = i;
  for (size_t qi = 0; qi < queue.size(); qi++) {
    int s = queue[qi];
    for (int k = pstart[s]; k < pstart[s + 1]; k++) {
      int pp = pred[k];
      if (val[pp] != 4) continue;
      if (val[s] == 2) { val[pp] = 1; queue.push_back(pp); }
      else if (--cnt[pp] == 0) { if (dex[pp]) val[pp] = 0; else { val[pp] = 2; queue.push_back(pp); } }
    }
  }
  vector<uint8_t> packed((NS + 3) / 4, 0);
  for (int i = 0; i < NS; i++) { int v = val[i] == 4 ? 0 : val[i]; packed[i >> 2] |= v << ((i & 3) * 2); }
  tabs[id].swap(packed);
  state[id] = 2;
  nSolved++;
  if (nSolved % 50000 == 0) fprintf(stderr, "solved %ld layers\n", nSolved);
  return id;
}

// ---------------- test ----------------
struct Cnt { long long place = 0, f1 = 0, f2 = 0, f3 = 0, one = 0, f4 = 0, half = 0, halfOne = 0; };
static int LISTMAX = 0;
static string sqName(int s) { char b[8]; snprintf(b, 8, "%c%d", 'a' + fileOf(s), rankOf(s) + 1); return b; }
static string posStr(const Pos& p) {
  string out = "K" + sqName(p.wk) + " k" + sqName(p.bk);
  for (u64 b = p.wp; b; b &= b - 1) out += " P" + sqName(__builtin_ctzll(b));
  for (u64 b = p.bp; b; b &= b - 1) out += " p" + sqName(__builtin_ctzll(b));
  return out;
}

// S = shuttler colour, F = freezer
static void testLayer(u64 wp, u64 bp, int S, Cnt& c, vector<Mv>& ms, vector<Mv>& ms2) {
  int F = 1 - S;
  u64 occ = wp | bp;
  u64 Sp = S == 0 ? wp : bp, Fp = S == 0 ? bp : wp;
  vector<char> safeS(N), safeF(N);
  for (int s = 0; s < N; s++) {
    safeS[s] = !((occ >> s) & 1) && !(ATT[F][s] & Fp);
    safeF[s] = !((occ >> s) & 1) && !(ATT[S][s] & Sp);
  }
  for (int z0 = 0; z0 < N; z0++) if (safeS[z0]) for (int i = 0; i < NNB[z0]; i++) {
    int z1 = NB[z0][i];
    if (z1 <= z0 || !safeS[z1]) continue;
    int z[2] = {z0, z1};
    for (int w0 = 0; w0 < N; w0++) {
      if (!safeF[w0] || DIST[w0][z0] < 2 || DIST[w0][z1] < 2) continue;
      c.place++;
      auto mk = [&](int a, int stm) { Pos p{wp, bp, 0, 0, stm, -1}; if (S == 0) { p.wk = z[a]; p.bk = w0; } else { p.bk = z[a]; p.wk = w0; } return p; };
      // (O1)/(U1)
      bool ok = true;
      for (int a = 0; a < 2 && ok; a++) {
        Pos p = mk(a, S);
        genMoves(p, ms);
        for (auto& m : ms) {
          if (m.kind == KMOVE && (S == 0 ? m.c.wk : m.c.bk) == z[1 - a]) continue;
          if (m.kind == PROMO) { ok = false; break; }
          if (valueOf(m.c) != 1) { ok = false; break; }
        }
      }
      if (!ok) continue;
      c.f1++;
      // (O2)
      vector<Pos> fr[2];
      for (int a = 0; a < 2 && ok; a++) {
        Pos p = mk(a, F);
        genMoves(p, ms);
        for (auto& m : ms) {
          if (m.kind == PROMO) { ok = false; break; }
          if (valueOf(m.c) != 1) fr[a].push_back(m.c);
        }
        if (fr[a].empty()) ok = false;
      }
      if (!ok) continue;
      c.f2++;
      // (O3)
      for (int a = 0; a < 2 && ok; a++) for (auto& q : fr[a]) {
        int nm; int v = evalNode(q, &nm);
        if (!(v == 2 && nm > 0)) { ok = false; break; }
      }
      if (!ok) continue;
      c.f3++;
      bool one = fr[0].size() == 1 && fr[1].size() == 1;
      if (one) c.one++;
      // (O4)
      bool rootEx[2];
      for (int a = 0; a < 2; a++) {
        rootEx[a] = true;
        for (auto q : fr[a]) {
          q.ep = -1; q.stm = F;
          if (!legalPos(q)) { rootEx[a] = false; break; }
          int nm; int v = evalNode(q, &nm);
          if (!(v == 2 && nm > 0)) { rootEx[a] = false; break; }
        }
      }
      if (rootEx[0] && rootEx[1]) {
        c.f4++;
        printf("EXACT %s shuttle %s-%s S=%c\n", posStr(mk(0, S)).c_str(), sqName(z0).c_str(), sqName(z1).c_str(), S ? 'b' : 'w');
      } else if (rootEx[0] || rootEx[1]) {
        c.half++;
        if (one) { c.halfOne++; if (c.halfOne <= LISTMAX) printf("HALFONE S=%c %s shuttle %s-%s zero-root %s\n", S ? 'b' : 'w', posStr(mk(0, S)).c_str(), sqName(z0).c_str(), sqName(z1).c_str(), sqName(z[rootEx[0] ? 0 : 1]).c_str()); }
      }
    }
  }
}

int main(int argc, char** argv) {
  string board = "cyl:7x6"; int f0 = 0, f1 = 3, maxw = 3, maxb = 3; bool evalMode = false;
  for (int i = 1; i < argc; i++) {
    if (!strcmp(argv[i], "--board")) board = argv[++i];
    else if (!strcmp(argv[i], "--files")) sscanf(argv[++i], "%d-%d", &f0, &f1);
    else if (!strcmp(argv[i], "--maxw")) maxw = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--maxb")) maxb = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--list")) LISTMAX = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--eval")) evalMode = true;
  }
  WRAP = board.substr(0, 3) == "cyl";
  sscanf(board.c_str() + board.find(':') + 1, "%dx%d", &W, &H);
  N = W * H;
  for (int s = 0; s < N; s++) {
    NNB[s] = 0;
    for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
      if (!df && !dr) continue;
      int t = sq(fileOf(s) + df, rankOf(s) + dr);
      if (t < 0) continue;
      bool dup = false; for (int k = 0; k < NNB[s]; k++) if (NB[s][k] == t) dup = true;
      if (!dup && t != s) NB[s][NNB[s]++] = t;
    }
    for (int c = 0; c < 2; c++) {
      ATT[c][s] = 0; int dir = c == 0 ? 1 : -1;
      for (int df = -1; df <= 1; df += 2) { int q = sq(fileOf(s) - df, rankOf(s) - dir); if (q >= 0 && rankOf(q) >= 1 && rankOf(q) <= H - 2) ATT[c][s] |= 1ULL << q; }
    }
  }
  for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) {
    int df = abs(fileOf(a) - fileOf(b)); if (WRAP) df = min(df, W - df);
    DIST[a][b] = max(df, abs(rankOf(a) - rankOf(b)));
  }
  if (evalMode) {
    char line[512];
    while (fgets(line, sizeof line, stdin)) {
      string L(line); while (!L.empty() && (L.back() == '\n' || L.back() == '\r')) L.pop_back();
      if (L.empty() || L[0] == '#') { printf("%s\n", L.c_str()); continue; }
      Pos p{0, 0, -1, -1, 0, -1}; char tok[16]; int n = 0; const char* q = L.c_str(); vector<string> toks;
      while (sscanf(q, "%15s%n", tok, &n) == 1) { toks.push_back(tok); q += n; }
      for (size_t k = 0; k + 2 < toks.size(); k++) {
        string t = toks[k]; int s = sq(t[1] - 'a', atoi(t.c_str() + 2) - 1);
        if (t[0] == 'K') p.wk = s; else if (t[0] == 'k') p.bk = s; else if (t[0] == 'P') p.wp |= 1ULL << s; else if (t[0] == 'p') p.bp |= 1ULL << s;
      }
      p.stm = toks[toks.size() - 2] == "w" ? 0 : 1;
      string e = toks.back(); p.ep = e == "-" ? -1 : sq(e[0] - 'a', atoi(e.c_str() + 1) - 1);
      char r = 'X';
      if (legalPos(p)) { int v = valueOf(p); r = v == 0 ? 'D' : ((v == 1) == (p.stm == 0) ? 'W' : 'L'); }
      printf("%s | %c\n", L.c_str(), r);
    }
    return 0;
  }
  // enumerate window squares: files f0..f1, ranks 2..H-1 (index 1..H-2)
  vector<int> win;
  for (int f = f0; f <= f1; f++) for (int r = 1; r <= H - 2; r++) win.push_back(sq(f, r));
  int M = (int)win.size();
  Cnt cu, co; vector<Mv> ms, ms2; long long nl = 0;
  // recursive enumeration of white then black subsets
  std::function<void(int, u64)> recW = [&](int start, u64 wp) {
    // choose black set
    std::function<void(int, u64)> rb = [&](int st, u64 bp) {
      nl++;
      layerId(wp, bp);
      testLayer(wp, bp, 0, cu, ms, ms2);
      testLayer(wp, bp, 1, co, ms, ms2);
      if (__builtin_popcountll(bp) == maxb) return;
      for (int k = st; k < M; k++) if (!((wp >> win[k]) & 1)) rb(k + 1, bp | 1ULL << win[k]);
    };
    rb(0, 0);
    if (__builtin_popcountll(wp) == maxw) return;
    for (int k = start; k < M; k++) recW(k + 1, wp | 1ULL << win[k]);
  };
  recW(0, 0);
  auto pr = [&](const char* nm, Cnt& c) {
    printf("RESULT %s board=%s files=%d-%d max=%d+%d layersTested=%lld placements=%lld F1=%lld F2=%lld F3=%lld one=%lld F4=%lld half=%lld halfOne=%lld\n",
           nm, board.c_str(), f0, f1, maxw, maxb, nl, c.place, c.f1, c.f2, c.f3, c.one, c.f4, c.half, c.halfOne);
  };
  pr("under", cu); pr("over", co);
  printf("layersSolved=%ld\n", nSolved);
  return 0;
}
