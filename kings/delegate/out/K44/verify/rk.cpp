// rk.cpp -- K44 referee's own solver for the local king game LK (K20 definition text), written from the
// definition in kings/delegate/out/K20/summary.json and LOOPY Definitions 1.1-1.3; no code taken from kg/lk/lk3.
// Usage:
//   rk BOARD FILES PAIRS [KINGS...]
//     BOARD  cyl:WxH or pln:WxH
//     FILES  region as "all" or "lo-hi" (file letters, cyclic arc from lo to hi, e.g. a-c, i-b)
//     PAIRS  comma list of white pawn squares, e.g. a2,c4,f2  (black pawn one rank above)
//     KINGS  optional list "c3/a4" (white/black); without it every legal root is classified.
// Output: per root (or class counts) the B34 signature and the B34 name.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <map>
#include <unordered_map>
#include <deque>
#include <cctype>
#include <set>
#include <functional>
#include <algorithm>
using namespace std;

static const int PLUS = -1, MINUS = -2;
struct Graph { vector<vector<int>> L, R; vector<string> nm;
  int add(const string& s){ L.emplace_back(); R.emplace_back(); nm.push_back(s); return (int)L.size()-1; } };
Graph G;

// ---------------- battery B34 ----------------
vector<string> bname; vector<int> broot;
void buildBattery(){
  auto nb=[&](const string&s){return G.add(s);};
  int z=nb("0"); int st=nb("*"); G.L[st]={z}; G.R[st]={z};
  int p1=nb("+1"); G.L[p1]={z}; int m1=nb("-1"); G.R[m1]={z};
  int p2=nb("+2"); G.L[p2]={p1}; int m2=nb("-2"); G.R[m2]={m1};
  int p3=nb("+3"); G.L[p3]={p2}; int m3=nb("-3"); G.R[m3]={m2};
  int h=nb("1/2"); G.L[h]={z}; G.R[h]={p1}; int mh=nb("-1/2"); G.L[mh]={m1}; G.R[mh]={z};
  int up=nb("up"); G.L[up]={z}; G.R[up]={st}; int dn=nb("down"); G.L[dn]={st}; G.R[dn]={z};
  int ups=nb("up*"); G.L[ups]={z,st}; G.R[ups]={z}; int dns=nb("down*"); G.L[dns]={z}; G.R[dns]={z,st};
  int s2=nb("*2"); G.L[s2]={z,st}; G.R[s2]={z,st};
  int on=nb("on"); G.L[on]={on}; int off=nb("off"); G.R[off]={off}; int dud=nb("dud"); G.L[dud]={dud}; G.R[dud]={dud};
  int ov=nb("over"); G.L[ov]={z}; G.R[ov]={ov}; int un=nb("under"); G.L[un]={un}; G.R[un]={z};
  int tis=nb("tis"); int tisn=nb("tisn"); G.L[tis]={tisn}; G.R[tisn]={tis};
  int t1=nb("{+|}"); G.L[t1]={PLUS}; int t2=nb("{|-}"); G.R[t2]={MINUS};
  int t3=nb("{+|-}"); G.L[t3]={PLUS}; G.R[t3]={MINUS};
  int t4=nb("{+|0}"); G.L[t4]={PLUS}; G.R[t4]={z}; int t5=nb("{0|-}"); G.L[t5]={z}; G.R[t5]={MINUS};
  int s10=nb("{1|0}"); G.L[s10]={p1}; G.R[s10]={z}; int s01=nb("{0|-1}"); G.L[s01]={z}; G.R[s01]={m1};
  int s20=nb("{2|0}"); G.L[s20]={p2}; G.R[s20]={z}; int s02=nb("{0|-2}"); G.L[s02]={z}; G.R[s02]={m2};
  int pon=nb("{+|on}"); G.L[pon]={PLUS}; G.R[pon]={on}; int offm=nb("{off|-}"); G.L[offm]={off}; G.R[offm]={MINUS};
  int onoff=nb("{on|off}"); G.L[onoff]={on}; G.R[onoff]={off};
  int order[]={z,st,p1,m1,p2,m2,p3,m3,h,mh,up,dn,ups,dns,s2,on,off,dud,ov,un,tis,tisn,t1,t2,t3,t4,t5,s10,s01,s20,s02,pon,offm,onoff};
  for(int x:order){ broot.push_back(x); bname.push_back(G.nm[x]); }
}

