"""Questions, expected answers and baseline facts for the first wave (model-only).
Each question has key points (what a good answer mentions at least) and a full computed list for the appendix.
Expected answers are computed from the planted world (before noise); each lists the noise items that touch it.
Output: build/answers.json"""
import json, datetime
from collections import defaultdict
from common import path

W = json.load(open(path('build', 'world-planted.json'), encoding='utf-8'))
TODAY = W['world_today']; TWO_YEARS = '2028-11-01'
E = {e['id']: e for e in W['elements']}; KEY = {(e['type'], e['key']): e['id'] for e in W['elements']}
out = defaultdict(lambda: defaultdict(list)); inn = defaultdict(lambda: defaultdict(list))
for r in W['relationships']: out[r['type']][r['source']].append(r['target']); inn[r['type']][r['target']].append(r['source'])
flows = [r for r in W['relationships'] if r['type'] == 'Flow']
plants = json.load(open(path('build', 'plants.json'), encoding='utf-8'))
noise = json.load(open(path('build', 'noise-log.json'), encoding='utf-8'))
K = lambda t, k: KEY[(t, k)]
n = lambda i: E[i]['name']                       # plain name (sorting)
c = lambda i: f"`{E[i]['name']}`"                # model element name as code
cs = lambda ids: ', '.join(c(i) for i in ids)
typ = lambda i: E[i]['type']
TYPE_FI = {'ApplicationComponent': 'tietojärjestelmä', 'DataObject': 'tietoaineisto', 'BusinessService': 'palvelu', 'BusinessProcess': 'prosessi'}
kind = lambda a: E[a]['attrs'].get('actor_kind')
parent = {t: s for s, ts in out['Composition'].items() for t in ts if typ(s) == typ(t) == 'BusinessActor'}
def division_of_actor(a):
    while a in parent and kind(a) != 'division': a = parent[a]
    return a if kind(a) == 'division' else None
role_actor = {t: s for s, ts in out['Assignment'].items() for t in ts if typ(t) == 'BusinessRole'}
def division(eid):
    o = E[eid]['meta'].get('owner'); return division_of_actor(role_actor[o]) if o in role_actor else None
def owner_role(eid):
    m = E[eid]['meta']
    if m.get('owner'): return c(m['owner'])
    if m.get('provider'):
        p = KEY.get(('BusinessActor', m['provider'])); return f"ulkoinen tarjoaja {c(p)}" if p else 'ulkoinen toimittaja'
    return 'omistajaa ei ole kirjattu'
apps = [e['id'] for e in W['elements'] if typ(e['id']) == 'ApplicationComponent']
active = lambda i: E[i]['meta']['lifecycle'] != 'retired'
def apps_serving(p): return sorted((a for a in inn['Serving'][p] if typ(a) == 'ApplicationComponent'), key=n)
def sw_of(a): return [s for s in inn['Serving'][a] if typ(s) == 'SystemSoftware']
def nodes_of(a): return [x for x in inn['Serving'][a] if typ(x) == 'Node']
def fi(d): x = datetime.date.fromisoformat(d); return f"{x.day}.{x.month}.{x.year}"
leaf_procs = [e['id'] for e in W['elements'] if typ(e['id']) == 'BusinessProcess' and not [x for x in out['Composition'][e['id']] if typ(x) == 'BusinessProcess']]
pl = {p['id']: p for p in plants}

# ---------------------------------------------------------------- baseline facts
baseline = []
def B(bid, title, summary, items, note=''):
    baseline.append(dict(id=bid, title=title, summary=summary, note=note, items=items))
sw_rows = []
for s in sorted((e['id'] for e in W['elements'] if typ(e['id']) == 'SystemSoftware'), key=lambda i: E[i]['attrs']['vendor_support_end']):
    deps = sorted((a for a in out['Serving'][s] if typ(a) == 'ApplicationComponent'), key=n)
    end = E[s]['attrs']['vendor_support_end']
    if deps and end <= TWO_YEARS:
        sw_rows.append(dict(ids=[s] + deps, text=f"{c(s)}: tuki {'päättyi' if end < TODAY else 'päättyy'} {fi(end)}; käyttävät {cs(deps)}"))
