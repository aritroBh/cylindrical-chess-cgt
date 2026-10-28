// Referee's own P-model solver, general pawn sets (no e.p.: valid only when no pawn can ever stand next to an enemy pawn's
// double-step file; true for the tested positions, whose context pawns are on file g and group pawns on files a-d).
// Build: c++ -O2 -std=c++17 -o pmini2 pmini2.cpp ; usage: pmini2 flat:8x6 < positions
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <string>
#include <vector>
using namespace std;
typedef uint64_t u64;
int W, H, N; bool CYL;
enum { U = 0, WIN = 1, LOSS = 2 };
int fstep(int f, int d) { int x = f + d; if (CYL) return ((x % W) + W) % W; return (x < 0 || x >= W) ? -1 : x; }
vector<vector<char>> ADJ;
u64 attW[64], attB[64];  // squares attacked by a white / black pawn on s
u64 attackedBy(u64 mask, int colour) { u64 a = 0; for (int s = 0; s < N; s++) if (mask >> s & 1) a |= colour == 0 ? attW[s] : attB[s]; return a; }
struct Mv { int kind; int val; int nwk, nbk; };
typedef vector<char> Layer;
map<pair<u64, u64>, Layer> memo;
const Layer& solve(u64 wp, u64 bp);
int look(u64 wp, u64 bp, int stm, int wk, int bk) { const Layer& L = solve(wp, bp); return L[((size_t)stm * N + wk) * N + bk]; }
const Layer& solve(u64 wp, u64 bp) {
  auto key = make_pair(wp, bp);
  auto it = memo.find(key); if (it != memo.end()) return it->second;
  Layer L((size_t)2 * N * N, U);
  u64 aW = attackedBy(wp, 0), aB = attackedBy(bp, 1), occP = wp | bp;
  vector<vector<Mv>> mv((size_t)2 * N * N); vector<char> legal((size_t)2 * N * N, 0), inCheck((size_t)2 * N * N, 0);
  for (int stm = 0; stm < 2; stm++) for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) {
    if (wk == bk || ADJ[wk][bk]) continue;
    if ((occP >> wk & 1) || (occP >> bk & 1)) continue;
    if (stm == 0 && (aW >> bk & 1)) continue;
    if (stm == 1 && (aB >> wk & 1)) continue;
    size_t id = ((size_t)stm * N + wk) * N + bk; legal[id] = 1;
    inCheck[id] = stm == 0 ? (aB >> wk & 1) : (aW >> bk & 1);
    vector<Mv>& out = mv[id];
    int myk = stm == 0 ? wk : bk, ok = stm == 0 ? bk : wk;
    u64 mine = stm == 0 ? wp : bp, opp = stm == 0 ? bp : wp;
    for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
      if (!df && !dr) continue;
      int g = fstep(myk % W, df), r = myk / W + dr; if (g < 0 || r < 0 || r >= H) continue;
      int t = r * W + g;
      if (mine >> t & 1) continue; if (ADJ[t][ok]) continue;
      if (opp >> t & 1) {
        u64 nopp = opp & ~(1ULL << t);
        u64 att = stm == 0 ? attackedBy(nopp, 1) : attackedBy(nopp, 0);
        if (att >> t & 1) continue;
        u64 nwp = stm == 0 ? wp : nopp, nbp = stm == 0 ? nopp : bp;
        out.push_back({0, look(nwp, nbp, 1 - stm, stm == 0 ? t : wk, stm == 0 ? bk : t), 0, 0});
      } else {
        if (stm == 0 && (aB >> t & 1)) continue; if (stm == 1 && (aW >> t & 1)) continue;
        out.push_back({1, 0, stm == 0 ? t : wk, stm == 0 ? bk : t});
      }
    }
    int dir = stm == 0 ? 1 : -1, last = stm == 0 ? H - 1 : 0, second = stm == 0 ? 1 : H - 2;
    auto occ = [&](int s) { return s == wk || s == bk || (occP >> s & 1); };
    for (int p = 0; p < N; p++) if (mine >> p & 1) {
      int f = p % W, r = p / W;
      auto kingSafe = [&](u64 nwp, u64 nbp) { return stm == 0 ? !(attackedBy(nbp, 1) >> wk & 1) : !(attackedBy(nwp, 0) >> bk & 1); };
      int s1 = (r + dir) * W + f;
      if (!occ(s1)) {
        if (r + dir == last) { if (kingSafe(wp, bp)) out.push_back({0, stm == 0 ? WIN : LOSS, 0, 0}); }
        else {
          u64 nm = (mine & ~(1ULL << p)) | (1ULL << s1);
          u64 nwp = stm == 0 ? nm : wp, nbp = stm == 0 ? bp : nm;
          if (kingSafe(nwp, nbp)) out.push_back({0, look(nwp, nbp, 1 - stm, wk, bk), 0, 0});
          if (r == second) { int s2 = (r + 2 * dir) * W + f; if (!occ(s2)) {
            u64 nm2 = (mine & ~(1ULL << p)) | (1ULL << s2); u64 mwp = stm == 0 ? nm2 : wp, mbp = stm == 0 ? bp : nm2;
            if (kingSafe(mwp, mbp)) out.push_back({0, look(mwp, mbp, 1 - stm, wk, bk), 0, 0}); } }
        }
      }
      for (int d = -1; d <= 1; d += 2) { int g = fstep(f, d); if (g < 0) continue; int t = (r + dir) * W + g;
        if (opp >> t & 1) {
          if (r + dir == last) { if (kingSafe(wp, bp)) out.push_back({0, stm == 0 ? WIN : LOSS, 0, 0}); }
          else {
            u64 nopp = opp & ~(1ULL << t); u64 nm = (mine & ~(1ULL << p)) | (1ULL << t);
            u64 nwp = stm == 0 ? nm : nopp, nbp = stm == 0 ? nopp : nm;
            if (kingSafe(nwp, nbp)) out.push_back({0, look(nwp, nbp, 1 - stm, wk, bk), 0, 0});
          }
        } }
    }
  }
  bool ch = true;
  while (ch) {
    ch = false;
    for (int stm = 0; stm < 2; stm++) for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) {
      size_t id = ((size_t)stm * N + wk) * N + bk; if (!legal[id] || L[id] != U) continue;
      vector<Mv>& out = mv[id];
      int mine = stm == 0 ? WIN : LOSS, theirs = stm == 0 ? LOSS : WIN;
      bool anyWin = false, allLose = true;
      for (auto& m : out) {
        int v = m.kind == 0 ? m.val : L[((size_t)(1 - stm) * N + m.nwk) * N + m.nbk];
        if (v == mine) anyWin = true; if (v != theirs) allLose = false;
      }
      int nv = U;
      if (anyWin) nv = mine; else if (out.empty()) { nv = inCheck[id] ? theirs : U; } else if (allLose) nv = theirs;
      if (nv != U) { L[id] = nv; ch = true; }
    }
  }
  return memo[key] = L;
}
int main(int argc, char** argv) {
  char kind[8]; sscanf(argv[1], "%7[a-z]:%dx%d", kind, &W, &H); CYL = !strcmp(kind, "cyl"); N = W * H;
  ADJ.assign(N, vector<char>(N, 0));
  for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) { int df = abs(a % W - b % W); if (CYL) df = min(df, W - df); ADJ[a][b] = df <= 1 && abs(a / W - b / W) <= 1; }
  for (int s = 0; s < N; s++) { attW[s] = attB[s] = 0; int f = s % W, r = s / W;
    for (int d = -1; d <= 1; d += 2) { int g = fstep(f, d); if (g < 0) continue; if (r + 1 < H) attW[s] |= 1ULL << ((r + 1) * W + g); if (r - 1 >= 0) attB[s] |= 1ULL << ((r - 1) * W + g); } }
  char line[512];
  while (fgets(line, sizeof line, stdin)) {
    string org(line); while (!org.empty() && org.back() == '\n') org.pop_back();
    int wk = -1, bk = -1, stm = 0; u64 wp = 0, bp = 0;
    char* p = strtok(line, " \n"); vector<string> toks; while (p) { toks.push_back(p); p = strtok(NULL, " \n"); }
    for (auto& t : toks) {
      if (t == "w") stm = 0; else if (t == "b") stm = 1; else if (t == "-") {}
      else { int f = t[1] - 'a', r = atoi(t.c_str() + 2) - 1; int s = r * W + f;
        if (t[0] == 'K') wk = s; else if (t[0] == 'k') bk = s; else if (t[0] == 'P') wp |= 1ULL << s; else if (t[0] == 'p') bp |= 1ULL << s; }
    }
    int v = look(wp, bp, stm, wk, bk);
    printf("%s | %c\n", org.c_str(), v == WIN ? 'W' : v == LOSS ? 'L' : 'D'); fflush(stdout);
  }
  fprintf(stderr, "layers solved: %zu\n", memo.size());
  return 0;
}
