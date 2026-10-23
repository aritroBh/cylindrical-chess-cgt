// s2.c -- adversarial re-implementation (written from cylcgt/pawns.py, NOT from h4.c).
// Whole-board semantics of cylcgt (components=[p]): ONE e.p. flag, cleared by ANY pawn move (the flag only survives a move of the nim heap).
// Value of a position G = bit vectors WL/WR over heap sizes k=0..63: bit k of WL = Left wins G+*k moving first, WR = Right wins moving first.
// Modes: eval FILE | sample | scan | dump
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64;
#define FULL (~(u64)0)
static int NF, WRAPF, EPON=1, SEMANTIC=0; // SEMANTIC 0: cylcgt whole-board (flag dies on any pawn move); 1: per-component flag (scanner-like) not implemented here
#define SQ(f,r) ((f)*8+((r)-1))
#define BIT(f,r) ((u64)1<<SQ(f,r))
static u64 FRONT[2][64];
static int nbr(int f,int df){ int g=f+df; if(WRAPF) return ((g%NF)+NF)%NF; return (g>=0&&g<NF)?g:-1; }
static void init(void){
  memset(FRONT,0,sizeof FRONT);
  for(int f=0;f<NF;f++) for(int r=1;r<=8;r++){
    u64 mw=0,mb=0;
    for(int df=-1;df<=1;df++){ int g=df?nbr(f,df):f; if(g<0)continue;
      for(int s=1;s<=8;s++){ if(s>r) mw|=BIT(g,s); if(s<r) mb|=BIT(g,s);} }
    FRONT[0][SQ(f,r)]=mw; FRONT[1][SQ(f,r)]=mb;
  }
}
static int ep_cap(int side,int s,u64 enemy,int ep){
  int f=s>>3, r=(s&7)+1;
  if(side==0){ if(ep!=1+f||r!=4) return 0; }
  else { if(ep!=9+f||r!=5) return 0; }
  for(int df=-1;df<=1;df+=2){ int g=nbr(f,df); if(g>=0 && (enemy&BIT(g,r))) return 1; }
  return 0;
}
static int passed_(int side,u64 wm,u64 bm,int ep){
  if(side==0){ for(u64 m=wm;m;m&=m-1){ int s=__builtin_ctzll(m); if(!(bm&FRONT[0][s])){ if(ep_cap(0,s,bm,ep)) continue; return 1; } } return 0; }
  for(u64 m=bm;m;m&=m-1){ int s=__builtin_ctzll(m); if(!(wm&FRONT[1][s])){ if(ep_cap(1,s,wm,ep)) continue; return 1; } } return 0;
}
static int dist_(int side,u64 wm,u64 bm,int ep){
  int best=1000000; u64 occ=wm|bm;
  u64 mine=side==0?wm:bm;
  for(u64 m=mine;m;m&=m-1){ int s=__builtin_ctzll(m); int f=s>>3,r=(s&7)+1;
    // isolated-pawn passed test against all enemy pawns
    if(side==0){ if(bm&FRONT[0][s]) continue; if(ep_cap(0,s,bm,ep)) continue;
      int blocked=0; for(int q=r+1;q<=8;q++) if(occ&BIT(f,q)) blocked=1; if(blocked) continue;
      int d=8-r-(r==2?1:0); if(d<best)best=d; }
    else { if(wm&FRONT[1][s]) continue; if(ep_cap(1,s,wm,ep)) continue;
      int blocked=0; for(int q=1;q<r;q++) if(occ&BIT(f,q)) blocked=1; if(blocked) continue;
      int d=r-1-(r==7?1:0); if(d<best)best=d; }
  }
  return best;
}
typedef struct { u64 WL,WR; } V;
typedef struct { u64 wm,bm; int ep; V v; int used; } E;
static E *tab; static u64 tcap, tcount;
static u64 mix(u64 x){ x^=x>>33; x*=0xff51afd7ed558ccdULL; x^=x>>33; x*=0xc4ceb9fe1a85ec53ULL; x^=x>>33; return x; }
static void tinit(u64 cap){ free(tab); tcap=cap; tcount=0; tab=calloc(cap,sizeof(E)); if(!tab){fprintf(stderr,"oom\n");exit(1);} }
static V solve(u64 wm,u64 bm,int ep);
static u64 child_win(int mover,u64 wm,u64 bm,int ep){
  int pw=passed_(0,wm,bm,ep), pb=passed_(1,wm,bm,ep);
  if(pw&&pb){ int other=1-mover; int dm=dist_(mover,wm,bm,ep), dop=dist_(other,wm,bm,ep); int winner=(dop<=dm)?other:mover; return winner==mover?FULL:0; }
  if(pw) return mover==0?FULL:0;
  if(pb) return mover==1?FULL:0;
  V v=solve(wm,bm,ep);
  return mover==0?~v.WR:~v.WL;
}
static u64 gen(int side,u64 wm,u64 bm,int ep){
  u64 acc=0, occ=wm|bm; u64 mine=side==0?wm:bm, theirs=side==0?bm:wm; int d=side==0?1:-1, start=side==0?2:7;
  for(u64 m=mine;m&&acc!=FULL;m&=m-1){ int s=__builtin_ctzll(m); int f=s>>3, r=(s&7)+1; int r1=r+d; if(r1<1||r1>8) continue;
    u64 rest=mine&~((u64)1<<s);
    #define CH(nm,nt,e) (side==0? child_win(0,(nm),(nt),(e)) : child_win(1,(nt),(nm),(e)))
    if(!(occ&BIT(f,r1))){
      acc|=CH(rest|BIT(f,r1),theirs,0);
      int r2=r+2*d;
      if(r==start && r2>=1&&r2<=8 && !(occ&BIT(f,r2))){
        int nep=0;
        if(EPON){ for(int df=-1;df<=1;df+=2){ int g=nbr(f,df); if(g>=0&&(theirs&BIT(g,r2))) nep=1; } }
        acc|=CH(rest|BIT(f,r2),theirs,nep?(side==0?1+f:9+f):0);
      }
    }
    for(int df=-1;df<=1;df+=2){ int g=nbr(f,df); if(g<0) continue;
      if(theirs&BIT(g,r1)) acc|=CH(rest|BIT(g,r1),theirs&~BIT(g,r1),0);
      else if(EPON && ((side==0&&r1==6&&ep==9+g)||(side==1&&r1==3&&ep==1+g))) acc|=CH(rest|BIT(g,r1),theirs&~BIT(g,r),0);
    }
  }
  return acc;
}
static V solve(u64 wm,u64 bm,int ep){
  u64 h=mix(wm^mix(bm^mix((u64)ep+77)))&(tcap-1);
  while(tab[h].used){ if(tab[h].wm==wm&&tab[h].bm==bm&&tab[h].ep==ep) return tab[h].v; h=(h+1)&(tcap-1); }
  u64 AL=gen(0,wm,bm,ep), AR=gen(1,wm,bm,ep);
  u64 WL=0,WR=0; int loseL=0,loseR=0;
  for(int k=0;k<64;k++){
    int wl=((AL>>k)&1)||loseR, wr=((AR>>k)&1)||loseL;
    if(wl)WL|=(u64)1<<k; if(wr)WR|=(u64)1<<k;
    if(!wr) loseR=1;   // Right moving first at G+*k loses  => Left can move heap to *k from any larger heap and win
    if(!wl) loseL=1;
  }
  V v={WL,WR};
  // re-probe (table may have been modified by recursion)
  h=mix(wm^mix(bm^mix((u64)ep+77)))&(tcap-1);
  while(tab[h].used){ if(tab[h].wm==wm&&tab[h].bm==bm&&tab[h].ep==ep) return v; h=(h+1)&(tcap-1); }
  if(tcount*10>=tcap*7) return v;     // table nearly full: do not store
  tab[h].wm=wm;tab[h].bm=bm;tab[h].ep=ep;tab[h].v=v;tab[h].used=1;tcount++;
  return v;
}
static void maybe_reset(void){ if(tcount*10>=tcap*5) tinit(tcap); }
static int nimber(V v){ for(int q=0;q<64;q++) if(!((v.WL>>q)&1)&&!((v.WR>>q)&1)) return q; return -1; }
static char oc(V v,int k){ int l=(v.WL>>k)&1, r=(v.WR>>k)&1; return l&&r?'N':l?'L':r?'R':'P'; }
static int prefN(V v){ int m=0; while(m<64&&((v.WL>>m)&1)&&((v.WR>>m)&1)) m++; return m; }
static int parse(const char*s,u64*wm,u64*bm){ *wm=*bm=0; u64*cur=0; for(const char*p=s;*p;){ if(*p=='W'&&p[1]==':'){cur=wm;p+=2;continue;} if(*p=='B'&&p[1]==':'){cur=bm;p+=2;continue;}
  if(*p>='a'&&*p<='h'&&p[1]>='1'&&p[1]<='8'&&cur){ *cur|=BIT(*p-'a',p[1]-'0'); p+=2; continue;} p++; } return 0; }
