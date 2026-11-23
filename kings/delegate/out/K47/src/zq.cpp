// K47 experiment: size of the bisimulation quotient of the component graph (labels: valid, check, promo per side;
// edges: White moves, Black moves, the e.p.-clearing map).
#define main za_main
#include "za.cpp"
#undef main
#include <map>
int main(int argc, char** argv) {
  W = atoi(argv[1]); H = atoi(argv[2]); NSQ = W * H;
  vector<Pl> roots; { ifstream f(argv[3]); string l; while (getline(f, l)) if (!l.empty() && l[0] != '#') roots.push_back(parse(l)); }
  build(roots); size_t N = nodes.size();
  vector<int> cls(N, 0), nc(N);
  for (size_t z = 0; z < N; z++) cls[z] = valid[0][z] | valid[1][z] << 1 | chk[0][z] << 2 | chk[1][z] << 3 | prom[0][z] << 4 | prom[1][z] << 5;
  size_t ncls = 0;
  for (int round = 0; round < 500; round++) {
    map<vector<int>, int> sig; vector<int> s;
    for (size_t z = 0; z < N; z++) {
      s.clear(); s.push_back(cls[z]); s.push_back(cls[clr[z]]);
      for (int c = 0; c < 2; c++) { vector<int> t; for (int k = sOff[c][z]; k < sOff[c][z + 1]; k++) t.push_back(cls[sLst[c][k]]);
        sort(t.begin(), t.end()); t.erase(unique(t.begin(), t.end()), t.end()); s.push_back(-1); s.insert(s.end(), t.begin(), t.end()); }
      auto it = sig.find(s); if (it == sig.end()) it = sig.emplace(s, sig.size()).first; nc[z] = it->second; }
    fprintf(stderr, "round %d classes %zu\n", round, sig.size());
    if (sig.size() == ncls) break; ncls = sig.size(); cls = nc;
  }
}
