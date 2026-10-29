// Referee-2 checker for K32 (LOOPY 4(d)).  Written from the definitions in LOOPY section 3 only
// (did not read K32's stopsA.c / stopsB.c or the first referee's vref.c).
// Game: finite graph, node v has Left options Lm[v] and Right options Rm[v] (bitmasks, self loops allowed), terminal-free.
// "Left wins" = forced win in finitely many moves (least fixed point); player unable to move loses.
// Product graph with a number game N_p (canonical form, p/D, D=2^K, |p/D|<=M): position (v,p,mover); q=p means y_v + N_q.
//   lambda(v) = min C>=0 with Left wins (v, q=C) moving second;  rho(v) = min C>=0 with Right wins (v, q=-C) moving second.
//   D2: RS(v) = sup{x : Left wins y - x second}, LS(v)=sup{x: Left wins y - x first}, x=-q.
//   D1: Siegel recursion, "v equals number x" iff second player wins y - x (both lose moving first).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 8
#define NVMAX 1100
#define PINF  1000000000L
#define NINF (-1000000000L)
#define LINF 99
static int K, D, M, NV, n;
static int nL[NVMAX], nR[NVMAX];
static int invL[NVMAX][16], ciL[NVMAX], invR[NVMAX][16], ciR[NVMAX];
static int Lm[MAXN], Rm[MAXN];
static uint8_t winT[2][MAXN*NVMAX*2];   // winT[0]: Left wins; winT[1]: Right wins
static int cntbuf[MAXN*NVMAX*2];
static int queue_[MAXN*NVMAX*2];

static long fdiv(long a, long b){ long q=a/b; if((a%b!=0)&&((a<0)!=(b<0))) q--; return q; }
static long cdiv(long a, long b){ return -fdiv(-a,b); }

