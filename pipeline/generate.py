"""Build the clean Älylä world from the skeleton. Deterministic for a given seed.
Output: build/world.json (elements and relationships with metadata)."""
import random, datetime, json, os
from collections import defaultdict, Counter
from common import load, slug, path, IdRegistry

cfg = load('world.yaml')
def rng(*key):
    # Each item draws from its own random stream, derived from the seed and the item's key, so a change
    # in one part of the skeleton or generator never shifts the random values of anything else.
    return random.Random(f"{cfg['seed']}|" + '|'.join(map(str, key)))
ids = IdRegistry()
E, R = {}, {}
KEY = {}                       # (type, key) -> element id

def d(s): return datetime.date.fromisoformat(s)
def rdate(a, b, *key):
    a, b = d(a), d(b); return (a + datetime.timedelta(days=rng('date', *key).randint(0, (b - a).days))).isoformat()
def confirmed(*key, after='2025-03-01'):
    # last confirmed between March 2025 and mid-October 2026, never before the item came into use
    return rdate(max('2025-03-01', after), max('2026-10-15', after), 'confirmed', *key)

def el(prefix, etype, key, name, description=None, owner=None, provider=None, source=None,
       valid_from='2021-01-01', classification='internal', **attrs):
    eid = ids.get(prefix, key)
    meta = dict(owner=owner, provider=provider, source=source, last_confirmed=confirmed(etype, key, after=valid_from),
                lifecycle='active', valid_from=valid_from, classification=classification)
    if provider: meta['external'] = True
    E[eid] = dict(id=eid, type=etype, key=key, name=name, description=description,
                  meta={k: v for k, v in meta.items() if v is not None},
                  attrs={k: v for k, v in attrs.items() if v is not None})
    KEY[(etype, key)] = eid
    return eid

def rel(rtype, src, tgt, name=None, **attrs):
    rkey = f"{rtype}:{src}:{tgt}:{name or ''}"   # element IDs: keys are unique only within a type
    rid = ids.get('REL', rkey)
    vf = max(E[src]['meta']['valid_from'], E[tgt]['meta']['valid_from'])
    if rid in R: return rid   # the same relationship stated twice (e.g. a platform serving an application in several flows)
    R[rid] = dict(id=rid, type=rtype, source=src, target=tgt, name=name,
                  meta=dict(source='Mallin ylläpito', last_confirmed=confirmed(rkey, after=vf), valid_from=vf),
                  attrs={k: v for k, v in attrs.items() if v is not None})
    return rid

FIRST = ["Aino","Eero","Helmi","Ilkka","Johanna","Kari","Laura","Mikko","Niina","Olli","Päivi","Riikka","Sami","Tiina","Ville","Anu","Heikki","Jari","Katja",
         "Marja","Pekka","Satu","Timo","Ulla","Antti","Elina","Hanna","Juha","Kirsi","Lauri","Minna","Petri","Sanna","Tuomas","Veera","Ari","Eija","Harri","Jenni",
         "Kalle","Leena","Markku","Noora","Pirjo","Reijo","Sirpa","Teemu","Outi","Ismo","Merja","Jukka","Tarja","Mervi","Henri","Sari","Janne","Kaisa","Matti","Liisa"]
LAST = ["Aaltonen","Heikkilä","Hirvonen","Huttunen","Jokinen","Kallio","Karjalainen","Koivisto","Korhonen","Laaksonen","Lehtinen","Lindholm","Mattila","Miettinen",
        "Mäkelä","Niemi","Nurmi","Ojala","Peltonen","Rantanen","Salminen","Savolainen","Tuominen","Turunen","Vainio","Virtanen","Väisänen","Ylönen","Hakala","Kettunen",
        "Kivelä","Leinonen","Manninen","Nieminen","Pitkänen","Räsänen","Saarinen","Sirola","Toivonen","Uotila","Vesterinen","Ahola","Halme","Ikonen","Jääskeläinen"]
