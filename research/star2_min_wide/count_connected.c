/* count_roots.c -- independent re-implementation of the ROOT ENUMERATION RULE of
 * frontier_split1_fixed2.c (flat boards): counts the positions it would scan, without solving anything.
 * CONNECTED VARIANT (all files occupied; i.e. no empty file at all).
 * Rule: W pawns on ranks 2..6, B pawns on ranks 3..7, no shared square, nw>=1, nb>=1,
 *       both edge files (0 and W-1) occupied (interior files may be empty), no passed pawn (no e.p. state).
 * Usage: count_roots WIDTH P   -> lines "w p nw nb all= sym= mirror_reduced=" (mirror_reduced = what the scanner keeps:
 * one position of each left-right mirror pair, because canonical_root() with WRAP=0 still reflects)
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
static int W;
static uint64_t mirror(uint64_t m){uint64_t o=0;for(;m;m&=m-1){int s=__builtin_ctzll(m);int f=s&7,r=s>>3;o|=UINT64_C(1)<<(r*8+(W-1-f));}return o;}
static inline uint64_t B(int f,int r){return UINT64_C(1)<<((r-1)*8+f);}
static uint64_t frontW[64], frontB[64], fm[8];
static void init(void){
  for(int f=0;f<W;f++){fm[f]=0;for(int r=1;r<=8;r++)fm[f]|=B(f,r);}
  for(int f=0;f<W;f++)for(int r=1;r<=8;r++){
    uint64_t mw=0,mb=0;
    for(int g=f-1;g<=f+1;g++){ if(g<0||g>=W)continue;
      for(int s=1;s<=8;s++){ if(s>r)mw|=B(g,s); if(s<r)mb|=B(g,s);} }
    frontW[(r-1)*8+f]=mw; frontB[(r-1)*8+f]=mb; }
}
static int passed(uint64_t wm,uint64_t bm){
  for(uint64_t m=wm;m;m&=m-1){int s=__builtin_ctzll(m); if(!(bm&frontW[s]))return 1;}
  for(uint64_t m=bm;m;m&=m-1){int s=__builtin_ctzll(m); if(!(wm&frontB[s]))return 1;}
  return 0;
}
int main(int argc,char**argv){
  W=atoi(argv[1]); int P=atoi(argv[2]); init();
  int wc[64],bc[64],nwc=0,nbc=0;
  for(int f=0;f<W;f++){for(int r=2;r<=6;r++)wc[nwc++]=B(f,r)?(r-1)*8+f:0;for(int r=3;r<=7;r++)bc[nbc++]=(r-1)*8+f;}
  for(int nw=1;nw<P;nw++){ int nb=P-nw; if(nw>nwc||nb>nbc){printf("%d %d %d %d all=0 sym=0 mirror_reduced=0\n",W,P,nw,nb);continue;}
    long long cnt=0, sym=0; int iw[16],ib[16];
    for(int i=0;i<nw;i++)iw[i]=i;
    for(;;){
      uint64_t wm=0; for(int i=0;i<nw;i++)wm|=UINT64_C(1)<<wc[iw[i]];
      for(int i=0;i<nb;i++)ib[i]=i;
      for(;;){
        uint64_t bm=0; for(int i=0;i<nb;i++)bm|=UINT64_C(1)<<bc[ib[i]];
        if(!(wm&bm)){ uint64_t occ=wm|bm;
          int allf=1; for(int f=0;f<W;f++) if(!(occ&fm[f])) allf=0; if(allf&&!passed(wm,bm)){cnt++; if(mirror(wm)==wm&&mirror(bm)==bm)sym++;} }
        int i=nb-1; while(i>=0&&ib[i]==nbc-nb+i)i--; if(i<0)break; ib[i]++; for(int j=i+1;j<nb;j++)ib[j]=ib[j-1]+1; }
      int i=nw-1; while(i>=0&&iw[i]==nwc-nw+i)i--; if(i<0)break; iw[i]++; for(int j=i+1;j<nw;j++)iw[j]=iw[j-1]+1; }
    printf("%d %d %d %d all=%lld sym=%lld mirror_reduced=%lld\n",W,P,nw,nb,cnt,sym,(cnt+sym)/2); fflush(stdout); }
  return 0; }