static void setup_grid(int k, int m){
  K=k; D=1<<k; M=m; NV=2*M*D+1;
  for(int i=0;i<NV;i++){ciL[i]=ciR[i]=0;}
  for(int i=0;i<NV;i++){
    int p=i-M*D; nL[i]=nR[i]=-1;
    if(p%D==0){ if(p>0) nL[i]=i-D; else if(p<0) nR[i]=i+D; }
    else { int ap=abs(p); int st=ap&-ap; nL[i]=i-st; nR[i]=i+st; }
  }
  for(int i=0;i<NV;i++){ if(nL[i]>=0){int t=nL[i]; invL[t][ciL[t]++]=i;} if(nR[i]>=0){int t=nR[i]; invR[t][ciR[t]++]=i;} }
}
#define SID(v,i,m) ((((v)*NV)+(i))*2+(m))
static void solve(int sigma){      // sigma=0: Left wins; 1: Right wins
  int S=n*NV*2; uint8_t *W=winT[sigma]; memset(W,0,S);
  int qh=0, qt=0;
  for(int v=0;v<n;v++) for(int i=0;i<NV;i++) for(int m=0;m<2;m++){
    int s=SID(v,i,m);
    int c=__builtin_popcount(m==0?Lm[v]:Rm[v]) + ((m==0?nL[i]:nR[i])>=0);
    cntbuf[s]=c;
    if(m!=sigma && c==0){ W[s]=1; queue_[qt++]=s; }
  }
  while(qh<qt){
    int t=queue_[qh++]; int m=t&1; int vi=t>>1; int v=vi/NV, i=vi%NV; int mm=1-m;
    // predecessors: states (u,i,mm) with v in opts_mm(u); (v,i2,mm) with i in opts_mm(i2)
    for(int u=0;u<n;u++){ int om=(mm==0?Lm[u]:Rm[u]); if(om>>v&1){ int s=SID(u,i,mm);
        if(W[s]) continue;
        if(mm==sigma){ W[s]=1; queue_[qt++]=s; } else { if(--cntbuf[s]==0){ W[s]=1; queue_[qt++]=s; } } } }
    int cnt = mm==0?ciL[i]:ciR[i];
    for(int k=0;k<cnt;k++){ int i2 = mm==0?invL[i][k]:invR[i][k]; int s=SID(v,i2,mm);
        if(W[s]) continue;
        if(mm==sigma){ W[s]=1; queue_[qt++]=s; } else { if(--cntbuf[s]==0){ W[s]=1; queue_[qt++]=s; } } }
  }
}
typedef struct { int lam[MAXN], rho[MAXN]; long LS[MAXN], RS[MAXN]; int num[MAXN]; long numv[MAXN]; int err; int d2bad[MAXN]; int mono[MAXN]; int amb[MAXN]; } Res;
static int memoS[MAXN][2]; static long memoV[MAXN][2]; static int isnum[MAXN]; static long numval[MAXN]; static int cyc;
static long stop_rec(int v,int which){ // which 0: LS, 1: RS
  if(isnum[v]) return numval[v];
  if(memoS[v][which]==2) return memoV[v][which];
  if(memoS[v][which]==1){ cyc=1; return 0; }
  memoS[v][which]=1; long r;
  if(which==0){ r=NINF; for(int u=0;u<n;u++) if(Lm[v]>>u&1){ long t=stop_rec(u,1); if(t>r) r=t; } }
  else { r=PINF; for(int u=0;u<n;u++) if(Rm[v]>>u&1){ long t=stop_rec(u,0); if(t<r) r=t; } }
  memoS[v][which]=2; memoV[v][which]=r; return r;
}
static void analyze(Res *R){
  solve(0); solve(1);
  memset(R,0,sizeof *R); cyc=0;
  memset(memoS,0,sizeof memoS);
  for(int v=0;v<n;v++){
    isnum[v]=0; int found=0;
    for(int i=0;i<NV;i++){ if(winT[0][SID(v,i,1)] && winT[1][SID(v,i,0)]){ found++; isnum[v]=1; numval[v]=-(long)(i-M*D); } }
    if(found>1) R->amb[v]=1;
  }
  for(int v=0;v<n;v++){
    R->LS[v]=stop_rec(v,0); R->RS[v]=stop_rec(v,1);
    int lam=LINF; for(int C=0;C<=M;C++){ if(winT[0][SID(v,M*D+C*D,1)]){lam=C;break;} }
    int rho=LINF; for(int C=0;C<=M;C++){ if(winT[1][SID(v,M*D-C*D,0)]){rho=C;break;} }
    R->lam[v]=lam; R->rho[v]=rho;
    // D1 vs D2 grid consistency and monotonicity
    int bad=0, mono=0;
    for(int w=0;w<2;w++){
      long st = w? R->RS[v] : R->LS[v];   // w=1: RS, Left wins second (m=1); w=0: LS, Left wins first (m=0)
      int prev=1;
      for(int i=NV-1;i>=0;i--){            // i high = q high = x low: x ascending as i descends
        long xs=-(long)(i-M*D);            // x scaled
        int win=winT[0][SID(v,i,w?1:0)];
        // as x increases (i decreases) win must go from 1 to 0 only
        if(win && !prev) mono=1; prev=win;
        if(st==PINF){ if(!win) bad=1; }
        else if(st==NINF){ if(win) bad=1; }
        else { if(xs<st && !win) bad=1; if(xs>st && win) bad=1; }
      }
    }
    R->d2bad[v]=bad; R->mono[v]=mono;
  }
  R->err=cyc;
}
typedef struct { long graphs, nodes, d2bad, mono, amb, cyc, bigstop;
  long corr[2], inf[2], lit_node[2], lit_root[2], lit_root_either, corr_root[2], nfinite_lit_ok[2], litwrong[2]; long sigcount[512]; long sigkey[512][4]; int nsig; } Tally;