// ---------------- sum solver (retrograde on A x B x mover) ----------------
// result: 'W' white wins, 'L' black wins, 'D' draw (infinite play)
struct Solve {
  vector<int> A,B; unordered_map<int,int> ia, ib; vector<char> res;
  int NA,NB;
  int idx(int a,int b,int m){ return ((ia[a]*NB)+ib[b])*2+m; }
  char get(int a,int b,int m){ return res[((ia.at(a)*NB)+ib.at(b))*2+m]; }
  void run(const vector<int>&A_, const vector<int>&B_){
    A=A_;B=B_;NA=A.size();NB=B.size();
    for(int i=0;i<NA;i++) ia[A[i]]=i; for(int i=0;i<NB;i++) ib[B[i]]=i;
    size_t N=(size_t)NA*NB*2; res.assign(N,0); vector<int> cnt(N,0);
    // reverse adjacency restricted to A and to B
    vector<vector<int>> rLA(NA), rRA(NA), rLB(NB), rRB(NB);
    for(int i=0;i<NA;i++){ for(int o:G.L[A[i]]) if(o>=0) rLA[ia.at(o)].push_back(i); for(int o:G.R[A[i]]) if(o>=0) rRA[ia.at(o)].push_back(i); }
    for(int i=0;i<NB;i++){ for(int o:G.L[B[i]]) if(o>=0) rLB[ib.at(o)].push_back(i); for(int o:G.R[B[i]]) if(o>=0) rRB[ib.at(o)].push_back(i); }
    deque<size_t> q;
    auto setr=[&](size_t s,char r){ if(!res[s]){res[s]=r;q.push_back(s);} };
    for(int i=0;i<NA;i++) for(int j=0;j<NB;j++) for(int m=0;m<2;m++){
      size_t s=((size_t)i*NB+j)*2+m;
      const vector<int>&oa = m==0? G.L[A[i]]:G.R[A[i]];
      const vector<int>&ob = m==0? G.L[B[j]]:G.R[B[j]];
      int good = m==0?PLUS:MINUS, bad = m==0?MINUS:PLUS; bool win=false; int c=0;
      for(int o:oa){ if(o==good) win=true; else if(o!=bad) c++; }
      for(int o:ob){ if(o==good) win=true; else if(o!=bad) c++; }
      cnt[s]=c;
      if(win) setr(s, m==0?'W':'L'); else if(c==0) setr(s, m==0?'L':'W');
    }
    while(!q.empty()){ size_t s=q.front(); q.pop_front(); char r=res[s];
      int m=s%2; size_t ij=s/2; int i=ij/NB, j=ij%NB; int pm=1-m; // predecessor mover
      auto touch=[&](size_t p){ if(res[p]) return; char good = pm==0?'W':'L';
        if(r==good) setr(p,good); else if(--cnt[p]==0) setr(p, pm==0?'L':'W'); };
      const vector<vector<int>>&ra = pm==0? rLA:rRA; const vector<vector<int>>&rb = pm==0? rLB:rRB;
      for(int pi:ra[i]) touch(((size_t)pi*NB+j)*2+pm);
      for(int pj:rb[j]) touch(((size_t)i*NB+pj)*2+pm);
    }
    for(auto&x:res) if(!x) x='D';
  }
};

