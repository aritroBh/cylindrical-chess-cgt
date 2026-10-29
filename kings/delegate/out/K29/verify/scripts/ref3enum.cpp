// ref3.cpp -- referee's own solver for K + pawns vs K + pawns, written from kings/SPEC.md only.
// Models:  default = P (first promotion wins for the promoter, real kings);  --frozen = kings may not move
// (any king move loses at once for the mover), promotion wins at once.
// Usage: ref3 --board cyl:7x6|flat:7x6 [--frozen] [--noep] < positions > results   ("<pos> | X" with X in W/L/D/X,
// White's point of view, one letter for the stated side to move)
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <unordered_map>
#include <iostream>
#include <sstream>
using namespace std;
typedef uint64_t u64;
static int W, H, N, WRAP = 1, FROZEN = 0, EPON = 1;
static int sqf(int s) { return s % W; }
static int sqr(int s) { return s / W; }
static int mk(int f, int r) { // -1 if off board
  if (r < 0 || r >= H) return -1;
  if (WRAP) f = ((f % W) + W) % W; else if (f < 0 || f >= W) return -1;
  return r * W + f;
}
static bool adjK(int a, int b) {
  for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
    if (!df && !dr) continue;
    if (mk(sqf(a) + df, sqr(a) + dr) == b) return true;
  }
  return false;
}
// is square s attacked by a pawn of colour c (0 white, 1 black) given pawn masks
static bool pawnAtt(int s, int c, u64 wp, u64 bp) {
  int dir = c == 0 ? 1 : -1;
  u64 m = c == 0 ? wp : bp;
  for (int df = -1; df <= 1; df += 2) {
    int q = mk(sqf(s) - df, sqr(s) - dir); // pawn standing at q attacks s
    if (q >= 0 && ((m >> q) & 1)) return true;
  }
  return false;
}
struct Key { u64 wp, bp; int ep; bool operator==(const Key&o) const { return wp==o.wp&&bp==o.bp&&ep==o.ep; } };
struct KH { size_t operator()(const Key&k) const { return k.wp * 0x9E3779B97F4A7C15ULL ^ (k.bp + 0x7F4A7C15ULL) * 0xC2B2AE3D27D4EB4FULL ^ (size_t)(k.ep + 2) * 0x165667B19E3779F9ULL; } };
// table values: 0 = draw/unknown, 1 = mover wins, 2 = mover loses, 3 = illegal
typedef vector<uint8_t> Table; // index (stm*N + wk)*N + bk
static unordered_map<Key, Table, KH> memo;
static long layersSolved = 0;

struct Move { int kind; // 0 = terminal mover wins, 1 = terminal mover loses, 2 = layer move (pawn), 3 = king move
  int nwk, nbk; Key nk; };

