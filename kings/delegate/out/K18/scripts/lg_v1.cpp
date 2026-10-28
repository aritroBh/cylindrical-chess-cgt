// lg.cpp -- local promotion game of LOOPY Definition 2.6 (K18, own implementation).
//
// s = White (the side that makes the sortie), sbar = Black (the punisher).  Colour-flip a position to test Black sorties.
// Game (Definition 2.6, L1): pieces = both kings + Z-pawns (all on the files F_Z, ranks 2..H-1), nothing else.
//   * the first promotion ends the game.  A promotion by s is a failure for sbar.  A promotion by sbar wins for
//     sbar if the new queen cannot be captured at once (variant Q, "L1"), or always (variant P, "L1_P").
//   * sbar's king may only step onto squares of F_Z.  s's king is free on the whole board.
//   * s may pass whenever it is not in check (variant "pass", k = infinity); in the variant "plain" it may not,
//     and a stalemate of s is then a failure for sbar.
//   * s in check with no legal move: mated, sbar wins.  sbar with no permitted move: failure.
//   * n(state) = least number of sbar moves needed to win under best play, INF if none (least fixed point).
// Four tables: plain/pass x Q/P, computed over ALL pawn configurations with <= maxw white and <= maxb black pawns
// on F_Z (ranks 2..H-1), all king placements.  e.p. rights are carried exactly.
//
// Modes:   --query   read "Kc3 Pb4 ka3 pb5 w -" lines (white = s) and print the four n-values
//          --search  enumerate all roots Y (both kings on F_Z, s to move) and sorties m, replies r; print groups.
//
// Usage: lg --board cyl:8x6 --fz 0:3 --maxw 2 --maxb 2 --query|--search [--nopasser 0|1]
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
using namespace std;
typedef unsigned long long u64;

static int W, H, N, CYL, NFZ;
static vector<int> fzsq;       // squares of F_Z
static int fzidx[64];
static u64 FZ = 0;
static int fzfiles[8], nfzf;
static u64 kingBB[64], attW[64], attB[64];
static int maxw = 2, maxb = 2;
static const uint8_t INF = 255;

static inline u64 bit(int s) { return 1ULL << s; }
static inline int ctz(u64 x) { return __builtin_ctzll(x); }
static inline int popc(u64 x) { return __builtin_popcountll(x); }
static int nbFile(int f, int d) {
  int g = f + d;
  if (CYL) return ((g % W) + W) % W;
  return (g < 0 || g >= W) ? -1 : g;
}
static inline int SQ(int f, int r) { return r * W + f; }

struct Pos {
  u64 wp, bp;
  int wk, bk, stm, ep;  // stm 0 = White (s), 1 = Black (sbar); ep = target square or -1
};
struct Move {
  Pos to;
  int kind;  // 0 normal, 1 promotion
  int from, dst;
};

static void init_geom() {
  N = W * H;
  for (int s = 0; s < N; s++) {
    int f = s % W, r = s / W;
    kingBB[s] = attW[s] = attB[s] = 0;
    for (int df = -1; df <= 1; df++)
      for (int dr = -1; dr <= 1; dr++) {
        if (!df && !dr) continue;
        int g = nbFile(f, df), q = r + dr;
        if (g < 0 || q < 0 || q >= H) continue;
        int t = SQ(g, q);
        if (t != s) kingBB[s] |= bit(t);
      }
    for (int df = -1; df <= 1; df += 2) {
      int g = nbFile(f, df);
      if (g < 0) continue;
      if (r + 1 < H) attW[s] |= bit(SQ(g, r + 1));
      if (r - 1 >= 0) attB[s] |= bit(SQ(g, r - 1));
    }
  }
}
static inline u64 patt(int c, u64 pawns) {
  u64 m = 0;
  while (pawns) {
    int s = ctz(pawns);
    pawns &= pawns - 1;
    m |= c == 0 ? attW[s] : attB[s];
  }
  return m;
}

