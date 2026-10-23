// Independent count of single-component roots on the 3-file ring (cylinder width 3): orbit counts under D3 (and colour reversal when nW==nB).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define MAXC 400
static int nc,cw[MAXC],cb[MAXC],nW[MAXC],nB[MAXC],mxW[MAXC],mnW[MAXC],mxB[MAXC],mnB[MAXC],fl[MAXC];
static int hi(int m){int r=0;for(int i=1;i<=8;i++)if(m>>i&1)r=i;return r;} static int lo(int m){for(int i=1;i<=8;i++)if(m>>i&1)return i;return 99;}
int main(){
  for(int w=0;w<512;w++){if(w&~0x7C)continue;for(int b=0;b<512;b++){if(b&~0xF8)continue;if(w&b)continue;if(!(w|b))continue;cw[nc]=w;cb[nc]=b;nc++;}}
  for(int i=0;i<nc;i++){nW[i]=__builtin_popcount(cw[i]);nB[i]=__builtin_popcount(cb[i]);mxW[i]=hi(cw[i]);mnW[i]=lo(cw[i]);mxB[i]=hi(cb[i]);mnB[i]=lo(cb[i]);
    int w2=0,b2=0;for(int r=1;r<=8;r++){if(cw[i]>>r&1)b2|=1<<(9-r);if(cb[i]>>r&1)w2|=1<<(9-r);}fl[i]=-1;for(int j=0;j<nc;j++)if(cw[j]==w2&&cb[j]==b2)fl[i]=j;}
  static uint64_t fix[12][20][20]; // group element x nW x nB
  int perm[6][3]={{0,1,2},{1,2,0},{2,0,1},{0,2,1},{2,1,0},{1,0,2}};
  for(int a=0;a<nc;a++)for(int b=0;b<nc;b++)for(int c=0;c<nc;c++){
    int t[3]={a,b,c};
    int MB=mxB[a]>mxB[b]?mxB[a]:mxB[b]; if(mxB[c]>MB)MB=mxB[c];
    int mW=mnW[a]<mnW[b]?mnW[a]:mnW[b]; if(mnW[c]<mW)mW=mnW[c];
    int ok=1; for(int i=0;i<3;i++){ if(nW[t[i]]>0&&!(MB>mxW[t[i]]))ok=0; if(nB[t[i]]>0&&!(mW<mnB[t[i]]))ok=0; }
    if(!ok)continue;
    int w=nW[a]+nW[b]+nW[c], bb=nB[a]+nB[b]+nB[c]; if(w>19||bb>19)continue;
    for(int g=0;g<12;g++){ int p=g%6, col=g/6; int u[3]; for(int i=0;i<3;i++){ int s=t[perm[p][i]]; u[i]=col?fl[s]:s; }
      if(u[0]==a&&u[1]==b&&u[2]==c) fix[g][w][bb]++; }
  }
  for(int N=11;N<=13;N++) for(int w=0;w<=N/2;w++){ int b=N-w; uint64_t n=fix[0][w][b]; if(!n&&w<2)continue;
    uint64_t s6=0; for(int g=0;g<6;g++) s6+=fix[g][w][b]; uint64_t s12=s6; for(int g=6;g<12;g++) s12+=fix[g][w][b];
    uint64_t orb = (w==b)? s12/12 : s6/6;
    printf("C3 N=%d split %d+%d labelled=%llu orbits=%llu%s\n",N,w,b,(unsigned long long)n,(unsigned long long)orb,(w==b? (s12%12?" !!":""):(s6%6?" !!":""))); }
  return 0; }