static Tally T;
static void addsig(long a,long b,long c,long d){
  for(int k=0;k<T.nsig;k++) if(T.sigkey[k][0]==a&&T.sigkey[k][1]==b&&T.sigkey[k][2]==c&&T.sigkey[k][3]==d){T.sigcount[k]++;return;}
  if(T.nsig<512){T.sigkey[T.nsig][0]=a;T.sigkey[T.nsig][1]=b;T.sigkey[T.nsig][2]=c;T.sigkey[T.nsig][3]=d;T.sigcount[T.nsig++]=1;}
}
static void tally_graph(Res *R, int root_only_sig, int example_dump){
  T.graphs++; if(R->err) T.cyc++;
  int rootlit[2]={0,0};
  for(int v=0;v<n;v++){
    T.nodes++; if(R->d2bad[v]) T.d2bad++; if(R->mono[v]) T.mono++; if(R->amb[v]) T.amb++;
    for(int w=0;w<2;w++){
      int res = w? R->rho[v] : R->lam[v];
      long st = w? R->LS[v] : R->RS[v];
      int okc=1, okl=1;
      if(w==0){
        if(st==NINF){ if(res!=LINF) okc=0; }
        else if(st==PINF){ if(res!=0) okc=0; }
        else { long lo=-fdiv(st,D); long hi=-cdiv(st,D)+1; if(lo<0)lo=0; if(hi<0)hi=0;
               if(res==LINF||res<lo||res>hi) okc=0;
               long c=-fdiv(st,D); if(!(res==c||res==c+1)) okl=0; if(res==LINF) okl=0; }
      } else {
        if(st==PINF){ if(res!=LINF) okc=0; }
        else if(st==NINF){ if(res!=0) okc=0; }
        else { long lo=cdiv(st,D); long hi=fdiv(st,D)+1; if(lo<0)lo=0; if(hi<0)hi=0;
               if(res==LINF||res<lo||res>hi) okc=0;
               long c=cdiv(st,D); if(!(res==c||res==c+1)) okl=0; if(res==LINF) okl=0; }
      }
      int finite = (st!=PINF && st!=NINF);
      if(finite){ int beyond = (w==0)? (st>=2L*D) : (st<=-2L*D); if(beyond==okl) T.litwrong[w]++; }
      if(!okc){ T.corr[w]++; if(v==0) T.corr_root[w]++; }
      if(finite && !okl){ T.lit_node[w]++; if(v==0){ T.lit_root[w]++; rootlit[w]=1; } }
      // infinity pairing: reserve infinite iff the stop is the extreme one
      int extreme = (w==0)? (st==NINF) : (st==PINF);
      if(extreme != (res==LINF)) T.inf[w]++;
    }
    if(R->RS[v]!=PINF && R->RS[v]!=NINF && (R->RS[v]>(long)(M-1)*D || R->RS[v]<-(long)(M-1)*D)) T.bigstop++;
    if(v==0 || !root_only_sig){
      if(v==0){ addsig(R->lam[v],R->rho[v],R->LS[v]==PINF||R->LS[v]==NINF?R->LS[v]:R->LS[v]*16/D, R->RS[v]==PINF||R->RS[v]==NINF?R->RS[v]:R->RS[v]*16/D); }
    }
  }
  if(rootlit[0]||rootlit[1]) T.lit_root_either++;
  if(example_dump && (rootlit[0]||rootlit[1])){
    printf("LITEX n=%d",n); for(int v=0;v<n;v++) printf(" %d:L%02x R%02x",v,Lm[v],Rm[v]); printf(" | root lam=%d rho=%d LS=%ld/%d RS=%ld/%d\n",R->lam[0],R->rho[0],R->LS[0],D,R->RS[0],D);
  }
}
static void print_tally(const char *tag){
  printf("[%s] graphs %ld nodes %ld  cyc-errors %ld  D2-vs-D1 bad nodes %ld  monotone-bad %ld  number-ambiguous %ld  bigstops %ld\n",tag,T.graphs,T.nodes,T.cyc,T.d2bad,T.mono,T.amb,T.bigstop);
  printf("[%s] node-level corrected violations lam %ld rho %ld ; infinity-pairing violations lam %ld rho %ld ; literal violations (finite stop) lam %ld rho %ld\n",tag,T.corr[0],T.corr[1],T.inf[0],T.inf[1],T.lit_node[0],T.lit_node[1]);
  printf("[%s] finite-stop nodes where (literal form fails) differs from (RS>=2 for lam / LS<=-2 for rho): lam %ld rho %ld\n",tag,T.litwrong[0],T.litwrong[1]);
  printf("[%s] root-level: corrected violations lam %ld rho %ld ; literal violations lam %ld rho %ld either %ld\n",tag,T.corr_root[0],T.corr_root[1],T.lit_root[0],T.lit_root[1],T.lit_root_either);
}
static void print_sigs(void){
  printf("signatures %d\n",T.nsig);
  for(int k=0;k<T.nsig;k++){ long a=T.sigkey[k][0],b=T.sigkey[k][1],c=T.sigkey[k][2],d=T.sigkey[k][3];
    char sc[32],sd[32];
    if(c==PINF) strcpy(sc,"+inf"); else if(c==NINF) strcpy(sc,"-inf"); else sprintf(sc,"%ld/16",c);
    if(d==PINF) strcpy(sd,"+inf"); else if(d==NINF) strcpy(sd,"-inf"); else sprintf(sd,"%ld/16",d);
    printf("SIG lam=%ld rho=%ld LS=%s RS=%s count=%ld\n",a,b,sc,sd,T.sigcount[k]); }
}
// ---------- structural predicates ----------
static int is_stopper(void){
  unsigned aliveL=(1u<<n)-1, aliveR=(1u<<n)-1; int ch=1;
  while(ch){ ch=0;
    for(int v=0;v<n;v++){
      if((aliveL>>v&1) && !(Lm[v]&aliveR)){ aliveL&=~(1u<<v); ch=1; }
      if((aliveR>>v&1) && !(Rm[v]&aliveL)){ aliveR&=~(1u<<v); ch=1; }
    } }
  return aliveL==0 && aliveR==0;
}
static unsigned reach_from0(void){
  unsigned r=1, nr; do{ nr=r; for(int v=0;v<n;v++) if(r>>v&1) nr|=Lm[v]|Rm[v]; if(nr==r)break; r=nr; }while(1);
  return r;
}
// ---------- enumeration (n<=4, root 0, all nodes reachable, class = canonical under perms of nodes 1..n-1) ----------
static int perms[24][MAXN]; static int nperm; static int pmask[24][1<<4];
static void make_perms(void){
  nperm=0; int a[MAXN]; for(int i=0;i<n;i++)a[i]=i;
  // generate perms of 1..n-1 by recursion (simple)
  int idx[MAXN]; 
  // iterative via Heap-less brute force: enumerate all n-tuples
  int total=1; for(int i=1;i<n;i++) total*=n;
  for(int t=0;t<total && nperm<24;t++){
    int x=t; int p[MAXN]; p[0]=0; unsigned used=1; int ok=1;
    for(int i=1;i<n;i++){ p[i]=x%n; x/=n; if(p[i]==0||(used>>p[i]&1)){ok=0;break;} used|=1u<<p[i]; }
    if(!ok) continue; memcpy(perms[nperm],p,sizeof p);
    for(int m=0;m<(1<<n);m++){ int r=0; for(int i=0;i<n;i++) if(m>>i&1) r|=1<<p[i]; pmask[nperm][m]=r; }
    nperm++; }
  (void)a;(void)idx;
}
static int canonical(void){   // code = sum_i field_i << ((n-1-i)*2n), field = L | R<<n ; canonical iff <= all permuted codes
  int fw=2*n;
  uint64_t code=0; for(int i=0;i<n;i++) code|=((uint64_t)(Lm[i]|(Rm[i]<<n)))<<((n-1-i)*fw);
  for(int pi=0;pi<nperm;pi++){
    int *p=perms[pi]; int nl[MAXN], nr[MAXN];
    for(int i=0;i<n;i++){ nl[p[i]]=pmask[pi][Lm[i]]; nr[p[i]]=pmask[pi][Rm[i]]; }
    uint64_t c2=0; for(int i=0;i<n;i++) c2|=((uint64_t)(nl[i]|(nr[i]<<n)))<<((n-1-i)*fw);
    if(c2<code) return 0;
  }
  return 1;
}
static void enum_range(int nn, uint64_t lo, uint64_t hi, long *labelled, long *classes, int dump){
  n=nn; make_perms(); int fw=2*n; uint64_t fmask=(1u<<fw)-1; 
  Res R; long lab=0, cls=0;
  for(uint64_t code=lo; code<hi; code++){
    for(int i=0;i<n;i++){ uint64_t f=(code>>((n-1-i)*fw))&fmask; Lm[i]=f&((1<<n)-1); Rm[i]=f>>n; }
    if(!(Lm[0]|Rm[0]) && n>1) { code |= ((1ull<<((n-1)*fw))-1); continue; }   // skip rest of node-0 field block (all have empty node 0 options)
    if(reach_from0()!=(1u<<n)-1) continue;
    if(!is_stopper()) continue;
    lab++;
    if(!canonical()) continue;
    cls++;
    analyze(&R); tally_graph(&R,1,dump);
  }
  *labelled=lab; *classes=cls;
}
// ---------- random ----------
static uint64_t rs;
static uint64_t rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static double rndu(void){ return (rnd()>>11)*(1.0/9007199254740992.0); }
int main(int argc,char**argv){
  if(argc<2){fprintf(stderr,"usage\n");return 1;}
  memset(&T,0,sizeof T);
  if(!strcmp(argv[1],"enum")){   // enum N lo hi K M [dump]   (lo,hi are code range; for N=4 use top-byte values times 2^24)
    int nn=atoi(argv[2]); uint64_t lo=strtoull(argv[3],0,10), hi=strtoull(argv[4],0,10); int k=atoi(argv[5]), m=atoi(argv[6]); int dump=argc>7;
    n=nn; setup_grid(k,m);
    if(nn==4){ lo<<=24; hi<<=24; }
    long lab,cls; enum_range(nn,lo,hi,&lab,&cls,dump);
    printf("ENUM n=%d range [%llu,%llu) K=%d M=%d labelled-rooted-stoppers %ld classes %ld\n",nn,(unsigned long long)lo,(unsigned long long)hi,k,m,lab,cls);
    print_tally("enum"); print_sigs();
  } else if(!strcmp(argv[1],"rand")){  // rand n count seed pmin pmax K M
    int nn=atoi(argv[2]); long cnt=atol(argv[3]); rs=strtoull(argv[4],0,10)*2654435761ull+88172645463325252ull; double pmin=atof(argv[5]),pmax=atof(argv[6]); int k=atoi(argv[7]), m=atoi(argv[8]);
    n=nn; setup_grid(k,m); Res R; long made=0, tried=0;
    long litnodesL=0;
    while(made<cnt){
      double p=pmin+(pmax-pmin)*rndu(); tried++;
      for(int v=0;v<n;v++){ Lm[v]=Rm[v]=0; for(int u=0;u<n;u++){ if(rndu()<p) Lm[v]|=1<<u; if(rndu()<p) Rm[v]|=1<<u; } }
      if(!is_stopper()) continue; made++;
      analyze(&R); tally_graph(&R,1,0);
    }
    (void)litnodesL;
    printf("RAND n=%d graphs %ld (tried %ld) K=%d M=%d p in [%.2f,%.2f]\n",nn,made,tried,k,m,pmin,pmax);
    print_tally("rand");
  } else if(!strcmp(argv[1],"batch")){  // batch K M  < lines "n L0 R0 L1 R1 ..." ; prints per-node results
    int k=atoi(argv[2]), m=atoi(argv[3]); setup_grid(k,m); Res R; char line[1024]; int gi=0;
    while(fgets(line,sizeof line,stdin)){
      char *p=line; int nn=strtol(p,&p,10); if(nn<=0) continue; n=nn;
      for(int v=0;v<n;v++){ Lm[v]=strtol(p,&p,10); Rm[v]=strtol(p,&p,10); }
      if(!is_stopper()){ printf("g%d notstopper\n",gi++); continue; }
      analyze(&R);
      for(int v=0;v<n;v++){
        char a[32],b[32];
        if(R.LS[v]==PINF) strcpy(a,"+inf"); else if(R.LS[v]==NINF) strcpy(a,"-inf"); else sprintf(a,"%ld",R.LS[v]*16/D);
        if(R.RS[v]==PINF) strcpy(b,"+inf"); else if(R.RS[v]==NINF) strcpy(b,"-inf"); else sprintf(b,"%ld",R.RS[v]*16/D);
        printf("g%d %d %d %d %s %s\n",gi,v,R.lam[v],R.rho[v],a,b);
      }
      gi++;
    }
  } else if(!strcmp(argv[1],"graph")){  // graph K M n L0 R0 L1 R1 ...  (masks, decimal)
    int k=atoi(argv[2]), m=atoi(argv[3]); n=atoi(argv[4]); setup_grid(k,m);
    for(int v=0;v<n;v++){ Lm[v]=atoi(argv[5+2*v]); Rm[v]=atoi(argv[6+2*v]); }
    Res R; if(!is_stopper()){ printf("not a stopper\n"); return 0; }
    analyze(&R);
    for(int v=0;v<n;v++){
      char a[32],b[32];
      if(R.LS[v]==PINF) strcpy(a,"+inf"); else if(R.LS[v]==NINF) strcpy(a,"-inf"); else sprintf(a,"%g",(double)R.LS[v]/D);
      if(R.RS[v]==PINF) strcpy(b,"+inf"); else if(R.RS[v]==NINF) strcpy(b,"-inf"); else sprintf(b,"%g",(double)R.RS[v]/D);
      printf("node %d  lam=%d rho=%d LS=%s RS=%s d2bad=%d\n",v,R.lam[v],R.rho[v],a,b,R.d2bad[v]);
    }
  }
  return 0;
}