used_names = set()
def person(key):
    r = rng('person', key)
    while True:
        n = f"{r.choice(FIRST)} {r.choice(LAST)}"
        if n not in used_names: used_names.add(n); return n

# ---------------------------------------------------------------- organisation
org = load('skeleton', 'organisation.yaml')
parent = {}; kind = {}; actor_name = {}
city = el('ACT', 'BusinessActor', 'alyla', org['city']['name'], 'Älymaan maakunnassa sijaitseva noin 69 000 asukkaan kaupunki.',
          source='Kaupungin hallintosääntö', classification='public', actor_kind='city', residents=org['city']['residents'])
def actor(x, k, par=None, external=False):
    kind[x['key']] = k; actor_name[x['key']] = x['name']
    if par: parent[x['key']] = par
    return el('ACT', 'BusinessActor', x['key'], x['name'], x.get('note'), provider=x['key'] if external else None,
              source='Kaupungin hallintosääntö', classification='public', actor_kind=k, relates_to=x.get('relates_to'))
for x in org['political_bodies']: rel('Composition', city, actor(x, 'political_body'))
for x in org.get('steering_groups', []): rel('Composition', city, actor(x, 'steering_group'))
for x in org['customer_groups']: actor(x, 'customer_group')
for dv in org['divisions']:
    did = actor(dv, 'division'); rel('Composition', city, did)
    for u in dv['units']:
        uid = actor(u, 'unit', dv['key']); rel('Composition', did, uid)
        for su in u.get('subunits', []):
            sid = actor(su, 'subunit', u['key']); rel('Composition', uid, sid)
for x in org['group_companies']:
    rel('Association', city, actor(x, 'group_company', external=True), name='omistaa')
for x in org['external_orgs']: actor(x, 'external_org', external=True)
for x in org['national_authorities']: actor(x, 'national_authority', external=True)
A = lambda k: KEY[('BusinessActor', k)]
def unit_of(k): return parent[k] if kind.get(k) == 'subunit' else k
def division_of(k):
    while kind.get(k) not in ('division', None): k = parent[k]
    return k

# ---------------------------------------------------------------- roles
roles = {}
def role(key, name, unit_key, role_kind, owner=None):
    rid = el('ROL', 'BusinessRole', key, name, owner=owner, source='Kaupungin hallintosääntö', holder=person(key), role_kind=role_kind)
    E[rid]['meta']['owner'] = owner or rid
    rel('Assignment', A(unit_key) if unit_key != 'alyla' else city, rid)
    roles[key] = rid; return rid
mayor = role('kaupunginjohtaja', 'Kaupunginjohtaja', 'alyla', 'other')
E[city]['meta']['owner'] = mayor
head = {}
for dv in org['divisions']:
    title = 'Konsernijohtaja' if dv['key'] == 'konsernihallinto' else f"Toimialajohtaja, {dv['name']}"
    head[dv['key']] = role(slug(title), title, dv['key'], 'other', mayor)
    E[A(dv['key'])]['meta']['owner'] = head[dv['key']]
# owner roles on division level: one service owner and one information system owner per division
service_owner, is_owner = {}, {}
for dv in org['divisions']:
    service_owner[dv['key']] = role(slug(f"Palveluomistaja {dv['name']}"), f"Palveluomistaja, {dv['name']}", dv['key'], 'service_owner', head[dv['key']])
    is_owner[dv['key']] = role(slug(f"Tietojärjestelmäomistaja {dv['name']}"), f"Tietojärjestelmäomistaja, {dv['name']}", dv['key'], 'application_owner', head[dv['key']])
    for u in dv['units']:
        E[A(u['key'])]['meta']['owner'] = service_owner[dv['key']]
        for su in u.get('subunits', []): E[A(su['key'])]['meta']['owner'] = service_owner[dv['key']]
