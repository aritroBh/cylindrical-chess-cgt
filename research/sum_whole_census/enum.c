// enumerate passer-free positions (textbook test, no e.p. right at root), flat board width w, ranks 2..7,
// total pawns <= nmax; print canonical reps (min over mirror x colour-swap) with exactly n pawns.
// output line: "a2 b3 / ..." encoded as W:<sq list> B:<sq list>, square = file letter + rank
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int w, nmax, nsel;
int cell[8][9]; // [file][rank] 0 empty 1 W 2 B
long cnt=0;
int passed(int side){
  for(int f=0;f<w;f++)for(int r=2;r<=7;r++) if(cell[f][r]==side){
    int blocked=0;
    for(int g=f-1;g<=f+1&&!blocked;g++){ if(g<0||g>=w)continue;
      if(side==1){for(int s=r+1;s<=7;s++) if(cell[g][s]==2){blocked=1;break;}}
      else {for(int s=2;s<r;s++) if(cell[g][s]==1){blocked=1;break;}}
    }
    if(!blocked) return 1;
  }
  return 0;
}
// encode as base-3 vector in fixed order; image: mirror f->w-1-f ; colour swap: r->9-r, W<->B
static long enc(int mir,int swp){
  long e=0;
  for(int f=0;f<w;f++)for(int r=2;r<=7;r++){
    int ff=mir? w-1-f:f; int rr=swp?9-r:r; int c=cell[ff][rr];
    if(swp&&c) c=3-c;
    e=e*3+c;
  }
  return e;
}
void emit(){
  if(passed(1)||passed(2)) return;
  long e0=enc(0,0);
  if(enc(1,0)<e0||enc(0,1)<e0||enc(1,1)<e0) return;
  // orbit size
  int orb=1; long im[4]={enc(0,0),enc(1,0),enc(0,1),enc(1,1)};
  int distinct=0; for(int i=0;i<4;i++){int d=1;for(int j=0;j<i;j++)if(im[j]==im[i])d=0; distinct+=d;}
  printf("%d ",distinct);
  printf("W:");for(int f=0;f<w;f++)for(int r=2;r<=7;r++)if(cell[f][r]==1)printf(" %c%d",'a'+f,r);
  printf(" / B:");for(int f=0;f<w;f++)for(int r=2;r<=7;r++)if(cell[f][r]==2)printf(" %c%d",'a'+f,r);
  printf("\n");
}
void rec(int idx,int k){
  if(k==nsel){emit();return;}
  if(idx==w*6) return;
  if(w*6-idx < nsel-k) return;
  int f=idx/6, r=idx%6+2;
  rec(idx+1,k);
  cell[f][r]=1; rec(idx+1,k+1);
  cell[f][r]=2; rec(idx+1,k+1);
  cell[f][r]=0;
}
int main(int c,char**v){w=atoi(v[1]);nsel=atoi(v[2]);memset(cell,0,sizeof cell);rec(0,0);return 0;}
