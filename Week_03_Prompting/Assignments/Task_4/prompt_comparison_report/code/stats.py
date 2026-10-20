from scipy.stats import binomtest, beta, chi2
import math, json
n=155; k=154
def wilson(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return c-h,c+h
def cp(k,n,a=0.05):
    lo=beta.ppf(a/2,k,n-k+1) if k>0 else 0; hi=beta.ppf(1-a/2,k+1,n-k) if k<n else 1; return lo,hi
print('wilson',wilson(k,n),'cp',cp(k,n))
# McNemar exact
def mcn(b,c):
    if b+c==0: return 1.0
    return binomtest(b,b+c,0.5).pvalue
print('same item',mcn(0,0),'diff item',mcn(1,1))
for b in range(1,10): print('b',b,'c0 p',round(mcn(b,0),4))
# Cochran Q for 3 prompts with identical vectors -> 0/0
# Scenario different failing items: rows sums
def cochranQ(mat):
    k=len(mat[0]); C=[sum(r[j] for r in mat) for j in range(k)]; R=[sum(r) for r in mat]; N=sum(R)
    den=k*N-sum(x*x for x in R)
    if den==0: return float('nan'),float('nan')
    Q=(k-1)*(k*sum(x*x for x in C)-N*N)/den; return Q,1-chi2.cdf(Q,k-1)
import itertools
same=[[1,1,1]]*154+[[0,0,0]]
diff=[[1,1,1]]*152+[[0,1,1],[1,0,1],[1,1,0]]
print('Q same',cochranQ(same),'Q diff',cochranQ(diff))
# unpaired Fisher
from scipy.stats import fisher_exact
print('fisher',fisher_exact([[154,1],[154,1]]))
# Bayesian: Beta(1,1) posterior difference P(theta_A>theta_B)
import numpy as np
rng=np.random.default_rng(0)
a=rng.beta(155,2,200000); b=rng.beta(155,2,200000)
d=a-b; print('post diff 95%',np.percentile(d,[2.5,97.5]),'P>0',(d>0).mean())
# MDE: needed discordant for alpha .05 and Bonferroni .0167
for alpha in (0.05,0.05/3):
    for b in range(1,15):
        if mcn(b,0)<alpha: print('alpha',alpha,'min one-sided discordant',b); break
# headroom
print('headroom items above 154:',155-154)
