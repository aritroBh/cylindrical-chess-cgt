// ref3pv.cpp (K63) = ref3m.cpp (K23 referee) plus a resolution-order table and option --pv MAXPLY, which prints one
// optimal line per input position (winner: child resolved first; loser: child resolved last). Marked K63; the
// game logic is unchanged.
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
static int W, H, N, WRAP = 1, FROZEN = 0, EPON = 1, MOVES = 0;
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
static unordered_map<Key, vector<uint32_t>, KH> ordmemo;  // K63
static uint32_t CLK = 1;  // K63: global resolution counter
static int PV = 0;  // K63
static long layersSolved = 0;

struct Move { int kind; // 0 = terminal mover wins, 1 = terminal mover loses, 2 = layer move (pawn), 3 = king move
  int nwk, nbk; Key nk; int from = -1, to = -1; };  // K63: from/to squares of a pawn move (for printing promotions)

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
        Move m; m.nwk = wk; m.nbk = bk; m.from = s; m.to = t1;  // K63
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
      Move m; m.nwk = wk; m.nbk = bk; m.from = s; m.to = t;  // K63
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
  vector<uint32_t> ordv(2 * N * N, 0);  // K63
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
      ordv[idx] = CLK++;  // K63
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
    if (win) { tab[idx] = 1; ordv[idx] = CLK++; continue; }  // K63: order
    if (s.kids.empty() && !s.anyDraw) { tab[idx] = 2; ordv[idx] = CLK++; continue; } // every move loses
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
      if (win) { tab[s.idx] = 1; ch = true; ordv[s.idx] = CLK++; }
      else if (allw) { tab[s.idx] = 2; ch = true; ordv[s.idx] = CLK++; }
    }
  }
  if (PV) ordmemo.emplace(k, std::move(ordv));  // K63
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
int main(int argc, char** argv) {
  string board = "cyl:7x6";
  for (int i = 1; i < argc; i++) {
    if (!strcmp(argv[i], "--board") && i + 1 < argc) board = argv[++i];
    else if (!strcmp(argv[i], "--frozen")) FROZEN = 1;
    else if (!strcmp(argv[i], "--noep")) EPON = 0;
    else if (!strcmp(argv[i], "--moves")) MOVES = 1;
    else if (!strcmp(argv[i], "--pv") && i + 1 < argc) PV = atoi(argv[++i]);  // K63
  }
  WRAP = board.substr(0, 3) == "cyl";
  sscanf(board.c_str() + 4, "%dx%d", &W, &H);
  N = W * H;
  string line;
  while (getline(cin, line)) {
    if (line.empty() || line[0] == '#') { puts(line.c_str()); continue; }
    istringstream is(line); vector<string> t; string x; while (is >> x) t.push_back(x);
    int wk = -1, bk = -1; u64 wp = 0, bp = 0; bool bad = false;
    int stm = 0, ep = -1;
    size_t nt = t.size();
    string epS = t[nt - 1], stmS = t[nt - 2];
    stm = stmS == "b";
    if (epS != "-") ep = parseSq(epS);
    for (size_t i = 0; i + 2 < nt; i++) {
      char c = t[i][0]; int s = parseSq(t[i].substr(1));
      if (s < 0) { bad = true; break; }
      u64 bit = 1ULL << s;
      if ((wp | bp | (wk >= 0 ? 1ULL << wk : 0) | (bk >= 0 ? 1ULL << bk : 0)) & bit) { bad = true; break; }
      if (c == 'K') wk = s; else if (c == 'k') bk = s; else if (c == 'P') { wp |= bit; if (sqr(s) == 0 || sqr(s) == H - 1) bad = true; }
      else if (c == 'p') { bp |= bit; if (sqr(s) == 0 || sqr(s) == H - 1) bad = true; }
    }
    char res = 'X';
    if (!bad && wk >= 0 && bk >= 0 && !adjK(wk, bk)) {
      int nmk = stm == 0 ? bk : wk;
      if (!pawnAtt(nmk, stm, wp, bp)) {
        const Table& tb = solve(Key{wp, bp, ep});
        uint8_t v = tb[(stm * N + wk) * N + bk];
        if (v == 3) res = 'X';
        else if (v == 0) res = 'D';
        else { bool mw = v == 1; bool white = (stm == 0) == mw; res = white ? 'W' : 'L'; }
      }
    }
    printf("%s | %c", line.c_str(), res);
    if (MOVES && res != 'X') {
      vector<Move> mv; genMoves(stm, wk, bk, wp, bp, ep, mv);
      for (auto& m : mv) {
        char v; // value from White's view
        if (m.kind == 0) v = stm == 0 ? 'W' : 'L';
        else if (m.kind == 1) v = stm == 0 ? 'L' : 'W';
        else {
          Key nk = m.nk; const Table& ct = solve(nk);
          uint8_t cv = ct[((1 - stm) * N + m.nwk) * N + m.nbk];
          if (cv == 0) v = 'D'; else { bool mw = cv == 1; bool white = ((1 - stm) == 0) == mw; v = white ? 'W' : 'L'; }
        }
        // describe the move
        string d;
        if (m.nwk != wk || m.nbk != bk) { int from = stm == 0 ? wk : bk, to = stm == 0 ? m.nwk : m.nbk;
          d = string("K") + char('a' + sqf(from)) + char('1' + sqr(from)) + char('a' + sqf(to)) + char('1' + sqr(to)); }
        else if (m.kind == 0) d = "promo";
        else {
          u64 before = stm == 0 ? wp : bp, after = stm == 0 ? m.nk.wp : m.nk.bp;
          u64 gone = before & ~after, came = after & ~before; int a = __builtin_ctzll(gone ? gone : 1);
          int b = came ? __builtin_ctzll(came) : -1;
          d = string("P") + char('a' + sqf(a)) + char('1' + sqr(a)) + (b >= 0 ? string(1, char('a' + sqf(b))) + char('1' + sqr(b)) : string("=Q"));
        }
        printf(" %s:%c", d.c_str(), v);
      }
    }
    if (PV && (res == 'W' || res == 'L')) {  // K63: one optimal line by resolution order
      printf(" | line:");
      int cwk = wk, cbk = bk, cstm = stm; Key ck{wp, bp, ep};
      for (int ply = 0; ply < PV; ply++) {
        const Table& tb = solve(ck); int idx = (cstm * N + cwk) * N + cbk; uint8_t v = tb[idx];
        vector<Move> mv; genMoves(cstm, cwk, cbk, ck.wp, ck.bp, ck.ep, mv);
        if (mv.empty()) { printf(" (%s)", pawnAtt(cstm == 0 ? cwk : cbk, 1 - cstm, ck.wp, ck.bp) ? "mate" : "stalemate"); break; }
        if (v != 1 && v != 2) { printf(" (draw)"); break; }
        int best = -1; uint32_t bo = 0; bool promo = false;
        for (int j = 0; j < (int)mv.size(); j++) {
          Move& m = mv[j];
          if (m.kind == 0) { if (v == 1) { best = j; promo = true; break; } continue; }
          const Table& ct = solve(m.nk); int ci = ((1 - cstm) * N + m.nwk) * N + m.nbk; uint32_t co = ordmemo[m.nk][ci];
          if (v == 1 && ct[ci] == 2 && (best < 0 || co < bo)) { best = j; bo = co; }
          if (v == 2 && (best < 0 || co > bo)) { best = j; bo = co; }
        }
        Move m = mv[best];
        string d;
        if (m.nwk != cwk || m.nbk != cbk) { int from = cstm == 0 ? cwk : cbk, to = cstm == 0 ? m.nwk : m.nbk;
          d = string(cstm == 0 ? "K" : "k") + char('a' + sqf(from)) + char('1' + sqr(from)) + char('a' + sqf(to)) + char('1' + sqr(to));
          u64 opp0 = cstm == 0 ? ck.bp : ck.wp, opp1 = cstm == 0 ? m.nk.bp : m.nk.wp; if (opp0 != opp1) d += "x"; }
        else if (promo) {  // K63: name the promoting pawn
          d = string(cstm == 0 ? "P" : "p") + char('a' + sqf(m.from)) + char('1' + sqr(m.from)) + char('a' + sqf(m.to)) + char('1' + sqr(m.to)) + "=promotes";
        }
        else {
          u64 before = cstm == 0 ? ck.wp : ck.bp, after = promo ? 0 : (cstm == 0 ? m.nk.wp : m.nk.bp);
          u64 gone = before & ~after, came = after & ~before; int a = __builtin_ctzll(gone ? gone : 1);
          int b = came ? __builtin_ctzll(came) : -1;
          d = string(cstm == 0 ? "P" : "p") + char('a' + sqf(a)) + char('1' + sqr(a)) + (b >= 0 ? string(1, char('a' + sqf(b))) + char('1' + sqr(b)) : string("=promotes"));
        }
        printf(" %s%s", cstm ? "..." : "", d.c_str());
        if (promo) break;
        cwk = m.nwk; cbk = m.nbk; ck = m.nk; cstm = 1 - cstm;
      }
    }
    printf("\n");
  }
  fprintf(stderr, "layers solved %ld\n", layersSolved);
  return 0;
}