expired = [r for r in sw_rows if E[r['ids'][0]]['attrs']['vendor_support_end'] < TODAY]
B('E01', 'Vanhentuneita ohjelmistoja', f"{len(expired)} ohjelmiston tuki on jo päättynyt ja {len(sw_rows) - len(expired)} ohjelmiston päättyy kahden vuoden sisällä.", sw_rows,
  'Jo päättynyt tuki on periaatteen 15 (Teknologioiden elinkaari hallitaan) vastaista.')
ct = sorted((a for a in apps if 'archetype' not in E[a]['attrs'] and E[a]['attrs'].get('contract_end') and E[a]['attrs']['contract_end'] <= '2027-06-30'),
            key=lambda a: E[a]['attrs']['contract_end'])
B('E02', 'Pian päättyviä sopimuksia', f"{len(ct)} tietojärjestelmän sopimus päättyy viimeistään 30.6.2027.",
  [dict(ids=[a], text=f"{c(a)}: sopimus päättyy {fi(E[a]['attrs']['contract_end'])}") for a in ct])
nos = sorted((p for p in leaf_procs if not apps_serving(p)), key=n)
B('E03', 'Prosesseja ilman tietojärjestelmää', f"{len(nos)} prosessia ei tue yksikään tietojärjestelmä.", [dict(ids=[p], text=c(p)) for p in nos])
writers = defaultdict(set)
for r in W['relationships']:
    if r['type'] == 'Access' and r['attrs']['access_type'] in ('write', 'readwrite'): writers[r['target']].add(r['source'])
linked = {(r['source'], r['target']) for r in flows} | {(r['target'], r['source']) for r in flows}
p10 = pl['P10']['elements']
undoc = []
for r in W['relationships']:
    if r['type'] == 'Access' and r['attrs']['access_type'] == 'read':
        a, dobj = r['source'], r['target']
        ws = writers[dobj] - {a}
        if ws and not any((w_, a) in linked for w_ in ws) and not (a in p10 and dobj in p10):
            undoc.append(dict(ids=[a, dobj], text=f"{c(a)} käyttää aineistoa {c(dobj)}; tietovirtaa sen kirjoittajista ({cs(sorted(ws, key=n))}) ei ole kuvattu"))
B('E04', 'Tiedon käyttöä ilman kuvattua tietovirtaa', f"{len(undoc)} tapausta, joissa järjestelmä käyttää toisen järjestelmän kirjoittamaa tietoa ilman kuvattua tietovirtaa.", undoc,
  'Ei välttämättä virhe: tieto voidaan saada myös muuta kautta. Istutettu puute P10 on näistä merkittävin ja kuvattu erikseen.')
book = sorted((a for a in apps if active(a) and ('varaus' in (E[a].get('description') or '').lower() or 'ajanvara' in (E[a].get('description') or '').lower())), key=n)
B('E05', 'Erillisiä varausjärjestelmiä', f"{len(book)} erillistä varaus- tai ajanvarausjärjestelmää: {cs(book)}.",
  [dict(ids=[a], text=f"{c(a)}: {E[a]['description']}") for a in book], 'Realistinen tilanne: yksiköt ovat hankkineet omia varaustyökalujaan. Liittyy istutettuun puutteeseen P12.')
vayla = K('ApplicationComponent', 'vayla'); vsw = sw_of(vayla)
vdeps = sorted((a for a in out['Serving'][vayla] if typ(a) == 'ApplicationComponent'), key=n)
nvf = sum(1 for r in flows if r['attrs'].get('via') == 'vayla')
B('E06', 'Integraatioalustan ohjelmiston tuki päättyy', f"{cs(vsw)}: tuki päättyy {fi(E[vsw[0]]['attrs']['vendor_support_end'])}. `Väylä` palvelee {len(vdeps)} tietojärjestelmää ja {nvf} tietovirtaa.",
  [dict(ids=[a], text=c(a)) for a in vdeps])
direct = [r for r in flows if r['attrs'].get('via') in ('direct', 'file') and E[r['source']]['attrs'].get('vendor') != E[r['target']]['attrs'].get('vendor')
          and 'national_service' not in (E[r['source']]['attrs'].get('deployment'), E[r['target']]['attrs'].get('deployment'))]
