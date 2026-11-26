// Finite pawn layers. Within each layer only noncapturing king moves cycle.
#include <algorithm>
#include <array>
#include <map>
#include <memory>
#include <cstdlib>
using namespace std;
namespace {
constexpr int X=64, M=1000;
struct Layer { short d[2][64][64]{}; };
using Key=array<int,4>; // white pawn, sorted black pawns, ep landing square
map<Key,unique_ptr<Layer>> layers;
int adj[65][9];
bool near(int a,int b){return a<X && b<X && max(abs(a/8-b/8),abs(a%8-b%8))<=1;}
bool hit(int p, int k, int dir){return p<X && k<X && k/8==p/8+dir && abs(k%8-p%8)==1;}
bool init=[](){for(int a=0;a<64;a++){int n=0;for(int b=0;b<64;b++)if(a!=b&&near(a,b))adj[a][n++]=b;adj[a][n]=X;}return true;}();
const Layer& solve(int w,int b,int c,int ep){
 if(b>c)swap(b,c);
 Key key{w,b,c,ep}; auto &ptr=layers[key]; if(ptr)return *ptr;
 ptr=make_unique<Layer>(); Layer &l=*ptr;
 // fixed holds the best value available by changing layer, from the mover's perspective
 short fixed[2][64][64]; unsigned long long quiet[2][64][64]{};
 for(int t:{0,1})for(int k=0;k<64;k++)for(int j=0;j<64;j++){
   int a=t?j:k, enemy=t?k:j; // k white king, j black king
   bool check=t?hit(w,j,1):hit(b,k,-1)||hit(c,k,-1);
   int best=-M-1; auto &q=quiet[t][k][j];
   bool valid=!near(k,j)&&k!=w&&k!=b&&k!=c&&j!=w&&j!=b&&j!=c;
   if(valid){
    for(int i=0;adj[a][i]<X;i++){int z=adj[a][i]; if(near(z,enemy))continue;
     if(t?(z==b||z==c||hit(w,z,1)):(z==w||hit(b,z,-1)||hit(c,z,-1)))continue;
     bool cap=t?z==w:(z==b||z==c);
     if(!cap && ep==X)q|=1ULL<<z;
     else {auto &s=solve(t&&z==w?X:w,!t&&z==b?X:b,!t&&z==c?X:c,X);
      best=max(best,-int(s.d[1-t][t?k:z][t?z:j]));}
    }
    int dir=t?-1:1;
    for(int p:{t?b:w,t?c:X})if(p<X){
     auto occupied=[&](int z){return z==w||z==b||z==c||z==k||z==j;};
     for(int dx:{0,-1,1,2}){
      bool dbl=dx==2; int z=p+dir*8+(dbl?0:dx)+(dbl?dir*8:0);
      if(z<0||z>=64||abs(z%8-p%8)>1)continue;
      int removed=X;
      if(dx==0||dbl){if(occupied(z)||(dbl&&(p/8!=(t?6:1)||occupied(p+dir*8))))continue;}
      else {if(z==enemy||z==a)continue;
       removed=(z==ep)?z-dir*8:z;
       if(t?(removed!=w):(removed!=b&&removed!=c))continue;}
      int nw=t?(removed==w?X:w):z;
      int nb=t?(p==b?z:b):(removed==b?X:b), nc=t?(p==c?z:c):(removed==c?X:c);
      if(t?hit(nw,j,1):(hit(nb,k,-1)||hit(nc,k,-1)))continue;
      if(z/8==(t?0:7)){best=M;continue;}
      int e=X;
      if(dbl){int m=p+dir*8; if(t?hit(w,m,1):(hit(b,m,-1)||hit(c,m,-1)))e=m;}
      best=max(best,-int(solve(nw,nb,nc,e).d[1-t][k][j]));
     }
    }
   }
   if(!q && best==-M-1)best=valid&&check?-M-1:0;
   fixed[t][k][j]=best;
 }
 bool changed;
 do{changed=false;
  for(int t:{0,1})for(int k=0;k<64;k++)for(int j=0;j<64;j++){
   int v=fixed[t][k][j]; auto q=quiet[t][k][j];
   while(q){int z=__builtin_ctzll(q);q&=q-1;
    v=max(v,-int(l.d[1-t][t?k:z][t?z:j]));}
   // Checkmate at the root takes zero plies. A promoting move takes one.
   if(v>0)--v;else if(v<0)++v;
   auto &d=l.d[t][k][j];if(d!=v){d=v;changed=true;}
  }
 }while(changed);
 return l;
}
}
extern "C" int val(int t,int k,int j,int w,int b,int c,int ep){return solve(w,b,c,ep).d[t][k][j];}
