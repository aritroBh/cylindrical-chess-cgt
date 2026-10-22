// Independent verifier: K + two opposite-coloured bishops vs K, 8x8, flat or cylinder (files wrapped).
#include <stdio.h>
#include <stdlib.h>
static int wrapf;
static int kn[64][8], nkn[64], ray[64][4][8], raylen[64][4];
static const int dr[4]={1,1,-1,-1}, df[4]={1,-1,1,-1};
static int dark[32], light[32], ndk=0, nlt=0, ci[64]; // compact index of a bishop square within its colour
static void init(void){
  ndk=nlt=0;
  for(int s=0;s<64;s++){ int r=s>>3,f=s&7; nkn[s]=0;
    if(((r+f)&1)==0){ ci[s]=ndk; dark[ndk++]=s; } else { ci[s]=nlt; light[nlt++]=s; }
    for(int a=-1;a<=1;a++)for(int b=-1;b<=1;b++){ if(!a&&!b)continue; int r2=r+a,f2=f+b; if(r2<0||r2>7)continue;
      if(wrapf) f2=(f2+8)&7; else if(f2<0||f2>7)continue; kn[s][nkn[s]++]=r2*8+f2; }
    for(int d=0;d<4;d++){ raylen[s][d]=0; int rr=r,ff=f;
      for(int k=0;k<8;k++){ rr+=dr[d]; ff+=df[d]; if(rr<0||rr>7)break; if(wrapf) ff=(ff+8)&7; else if(ff<0||ff>7)break;
        ray[s][d][raylen[s][d]++]=rr*8+ff; } } }
}
static int adj(int a,int b){ for(int i=0;i<nkn[a];i++) if(kn[a][i]==b) return 1; return 0; }
static int attacks(int bs,int t,int b1,int b2){ // bishop on bs attacks t, blockers b1,b2 (squares)
  for(int d=0;d<4;d++) for(int k=0;k<raylen[bs][d];k++){ int s=ray[bs][d][k]; if(s==t) return 1; if(s==b1||s==b2) break; }
  return 0; }
#define IDX(wk,a,b,bk) ((((wk)*32+(a))*32+(b))*64+(bk))
#define NI (64*32*32*64)
static int legal(int stm,int wk,int A,int Bq,int bk){ // A: dark bishop square, Bq: light bishop square
  if(wk==A||wk==Bq||wk==bk||A==bk||Bq==bk) return 0; if(adj(wk,bk)) return 0;
  if(stm==0){ if(attacks(A,bk,wk,Bq)||attacks(Bq,bk,wk,A)) return 0; }
  return 1; }
