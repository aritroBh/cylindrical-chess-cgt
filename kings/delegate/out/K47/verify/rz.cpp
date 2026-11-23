// K47 referee: own solver for r(Z + T), Z = the P game of a K+P group on cyl:Wx6 (Definition 1.3 sum, LOOPY 1.2/1.5),
// T = a small D-game read from a test file. Written from kings/SPEC.md and LOOPY Definitions 1.2, 1.3, 1.5 only.
// Component rules: P moves (SPEC.md), a promotion is a terminal win for the promoter (ends the whole play), a side in
// check may not move in T, a move in T clears the e.p. right, no move at all: loses (N) or, if not in check, draws (C).
// Usage: rz W H roots.txt tests.txt N|C [pv]
// roots.txt: lines "<pieces>" (no side, no ep). tests.txt: lines "name | n | 0: L=.. R=.. ; 1: ..." (node 0 = start).
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <deque>
using namespace std;
typedef uint64_t u64;
static int W, H, NS;
struct Pos { u64 wp, bp; int wk, bk, ep; }; // ep: target square or -1
static inline int F(int s){return s%W;} static inline int R(int s){return s/W;}
static inline int sq(int f,int r){ f=((f%W)+W)%W; return r*W+f; }
static inline bool adjk(int a,int b){ int df=abs(F(a)-F(b)); df=min(df,W-df); return df<=1 && abs(R(a)-R(b))<=1 && a!=b; }
// is square t attacked by side c's pawns/king (c=0 white)
static bool attacked(const Pos&p,int t,int c){
  int f=F(t), r=R(t);
  if(c==0){ if(r>=1){ if(p.wp>>sq(f-1,r-1)&1) return true; if(p.wp>>sq(f+1,r-1)&1) return true; } return adjk(p.wk,t); }
  else { if(r<=H-2){ if(p.bp>>sq(f-1,r+1)&1) return true; if(p.bp>>sq(f+1,r+1)&1) return true; } return adjk(p.bk,t); }
}
static bool inCheck(const Pos&p,int c){ return attacked(p, c==0?p.wk:p.bk, 1-c); }
// normalise ep: keep only if a capture by the side that may capture is pseudo-possible
static void normEp(Pos&p){
  if(p.ep<0) return; int f=F(p.ep), r=R(p.ep);
  // target rank r: white double step skips r=1 -> black captures from r+1 (black pawns at (f+-1, r+1)); black skips H-3 -> white from r-1
  bool ok=false;
  // white double step 2->4 skips rank index 2, captured by a black pawn on (f+-1, 3); black 5->3 skips H-3, captured from (f+-1, H-4)
  if(r==2 && r!=H-3){ if((p.bp>>sq(f-1,3)&1)||(p.bp>>sq(f+1,3)&1)) ok=true; }
  else if(r==H-3 && r!=2){ if((p.wp>>sq(f-1,H-4)&1)||(p.wp>>sq(f+1,H-4)&1)) ok=true; }
  else ok=true; // ambiguous heights: keep the flag
  if(!ok) p.ep=-1;
}
struct Mv { Pos to; bool promo; };
static void gen(const Pos&p,int c,vector<Mv>&out){
  out.clear();
  u64 occ=p.wp|p.bp|(1ULL<<p.wk)|(1ULL<<p.bk);
  u64 own = c==0?p.wp:p.bp, opp = c==0?p.bp:p.wp;
  int k = c==0?p.wk:p.bk, ok = c==0?p.bk:p.wk;
  auto push=[&](Pos q,bool promo){ q.ep = promo? -1 : q.ep; if(inCheck(q,c)) return; if(!promo) normEp(q); out.push_back({q,promo}); };
  // king
  for(int df=-1;df<=1;df++) for(int dr=-1;dr<=1;dr++){ if(!df&&!dr) continue; int r=R(k)+dr; if(r<0||r>=H) continue; int t=sq(F(k)+df,r);
    if(own>>t&1) continue; if(adjk(t,ok)) continue; Pos q=p; q.ep=-1; if(c==0){q.wk=t; q.bp&=~(1ULL<<t);} else {q.bk=t; q.wp&=~(1ULL<<t);} push(q,false); }
  int dir = c==0?1:-1, last = c==0?H-1:0, start = c==0?1:H-2;
  for(int s=0;s<NS;s++) if(own>>s&1){ int f=F(s), r=R(s); int r1=r+dir; if(r1<0||r1>=H) continue;
    int t=sq(f,r1);
    if(!(occ>>t&1)){ Pos q=p; q.ep=-1; if(c==0){q.wp&=~(1ULL<<s); if(r1!=last) q.wp|=1ULL<<t;} else {q.bp&=~(1ULL<<s); if(r1!=last) q.bp|=1ULL<<t;} push(q,r1==last);
      if(r==start){ int r2=r+2*dir; if(r2>=0&&r2<H){ int t2=sq(f,r2); if(!(occ>>t2&1)){ Pos q2=p; if(c==0){q2.wp&=~(1ULL<<s); if(r2!=last) q2.wp|=1ULL<<t2;} else {q2.bp&=~(1ULL<<s); if(r2!=last) q2.bp|=1ULL<<t2;} q2.ep = (r2==last)? -1 : t; push(q2, r2==last);} } }
    }
    for(int d=-1;d<=1;d+=2){ int tc=sq(f+d,r1);
      if(opp>>tc&1){ Pos q=p; q.ep=-1; if(c==0){q.wp&=~(1ULL<<s); q.bp&=~(1ULL<<tc); if(r1!=last) q.wp|=1ULL<<tc;} else {q.bp&=~(1ULL<<s); q.wp&=~(1ULL<<tc); if(r1!=last) q.bp|=1ULL<<tc;} push(q,r1==last); }
      else if(p.ep==tc){ // e.p.: the double-stepped pawn is behind the target from the capturer's view
        int vic = sq(F(tc), R(tc)-dir); if(opp>>vic&1){ Pos q=p; q.ep=-1; if(c==0){q.wp&=~(1ULL<<s); q.bp&=~(1ULL<<vic); q.wp|=1ULL<<tc;} else {q.bp&=~(1ULL<<s); q.wp&=~(1ULL<<vic); q.bp|=1ULL<<tc;} push(q,false);} }
    }
  }
}
// hash table
static u64 K1(const Pos&p){ return p.wp | ((u64)p.wk<<48) | ((u64)(p.ep<0?63:p.ep)<<54); }
static u64 K2(const Pos&p){ return p.bp | ((u64)p.bk<<48); }
static size_t HS; static u64 *hk1,*hk2; static int32_t *hid;
static vector<Pos> nodes;
static int lookup(const Pos&p,bool add){ u64 a=K1(p), b=K2(p); size_t h=(a*0x9E3779B97F4A7C15ULL ^ (b+0x632BE59BD9B4E019ULL)*0xC2B2AE3D27D4EB4FULL); h^=h>>29; h&=HS-1;
  while(hid[h]>=0){ if(hk1[h]==a&&hk2[h]==b) return hid[h]; h=(h+1)&(HS-1);} if(!add) return -1; hk1[h]=a; hk2[h]=b; hid[h]=nodes.size(); nodes.push_back(p); return hid[h]; }
