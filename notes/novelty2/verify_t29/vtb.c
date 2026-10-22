// Independent verifier solver: White K + one white piece X vs lone black K, 8x8 board, files optionally wrapped.
// X in {Q,R,B,N,P}. Pawn table uses promotion sub-tables (Q,R,B,N). Plain level-by-level retrograde (forward sweeps).
// Written from the rules in paper/ieee/sections/10_tablebases.tex only (kings may not touch across the seam; no null move).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define NSQ 64
#define NIDX (64*64*64)
enum {Q=0,R=1,B=2,N=3,P=4};
static int wrapf;                 // 1 = cylinder
static int kn[NSQ][8], nkn[NSQ];  // king neighbours
static int nt[NSQ][8], nnt[NSQ];  // knight targets
static int ray[NSQ][8][8], raylen[NSQ][8];
static const int dr[8]={1,-1,0,0,1,1,-1,-1}, df[8]={0,0,1,-1,1,-1,1,-1}; // 0-3 orth, 4-7 diag
static int pa[NSQ][2], npa[NSQ];  // white pawn attack squares
static inline int idx(int wk,int x,int bk){return (wk<<12)|(x<<6)|bk;}
static int adj(int a,int b){ // kings adjacent?
  for(int i=0;i<nkn[a];i++) if(kn[a][i]==b) return 1; return 0; }
