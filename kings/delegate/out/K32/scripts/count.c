/* K32 helper: count BFS-canonical rooted stopper graphs on exactly n nodes (all nodes reachable from node 0). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n;
static uint8_t Lm[8], Rm[8];
static long cnt=0, nodes_visited=0;
static int acyclic(int upto){ /* states (i,0=L-to-move),(i,1=R); successors via Lm / Rm of processed nodes */
  int alive[16]; int na=0; for(int s=0;s<2*upto;s++) alive[s]=1; na=2*upto;
  int changed=1;
  while(changed&&na){ changed=0;
    for(int s=0;s<2*upto;s++) if(alive[s]){ int i=s>>1,m=s&1; uint8_t o=m?Rm[i]:Lm[i]; int has=0;
      for(int j=0;j<upto;j++) if((o>>j&1) && alive[2*j+(1-m)]){has=1;break;}
      if(!has){alive[s]=0;na--;changed=1;} } }
  return na==0;
}
static void rec(int i,int k){
  if(i==n){ if(k==n) cnt++; return; }
  if(i>=k) return;
  int maxnew=n-k;
  for(int t=0;t<=maxnew;t++){
    uint32_t newmask=((1u<<t)-1)<<k; int k1=k+t;
    for(uint32_t old=0; old<(1u<<k); old++){
      Lm[i]=(uint8_t)(old|newmask);
      int maxnew2=n-k1;
      for(int t2=0;t2<=maxnew2;t2++){
        uint32_t nm2=((1u<<t2)-1)<<k1; int k2=k1+t2;
        for(uint32_t old2=0; old2<(1u<<k1); old2++){
          Rm[i]=(uint8_t)(old2|nm2);
          nodes_visited++;
          if(!acyclic(i+1)) continue;
          rec(i+1,k2);
        }
      }
    }
  }
}
int main(int argc,char**argv){ n=atoi(argv[1]); rec(0,1); printf("n=%d canonical-ish rooted stopper graphs: %ld (visited %ld)\n",n,cnt,nodes_visited); return 0; }