static int fidx(const char*s){ return s[0]-'a'; }
static bool parse(const char*line,Pos&p){ p.wp=p.bp=0; p.wk=p.bk=-1; p.ep=-1; char buf[64]; const char*c=line; int n;
  while(sscanf(c,"%63s%n",buf,&n)==1){ c+=n; if(strlen(buf)<3) continue; int s=sq(fidx(buf+1),atoi(buf+2)-1);
    switch(buf[0]){case 'K':p.wk=s;break;case 'k':p.bk=s;break;case 'P':p.wp|=1ULL<<s;break;case 'p':p.bp|=1ULL<<s;break;default:return false;} }
  return p.wk>=0&&p.bk>=0; }
static string str(const Pos&p){ string o; char b[8]; auto nm=[&](char c,int s){ snprintf(b,8,"%c%c%d ",c,'a'+F(s),R(s)+1); o+=b; };
  nm('K',p.wk); nm('k',p.bk); for(int s=0;s<NS;s++) if(p.wp>>s&1) nm('P',s); for(int s=0;s<NS;s++) if(p.bp>>s&1) nm('p',s); if(p.ep>=0){ snprintf(b,8,"ep=%c%d",'a'+F(p.ep),R(p.ep)+1); o+=b;} return o; }
// Z graph (CSR)
static vector<int64_t> off[2]; static vector<int32_t> adj[2]; static vector<int64_t> roff[2]; static vector<int32_t> radj[2];
static vector<uint8_t> promo[2], chk[2]; static vector<int32_t> clr; static vector<int64_t> evoff; static vector<int32_t> evadj;
struct TG { string name; int n; vector<vector<int>> L,R; };
static vector<TG> readTests(const char*fn){ vector<TG> v; FILE*f=fopen(fn,"r"); char line[1<<16];
  while(fgets(line,sizeof line,f)){ if(line[0]=='#'||line[0]=='\n') continue; TG g; char*p=strtok(line,"|"); string nm=p; while(!nm.empty()&&nm.back()==' ') nm.pop_back(); g.name=nm;
    g.n=atoi(strtok(NULL,"|")); g.L.assign(g.n,{}); g.R.assign(g.n,{}); char*rest=strtok(NULL,"\n");
    // parse "i: L=a,b R=c ; ..."
    string s=rest; size_t pos=0; while(pos<s.size()){ size_t e=s.find(';',pos); if(e==string::npos) e=s.size(); string part=s.substr(pos,e-pos); pos=e+1;
      int i; char Ls[4096]="",Rs[4096]=""; const char*q=part.c_str(); while(*q==' ') q++; i=atoi(q); const char*l=strstr(q,"L="), *r=strstr(q,"R=");
      auto rd=[&](const char*x,vector<int>&o){ x+=2; while(*x&&*x!=' '&&*x!='\n'){ if(*x>='0'&&*x<='9'){ o.push_back(atoi(x)); while(*x>='0'&&*x<='9') x++; } else x++; } };
      rd(l,g.L[i]); rd(r,g.R[i]); (void)Ls;(void)Rs; }
    v.push_back(g);} fclose(f); return v; }
