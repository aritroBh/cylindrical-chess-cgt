// k42.cpp -- K42 solver, written from kings/SPEC.md and Definition 2.6 of kings/theory/LOOPY.md.
// Model P (first promotion wins for the promoter, real kings, stalemate and infinite play draw), solved by
// pawn-configuration layers (pawn moves and captures are irreversible; king moves are solved inside a layer by
// retrograde counting). Options turn the same engine into the local game of Definition 2.6 (s = White,
// s-bar = Black):  --confine FILES  Black's king may only step onto these files;  --pass  White may pass when not
// in check (k = infinity);  --qclause  a Black promotion that White's king can capture at once is not a Black win.
// White promotion always ends the game as a White win (a failure for Black), as in Definition 2.6 rule 1.
//
// Modes:
//   k42 solve   --board cyl:8x6 [opts] < positions      -> "<pos> | V"   V in W D L X, White's point of view
//   k42 sorties --board cyl:8x6 --fz 0,1,2 --maxw 2 --maxb 2   -> plain-only sorties (see below)
//   k42 test    --board cyl:8x6 --sorties FILE --contexts FILE -> P value of (position after m) + G, Black to move
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <array>
#include <unordered_map>
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <map>
#include <set>
using namespace std;
typedef uint64_t u64;

static int W = 8, H = 6, K = 48, NS = 2 * 48 * 48;
static bool CYL = true, EPON = true, PASSW = false, QCL = false;
static u64 BCONF = ~0ULL;          // squares Black's king may step onto
static u64 WCONF = ~0ULL;          // squares White's king may step onto (diagnostic option --wconfine)
static bool WSTALL = false;
static u64 WBAD = 0;              // --wbad: a White king step onto these squares is a White win (certificate test)
static bool P1E = false;           // --p1e: a White-to-move node with an e.p. right whose legal moves are all e.p. captures is a White win        // diagnostic: a stalemate of White counts as a Black win (--wstalemate-loss)
static u64 NBM[64];
static int NB[64][8], NNB[64];
static size_t MAXMB = 1500;

static inline u64 bit(int s) { return 1ULL << s; }
static inline int Fo(int s) { return s % W; }
static inline int Ro(int s) { return s / W; }
static int mk(int f, int r) {
  if (r < 0 || r >= H) return -1;
  if (CYL) f = ((f % W) + W) % W; else if (f < 0 || f >= W) return -1;
  return r * W + f;
}
static u64 attW(u64 p) { // squares attacked by white pawns
  u64 a = 0;
  while (p) { int s = __builtin_ctzll(p); p &= p - 1; int f = Fo(s), r = Ro(s);
    for (int d = -1; d <= 1; d += 2) { int t = mk(f + d, r + 1); if (t >= 0) a |= bit(t); } }
  return a;
}
static u64 attB(u64 p) {
  u64 a = 0;
  while (p) { int s = __builtin_ctzll(p); p &= p - 1; int f = Fo(s), r = Ro(s);
    for (int d = -1; d <= 1; d += 2) { int t = mk(f + d, r - 1); if (t >= 0) a |= bit(t); } }
  return a;
}
static void initBoard() {
  K = W * H; NS = 2 * K * K;
  for (int s = 0; s < K; s++) {
    NBM[s] = 0; NNB[s] = 0;
    for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
      if (!df && !dr) continue;
      int t = mk(Fo(s) + df, Ro(s) + dr);
      if (t < 0 || t == s || (NBM[s] & bit(t))) continue;
      NBM[s] |= bit(t); NB[s][NNB[s]++] = t;
    }
  }
}

struct Pos { u64 w, b; int wk, bk, side, ep; };
struct Child { Pos p; int term; int isEp; };   // term: -1 not terminal; else value 0 D, 1 W, 2 L (White's view)