static void init(void){
  for(int s=0;s<NSQ;s++){
    int r=s>>3,f=s&7; nkn[s]=nnt[s]=npa[s]=0;
    for(int a=-1;a<=1;a++)for(int b=-1;b<=1;b++){ if(!a&&!b)continue;
      int r2=r+a,f2=f+b; if(r2<0||r2>7)continue;
      if(wrapf) f2=(f2+8)&7; else if(f2<0||f2>7)continue;
      kn[s][nkn[s]++]=r2*8+f2; }
    static const int kj[8][2]={{1,2},{2,1},{-1,2},{-2,1},{1,-2},{2,-1},{-1,-2},{-2,-1}};
    for(int k=0;k<8;k++){ int r2=r+kj[k][0],f2=f+kj[k][1]; if(r2<0||r2>7)continue;
      if(wrapf) f2=(f2+8)&7; else if(f2<0||f2>7)continue; nt[s][nnt[s]++]=r2*8+f2; }
    for(int d=0;d<8;d++){ raylen[s][d]=0; int rr=r,ff=f;
      for(int k=0;k<8;k++){ rr+=dr[d]; ff+=df[d]; if(rr<0||rr>7)break;
        if(wrapf) ff=(ff+8)&7; else if(ff<0||ff>7)break;
        if(rr*8+ff==s)break; ray[s][d][raylen[s][d]++]=rr*8+ff; } }
    if(r<7) for(int b=-1;b<=1;b+=2){ int f2=f+b; if(wrapf) f2=(f2+8)&7; else if(f2<0||f2>7)continue; pa[s][npa[s]++]=(r+1)*8+f2; }
  }
}
// does piece X on xs attack target t, given a single blocker square blk (white king); target itself ends the ray
static int attacks(int X,int xs,int t,int blk){
  if(X==N){ for(int i=0;i<nnt[xs];i++) if(nt[xs][i]==t) return 1; return 0; }
  if(X==P){ for(int i=0;i<npa[xs];i++) if(pa[xs][i]==t) return 1; return 0; }
  int d0=0,d1=8; if(X==R){d1=4;} else if(X==B){d0=4;}
  for(int d=d0;d<d1;d++) for(int k=0;k<raylen[xs][d];k++){ int s=ray[xs][d][k]; if(s==t) return 1; if(s==blk) break; }
  return 0;
}
typedef struct { short *d[2]; } Tab;   // depth in plies, -1 = not (yet) a white win; d[0]=WTM, d[1]=BTM
static char *legal[2];
static int islegal(int X,int stm,int wk,int x,int bk){
  if(wk==x||wk==bk||x==bk) return 0;
  if(adj(wk,bk)) return 0;
  if(X==P){ int r=x>>3; if(r<1||r>6) return 0; }
  if(stm==0 && attacks(X,x,bk,wk)) return 0;   // WTM: BK may not be in check
  return 1;
}
static Tab solve(int X, Tab *sub){
  Tab T; for(int s=0;s<2;s++){ T.d[s]=malloc(NIDX*sizeof(short)); for(int i=0;i<NIDX;i++) T.d[s][i]=-1; }
  char *lg[2]; for(int s=0;s<2;s++){ lg[s]=calloc(NIDX,1);
    for(int wk=0;wk<64;wk++)for(int x=0;x<64;x++)for(int bk=0;bk<64;bk++) lg[s][idx(wk,x,bk)]=islegal(X,s,wk,x,bk); }
  // ply 0: mates
  for(int wk=0;wk<64;wk++)for(int x=0;x<64;x++)for(int bk=0;bk<64;bk++){ int i=idx(wk,x,bk); if(!lg[1][i])continue;
    int chk=attacks(X,x,bk,wk), nm=0;
    for(int k=0;k<nkn[bk]&&!nm;k++){ int s=kn[bk][k]; if(s==wk||adj(wk,s))continue; if(s==x){nm=1;break;} if(attacks(X,x,s,wk))continue; nm=1; }
    if(!nm && chk) T.d[1][i]=0; }
  // promotion successors for pawns are treated as constants looked up on demand
  int lastch=0;
  for(int p=1;p<400;p++){
    int changed=0;
    if(p&1){ // white to move positions: win in p plies if a successor BTM position has depth <= p-1 (and is a win)
      for(int wk=0;wk<64;wk++)for(int x=0;x<64;x++)for(int bk=0;bk<64;bk++){ int i=idx(wk,x,bk); if(!lg[0][i]||T.d[0][i]>=0)continue;
        int ok=0;
        for(int k=0;k<nkn[wk]&&!ok;k++){ int s=kn[wk][k]; if(s==x||s==bk||adj(s,bk))continue; short dd=T.d[1][idx(s,x,bk)]; if(dd>=0&&dd<=p-1)ok=1; }
        if(!ok){
          if(X==P){ int r=x>>3,f=x&7; int t1=x+8;
            if(t1!=wk&&t1!=bk){ if(r==6){ // promotion
                  for(int pt=0;pt<4&&!ok;pt++){ short dd=sub[pt].d[1][idx(wk,t1,bk)]; if(dd>=0&&dd<=p-1)ok=1; }
                } else { short dd=T.d[1][idx(wk,t1,bk)]; if(dd>=0&&dd<=p-1)ok=1;
                  if(!ok&&r==1){ int t2=x+16; if(t2!=wk&&t2!=bk){ dd=T.d[1][idx(wk,t2,bk)]; if(dd>=0&&dd<=p-1)ok=1; } } } }
            (void)f;
          } else {
            int d0=0,d1=8; if(X==R)d1=4; else if(X==B)d0=4;
            if(X==N){ for(int k=0;k<nnt[x]&&!ok;k++){ int t=nt[x][k]; if(t==wk||t==bk)continue; short dd=T.d[1][idx(wk,t,bk)]; if(dd>=0&&dd<=p-1)ok=1; } }
            else for(int d=d0;d<d1&&!ok;d++) for(int k=0;k<raylen[x][d];k++){ int t=ray[x][d][k]; if(t==wk||t==bk)break; short dd=T.d[1][idx(wk,t,bk)]; if(dd>=0&&dd<=p-1){ok=1;break;} }
          } }
        if(ok){ T.d[0][i]=p; changed=1; } }
    } else { // black to move: win when every legal move leads to a white-to-move win of depth <= p-1 (captures are draws)
      for(int wk=0;wk<64;wk++)for(int x=0;x<64;x++)for(int bk=0;bk<64;bk++){ int i=idx(wk,x,bk); if(!lg[1][i]||T.d[1][i]>=0)continue;
        int nm=0, allwin=1;
        for(int k=0;k<nkn[bk];k++){ int s=kn[bk][k]; if(s==wk||adj(wk,s))continue;
          if(s==x){ nm++; allwin=0; break; }
          if(attacks(X,x,s,wk))continue; nm++;
          short dd=T.d[0][idx(wk,x,s)]; if(!(dd>=0&&dd<=p-1)){allwin=0;break;} }
        if(nm>0&&allwin){ T.d[1][i]=p; changed=1; } }
    }
    if(changed) lastch=p; else if(p-lastch>80) break;
  }
  for(int s=0;s<2;s++) free(lg[s]);
  return T;
}
static void stats(const char*name,int X,Tab *T){
  long lg[2]={0,0}, w[2]={0,0}; int mx[2]={0,0};
  for(int s=0;s<2;s++) for(int wk=0;wk<64;wk++)for(int x=0;x<64;x++)for(int bk=0;bk<64;bk++){ int i=idx(wk,x,bk);
    if(!islegal(X,s,wk,x,bk))continue; lg[s]++; short d=T->d[s][i]; if(d>=0){w[s]++; if(d>mx[s])mx[s]=d;} }
  printf("%s %s: WTM legal %ld wins %ld (%.4f%%) longest %d moves | BTM legal %ld wins %ld (%.4f%%) longest %d plies\n",
    name, wrapf?"cyl ":"flat", lg[0], w[0], 100.0*w[0]/lg[0], (mx[0]+1)/2, lg[1], w[1], 100.0*w[1]/lg[1], mx[1]);
}
int main(int argc,char**argv){
  static Tab flat[5], cyl[5]; const char *nm[5]={"KQK","KRK","KBK","KNK","KPK"};
  for(int wr=0;wr<2;wr++){ wrapf=wr; init(); Tab *tt=wr?cyl:flat;
    for(int X=0;X<4;X++){ tt[X]=solve(X,NULL); stats(nm[X],X,&tt[X]); }
    tt[P]=solve(P,tt); stats(nm[P],P,&tt[P]);
  }
  // KPK flat vs cylinder comparison on positions legal on both boards
  long a_d2w[2]={0,0}, a_w2d[2]={0,0}; long zug[2]={0,0}, both[2]={0,0};
  for(int s=0;s<2;s++) for(int wk=0;wk<64;wk++)for(int x=0;x<64;x++)for(int bk=0;bk<64;bk++){
    int i=idx(wk,x,bk); int lf,lc;
    wrapf=0; init(); lf=islegal(P,s,wk,x,bk); wrapf=1; init(); lc=islegal(P,s,wk,x,bk);
    if(lf&&lc){ both[s]++; int wf=flat[P].d[s][i]>=0, wc=cyl[P].d[s][i]>=0; if(!wf&&wc)a_d2w[s]++; if(wf&&!wc)a_w2d[s]++; } }
  printf("KPK positions legal on both boards: WTM %ld BTM %ld\n",both[0],both[1]);
  printf("flat draw -> cyl win: WTM %ld BTM %ld total %ld\n",a_d2w[0],a_d2w[1],a_d2w[0]+a_d2w[1]);
  printf("flat win -> cyl draw: WTM %ld BTM %ld total %ld\n",a_w2d[0],a_w2d[1],a_w2d[0]+a_w2d[1]);
  // mutual zugzwangs per board: WTM not a win, BTM same placement a win
  for(int wr=0;wr<2;wr++){ wrapf=wr; init(); Tab *tt=wr?cyl:flat; long z=0;
    for(int wk=0;wk<64;wk++)for(int x=0;x<64;x++)for(int bk=0;bk<64;bk++){ int i=idx(wk,x,bk);
      if(islegal(P,0,wk,x,bk)&&islegal(P,1,wk,x,bk)&&tt[P].d[0][i]<0&&tt[P].d[1][i]>=0) z++; }
    printf("KPK mutual zugzwangs %s: %ld\n",wr?"cyl":"flat",z); }
  // rook-pawn position Ka6 Pa5 vs Ka8 : wk=a6 (r5,f0)=40, pawn a5 (r4,f0)=32, bk=a8=56
  for(int wr=0;wr<2;wr++){ wrapf=wr; init(); Tab *tt=wr?cyl:flat; int i=idx(40,32,56);
    printf("Ka6 Pa5 vs Ka8 %s: WTM depth %d  BTM depth %d (-1 = not a win)\n",wr?"cyl":"flat",tt[P].d[0][i],tt[P].d[1][i]); }
  return 0;
}
