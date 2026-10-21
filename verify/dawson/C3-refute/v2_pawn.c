/* C3 REFUTE-lens verifier, version 2 (written from scratch in this session).
   Raw pawn-level Dawson's chess on a 3 x n board, flat or cylinder.
   No macro-move / octal assumption, no symmetry reduction.
   Rules: W pawns start rank 1, B pawns rank 3, rank 2 empty. A pawn moves one square
   straight forward onto an empty square, or one square diagonally forward onto an enemy
   pawn (capture; files 0 and n-1 adjacent when wrap). Captures compulsory.
   Normal play: side to move with no move loses; misere: it wins.
   Instrumentation: count legal moves that land on the last rank (promotion), and
   positions where a pawn of the side to move has two empty squares ahead (double-step
   geometry), split by whether a capture is available (then a double step would be illegal
   anyway because captures are compulsory).
   Usage: v2_pawn <maxflat> <maxring>                                              */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int N, WRAP;
/* board: 5 bits per file holding code c = r1 + 3*r2 + 9*r3 (each 0 empty, 1 W, 2 B); n <= 24 */
static const int P3[3]={1,3,9};
static inline int get(u128 b, int f, int r){ int c=(int)((b >> (5*f)) & 31); return (c / P3[r-1]) % 3; }
static inline u128 put(u128 b, int f, int r, int v){
  int c=(int)((b >> (5*f)) & 31); c += (v - (c / P3[r-1]) % 3) * P3[r-1];
  b &= ~(((u128)31) << (5*f)); b |= ((u128)c) << (5*f); return b; }
static int nb(int f, int d){ int x=f+d; if(WRAP){ x=(x+N)%N; return x; } return (x>=0&&x<N)?x:-1; }
/* hash table */
static u128 *K; static unsigned char *V; static uint64_t cap, cnt;
static uint64_t hsh(u128 k){ uint64_t a=(uint64_t)k, c=(uint64_t)(k>>64);
  uint64_t h=a*0x9E3779B97F4A7C15ULL ^ (c+0x632BE59BD9B4E019ULL)*0xC2B2AE3D27D4EB4FULL;
  h^=h>>31; h*=0x94D049BB133111EBULL; h^=h>>29; return h; }
static void tinit(uint64_t c){ cap=c; cnt=0; K=calloc(cap,sizeof(u128)); V=calloc(cap,1); if(!K||!V){fprintf(stderr,"oom\n");exit(1);} }
static void tfree(void){ free(K); free(V); }
static int tget(u128 k){ uint64_t i=hsh(k)&(cap-1); while(K[i]){ if(K[i]==k) return V[i]; i=(i+1)&(cap-1);} return -1; }
static void tput(u128 k,int v);
static void grow(void){ u128*ok=K; unsigned char*ov=V; uint64_t oc=cap; tinit(oc*2);
  for(uint64_t i=0;i<oc;i++) if(ok[i]) tput(ok[i],ov[i]); free(ok); free(ov); }
static void tput(u128 k,int v){ if((cnt+1)*2>cap) grow(); uint64_t i=hsh(k)&(cap-1);
  while(K[i]){ if(K[i]==k){V[i]=v;return;} i=(i+1)&(cap-1);} K[i]=k; V[i]=v; cnt++; }
static uint64_t promo_legal, dbl_quiet, dbl_capt, stuck_last;
typedef struct { u128 b; int capt; int promo; } Mv;
/* generate legal moves for side s (1=W up, 2=B down) */
static int gen(u128 b, int s, Mv *out){
  int dir = (s==1)?1:-1, opp=3-s, nc=0, np=0; Mv caps[256], pushes[256];
  int dbl=0;
  for(int f=0;f<N;f++) for(int r=1;r<=3;r++){
    if(get(b,f,r)!=s) continue;
    int r2=r+dir; if(r2<1||r2>3){ stuck_last++; continue; }
    int last = (s==1)? (r2==3) : (r2==1);
    for(int d=-1; d<=1; d+=2){ int g=nb(f,d); if(g<0) continue;
      if(get(b,g,r2)==opp){ u128 nb2=put(put(b,f,r,0),g,r2,s); caps[nc].b=nb2; caps[nc].capt=1; caps[nc].promo=last; nc++; } }
    if(get(b,f,r2)==0){ u128 nb2=put(put(b,f,r,0),f,r2,s); pushes[np].b=nb2; pushes[np].capt=0; pushes[np].promo=last; np++;
      int r3=r2+dir; if(((s==1&&r==1)||(s==2&&r==3)) && r3>=1&&r3<=3 && get(b,f,r3)==0) dbl=1; }
  }
  if(dbl){ if(nc) dbl_capt++; else dbl_quiet++; }
  if(nc){ for(int i=0;i<nc;i++){ out[i]=caps[i]; if(caps[i].promo) promo_legal++; } return nc; }
  for(int i=0;i<np;i++){ out[i]=pushes[i]; if(pushes[i].promo) promo_legal++; } return np;
}
#define SIDEBIT 121
#define VALIDBIT 122
/* (The first version stored 6 bits per file and put the side bit at 125; for n >= 21 that
   overlapped board bits and for n >= 22 the board overflowed -- that run is kept as
   v2_pawn_20_23.BUGGY_n21plus.out and must not be used. Now 5 bits/file, n <= 24.) */