def so(k): return service_owner[division_of(k)]
architect = role('kokonaisarkkitehti', 'Kokonaisarkkitehti', 'arkkitehtuuri_ja_tiedonhallinta', 'architect', so('arkkitehtuuri_ja_tiedonhallinta'))
platform_owner = role('alustaomistaja_ict_palvelutuotanto', 'Alustaomistaja, ICT-palvelutuotanto', 'ict_palvelutuotanto', 'platform_owner', so('ict_palvelutuotanto'))
for x in org['political_bodies'] + org.get('steering_groups', []) + org['customer_groups']:
    E[A(x['key'])]['meta']['owner'] = so('hallinto_ja_lakipalvelut')

# ---------------------------------------------------------------- goals, services, processes, capabilities
for g in load('skeleton', 'goals.yaml')['goals']:
    el('GOL', 'Goal', g['key'], g['name'], g['description'], owner=mayor, source='Kaupunkistrategia', classification='public')
procs_raw = load('skeleton', 'processes.yaml')['process_groups']
for s in load('skeleton', 'services.yaml')['services']:
    if 'provider' in s:
        sid = el('SRV', 'BusinessService', s['key'], s['name'], provider=s['provider'], source='Palveluluettelo', classification='public', audience=s['audience'])
    else:
        vf = '2025-01-01' if unit_of(s['unit']) == 'tyollisyyspalvelut' else '2021-01-01'
        sid = el('SRV', 'BusinessService', s['key'], s['name'], owner=so(s['unit']), source='Palveluluettelo', classification='public', valid_from=vf, audience=s['audience'])
    for c in s.get('serves', []): rel('Serving', sid, A(c))
proc_unit = {}
for g in procs_raw:
    gid = el('PRC', 'BusinessProcess', g['key'], g['name'], owner=so(g['unit']), source='Prosessikartta', process_kind=g['kind'])
    proc_unit[g['key']] = g['unit']; rel('Assignment', A(g['unit']), gid)
    for p in g['processes']:
        vf = '2025-01-01' if unit_of(p['unit']) == 'tyollisyyspalvelut' else '2021-01-01'
        pid = el('PRC', 'BusinessProcess', p['key'], p['name'], owner=so(p['unit']), source='Prosessikartta', valid_from=vf, process_kind=g['kind'])
        proc_unit[p['key']] = p['unit']
        rel('Composition', gid, pid); rel('Assignment', A(p['unit']), pid)
        for s in p.get('realizes', []): rel('Realization', pid, KEY[('BusinessService', s)])
P = lambda k: KEY[('BusinessProcess', k)]
def cap(c, level, par=None):
    cid = el('CAP', 'Capability', c['key'], c['name'], owner=architect, source='Kyvykkyyskartta', level=level)
    if par: rel('Composition', par, cid)
    for p in c.get('realized_by', []): rel('Realization', P(p), cid)
    for g in c.get('supports', []): rel('Realization', cid, KEY[('Goal', g)])
    for ch in c.get('children', []): cap(ch, level + 1, cid)
for c in load('skeleton', 'capabilities.yaml')['capabilities']: cap(c, 1)

# ---------------------------------------------------------------- information, laws
for x in load('skeleton', 'information.yaml')['information']:
    ext = kind.get(x['owner']) == 'group_company'
    el('DAT', 'DataObject', x['key'], x['name'], owner=None if ext else so(x['owner']), provider=x['owner'] if ext else None,
       source='Tiedonhallintamalli', classification='confidential' if x['personal_data'] else 'internal', personal_data=x['personal_data'])
D = lambda k: KEY[('DataObject', k)]
lawyer = so('hallinto_ja_lakipalvelut')
for c in load('skeleton', 'constraints.yaml')['constraints']:
    cid = el('CON', 'Constraint', c['key'], c['name'], c['description'], owner=lawyer, source='Lainsäädäntö', classification='public', based_on=c['based_on'])
    for s in c.get('services', []): rel('Realization', KEY[('BusinessService', s)], cid)
    for p in c.get('processes', []): rel('Realization', P(p), cid)
    for x in c.get('data', []): rel('Association', cid, D(x))