// ---------------- LK ----------------
int W,H; bool cyl; vector<char> inR; // region by file
struct Pawn{int f,r; bool white;}; vector<Pawn> P;
int fadd(int f,int d){ int g=f+d; if(cyl){ g%=W; if(g<0) g+=W; return g;} return (g<0||g>=W)?-1:g; }
bool fadj(int a,int b){ if(a==b) return true; return fadd(a,1)==b||fadd(a,-1)==b; }
int sq(int f,int r){ return f*(H+1)+r; }
bool kadj(int s,int t){ int f1=s/(H+1),r1=s%(H+1),f2=t/(H+1),r2=t%(H+1); return fadj(f1,f2)&&abs(r1-r2)<=1&&s!=t; }
bool attackedBy(int S,int f,int r,bool byWhite){ // by alive pawns of colour
  for(size_t i=0;i<P.size();i++) if((S>>i)&1){ auto&p=P[i]; if(p.white!=byWhite) continue;
    int ar = p.white? p.r+1 : p.r-1; if(ar!=r) continue; if(fadd(p.f,1)==f||fadd(p.f,-1)==f) return true; }
  return false; }
int pawnAt(int S,int f,int r){ for(size_t i=0;i<P.size();i++) if(((S>>i)&1)&&P[i].f==f&&P[i].r==r) return i; return -1; }
bool passedSide(int S,bool white){
  for(size_t i=0;i<P.size();i++) if(((S>>i)&1)&&P[i].white==white){ bool pas=true;
    for(size_t j=0;j<P.size();j++) if(((S>>j)&1)&&P[j].white!=white){
      if(!fadj(P[i].f,P[j].f)) continue; if(white? P[j].r>P[i].r : P[j].r<P[i].r) pas=false; }
    if(pas) return true; }
  return false; }
long races=0;
map<long,int> lkid; vector<long> lkkey;
long key(int S,int wk,int bk){ return ((long)S*4096+wk)*4096+bk; }
bool legal(int S,int wk,int bk){
  int wf=wk/(H+1),wr=wk%(H+1),bf=bk/(H+1),br=bk%(H+1);
  if(wk==bk||kadj(wk,bk)) return false; if(pawnAt(S,wf,wr)>=0||pawnAt(S,bf,br)>=0) return false;
  if(attackedBy(S,wf,wr,false)||attackedBy(S,bf,br,true)) return false; return inR[wf]&&inR[bf]; }
int getNode(int S,int wk,int bk, deque<int>&todo){ long k=key(S,wk,bk); auto it=lkid.find(k); if(it!=lkid.end()) return it->second;
  int id=G.add(""); lkid[k]=id; lkkey.resize(G.L.size()); lkkey[id]=k; todo.push_back(id); return id; }
void expand(int id, deque<int>&todo){ long k=lkkey[id]; int bk=k%4096, wk=(k/4096)%4096, S=k/4096/4096;
  for(int side=0;side<2;side++){ bool white=side==0; int me= white?wk:bk, en= white?bk:wk; int f=me/(H+1), r=me%(H+1);
    vector<int> opt;
    for(int df=-1;df<=1;df++) for(int dr=-1;dr<=1;dr++){ if(!df&&!dr) continue; int tf=fadd(f,df), tr=r+dr;
      if(tf<0||tr<1||tr>H||!inR[tf]) continue; int t=sq(tf,tr); if(t==en||kadj(t,en)) continue;
      int pi=pawnAt(S,tf,tr); int S2=S;
      if(pi>=0){ if(P[pi].white==white) continue; S2=S&~(1<<pi); }
      if(attackedBy(S2,tf,tr,!white)) continue;
      if(pi>=0){ bool pw=passedSide(S2,true), pb=passedSide(S2,false);
        if(pw&&pb){ races++; } if(pw&&!pb){ opt.push_back(PLUS); continue; } if(pb&&!pw){ opt.push_back(MINUS); continue; } }
      int nw= white? t:wk, nbk= white? bk:t; opt.push_back(getNode(S2,nw,nbk,todo)); }
    if(white) G.L[id]=opt; else G.R[id]=opt; } }
int parseFile(char c){ return c-'a'; }
string sqs(int s){ char b[8]; snprintf(b,8,"%c%d",'a'+s/(H+1),s%(H+1)); return b; }