// generate legal moves of side `us` in (wk,bk,wp,bp,ep)
static void genMoves(int us, int wk, int bk, u64 wp, u64 bp, int ep, vector<Move>& out) {
  out.clear();
  int ok = us == 0 ? wk : bk, ek = us == 0 ? bk : wk;
  u64 own = us == 0 ? wp : bp, opp = us == 0 ? bp : wp;
  int dir = us == 0 ? 1 : -1;
  int last = us == 0 ? H - 1 : 0;
  int second = us == 0 ? 1 : H - 2;
  // king
  for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
    if (!df && !dr) continue;
    int n = mk(sqf(ok) + df, sqr(ok) + dr);
    if (n < 0) continue;
    if ((own >> n) & 1) continue;
    if (n == ek || adjK(n, ek)) continue;
    u64 nopp = opp & ~(1ULL << n);
    u64 nwp = us == 0 ? own : nopp, nbp = us == 0 ? nopp : own;
    if (pawnAtt(n, 1 - us, nwp, nbp)) continue;
    Move m; m.kind = FROZEN ? 1 : 3; m.nwk = us == 0 ? n : wk; m.nbk = us == 0 ? bk : n;
    m.nk = Key{nwp, nbp, -1};
    out.push_back(m);
  }
  // pawns
  u64 occ = wp | bp | (1ULL << wk) | (1ULL << bk);
  for (int s = 0; s < N; s++) if ((own >> s) & 1) {
    int f = sqf(s), r = sqr(s);
    // pushes
    int t1 = mk(f, r + dir);
    if (t1 >= 0 && !((occ >> t1) & 1)) {
      u64 nown = (own & ~(1ULL << s));
      bool promo = sqr(t1) == last;
      if (!promo) nown |= 1ULL << t1;
      u64 nwp = us == 0 ? nown : opp, nbp = us == 0 ? opp : nown;
      if (!pawnAtt(ok, 1 - us, nwp, nbp)) {
        Move m; m.nwk = wk; m.nbk = bk;
        if (promo) { m.kind = 0; m.nk = Key{0,0,-1}; }
        else { m.kind = 2; m.nk = Key{nwp, nbp, -1}; }
        out.push_back(m);
      }
      // double step
      if (r == second && !promo) {
        int t2 = mk(f, r + 2 * dir);
        if (t2 >= 0 && !((occ >> t2) & 1)) {
          u64 nown2 = (own & ~(1ULL << s)) | (1ULL << t2);
          u64 nwp2 = us == 0 ? nown2 : opp, nbp2 = us == 0 ? opp : nown2;
          if (!pawnAtt(ok, 1 - us, nwp2, nbp2)) {
            Move m2; m2.nwk = wk; m2.nbk = bk; m2.kind = 2;
            int epn = EPON ? t1 : -1;
            if (epn >= 0) { // record only if an enemy pawn can capture it
              bool can = false;
              for (int d2 = -1; d2 <= 1; d2 += 2) {
                int q = mk(f + d2, r + 2 * dir);
                if (q >= 0 && ((opp >> q) & 1)) can = true;
              }
              if (!can) epn = -1;
            }
            m2.nk = Key{nwp2, nbp2, epn};
            out.push_back(m2);
          }
        }
      }
    }
    // captures
    for (int d2 = -1; d2 <= 1; d2 += 2) {
      int t = mk(f + d2, r + dir);
      if (t < 0) continue;
      bool epcap = (ep >= 0 && t == ep && !((occ >> t) & 1));
      if (!(((opp >> t) & 1) || epcap)) continue;
      u64 nown = own & ~(1ULL << s);
      u64 nopp = opp;
      if (epcap) { int vs = mk(sqf(t), sqr(s)); nopp &= ~(1ULL << vs); }
      else nopp &= ~(1ULL << t);
      bool promo = sqr(t) == last;
      if (!promo) nown |= 1ULL << t;
      u64 nwp = us == 0 ? nown : nopp, nbp = us == 0 ? nopp : nown;
      if (pawnAtt(ok, 1 - us, nwp, nbp)) continue;
      Move m; m.nwk = wk; m.nbk = bk;
      if (promo) { m.kind = 0; m.nk = Key{0,0,-1}; }
      else { m.kind = 2; m.nk = Key{nwp, nbp, -1}; }
      out.push_back(m);
    }
  }
}

static const Table& solve(const Key& k);

