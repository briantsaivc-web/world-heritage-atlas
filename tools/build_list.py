#!/usr/bin/env python3
"""由 atlas-audit/whc 的 UNESCO 官方清單＋Wikidata 建 data/sites.json 與 data/countries.json"""
import json, re, html, sys
from babel import Locale
import opencc
AUD = '/home/claude/atlas-audit/whc/'; R = '/home/claude/world-heritage-atlas/data/'
cc = opencc.OpenCC('s2twp'); L = Locale.parse('zh_Hant_TW')
U = json.load(open(AUD + 'unesco.json')); W = json.load(open(AUD + 'wikidata.json'))['items']
by = {}
for d in W:
    for w in d['whs']: by.setdefault(w, []).append(d)
REG = {'Africa': ('africa', '非洲'), 'Arab States': ('arab', '阿拉伯國家'), 'Asia and the Pacific': ('asia', '亞洲及太平洋'),
       'Europe and North America': ('europe', '歐洲及北美'), 'Latin America and the Caribbean': ('latam', '拉丁美洲及加勒比海')}
CAT = {'Cultural': 'cultural', 'Natural': 'natural', 'Mixed': 'mixed'}
sites = []; countries = {}
for u in U:
    sid = u['id_number']; main = by.get(sid, [])
    zh = None; zsrc = None
    for d in main:
        if d.get('zhtw'): zh, zsrc = d['zhtw'], 'wikidata zh-tw'; break
        if d.get('zht'): zh, zsrc = d['zht'], 'wikidata zh-hant'; break
    if not zh:
        for d in main:
            if d.get('zh'): zh, zsrc = cc.convert(d['zh']), 'wikidata zh（轉繁）'; break
    coord = None
    for d in main:
        m = re.match(r'Point\(([-\d.]+) ([-\d.]+)\)', d.get('coord') or '')
        if m: coord = [round(float(m.group(2)), 4), round(float(m.group(1)), 4)]; break
    isos = [x.strip().upper() for x in u['iso_code'].split(',') if x.strip()]
    regs = [REG[r.strip()][0] for r in u['regions'].split(',') if r.strip() in REG]
    for iso, st in zip(isos, [s.strip() for s in u['states'].split(',')]):
        c = countries.setdefault(iso, {'iso': iso, 'en': st, 'zh': L.territories.get(iso, st), 'regions': set(), 'n': 0})
        c['n'] += 1; c['regions'] |= set(regs)
    desc = html.unescape(re.sub('<[^>]+>', ' ', u['short_description'])).strip()
    sites.append({'id': sid, 'en': html.unescape(u['site']), 'zh': zh, 'zh_src': zsrc, 'cat': CAT[u['category']],
                  'criteria': re.findall(r'\(([ivx]+)\)', u['criteria_txt']), 'year': int(u['date_inscribed']) if u['date_inscribed'].isdigit() else None,
                  'ext': [int(x) for x in u['secondary_dates'].split(',') if x.strip().isdigit()], 'danger': u['danger'] == '1',
                  'trans': u['transnational'] == '1', 'iso': isos, 'regions': regs, 'coord': coord, 'unesco': u['http_url'],
                  'q': [d['q'] for d in main if sid in d['whs']], 'en_desc': re.sub(r'\s+', ' ', desc)})
for c in countries.values(): c['regions'] = sorted(c['regions'])
sites.sort(key=lambda s: int(s['id']))
json.dump(sites, open(R + 'sites.json', 'w'), ensure_ascii=False, indent=0)
json.dump(sorted(countries.values(), key=lambda c: -c['n']), open(R + 'countries.json', 'w'), ensure_ascii=False, indent=0)
json.dump([{'id': v[0], 'zh': v[1], 'en': k} for k, v in REG.items()], open(R + 'regions.json', 'w'), ensure_ascii=False, indent=0)
print(len(sites), 'zh', sum(1 for s in sites if s['zh']), 'coord', sum(1 for s in sites if s['coord']), 'countries', len(countries))
