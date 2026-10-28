// Referee's own mini solver of the P model (first promotion wins, stalemate and infinite play draw) for positions with
// at most one white pawn and one black pawn, kings real.  Written from LOOPY Definition 1.5 and kings/SPEC.md only.
// No en passant (with one pawn per side blocked or alone no e.p. capture can ever arise: the only way a pawn double-steps
// is when the other side's pawn is gone or not on an adjacent file next to it).
// Build: c++ -O2 -std=c++17 -o pmini pmini.cpp ; usage: pmini cyl:6x6 < positions   (lines "Kd3 kd1 Pa2 pa3 w -")
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <string>
#include <vector>
#include <array>
using namespace std;
int W, H, N; bool CYL;
enum { U = 0, WIN = 1, LOSS = 2 };  // from White's point of view; U = draw (never resolved)
int fstep(int f, int d) { int x = f + d; if (CYL) return ((x % W) + W) % W; return (x < 0 || x >= W) ? -1 : x; }
bool adjk(int a, int b) { int fa = a % W, fb = b % W, df = abs(fa - fb); if (CYL) df = min(df, W - df); return df <= 1 && abs(a / W - b / W) <= 1; }
bool attackedByWP(int wp, int s) { if (wp < 0) return false; int f = wp % W, r = wp / W; for (int d = -1; d <= 1; d += 2) { int g = fstep(f, d); if (g >= 0 && r + 1 == s / W && g == s % W) return true; } return false; }
bool attackedByBP(int bp, int s) { if (bp < 0) return false; int f = bp % W, r = bp / W; for (int d = -1; d <= 1; d += 2) { int g = fstep(f, d); if (g >= 0 && r - 1 == s / W && g == s % W) return true; } return false; }
typedef vector<char> Layer;  // index ((stm*N + wk)*N + bk)
map<pair<int, int>, Layer> memo;
const Layer& solve(int wp, int bp);
// result of a move target, from White's view: returns U/WIN/LOSS; terminal if promoting
int look(int wp, int bp, int stm, int wk, int bk) { const Layer& L = solve(wp, bp); return L[((size_t)stm * N + wk) * N + bk]; }
bool legalPos(int wp, int bp, int wk, int bk) {
  if (wk == bk || adjk(wk, bk)) return false;
  if (wk == wp || wk == bp || bk == wp || bk == bp) return false;
  return true;
}
const Layer& solve(int wp, int bp) {
  auto key = make_pair(wp, bp);
  auto it = memo.find(key); if (it != memo.end()) return it->second;
  Layer L((size_t)2 * N * N, U);
  memo[key] = L;  // placeholder; replaced below (recursion only goes to strictly later layers)
  // enumerate moves per node: list of (kind, a, b, c): 0 terminal win for mover; 1 move inside layer to (wk',bk'); 2 to other layer value fixed
  struct Mv { int kind; int val; int nwk, nbk; };  // kind 0: fixed value val (WIN/LOSS from White's view); kind 1: in-layer node (stm flips)
  vector<vector<Mv>> mv((size_t)2 * N * N); vector<char> legal((size_t)2 * N * N, 0), inCheck((size_t)2 * N * N, 0);
  for (int stm = 0; stm < 2; stm++) for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) {
    if (!legalPos(wp, bp, wk, bk)) continue;
    // side not to move may not be in check
    if (stm == 0 && attackedByWP(wp, bk)) continue;
    if (stm == 1 && attackedByBP(bp, wk)) continue;
    size_t id = ((size_t)stm * N + wk) * N + bk; legal[id] = 1;
    bool chk = stm == 0 ? attackedByBP(bp, wk) : attackedByWP(wp, bk); inCheck[id] = chk;
    vector<Mv>& out = mv[id];
    int myk = stm == 0 ? wk : bk, ok = stm == 0 ? bk : wk;
    int mypawn = stm == 0 ? wp : bp, oppawn = stm == 0 ? bp : wp;
    // king moves
    for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
      if (!df && !dr) continue;
      int g = fstep(myk % W, df), r = myk / W + dr; if (g < 0 || r < 0 || r >= H) continue;
      int t = r * W + g;
      if (t == mypawn) continue; if (adjk(t, ok) || t == ok) continue;
      if (t == oppawn) {  // capture the enemy pawn: it is gone, so no enemy attacker remains
        int nwp = stm == 0 ? wp : -1, nbp = stm == 0 ? -1 : bp;
        int nwk = stm == 0 ? t : wk, nbk = stm == 0 ? bk : t;
        out.push_back({0, look(nwp, nbp, 1 - stm, nwk, nbk), 0, 0});
      } else {
        // target must not be attacked by the enemy pawn
        if (stm == 0 && attackedByBP(bp, t)) continue; if (stm == 1 && attackedByWP(wp, t)) continue;
        out.push_back({1, 0, stm == 0 ? t : wk, stm == 0 ? bk : t});
      }
    }
    // pawn moves
    if (mypawn >= 0) {
      int f = mypawn % W, r = mypawn / W; int dir = stm == 0 ? 1 : -1; int last = stm == 0 ? H - 1 : 0; int second = stm == 0 ? 1 : H - 2;
      auto occ = [&](int s) { return s == wk || s == bk || s == wp || s == bp; };
      auto afterOwnKingSafe = [&](int nwp, int nbp) { return stm == 0 ? !attackedByBP(nbp, wk) : !attackedByWP(nwp, bk); };
      // forward steps
      int s1 = (r + dir) * W + f;
      if (!occ(s1)) {
        if (r + dir == last) { if (afterOwnKingSafe(wp, bp)) out.push_back({0, stm == 0 ? WIN : LOSS, 0, 0}); }
        else { int nwp = stm == 0 ? s1 : wp, nbp = stm == 0 ? bp : s1; if (afterOwnKingSafe(nwp, nbp)) out.push_back({0, look(nwp, nbp, 1 - stm, wk, bk), 0, 0});
          if (r == second) { int s2 = (r + 2 * dir) * W + f; if (!occ(s2)) { int mwp = stm == 0 ? s2 : wp, mbp = stm == 0 ? bp : s2; if (afterOwnKingSafe(mwp, mbp)) out.push_back({0, look(mwp, mbp, 1 - stm, wk, bk), 0, 0}); } } }
      }
      // captures of the enemy pawn
      for (int d = -1; d <= 1; d += 2) { int g = fstep(f, d); if (g < 0) continue; int t = (r + dir) * W + g;
        if (t == oppawn) {
          if (r + dir == last) { if (afterOwnKingSafe(wp, bp)) out.push_back({0, stm == 0 ? WIN : LOSS, 0, 0}); }
          else { int nwp = stm == 0 ? t : -1, nbp = stm == 0 ? -1 : t; if (afterOwnKingSafe(nwp, nbp)) out.push_back({0, look(nwp, nbp, 1 - stm, wk, bk), 0, 0}); }
        } }
    }
  }
  // value iteration to the least fixed point
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
  memo[key] = L;
  return memo[key];
}
int main(int argc, char** argv) {
  char kind[8]; sscanf(argv[1], "%7[a-z]:%dx%d", kind, &W, &H); CYL = !strcmp(kind, "cyl"); N = W * H;
  char line[512];
  while (fgets(line, sizeof line, stdin)) {
    int wk = -1, bk = -1, wp = -1, bp = -1, stm = 0; int np = 0; string org(line); while (!org.empty() && (org.back() == '\n')) org.pop_back();
    char* p = strtok(line, " \n"); int ntok = 0; vector<string> toks; while (p) { toks.push_back(p); p = strtok(NULL, " \n"); }
    for (auto& t : toks) {
      if (t == "w") stm = 0; else if (t == "b") stm = 1; else if (t == "-") {}
      else { int f = t[1] - 'a', r = atoi(t.c_str() + 2) - 1; int s = r * W + f;
        if (t[0] == 'K') wk = s; else if (t[0] == 'k') bk = s; else if (t[0] == 'P') wp = s; else if (t[0] == 'p') bp = s; }
    }
    (void)np; (void)ntok;
    int v = look(wp, bp, stm, wk, bk);
    printf("%s | %c\n", org.c_str(), v == WIN ? 'W' : v == LOSS ? 'L' : 'D');
  }
  return 0;
}
