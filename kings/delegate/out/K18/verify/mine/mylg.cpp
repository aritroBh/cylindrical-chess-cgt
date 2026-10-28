// mylg.cpp -- referee's own solver of the local game of LOOPY Definition 2.6 (s = White, s-bar = Black).
// Written from Definition 2.6 and the text of the K18 claims only (did not read K18/scripts/lg.cpp except the passer rule
// and the output format of --search, which are needed to compare line by line).
// Layered by pawn configuration (pawn moves are irreversible); inside a configuration, rounds t = 1,2,... compute
//   VB[b][B] = least t such that s-bar (to move) wins by its t-th move,   VS[b][S] = least T such that s-bar wins within T,
// b = number of passes left for s (0..KM) or INF (index KM+1).
// usage: mylg --board cyl:8x6 --fz 3 --maxw 2 --maxb 2 --kmax 0 --queen 0|1 --search | --query < positions
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <algorithm>
#include <map>
using namespace std;
typedef uint64_t u64;
static int W=8,H=6,NF=3,KM=0,QUEEN=1,MAXW=2,MAXB=2,WRAP=1; static FILE*dumpf=nullptr; struct ScanE{int cid,e,wk,bk;}; static vector<ScanE> scanv; static u64 FORBID=0;
static int N;
static const uint8_t INF=255;
static inline u64 bit(int s){return 1ULL<<s;}
static int sqf(int s){return s%W;} static int sqr(int s){return s/W;}
static int mk(int f,int r){ if(r<0||r>=H) return -1; if(WRAP) f=((f%W)+W)%W; else if(f<0||f>=W) return -1; return r*W+f; }
static u64 adjM[64]; static vector<int> nbr[64];
static u64 wAttFrom[64], bAttFrom[64]; // squares from which a white/black pawn attacks sq
static bool adjK(int a,int b){ return (adjM[a]>>b)&1; }
struct Pos { u64 wp,bp; int wk,bk; int ep; }; // ep = target square or -1
struct Mv { Pos to; bool promo; int from,dst; bool king; };
static inline bool attackedByW(int sq,u64 wp){ return (wAttFrom[sq]&wp)!=0; }
static inline bool attackedByB(int sq,u64 bp){ return (bAttFrom[sq]&bp)!=0; }
// generate legal moves of side c (0 white, 1 black). fzOnly: black king confined to F_Z squares
static u64 FZMASK=0;
static void gen(int c,const Pos&p,vector<Mv>&out,bool confine){
  out.clear();
  u64 own = c==0?p.wp:p.bp, opp = c==0?p.bp:p.wp;
  int ok = c==0?p.wk:p.bk, ek = c==0?p.bk:p.wk;
  // king moves
  for(int d: nbr[ok]){
    if(((own>>d)&1)) continue;
    if(d==ek||adjK(d,ek)) continue;
    u64 nopp = opp & ~bit(d);
    bool att = c==0 ? attackedByB(d,nopp) : attackedByW(d,nopp);
    if(att) continue;
    if(c==1 && confine && !((FZMASK>>d)&1)) continue;
    Mv m; m.to=p; m.promo=false; m.from=ok; m.dst=d; m.king=true; m.to.ep=-1;
    if(c==0){m.to.wk=d;m.to.bp=nopp;} else {m.to.bk=d;m.to.wp=nopp;}
    out.push_back(m);
  }
  u64 occ = p.wp|p.bp|bit(p.wk)|bit(p.bk);
  int dir = c==0?1:-1; int last = c==0?H-1:0; int start = c==0?1:H-2;
  for(u64 x=own;x;x&=x-1){
    int s=__builtin_ctzll(x); int f=sqf(s), r=sqr(s);
    int t1=mk(f,r+dir);
    auto okAfter=[&](u64 nown,u64 nopp)->bool{
      return c==0 ? !attackedByB(p.wk,nopp) : !attackedByW(p.bk,nopp);
    };
    if(t1>=0 && !((occ>>t1)&1)){
      bool promo = sqr(t1)==last;
      u64 nown = own & ~bit(s); if(!promo) nown|=bit(t1);
      if(okAfter(nown,opp)){
        Mv m; m.to=p; m.promo=promo; m.from=s; m.dst=t1; m.king=false; m.to.ep=-1;
        if(c==0) m.to.wp=nown; else m.to.bp=nown;
        out.push_back(m);
      }
      if(r==start){
        int t2=mk(f,r+2*dir);
        if(t2>=0 && !((occ>>t2)&1)){
          u64 n2=(own&~bit(s))|bit(t2);
          if(okAfter(n2,opp)){
            Mv m; m.to=p; m.promo=false; m.from=s; m.dst=t2; m.king=false; m.to.ep=-1;
            if(c==0) m.to.wp=n2; else m.to.bp=n2;
            // e.p. right if an enemy pawn stands beside the destination
            bool can=false;
            for(int df=-1;df<=1;df+=2){ int q=mk(f+df,r+2*dir); if(q>=0 && ((opp>>q)&1)) can=true; }
            if(can) m.to.ep=t1;
            out.push_back(m);
          }
        }
      }
    }
    for(int df=-1;df<=1;df+=2){
      int t=mk(f+df,r+dir); if(t<0) continue;
      bool epcap=false; u64 nopp=opp;
      if((opp>>t)&1){ nopp&=~bit(t); }
      else if(p.ep==t && !((occ>>t)&1)){
        int vs=mk(f+df,r); // square of the pawn that double-stepped
        if(vs>=0 && ((opp>>vs)&1)){ nopp&=~bit(vs); epcap=true; }
        else continue;
      } else continue;
      (void)epcap;
      bool promo=sqr(t)==last;
      u64 nown=own&~bit(s); if(!promo) nown|=bit(t);
      if(!okAfter(nown,nopp)) continue;
      Mv m; m.to=p; m.promo=promo; m.from=s; m.dst=t; m.king=false; m.to.ep=-1;
      if(c==0){m.to.wp=nown;m.to.bp=nopp;} else {m.to.bp=nown;m.to.wp=nopp;}
      out.push_back(m);
    }
  }
}
// promotion square by black pawn at s->dst: queen safe iff white king cannot capture it
static bool queenSafe(const Pos&before,const Mv&m){ // m = black promotion move
  int d=m.dst; u64 nbp=m.to.bp; // pawn already removed
  if(!adjK(before.wk,d)) return true;      // white king not adjacent: cannot capture
  if(adjK(before.bk,d)) return true;       // protected by the black king: capture illegal
  if(attackedByB(d,nbp)) return true;      // protected by a black pawn: capture illegal
  return false;                            // white king can capture
}
// ---------- pawn configurations ----------
static int NSLOT; static vector<int> slotSq;
static vector<unsigned> wmasks,bmasks; static vector<int> wId,bId; // mask -> index or -1
static vector<u64> maskGlob;
static int NB;
struct Cfg{ unsigned wm,bm; };
static vector<Cfg> cfgs; static vector<int> cfgOfPair; // pair index wi*NB+bi -> cid or -1
static int ncfg;
static int slotOf[64];
static bool toCfg(u64 wp,u64 bp,int&cid){
  unsigned wm=0,bm=0;
  for(u64 x=wp;x;x&=x-1){int s=__builtin_ctzll(x); if(slotOf[s]<0) return false; wm|=1u<<slotOf[s];}
  for(u64 x=bp;x;x&=x-1){int s=__builtin_ctzll(x); if(slotOf[s]<0) return false; bm|=1u<<slotOf[s];}
  if(wId[wm]<0||bId[bm]<0) return false;
  cid=cfgOfPair[wId[wm]*NB+bId[bm]]; return cid>=0;
}
// ---------- tables ----------
static int NBUD; // KM+2
static int NFZSQ; static vector<int> fzsq; static int fzIdx[64];
static int EPN; // 1+NF*2 : ep index: 0 none; 1.. target squares (index by file*2+colourRank)
static inline int epIndex(int ep){ if(ep<0) return 0; int f=sqf(ep); int r=sqr(ep); int col = (r==2)?0:1; // r==2: target of a white double step
  return 1+f*2+col; }