// ---- move generation (legal moves of the side to move; Black's king confined to F_Z when confine) ----
static int gen(const Pos& p, Move* mv, bool confine) {
  int n = 0, c = p.stm;
  u64 own = c == 0 ? p.wp : p.bp, en = c == 0 ? p.bp : p.wp;
  int ok = c == 0 ? p.wk : p.bk, ek = c == 0 ? p.bk : p.wk;
  u64 occ = p.wp | p.bp | bit(p.wk) | bit(p.bk);
  u64 d = kingBB[ok] & ~own & ~kingBB[ek] & ~bit(ek);
  if (c == 1 && confine) d &= FZ;
  while (d) {
    int t = ctz(d);
    d &= d - 1;
    u64 en2 = en & ~bit(t);
    if (patt(1 - c, en2) & bit(t)) continue;
    Pos q = p;
    if (c == 0) { q.wk = t; q.bp = en2; } else { q.bk = t; q.wp = en2; }
    q.stm = 1 - c; q.ep = -1;
    mv[n++] = Move{q, 0, ok, t};
  }
  u64 ps = own;
  while (ps) {
    int s = ctz(ps);
    ps &= ps - 1;
    int f = s % W, r = s / W;
    int dir = c == 0 ? 1 : -1;
    int lastr = c == 0 ? H - 1 : 0;
    int startr = c == 0 ? 1 : H - 2;
    auto emit = [&](u64 newown, u64 newen, int to, int ep, int kind) {
      Pos q = p;
      if (c == 0) { q.wp = newown; q.bp = newen; } else { q.bp = newown; q.wp = newen; }
      q.stm = 1 - c; q.ep = ep;
      // own king must not be attacked by enemy pawns
      if (patt(1 - c, newen) & bit(ok)) return;
      mv[n++] = Move{q, kind, s, to};
    };
    int t = s + dir * W;
    if (!((occ >> t) & 1)) {
      if (r + dir == lastr) emit(own & ~bit(s), en, t, -1, 1);
      else {
        emit((own & ~bit(s)) | bit(t), en, t, -1, 0);
        if (r == startr) {
          int t2 = t + dir * W;
          if (!((occ >> t2) & 1)) {
            int ep = -1;
            for (int df = -1; df <= 1; df += 2) {
              int g = nbFile(f, df);
              if (g >= 0 && ((en >> SQ(g, r + 2 * dir)) & 1)) ep = t;
            }
            emit((own & ~bit(s)) | bit(t2), en, t2, ep, 0);
          }
        }
      }
    }
    for (int df = -1; df <= 1; df += 2) {
      int g = nbFile(f, df);
      if (g < 0) continue;
      int tc = SQ(g, r + dir);
      if ((en >> tc) & 1) {
        if (r + dir == lastr) emit(own & ~bit(s), en & ~bit(tc), tc, -1, 1);
        else emit((own & ~bit(s)) | bit(tc), en & ~bit(tc), tc, -1, 0);
      } else if (p.ep == tc) {
        int vic = SQ(g, r);
        if ((en >> vic) & 1) emit((own & ~bit(s)) | bit(tc), en & ~bit(vic), tc, -1, 0);
      }
    }
  }
  return n;
}
static inline bool whiteInCheck(const Pos& p) { return (patt(1, p.bp) >> p.wk) & 1; }
static inline bool blackInCheck(const Pos& p) { return (patt(0, p.wp) >> p.bk) & 1; }

// can White capture the queen that Black's pawn on `from` makes on from-W?
static bool queenSafe(const Pos& p, int from) {
  int dst = from - W;
  u64 bp2 = p.bp & ~bit(from);
  bool cap = ((kingBB[p.wk] >> dst) & 1) && !((kingBB[p.bk] >> dst) & 1) && !((patt(1, bp2) >> dst) & 1);
  return !cap;
}

