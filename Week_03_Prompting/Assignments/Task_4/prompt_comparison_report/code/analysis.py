import csv,json,collections,db,solver
rows=list(csv.DictReader(open('restaurants_dataset.csv',encoding='utf-8')))
c=db.conn()
gold=[collections.Counter(map(tuple,json.loads(r['result']))) for r in rows]
parsed=[solver.parse(r['question']) for r in rows]
def score(fn):
    ok=[]
    for f,g in zip(parsed,gold):
        try: got=collections.Counter(c.execute(fn(f)).fetchall())
        except Exception: return None
        ok.append(got==g)
    return ok
def as_city(f):
    if f and 'region' in f: f=dict(f); f['city']=f.pop('region')
    return solver.sql(f)
def order_limit(f):
    if f and f.get('best'):
        s=solver.sql(f,best=False); return s+" ORDER BY R.RATING DESC LIMIT 1"
    return solver.sql(f)
def r_city(f): return solver.sql(f,city_col='R')
variants={
 'Reference (all conventions)':lambda f: solver.sql(f),
 'City on R.CITY_NAME':r_city,
 'Region joined via L.CITY_NAME':lambda f: solver.sql(f,region_key='L'),
 'RATING >= instead of >':lambda f: solver.sql(f,op='>='),
 'SELECT DISTINCT':lambda f: solver.sql(f,distinct=True),
 '"best" as ORDER BY … LIMIT 1':order_limit,
 '"best" ignored (no MAX subquery)':lambda f: solver.sql(f,best=False),
 '"in the X" treated as city':as_city,
 'Return nothing (WHERE 0 everywhere)':lambda f: solver.sql(None),
}
res={}
for k,fn in variants.items():
    o=score(fn); res[k]=o
    print(f"{k:40s} {sum(o)}/155  {sum(o)/155:.2%}")
json.dump({k:v for k,v in res.items()},open('ablation.json','w'))
# features
feat=[]
for r,f,g in zip(rows,parsed,gold):
    q=r['question']; cl=solver.clause(q) or ''
    feat.append(dict(
      noisy = len(q.strip()) > len(cl.strip())+3,
      best = bool(f and f.get('best')),
      rating = bool(f and 'rating' in f),
      region = bool(f and 'region' in f),
      street = bool(f and 'street' in f),
      wherename = bool(f and 'name' in f),
      empty = sum(g.values())==0,
      size = sum(g.values()), qlen=len(q), none=f is None))
json.dump(feat,open('features.json','w'))
for k in ['noisy','best','rating','region','street','wherename','empty','none']:
    print(k, sum(x[k] for x in feat))
import statistics
print('qlen mean noisy/clean', statistics.mean(x['qlen'] for x in feat if x['noisy']), statistics.mean(x['qlen'] for x in feat if not x['noisy']))
print('size buckets', collections.Counter('0' if x['size']==0 else '1' if x['size']==1 else '2-10' if x['size']<=10 else '11-100' if x['size']<=100 else '>100' for x in feat))
print('total gold rows', sum(x['size'] for x in feat))
