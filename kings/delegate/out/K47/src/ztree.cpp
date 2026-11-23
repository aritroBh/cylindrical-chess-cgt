// K47 proof aid: P values with depth (plies to the end under best play: the winner hurries, the loser delays) on the
// component graph of za.cpp, and a printed proof tree (winner: one fastest move; loser: every move).
// Usage: ztree <W> <H> <roots file> <queries file> <maxdepth>
//   queries: lines "<pieces> <w|b>" (no e.p.); prints the move list with values and depths, then the tree.
#define main za_main
#include "za.cpp"
#undef main
vector<int16_t> dep[2]; vector<uint8_t> pv[2];  // pv: 0 draw, 1 mover wins, 2 mover loses
string sqs(int q) { return string(1, char('a' + F(q))) + char('1' + R(q)); }
string mname(const Pl& a, const Pl& b, int c) {
  if (c == 0 && a.wk != b.wk) return "K" + sqs(a.wk) + (a.bp != b.bp ? "x" : "-") + sqs(b.wk);
  if (c == 1 && a.bk != b.bk) return "k" + sqs(a.bk) + (a.wp != b.wp ? "x" : "-") + sqs(b.bk);
  u64 o = c == 0 ? a.wp : a.bp, n = c == 0 ? b.wp : b.bp; u64 gone = o & ~n, came = n & ~o;
  bool cap = c == 0 ? a.bp != b.bp : a.wp != b.wp;
  return string(c == 0 ? "P" : "p") + sqs(__builtin_ctzll(gone)) + (cap ? "x" : "-") + sqs(__builtin_ctzll(came));
}
string pstr(const Pl& p) {
  string s = "K" + sqs(p.wk) + " k" + sqs(p.bk);
  for (u64 b = p.wp; b; b &= b - 1) s += " P" + sqs(__builtin_ctzll(b));
  for (u64 b = p.bp; b; b &= b - 1) s += " p" + sqs(__builtin_ctzll(b));
  if (p.ep >= 0) s += " ep" + sqs(p.ep);
  return s;
}
void solveP() {
  size_t N = nodes.size();
  for (int c = 0; c < 2; c++) { dep[c].assign(N, -1); pv[c].assign(N, 0); }
  // ply rounds: round d decides states whose value is fixed with depth d
  for (size_t z = 0; z < N; z++) for (int c = 0; c < 2; c++) {
    if (!valid[c][z]) { pv[c][z] = 3; continue; }
    if (prom[c][z]) { pv[c][z] = 1; dep[c][z] = 1; }
    else if (sOff[c][z + 1] == sOff[c][z]) { if (chk[c][z]) { pv[c][z] = 2; dep[c][z] = 0; } else { pv[c][z] = 0; dep[c][z] = 0; } }
  }
  for (int d = 1; d < 400; d++) {
    size_t changed = 0;
    for (size_t z = 0; z < N; z++) for (int c = 0; c < 2; c++) {
      if (pv[c][z] == 3 || dep[c][z] >= 0) continue;
      bool win = false, allLose = true;
      for (int k = sOff[c][z]; k < sOff[c][z + 1]; k++) { int y = sLst[c][k];
        int16_t dy = dep[1 - c][y]; uint8_t vy = pv[1 - c][y];
        if (dy >= 0 && dy <= d - 1 && vy == 2) win = true;
        if (!(dy >= 0 && dy <= d - 1 && vy == 1)) allLose = false; }
      if (win) { pv[c][z] = 1; dep[c][z] = d; changed++; }
      else if (allLose) { pv[c][z] = 2; dep[c][z] = d; changed++; }
    }
    if (!changed && d > 2) { bool more = false; (void)more; }
    if (!changed && d > 60) break;
  }
}
void tree(int z, int c, int indent, int maxd) {
  const Pl& p = nodes[z];
  string pad(indent * 2, ' ');
  if (pv[c][z] == 1 && prom[c][z]) { printf("%s%s promotes\n", pad.c_str(), c ? "Black" : "White"); return; }
  if (indent >= maxd) { printf("%s...\n", pad.c_str()); return; }
  if (pv[c][z] == 1) {  // winner: fastest move
    int best = -1;
    for (int k = sOff[c][z]; k < sOff[c][z + 1]; k++) { int y = sLst[c][k];
      if (pv[1 - c][y] == 2 && dep[1 - c][y] == dep[c][z] - 1) { best = y; break; } }
    printf("%s%s  [%s wins, %d]\n", pad.c_str(), mname(p, nodes[best], c).c_str(), c ? "Black" : "White", dep[c][z]);
    tree(best, 1 - c, indent + 1, maxd);
  } else if (pv[c][z] == 2) {
    if (sOff[c][z + 1] == sOff[c][z]) { printf("%s(%s checkmated)\n", pad.c_str(), c ? "Black" : "White"); return; }
    for (int k = sOff[c][z]; k < sOff[c][z + 1]; k++) { int y = sLst[c][k];
      printf("%s%s:\n", pad.c_str(), mname(p, nodes[y], c).c_str()); tree(y, 1 - c, indent + 1, maxd); }
  } else printf("%s(draw)\n", pad.c_str());
}
int main(int argc, char** argv) {
  W = atoi(argv[1]); H = atoi(argv[2]); NSQ = W * H; int maxd = atoi(argv[5]);
  vector<Pl> roots; { ifstream f(argv[3]); string l; while (getline(f, l)) if (!l.empty() && l[0] != '#') roots.push_back(parse(l)); }
  build(roots); solveP();
  ifstream f(argv[4]); string l;
  while (getline(f, l)) { if (l.empty() || l[0] == '#') { printf("%s\n", l.c_str()); continue; }
    size_t sp = l.find_last_of(' '); int c = l[sp + 1] == 'b'; Pl p = parse(l.substr(0, sp));
    auto it = idx.find(key(p)); if (it == idx.end()) { printf("NOT IN COMPONENT: %s\n", l.c_str()); continue; }
    int z = it->second;
    const char* vs[] = {"draw", "mover wins", "mover loses", "invalid"};
    printf("== %s, %s to move: %s in %d plies\n", pstr(p).c_str(), c ? "Black" : "White", vs[pv[c][z]], dep[c][z]);
    vector<Pl> mv; bool pr; gen(p, c, mv, pr);
    if (pr) printf("   promotion available\n");
    for (int k = sOff[c][z]; k < sOff[c][z + 1]; k++) { int y = sLst[c][k];
      printf("   %-10s -> opponent %s (%d)\n", mname(p, nodes[y], c).c_str(), vs[pv[1 - c][y]], dep[1 - c][y]); }
    tree(z, c, 1, maxd);
  }
}
