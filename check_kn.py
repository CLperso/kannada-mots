import json,re,sys
V={'ಅ':'a','ಆ':'ā','ಇ':'i','ಈ':'ī','ಉ':'u','ಊ':'ū','ಋ':'ṛ','ಎ':'e','ಏ':'ē','ಐ':'ai','ಒ':'o','ಓ':'ō','ಔ':'au'}
S={'ಾ':'ā','ಿ':'i','ೀ':'ī','ು':'u','ೂ':'ū','ೃ':'ṛ','ೆ':'e','ೇ':'ē','ೈ':'ai','ೊ':'o','ೋ':'ō','ೌ':'au'}
C={'ಕ':'k','ಖ':'kh','ಗ':'g','ಘ':'gh','ಙ':'ṅ','ಚ':'ch','ಛ':'chh','ಜ':'j','ಝ':'jh','ಞ':'ñ','ಟ':'ṭ','ಠ':'ṭh','ಡ':'ḍ','ಢ':'ḍh','ಣ':'ṇ','ತ':'t','ಥ':'th','ದ':'d','ಧ':'dh','ನ':'n','ಪ':'p','ಫ':'ph','ಬ':'b','ಭ':'bh','ಮ':'m','ಯ':'y','ರ':'r','ಱ':'r','ಲ':'l','ಳ':'ḷ','ವ':'v','ಶ':'sh','ಷ':'ṣ','ಸ':'s','ಹ':'h'}
def tl(s):
    out='';i=0
    while i<len(s):
        c=s[i]; n=s[i+1] if i+1<len(s) else ''
        if c in C:
            out+=C[c]
            if n=='್': i+=1
            elif n in S: out+=S[n]; i+=1
            else: out+='a'
        elif c in V: out+=V[c]
        elif c=='ಂ':
            nn=C.get(n,''); out+='m' if nn and nn[0] in 'pbm' else 'n'
        else: out+=c
        i+=1
    return out
D={'ā':'a','ī':'i','ū':'u','ē':'e','ō':'o','ṭ':'t','ḍ':'d','ṇ':'n','ḷ':'l','ṣ':'s','ś':'s','ṛ':'r','ṅ':'n','ñ':'n','ḥ':'h','ṁ':'m'}
def norm(s):
    s=s.lower(); s=re.sub(r'\(.*?\)',' ',s).replace('…',' ')
    s=''.join(D.get(ch,ch) for ch in s); s=re.sub('[^a-z]','',s)
    s=s.replace('ee','i').replace('oo','u')
    for h in ['sh','th','dh','bh','ph','kh','gh','ch','jh']: s=s.replace(h,h[0])
    s=s.replace('w','v').replace('z','s'); s=re.sub(r'(.)\1+',r'\1',s); return s
def lev(a,b):
    p=list(range(len(b)+1))
    for i,x in enumerate(a):
        c=[i+1]
        for j,y in enumerate(b): c.append(min(c[j]+1,p[j+1]+1,p[j]+(x!=y)))
        p=c
    return p[-1]
import importlib.util, os
src=sys.argv[1]
if src.endswith('.py'):
    spec=importlib.util.spec_from_file_location('m',src); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    name=[k for k in dir(m) if k.startswith('NIVEAU')][0]
    d=[{'fr':fr,'tr':tr,'kn':kn} for t,items in getattr(m,name) for (fr,tr,kn,note) in items]
else:
    d=json.load(open(src))['words']
bad=0
for w in d:
    if '/' in w['kn'] or re.search('[A-Z]',w['tr']): continue
    a=norm(tl(w['kn'])); b=norm(w['tr'])
    if lev(a,b)>max(1,len(b)//6): bad+=1; print('ECART:',w['tr'],'|',tl(w['kn']),'|',w['kn'])
print(len(d),'entrées,',bad,'écarts')
