/* Independent check (verifier C4): Grundy values of Dawson's chess rows,
   written from the file-push rule, NOT from octal-digit parsing.
   A row of n untouched files; a push on file i (1..n) removes files
   i-1, i, i+1 (those that exist) and leaves rows of lengths L=max(i-2,0)
   and R=max(n-i-1,0).  Also computes Dawson's Kayles (0.07: remove two
   adjacent pins from a row, leaving rows a, b with a+b=m-2) to check the
   shift g_chess(n) = g_kayles(n+1). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 5001
static int gc[MAXN+2], gk[MAXN+3];
static int mex(char *seen, int lim){ int m=0; while(m<lim && seen[m]) m++; return m; }
int main(int argc, char **argv){
  int N = argc>1 ? atoi(argv[1]) : 300;
  if (N > MAXN) N = MAXN;
  char seen[1024];
  gc[0]=0;
  for (int n=1;n<=N;n++){
    memset(seen,0,sizeof seen);
    for (int i=1;i<=n;i++){
      int L = i-2; if (L<0) L=0;
      int R = n-i-1; if (R<0) R=0;
      seen[gc[L]^gc[R]] = 1;
    }
    gc[n]=mex(seen,1024);
  }
  gk[0]=0;
  for (int m=1;m<=N+1;m++){
    memset(seen,0,sizeof seen);
    for (int a=0;a+2<=m;a++){ int b=m-2-a; seen[gk[a]^gk[b]]=1; }
    gk[m]=mex(seen,1024);
  }
  int shift_ok=1;
  for (int n=0;n<=N;n++) if (gc[n]!=gk[n+1]) { shift_ok=0; printf("shift mismatch n=%d\n",n); }
  printf("N=%d shift_ok=%d\n",N,shift_ok);
  int mx=0; for(int n=0;n<=N;n++) if(gc[n]>mx) mx=gc[n];
  printf("max g(0..%d) = %d\n",N,mx);
  printf("g(0..33):"); for(int n=0;n<=33;n++) printf(" %d",gc[n]); printf("\n");
  printf("g(52..85):"); for(int n=52;n<=85;n++) printf(" %d",gc[n]); printf("\n");
  /* exceptions for p=34 */
  printf("n with g(n)!=g(n+34), n+34<=N:");
  for(int n=0;n+34<=N;n++) if(gc[n]!=gc[n+34]) printf(" %d",n);
  printf("\n");
  /* least eventual period: for each p, last n with g(n)!=g(n+p) */
  for (int p=1;p<=68;p++){
    int last=-1; for(int n=0;n+p<=N;n++) if(gc[n]!=gc[n+p]) last=n;
    if (last < N/2) printf("p=%d last exception=%d (data to n+p<=%d)\n",p,last,N);
  }
  /* full listing to a file */
  FILE *f=fopen(argc>2?argv[2]:"/dev/null","w");
  if(f){ for(int n=0;n<=N;n++) fprintf(f,"%d %d\n",n,gc[n]); fclose(f);}  
  return 0;
}