static vector<int> epSqOf; // index -> square
static vector<uint8_t> VS,VB; // index ((((cid*NBUD+b)*EPN+e)*N+wk)*NFZSQ+bkIdx)
static inline size_t ix(int cid,int b,int e,int wk,int bk){ return ((((size_t)cid*NBUD+b)*EPN+e)*N+wk)*NFZSQ+fzIdx[bk]; }
// ep consistency: for S states (white to move) ep must be a black double step target (rank H-3); for B states white's (rank 2)
static int potOf(const Cfg&c){ int pot=0,cnt=0; for(int i=0;i<NSLOT;i++){ int r=sqr(slotSq[i]);
   if((c.wm>>i)&1){pot+=r;cnt++;} if((c.bm>>i)&1){pot+=H-1-r;cnt++;} } return pot+100*(MAXW+MAXB-cnt); }
static bool validPos(const Pos&p,int stm){
  if(p.wk==p.bk||adjK(p.wk,p.bk)) return false;
  u64 occ=p.wp|p.bp; if(((occ>>p.wk)&1)||((occ>>p.bk)&1)) return false;
  if(p.wp&p.bp) return false;
  return true;
}
static string posstr(const Pos&p,int stm);
struct Succ{ int cid; int e; int wk,bk; int kind; }; // kind 0 normal, 1 win-immediate (s-bar promotion safe or mate), 2 s promotion (S side)
static void solveConfig(int cid){
  Cfg cf=cfgs[cid]; u64 wp=0,bp=0;
  for(int i=0;i<NSLOT;i++){ if((cf.wm>>i)&1) wp|=bit(slotSq[i]); if((cf.bm>>i)&1) bp|=bit(slotSq[i]); }
  // successor lists for all states (stm,e,wk,bk)
  // state key: ((stm*EPN+e)*N+wk)*NFZSQ+bkIdx
  size_t NS=(size_t)2*EPN*N*NFZSQ;
  vector<vector<Succ>> succ(NS); vector<char> valid(NS,0), inCheckS(NS,0), hasMove(NS,0);
  vector<Mv> mv;
  for(int stm=0;stm<2;stm++) for(int e=0;e<EPN;e++){
    int ep = e==0?-1:-2;
    if(e>0){ // target square
      int f=(e-1)/2, col=(e-1)%2; ep = mk(f, col==0?2:H-3);
      // stm white to move: ep must be black's (col==1); stm black: white's (col==0)
      if((stm==0)!=(col==1)) continue;
      // there must be the double-stepped pawn
      int pawnsq = mk(f, col==0?3:H-4);
      if(!(((col==0?wp:bp)>>pawnsq)&1)) continue;
    }
    for(int wk=0;wk<N;wk++) for(int bk: fzsq){
      Pos p{wp,bp,wk,bk,ep};
      if(!validPos(p,stm)) continue;
      // side not to move must not be in check
      if(stm==0 && attackedByW(bk,wp)) continue;
      if(stm==1 && attackedByB(wk,bp)) continue;
      size_t key=(((size_t)stm*EPN+e)*N+wk)*NFZSQ+fzIdx[bk];
      valid[key]=1;
      gen(stm,p,mv,stm==1);
      vector<Succ>&L=succ[key];
      hasMove[key]=!mv.empty();
      inCheckS[key]= stm==0 ? attackedByB(wk,bp) : attackedByW(bk,wp);
      for(auto&m:mv){
        Succ s;
        if(m.promo){
          if(stm==0){ s.kind=2; s.cid=cid; s.e=0; s.wk=0; s.bk=bk; L.push_back(s); continue; }
          // black promotion: immediate win if safe (queen clause) -- recorded with kind 1 (safe) or 3 (unsafe/failure = no win)
          bool safe = QUEEN? queenSafe(p,m) : true;
          s.kind = safe?1:3; s.cid=cid; s.e=0; s.wk=0; s.bk=bk; L.push_back(s); continue;
        }
        if(stm==0 && m.king && ((FORBID>>m.dst)&1)){ s.kind=2; s.cid=cid; s.e=0; s.wk=0; s.bk=bk; L.push_back(s); continue; }
        int ncid; if(!toCfg(m.to.wp,m.to.bp,ncid)){ fprintf(stderr,"config escape\n"); exit(3);}
        s.cid=ncid; s.e=epIndex(m.to.ep); s.wk=m.to.wk; s.bk=m.to.bk; s.kind=0;
        if(!m.king && stm==1 && false){}
        L.push_back(s);
      }
    }
  }
  // helper: is state (stm=0,e,wk,bk) with white in check and no moves (mate)?
  auto stateIdx=[&](int stm,int e,int wk,int bk){ return (((size_t)stm*EPN+e)*N+wk)*NFZSQ+fzIdx[bk]; };
  auto getVS=[&](int ncid,int b,int e,int wk,int bk)->uint8_t{ return VS[ix(ncid,b,e,wk,bk)]; };
  auto getVB=[&](int ncid,int b,int e,int wk,int bk)->uint8_t{ return VB[ix(ncid,b,e,wk,bk)]; };
  // Evaluate S at budget b given current tables: returns INF or max VB of children (0 if mate)
  auto evalS=[&](int e,int wk,int bk,int b)->uint8_t{
    size_t key=stateIdx(0,e,wk,bk); if(!valid[key]) return INF;
    const vector<Succ>&L=succ[key];
    if(L.empty()){ // no legal move: mate (in check) or stalemate
      if(inCheckS[key]) return 0;
      // stalemate: s may pass if it has passes
      if(b==0) return INF;
      int nb = (b==KM+1)?KM+1:b-1;
      uint8_t v=getVB(cid,nb,0,wk,bk); return v;
    }
    int mx=0;
    for(const Succ&s:L){
      if(s.kind==2) return INF;
      uint8_t v=getVB(s.cid,b,s.e,s.wk,s.bk); if(v==INF) return INF; if(v>mx) mx=v;
    }
    if(!inCheckS[key] && b>0){
      int nb=(b==KM+1)?KM+1:b-1; uint8_t v=getVB(cid,nb,0,wk,bk); if(v==INF) return INF; if(v>mx) mx=v;
    }
    return (uint8_t)mx;
  };
  auto evalB=[&](int e,int wk,int bk,int b)->uint8_t{
    size_t key=stateIdx(1,e,wk,bk); if(!valid[key]) return INF;
    const vector<Succ>&L=succ[key]; int best=INF;
    for(const Succ&s:L){
      if(s.kind==3) continue;
      if(s.kind==1){ best=1; break; }
      uint8_t v=getVS(s.cid,b,s.e,s.wk,s.bk); if(v==INF) continue;
      // a move to a mate position has v==0 -> value 1
      if(1+v<best) best=1+v;
    }
    return (uint8_t)best;
  };
  // none layer: rounds. Initially all INF (tables are pre-filled with INF).
  for(int b=0;b<NBUD;b++){
    // order of budgets: 0..KM then INF; S(b) depends on B(b-1) (final) and same-b B/S
    // mate states get VS=0 immediately; others by rounds
    bool changed=true,pending=true; int round=0;
    for(int wk=0;wk<N;wk++) for(int bk:fzsq){ size_t key=stateIdx(0,0,wk,bk); if(valid[key]&&succ[key].empty()&&inCheckS[key]) VS[ix(cid,b,0,wk,bk)]=0; }
    // a state is assigned in round t only if its value (computed from values already assigned) is <= t; this keeps the
    // invariant "value assigned in the round equal to the value", which the min/max recursions need.
    while((changed||pending) && round<250){
      changed=false; pending=false; round++;
      vector<pair<size_t,uint8_t>> upd;
      for(int wk=0;wk<N;wk++) for(int bk:fzsq){
        size_t i2=ix(cid,b,0,wk,bk); if(VB[i2]!=INF) continue;
        uint8_t v=evalB(0,wk,bk,b); if(v!=INF){ if(v<=round) upd.push_back({i2,v}); else pending=true; }
      }
      for(auto&u:upd){ VB[u.first]=u.second; changed=true; }
      upd.clear();
      for(int wk=0;wk<N;wk++) for(int bk:fzsq){
        size_t i2=ix(cid,b,0,wk,bk); if(VS[i2]!=INF) continue;
        uint8_t v=evalS(0,wk,bk,b); if(v!=INF){ if(v<=round) upd.push_back({i2,v}); else pending=true; }
      }
      for(auto&u:upd){ VS[u.first]=u.second; changed=true; }
    }
  }
  if(getenv("SCANEP")){ // diagnostic: S states with an e.p. right, finite plain value, whose only legal moves are e.p. captures
    for(int e=1;e<EPN;e++) for(int wk=0;wk<N;wk++) for(int bk:fzsq){
      size_t key=stateIdx(0,e,wk,bk); if(!valid[key]||succ[key].empty()) continue;
      int f=(e-1)/2,col=(e-1)%2; if(col!=1) continue;
      Pos p{wp,bp,wk,bk,mk(f,H-3)}; Pos q=p; q.ep=-1; vector<Mv> m2; gen(0,q,m2,false);
      if(m2.empty() && !inCheckS[key]) scanv.push_back({cid,e,wk,bk});
    }
  }
  // ep layers: direct evaluation
  for(int b=0;b<NBUD;b++) for(int e=1;e<EPN;e++) for(int wk=0;wk<N;wk++) for(int bk:fzsq){
    if(valid[stateIdx(0,e,wk,bk)]){ uint8_t v=evalS(e,wk,bk,b);
      if(getenv("LAPSE") && v!=INF){ uint8_t v2=VS[ix(cid,b,0,wk,bk)]; if(v2==INF) v=INF; else if(v2>v) v=v2; }
      VS[ix(cid,b,e,wk,bk)]=v; }
    if(valid[stateIdx(1,e,wk,bk)]) VB[ix(cid,b,e,wk,bk)]=evalB(e,wk,bk,b);
  }
}
// ---------- passers (the note's rule: no enemy pawn ahead on the same or an adjacent file) ----------
static bool hasPasser(u64 wp,u64 bp){
  for(u64 x=wp;x;x&=x-1){ int s=__builtin_ctzll(x); int f=sqf(s),r=sqr(s); bool blocked=false;
    for(u64 y=bp;y;y&=y-1){ int t=__builtin_ctzll(y); int g=sqf(t),q=sqr(t); int df=((g-f)%W+W)%W; bool adj=WRAP?(df==0||df==1||df==W-1):(abs(g-f)<=1); if(adj&&q>r) blocked=true; }
    if(!blocked) return true; }
  for(u64 y=bp;y;y&=y-1){ int t=__builtin_ctzll(y); int g=sqf(t),q=sqr(t); bool blocked=false;
    for(u64 x=wp;x;x&=x-1){ int s=__builtin_ctzll(x); int f=sqf(s),r=sqr(s); int df=((g-f)%W+W)%W; bool adj=WRAP?(df==0||df==1||df==W-1):(abs(g-f)<=1); if(adj&&r<q) blocked=true; }
    if(!blocked) return true; }
  return false;
}
static string sqn(int s){ char b[8]; snprintf(b,8,"%c%d",'a'+sqf(s),sqr(s)+1); return b; }
static string posstr(const Pos&p,int stm){
  string s="K"+sqn(p.wk);
  vector<int> a,b; for(u64 x=p.wp;x;x&=x-1) a.push_back(__builtin_ctzll(x)); for(u64 x=p.bp;x;x&=x-1) b.push_back(__builtin_ctzll(x));
  sort(a.begin(),a.end()); sort(b.begin(),b.end());
  for(int x:a) s+=" P"+sqn(x); s+=" k"+sqn(p.bk); for(int x:b) s+=" p"+sqn(x);
  s+= stm?" b":" w"; s+= p.ep>=0? " "+sqn(p.ep):" -"; return s;
}
static bool parsePos(char*line,Pos&p,int&stm){
  p.wp=p.bp=0;p.wk=p.bk=-1;p.ep=-1; vector<string> t; char*sv; for(char*tk=strtok_r(line," \t\r\n",&sv);tk;tk=strtok_r(nullptr," \t\r\n",&sv)) t.push_back(tk);
  if(t.size()<4) return false; string ep=t.back(), sd=t[t.size()-2]; stm= sd=="b";
  if(ep!="-"){ p.ep=mk(ep[0]-'a',atoi(ep.c_str()+1)-1); }
  for(size_t i=0;i+2<t.size();i++){ int s=mk(t[i][1]-'a',atoi(t[i].c_str()+2)-1); char c=t[i][0];
    if(c=='K')p.wk=s; else if(c=='k')p.bk=s; else if(c=='P')p.wp|=bit(s); else p.bp|=bit(s); }
  return p.wk>=0&&p.bk>=0;
}
int main(int argc,char**argv){
  const char*board="cyl:8x6"; int mode=0; int fz0=0;
  for(int i=1;i<argc;i++){
    if(!strcmp(argv[i],"--board")) board=argv[++i];
    else if(!strcmp(argv[i],"--fz")) NF=atoi(argv[++i]);
    else if(!strcmp(argv[i],"--maxw")) MAXW=atoi(argv[++i]);
    else if(!strcmp(argv[i],"--maxb")) MAXB=atoi(argv[++i]);
    else if(!strcmp(argv[i],"--kmax")) KM=atoi(argv[++i]);
    else if(!strcmp(argv[i],"--queen")) QUEEN=atoi(argv[++i]);
    else if(!strcmp(argv[i],"--search")) mode=2;
    else if(!strcmp(argv[i],"--query")) mode=1;
    else if(!strcmp(argv[i],"--fquery")) mode=3;
    else if(!strcmp(argv[i],"--dump")) dumpf=fopen(argv[++i],"w");
  }
  WRAP=!strncmp(board,"cyl",3);
  sscanf(strchr(board,':')+1,"%dx%d",&W,&H); N=W*H; NBUD=KM+2; (void)fz0;
  for(int s=0;s<N;s++){ adjM[s]=0; nbr[s].clear(); wAttFrom[s]=bAttFrom[s]=0; }
  for(int s=0;s<N;s++){ for(int df=-1;df<=1;df++) for(int dr=-1;dr<=1;dr++){ if(!df&&!dr) continue; int t=mk(sqf(s)+df,sqr(s)+dr); if(t>=0 && t!=s){ adjM[s]|=bit(t); nbr[s].push_back(t);} } }
  for(int s=0;s<N;s++){ int f=sqf(s),r=sqr(s);
    for(int df=-1;df<=1;df+=2){ int a=mk(f+df,r-1); if(a>=0) wAttFrom[s]|=bit(a); int b=mk(f+df,r+1); if(b>=0) bAttFrom[s]|=bit(b); } }
  for(int f=0;f<NF;f++) for(int r=0;r<H;r++){ fzIdx[r*W+f]=-1; }
  for(int i=0;i<64;i++){ fzIdx[i]=-1; slotOf[i]=-1; }
  for(int f=0;f<NF;f++) for(int r=0;r<H;r++){ int s=r*W+f; fzIdx[s]=fzsq.size(); fzsq.push_back(s); FZMASK|=bit(s); }
  NFZSQ=fzsq.size();
  for(int f=0;f<NF;f++) for(int r=1;r<=H-2;r++){ slotOf[r*W+f]=slotSq.size(); slotSq.push_back(r*W+f); }
  NSLOT=slotSq.size();
  wId.assign(1u<<NSLOT,-1); bId.assign(1u<<NSLOT,-1);
  for(unsigned m=0;m<(1u<<NSLOT);m++){ int pc=__builtin_popcount(m); if(pc<=MAXW){wId[m]=wmasks.size();wmasks.push_back(m);} if(pc<=MAXB){bId[m]=bmasks.size();bmasks.push_back(m);} }
  NB=bmasks.size(); cfgOfPair.assign(wmasks.size()*NB,-1);
  for(size_t a=0;a<wmasks.size();a++) for(int b=0;b<NB;b++){ if(wmasks[a]&bmasks[b]) continue; cfgOfPair[a*NB+b]=cfgs.size(); cfgs.push_back({wmasks[a],bmasks[b]}); }
  ncfg=cfgs.size(); EPN=1+NF*2;
  size_t tot=(size_t)ncfg*NBUD*EPN*N*NFZSQ;
  fprintf(stderr,"[mylg] %s NF=%d slots=%d configs=%d table=%.1f MB each\n",board,NF,NSLOT,ncfg,tot/1e6);
  VS.assign(tot,INF); VB.assign(tot,INF);
  vector<int> order(ncfg); for(int i=0;i<ncfg;i++) order[i]=i;
  if(mode==3){
    // lines: "<Black-to-move pos> | <forbidden squares of the White king, space separated or empty>" -> min over admissible replies of V (budget 0)
    vector<pair<string,string>> in; char line[600];
    while(fgets(line,sizeof line,stdin)){ line[strcspn(line,"\n")]=0; if(!line[0]||line[0]=='#') continue; string L=line; size_t b=L.find('|'); in.push_back({L.substr(0,b),b==string::npos?"":L.substr(b+1)}); }
    map<string,vector<int>> grp; for(size_t i=0;i<in.size();i++){ string f=in[i].second; // normalise
      vector<string> t; { char*c=strdup(f.c_str()); char*sv; for(char*tk=strtok_r(c," \t",&sv);tk;tk=strtok_r(nullptr," \t",&sv)) t.push_back(tk); free(c);} sort(t.begin(),t.end()); string key; for(auto&x:t) key+=x+" "; grp[key].push_back(i); }
    vector<int> pot(ncfg); for(int i=0;i<ncfg;i++) pot[i]=potOf(cfgs[i]);
    sort(order.begin(),order.end(),[&](int a,int b){return pot[a]>pot[b];});
    vector<string> outl(in.size());
    for(auto&g:grp){
      FORBID=0; { char*c=strdup(g.first.c_str()); char*sv; for(char*tk=strtok_r(c," \t",&sv);tk;tk=strtok_r(nullptr," \t",&sv)){ int s=mk(tk[0]-'a',atoi(tk+1)-1); FORBID|=bit(s);} free(c);}
      fill(VS.begin(),VS.end(),INF); fill(VB.begin(),VB.end(),INF);
      for(int cid:order) solveConfig(cid);
      for(int i:g.second){ char buf[512]; strncpy(buf,in[i].first.c_str(),511); buf[511]=0; Pos p; int stm; if(!parsePos(buf,p,stm)||stm!=1){ outl[i]=in[i].first+" | parse error"; continue; }
        vector<Mv> rm; gen(1,p,rm,true); int best=INF; bool immw=false;
        for(auto&q:rm){ if(q.promo){ bool safe=QUEEN?queenSafe(p,q):true; if(safe) immw=true; continue; }
          if((FORBID>>q.to.wk)&1) continue; // the king is already on a forbidden square
          int cid2; if(!toCfg(q.to.wp,q.to.bp,cid2)) continue; uint8_t v=VS[ix(cid2,0,epIndex(q.to.ep),q.to.wk,q.to.bk)]; if(v<best) best=v; }
        char o[64]; if(immw) snprintf(o,64," | imm"); else if(best==INF) snprintf(o,64," | INF"); else snprintf(o,64," | %d",best);
        outl[i]=in[i].first+o; }
    }
    for(auto&x:outl) printf("%s\n",x.c_str());
    return 0;
  }
  vector<int> pot(ncfg); for(int i=0;i<ncfg;i++) pot[i]=potOf(cfgs[i]);
  sort(order.begin(),order.end(),[&](int a,int b){return pot[a]>pot[b];});
  for(int cid:order) solveConfig(cid);
  fprintf(stderr,"[mylg] solved\n");
  if(getenv("DUMPFIN")){ FILE*f=fopen(getenv("DUMPFIN"),"w");
    for(int cid=0;cid<ncfg;cid++){ Cfg cf=cfgs[cid]; u64 wp=0,bp=0; for(int i=0;i<NSLOT;i++){ if((cf.wm>>i)&1) wp|=bit(slotSq[i]); if((cf.bm>>i)&1) bp|=bit(slotSq[i]); }
      for(int wk=0;wk<N;wk++) for(int bk:fzsq){ Pos p{wp,bp,wk,bk,-1}; if(!validPos(p,0)||attackedByW(bk,wp)) continue; uint8_t v=VS[ix(cid,0,0,wk,bk)]; if(v!=INF) fprintf(f,"%s T=%d\n",posstr(p,0).c_str(),v); } }
    fclose(f); }
  if(getenv("SCANEP")) fprintf(stderr,"[scan] states with only-ep-capture moves: %zu\n",scanv.size());
  for(auto&x:scanv){ if(VS[ix(x.cid,0,x.e,x.wk,x.bk)]!=INF){ Cfg cf=cfgs[x.cid]; Pos p{0,0,x.wk,x.bk,-1}; for(int i=0;i<NSLOT;i++){ if((cf.wm>>i)&1) p.wp|=bit(slotSq[i]); if((cf.bm>>i)&1) p.bp|=bit(slotSq[i]); } int f=(x.e-1)/2; p.ep=mk(f,H-3); printf("EPSTALE T=%d %s\n",VS[ix(x.cid,0,x.e,x.wk,x.bk)],posstr(p,0).c_str()); } }
  auto Vs=[&](const Pos&p,int b)->uint8_t{ int cid; if(!toCfg(p.wp,p.bp,cid)) return 254; return VS[ix(cid,b,epIndex(p.ep),p.wk,p.bk)]; };
  if(mode==1){
    char line[512];
    while(fgets(line,sizeof line,stdin)){
      if(line[0]=='#'||line[0]=='\n'){fputs(line,stdout);continue;}
      line[strcspn(line,"\n")]=0; string orig=line; Pos p; int stm; if(!parsePos(line,p,stm)||stm!=0){ printf("%s | parse error or not s-to-move\n",orig.c_str()); continue; }
      printf("%s |",orig.c_str());
      for(int b=0;b<NBUD;b++){ uint8_t v=Vs(p,b); if(b==KM+1) printf(" inf="); else printf(" k%d=",b); if(v==INF) printf("INF"); else printf("%d",v); }
      printf("\n");
    }
    return 0;
  }
  if(mode==2){
    long nroots=0,candAny=0,candNoEsc=0; vector<Mv> ym,rm;
    for(int cid=0;cid<ncfg;cid++){
      u64 wp=0,bp=0; Cfg cf=cfgs[cid]; for(int i=0;i<NSLOT;i++){ if((cf.wm>>i)&1) wp|=bit(slotSq[i]); if((cf.bm>>i)&1) bp|=bit(slotSq[i]); }
      if(hasPasser(wp,bp)) continue;
      for(int wk: fzsq) for(int bk: fzsq){
        Pos Y{wp,bp,wk,bk,-1};
        if(!validPos(Y,0)) continue; if(attackedByW(bk,wp)) continue;
        gen(0,Y,ym,false); bool canPromo=false; for(auto&m:ym) if(m.promo) canPromo=true; if(canPromo) continue;
        nroots++;
        struct R{ string name; int Tplain,Tpass; bool imm; int Tk[16]; };
        vector<R> res; bool anyOnly=false,esc=false; int nonly=0,nesc=0;
        for(auto&m:ym){
          R r; r.name=(m.king?"K":"")+sqn(m.from)+"-"+sqn(m.dst); r.Tplain=INF; r.Tpass=INF; r.imm=false; for(int k=0;k<16;k++) r.Tk[k]=INF;
          gen(1,m.to,rm,true);
          for(auto&q:rm){
            if(q.promo){ bool safe=QUEEN?queenSafe(m.to,q):true; if(safe) r.imm=true; continue; }
            uint8_t a=Vs(q.to,0), c2=Vs(q.to,KM+1); for(int k=0;k<=KM;k++){ uint8_t x=Vs(q.to,k); if(x<r.Tk[k]) r.Tk[k]=x; }
            if(a<r.Tplain) r.Tplain=a; if(c2<r.Tpass) r.Tpass=c2;
          }
          bool plainP=r.imm||r.Tplain!=INF, passP=r.imm||r.Tpass!=INF;
          if(!plainP&&!passP){esc=true;nesc++;}
          if(plainP&&!passP){anyOnly=true;nonly++;}
          res.push_back(r);
        }
        if(dumpf) for(size_t i=0;i<ym.size();i++){ const R&r=res[i]; fprintf(dumpf,"%s | %s | %d %d %d | %s | %s\n",posstr(ym[i].to,1).c_str(),res[i].name.c_str(),r.Tplain==INF?-1:r.Tplain,r.Tpass==INF?-1:r.Tpass,r.imm?1:0,posstr(Y,0).c_str(),esc?"ESCAPE":"NOESC"); }
        if(!anyOnly) continue;
        candAny++; if(!esc) candNoEsc++;
        printf("%s | %s | only=%d esc=%d | %s |",QUEEN?"Q":"P",posstr(Y,0).c_str(),nonly,nesc,esc?"ESCAPE":"NOESC");
        for(auto&r:res){ bool plainP=r.imm||r.Tplain!=INF,passP=r.imm||r.Tpass!=INF;
          const char*cls=r.imm?"IMM":(plainP&&passP)?"both":plainP?"PLAIN-ONLY":passP?"pass-only":"ESC";
          printf(" [%s %s",r.name.c_str(),cls); if(r.Tplain!=INF) printf(" Tplain=%d",r.Tplain); if(r.Tpass!=INF) printf(" Tpass=%d",r.Tpass); if(KM>0){ printf(" k="); for(int k=0;k<=KM;k++){ if(r.Tk[k]==INF) printf("-"); else printf("%d",r.Tk[k]); if(k<KM) printf(","); } } printf("]"); }
        printf("\n");
      }
    }
    printf("# roots=%ld cand_any=%ld cand_noesc=%ld\n",nroots,candAny,candNoEsc);
  }
  return 0;
}
