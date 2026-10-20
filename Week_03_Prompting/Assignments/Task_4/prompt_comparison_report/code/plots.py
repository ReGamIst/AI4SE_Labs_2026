import json, math, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import binomtest
S='#fcfcfb'; T1='#0b0b0b'; T2='#52514e'; GRID='#e4e3df'; GRAY='#9a9893'
C={'ICIO':'#2a78d6','TRACE':'#eb6834','ReAct':'#1baf7a'}
plt.rcParams.update({'figure.facecolor':S,'axes.facecolor':S,'axes.edgecolor':GRID,'axes.labelcolor':T2,
 'xtick.color':T2,'ytick.color':T2,'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
 'axes.grid':True,'grid.color':GRID,'grid.linewidth':0.8,'axes.axisbelow':True,'text.color':T1})
def wilson(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return c-h,c+h
def title(ax,t,s=None):
    ax.set_title(t,loc='left',fontsize=12,fontweight='bold',color=T1,pad=18 if s else 8)
    if s: ax.text(0,1.02,s,transform=ax.transAxes,fontsize=9,color=T2)

# 1 accuracy
items=[('ICIO prompt',154,C['ICIO']),('TRACE prompt',154,C['TRACE']),('ReAct prompt',154,C['ReAct']),
       ('Rule-based reference solver',154,GRAY),('Regex generator (from prompt design)',151,GRAY),
       ('Empty result for every question',43,GRAY)]
fig,ax=plt.subplots(figsize=(8,3.6))
for i,(n_,k,c) in enumerate(items[::-1]):
    lo,hi=wilson(k,155); p=k/155
    ax.plot([lo*100,hi*100],[i,i],color=c,lw=2,solid_capstyle='round')
    ax.plot(p*100,i,'o',ms=8,color=c,mec=S,mew=2)
    ax.text(hi*100+0.8,i,f'{k}/155 = {p:.2%}',va='center',fontsize=9,color=T1)
ax.set_yticks(range(len(items))); ax.set_yticklabels([x[0] for x in items[::-1]])
ax.set_xlim(20,108); ax.set_ylim(-1.1,len(items)-0.5); ax.set_xlabel('Execution accuracy, % (bars: 95% Wilson interval)'); ax.grid(axis='y',visible=False)
ax.axvline(154/155*100,color=GRAY,lw=1,ls=':'); ax.text(154/155*100-0.8,-0.85,'ceiling 154/155',fontsize=8,color=T2,ha='right')
title(ax,'All three prompts land on the same 154/155','Accuracy and 95% CI vs. reference points on the same 155 questions')
fig.tight_layout(); fig.savefig('report/figures/fig1_accuracy.png',dpi=160); plt.close()

# 2 cost: two panels, no dual axis
fig,axs=plt.subplots(1,3,figsize=(10,3.3))
names=['TRACE','ReAct','ICIO']; tm=[40,70,120]; tok=[1,2.5,5]
for ax,vals,lab,fmt,tt in [(axs[0],tm,'Wall-clock time, s','{:.0f} s','Time to finish'),(axs[1],tok,'Tokens, relative to TRACE','{:g}×','Token usage (approx.)'),
                           (axs[2],[99.35/t for t in tok],'Accuracy points per token unit','{:.1f}','Accuracy per token unit')]:
    b=ax.bar(names,vals,color=[C[n] for n in names],width=0.6)
    for r,v in zip(b,vals): ax.text(r.get_x()+r.get_width()/2,v,fmt.format(v),ha='center',va='bottom',fontsize=9,color=T1)
    ax.set_ylabel(lab); ax.grid(axis='x',visible=False); ax.set_title(tt,loc='left',fontsize=11,fontweight='bold'); ax.margins(y=0.15)
fig.suptitle('Same accuracy, very different cost (single run per prompt)',x=0.01,ha='left',fontsize=12,fontweight='bold')
fig.tight_layout(); fig.savefig('report/figures/fig2_cost.png',dpi=160); plt.close()

# 3 ablation
ab=json.load(open('ablation.json'))
ref=sum(ab['Reference (all conventions)'])
rows=[(k,ref-sum(v)) for k,v in ab.items() if k not in('Reference (all conventions)','Return nothing (WHERE 0 everywhere)')]
rows.sort(key=lambda x:x[1])
fig,ax=plt.subplots(figsize=(8,3.6))
b=ax.barh([r[0] for r in rows],[r[1] for r in rows],color=GRAY,height=0.6)
for r,(k,v) in zip(b,rows): ax.text(v+0.5,r.get_y()+r.get_height()/2,f'−{v} questions ({v/155:.1%})' if v else '0 — no effect on this dataset',va='center',fontsize=9)
ax.set_xlabel('Questions lost vs. the 154/155 reference when one convention is broken'); ax.grid(axis='y',visible=False); ax.set_xlim(0,56)
title(ax,'What each convention in the prompts is worth','Every one of these rules appears in all three prompts')
fig.tight_layout(); fig.savefig('report/figures/fig3_ablation.png',dpi=160); plt.close()

# 4 mcnemar
ks=list(range(0,11)); ps=[1.0 if k==0 else binomtest(k,k,0.5).pvalue for k in ks]
fig,ax=plt.subplots(figsize=(8,3.4))
ax.plot(ks,ps,'-o',color=C['ICIO'],lw=2,ms=7,mec=S,mew=2)
ax.axhline(0.05,color=T2,lw=1,ls='--'); ax.text(10,0.055,'α = 0.05',ha='right',fontsize=8,color=T2)
ax.axhline(0.05/3,color=T2,lw=1,ls=':'); ax.text(10,0.02,'α = 0.0167 (Bonferroni, 3 pairs)',ha='right',fontsize=8,color=T2)
ax.axvspan(-0.3,1.3,color='#eda100',alpha=0.15,lw=0); ax.text(0.5,0.25,'reachable here\n(max 1 item of headroom)',ha='center',fontsize=8,color=T1)
ax.set_yscale('log'); ax.set_xticks(ks); ax.set_xlabel('Questions one prompt solves and the other does not (with no reverse cases)')
ax.set_ylabel('Exact McNemar p-value'); ax.grid(axis='x',visible=False)
title(ax,'A significant difference would need ≥ 6 one-sided wins','Exact two-sided McNemar test, n = 155 paired questions')
fig.tight_layout(); fig.savefig('report/figures/fig4_mcnemar.png',dpi=160); plt.close()

# 5 dataset
feat=json.load(open('features.json'))
fig,axs=plt.subplots(1,2,figsize=(10,3.5))
bk=['0','1','2–10','11–100','>100']
def bucket(s): return '0' if s==0 else '1' if s==1 else '2–10' if s<=10 else '11–100' if s<=100 else '>100'
cnt=[sum(1 for f in feat if bucket(f['size'])==b) for b in bk]
b=axs[0].bar(bk,cnt,color=GRAY,width=0.6)
for r,v in zip(b,cnt): axs[0].text(r.get_x()+r.get_width()/2,v,str(v),ha='center',va='bottom',fontsize=9)
axs[0].set_xlabel('Rows in the gold result'); axs[0].set_ylabel('Questions'); axs[0].grid(axis='x',visible=False); axs[0].margins(y=0.15)
axs[0].set_title('70% of answers have 0 or 1 row',loc='left',fontsize=11,fontweight='bold')
lab=[('rating','"rating above N"'),('street','Street filter'),('noisy','Noise-wrapped'),('region','Region ("in the X")'),('best','"best …"'),('wherename','"where is NAME"'),('none','No request')]
v=[sum(f[k] for f in feat) for k,_ in lab]
b=axs[1].barh([l for _,l in lab][::-1],v[::-1],color=GRAY,height=0.6)
for r,x in zip(b,v[::-1]): axs[1].text(x+1,r.get_y()+r.get_height()/2,str(x),va='center',fontsize=9)
axs[1].set_xlabel('Questions containing the feature (overlapping)'); axs[1].grid(axis='y',visible=False); axs[1].set_xlim(0,125)
axs[1].set_title('Question features',loc='left',fontsize=11,fontweight='bold')
fig.tight_layout(); fig.savefig('report/figures/fig5_dataset.png',dpi=160); plt.close()
print('done')