// ---- configurations and tables ----
static int P;  // pawn squares
static vector<int> psq;
static int lidx[64];
static vector<u64> globOf;  // local mask -> global bitboard
static vector<int> wsetId, bsetId;
static vector<unsigned> wsets, bsets;
static int ncfg, SL;
static vector<int> cfgW, cfgB;     // cfg -> set indices
static int nbs;
struct Tables {
  vector<uint8_t> val, epv;
};
static Tables tab[4];  // variant = pass*2 + queenClause... see vname
static int cur = 0;
static bool passV[4], qV[4];
static const char* vname[4] = {"plain/P", "plain/Q", "pass/P", "pass/Q"};

static inline unsigned localMask(u64 g) {
  unsigned m = 0;
  while (g) { int s = ctz(g); g &= g - 1; m |= 1u << lidx[s]; }
  return m;
}
static inline int cfgOf(u64 wp, u64 bp) {
  int a = wsetId[localMask(wp)], b = bsetId[localMask(bp)];
  return a * nbs + b;
}
static inline int ordinal(u64 pawns, int sq) { return popc(pawns & (bit(sq) - 1)); }

static inline uint8_t getv(int v, const Pos& p) {
  int cfg = cfgOf(p.wp, p.bp);
  int bi = fzidx[p.bk];
  if (p.ep < 0) return tab[v].val[(((size_t)cfg * 2 + p.stm) * N + p.wk) * NFZ + bi];
  int slot;
  if (p.stm == 1) slot = ordinal(p.wp, p.ep + W);               // White just double-stepped
  else slot = maxw + ordinal(p.bp, p.ep - W);                   // Black just double-stepped
  return tab[v].epv[(((size_t)cfg * SL + slot) * N + p.wk) * NFZ + bi];
}
static inline void setv(int v, const Pos& p, uint8_t x) {
  int cfg = cfgOf(p.wp, p.bp);
  int bi = fzidx[p.bk];
  if (p.ep < 0) { tab[v].val[(((size_t)cfg * 2 + p.stm) * N + p.wk) * NFZ + bi] = x; return; }
  int slot;
  if (p.stm == 1) slot = ordinal(p.wp, p.ep + W);
  else slot = maxw + ordinal(p.bp, p.ep - W);
  tab[v].epv[(((size_t)cfg * SL + slot) * N + p.wk) * NFZ + bi] = x;
}

static uint8_t evalState(int v, const Pos& p) {
  Move mv[96];
  if (p.stm == 1) {
    int n = gen(p, mv, true), best = INF;
    for (int i = 0; i < n; i++) {
      if (mv[i].kind == 1) {
        if (!qV[v] || queenSafe(p, mv[i].from)) best = min(best, 1);
        continue;
      }
      uint8_t x = getv(v, mv[i].to);
      if (x != INF) best = min(best, (int)x + 1);
    }
    return (uint8_t)best;
  }
  int n = gen(p, mv, false);
  bool chk = whiteInCheck(p);
  if (n == 0 && chk) return 0;
  int worst = 0;
  for (int i = 0; i < n; i++) {
    if (mv[i].kind == 1) return INF;
    worst = max(worst, (int)getv(v, mv[i].to));
    if (worst == INF) return INF;
  }
  if (passV[v] && !chk) {
    Pos q = p; q.stm = 1; q.ep = -1;
    worst = max(worst, (int)getv(v, q));
  } else if (n == 0) return INF;  // plain stalemate: failure for sbar
  return (uint8_t)worst;
}

static bool legalKings(const Pos& p) {
  if (p.wp & p.bp) return false;   // a square cannot hold a White and a Black pawn
  if (p.wk == p.bk) return false;
  if ((kingBB[p.wk] >> p.bk) & 1) return false;
  if (((p.wp | p.bp) >> p.wk) & 1) return false;
  if (((p.wp | p.bp) >> p.bk) & 1) return false;
  if (p.stm == 1 && whiteInCheck(p)) return false;   // side not to move must not be in check
  if (p.stm == 0 && blackInCheck(p)) return false;
  return true;
}

