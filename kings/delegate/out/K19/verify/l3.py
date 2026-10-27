from lg import *
class G3(Game):
    def l3D(self, st, t):
        """D (real, no passes) to move, A has t moves left. exists-guided-strategy semantics evaluated at A nodes."""
        key=('L3D',st,t)
        if key in self.memo: return self.memo[key]
        D=self.D
        ms=self.moves(D,st)
        chk=self.in_check(D,st)
        if not ms:
            return self._s(key, chk)      # mate: fine; stalemate: violates L3
        for ns,kind,q in ms:
            if kind=='promo': return self._s(key, False)  # cannot happen when local win guaranteed
            if not self.l3A(ns,t): return self._s(key, False)
        return self._s(key, True)
    def l3A(self,st,t):
        key=('L3A',st,t)
        if key in self.memo: return self.memo[key]
        A=self.A
        if t<=0: return self._s(key, False)
        for ns,kind,q in self.moves(A,st,confineK=self.confine):
            if kind=='promo':
                if (not self.queen) or self.queen_safe(ns,q): return self._s(key, True)
                continue
            if self.mate and self.in_check(self.D,ns) and not self.moves(self.D,ns): return self._s(key, True)
            # guided: ns must be a winning move of the local game (with passes) with t-1 left
            if not self.winD(ns,t-1,None): continue
            if self.l3D(ns,t-1): return self._s(key, True)
        return self._s(key, False)
if __name__=='__main__':
    for q in (True,False):
        out=[]
        for sq in ('g4','g5','g6','h6','a6'):
            G=G3(8,8,True,'b',{7,0,1},queen=q)
            st=parse(f'K{sq} ka4 pa5'); T=G.T(st,None,12)
            out.append((T,[G.l3D(st,T+d) for d in (0,1,2)]))
        print('White sorties queen=%s'%q,out)
        out=[]
        for sq in ('a3','b3','c3','c4','c5'):
            G=G3(8,8,True,'w',{7,0,1},queen=q)
            st=parse(f'Ka5 Pa4 k{sq}'); T=G.T(st,None,12)
            out.append((T,[G.l3D(st,T+d) for d in (0,1,2)]))
        print('Black sorties queen=%s'%q,out)