static void pstr(char*o,u64 wm,u64 bm){ char*p=o; p+=sprintf(p,"W:"); for(int f=0;f<NF;f++)for(int r=1;r<=8;r++) if(wm&BIT(f,r)) p+=sprintf(p," %c%d",'a'+f,r); p+=sprintf(p," / B:"); for(int f=0;f<NF;f++)for(int r=1;r<=8;r++) if(bm&BIT(f,r)) p+=sprintf(p," %c%d",'a'+f,r); }
static int valid_root(u64 wm,u64 bm,int single){
  if(wm&bm) return 0;
  if(passed_(0,wm,bm,0)||passed_(1,wm,bm,0)) return 0;
  if(single){ u64 occ=wm|bm; for(int f=0;f<NF;f++){ int has=0; for(int r=1;r<=8;r++) if(occ&BIT(f,r)) has=1; if(!has) return 0; } }
  return 1;
}
// ---- enumeration of canonical roots (flat only): per-file configs
#define MAXC 400
static int nc, cw[MAXC], cb[MAXC], cnW[MAXC], cnB[MAXC], cmaxW[MAXC], cminW[MAXC], cmaxB[MAXC], cminB[MAXC], cflip[MAXC];
static int hi_(int m){int r=0;for(int i=1;i<=8;i++)if(m>>i&1)r=i;return r;} static int lo_(int m){for(int i=1;i<=8;i++)if(m>>i&1)return i;return 99;}
static void mkcfg(void){ nc=0; for(int w=0;w<512;w++){ if(w&~0x7C)continue; for(int b=0;b<512;b++){ if(b&~0xF8)continue; if(w&b)continue; if(!(w|b))continue; cw[nc]=w;cb[nc]=b;nc++; } }
  for(int i=0;i<nc;i++){ cnW[i]=__builtin_popcount(cw[i]);cnB[i]=__builtin_popcount(cb[i]);cmaxW[i]=hi_(cw[i]);cminW[i]=lo_(cw[i]);cmaxB[i]=hi_(cb[i]);cminB[i]=lo_(cb[i]);
    int w2=0,b2=0; for(int r=1;r<=8;r++){ if(cw[i]>>r&1)b2|=1<<(9-r); if(cb[i]>>r&1)w2|=1<<(9-r);} cflip[i]=-1; for(int j=0;j<nc;j++) if(cw[j]==w2&&cb[j]==b2) cflip[i]=j; } }