int main(int argc,char**argv){
  if(argc<4){ fprintf(stderr,"usage\n"); return 1; }
  string bd=argv[1]; cyl = bd.substr(0,3)=="cyl"; sscanf(bd.c_str()+4,"%dx%d",&W,&H);
  inR.assign(W,0); string rg=argv[2];
  if(rg=="all") for(int f=0;f<W;f++) inR[f]=1; else { int lo,hi; if(isdigit(rg[0])) sscanf(rg.c_str(),"%d-%d",&lo,&hi); else { lo=parseFile(rg[0]); hi=parseFile(rg[2]); } for(int f=lo;;f=fadd(f,1)){ inR[f]=1; if(f==hi) break; } }
  { string ps=argv[3]; size_t p=0; while(p<ps.size()){ size_t c=ps.find(',',p); if(c==string::npos) c=ps.size(); string t=ps.substr(p,c-p);
      int f=parseFile(t[0]), r=atoi(t.c_str()+1); P.push_back({f,r,true}); P.push_back({f,r+1,false}); p=c+1; } }
  buildBattery(); int NBat=G.L.size();
  int Sfull=(1<<P.size())-1; deque<int> todo; vector<int> roots; vector<pair<int,int>> rk;
  if(argc>4){ for(int a=4;a<argc;a++){ string s=argv[a]; size_t sl=s.find('/'); int wk=sq(parseFile(s[0]),atoi(s.substr(1,sl-1).c_str())); int bk=sq(parseFile(s[sl+1]),atoi(s.c_str()+sl+2));
      if(!legal(Sfull,wk,bk)){ printf("%s illegal\n",s.c_str()); continue; } roots.push_back(getNode(Sfull,wk,bk,todo)); rk.push_back({wk,bk}); } }
  else { for(int wk=0;wk<W*(H+1);wk++) for(int bk=0;bk<W*(H+1);bk++){ if(wk%(H+1)==0||bk%(H+1)==0) continue; if(legal(Sfull,wk,bk)){ roots.push_back(getNode(Sfull,wk,bk,todo)); rk.push_back({wk,bk}); } } }
  while(!todo.empty()){ int id=todo.front(); todo.pop_front(); expand(id,todo); }
  vector<int> A; for(int i=NBat;i<(int)G.L.size();i++) A.push_back(i); vector<int> Bv; for(int i=0;i<NBat;i++) Bv.push_back(i);

  if(getenv("RK_BISIM")){ // coarsest bisimulation on the LK nodes (options L, R; terminals + and - as fixed classes)
    int n=G.L.size(); vector<int> cl(n,0); int nc=1;
    for(int it=0;;it++){ map<pair<int,pair<vector<int>,vector<int>>>,int> m; vector<int> nc2(n,0);
      for(int i=NBat;i<n;i++){ vector<int> l,r; for(int o:G.L[i]) l.push_back(o<0?o:cl[o]); for(int o:G.R[i]) r.push_back(o<0?o:cl[o]);
        sort(l.begin(),l.end()); l.erase(unique(l.begin(),l.end()),l.end()); sort(r.begin(),r.end()); r.erase(unique(r.begin(),r.end()),r.end());
        auto k=make_pair(cl[i],make_pair(l,r)); auto f=m.find(k); if(f==m.end()){ int id=m.size(); m[k]=id; nc2[i]=id;} else nc2[i]=f->second; }
      int cnt=m.size(); cl=nc2; if(cnt==nc) break; nc=cnt; }
    printf("# bisimulation classes %d of %zu nodes\n", nc, A.size());
    // option edges of the quotient
    set<pair<int,int>> eL,eR; for(int i=NBat;i<n;i++){ for(int o:G.L[i]) eL.insert({cl[i],o<0?o:cl[o]}); for(int o:G.R[i]) eR.insert({cl[i],o<0?o:cl[o]}); }
    printf("# quotient option edges %zu\n", eL.size()+eR.size());
  }
  Solve ref; ref.run(Bv,Bv); Solve s; s.run(A,Bv);
  vector<string> refsig; for(int h:broot){ string z; for(int k:broot){ z+=ref.get(h,k,0); z+=ref.get(h,k,1);} refsig.push_back(z); }
  // check reference signatures distinct
  for(size_t i=0;i<refsig.size();i++) for(size_t j=0;j<i;j++) if(refsig[i]==refsig[j]) fprintf(stderr,"ref sig clash %s %s\n",bname[i].c_str(),bname[j].c_str());
  // acyclicity of each root's reachable graph
  map<string,int> cls; map<string,int> unsig;
  printf("# nodes %zu races %ld roots %zu\n", A.size(), races, roots.size());
  for(size_t i=0;i<roots.size();i++){ string z; for(int k:broot){ z+=s.get(roots[i],k,0); z+=s.get(roots[i],k,1);} string name="?";
    for(size_t h=0;h<refsig.size();h++) if(refsig[h]==z) name=bname[h];
    if(name=="?") unsig[z]++;
    cls[name]++;
    if(argc>4 || getenv("RK_ALL")) { printf("K%s k%s %s ", sqs(rk[i].first).c_str(), sqs(rk[i].second).c_str(), name.c_str());
      for(size_t k=0;k<broot.size();k++) printf(" %s:%c%c", bname[k].c_str(), z[2*k], z[2*k+1]); printf("\n"); }
  }
  if(getenv("RK_SIGS")) for(auto&u:unsig) printf("SIG %s %d\n",u.first.c_str(),u.second);

  if(getenv("RK_PAIRS")){ // contexts: every B34 game and every sum of two B34 games (with repetition); compare each root with the reference named in RK_PAIRS
    string refn=getenv("RK_PAIRS"); int refnode=-1; for(size_t h=0;h<bname.size();h++) if(bname[h]==refn) refnode=broot[h];
    map<pair<int,int>,int> memo; vector<int> Bx; for(int i=0;i<NBat;i++) Bx.push_back(i);
    std::function<int(int,int)> sum=[&](int a,int b)->int{ auto k=make_pair(a,b); auto f=memo.find(k); if(f!=memo.end()) return f->second;
      int id=G.add("sum"); memo[k]=id; Bx.push_back(id); vector<int> l,r;
      for(int o:G.L[a]) l.push_back(o<0?o:sum(o,b)); for(int o:G.L[b]) l.push_back(o<0?o:sum(a,o));
      for(int o:G.R[a]) r.push_back(o<0?o:sum(o,b)); for(int o:G.R[b]) r.push_back(o<0?o:sum(a,o));
      G.L[id]=l; G.R[id]=r; return id; };
    vector<int> ctx; for(int h:broot) ctx.push_back(h);
    for(size_t i=0;i<broot.size();i++) for(size_t j=i;j<broot.size();j++) ctx.push_back(sum(broot[i],broot[j]));
    vector<int> Aref; for(int i=0;i<NBat;i++) Aref.push_back(i);
    Solve s1; s1.run(A,Bx); Solve s2; s2.run(Aref,Bx);
    for(size_t i=0;i<roots.size();i++){ int mm=0; for(int c:ctx) for(int m=0;m<2;m++) if(s1.get(roots[i],c,m)!=s2.get(refnode,c,m)) mm++;
      printf("PAIRS K%s k%s vs %s: contexts %zu, outcome mismatches %d\n", sqs(rk[i].first).c_str(), sqs(rk[i].second).c_str(), refn.c_str(), ctx.size(), mm); }
  }
  printf("# classes:"); for(auto&c:cls) printf(" %s=%d",c.first.c_str(),c.second); printf("\n# distinct unnamed sigs %zu\n", unsig.size());
  if(getenv("RK_NAMED")) for(size_t i=0;i<roots.size();i++){ string z; for(int k:broot){ z+=s.get(roots[i],k,0); z+=s.get(roots[i],k,1);} for(size_t h=0;h<refsig.size();h++) if(refsig[h]==z && (bname[h]=="over"||bname[h]=="under"||bname[h]=="+1"||bname[h]=="-1"||bname[h]=="*"||bname[h]=="{1|0}"||bname[h]=="{0|-1}")) printf("  %s K%s k%s\n",bname[h].c_str(),sqs(rk[i].first).c_str(),sqs(rk[i].second).c_str()); }
}
