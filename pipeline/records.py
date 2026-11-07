"""Build the records layer from skeleton/records and the world. Outputs build/records.json and readable files under
export/records/. Currently principles (PRI); decisions, initiatives and documents follow in phase 2."""
import json, os, random, datetime
from collections import defaultdict
from common import load, slug, path, IdRegistry

cfg = load('world.yaml')
def rng(*key): return random.Random(f"{cfg['seed']}|" + '|'.join(map(str, key)))
ids = IdRegistry()
w = json.load(open(path('build', 'world.json'), encoding='utf-8'))
E = {e['id']: e for e in w['elements']}
KEY = {(e['type'], e['key']): e['id'] for e in w['elements']}
out = defaultdict(lambda: defaultdict(list))
for r in w['relationships']: out[r['type']][r['source']].append(r['target'])
kind = lambda a: E[a]['attrs'].get('actor_kind')
parent = {t: s for s, ts in out['Composition'].items() for t in ts if E[s]['type'] == E[t]['type'] == 'BusinessActor'}
unit_of = lambda a: parent[a] if kind(a) == 'subunit' else a
def division_of(a):
    while a in parent and kind(a) != 'division': a = parent[a]
    return a if kind(a) == 'division' else None
role_actor = {t: s for s, ts in out['Assignment'].items() for t in ts if E[t]['type'] == 'BusinessRole'}
def responsible_unit(app):
    """The unit (or sub-unit) an information system serves within its owner's division."""
    dv = role_actor.get(E[app]['meta'].get('owner'))
    cand = sorted(x for x in out['Serving'][app] if kind(x) in ('unit', 'subunit') and (dv is None or division_of(x) == dv))
    return cand[0] if cand else None
def fi_date(s): d = datetime.date.fromisoformat(s); return f"{d.day}.{d.month}.{d.year}"

records = {'principles': [], 'documents': []}
architect = KEY[('BusinessRole', 'kokonaisarkkitehti')]
board = KEY[('BusinessActor', 'kokonaisarkkitehtuuriryhma')]
CAT_FI = {'general': 'Yleiset', 'business': 'Toiminta', 'information': 'Tieto', 'application': 'Tietojärjestelmät',
          'technology': 'Teknologia', 'security': 'Turvallisuus'}

# ---------------------------------------------------------------- principles
for p in load('skeleton', 'records', 'principles.yaml')['principles']:
    key = slug(p['title'])
    records['principles'].append(dict(id=ids.get('PRI', key), key=key, title=p['title'], category=p['category'], statement=p['statement'],
        rationale=p['rationale'], implications=p['implications'], owner=architect, status='approved',
        approved_on=str(p['approved_on']), approved_by=board))

# Documents (system register extract, public description of record-holding systems, etc.) are phase 2.

# ---------------------------------------------------------------- write
ids.save()
with open(path('build', 'records.json'), 'w', encoding='utf-8') as f: json.dump(records, f, ensure_ascii=False, indent=1)
base = path('export', 'records')
os.makedirs(os.path.join(base, 'periaatteet'), exist_ok=True)
def yaml_header(d):
    import yaml
    return '---\n' + yaml.safe_dump(d, allow_unicode=True, sort_keys=False, width=200) + '---\n'
for p in records['principles']:
    hdr = {k: p[k] for k in ('id', 'title', 'category', 'owner', 'status', 'approved_on', 'approved_by')}
    body = (f"# {p['title']}\n\nAlue: {CAT_FI[p['category']]}. Hyväksytty {fi_date(p['approved_on'])}, {E[p['approved_by']]['name']}.\n\n"
            f"## Periaate\n\n{p['statement']}\n\n## Perustelut\n\n{p['rationale']}\n\n## Vaikutukset\n\n" + '\n'.join(f"- {x}" for x in p['implications']) + '\n')
    open(os.path.join(base, 'periaatteet', f"{p['id']}.md"), 'w', encoding='utf-8').write(yaml_header(hdr) + '\n' + body)
idx = ['# Älylän kaupungin arkkitehtuuriperiaatteet']
for cat, fi in CAT_FI.items():
    idx.append(f"\n## {fi}\n")
    idx += [f"- {p['id']} {p['title']}" for p in records['principles'] if p['category'] == cat]
open(os.path.join(base, 'periaatteet', 'README.md'), 'w', encoding='utf-8').write('\n'.join(idx) + '\n')
print('principles', len(records['principles']), '| documents', len(records['documents']))
