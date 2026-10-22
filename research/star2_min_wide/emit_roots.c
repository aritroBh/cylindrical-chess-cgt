/* emit_roots.c WIDTH NW NB MODE MOD REM : print the roots the scanner enumerates (same rule + mirror reduction as
 * frontier_split1_fixed2.c on flat boards) -- MODE 'a' = edge files occupied (what the scanner scans), 'c' = every file occupied.
 * Only roots whose running index is == REM mod MOD are printed.  Position format as the scanner's. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
static int W;
static inline uint64_t B(int f,int r){return UINT64_C(1)<<((r-1)*8+f);}
static uint64_t frontW[64], frontB[64], fm[8];
static uint64_t mirror(uint64_t m){uint64_t o=0;for(;m;m&=m-1){int s=__builtin_ctzll(m);int f=s&7,r=s>>3;o|=UINT64_C(1)<<(r*8+(W-1-f));}return o;}
static void init(void){
  for(int f=0;f<W;f++){fm[f]=0;for(int r=1;r<=8;r++)fm[f]|=B(f,r);}
  for(int f=0;f<W;f++)for(int r=1;r<=8;r++){uint64_t mw=0,mb=0;
    for(int g=f-1;g<=f+1;g++){ if(g<0||g>=W)continue; for(int s=1;s<=8;s++){ if(s>r)mw|=B(g,s); if(s<r)mb|=B(g,s);} }
    frontW[(r-1)*8+f]=mw; frontB[(r-1)*8+f]=mb; } }
static int passed(uint64_t wm,uint64_t bm){
  for(uint64_t m=wm;m;m&=m-1){int s=__builtin_ctzll(m); if(!(bm&frontW[s]))return 1;}
  for(uint64_t m=bm;m;m&=m-1){int s=__builtin_ctzll(m); if(!(wm&frontB[s]))return 1;}
  return 0; }
static void pr(uint64_t wm,uint64_t bm){
  printf("W:"); for(int f=0;f<W;f++)for(int r=1;r<=8;r++) if(wm&B(f,r)) printf(" %c%d",'a'+f,r);
  printf(" / B:"); for(int f=0;f<W;f++)for(int r=1;r<=8;r++) if(bm&B(f,r)) printf(" %c%d",'a'+f,r);
  printf("\n"); }
int main(int argc,char**argv){
  W=atoi(argv[1]); int nw=atoi(argv[2]), nb=atoi(argv[3]); char mode=argv[4][0]; long MOD=atol(argv[5]), REM=atol(argv[6]); init();
  int wc[64],bc[64],nwc=0,nbc=0;
  for(int f=0;f<W;f++){for(int r=2;r<=6;r++)wc[nwc++]=(r-1)*8+f;for(int r=3;r<=7;r++)bc[nbc++]=(r-1)*8+f;}
  long idx=0; int iw[16],ib[16];
  for(int i=0;i<nw;i++)iw[i]=i;
  for(;;){
    uint64_t wm=0; for(int i=0;i<nw;i++)wm|=UINT64_C(1)<<wc[iw[i]];
    for(int i=0;i<nb;i++)ib[i]=i;
    for(;;){
      uint64_t bm=0; for(int i=0;i<nb;i++)bm|=UINT64_C(1)<<bc[ib[i]];
      if(!(wm&bm)){ uint64_t occ=wm|bm; int ok;
        if(mode=='c'){ok=1; for(int f=0;f<W;f++) if(!(occ&fm[f])) ok=0;} else ok=(occ&fm[0])&&(occ&fm[W-1]);
        if(ok&&!passed(wm,bm)){ uint64_t mw=mirror(wm), mb=mirror(bm);
          if(wm<mw||(wm==mw&&bm<=mb)){ if(idx%MOD==REM) pr(wm,bm); idx++; } } }
      int i=nb-1; while(i>=0&&ib[i]==nbc-nb+i)i--; if(i<0)break; ib[i]++; for(int j=i+1;j<nb;j++)ib[j]=ib[j-1]+1; }
    int i=nw-1; while(i>=0&&iw[i]==nwc-nw+i)i--; if(i<0)break; iw[i]++; for(int j=i+1;j<nw;j++)iw[j]=iw[j-1]+1; }
  fprintf(stderr,"emitted index range 0..%ld\n",idx); return 0; }
