import re, csv, json, collections
csv.field_size_limit(10**9)
START = re.compile(r"\b(what is|what are|where is|where are|where can|give me)\b", re.I)
END = re.compile(r"(\?|,\s*(and|while|though|but|or)\b|\.\s+(?=[A-Z])|, I\b|; )")
NOISE_HINTS = re.compile(r"\b(I|My|my|wonder|whether|dilemma|picnic|snacks?)\b")

def clause(q):
    cands=[]
    for m in START.finditer(q):
        rest=q[m.start():]
        e=END.search(rest)
        c=rest[:e.start()] if e else rest
        if re.search(r"\b(restaurant|place|eat|best|in|on)\b", c): cands.append(c)
    return cands[0].strip() if cands else None

def esc(s): return s.replace("'","''")

def parse(q):
    c=clause(q)
    if c is None: return None
    c=c.lower().strip()
    f={}
    m=re.search(r"with a rating above ([\d.]+)(\s*\([^)]*\))?", c)
    if m: f['rating']=m.group(1); c=c[:m.start()]+c[m.end():]
    best = c.startswith('what is the best') or ' the best ' in c
    f['best']=best
    m=re.match(r"where is (?!a |some )(.+?) in (?!the )(.+)$", c.strip())
    if m and not best:
        f['name']=m.group(1); f['city']=m.group(2).strip(); return f
    # location
    m=re.search(r" on (.+?) in (?!the )(.+?)(?= for | with |$)", c)
    if m: f['street']=m.group(1); f['city']=m.group(2).strip(); c=c[:m.start()]+' '+c[m.end():]
    else:
        m=re.search(r" in the (.+?)(?= for | with |$)", c)
        if m: f['region']=m.group(1).strip(); c=c[:m.start()]+' '+c[m.end():]
        else:
            m=re.search(r" in (.+?)(?= for | with |$)", c)
            if m: f['city']=m.group(1).strip(); c=c[:m.start()]+' '+c[m.end():]
            else:
                m=re.search(r" on (.+?)(?= for | with |$)", c)
                if m: f['street']=m.group(1).strip(); c=c[:m.start()]+' '+c[m.end():]
    c=re.sub(r"\s+"," ",c).strip()
    pats=[r"for (.+?) food", r"eat (?:some )?(.+?) food", r"places for (.+)$", r"best place for (.+?) food",
          r"(?:a|some) (.+?) restaurants?$", r"(?:a|some) (.+?) restaurants? ", r"best (?!place)(.+?)$", r"where is a (.+?)$"]
    for p in pats:
        m=re.search(p,c)
        if m:
            v=m.group(1).strip()
            if v not in ('restaurant','restaurants','place','places'): f['food']=v
            break
    return f

def sql(f, city_col='L', region_key='R', op='>', distinct=False, best=True):
    if f is None:
        return "SELECT L.HOUSE_NUMBER, R.NAME FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID WHERE 0"
    frm="FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID"
    w=[]
    if 'region' in f:
        frm+=f" JOIN GEOGRAPHIC G ON {region_key}.CITY_NAME = G.CITY_NAME"; w.append(f"G.REGION = '{esc(f['region'])}'")
    if 'city' in f: w.append(f"{city_col}.CITY_NAME = '{esc(f['city'])}'")
    if 'street' in f: w.append(f"L.STREET_NAME = '{esc(f['street'])}'")
    if 'food' in f: w.append(f"R.FOOD_TYPE = '{esc(f['food'])}'")
    if 'name' in f: w.append(f"R.NAME = '{esc(f['name'])}'")
    if 'rating' in f: w.append(f"R.RATING {op} {f['rating']}")
    where=(" WHERE "+" AND ".join(w)) if w else ""
    s=f"SELECT {'DISTINCT ' if distinct else ''}L.HOUSE_NUMBER, R.NAME {frm}{where}"
    if f.get('best') and best:
        s+=(" AND " if w else " WHERE ")+f"R.RATING = (SELECT MAX(R.RATING) {frm}{where})"
    return s