static int okmid(int a,int b,int c){ int mB=0,mW=99; int t[3]={a,b,c}; for(int i=0;i<3;i++) if(t[i]>=0){ if(cmaxB[t[i]]>mB)mB=cmaxB[t[i]]; if(cminW[t[i]]<mW)mW=cminW[t[i]]; }
  if(cnW[b]>0&&!(mB>cmaxW[b]))return 0; if(cnB[b]>0&&!(mW<cminB[b]))return 0; return 1; }
static int T[8]; static int TW, TNW, TNB, CHI=0, CHN=1; static long nroots=0, hnim[66], hnear[8], hprefix[66], hsig=0; static long budget_roots=0;
static u64 tomask(int*t,int*nbm){ u64 wm=0,bm=0; for(int f=0;f<TW;f++){ for(int r=1;r<=8;r++){ if(cw[t[f]]>>r&1) wm|=BIT(f,r); if(cb[t[f]]>>r&1) bm|=BIT(f,r);} } *nbm=0; (void)nbm; return wm; }
static int lexcmp(int*a,int*b){ for(int f=0;f<TW;f++){ if(a[f]!=b[f]) return a[f]<b[f]?-1:1; } return 0; }
static long seq=0; static int PRINT_ALL=0; static long SLO=0, SHI=1L<<60; static int LISTONLY=0, PERROOT=0;
static void leaf(void){
  int m[8],fl[8],mf[8]; for(int f=0;f<TW;f++){ m[f]=T[TW-1-f]; fl[f]=cflip[T[f]]; mf[f]=cflip[T[TW-1-f]]; }
  if(lexcmp(T,m)>0) return;
  if(TNW==TNB){ if(lexcmp(T,fl)>0) return; if(lexcmp(T,mf)>0) return; }
  long my=seq++; if(my%CHN!=CHI) return; if(my<SLO||my>=SHI) return;
  u64 wm=0,bm=0; for(int f=0;f<TW;f++) for(int r=1;r<=8;r++){ if(cw[T[f]]>>r&1) wm|=BIT(f,r); if(cb[T[f]]>>r&1) bm|=BIT(f,r); }
  if(LISTONLY){ char b[300]; pstr(b,wm,bm); puts(b); nroots++; return; }
  maybe_reset();
  V v=solve(wm,bm,0); nroots++;
  if(PERROOT){ char b[300]; pstr(b,wm,bm); char o[10]; for(int k=0;k<8;k++)o[k]=oc(v,k); o[8]=0; printf("R\t%s\t%s\n",b,o); }
  int nim=nimber(v), pm=prefN(v); hnim[nim<0?65:nim]++; hprefix[pm>64?64:pm]++;
  int cnt=0,at=-1; for(int h=0;h<8;h++) if(oc(v,h)!='N'){cnt++;at=h;} if(cnt==1) hnear[at]++;
  if(nim>=2 || (cnt==1&&at>=3&&nim<0) || pm>=4){ char b[300]; pstr(b,wm,bm); char o[12]; for(int k=0;k<10;k++)o[k]=oc(v,k); o[10]=0; printf("%s\t%s\tnim=%d\tpref=%d\t%s\n",nim>=2?"HIT":(pm>=4?"RUN":"NEAR"),b,nim,pm,o); fflush(stdout);}
}
static void rec(int f,int w,int b){
  if(f==TW){ if(w==TNW&&b==TNB) leaf(); return; }
  for(int c=0;c<nc;c++){ int w2=w+cnW[c], b2=b+cnB[c]; if(w2>TNW||b2>TNB) continue;
    // remaining files must be able to hold the rest (each file has at least 1 pawn)
    int remf=TW-f-1; int rem=(TNW-w2)+(TNB-b2); if(rem<remf) continue;
    T[f]=c; if(f>=1 && !okmid(f>=2?T[f-2]:-1,T[f-1],c)) continue; if(f==TW-1 && !okmid(f>=1?T[f-1]:-1,c,-1)) continue; if(TW==1 && !okmid(-1,c,-1)) continue;
    rec(f+1,w2,b2); }
}
static u64 rs=88172645463325252ULL; static u64 rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
int main(int argc,char**argv){
  if(argc<3){fprintf(stderr,"usage: s2 MODE WIDTH ...\n");return 2;}
  const char*mode=argv[1]; NF=atoi(argv[2]); WRAPF=getenv("S2_WRAP")?1:0; init(); mkcfg();
  u64 cap=1ULL<<23;
  if(!strcmp(mode,"eval")){ tinit(cap); FILE*fp=fopen(argv[3],"r"); char line[2048]; printf("#position\twidth\tn\toutcome\tnimber\tG+*k_k0-7\n");
    while(fgets(line,sizeof line,fp)){ if(line[0]=='#'||strlen(line)<5)continue; line[strcspn(line,"\r\n")]=0; u64 wm,bm; parse(line,&wm,&bm); char b[300]; pstr(b,wm,bm);
      if(wm&bm){printf("%s\t%d\t-\tOVERLAP\n",b,NF);continue;} int n=__builtin_popcountll(wm)+__builtin_popcountll(bm);
      if(passed_(0,wm,bm,0)||passed_(1,wm,bm,0)){printf("%s\t%d\t%d\tPASSED\n",b,NF,n);continue;}
      maybe_reset(); V v=solve(wm,bm,0); char o[10]; for(int k=0;k<8;k++)o[k]=oc(v,k); o[8]=0; V vv=v; char outc=(vv.WL&1)&&(vv.WR&1)?'N':(vv.WL&1)?'L':(vv.WR&1)?'R':'P';
      printf("%s\t%d\t%d\t%c\t%d\t%s\n",b,NF,n,outc,nimber(v),o); }
    return 0; }
  if(!strcmp(mode,"sample")){ // sample WIDTH NW NB COUNT SEED
    int nw=atoi(argv[3]),nb=atoi(argv[4]); long cnt=atol(argv[5]); rs^=mix(atol(argv[6])); long got=0;
    while(got<cnt){ u64 wm=0,bm=0; int a=0; while(a<nw){ int f=rnd()%NF,r=2+rnd()%5; if(!(wm&BIT(f,r))){wm|=BIT(f,r);a++;} } a=0; while(a<nb){ int f=rnd()%NF,r=3+rnd()%5; if(!(bm&BIT(f,r))&&!(wm&BIT(f,r))){bm|=BIT(f,r);a++;} }
      if(!valid_root(wm,bm,1)) continue; char b[300]; pstr(b,wm,bm); puts(b); got++; }
    return 0; }
  if(!strcmp(mode,"scan")){ // scan WIDTH NW NB CHUNK_I CHUNK_N
    TW=NF; if(getenv("SLO"))SLO=atol(getenv("SLO")); if(getenv("SHI"))SHI=atol(getenv("SHI")); LISTONLY=getenv("LISTONLY")!=0; PERROOT=getenv("PERROOT")!=0; TNW=atoi(argv[3]); TNB=atoi(argv[4]); if(argc>6){CHI=atoi(argv[5]);CHN=atoi(argv[6]);} tinit(cap);
    rec(0,0,0);
    printf("#summary roots=%ld",nroots); for(int q=0;q<66;q++) if(hnim[q]) printf(" nim%d=%ld",q<65?q:-1,hnim[q]); printf(" near0..7:"); for(int i=0;i<8;i++)printf(" %ld",hnear[i]); printf(" prefix:"); for(int i=0;i<=64;i++) if(hprefix[i]) printf(" p%d=%ld",i,hprefix[i]); printf("\n");
    return 0; }
  return 2;
}
