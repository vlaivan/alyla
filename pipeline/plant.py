"""Apply planted findings (skeleton/plants.yaml) to the clean world. Output: build/world-planted.json, build/plants.json."""
import json, copy
from common import load, path, IdRegistry

ids = IdRegistry()
w = json.load(open(path('build', 'world.json'), encoding='utf-8'))
w = copy.deepcopy(w)
E = {e['id']: e for e in w['elements']}
KEY = {(e['type'], e['key']): e['id'] for e in w['elements']}
R = {r['id']: r for r in w['relationships']}
def ref(x): return KEY[tuple(x)]
plants_out = []
for p in load('skeleton', 'plants.yaml')['plants']:
    touched_e, touched_r = set(), set()
    for op in p['ops']:
        (kind, a), = op.items()
        if kind == 'set':
            e = E[ref(a['target'])]; touched_e.add(e['id'])
            for part in ('meta', 'attrs'):
                for k, v in (a.get(part) or {}).items():
                    if v is None: e[part].pop(k, None)
                    else: e[part][k] = v
        elif kind == 'add_element':
            prefix = {'ApplicationComponent': 'APP', 'Node': 'NOD', 'DataObject': 'DAT'}[a['type']]
            eid = ids.get(prefix, a['key'])
            meta = dict(lifecycle='active', last_confirmed='2026-06-15'); meta.update(a.get('meta', {}))
            if isinstance(meta.get('owner'), list): meta['owner'] = ref(meta['owner'])
            if meta.get('provider'): meta['external'] = True
            e = dict(id=eid, type=a['type'], key=a['key'], name=a['name'], description=a.get('description'), meta=meta, attrs=dict(a.get('attrs', {})))
            w['elements'].append(e); E[eid] = e; KEY[(a['type'], a['key'])] = eid; touched_e.add(eid)
        elif kind == 'add_rel':
            s, t = ref(a['source']), ref(a['target'])
            rid = ids.get('REL', f"{a['type']}:{s}:{t}:{a.get('name') or ''}")
            meta = dict(source='Mallin ylläpito', last_confirmed='2026-06-15', valid_from=max(E[s]['meta']['valid_from'], E[t]['meta']['valid_from']))
            meta.update(a.get('meta', {}))
            r = dict(id=rid, type=a['type'], source=s, target=t, name=a.get('name'), meta=meta, attrs=dict(a.get('attrs', {})))
            w['relationships'].append(r); R[rid] = r; touched_r.add(rid); touched_e |= {s, t}
        elif kind == 'remove_rel':
            s, t = ref(a['source']), ref(a['target'])
            hit = [r for r in w['relationships'] if r['type'] == a['type'] and r['source'] == s and r['target'] == t]
            assert len(hit) == 1, (p['id'], a)
            w['relationships'].remove(hit[0]); touched_r.add(hit[0]['id']); touched_e |= {s, t}
    plants_out.append(dict(id=p['id'], title=p['title'], use_cases=sorted(p['use_cases']), principles=p['principles'], where=p['where'],
                           good_answer=p['good_answer'], expected_deviations=p.get('expected_deviations', []),
                           elements=sorted(touched_e), relationships=sorted(touched_r)))
w['elements'].sort(key=lambda e: e['id']); w['relationships'].sort(key=lambda r: r['id'])
w['variant'] = 'planted'
ids.save()
json.dump(w, open(path('build', 'world-planted.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(plants_out, open(path('build', 'plants.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('planted', len(plants_out), 'findings |', len(w['elements']), 'elements,', len(w['relationships']), 'relationships')