B('E07', 'Suoria integraatioita', f"{len(direct)} tietovirtaa kulkee eri toimittajien järjestelmien välillä suoraan tai tiedostona, ei integraatioalustan kautta.",
  [dict(ids=[r['source'], r['target']], text=f"{c(r['source'])} → {c(r['target'])}: {r['name']} ({'suora' if r['attrs']['via'] == 'direct' else 'tiedosto'})") for r in direct],
  'Periaate 11 edellyttää integraatioalustaa. Poikkeamispäätökset kuvataan vaiheessa 2.')

# ---------------------------------------------------------------- questions
Q = []
def q(qid, k, question, points, items, plants_=()):
    Q.append(dict(id=qid, k=k, question=question, points=points, items=[dict(ids=i[0], text=i[1]) for i in items], plants=list(plants_)))

# U01 Neuvonta ja viestintä
p = K('BusinessProcess', 'varhaiskasvatushakemusten_kasittely_ja_sijoittaminen'); ap = apps_serving(p)
q('Q01', 'U01', 'Mitkä tietojärjestelmät tukevat varhaiskasvatushakemusten käsittelyä, ja kuka niistä vastaa?',
  [f"{len(ap)} järjestelmää: " + '; '.join(f"{c(a)} ({owner_role(a)})" for a in ap) + '.'], [([a], f"{c(a)}: {owner_role(a)}") for a in ap])
a = K('ApplicationComponent', 'kerro_kartalla'); u = [x for x in out['Serving'][a] if typ(x) == 'BusinessActor']
q('Q02', 'U01', 'Kuka omistaa Kerro kartalla -järjestelmän?',
  ["Omistajaa ei ole kirjattu, eikä vastaus arvaa sitä.", f"Järjestelmää käyttää {cs(u)}; vastaus voi ehdottaa omistajan nimeämistä."],
  [([a] + u, f"{c(a)}: {owner_role(a)}; käyttäjä {cs(u)}")], ['P01'])
unit = K('BusinessActor', 'rakennusvalvonta')
procs = sorted((x for x in out['Assignment'][unit] if typ(x) == 'BusinessProcess'), key=n)
svcs = sorted({s for x in procs for s in out['Realization'][x] if typ(s) == 'BusinessService'}, key=n)
uapps = sorted({a for x in procs for a in apps_serving(x)} | {a for a in inn['Serving'][unit] if typ(a) == 'ApplicationComponent'}, key=n)
q('Q03', 'U01', 'Mitä prosesseja, palveluja ja tietojärjestelmiä Rakennusvalvonnan organisaatiomuutos koskee?',
  [f"Prosessit ({len(procs)}): {cs(procs)}.", f"Palvelut ({len(svcs)}): {cs(svcs)}.", f"Tietojärjestelmät ({len(uapps)}): {cs(uapps)}."],
  [([a], f"{c(a)}: {owner_role(a)}") for a in uapps])

# U02 Nykytila-analyysi
ov_real, ov_nat = [], []
real_apps = {x for pid in ('P03', 'P11') for x in pl[pid]['elements'] if typ(x) == 'ApplicationComponent'}
for dobj, ws in sorted(writers.items(), key=lambda kv: n(kv[0])):
    ws = sorted((x for x in ws if active(x) and E[x]['attrs'].get('deployment') != 'national_service'), key=n)
    if len(ws) >= 2:
        (ov_real if set(ws) & real_apps else ov_nat).append((ws + [dobj], f"{c(dobj)}: {cs(ws)}"))
q('Q04', 'U02', 'Missä on päällekkäisiä tietojärjestelmiä samaan käyttötarkoitukseen?',
  ["Mahdollinen päällekkäisyys: `Ympäristöasiat` kirjaa samaa asiarekisteriä kuin kaupunkiyhteinen `Diaari` (P03). Yksikön oma järjestelmä voi olla perusteltu; hyvä vastaus nostaa asian esiin, ei tuomitse sitä.",
   "Todennäköinen kaksoiskuvaus: `Infrakone` ja `Infra-kone 2` (P11).",
   f"Erilliset varausjärjestelmät: {cs(book)} (E05). Lisäksi tilavarauspalvelu on kahden yksikön vastuulla (P12).",
   f"Muut samaa tietoa kirjoittavat parit ({len(ov_nat)}) ovat luontevaa työnjakoa, esimerkiksi verkkoasiointi ja sen taustajärjestelmä. Niitä ei pidä esittää päällekkäisyyksinä."],
  [(ids, 'Mahdollinen päällekkäisyys, ' + t) for ids, t in ov_real] + [(book, 'Mahdollinen päällekkäisyys, varausjärjestelmät: ' + cs(book))] + [(ids, 'Luontevaa työnjakoa, ' + t) for ids, t in ov_nat],
  ['P03', 'P11', 'P12'])