int main(int argc,char**argv){
  W=atoi(argv[1]); H=atoi(argv[2]); NS=W*H; const char*rootsf=argv[3], *testsf=argv[4]; bool conv_C = argv[5][0]=='C'; bool pv = argc>6;
  HS=1ULL<<24; hk1=(u64*)malloc(HS*8); hk2=(u64*)malloc(HS*8); hid=(int32_t*)malloc(HS*4); memset(hid,-1,HS*4);
  vector<int> roots; vector<string> rootnames; { FILE*f=fopen(rootsf,"r"); char line[512]; while(fgets(line,sizeof line,f)){ if(line[0]=='#'||line[0]=='\n') continue; Pos p; line[strcspn(line,"\n")]=0; if(!parse(line,p)){fprintf(stderr,"bad root %s\n",line); return 1;} roots.push_back(lookup(p,true)); rootnames.push_back(line);} fclose(f);}
  // BFS with forward lists
  vector<vector<int32_t>> tmp; // too big as vector of vectors; build CSR incrementally in node order (BFS order = id order)
  for(int c=0;c<2;c++){ off[c].push_back(0); }
  vector<Mv> mv;
  for(size_t i=0;i<nodes.size();i++){
    Pos p=nodes[i];
    for(int c=0;c<2;c++){ gen(p,c,mv); bool pr=false; for(auto&m:mv){ if(m.promo){pr=true; continue;} adj[c].push_back(lookup(m.to,true)); }
      off[c].push_back(adj[c].size()); promo[c].push_back(pr); chk[c].push_back(inCheck(p,c)); }
    Pos q=p; q.ep=-1; clr.push_back(lookup(q,true));
  }
  size_t N=nodes.size(); fprintf(stderr,"nodes %zu, white moves %zu, black moves %zu\n",N,adj[0].size(),adj[1].size());
  for(int c=0;c<2;c++){ roff[c].assign(N+1,0); for(auto x:adj[c]) roff[c][x+1]++; for(size_t i=0;i<N;i++) roff[c][i+1]+=roff[c][i]; radj[c].resize(adj[c].size()); vector<int64_t> pos(roff[c].begin(),roff[c].end()-1);
    for(size_t i=0;i<N;i++) for(int64_t e=off[c][i];e<off[c][i+1];e++) radj[c][pos[adj[c][e]]++]=i; }
  evoff.assign(N+1,0); for(size_t i=0;i<N;i++) if(clr[i]!=(int)i) evoff[clr[i]+1]++; for(size_t i=0;i<N;i++) evoff[i+1]+=evoff[i]; evadj.resize(evoff[N]); { vector<int64_t> pos(evoff.begin(),evoff.end()-1); for(size_t i=0;i<N;i++) if(clr[i]!=(int)i) evadj[pos[clr[i]]++]=i; }
  auto tests=readTests(testsf);
  for(auto&T:tests){
    int nT=T.n; size_t NSt=N*nT*2; vector<uint8_t> val(NSt,0), cnt(NSt,0); vector<uint16_t> dep(pv?NSt:0,0);
    vector<vector<int>> rT[2]; rT[0].assign(nT,{}); rT[1].assign(nT,{}); for(int t=0;t<nT;t++){ for(int x:T.L[t]) rT[0][x].push_back(t); for(int x:T.R[t]) rT[1][x].push_back(t); }
    deque<size_t> Q; auto ST=[&](size_t z,int t,int s){ return (z*nT+t)*2+s; };
    for(size_t z=0;z<N;z++) for(int t=0;t<nT;t++) for(int s=0;s<2;s++){ size_t i=ST(z,t,s);
      if(promo[s][z]){ val[i]= s==0?1:2; Q.push_back(i); if(pv) dep[i]=1; continue; }
      int d=off[s][z+1]-off[s][z] + (chk[s][z]?0:(s==0?T.L[t].size():T.R[t].size())); cnt[i]=d;
      if(d==0){ if(conv_C && !chk[s][z]) continue; val[i]= s==0?2:1; Q.push_back(i); } }
    while(!Q.empty()){ size_t i=Q.front(); Q.pop_front(); int s=i&1; size_t zt=i>>1; int t=zt%nT; size_t z=zt/nT; int v=val[i]; int ps=1-s; int pwin = ps==0?1:2;
      auto touch=[&](size_t j){ if(val[j]) return; if(v==pwin){ val[j]=pwin; if(pv) dep[j]=dep[i]+1; Q.push_back(j);} else { if(--cnt[j]==0){ val[j]= pwin==1?2:1; if(pv) dep[j]=dep[i]+1; Q.push_back(j);} } };
      for(int64_t e=roff[ps][z];e<roff[ps][z+1];e++) touch(ST(radj[ps][e],t,ps));
      if(clr[z]==(int)z){ auto doz=[&](size_t z2){ if(chk[ps][z2]) return; for(int t2: rT[ps][t]) touch(ST(z2,t2,ps)); }; doz(z); for(int64_t e=evoff[z];e<evoff[z+1];e++) doz(evadj[e]); }
    }
    auto ch=[&](int v){ return v==1?'W':v==2?'L':'D'; };
    printf("%s",T.name.c_str()); for(size_t r=0;r<roots.size();r++) printf(" | %c%c", ch(val[ST(roots[r],0,0)]), ch(val[ST(roots[r],0,1)])); printf("\n"); fflush(stdout);
    if(pv){ // per root, Black to move and White to move: list each move's value; then a principal line from root A, Black to move
      for(size_t r=0;r<roots.size();r++) for(int s=0;s<2;s++){ size_t z=roots[r]; printf("  root %zu %s to move: %c d%d\n",r,s?"Black":"White",ch(val[ST(z,0,s)]),dep.size()?dep[ST(z,0,s)]:0);
        for(int64_t e=off[s][z];e<off[s][z+1];e++){ size_t z2=adj[s][e]; printf("    Z-> %s : %c d%d\n",str(nodes[z2]).c_str(),ch(val[ST(z2,0,1-s)]),dep[ST(z2,0,1-s)]); }
        if(!chk[s][z]) for(int t2:(s==0?T.L[0]:T.R[0])) printf("    T-> %d : %c d%d\n",t2,ch(val[ST(clr[z],t2,1-s)]),dep[ST(clr[z],t2,1-s)]); }
      // principal variation from root 0, Black to move (and root 0 White to move)
      for(int s0=0;s0<2;s0++){ size_t z=roots[0]; int t=0, s=s0; printf("  PV root0 %s to move:",s?"b":"w");
        for(int ply=0;ply<80;ply++){ size_t i=ST(z,t,s); int v=val[i]; if(!v){printf(" (draw)");break;} bool mw = (v==1&&s==0)||(v==2&&s==1);
          if(promo[s][z] && mw){ printf(" [promotes]"); break; }
          long bz=-1; int bt=-1; int bd= mw?1<<30:-1;
          for(int64_t e=off[s][z];e<off[s][z+1];e++){ size_t z2=adj[s][e]; size_t j=ST(z2,t,1-s); if(val[j]!=v) { if(mw) continue; } int d=dep[j]; if(mw? (val[j]==v&&d<bd):(d>bd)){bd=d;bz=z2;bt=t;} }
          if(!chk[s][z]) for(int t2:(s==0?T.L[t]:T.R[t])){ size_t j=ST(clr[z],t2,1-s); int d=dep[j]; if(mw? (val[j]==v&&d<bd):(d>bd)){bd=d;bz=clr[z];bt=t2;} }
          if(bz<0){ printf(" [%s has no move]", s?"Black":"White"); break; }
          if(bt!=t) printf(" %s:T%d->%d", s?"b":"w", t, bt); else printf(" %s:%s", s?"b":"w", str(nodes[bz]).c_str()); printf(";");
          z=bz; t=bt; s=1-s; }
        printf("\n"); }
    }
  }
  return 0;
}