static bool legal(const Pos& P) {
  if (P.wk == P.bk) return false;
  u64 occ = P.w | P.b;
  if (occ & (bit(P.wk) | bit(P.bk))) return false;
  if (P.w & P.b) return false;
  for (int s = 0; s < K; s++) if ((P.w & bit(s)) || (P.b & bit(s))) if (Ro(s) == 0 || Ro(s) == H - 1) return false;
  if (NBM[P.wk] & bit(P.bk)) return false;
  if (P.side == 0) { if (attW(P.w) & bit(P.bk)) return false; }
  else { if (attB(P.b) & bit(P.wk)) return false; }
  return true;
}
static bool inCheck(const Pos& P) { return P.side == 0 ? (attB(P.b) & bit(P.wk)) != 0 : (attW(P.w) & bit(P.bk)) != 0; }

// legal moves of P (assumed legal); returns count
static int gen(const Pos& P, Child* out, char (*names)[12] = nullptr) {
  int n = 0, S = P.side;
  u64 own = S ? P.b : P.w, opp = S ? P.w : P.b;
  int myk = S ? P.bk : P.wk, ek = S ? P.wk : P.bk;
  u64 occ = P.w | P.b, kings = bit(P.wk) | bit(P.bk);
  int dir = S ? -1 : 1, prom = S ? 0 : H - 1, start = S ? H - 2 : 1;
  auto oppAtt = [&](u64 o) { return S ? attW(o) : attB(o); };
  u64 A = oppAtt(opp);
  bool chk = (A & bit(myk)) != 0;
  auto add = [&](u64 nown, u64 nopp, int nmyk, int nep, int term, const char* nm) {
    Child& c = out[n];
    c.p.w = S ? nopp : nown; c.p.b = S ? nown : nopp;
    c.p.wk = S ? P.wk : nmyk; c.p.bk = S ? nmyk : P.bk; c.p.side = 1 - S; c.p.ep = nep; c.term = term; c.isEp = 0;
    if (names) snprintf(names[n], 12, "%s", nm);
    n++;
  };
  char nm[12];
  auto sqn = [&](int s, char* b) { b[0] = 'a' + Fo(s); b[1] = '1' + Ro(s); b[2] = 0; };
  // king moves
  for (int i = 0; i < NNB[myk]; i++) {
    int d = NB[myk][i];
    if (own & bit(d)) continue;
    if (d == ek || (NBM[ek] & bit(d))) continue;
    if (S == 1 && !(BCONF & bit(d))) continue;
    if (S == 0 && !(WCONF & bit(d))) continue;
    u64 nopp = opp & ~bit(d);
    if (oppAtt(nopp) & bit(d)) continue;
    if (names) { char a[3], b[3]; sqn(myk, a); sqn(d, b); snprintf(nm, 12, "%c%s%s", S ? 'k' : 'K', a, b); }
    add(own, nopp, d, -1, (S == 0 && (WBAD & bit(d))) ? 1 : -1, nm);
  }
  if (S == 0 && PASSW && !chk) add(own, opp, myk, -1, -1, "pass");
  // pawn moves
  u64 pp = own;
  while (pp) {
    int p = __builtin_ctzll(pp); pp &= pp - 1;
    int f = Fo(p), r = Ro(p);
    char a[3]; sqn(p, a);
    int t1 = mk(f, r + dir);
    if (t1 >= 0 && !((occ | kings) & bit(t1))) {
      u64 nown = own ^ bit(p) ^ bit(t1);
      if (!chk) {
        char b[3]; sqn(t1, b); if (names) snprintf(nm, 12, "%c%s%s", S ? 'p' : 'P', a, b);
        if (Ro(t1) == prom) {
          int term = S ? 2 : 1;
          if (S == 1 && QCL) { // can White's king take the new piece at once?
            bool cap = (NBM[P.wk] & bit(t1)) && !(NBM[P.bk] & bit(t1)) && !(attB(own ^ bit(p)) & bit(t1));
            if (cap) term = 0;
          }
          add(nown, opp, myk, -1, term, nm);
        } else add(nown, opp, myk, -1, -1, nm);
      }
      if (r == start) {
        int t2 = mk(f, r + 2 * dir);
        if (t2 >= 0 && !((occ | kings) & bit(t2)) && !chk) {
          u64 nown2 = own ^ bit(p) ^ bit(t2);
          char b[3]; sqn(t2, b); if (names) snprintf(nm, 12, "%c%s%s", S ? 'p' : 'P', a, b);
          if (Ro(t2) == prom) {
            add(nown2, opp, myk, -1, S ? 2 : 1, nm);
          } else {
            int ep = -1;
            if (EPON) for (int d = -1; d <= 1; d += 2) { int c = mk(f + d, r + 2 * dir); if (c >= 0 && (opp & bit(c))) ep = t1; }
            add(nown2, opp, myk, ep, -1, nm);
          }
        }
      }
    }
    for (int d = -1; d <= 1; d += 2) {
      int c = mk(f + d, r + dir);
      if (c < 0) continue;
      char b[3]; sqn(c, b);
      if (opp & bit(c)) {
        u64 nopp = opp ^ bit(c);
        if (oppAtt(nopp) & bit(myk)) continue;
        u64 nown = own ^ bit(p) ^ bit(c);
        if (names) snprintf(nm, 12, "%c%sx%s", S ? 'p' : 'P', a, b);
        if (Ro(c) == prom) {
          int term = S ? 2 : 1;
          if (S == 1 && QCL) {
            bool cap = (NBM[P.wk] & bit(c)) && !(NBM[P.bk] & bit(c)) && !(attB(own ^ bit(p)) & bit(c));
            if (cap) term = 0;
          }
          add(nown, nopp, myk, -1, term, nm);
        } else add(nown, nopp, myk, -1, -1, nm);
      } else if (EPON && P.ep == c && !(kings & bit(c))) {
        int capt = mk(Fo(c), r);
        if (capt >= 0 && (opp & bit(capt))) {
          u64 nopp = opp ^ bit(capt);
          if (oppAtt(nopp) & bit(myk)) continue;
          u64 nown = own ^ bit(p) ^ bit(c);
          if (names) snprintf(nm, 12, "%c%sx%sep", S ? 'p' : 'P', a, b);
          add(nown, nopp, myk, -1, -1, nm);
          out[n - 1].isEp = 1;
        }
      }
    }
  }
  return n;
}