q('Q05', 'U02', 'Mitkä prosessit ovat ilman tietojärjestelmätukea?', [f"{len(nos)} prosessia: {cs(nos)}."], [([x], c(x)) for x in nos])
po = sorted((a for a in apps if E[a]['meta']['lifecycle'] == 'phasing_out'), key=n)
items, points = [], ["Korvaaja tarkoittaa toista aktiivista tai suunniteltua järjestelmää, joka tukee samoja prosesseja. Mallissa sellaista ei näy."]
for a in po:
    points.append(f"{c(a)} poistuu {fi(E[a]['meta']['valid_to'])}.")
    for x in sorted((x for x in out['Serving'][a] if typ(x) == 'BusinessProcess'), key=n):
        others = [o for o in apps_serving(x) if o != a and E[o]['meta']['lifecycle'] in ('active', 'planned')]
        items.append(([a, x] + others, f"{c(a)} → {c(x)}; muut tukevat järjestelmät: {cs(others) or 'ei yhtään'}"))
        points.append(f"{c(x)}: " + (f"jäljelle jäävät {cs(others)}" if others else 'jää kokonaan ilman järjestelmää') + '.')
points.append("`Tonttihaku` itse riippuu `Tonttipalvelu`-järjestelmästä (P05), joten se ei ole korvaaja.")
q('Q06', 'U02', 'Mitkä poistuvat tietojärjestelmät tukevat yhä prosesseja, ja onko niille korvaaja?', points, items, ['P04', 'P05'])

# U03 Tietoaukot ja ristiriidat
rv = [a for a in uapps if K('BusinessActor', 'rakennusvalvonta') in out['Serving'][a]]
items, points, small = [], [], []
for a in rv:
    issues = [f"{c(s)} tuki päättyi {fi(E[s]['attrs']['vendor_support_end'])}" for s in sw_of(a) if E[s]['attrs']['vendor_support_end'] < TODAY]
    issues += [f"alusta {c(x)} poistuu {fi(E[x]['meta']['valid_to'])}" for x in nodes_of(a) if E[x]['meta']['lifecycle'] == 'phasing_out']
    txt = f"{c(a)} ({E[a]['description']}): " + ('; '.join(issues) if issues else 'ei elinkaaripuutteita')
    items.append(([a] + sw_of(a) + nodes_of(a), txt))
    if 'archetype' in E[a]['attrs'] and not issues: small.append(a)
    else: points.append(txt + '.')
if small: points.append(f"Lisäksi yksikön pienjärjestelmät: {cs(small)}.")
q('Q07', 'U03', 'Mitä tiedämme Rakennusvalvonnan tietojärjestelmistä, ja missä tiedot ovat puutteellisia tai ristiriitaisia?', points, items, ['P09'])
no_owner = sorted((e['id'] for e in W['elements'] if typ(e['id']) in TYPE_FI and not E[e['id']]['meta'].get('owner') and not E[e['id']]['meta'].get('provider')), key=n)
n5 = [x for x in noise if x['noise'] == 'N03']
q('Q08', 'U03', 'Mistä tietojärjestelmistä ja tietoaineistoista puuttuu omistaja?',
  [f"{c(x)} ({TYPE_FI[typ(x)]})" for x in no_owner] + [f"Testiversiossa lisäksi roolilta `{x['target_name']}` puuttuu henkilön nimi (kohina). Rooli on olemassa, mutta sen haltijaa ei tiedetä." for x in n5],
  [([x], f"{c(x)} ({TYPE_FI[typ(x)]})") for x in no_owner], ['P01', 'P02'])
