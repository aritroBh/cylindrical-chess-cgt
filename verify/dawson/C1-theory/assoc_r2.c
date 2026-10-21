/* Full associativity check of a monoid table: (xy)z == x(yz) for all x,y,z.
   cc -O2 -o verify/dawson/C1-theory/assoc_r2 verify/dawson/C1-theory/assoc_r2.c
   verify/dawson/C1-theory/assoc_r2 < verify/dawson/C1-theory/q32_table_r2.txt */
#include <stdio.h>
#include <stdlib.h>
int main(void){int N; if(scanf("%d",&N)!=1) return 1; int *m=malloc(sizeof(int)*N*N);
 for(int i=0;i<N*N;i++) if(scanf("%d",&m[i])!=1) return 1;
 long bad=0; for(int x=0;x<N;x++) for(int y=0;y<N;y++){int xy=m[x*N+y]; for(int z=0;z<N;z++) if(m[xy*N+z]!=m[x*N+m[y*N+z]]) bad++;}
 printf("N=%d triples=%ld associativity failures=%ld\n",N,(long)N*N*N,bad); return 0;}