static Table compute(const Key& k) {
  layersSolved++;
  Table tab(2 * N * N, 3);
  vector<Move> mv;
  // per state move info: for in-layer children store indices
  struct St { int idx; vector<int> kids; bool anyDraw; bool anyMove; };
  vector<St> sts;
  vector<int> stOf(2 * N * N, -1);
  for (int stm = 0; stm < 2; stm++) {
    if (k.ep >= 0) {
      // ep layer: stm is the side that can capture. ep target rank tells who just moved.
      int stepper = (sqr(k.ep) == 2 || (H - 1 - sqr(k.ep)) > sqr(k.ep)) ? 0 : 1; // white steps onto rank index 2 -> skipped index 2
      stepper = sqr(k.ep) == 2 ? 0 : 1;
      if (stm == stepper) continue;
    }
    for (int wk = 0; wk < N; wk++) {
      if (((k.wp | k.bp) >> wk) & 1) continue;
      for (int bk = 0; bk < N; bk++) {
        if (bk == wk || (((k.wp | k.bp) >> bk) & 1)) continue;
        if (adjK(wk, bk)) continue;
        // side not to move must not be in check
        int nm = 1 - stm; int nmk = nm == 0 ? wk : bk;
        if (pawnAtt(nmk, stm, k.wp, k.bp)) continue;
        // ep consistency: skip
        tab[(stm * N + wk) * N + bk] = 0;
      }
    }
  }
  // first pass: resolve external, collect in-layer kids
  for (int stm = 0; stm < 2; stm++) for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) {
    int idx = (stm * N + wk) * N + bk;
    if (tab[idx] == 3) continue;
    genMoves(stm, wk, bk, k.wp, k.bp, k.ep, mv);
    int ok = stm == 0 ? wk : bk;
    if (mv.empty()) {
      bool chk = pawnAtt(ok, 1 - stm, k.wp, k.bp);
      tab[idx] = chk ? 2 : 0; // mate: loss; stalemate: draw
      continue;
    }
    St s; s.idx = idx; s.anyDraw = false; s.anyMove = true;
    bool win = false;
    for (auto& m : mv) {
      if (m.kind == 0) { win = true; break; }
      if (m.kind == 1) { continue; } // mover loses at once: never better than a loss
      if (m.kind == 2) {
        const Table& ct = solve(m.nk);
        uint8_t v = ct[((1 - stm) * N + m.nwk) * N + m.nbk];
        if (v == 3) { fprintf(stderr, "internal: child illegal\n"); exit(2); }
        if (v == 2) { win = true; break; }
        if (v == 0) s.anyDraw = true;
        continue;
      }
      // king move (kind 3): same layer iff pawns unchanged and this layer has no e.p. right
      if (!(m.nk.wp == k.wp && m.nk.bp == k.bp && k.ep == -1)) {
        const Table& ct = solve(m.nk);
        uint8_t v = ct[((1 - stm) * N + m.nwk) * N + m.nbk];
        if (v == 2) { win = true; break; }
        if (v == 0) s.anyDraw = true;
        continue;
      }
      s.kids.push_back(((1 - stm) * N + m.nwk) * N + m.nbk);
    }
    if (win) { tab[idx] = 1; continue; }
    if (s.kids.empty() && !s.anyDraw) { tab[idx] = 2; continue; } // every move loses
    if (s.kids.empty() && s.anyDraw) { tab[idx] = 0; continue; }
    stOf[idx] = sts.size(); sts.push_back(s);
  }
  // fixpoint
  bool ch = true;
  while (ch) {
    ch = false;
    for (auto& s : sts) {
      if (tab[s.idx] != 0) continue;
      bool win = false, allw = !s.anyDraw;
      for (int c : s.kids) {
        uint8_t v = tab[c];
        if (v == 2) { win = true; break; }
        if (v != 1) allw = false;
      }
      if (win) { tab[s.idx] = 1; ch = true; }
      else if (allw) { tab[s.idx] = 2; ch = true; }
    }
  }
  return tab;
}
static const Table& solve(const Key& k) {
  auto it = memo.find(k);
  if (it != memo.end()) return it->second;
  Table t = compute(k);
  auto r = memo.emplace(k, std::move(t));
  return r.first->second;
}