pd_objs = {e['id'] for e in W['elements'] if typ(e['id']) == 'DataObject' and E[e['id']]['attrs'].get('personal_data')}
items = []
for r in flows:
    if E[r['target']]['meta']['lifecycle'] == 'retired':
        items.append(([r['source'], r['target']], f"Tietovirta {c(r['source'])} → {c(r['target'])}, vaikka {c(r['target'])} on poistettu käytöstä (P06)"))
for r in W['relationships']:
    if r['type'] == 'Access' and r['target'] in pd_objs and E[r['source']]['attrs'].get('personal_data') is False:
        items.append(([r['source'], r['target']], f"{c(r['source'])} käyttää aineistoa {c(r['target'])}, mutta on merkitty henkilötiedottomaksi (P07)"))
items.append(([K('ApplicationComponent', 'infrakone'), K('ApplicationComponent', 'infra_kone_2')], "`Infrakone` ja `Infra-kone 2` kuvaavat todennäköisesti samaa järjestelmää (P11)"))
q('Q09', 'U03', 'Missä mallin tiedot ovat keskenään ristiriidassa?',
  [f"{t}." for _, t in items] +
  ["Lisäksi mahdollisia aukkoja: `Pysäköintivahti` käyttää aineistoa `Henkilöiden perustiedot`, mutta lähdettä ei ole kuvattu (P10), ja muita vastaavia tapauksia on mallissa valmiiksi (E04). Nämä eivät ole välttämättä virheitä."],
  items + [(p10, '`Pysäköintivahti` käyttää aineistoa `Henkilöiden perustiedot` ilman kuvattua lähdettä (P10)')], ['P06', 'P07', 'P10', 'P11'])

# U04 Elinkaari ja tekninen velka
ky = K('BusinessActor', 'kaupunkiymparisto')
items, tech_n, contract_n = [], 0, 0
for a in sorted((a for a in apps if division(a) == ky and active(a)), key=n):
    tech = [f"{c(s)} tuki {fi(E[s]['attrs']['vendor_support_end'])}" for s in sw_of(a) if E[s]['attrs']['vendor_support_end'] <= TWO_YEARS]
    tech += [f"alusta {c(x)} poistuu {fi(E[x]['meta']['valid_to'])}" for x in nodes_of(a) if E[x]['meta']['lifecycle'] == 'phasing_out']
    if E[a]['meta']['lifecycle'] == 'phasing_out': tech.append(f"järjestelmä poistuu {fi(E[a]['meta']['valid_to'])}")
    con = [f"sopimus päättyy {fi(E[a]['attrs']['contract_end'])}"] if E[a]['attrs'].get('contract_end') and E[a]['attrs']['contract_end'] <= TWO_YEARS else []
    if tech: tech_n += 1
    if con: contract_n += 1
    if tech or con: items.append(([a] + sw_of(a) + nodes_of(a), f"{c(a)}: " + '; '.join(tech + con)))
gis = sorted({a for s in sw_of(K('ApplicationComponent', 'karttakone')) if E[s]['attrs']['vendor_support_end'] < TWO_YEARS for a in out['Serving'][s] if typ(a) == 'ApplicationComponent'}, key=n)
q('Q10', 'U04', 'Mikä Kaupunkiympäristössä vaatii uusimista kahden vuoden sisällä?',
  [f"Paikkatietojärjestelmien alusta: `Geomatica Server 10` ja `OpenRel 12` vanhenevat; niitä käyttävät {cs(gis)}.",
   "`Lupakone` toimii vanhentuneilla ohjelmistoilla ja poistuvalla alustalla `Tietokantaklusteri Quarry` (P09).",
   "`Tonttipalvelu` poistuu, ja se toimii ohjelmistoilla, joiden tuki on päättynyt (P04).",
   f"Yhteensä {tech_n} järjestelmällä on teknologia- tai elinkaaririski ja {contract_n} järjestelmän sopimus päättyy. Täysi lista on liitteessä."],
  items, ['P04', 'P09'])
q('Q11', 'U04', 'Mitkä tietojärjestelmät ovat riippuvaisia ohjelmistoista, joiden tuki on jo päättynyt?',
  [r['text'] + '.' for r in expired], [(r['ids'], r['text']) for r in expired])
