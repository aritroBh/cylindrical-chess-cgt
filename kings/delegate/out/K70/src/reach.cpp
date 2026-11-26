// Reachability in a repertoire. Each bit denotes a possible white king.
#include <vector>
#include <algorithm>
#include <cstdint>
using namespace std;
using U=uint64_t;
struct Edge{int dst, id; U mask; bool king;};
struct Node{int t; U valid,mate,won,base; vector<Edge> e;};
vector<Node> g;
vector<char> enabled;
extern "C" void reset_graph(){g.clear(); enabled.assign(1,1);}
extern "C" int node(int t,U valid,U mate,U base){g.push_back({t,valid,mate,0,base,{}});return g.size()-1;}
extern "C" int edge(int i,int d,U mask,int king){
 int id=0;if(g[i].t){id=enabled.size();enabled.push_back(1);}
 g[i].e.push_back({d,id,mask,bool(king)});return id;
}
inline U around(U m){
 U a=(m&0x7f7f7f7f7f7f7f7fULL)<<1,b=(m&0xfefefefefefefefeULL)>>1;
 return a|b|((a|b|m)<<8)|((a|b|m)>>8);
}
vector<int> order;
extern "C" void set_order(int *p,int n){order.assign(p,p+n);}
extern "C" void toggle(int id,int on){enabled[id]=on;}
extern "C" void run(int hold){
 for(auto &n:g)n.won=hold?n.valid:0;
 bool changed;
 do{changed=false;for(int i:order){auto &n=g[i];U v=0;
  if(n.t){
   for(auto e:n.e)if(enabled[e.id])v|=e.mask & (e.dst<0?~U(0):g[e.dst].won);
  }else{
   for(auto e:n.e){U fail=e.mask & (e.dst<0?~U(0):~g[e.dst].won);
    v|=e.king?around(fail):fail;}
   v=n.mate & ~v;
  }
  v|=n.base; if(v!=n.won){n.won=v;changed=true;}
 }}while(changed);
}
extern "C" U zone(int i){return g[i].won;}