static int parseSq(const string& s) {
  int f = s[0] - 'a', r = atoi(s.c_str() + 1) - 1;
  if (f < 0 || f >= W || r < 0 || r >= H) return -2;
  return r * W + f;
}
// ---- K29 referee addition: own enumerator of bare groups with P value (L,W) (mover loses with either side to move),
// ---- kings and Z-pawns on the files of F_Z (arc starting at file zs, width fz), pawns on ranks rlo..rhi (1-based),
// ---- at most zw white and zb black pawns, at least one pawn.  Solver above is the K23 referee's ref3, unchanged.
static bool hasPromo(int us, int wk, int bk, u64 wp, u64 bp, int ep) {
  vector<Move> mv; genMoves(us, wk, bk, wp, bp, ep, mv);
  for (auto& m : mv) if (m.kind == 0) return true;
  return false;
}
// does the mover (stm) lose within 2 plies?  mated (0 plies), or every legal move is a non-promotion after which the
// opponent has a promotion.  (No legal move and not in check = stalemate = draw, so not a loss.)
static bool loses2(int stm, int wk, int bk, u64 wp, u64 bp) {
  vector<Move> mv; genMoves(stm, wk, bk, wp, bp, -1, mv);
  int ok = stm == 0 ? wk : bk;
  if (mv.empty()) return pawnAtt(ok, 1 - stm, wp, bp);
  for (auto& m : mv) {
    if (m.kind == 0) return false;
    if (!hasPromo(1 - stm, m.nwk, m.nbk, m.nk.wp, m.nk.bp, m.nk.ep)) return false;
  }
  return true;
}
int main(int argc, char** argv) {
  string board = "cyl:7x6"; int zs = 0, fz = 3, zw = 2, zb = 2, rlo = 2, rhi = 5;
  for (int i = 1; i < argc; i++) {
    if (!strcmp(argv[i], "--board") && i + 1 < argc) board = argv[++i];
    else if (!strcmp(argv[i], "--zs")) zs = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--fz")) fz = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--zw")) zw = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--zb")) zb = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--rlo")) rlo = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--rhi")) rhi = atoi(argv[++i]);
  }
  WRAP = board.substr(0, 3) == "cyl";
  sscanf(board.c_str() + 4, "%dx%d", &W, &H);
  N = W * H;
  vector<int> files; for (int k = 0; k < fz; k++) files.push_back(WRAP ? (zs + k) % W : zs + k);
  vector<int> psq; for (int f : files) for (int r = rlo - 1; r <= rhi - 1; r++) psq.push_back(r * W + f);
  vector<int> ksq; for (int f : files) for (int r = 0; r < H; r++) ksq.push_back(r * W + f);
  int ns = psq.size();
  // subsets of pawn squares by size
  auto subsetsUpTo = [&](int mx) { vector<u64> v; vector<int> idx;
    // recursive generation of all subsets with <= mx elements (as masks of squares)
    function<void(int, int, u64)> rec = [&](int start, int cnt, u64 m) { v.push_back(m); if (cnt == mx) return;
      for (int i = start; i < ns; i++) rec(i + 1, cnt + 1, m | (1ULL << psq[i])); };
    rec(0, 0, 0); return v; };
  vector<u64> ws = subsetsUpTo(zw), bs = subsetsUpTo(zb);
  long ncfg = 0, ncand = 0, nl2w = 0, nl2b = 0, nl2both = 0, ntot = 0;
  for (u64 wp : ws) for (u64 bp : bs) {
    if ((wp | bp) == 0 || (wp & bp)) continue;
    ncfg++;
    const Table& tb = solve(Key{wp, bp, -1});
    for (int wk : ksq) { if (((wp | bp) >> wk) & 1) continue;
      for (int bk : ksq) { if (((wp | bp) >> bk) & 1) continue; if (bk == wk) continue;
        ntot++;
        uint8_t a = tb[(0 * N + wk) * N + bk], b = tb[(1 * N + wk) * N + bk];
        if (a != 2 || b != 2) continue;
        ncand++;
        bool lw = loses2(0, wk, bk, wp, bp), lb = loses2(1, wk, bk, wp, bp);
        if (lw) nl2w++; if (lb) nl2b++; if (lw && lb) nl2both++;
        // print group
        char buf[400]; buf[0] = 0; char t[8];
        auto sqn = [&](int s, char* o) { o[0] = 'a' + s % W; o[1] = '1' + s / W; o[2] = 0; };
        sqn(wk, t); strcat(buf, "K"); strcat(buf, t);
        for (int s = 0; s < N; s++) if ((wp >> s) & 1) { sqn(s, t); strcat(buf, " P"); strcat(buf, t); }
        sqn(bk, t); strcat(buf, " k"); strcat(buf, t);
        for (int s = 0; s < N; s++) if ((bp >> s) & 1) { sqn(s, t); strcat(buf, " p"); strcat(buf, t); }
        printf("%s | %d %d\n", buf, (int)lw, (int)lb);
      } }
  }
  fprintf(stderr, "pawn configs %ld, king placements tested %ld, candidates (L,W) %ld, loses-within-2-plies: white %ld black %ld both %ld, layers solved %ld\n",
          ncfg, ntot, ncand, nl2w, nl2b, nl2both, layersSolved);
  return 0;
}