CON = lambda k: KEY[('Constraint', k)]

# ---------------------------------------------------------------- technology
tech = load('skeleton', 'technology.yaml')
for l in tech['locations']:
    lid = el('LOC', 'Location', l['key'], l['name'], owner=platform_owner, source='Konfiguraatiotietokanta', location_kind=l['location_kind'], data_region=l['data_region'])
    for a in l.get('hosts', []): rel('Aggregation', lid, A(a))
for s in tech['system_software']:
    el('SSW', 'SystemSoftware', s['key'], s['name'], owner=platform_owner, source='Konfiguraatiotietokanta', valid_from=rdate('2014-01-01', '2024-06-30', 'ssw', s['key']),
       product=s['product'], version=str(s['version']), vendor=s['vendor'], software_kind=s['software_kind'], vendor_support_end=str(s['vendor_support_end']))
for n in tech['nodes']:
    if n.get('external'):
        own, prov = None, n.get('owner') or 'toimittaja'
    else:
        own, prov = (platform_owner if n['owner'] == 'ict_palvelutuotanto' else so(n['owner'])), None
    nid = el('NOD', 'Node', n['key'], n['name'], n['description'], owner=own, provider=prov,
             source='Konfiguraatiotietokanta', valid_from=rdate('2012-01-01', '2023-12-31', 'nod', n['key']), data_region=n['data_region'])
    rel('Aggregation', KEY[('Location', n['location'])], nid)
    for s in n.get('consists_of') or []: rel('Composition', nid, KEY[('SystemSoftware', s)])
    for l in n.get('laws') or []: rel('Realization', nid, CON(l))

# ---------------------------------------------------------------- applications
apps = load('skeleton', 'applications.yaml')
profiles = apps['hosting_profiles']
def host(aid, prof):
    for n in profiles[prof]['nodes']: rel('Serving', KEY[('Node', n)], aid)
    for s in profiles[prof]['software']: rel('Serving', KEY[('SystemSoftware', s)], aid)
def access(aid, reads, writes):
    for x in sorted(set(reads) | set(writes)):
        t = 'readwrite' if x in reads and x in writes else ('write' if x in writes else 'read')
        rel('Access', aid, D(x), access_type=t)
def app_dates(dep, key):
    if dep == 'on_prem': return rdate('2008-01-01', '2019-12-31', 'app', key)
    if dep == 'national_service': return rdate('2015-01-01', '2023-12-31', 'app', key)
    return rdate('2016-01-01', '2025-09-30', 'app', key)
def app_owner(u): return is_owner[division_of(u)]   # the division's information system owner
for a in apps['applications']:
    ext = a.get('owner_external')
    vf = '2025-01-01' if unit_of(a['unit']) == 'tyollisyyspalvelut' and not ext else app_dates(a['deployment'], a['key'])
    owner = None if ext else app_owner(a['unit'])
    aid = el('APP', 'ApplicationComponent', a['key'], a['name'], a['purpose'], owner=owner, provider=ext, source='Sovellussalkku',
             valid_from=vf, classification='confidential' if a['personal_data'] else 'internal',
             vendor=a['vendor'], deployment=a['deployment'], contract_end=None if ext else rdate('2026-12-01', '2031-12-31', 'contract', a['key']),
             criticality=a['criticality'], personal_data=a['personal_data'])
    for p in a.get('serves', []): rel('Serving', aid, P(p))
    users = ({a['unit']} if not ext else set()) | set(a.get('used_by', []))   # the responsible unit, plus wider use
    for u in sorted(users): rel('Serving', aid, A(u))
    access(aid, a.get('reads', []), a.get('writes', []))
    if any(E[D(x)]['attrs'].get('personal_data') for x in a.get('reads', []) + a.get('writes', [])):
        # a system that handles personal data is marked so, consistently
        E[aid]['attrs']['personal_data'] = True; E[aid]['meta']['classification'] = 'confidential'
    for l in a.get('laws', []): rel('Realization', aid, CON(l))
    host(aid, a['hosting'])