static void solveAll(int v) {
  tab[v].val.assign((size_t)ncfg * 2 * N * NFZ, INF);
  tab[v].epv.assign((size_t)ncfg * SL * N * NFZ, INF);
  // order configs by decreasing potential
  vector<int> order(ncfg);
  vector<int> phi(ncfg);
  for (int c = 0; c < ncfg; c++) {
    order[c] = c;
    u64 wp = globOf[wsets[cfgW[c]]], bp = globOf[bsets[cfgB[c]]];
    int ph = 100 * (maxw + maxb - popc(wp) - popc(bp));
    for (u64 x = wp; x; x &= x - 1) ph += ctz(x) / W;
    for (u64 x = bp; x; x &= x - 1) ph += H - 1 - ctz(x) / W;
    phi[c] = ph;
  }
  sort(order.begin(), order.end(), [&](int a, int b) { return phi[a] > phi[b]; });
  vector<Pos> states;
  for (int ci = 0; ci < ncfg; ci++) {
    int c = order[ci];
    u64 wp = globOf[wsets[cfgW[c]]], bp = globOf[bsets[cfgB[c]]];
    states.clear();
    for (int stm = 0; stm < 2; stm++)
      for (int wk = 0; wk < N; wk++)
        for (int bi = 0; bi < NFZ; bi++) {
          Pos p{wp, bp, wk, fzsq[bi], stm, -1};
          if (legalKings(p)) states.push_back(p);
        }
    bool changed = true;
    while (changed) {
      changed = false;
      for (const Pos& p : states) {
        uint8_t nv = evalState(v, p), old = getv(v, p);
        if (nv != old) { setv(v, p, nv); changed = true; }
      }
    }
    // ep states of this configuration
    for (int j = 0; j < maxw; j++) {  // White pawn j just double-stepped (lands on rank index 3), Black to move
      u64 x = wp; int k = 0, s = -1;
      while (x) { if (k == j) { s = ctz(x); break; } x &= x - 1; k++; }
      if (s < 0 || s / W != 3) continue;
      int tgt = s - W;
      for (int wk = 0; wk < N; wk++)
        for (int bi = 0; bi < NFZ; bi++) {
          Pos p{wp, bp, wk, fzsq[bi], 1, tgt};
          if (legalKings(p)) setv(v, p, evalState(v, p));
        }
    }
    for (int j = 0; j < maxb; j++) {  // Black pawn j just double-stepped (lands on rank index H-4), White to move
      u64 x = bp; int k = 0, s = -1;
      while (x) { if (k == j) { s = ctz(x); break; } x &= x - 1; k++; }
      if (s < 0 || s / W != H - 4) continue;
      int tgt = s + W;
      for (int wk = 0; wk < N; wk++)
        for (int bi = 0; bi < NFZ; bi++) {
          Pos p{wp, bp, wk, fzsq[bi], 0, tgt};
          if (legalKings(p)) setv(v, p, evalState(v, p));
        }
    }
  }
}

