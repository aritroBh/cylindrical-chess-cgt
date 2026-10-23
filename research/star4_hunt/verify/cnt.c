// Independent root counter for flat boards: DP over files + Burnside.  Root = all files occupied, W on ranks 2..6, B on ranks 3..7,
// no passed pawn for either side (textbook test; no e.p. flag at the root).  Orbit counts under mirror (and colour reversal if nW==nB).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64;
#define MAXC 400
static int nc; static int cw[MAXC], cb[MAXC];            // rank bitmasks (bit r) for W / B
static int nW[MAXC], nB[MAXC], maxW[MAXC], minW[MAXC], maxB[MAXC], minB[MAXC], flipc[MAXC];
static int NMAX;
static int hi(int m){int r=0;for(int i=1;i<=8;i++)if(m>>i&1)r=i;return r;}
static int lo(int m){for(int i=1;i<=8;i++)if(m>>i&1)return i;return 99;}
static int idx_of(int w,int b){for(int i=0;i<nc;i++)if(cw[i]==w&&cb[i]==b)return i;return -1;}
// validity of the middle file given neighbours a,c (index -1 = no file)
static int okmid(int a,int b,int c){
  int mB=0,mW=99;
  int t[3]={a,b,c};
  for(int i=0;i<3;i++) if(t[i]>=0){ if(maxB[t[i]]>mB)mB=maxB[t[i]]; if(minW[t[i]]<mW)mW=minW[t[i]]; }
  if(nW[b]>0 && !(mB>maxW[b])) return 0;     // highest W pawn on b must have a B pawn ahead on b-1,b,b+1
  if(nB[b]>0 && !(mW<minB[b])) return 0;     // lowest B pawn on b must have a W pawn "ahead" (lower rank)
  return 1;
}
int main(int argc,char**argv){
  int W=atoi(argv[1]); int N=atoi(argv[2]); NMAX=N;
  nc=0;
  for(int w=0;w<(1<<9);w++){ if(w&~0x7C) continue;           // ranks 2..6 -> bits 2..6
    for(int b=0;b<(1<<9);b++){ if(b&~0xF8) continue;         // ranks 3..7 -> bits 3..7
      if(w&b) continue; if(!(w|b)) continue;                 // non-empty file
      cw[nc]=w; cb[nc]=b; nc++; } }
  for(int i=0;i<nc;i++){ nW[i]=__builtin_popcount(cw[i]); nB[i]=__builtin_popcount(cb[i]); maxW[i]=hi(cw[i]); minW[i]=lo(cw[i]); maxB[i]=hi(cb[i]); minB[i]=lo(cb[i]);}
  for(int i=0;i<nc;i++){ // colour reversal: W at rank r -> B at 9-r
    int w2=0,b2=0; for(int r=1;r<=8;r++){ if(cw[i]>>r&1) b2|=1<<(9-r); if(cb[i]>>r&1) w2|=1<<(9-r);} flipc[i]=idx_of(w2,b2); if(flipc[i]<0){fprintf(stderr,"flip err\n");return 1;} }
  fprintf(stderr,"configs %d\n",nc);
  int D=N+1;
  // DP: state (prev,cur) with prev in 0..nc (nc = none)
  size_t S=(size_t)(nc+1)*nc;
  u64 *cur=calloc(S*D*D,8), *nxt;
  if(!cur){fprintf(stderr,"oom\n");return 1;}
  for(int c=0;c<nc;c++){ if(nW[c]+nB[c]>N)continue; cur[(((size_t)nc*nc+c)*D+nW[c])*D+nB[c]]+=1; }
  for(int f=1;f<W;f++){
    nxt=calloc(S*D*D,8);
    for(int p=0;p<=nc;p++) for(int c=0;c<nc;c++){
      u64*src=&cur[(((size_t)p*nc)+c)*D*D]; int any=0; for(int i=0;i<D*D;i++) if(src[i]){any=1;break;} if(!any)continue;
      for(int d=0;d<nc;d++){
        if(!okmid(p==nc?-1:p,c,d)) continue;
        u64*dst=&nxt[(((size_t)c*nc)+d)*D*D];
        for(int i=0;i+nW[d]<D;i++)for(int j=0;j+nB[d]<D && i+nW[d]+j+nB[d]<=N;j++){ u64 v=src[i*D+j]; if(v) dst[(i+nW[d])*D+(j+nB[d])]+=v; }
      }
    }
    free(cur);cur=nxt;
  }
  u64 *tot=calloc(D*D,8);
  for(int p=0;p<=nc;p++)for(int c=0;c<nc;c++){ if(!okmid(p==nc?-1:p,c,-1)) continue; u64*src=&cur[(((size_t)p*nc)+c)*D*D]; for(int i=0;i<D*D;i++) tot[i]+=src[i]; }
  // fixed points
  u64 *Fm=calloc(D*D,8),*Fc=calloc(D*D,8),*Fmc=calloc(D*D,8);
  // enumerate all tuples via recursion restricted to the symmetric families
  int t[8];
  int half=(W+1)/2;
  // mirror-fixed: c_{W-1-f}=c_f ; free choice of first half
  { int idx[8]; long long tot_=1; for(int i=0;i<half;i++)tot_*=nc;
    for(long long x=0;x<tot_;x++){ long long y=x; for(int i=0;i<half;i++){idx[i]=y%nc;y/=nc;}
      for(int f=0;f<W;f++) t[f]= f<half? idx[f] : idx[W-1-f];
      int w=0,b=0,ok=1; for(int f=0;f<W;f++){w+=nW[t[f]];b+=nB[t[f]];} if(w+b>N)continue;
      for(int f=0;f<W&&ok;f++) ok=okmid(f?t[f-1]:-1,t[f],f<W-1?t[f+1]:-1); if(ok)Fm[w*D+b]++; } }
  // colour-fixed: each file self-flip
  { int sf[MAXC],ns=0; for(int i=0;i<nc;i++) if(flipc[i]==i) sf[ns++]=i; long long tot_=1; for(int i=0;i<W;i++)tot_*=ns;
    for(long long x=0;x<tot_;x++){ long long y=x; for(int f=0;f<W;f++){t[f]=sf[y%ns];y/=ns;}
      int w=0,b=0,ok=1; for(int f=0;f<W;f++){w+=nW[t[f]];b+=nB[t[f]];} if(w+b>N)continue;
      for(int f=0;f<W&&ok;f++) ok=okmid(f?t[f-1]:-1,t[f],f<W-1?t[f+1]:-1); if(ok)Fc[w*D+b]++; } }
  // mirror o colour: c_{W-1-f}=flip(c_f); middle file (odd W) must be self-flip
  { int idx[8]; long long tot_=1; for(int i=0;i<half;i++)tot_*=nc;
    for(long long x=0;x<tot_;x++){ long long y=x; for(int i=0;i<half;i++){idx[i]=y%nc;y/=nc;}
      int good=1; for(int f=0;f<W;f++){ if(f<half)t[f]=idx[f]; else t[f]=flipc[idx[W-1-f]]; }
      if(W%2==1){ int m=W/2; if(flipc[idx[m]]!=idx[m]) good=0; }
      if(!good)continue;
      int w=0,b=0,ok=1; for(int f=0;f<W;f++){w+=nW[t[f]];b+=nB[t[f]];} if(w+b>N)continue;
      for(int f=0;f<W&&ok;f++) ok=okmid(f?t[f-1]:-1,t[f],f<W-1?t[f+1]:-1); if(ok)Fmc[w*D+b]++; } }
  for(int w=0;w<=N;w++){ int b=N-w; if(w>b) continue; u64 n=tot[w*D+b];
    u64 orb;
    if(w==b) orb=(n+Fm[w*D+b]+Fc[w*D+b]+Fmc[w*D+b])/4; else orb=(n+Fm[w*D+b])/2;
    printf("W=%d split %d+%d labelled=%llu fixM=%llu fixC=%llu fixMC=%llu orbits=%llu%s\n",W,w,b,(unsigned long long)n,(unsigned long long)Fm[w*D+b],(unsigned long long)Fc[w*D+b],(unsigned long long)Fmc[w*D+b],(unsigned long long)orb,
      (w==b&&((n+Fm[w*D+b]+Fc[w*D+b]+Fmc[w*D+b])%4))?"  (!!not divisible)":""); }
  return 0;
}