int main(void){
  for(wrapf=0;wrapf<2;wrapf++){
    init();
    short *d[2]; for(int s=0;s<2;s++){ d[s]=malloc(NI*sizeof(short)); for(int i=0;i<NI;i++) d[s][i]=-1; }
    long lg[2]={0,0};
    for(int wk=0;wk<64;wk++)for(int a=0;a<32;a++)for(int b=0;b<32;b++)for(int bk=0;bk<64;bk++){
      int A=dark[a],Bq=light[b]; for(int s=0;s<2;s++) if(legal(s,wk,A,Bq,bk)) lg[s]++; }
    // mates
    for(int wk=0;wk<64;wk++)for(int a=0;a<32;a++)for(int b=0;b<32;b++)for(int bk=0;bk<64;bk++){
      int A=dark[a],Bq=light[b]; if(!legal(1,wk,A,Bq,bk))continue;
      int chk=attacks(A,bk,wk,Bq)||attacks(Bq,bk,wk,A); if(!chk)continue; int nm=0;
      for(int k=0;k<nkn[bk]&&!nm;k++){ int s=kn[bk][k]; if(s==wk||adj(wk,s))continue;
        if(s==A){ if(!attacks(Bq,s,wk,-1)){nm=1;} continue; }  // capture of A allowed only if B does not protect it
        if(s==Bq){ if(!attacks(A,s,wk,-1)){nm=1;} continue; }
        if(attacks(A,s,wk,Bq)||attacks(Bq,s,wk,A))continue; nm=1; }
      if(!nm) d[1][IDX(wk,a,b,bk)]=0; }
    int lastch=0;
    for(int p=1;p<400;p++){ int changed=0;
      if(p&1){
        for(int wk=0;wk<64;wk++)for(int a=0;a<32;a++)for(int b=0;b<32;b++)for(int bk=0;bk<64;bk++){
          int i=IDX(wk,a,b,bk); if(d[0][i]>=0)continue; int A=dark[a],Bq=light[b]; if(!legal(0,wk,A,Bq,bk))continue; int ok=0;
          for(int k=0;k<nkn[wk]&&!ok;k++){ int s=kn[wk][k]; if(s==A||s==Bq||s==bk||adj(s,bk))continue; short dd=d[1][IDX(s,a,b,bk)]; if(dd>=0&&dd<=p-1)ok=1; }
          for(int dir=0;dir<4&&!ok;dir++) for(int k=0;k<raylen[A][dir];k++){ int t=ray[A][dir][k]; if(t==wk||t==Bq||t==bk)break;
            short dd=d[1][IDX(wk,ci[t],b,bk)]; if(dd>=0&&dd<=p-1){ok=1;break;} }
          for(int dir=0;dir<4&&!ok;dir++) for(int k=0;k<raylen[Bq][dir];k++){ int t=ray[Bq][dir][k]; if(t==wk||t==A||t==bk)break;
            short dd=d[1][IDX(wk,a,ci[t],bk)]; if(dd>=0&&dd<=p-1){ok=1;break;} }
          if(ok){ d[0][i]=p; changed=1; } }
      } else {
        for(int wk=0;wk<64;wk++)for(int a=0;a<32;a++)for(int b=0;b<32;b++)for(int bk=0;bk<64;bk++){
          int i=IDX(wk,a,b,bk); if(d[1][i]>=0)continue; int A=dark[a],Bq=light[b]; if(!legal(1,wk,A,Bq,bk))continue;
          int nm=0, allwin=1;
          for(int k=0;k<nkn[bk];k++){ int s=kn[bk][k]; if(s==wk||adj(wk,s))continue;
            if(s==A){ if(attacks(Bq,s,wk,-1))continue; nm++; allwin=0; break; }   // unprotected capture -> KBK draw
            if(s==Bq){ if(attacks(A,s,wk,-1))continue; nm++; allwin=0; break; }
            if(attacks(A,s,wk,Bq)||attacks(Bq,s,wk,A))continue; nm++;
            short dd=d[0][IDX(wk,a,b,s)]; if(!(dd>=0&&dd<=p-1)){allwin=0;break;} }
          if(nm>0&&allwin){ d[1][i]=p; changed=1; } }
      }
      if(changed) lastch=p; else if(p-lastch>80) break; }
    long w[2]={0,0}; int mx[2]={0,0};
    for(int wk=0;wk<64;wk++)for(int a=0;a<32;a++)for(int b=0;b<32;b++)for(int bk=0;bk<64;bk++){ int A=dark[a],Bq=light[b];
      for(int s=0;s<2;s++) if(legal(s,wk,A,Bq,bk)){ short x=d[s][IDX(wk,a,b,bk)]; if(x>=0){w[s]++; if(x>mx[s])mx[s]=x;} } }
    printf("KBBK(opposite colours) %s: WTM legal %ld wins %ld (%.4f%%) longest %d moves; BTM legal %ld wins %ld longest %d plies\n",
      wrapf?"cyl ":"flat",lg[0],w[0],100.0*w[0]/lg[0],(mx[0]+1)/2,lg[1],w[1],mx[1]);
    for(int s=0;s<2;s++) free(d[s]);
  }
  return 0; }