// ---- parsing / printing ----
static string sqname(int s) { char b[8]; snprintf(b, 8, "%c%d", 'a' + s % W, s / W + 1); return b; }
static string posstr(const Pos& p) {
  string s = "K" + sqname(p.wk);
  for (u64 x = p.wp; x; x &= x - 1) s += " P" + sqname(ctz(x));
  s += " k" + sqname(p.bk);
  for (u64 x = p.bp; x; x &= x - 1) s += " p" + sqname(ctz(x));
  s += p.stm == 0 ? " w " : " b ";
  s += p.ep < 0 ? "-" : sqname(p.ep);
  return s;
}
static bool parsePos(const char* line, Pos& p) {
  p = Pos{0, 0, -1, -1, 0, -1};
  char buf[256];
  strncpy(buf, line, 255); buf[255] = 0;
  char* sv; char* tok = strtok_r(buf, " \t\r\n", &sv);
  int ntok = 0; char last[16] = "", last2[16] = "";
  while (tok) {
    strcpy(last2, last); strncpy(last, tok, 15);
    char ch = tok[0];
    if (strchr("KkPp", ch) && strlen(tok) >= 3 && isalpha(tok[1])) {
      int f = tok[1] - 'a', r = atoi(tok + 2) - 1;
      int s = SQ(f, r);
      if (ch == 'K') p.wk = s; else if (ch == 'k') p.bk = s;
      else if (ch == 'P') p.wp |= bit(s); else p.bp |= bit(s);
    }
    tok = strtok_r(nullptr, " \t\r\n", &sv); ntok++;
  }
  // last two tokens: side, ep
  p.stm = (last2[0] == 'b') ? 1 : 0;
  if (last[0] != '-' && isalpha(last[0])) p.ep = SQ(last[0] - 'a', atoi(last + 1) - 1);
  return p.wk >= 0 && p.bk >= 0;
}

// ---- passers (cylcgt.pawns.passed: no enemy pawn ahead on the same or an adjacent file; no e.p. at the root) ----
static bool hasPasser(u64 wp, u64 bp) {
  for (u64 x = wp; x; x &= x - 1) {
    int s = ctz(x), f = s % W, r = s / W; bool blocked = false;
    for (u64 y = bp; y; y &= y - 1) {
      int t = ctz(y), g = t % W, q = t / W;
      int df = (g - f + W) % W;
      bool adj = CYL ? (df == 0 || df == 1 || df == W - 1) : (abs(g - f) <= 1);
      if (adj && q > r) blocked = true;
    }
    if (!blocked) return true;
  }
  for (u64 y = bp; y; y &= y - 1) {
    int t = ctz(y), g = t % W, q = t / W; bool blocked = false;
    for (u64 x = wp; x; x &= x - 1) {
      int s = ctz(x), f = s % W, r = s / W;
      int df = (g - f + W) % W;
      bool adj = CYL ? (df == 0 || df == 1 || df == W - 1) : (abs(g - f) <= 1);
      if (adj && r < q) blocked = true;
    }
    if (!blocked) return true;
  }
  return false;
}

static string movestr(const Pos& from, const Move& m) {
  // king move or pawn move text
  string s;
  bool king = (m.from == from.wk || m.from == from.bk) && m.kind == 0 && !(((from.stm == 0 ? from.wp : from.bp) >> m.from) & 1);
  s = king ? "K" : "";
  s += sqname(m.from) + "-" + sqname(m.dst);
  if (m.kind == 1) s += "=Q";
  return s;
}