units_all = sorted(k for k, v in kind.items() if v in ('unit', 'subunit'))
procs_by_actor = defaultdict(list)
for p, u in proc_unit.items(): procs_by_actor[u].append(p)
small_vendors = ["Appsi Oy","Pilvipaja Oy","Koodiverstas Oy","Digiraami Oy","Nettinikkari Oy","Sovelluspuoti Oy","Datapolku Oy","Webtaimi Oy","Ohjelmistoapaja Oy",
                 "Kirkas Software","Tieto-Tuuli Oy","Linkki Labs","Oppiva Media Oy","Edutaito Oy","Satakieli Apps"]
def pick_weighted(w, r):
    x = r.random(); acc = 0
    for k, v in w.items():
        acc += v
        if x < acc: return k
    return list(w)[-1]
app_keys = {a['key'] for a in apps['applications']}
for lt in apps['long_tail']:
    names = list(lt['names']); rng('pool', lt['archetype']).shuffle(names)
    for i in range(lt['count']):
        name = names[i]; key = slug(name); r = rng('long_tail', key)
        assert key not in app_keys, key; app_keys.add(key)
        u = lt['unit']
        if u == 'any_unit': u = r.choice(units_all)
        elif isinstance(u, list): u = r.choice(u)
        if lt['serves'] == 'unit_processes':
            cand = procs_by_actor.get(u) or procs_by_actor.get(unit_of(u)) or []
            serves = [r.choice(sorted(cand))] if cand else []
        else:
            serves = [r.choice(lt['serves'])]
        prof = pick_weighted(lt['hosting'], r); pd = r.random() < lt['personal_data_share']; dep = lt['deployment']
        aid = el('APP', 'ApplicationComponent', key, name, lt['archetype'], owner=app_owner(u), source='Sovellussalkku',
                 valid_from=rdate('2015-01-01', '2026-06-30', 'app', key), classification='confidential' if pd else 'internal',
                 vendor='Kaupunki (oma)' if prof == 'file_server' else r.choice(small_vendors),
                 deployment=dep, contract_end=None if prof == 'file_server' else rdate('2026-12-01', '2029-12-31', 'contract', key),
                 criticality=lt['criticality'], personal_data=pd, archetype=lt['archetype'])
        for p in serves: rel('Serving', aid, P(p))
        rel('Serving', aid, A(u)); host(aid, prof)

APPK = lambda k: KEY[('ApplicationComponent', k)]
vayla = APPK('vayla'); natl = KEY[('Node', 'kansallinen_tiedonvalityskerros')]
for f in apps['flows']:
    s, t = APPK(f['from']), APPK(f['to'])
    # One flow per integration, sender -> receiver. The integration platform (Väylä) and the national data
    # exchange layer are modelled as serving the city-side endpoints, so platform dependence stays traversable.
    rel('Flow', s, t, f['payload'], via=f['via'])
    if f['via'] == 'vayla':
        for x in (s, t): rel('Serving', vayla, x)
    if f['via'] == 'national_layer':
        for x in (s, t):
            if E[x]['attrs'].get('deployment') != 'national_service': rel('Serving', natl, x)

# ---------------------------------------------------------------- write
os.makedirs(path('build'), exist_ok=True)
world = dict(seed=cfg['seed'], world_today=cfg['world_today'], elements=sorted(E.values(), key=lambda e: e['id']),
             relationships=sorted(R.values(), key=lambda r: r['id']))
with open(path('build', 'world.json'), 'w', encoding='utf-8') as f: json.dump(world, f, ensure_ascii=False, indent=1)
ids.save()
print('elements', len(E), dict(Counter(e['type'] for e in E.values())))
print('relationships', len(R), dict(Counter(r['type'] for r in R.values())))