// ---------------- layers ----------------
struct Key { u64 w, b; int ep; bool operator==(const Key& o) const { return w == o.w && b == o.b && ep == o.ep; } };
struct KeyH { size_t operator()(const Key& k) const {
  u64 h = k.w * 0x9E3779B97F4A7C15ULL; h ^= (k.b + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL;
  h ^= (u64)(k.ep + 1) * 0x165667B19E3779F9ULL; h ^= h >> 31; return (size_t)h; } };
static unordered_map<Key, vector<uint8_t>, KeyH> cache;
static size_t cacheBytes = 0;
static long nLayers = 0;
static inline int sidx(int side, int wk, int bk) { return (side * K + wk) * K + bk; }
static inline int getv(const vector<uint8_t>& v, int i) { return (v[i >> 2] >> ((i & 3) * 2)) & 3; }
static int epSide(int ep) { return Ro(ep) == 2 ? 1 : 0; } // white double step -> target rank 3 (index 2), Black to move

static const vector<uint8_t>& solve(const Key& k);
static string posStr(const Pos& P);

static const vector<uint8_t>& lookup(const Key& k) {
  auto it = cache.find(k);
  if (it != cache.end()) return it->second;
  return solve(k);
}

static const vector<uint8_t>& solve(const Key& k) {
  vector<int8_t> val(NS, -1);
  vector<uint8_t> deg(NS, 0);
  vector<int> eStart(NS + 1, 0); vector<int> edges; edges.reserve(NS * 6);
  static thread_local Child buf[64];
  vector<pair<Key, const vector<uint8_t>*>> local;
  for (int side = 0; side < 2; side++) for (int wk = 0; wk < K; wk++) for (int bk = 0; bk < K; bk++) {
    int s = sidx(side, wk, bk);
    eStart[s] = edges.size();
    Pos P{k.w, k.b, wk, bk, side, k.ep};
    if (k.ep >= 0 && (side != epSide(k.ep) || wk == k.ep || bk == k.ep)) { val[s] = 3; continue; }
    if (!legal(P)) { val[s] = 3; continue; }
    Child cb[64];
    int n = gen(P, cb);
    int winV = side ? 2 : 1, loseV = side ? 1 : 2;
    bool win = false; int cnt = 0;
    for (int i = 0; i < n; i++) {
      const Child& c = cb[i];
      int v;
      if (c.term >= 0) v = c.term;
      else {
        Key ck{c.p.w, c.p.b, c.p.ep};
        int ci = sidx(c.p.side, c.p.wk, c.p.bk);
        if (ck == k) { edges.push_back(ci); cnt++; continue; }
        const vector<uint8_t>* L = nullptr;
        for (auto& pr : local) if (pr.first == ck) { L = pr.second; break; }
        if (!L) { L = &lookup(ck); local.push_back({ck, L}); }
        v = getv(*L, ci);
        if (v == 3) { fprintf(stderr, "internal error: illegal child %s from %s\n", posStr(c.p).c_str(), posStr(P).c_str()); exit(2); }
      }
      if (v == winV) win = true; else if (v != loseV) cnt++;
    }
    if (n == 0) { val[s] = (inCheck(P) || (side == 0 && WSTALL)) ? loseV : 0; continue; }
    if (P1E && side == 0 && k.ep >= 0) { bool allEp = true; for (int i = 0; i < n; i++) if (!cb[i].isEp) allEp = false; if (allEp) { val[s] = 1; continue; } }
    if (win) val[s] = winV;
    else if (cnt == 0) val[s] = loseV;
    else deg[s] = (uint8_t)min(cnt, 255);
  }
  eStart[NS] = edges.size();
  // reverse edges
  vector<int> rStart(NS + 1, 0), redges(edges.size());
  for (int e : edges) rStart[e + 1]++;
  for (int i = 0; i < NS; i++) rStart[i + 1] += rStart[i];
  { vector<int> pos(rStart.begin(), rStart.end() - 1);
    for (int s = 0; s < NS; s++) for (int j = eStart[s]; j < eStart[s + 1]; j++) redges[pos[edges[j]]++] = s; }
  vector<int> q; q.reserve(NS);
  for (int s = 0; s < NS; s++) if (val[s] == 1 || val[s] == 2) q.push_back(s);
  for (size_t qi = 0; qi < q.size(); qi++) {
    int t = q[qi];
    for (int j = rStart[t]; j < rStart[t + 1]; j++) {
      int p = redges[j];
      if (val[p] != -1) continue;
      int pside = p / (K * K);
      int pw = pside ? 2 : 1, pl = pside ? 1 : 2;
      if (val[t] == pw) { val[p] = pw; q.push_back(p); }
      else if (--deg[p] == 0) { val[p] = pl; q.push_back(p); }
    }
  }
  vector<uint8_t> packed((NS + 3) / 4, 0);
  for (int s = 0; s < NS; s++) { int v = val[s] < 0 ? 0 : val[s]; packed[s >> 2] |= v << ((s & 3) * 2); }
  cacheBytes += packed.size() + 64; nLayers++;
  auto r = cache.emplace(k, std::move(packed));
  return r.first->second;
}

// ---------------- parsing / printing ----------------
static int parseSq(const string& t) { int f = t[0] - 'a', r = atoi(t.c_str() + 1) - 1; return mk(f, r); }
static string sqName(int s) { string r; r += char('a' + Fo(s)); r += to_string(Ro(s) + 1); return r; }
static bool parsePos(const string& line, Pos& P) {
  istringstream is(line); string t; vector<string> tok;
  while (is >> t) tok.push_back(t);
  if (tok.size() < 3) return false;
  P.w = P.b = 0; P.wk = P.bk = -1;
  for (size_t i = 0; i + 2 < tok.size(); i++) {
    char c = tok[i][0]; int s = parseSq(tok[i].substr(1));
    if (s < 0) return false;
    if (c == 'K') P.wk = s; else if (c == 'k') P.bk = s; else if (c == 'P') P.w |= bit(s); else if (c == 'p') P.b |= bit(s); else return false;
  }
  P.side = tok[tok.size() - 2] == "w" ? 0 : 1;
  string e = tok.back(); P.ep = e == "-" ? -1 : parseSq(e);
  return P.wk >= 0 && P.bk >= 0;
}
static string posStr(const Pos& P) {
  string s = "K" + sqName(P.wk);
  for (int q = 0; q < K; q++) if (P.w & bit(q)) s += " P" + sqName(q);
  s += " k" + sqName(P.bk);
  for (int q = 0; q < K; q++) if (P.b & bit(q)) s += " p" + sqName(q);
  s += P.side ? " b " : " w ";
  s += P.ep >= 0 ? sqName(P.ep) : "-";
  return s;
}
// normalise the e.p. right: keep it only if a pawn of the side to move could capture onto it
static void normEp(Pos& P) {
  if (P.ep < 0) return;
  if (!EPON) { P.ep = -1; return; }
  int S = P.side; u64 own = S ? P.b : P.w; int dir = S ? -1 : 1;
  bool ok = false;
  for (int d = -1; d <= 1; d += 2) { int q = mk(Fo(P.ep) + d, Ro(P.ep) - dir); if (q >= 0 && (own & bit(q))) ok = true; }
  if (!ok || epSide(P.ep) != S || P.ep == P.wk || P.ep == P.bk) P.ep = -1;
}
static int value(Pos P) { // White's view, 0 D 1 W 2 L 3 illegal
  normEp(P);
  if (!legal(P)) return 3;
  if (cacheBytes > MAXMB * 1000000ULL) { cache.clear(); cacheBytes = 0; }
  const vector<uint8_t>& L = lookup(Key{P.w, P.b, P.ep});
  return getv(L, sidx(P.side, P.wk, P.bk));
}
static const char* VC = "DWLX";

// ---------------- main ----------------
int main(int argc, char** argv) {
  if (argc < 2) { fprintf(stderr, "usage: k42 solve|sorties|test ...\n"); return 1; }
  string mode = argv[1];
  string board = "cyl:8x6", fz = "0,1,2", sortf, ctxf; int maxw = 2, maxb = 2; string conf = "", wconf = "", badf, failf; double sampleP = 1.0; long seed = 1; int minp = 0;
  bool moves = false;
  for (int i = 2; i < argc; i++) {
    string a = argv[i];
    if (a == "--board") board = argv[++i];
    else if (a == "--ep") EPON = string(argv[++i]) == "on";
    else if (a == "--pass") PASSW = true;
    else if (a == "--qclause") QCL = true;
    else if (a == "--confine") conf = argv[++i];
    else if (a == "--wconfine") wconf = argv[++i];
    else if (a == "--wstalemate-loss") WSTALL = true;
    else if (a == "--bad") badf = argv[++i];
    else if (a == "--fails") failf = argv[++i];
    else if (a == "--p1e") P1E = true;
    else if (a == "--sample") sampleP = atof(argv[++i]);
    else if (a == "--seed") seed = atol(argv[++i]);
    else if (a == "--minpawns") minp = atoi(argv[++i]);
    else if (a == "--fz") fz = argv[++i];
    else if (a == "--maxw") maxw = atoi(argv[++i]);
    else if (a == "--maxb") maxb = atoi(argv[++i]);
    else if (a == "--sorties") sortf = argv[++i];
    else if (a == "--contexts") ctxf = argv[++i];
    else if (a == "--maxmb") MAXMB = atol(argv[++i]);
    else if (a == "--moves") moves = true;
    else { fprintf(stderr, "bad arg %s\n", a.c_str()); return 1; }
  }
  { auto c = board.find(':'); CYL = board.substr(0, c) == "cyl"; auto x = board.find('x');
    W = atoi(board.substr(c + 1, x - c - 1).c_str()); H = atoi(board.substr(x + 1).c_str()); }
  if (W * H > 64 || H < 6) { fprintf(stderr, "board too large or H < 6\n"); return 1; }
  initBoard();
  vector<int> fzf; { stringstream ss(fz); string t; while (getline(ss, t, ',')) fzf.push_back(atoi(t.c_str())); }
  u64 FZM = 0; for (int f : fzf) for (int r = 0; r < H; r++) FZM |= bit(mk(f, r));
  if (!wconf.empty()) { WCONF = 0; for (char c : wconf) for (int r = 0; r < H; r++) WCONF |= bit(mk(c - 'a', r)); }
  if (!conf.empty()) { BCONF = 0; for (char c : conf) for (int r = 0; r < H; r++) BCONF |= bit(mk(c - 'a', r)); }

  if (mode == "solve") {
    string line;
    while (getline(cin, line)) {
      if (line.empty() || line[0] == '#') { cout << line << "\n"; continue; }
      Pos P; if (!parsePos(line, P)) { cout << line << " | ?\n"; continue; }
      int v = value(P);
      cout << line << " | " << VC[v];
      if (moves && v != 3) {
        Child cb[64]; char nm[64][12]; Pos Q = P; normEp(Q); int n = gen(Q, cb, nm);
        cout << " |";
        for (int i = 0; i < n; i++) { int cv = cb[i].term >= 0 ? cb[i].term : value(cb[i].p); cout << " " << nm[i] << ":" << VC[cv]; }
      }
      cout << "\n"; cout.flush();
    }
    fprintf(stderr, "[k42 %s layers=%ld cacheMB=%zu]\n", board.c_str(), nLayers, cacheBytes / 1000000);
    return 0;
  }

  if (mode == "sorties") {
    // Roots Y: both kings on F_Z, Z-pawns on F_Z (ranks 2..H-1), White to move, no e.p. right, legal.
    // For each legal non-promoting White Z-move m after which Black has no immediate promotion:
    // admissible replies r = Black non-promoting moves that leave Black's king on F_Z (all Black moves are Z-moves).
    // plain(r) = Black wins L^0 at Q_Z = Q (no context); pass(r) = Black wins the k = infinity game.
    // Output, per m: "<Y> | <m> | <position after m> | P0 Pinf P0q Pinfq" where P0 = some r wins plain,
    // Pinf = some r wins pass ((L1_P) form), q = queen-clause forms. Only lines with P0 or P0q and not both
    // pass flags... all lines with (P0 && !Pinf) || (P0q && !Pinfq) are printed.
    BCONF = FZM;
    vector<int> sqs; for (int f : fzf) for (int r = 1; r < H - 1; r++) sqs.push_back(mk(f, r));
    vector<int> ksq; for (int f : fzf) for (int r = 0; r < H; r++) ksq.push_back(mk(f, r));
    int ns = sqs.size();
    vector<u64> sets[8];
    for (u64 m = 0; m < (1ULL << ns); m++) { int c = __builtin_popcountll(m); if (c > max(maxw, maxb)) continue;
      u64 bb = 0; for (int i = 0; i < ns; i++) if (m >> i & 1) bb |= bit(sqs[i]); sets[c].push_back(bb); }
    // four solver "modes" share one cache keyed additionally by mode: we run them as separate passes instead.
    long nroot = 0, nsort = 0, nout = 0;
    struct Rec { Pos Y; string mv; Pos after; vector<Pos> rs; };
    vector<Rec> recs;
    for (int a = 0; a <= maxw; a++) for (int b = 0; b <= maxb; b++)
      for (u64 wp : sets[a]) for (u64 bp : sets[b]) {
        if (wp & bp) continue;
        for (int wk : ksq) for (int bk : ksq) {
          Pos Y{wp, bp, wk, bk, 0, -1};
          if (a + b < minp) continue;
          if (sampleP < 1.0) { u64 h = (wp * 0x9E3779B97F4A7C15ULL) ^ (bp * 0xC2B2AE3D27D4EB4FULL) ^ ((u64)(wk * 64 + bk + 1) * 0x165667B19E3779F9ULL) ^ (u64)seed;
            h ^= h >> 29; h *= 0xBF58476D1CE4E5B9ULL; h ^= h >> 32; if ((double)(h % 1000000) / 1e6 >= sampleP) continue; }
          if (!legal(Y)) continue;
          nroot++;
          Child cb[64]; char nm[64][12];
          int saveP = PASSW; PASSW = false;
          int n = gen(Y, cb, nm);
          for (int i = 0; i < n; i++) {
            if (cb[i].term >= 0) continue;          // promotion: not a sortie
            Pos A = cb[i].p;
            Child cr[64]; int nr = gen(A, cr);
            bool immp = false; vector<Pos> rs;
            for (int j = 0; j < nr; j++) { if (cr[j].term >= 0) { immp = true; break; } if (FZM & bit(cr[j].p.bk)) rs.push_back(cr[j].p); }
            if (immp || rs.empty()) continue;
            nsort++;
            recs.push_back({Y, nm[i], A, rs});
          }
          PASSW = saveP;
        }
      }
    fprintf(stderr, "roots %ld sorties %ld\n", nroot, nsort);
    // flags
    vector<array<int, 4>> fl(recs.size(), {0, 0, 0, 0});
    for (int md = 0; md < 4; md++) {
      cache.clear(); cacheBytes = 0;
      PASSW = md & 1; QCL = md & 2;
      for (size_t i = 0; i < recs.size(); i++) {
        for (auto& Q : recs[i].rs) { if (value(Q) == 2) { fl[i][md] = 1; break; } }
      }
      fprintf(stderr, "mode %d done, layers %ld\n", md, nLayers);
    }
    for (size_t i = 0; i < recs.size(); i++) {
      bool po = fl[i][0] && !fl[i][1], poq = fl[i][2] && !fl[i][3];
      if (!po && !poq) continue;
      nout++;
      cout << posStr(recs[i].Y) << " | " << recs[i].mv << " | " << posStr(recs[i].after) << " | "
           << fl[i][0] << fl[i][1] << fl[i][2] << fl[i][3] << "\n";
    }
    fprintf(stderr, "plain-only sorties (either form) %ld\n", nout);
    return 0;
  }
  if (mode == "test") {
    // sorties file: lines "<Y> | <m> | <after> | flags" ; contexts file: lines "<id> <pawn tokens...>"
    vector<pair<string, Pos>> S; vector<pair<string, pair<u64, u64>>> C;
    { ifstream f(sortf); string line;
      while (getline(f, line)) { if (line.empty() || line[0] == '#') continue;
        vector<string> parts; size_t p0 = 0, p;
        while ((p = line.find(" | ", p0)) != string::npos) { parts.push_back(line.substr(p0, p - p0)); p0 = p + 3; }
        parts.push_back(line.substr(p0));
        Pos A; if (!parsePos(parts[2], A)) { fprintf(stderr, "bad sortie %s\n", line.c_str()); return 1; }
        S.push_back({parts[0] + " | " + parts[1] + " | " + parts[3], A}); } }
    { ifstream f(ctxf); string line;
      while (getline(f, line)) { if (line.empty() || line[0] == '#') continue;
        istringstream is(line); string id, t; is >> id; u64 w = 0, b = 0;
        while (is >> t) { int s = parseSq(t.substr(1)); if (t[0] == 'P') w |= bit(s); else b |= bit(s); }
        C.push_back({id, {w, b}}); } }
    for (auto& c : C) {
      long cnt[4] = {0, 0, 0, 0};
      for (auto& s : S) {
        Pos P = s.second;
        if ((P.w | P.b) & (c.second.first | c.second.second)) { cnt[3]++; continue; }
        P.w |= c.second.first; P.b |= c.second.second;
        int v = value(P);
        cnt[v]++;
        if (v == 0 || v == 1) cout << "FAIL | " << c.first << " | " << s.first << " | " << posStr(P) << " | " << VC[v] << "\n";
      }
      cout << "SUM | " << c.first << " | L " << cnt[2] << " D " << cnt[0] << " W " << cnt[1] << " X " << cnt[3] << "\n";
      cout.flush();
      fprintf(stderr, "context %s done, layers %ld, cacheMB %zu\n", c.first.c_str(), nLayers, cacheBytes / 1000000);
    }
    return 0;
  }
  if (mode == "cert") {
    // For every sortie (position after m, Black to move) and every context line "<id> sq sq ..." of the bad-square
    // file: is there an admissible reply r with which Black wins the plain local game L^0(Q_Z) in which a White king
    // step onto a bad square is a failure for Black, and (with --p1e) an e.p.-only White node is a failure too?
    // Pairs whose real position (sortie + context) is illegal are skipped. --fails TESTOUT gives the FAIL lines of
    // a test run; the output counts certified pairs and lists certified pairs that are FAIL lines (should be none).
    BCONF = FZM; PASSW = false;
    vector<pair<string, Pos>> S;
    { ifstream f(sortf); string line;
      while (getline(f, line)) { if (line.empty() || line[0] == '#') continue;
        vector<string> parts; size_t p0 = 0, p;
        while ((p = line.find(" | ", p0)) != string::npos) { parts.push_back(line.substr(p0, p - p0)); p0 = p + 3; }
        parts.push_back(line.substr(p0));
        Pos A; parsePos(parts[2], A); S.push_back({parts[0] + " | " + parts[1], A}); } }
    vector<pair<string, u64>> bads; map<string, pair<u64, u64>> ctxp;
    { ifstream f(badf); string line;
      while (getline(f, line)) { istringstream is(line); string id, t; is >> id; u64 m = 0; while (is >> t) m |= bit(parseSq(t)); bads.push_back({id, m}); } }
    { ifstream f(ctxf); string line;
      while (getline(f, line)) { if (line.empty() || line[0] == '#') continue; istringstream is(line); string id, t; is >> id; u64 w = 0, b = 0;
        while (is >> t) { int q = parseSq(t.substr(1)); if (t[0] == 'P') w |= bit(q); else b |= bit(q); } ctxp[id] = {w, b}; } }
    set<string> fails;
    if (!failf.empty()) { ifstream f(failf); string line;
      while (getline(f, line)) { if (line.rfind("FAIL | ", 0) != 0) continue;
        vector<string> parts; size_t p0 = 0, p;
        while ((p = line.find(" | ", p0)) != string::npos) { parts.push_back(line.substr(p0, p - p0)); p0 = p + 3; }
        fails.insert(parts[1] + " | " + parts[2] + " | " + parts[3]); } }
    for (auto& bd : bads) {
      cache.clear(); cacheBytes = 0; WBAD = bd.second;
      auto cp = ctxp[bd.first];
      long legalPairs = 0, cert = 0, certFail = 0;
      for (auto& s : S) {
        Pos R = s.second;
        if ((R.w | R.b) & (cp.first | cp.second)) continue;
        Pos RR = R; RR.w |= cp.first; RR.b |= cp.second;
        if (!legal(RR)) continue;
        legalPairs++;
        Child cr[64]; int nr = gen(R, cr);
        bool ok = false;
        for (int j = 0; j < nr && !ok; j++) { if (cr[j].term >= 0) continue; if (!(FZM & bit(cr[j].p.bk))) continue;
          if (WBAD & bit(cr[j].p.wk)) continue;
          Pos q = cr[j].p; normEp(q); if (q.ep >= 0) continue;   // Proposition 8.1 needs Q without an e.p. right
          if (value(q) == 2) ok = true; }
        if (ok) { cert++; if (fails.count(bd.first + " | " + s.first)) { certFail++; cout << "CERTFAIL | " << bd.first << " | " << s.first << "\n"; } }
      }
      cout << "CSUM | " << bd.first << " | legal " << legalPairs << " cert " << cert << " certfail " << certFail << "\n"; cout.flush();
    }
    return 0;
  }
  fprintf(stderr, "unknown mode\n");
  return 1;
}