static u128 compress(u128 b){ return b; }
/* returns bit0 = normal win for side to move, bit1 = misere win */
static int solve(u128 b, int s){
  u128 key = compress(b) | (((u128)(s-1))<<SIDEBIT) | (((u128)1)<<VALIDBIT);
  int v=tget(key); if(v>=0) return v;
  Mv mv[256]; int m=gen(b,s,mv);
  int nw=0, mw=0;
  if(m==0){ nw=0; mw=1; }
  else for(int i=0;i<m;i++){ int c=solve(mv[i].b,3-s); if(!(c&1)) nw=1; if(!(c&2)) mw=1; }
  v = nw | (mw<<1); tput(key,v); return v;
}
static u128 startpos(void){ u128 b=0; for(int f=0;f<N;f++){ b=put(b,f,1,1); b=put(b,f,3,2);} return b; }
/* forced-line lemma check from the start for side s: every push followed by every forced
   capture line until the side to move has no capture. Returns 1 if all results have the
   claimed shape: one file f with a blocked pair, f-1 and f+1 empty, rest untouched,
   and the opponent of s to move after an odd number of plies. */
static int lemma_ok, lemma_lines, lemma_badplies;
static void follow(u128 b, int s, int mover, int ply, int f0){
  Mv mv[256]; int m=gen(b,s,mv);
  int anycap = (m>0 && mv[0].capt);
  if(ply>0 && !anycap){ /* quiet */
    lemma_lines++;
    if(s==mover || (ply%2)==0){ lemma_badplies++; lemma_ok=0; }
    /* check shape */
    for(int f=0;f<N;f++){
      int r1=get(b,f,1), r2=get(b,f,2), r3=get(b,f,3);
      int dl = (f - f0 + N) % N; /* distance */
      int isf = (f==f0), isn = (nb(f0,-1)==f || nb(f0,1)==f);
      if(isf){ int ok = (mover==1)? (r1==0&&r2==1&&r3==2) : (r1==1&&r2==2&&r3==0); if(!ok) lemma_ok=0; }
      else if(isn){ if(r1||r2||r3) lemma_ok=0; }
      else { if(!(r1==1&&r2==0&&r3==2)) lemma_ok=0; }
      (void)dl;
    }
    return;
  }
  for(int i=0;i<m;i++){ if(ply>0 && !mv[i].capt) continue; follow(mv[i].b,3-s,mover,ply+1,f0); }
}
static int lemma(int s){
  u128 b=startpos(); lemma_ok=1; lemma_lines=0; lemma_badplies=0;
  int r = (s==1)?1:3; int dir=(s==1)?1:-1;
  for(int f=0;f<N;f++){ u128 nb2=put(put(b,f,r,0),f,r+dir,s); follow(nb2,3-s,s,1,f); }
  return lemma_ok;
}
int main(int argc,char**argv){
  int maxflat=atoi(argv[1]), maxring=atoi(argv[2]);
  if(maxflat>24||maxring>24){ fprintf(stderr,"n<=24 only\n"); return 1; }
  int flatN[64], flatM[64];
  printf("FLAT boards (raw pawn minimax). cols: n states normalW normalB misereW misereB promo_legal dbl_quiet dbl_capt\n");
  for(int n=0;n<=maxflat;n++){
    N=n; WRAP=0; tinit(1<<16); promo_legal=dbl_quiet=dbl_capt=stuck_last=0;
    u128 b=startpos(); int w=solve(b,1), k=solve(b,2);
    flatN[n]=w&1; flatM[n]=(w>>1)&1;
    printf("flat %2d %10llu  N:%s/%s  M:%s/%s  %llu %llu %llu\n", n,(unsigned long long)cnt,
      (w&1)?"win":"loss",(k&1)?"win":"loss",(w&2)?"win":"loss",(k&2)?"win":"loss",
      (unsigned long long)promo_legal,(unsigned long long)dbl_quiet,(unsigned long long)dbl_capt);
    if(((w^k)&3)) printf("  !! colour asymmetry on flat %d\n",n);
    fflush(stdout); tfree();
  }
  printf("RING boards. cols: n states normalW normalB misereW misereB | lemma(W,B) lines | flat(n-3) normal/misere first-player | ringrule_normal ringrule_misere | promo_legal dbl_quiet dbl_capt\n");
  for(int n=3;n<=maxring;n++){
    N=n; WRAP=1; tinit(1<<16); promo_legal=dbl_quiet=dbl_capt=stuck_last=0;
    u128 b=startpos(); int w=solve(b,1), k=solve(b,2);
    uint64_t st=cnt; uint64_t pl=promo_legal, dq=dbl_quiet, dc=dbl_capt;
    int lw=lemma(1); int lwl=lemma_lines; int lb=lemma(2); int lbl=lemma_lines;
    int m=n-3; char fn[8]="?", fm[8]="?"; int okN=-1, okM=-1;
    if(m<=maxflat){ /* ring first player wins iff flat(m) first player loses */
      okN = ((w&1) == (!flatN[m])); okM = (((w>>1)&1) == (!flatM[m]));
      strcpy(fn, flatN[m]?"win":"loss"); strcpy(fm, flatM[m]?"win":"loss"); }
    printf("ring %2d %10llu  N:%s/%s  M:%s/%s | lemma %d,%d lines %d,%d | flat%d %s/%s | %d %d | %llu %llu %llu\n",
      n,(unsigned long long)st,(w&1)?"win":"loss",(k&1)?"win":"loss",(w&2)?"win":"loss",(k&2)?"win":"loss",
      lw,lb,lwl,lbl,m,fn,fm,okN,okM,(unsigned long long)pl,(unsigned long long)dq,(unsigned long long)dc);
    if(((w^k)&3)) printf("  !! colour asymmetry on ring %d\n",n);
    fflush(stdout); tfree();
  }
  return 0;
}