int main(int argc, char** argv) {
  int mode = 0, nopasser = 1; int fzstart = 0, fzlen = 3;
  const char* board = "cyl:8x6";
  int onlyv = -1; const char* dumpbare = nullptr;
  for (int i = 1; i < argc; i++) {
    if (!strcmp(argv[i], "--board")) board = argv[++i];
    else if (!strcmp(argv[i], "--fz")) sscanf(argv[++i], "%d:%d", &fzstart, &fzlen);
    else if (!strcmp(argv[i], "--maxw")) maxw = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--maxb")) maxb = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--query")) mode = 1;
    else if (!strcmp(argv[i], "--search")) mode = 2;
    else if (!strcmp(argv[i], "--nopasser")) nopasser = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--only")) onlyv = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--dumpbare")) dumpbare = argv[++i];
  }
  CYL = !strncmp(board, "cyl", 3);
  sscanf(strchr(board, ':') + 1, "%dx%d", &W, &H);
  init_geom();
  nfzf = fzlen;
  for (int i = 0; i < fzlen; i++) fzfiles[i] = (fzstart + i) % W;
  for (int i = 0; i < 64; i++) fzidx[i] = -1, lidx[i] = -1;
  for (int i = 0; i < fzlen; i++)
    for (int r = 0; r < H; r++) { int s = SQ(fzfiles[i], r); fzidx[s] = (int)fzsq.size(); fzsq.push_back(s); FZ |= bit(s); }
  NFZ = fzsq.size();
  for (int i = 0; i < fzlen; i++)
    for (int r = 1; r <= H - 2; r++) { lidx[SQ(fzfiles[i], r)] = (int)psq.size(); psq.push_back(SQ(fzfiles[i], r)); }
  P = psq.size();
  globOf.assign(1u << P, 0);
  for (unsigned m = 0; m < (1u << P); m++) { u64 g = 0; for (int i = 0; i < P; i++) if ((m >> i) & 1) g |= bit(psq[i]); globOf[m] = g; }
  wsetId.assign(1u << P, -1); bsetId.assign(1u << P, -1);
  for (unsigned m = 0; m < (1u << P); m++) {
    if (popc(m) <= maxw) { wsetId[m] = wsets.size(); wsets.push_back(m); }
    if (popc(m) <= maxb) { bsetId[m] = bsets.size(); bsets.push_back(m); }
  }
  nbs = bsets.size(); ncfg = wsets.size() * nbs; SL = maxw + maxb;
  cfgW.resize(ncfg); cfgB.resize(ncfg);
  for (int a = 0; a < (int)wsets.size(); a++) for (int b = 0; b < nbs; b++) { cfgW[a * nbs + b] = a; cfgB[a * nbs + b] = b; }
  for (int v = 0; v < 4; v++) { passV[v] = v >= 2; qV[v] = v & 1; }
  fprintf(stderr, "[lg] %s fz=%d:%d P=%d configs=%d NFZ=%d\n", board, fzstart, fzlen, P, ncfg, NFZ);
  for (int v = 0; v < 4; v++) {
    if (onlyv >= 0 && v != onlyv) continue;
    solveAll(v);
    fprintf(stderr, "[lg] solved %s\n", vname[v]);
  }
  if (mode == 1) {
    char line[512];
    while (fgets(line, sizeof line, stdin)) {
      if (line[0] == '#' || line[0] == '\n') { fputs(line, stdout); continue; }
      Pos p; line[strcspn(line, "\n")] = 0;
      if (!parsePos(line, p)) { printf("%s | parse error\n", line); continue; }
      printf("%s |", line);
      for (int v = 0; v < 4; v++) {
        if (onlyv >= 0 && v != onlyv) continue;
        uint8_t x = getv(v, p);
        if (x == INF) printf(" %s=inf", vname[v]); else printf(" %s=%d", vname[v], x);
      }
      printf("\n");
    }
    return 0;
  }
  if (mode == 2) {
    FILE* df = dumpbare ? fopen(dumpbare, "w") : nullptr;
    long nroots = 0, ncand[4] = {0, 0, 0, 0}, ncandAny[4] = {0, 0, 0, 0};
    for (int c = 0; c < ncfg; c++) {
      u64 wp = globOf[wsets[cfgW[c]]], bp = globOf[bsets[cfgB[c]]];
      if (nopasser && hasPasser(wp, bp)) continue;
      // s can promote at once?  skip such roots
      for (int wk : fzsq) for (int bk : fzsq) {
        Pos Y{wp, bp, wk, bk, 0, -1};
        if (!legalKings(Y)) continue;
        Move ym[96]; int ny = gen(Y, ym, false);
        bool canPromo = false;
        for (int i = 0; i < ny; i++) if (ym[i].kind == 1) canPromo = true;
        if (canPromo) continue;
        nroots++;
        // per sortie, per variant: status bits: 1 = plain-punished, 2 = pass-punished, 4 = immediate promotion reply
        struct Res { int st[4]; int bestr[4][2]; int Tplain[4], Tpass[4]; string rplain[4], rpass[4]; };
        vector<Res> res(ny);
        vector<string> mnames(ny);
        for (int i = 0; i < ny; i++) {
          mnames[i] = movestr(Y, ym[i]);
          Res& R = res[i];
          for (int v = 0; v < 4; v++) { R.st[v] = 0; R.Tplain[v] = R.Tpass[v] = INF; }
          const Pos& Ym = ym[i].to;
          Move rm[96]; int nr = gen(Ym, rm, true);
          for (int j = 0; j < nr; j++) {
            if (rm[j].kind == 1) {
              for (int v = 0; v < 4; v++) if (!qV[v] || queenSafe(Ym, rm[j].from)) R.st[v] |= 4;
              continue;
            }
            for (int v = 0; v < 4; v++) {
              uint8_t x = getv(v, rm[j].to);
              if (x == INF) continue;
              if (!passV[v]) { if (x < R.Tplain[v]) { R.Tplain[v] = x; R.rplain[v] = movestr(Ym, rm[j]); } }
              else { if (x < R.Tpass[v]) { R.Tpass[v] = x; R.rpass[v] = movestr(Ym, rm[j]); } }
            }
          }
        }
        if (df) for (int i = 0; i < ny; i++) {
          if (ym[i].kind == 1) continue;
          Res& R = res[i];
          fprintf(df, "%s |", posstr(ym[i].to).c_str());
          for (int v = 0; v < 4; v++) fprintf(df, " %d", (passV[v] ? R.Tpass[v] : R.Tplain[v]) != INF);
          fprintf(df, " %d %d\n", (R.st[0] & 4) != 0, (R.st[1] & 4) != 0);
        }
        // classify for the two queen settings: (plain v=0/1, pass v=2/3): index q = 0 (P) or 1 (Q)
        for (int q = 0; q < 2; q++) {
          int vp = q, vs = 2 + q;
          bool anyOnly = false, escape = false; int nonly = 0, nesc = 0;
          for (int i = 0; i < ny; i++) {
            if (ym[i].kind == 1) continue;
            Res& R = res[i];
            bool imm = R.st[vp] & 4;
            bool plainP = imm || R.Tplain[vp] != INF;
            bool passP = imm || R.Tpass[vs] != INF;
            if (!plainP && !passP) { escape = true; nesc++; }
            if (plainP && !passP) { anyOnly = true; nonly++; }
          }
          if (!anyOnly) continue;
          ncandAny[q]++;
          if (!escape) ncand[q]++;
          printf("%s | %s | only=%d esc=%d | %s |", q ? "Q" : "P", posstr(Y).c_str(), nonly, nesc, escape ? "ESCAPE" : "NOESC");
          for (int i = 0; i < ny; i++) {
            if (ym[i].kind == 1) continue;
            Res& R = res[i];
            bool imm = R.st[vp] & 4;
            bool plainP = imm || R.Tplain[vp] != INF, passP = imm || R.Tpass[vs] != INF;
            const char* cls = imm ? "IMM" : (plainP && passP) ? "both" : plainP ? "PLAIN-ONLY" : passP ? "pass-only" : "ESC";
            printf(" [%s %s", mnames[i].c_str(), cls);
            if (R.Tplain[vp] != INF) printf(" Tplain=%d(%s)", R.Tplain[vp], R.rplain[vp].c_str());
            if (R.Tpass[vs] != INF) printf(" Tpass=%d(%s)", R.Tpass[vs], R.rpass[vs].c_str());
            printf("]");
          }
          printf("\n");
        }
      }
    }
    fprintf(stderr, "[lg] roots=%ld  candidates(any) P=%ld Q=%ld  candidates(no escape) P=%ld Q=%ld\n", nroots, ncandAny[0], ncandAny[1], ncand[0], ncand[1]);
    if (df) fclose(df);
    printf("# roots=%ld cand_any P=%ld Q=%ld cand_noesc P=%ld Q=%ld\n", nroots, ncandAny[0], ncandAny[1], ncand[0], ncand[1]);
  }
  return 0;
}