nat_flows = [r for r in flows if r['attrs'].get('via') == 'vayla' and E[r['target']]['attrs'].get('deployment') == 'national_service']
q('Q12', 'U04', 'Mitä seuraa, jos integraatioalusta Väylän ohjelmiston tuki päättyy?',
  [f"{cs(vsw)}: tuki päättyy {fi(E[vsw[0]]['attrs']['vendor_support_end'])}.",
   f"`Väylä` palvelee {len(vdeps)} tietojärjestelmää, ja sen kautta kulkee {nvf} tietovirtaa.",
   f"Niistä {len(nat_flows)} on ilmoituksia kansallisiin palveluihin: " + '; '.join(f"{c(r['source'])} → {c(r['target'])}" for r in nat_flows) + '.',
   "Riski: lakisääteiset ilmoitukset voivat katketa, jos alustaa ei päivitetä ajoissa."],
  [([vayla] + vsw, f"{cs(vsw)} → `Väylä`")] + [([r['source'], r['target']], f"{c(r['source'])} → {c(r['target'])}: {r['name']}") for r in nat_flows])

# U05 Muutosten vaikutukset
law = K('Constraint', 'digipalvelulaki')
reg = sorted(inn['Realization'][law], key=n)
by_owner = defaultdict(list)
for x in reg: by_owner[owner_role(x)].append(x)
q('Q13', 'U05', 'Mitä digipalvelulain saavutettavuusvaatimusten muutos koskee, ja kenelle siitä pitää kertoa?',
  [f"{len(reg)} kohdetta, jotka digipalvelulaki sääntelee. Vastaus ryhmittelee ne omistajan mukaan, koska omistajille pitää kertoa muutoksesta:"] +
  [f"{o}: {cs(v)}" for o, v in sorted(by_owner.items())],
  [([x], f"{c(x)}: {owner_role(x)}") for x in reg])
outside = []
for a in apps:
    regions = {E[x]['attrs'].get('data_region') for x in nodes_of(a)}
    reads_pd = [r['target'] for r in W['relationships'] if r['type'] == 'Access' and r['source'] == a and r['target'] in pd_objs]
    if 'outside_eu_eea' in regions and (E[a]['attrs'].get('personal_data') or reads_pd):
        outside.append(([a] + nodes_of(a) + reads_pd, f"{c(a)} toimii alustalla {cs(nodes_of(a))} ja käyttää aineistoa {cs(reads_pd)}"))
q('Q14', 'U05', 'Missä henkilötietoja käsitellään EU/ETA-alueen ulkopuolella?',
  [t + ' (P08).' for _, t in outside] + ["Koskee lasten henkilötietoja ja on periaatteen 19 vastaista."], outside, ['P08'])
vtj = K('ApplicationComponent', 'kansallinen_vaestotietojarjestelma'); hp = K('DataObject', 'henkiloiden_perustiedot')
via_flow = sorted({r['target'] for r in flows if r['source'] == vtj}, key=n)
via_access = sorted({r['source'] for r in W['relationships'] if r['type'] == 'Access' and r['target'] == hp and r['source'] != vtj} - set(via_flow), key=n)
q('Q15', 'U05', 'Jos väestötietojen toimitus kansallisesta väestötietojärjestelmästä muuttuu, mihin kaupungin järjestelmiin se vaikuttaa?',
  [f"Tietovirtojen kautta: {cs(via_flow)}."] +
  [f"Lisäksi {c(a)} käyttää aineistoa `Henkilöiden perustiedot`, mutta sen lähdettä ei ole kuvattu (P10). Pelkkiä tietovirtoja seuraamalla se jäisi huomaamatta; hyvä vastaus mainitsee sen ja suosittelee tarkistamaan, miten tieto saadaan." for a in via_access],
  [([d], f"{c(d)} (tietovirta)") for d in via_flow] + [([d], f"{c(d)} (käyttää tietoa, lähdettä ei kuvattu)") for d in via_access], ['P10'])

# noise touching each answer
by_target = defaultdict(list)
for x in noise: by_target[x['target']].append(x)
for qq in Q:
    ids_ = {i for it in qq['items'] for i in it['ids']}
    qq['noise'] = [dict(noise=x['noise'], target=x['target'], target_name=x['target_name'], field=x['field']) for i in sorted(ids_) for x in by_target.get(i, [])]
json.dump(dict(questions=Q, baseline=baseline), open(path('build', 'answers.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('questions', len(Q), '| baseline', len(baseline))
