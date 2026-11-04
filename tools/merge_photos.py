# 2026-11-04 起：加讀 vision_claude.json（Claude 篩選，key 為 p3_<id>/p4_<id>）
# 用法：cd /home/claude && D=YYYY-MM-DD python3 world-heritage-atlas/tools/merge_photos.py（合併 atlas-audit/whc 的 photos3＋photos4 vision 結果）
import json,math,shutil,os,glob
A='atlas-audit/whc'; R='world-heritage-atlas'
d=json.load(open(f'{A}/photos3.json')); G=json.load(open(f'{A}/geo.json'))
p4=json.load(open(f'{A}/photos4.json')) if os.path.exists(f'{A}/photos4.json') else {}
CV=json.load(open(f'{A}/vision_claude.json')) if os.path.exists(f'{A}/vision_claude.json') else {}  # Claude 子代理看圖結果（Gemini 沒篩到的才用）
S=json.load(open(f'{R}/data/sites.json')); I={s['id']:s for s in S}
for f in glob.glob(f'{R}/img/800/*')+glob.glob(f'{R}/img/thumb/*'): os.remove(f)
def dist(a,b):
    la1,lo1,la2,lo2=map(math.radians,[a[0],a[1],b[0],b[1]])
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 6371*2*math.asin(math.sqrt(h))
out={}
for sid,s in I.items():
    c=s.get('coord'); lim=3000 if len(s['iso'])>1 else 600
    cand=[]
    v=d.get(sid)
    if v and 'vision' not in v and f'p3_{sid}' in CV: v=dict(v,vision=CV[f'p3_{sid}'])
    if v and 'vision' in v:
        def ok(k):
            p=v['photos'][k]; g=G.get(p['file'])
            if g and c: return dist(g,c)<=lim
            return p['score'] in (25,15,5)
        keep=[k for k in dict.fromkeys(v['vision']['keep']) if k<len(v['photos']) and ok(k)]
        rej={int(k) for k in (v['vision'].get('reject') or {}) if str(k).isdigit()}
        cand+=[('img3',k,v['photos'][k]) for k in keep]
        if len(cand)<4:
            rest=sorted([k for k in range(len(v['photos'])) if k not in keep and k not in rej and ok(k) and v['photos'][k]['score']>=15],key=lambda k:-v['photos'][k]['score'])
            cand+=[('img3',k,v['photos'][k]) for k in rest[:4-len(cand)]]
    w=p4.get(sid)
    if w and len(cand)<6:
        if 'vision' not in w and f'p4_{sid}' in CV: w=dict(w,vision=CV[f'p4_{sid}'])
        if 'vision' in w: ks=[k for k in dict.fromkeys(w['vision']['keep']) if k<len(w['photos'])]
        else: ks=[]
        seen={x[2]['file'] for x in cand}
        cand+=[('img4',k,w['photos'][k]) for k in ks if w['photos'][k]['file'] not in seen]
    if not cand and v and f'r3_{sid}' in CV:  # 第二意見：原本零照片者，Claude 判定為該遺產即採用（不做座標檢查，先求有）
        cand+=[('img3',k,v['photos'][k]) for k in dict.fromkeys(CV[f'r3_{sid}']['keep']) if k<len(v['photos'])]
    out[sid]=cand[:6]
for s in S: s.pop('photos',None)
for sid,cs in out.items():
    ph=[]
    for j,(src,k,p) in enumerate(cs):
        shutil.copy(f'{A}/{src}/800/{sid}_{k}.webp',f'{R}/img/800/{sid}_{j}.webp')
        e={'file':p['file'],'artist':p.get('artist',''),'license':p.get('license',''),'license_url':p.get('license_url',''),'src':f'img/800/{sid}_{j}.webp'}
        if j==0: shutil.copy(f'{A}/{src}/thumb/{sid}_{k}.webp',f'{R}/img/thumb/{sid}_0.webp'); e['thumb']=f'img/thumb/{sid}_0.webp'
        ph.append(e)
    if ph: I[sid]['photos']=ph
json.dump(S,open(f'{R}/data/sites.json','w'),ensure_ascii=False,indent=0)
wp=[s for s in S if s.get('photos')]; n=sum(len(s['photos']) for s in wp)
m=json.load(open(f'{R}/data/meta.json')); m['counts']['with_photo']=len(wp); m['counts']['photos']=n; m['updated']=os.environ.get('D','2026-11-04')
m['notes'].append(f"{m['updated']}：照片更新為 {len(wp)} 處、{n} 張。")
json.dump(m,open(f'{R}/data/meta.json','w'),ensure_ascii=False,indent=1)
print('with photo',len(wp),'photos',n,'avg',round(n/max(1,len(wp)),2),'>=5',sum(1 for s in wp if len(s['photos'])>=5),'zero',len(S)-len(wp))
json.dump({k:[(a,b) for a,b,_ in v] for k,v in out.items()},open('/tmp/claude-0/whc_out.json','w'))
