"""Apply the noise catalogue (skeleton/noise.yaml) to the planted world. Output: build/world-test.json, build/noise-log.json."""
import json, copy, random, datetime
from common import load, path, IdRegistry, slug

cfg = load('world.yaml'); spec = load('skeleton', 'noise.yaml')['noise']
def rng(*key): return random.Random(f"{cfg['seed']}|noise|" + '|'.join(map(str, key)))
def rdate(a, b, *key):
    a, b = datetime.date.fromisoformat(a), datetime.date.fromisoformat(b)
    return (a + datetime.timedelta(days=rng('date', *key).randint(0, (b - a).days))).isoformat()
ids = IdRegistry()
w = copy.deepcopy(json.load(open(path('build', 'world-planted.json'), encoding='utf-8')))
plants = json.load(open(path('build', 'plants.json'), encoding='utf-8'))
protected = {x for p in plants for x in p['elements']}
E = {e['id']: e for e in w['elements']}; KEY = {(e['type'], e['key']): e['id'] for e in w['elements']}
log = []
def note(n, target, field, old, new): log.append(dict(noise=n, name=spec[n]['name'], target=target, target_name=E[target]['name'] if target in E else '', field=field, old=old, new=new))
apps = [e for e in w['elements'] if e['type'] == 'ApplicationComponent' and e['id'] not in protected]
long_tail = sorted((e for e in apps if 'archetype' in e['attrs']), key=lambda e: e['key'])

# N01: stale confirmations
s = spec['N01']
for e in w['elements']:
    lo, hi = s['last_confirmed_between']
    if e['id'] in protected or e['meta']['valid_from'] > hi or rng('N01', e['key'], e['type']).random() >= s['rate']: continue
    new = rdate(max(lo, e['meta']['valid_from']), hi, e['type'], e['key'])
    note('N01', e['id'], 'last_confirmed', e['meta']['last_confirmed'], new); e['meta']['last_confirmed'] = new
# N02: missing description or vendor
for e in apps:
    if e['attrs'].get('deployment') == 'national_service': continue
    r = rng('N02', e['key'])
    if r.random() >= spec['N02']['rate']: continue
    if r.random() < 0.6 and e.get('description'):
        note('N02', e['id'], 'description', e['description'], None); e['description'] = None
    elif e['attrs'].get('vendor'):
        note('N02', e['id'], 'vendor', e['attrs']['vendor'], None); e['attrs'].pop('vendor')
# N03: role holder missing
roles = sorted((e for e in w['elements'] if e['type'] == 'BusinessRole' and e['attrs'].get('role_kind') in ('service_owner', 'application_owner')), key=lambda e: e['key'])
for e in rng('N03').sample(roles, spec['N03']['count']):
    note('N03', e['id'], 'holder', e['attrs'].get('holder'), None); e['attrs'].pop('holder', None)
# relationships by element
def rels_of(eid): return [r for r in w['relationships'] if r['source'] == eid or r['target'] == eid]
def new_rel(r, s, t):
    rid = ids.get('REL', f"{r['type']}:{s}:{t}:{r.get('name') or ''}")
    w['relationships'].append(dict(r, id=rid, source=s, target=t))
# N04: duplicate long-tail entries
pool = [e for e in long_tail]
dups = rng('N04').sample(pool, spec['N04']['count'])
for i, e in enumerate(dups):
    name = e['name'] + spec['N04']['name_variants'][i]; key = slug(name)
    nid = ids.get('APP', key)
    d = copy.deepcopy(e); d.update(id=nid, key=key, name=name); w['elements'].append(d); E[nid] = d
    for r in rels_of(e['id']):
        if r['source'] == e['id']: new_rel(r, nid, r['target'])
        else: new_rel(r, r['source'], nid)
    note('N04', nid, 'element', None, f"kaksoiskuvaus: {e['id']} {e['name']}")
pool = [e for e in long_tail if e not in dups]
# N05: module modelled as its own system
for parent_key, name, proc in spec['N05']['modules']:
    p = E[KEY[('ApplicationComponent', parent_key)]]; key = slug(name); nid = ids.get('APP', key)
    m = copy.deepcopy(p); m.update(id=nid, key=key, name=name, description=f"{p['description']} – moduuli")
    m['meta']['valid_from'] = rdate('2018-01-01', '2024-12-31', 'N05', key)
    m['meta']['last_confirmed'] = rdate(m['meta']['valid_from'], '2026-10-15', 'N05c', key)
    w['elements'].append(m); E[nid] = m
    pid = KEY[('BusinessProcess', proc)]
    new_rel(dict(type='Serving', name=None, meta=dict(source='Mallin ylläpito', last_confirmed=m['meta']['last_confirmed'], valid_from=m['meta']['valid_from']), attrs={}), nid, pid)
    for r in rels_of(p['id']):
        if r['type'] == 'Serving' and r['target'] == p['id'] and E[r['source']]['type'] in ('Node', 'SystemSoftware'): new_rel(r, r['source'], nid)
    note('N05', nid, 'element', None, f"moduuli kuvattu omana järjestelmänä: {p['id']} {p['name']}")
# N06: orphan systems
for e in rng('N06').sample(pool, spec['N06']['count']):
    gone = rels_of(e['id'])
    for r in gone: w['relationships'].remove(r)
    note('N06', e['id'], 'relationships', len(gone), 0)
w['elements'].sort(key=lambda e: e['id']); w['relationships'].sort(key=lambda r: r['id'])
w['variant'] = 'test'
ids.save()
json.dump(w, open(path('build', 'world-test.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(log, open(path('build', 'noise-log.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
from collections import Counter
print('noise', dict(Counter(x['noise'] for x in log)), '|', len(w['elements']), 'elements,', len(w['relationships']), 'relationships')
