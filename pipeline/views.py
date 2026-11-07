"""Generated views for Archi, organised in folders. Simple nested grid layout; absolute coordinates as in the
exchange format. Views are outputs: regenerating overwrites them, so changes belong in the skeleton."""
from collections import defaultdict, Counter
from labels import MODEL_TITLE, VARIANTS, VERSION
W, H, GAP, PAD, TOP, MAXW = 150, 55, 12, 12, 28, 1900

class Box:
    def __init__(self, elem=None, label=None, children=None, mode='row', maxw=MAXW, leaf_w=W, note=None, role='main'):
        self.elem, self.label, self.children, self.mode, self.maxw, self.leaf_w, self.note, self.role = elem, label, children or [], mode, maxw, leaf_w, note, role
    def measure(self):
        if self.note:
            self.w = 980; self.h = 18 * (self.note.count('\n') + 1) + 24; return
        if not self.children:
            self.w, self.h = self.leaf_w, H
            if self.label: self.w, self.h = max(self.leaf_w, 8 * len(self.label) + 2 * PAD), TOP + PAD
            return
        for c in self.children: c.measure()
        if self.mode == 'col':
            self.w = max(c.w for c in self.children) + 2 * PAD
            self.h = TOP + sum(c.h for c in self.children) + GAP * (len(self.children) - 1) + PAD
            return
        lines, line, lw = [], [], 0
        for c in self.children:
            if line and lw + GAP + c.w > self.maxw - 2 * PAD: lines.append(line); line, lw = [], 0
            lw += (GAP if line else 0) + c.w; line.append(c)
        lines.append(line); self.lines = lines
        self.w = max(sum(c.w for c in l) + GAP * (len(l) - 1) for l in lines) + 2 * PAD
        self.h = TOP + sum(max(c.h for c in l) for l in lines) + GAP * (len(lines) - 1) + PAD
    def place(self, x, y):
        self.x, self.y = x, y
        if not self.children: return
        if self.mode == 'col':
            cy = y + TOP
            for c in self.children: c.place(x + PAD, cy); cy += c.h + GAP
            return
        cy = y + TOP
        for l in self.lines:
            cx = x + PAD
            for c in l: c.place(cx, cy); cx += c.w + GAP
            cy += max(c.h for c in l) + GAP

TYPE_FI = {'Goal': 'Tavoitteet', 'Constraint': 'Säädökset ja kansalliset vaatimukset', 'Capability': 'Kyvykkyydet', 'BusinessActor': 'Toimijat',
           'BusinessRole': 'Roolit', 'BusinessService': 'Palvelut', 'BusinessProcess': 'Prosessit', 'ApplicationComponent': 'Tietojärjestelmät',
           'DataObject': 'Tietoaineistot', 'Node': 'Teknologia-alustat', 'SystemSoftware': 'Ohjelmistot', 'Location': 'Sijainnit'}
def type_fi(t): return TYPE_FI.get(t, t)          # a new metamodel type still gets a view, with its English name

def build_views(world, metamodel):
    E = {e['id']: e for e in world['elements']}
    R = world['relationships']
    by_type = defaultdict(list)
    for e in world['elements']: by_type[e['type']].append(e)
    out = defaultdict(lambda: defaultdict(list)); inn = defaultdict(lambda: defaultdict(list))
    for r in R: out[r['type']][r['source']].append(r['target']); inn[r['type']][r['target']].append(r['source'])
    name = lambda i: E[i]['name']
    srt = lambda ids: sorted(set(ids), key=name)
    comp_children = lambda i: srt(t for t in out['Composition'][i] if E[t]['type'] == E[i]['type'])
    attr = lambda i, k: E[i]['attrs'].get(k)
    kind = lambda i: attr(i, 'actor_kind')
    actors = {e['key']: e['id'] for e in by_type['BusinessActor']}
    city_id = actors.get('alyla')
    divisions = sorted(d for d in comp_children(city_id) if kind(d) == 'division') if city_id else []   # model order
    parent = {t: s for s, ts in out['Composition'].items() for t in ts if E[s]['type'] == E[t]['type'] == 'BusinessActor'}
    def div_of_actor(a):
        while a in parent and kind(a) != 'division': a = parent[a]
        return a if kind(a) == 'division' else None
    unit_of = lambda a: parent[a] if kind(a) == 'subunit' and a in parent else a
    role_unit = {t: s for s, ts in out['Assignment'].items() for t in ts if E[t]['type'] == 'BusinessRole'}
    def div_of(eid):
        o = E[eid]['meta'].get('owner'); return div_of_actor(role_unit[o]) if o in role_unit else None
    def unit_owning(eid):
        # an information system's responsible unit: the unit (or sub-unit) it serves within its owner's division
        dv = div_of(eid)
        cand = sorted(unit_of(x) for x in out['Serving'][eid] if kind(x) in ('unit', 'subunit'))
        cand = [u for u in cand if dv is None or div_of_actor(u) == dv]
        return cand[0] if cand else None
    def order_groups(g):   # largest group first, "Muut ..." always last
        return sorted(g, key=lambda k: (k.startswith('Muut'), -len(g[k]), k))
    def grouped(t, items, group_of):   # groups ordered by size
        g = defaultdict(list)
        for i in items: g[group_of(i) or 'Muut'].append(i)
        return [Box(label=f"{type_fi(t)}: {k} ({len(g[k])})", children=[Box(i) for i in srt(g[k])]) for k in order_groups(g)]
    div_names = [name(d) for d in divisions]
    V = []
    focus = {}
    def num(i, n=None): return f'{i:02d}'   # two digits so Archi's alphabetical sorting keeps the order

    # ---------- Aloitusnäkymä
    cnt = Counter(e['type'] for e in world['elements'])
    contents = ', '.join(f"{type_fi(t)} {cnt[t]}" for t in metamodel['elements'] if cnt[t])
    d_ = world['world_today'].split('-')
    note = '\n'.join([
        MODEL_TITLE, "",
        "Synteettinen arkkitehtuurimalli kokonaisarkkitehtuurin tekoälykäyttötapausten kokeiluun. Kaikki nimet ja sisältö ovat kuvitteellisia.",
        "Säädökset perustuvat todelliseen lainsäädäntöön yleisellä tasolla, mutta eivät välttämättä heijasta oikeaa todellisuutta.",
        f"Versio {VERSION}. Maailman päivä on {int(d_[2])}.{int(d_[1])}.{d_[0]}.", "",
        VARIANTS.get(world.get('variant'), ('', '', '', ''))[3], "",
        "Kaupunki: noin 69 000 asukasta, neljä toimialaa (Konsernihallinto, Elinvoima, Kaupunkiympäristö, Sivistys), Älymaan maakunta.", "",
        f"Mallin sisältö: {contents}. Suhteita {len(R)}.", "",
        "Ominaisuudet: Elementeillä on vastuu-, lähde-, voimassaolo-, elinkaari- ja luokittelutiedot. Tietojärjestelmillä ja tietovirroilla on lisäksi",
        "tyyppikohtaisia ominaisuuksia.", "",
        "Näkymät:",
        "  01. Karttanäkymät – kunkin elementtityypin kaikki elementit ryhmiteltyinä",
        "  02. Kerrosnäkymät – toimialan kansiossa näkymä kustakin prosessista toimijoista sijainteihin",
        "  03. Integraationäkymät – kunkin yksikön tietojärjestelmien tietovirrat", "",
        "Näkymät tuotetaan uudelleen jokaisella generoinnilla: muutokset tehdään lähdeaineistoon, ei näkymiin."])
    V.append(((), 'Aloitusnäkymä', [Box(note=note)], set(), 'stack'))

    # ---------- Karttanäkymät
    def map_view(t):
        items = [e['id'] for e in by_type[t]]
        if t == 'BusinessActor':
            def g(a):
                k = kind(a)
                if k in ('division', 'unit', 'subunit'): return name(div_of_actor(a))
                return {'city': 'Kaupunki ja toimielimet', 'political_body': 'Kaupunki ja toimielimet', 'steering_group': 'Kaupunki ja toimielimet', 'customer_group': 'Asiakasryhmät'}.get(k, 'Konserniyhtiöt ja ulkoiset toimijat')
            return grouped(t, items, g)
        if t == 'BusinessRole':
            m = {'other': 'Johto', 'service_owner': 'Palveluomistajat', 'application_owner': 'Tietojärjestelmäomistajat'}
            return grouped(t, items, lambda i: m.get(attr(i, 'role_kind'), 'Muut roolit'))
        if t == 'Capability':
            l1 = srt(i for i in items if attr(i, 'level') == 1)
            def desc(c): return [x for ch in comp_children(c) for x in [ch] + desc(ch)]
            g = {name(c): [c] + desc(c) for c in l1}
            return [Box(label=f"{type_fi(t)}: {k} ({len(g[k])})", children=[Box(x) for x in g[k]]) for k in order_groups(g)]
        if t == 'BusinessService':
            return grouped(t, items, lambda i: name(div_of(i)) if div_of(i) else 'Ulkoiset tarjoajat')
        if t == 'BusinessProcess':
            pk = {'governance': 'Ohjausprosessit', 'core': 'Ydinprosessit', 'support': 'Tukiprosessit'}
            tops = srt(i for i in items if not inn['Composition'][i] or E[inn['Composition'][i][0]]['type'] != 'BusinessProcess')
            g = defaultdict(list)
            for p in tops: g[pk.get(attr(p, 'process_kind'), 'Muut')].append(p)
            n = {k: sum(1 + len(comp_children(p)) for p in v) for k, v in g.items()}
            return [Box(label=f"{type_fi(t)}: {k} ({n[k]})", children=[Box(p, children=[Box(c) for c in comp_children(p)], maxw=2 * W + 3 * PAD) for p in g[k]])
                    for k in sorted(g, key=lambda k: (k.startswith('Muut'), -n[k], k))]
        if t == 'DataObject':
            return grouped(t, items, lambda i: name(div_of(i)) if div_of(i) else 'Konserniyhtiöt')
        if t == 'Constraint':
            def area(c):
                ds = {div_of(x) for x in inn['Realization'][c] + out['Association'][c]} - {None}
                ds = {name(d) for d in ds}
                return ds.pop() if len(ds) == 1 and 'Konsernihallinto' not in ds else 'Yleishallinto'
            return grouped(t, items, area)
        if t == 'ApplicationComponent':
            def g(a):
                if div_of(a): return name(div_of(a))
                return 'Kansalliset palvelut' if attr(a, 'deployment') == 'national_service' else 'Konserniyhtiöt ja hyvinvointialue'
            return grouped(t, items, g)
        if t == 'Node':
            def g(n):
                m = E[n]['meta']
                if m.get('owner'): return 'Kaupungin omat'
                return 'Toimittajien' if m.get('provider') == 'toimittaja' else 'Kansalliset ja ulkoiset'
            return grouped(t, items, g)
        if t == 'SystemSoftware':
            m = {'os': 'Käyttöjärjestelmät', 'database': 'Tietokannat', 'runtime': 'Ajoympäristöt'}
            return grouped(t, items, lambda i: m.get(attr(i, 'software_kind'), 'Muut ohjelmistot'))
        if t == 'Location':
            m = {'datacenter': 'Konesalit', 'cloud_region': 'Pilvialueet', 'site': 'Toimipisteet'}
            return grouped(t, items, lambda i: m.get(attr(i, 'location_kind'), 'Muut'))
        return [Box(label=f"{type_fi(t)} ({len(items)})", children=[Box(i) for i in srt(items)])]
    LAYER_ORDER = ['Goal', 'Constraint', 'Capability', 'BusinessActor', 'BusinessRole', 'BusinessService', 'BusinessProcess', 'DataObject',
                   'ApplicationComponent', 'SystemSoftware', 'Node', 'Location']
    types = [t for t in LAYER_ORDER if t in metamodel['elements']] + [t for t in metamodel['elements'] if t not in LAYER_ORDER]
    types = [t for t in types if by_type[t]]
    for i, t in enumerate(types, 1):
        V.append(((f'{num(1)}. Karttanäkymät',), f"{num(i, len(types))}. {type_fi(t)}", map_view(t), set(), 'stack'))

    # ---------- Kerrosnäkymät: folder per division, view per process; one band per element type
    def band(label, ids):
        return Box(label=label, children=[Box(x) for x in ids]) if ids else None
    layered = defaultdict(list)
    for p in sorted(e['id'] for e in by_type['BusinessProcess'] if not comp_children(e['id'])):
        resp = [a for a in inn['Assignment'][p] if E[a]['type'] == 'BusinessActor']
        svcs = srt(s for s in out['Realization'][p] if E[s]['type'] == 'BusinessService')
        acts = srt(resp + [c for s in svcs for c in out['Serving'][s] if E[c]['type'] == 'BusinessActor'])
        apps = srt(a for a in inn['Serving'][p] if E[a]['type'] == 'ApplicationComponent')
        data = srt([x for a in apps for x in out['Access'][a]] + out['Access'][p])
        sws = srt(x for a in apps for x in inn['Serving'][a] if E[x]['type'] == 'SystemSoftware')
        nodes = srt(x for a in apps for x in inn['Serving'][a] if E[x]['type'] == 'Node')
        locs = srt(l for n in nodes for l in inn['Aggregation'][n] if E[l]['type'] == 'Location')
        bands = [band('Toimijat', acts), band('Palvelut', svcs), band('Prosessi', [p]), band('Tietojärjestelmät', apps),
                 band('Tietoaineistot', data), band('Ohjelmistot', sws), band('Teknologia-alustat', nodes), band('Sijainnit', locs)]
        layered[div_of(p)].append((p, [b for b in bands if b]))
    for di, dv in enumerate([d for d in divisions if layered[d]] + ([None] if layered[None] else []), 1):
        folder = name(dv) if dv else 'Muut'
        for pi, (p, bands) in enumerate(layered[dv], 1):
            V.append(((f'{num(2)}. Kerrosnäkymät', folder), name(p), bands,
                      {'Realization', 'Serving', 'Assignment', 'Access', 'Aggregation', 'Composition'}, 'stack'))

    # ---------- Integraationäkymät: senders | the unit's systems | receivers
    flows = [r for r in R if r['type'] == 'Flow']
    platforms = {e['id'] for e in by_type['ApplicationComponent'] if e['key'] == 'vayla'} | {e['id'] for e in by_type['Node'] if e['key'] == 'kansallinen_tiedonvalityskerros'}
    units = sorted(e['id'] for e in by_type['BusinessActor'] if kind(e['id']) == 'unit')
    integ = []
    for u in units:
        own = {a['id'] for a in by_type['ApplicationComponent'] if unit_owning(a['id']) == u}
        uf = [r for r in flows if r['source'] in own or r['target'] in own]
        if not uf: continue
        mine = {x for r in uf for x in (r['source'], r['target']) if x in own}
        # senders: sources of flows into the unit's systems; receivers: targets of flows out of them.
        # A flow between two of the unit's own systems is drawn to a copy of the receiving system on the right.
        senders = srt(r['source'] for r in uf if r['source'] not in own)
        receivers = srt(r['target'] for r in uf if r['source'] in own)
        cols = []
        if senders: cols.append(Box(label='Lähettävät tietojärjestelmät', children=[Box(a, role='sender') for a in senders], mode='col'))
        cols.append(Box(label=f"Tietojärjestelmät: {name(u)}", children=[Box(a, role='mine') for a in srt(mine)], mode='col'))
        if receivers: cols.append(Box(label='Vastaanottavat tietojärjestelmät', children=[Box(a, role='receiver') for a in receivers], mode='col'))
        plats = srt(x for a in mine for x in inn['Serving'][a] if x in platforms)
        if plats: cols.append(Box(label='Integraatioalustat', children=[Box(x) for x in plats]))
        integ.append((name(u), cols, set(mine)))
    for n, cols, mine in integ:
        V.append(((f'{num(3)}. Integraationäkymät',), n, cols, {'Flow', 'Serving:platform'}, 'integration'))
        focus[n] = mine
    return V, (platforms, focus)

def render_views(world, metamodel, escape):
    """Returns (views xml, organizations xml)."""
    E = {e['id']: e for e in world['elements']}
    views, (platforms, focus) = build_views(world, metamodel)
    out = ['<views><diagrams>']; folders = {}
    for vi, (folder, vname, boxes, rel_types, arrange) in enumerate(views, 1):
        vid = f'view-{vi:03d}'
        folders.setdefault(folder, []).append(vid)
        for b in boxes: b.measure()
        x, y, rowh, placed = 20, 20, 0, {}
        for b in boxes:
            if arrange == 'stack': b.place(20, y); y += b.h + 40
            elif arrange == 'integration' and b.label == 'Integraatioalustat':
                mid = next(c for c in boxes if (c.label or '').startswith('Tietojärjestelmät:'))
                b.place(mid.x, y + rowh + 60)   # below the unit's own systems
            else:
                if x > 20 and x + b.w > 3200: x, y, rowh = 20, y + rowh + 40, 0
                b.place(x, y); x += b.w + (120 if arrange == 'integration' else 40); rowh = max(rowh, b.h)
        counter = [0]
        def node_xml(b):
            counter[0] += 1; nid = f'{vid}-n{counter[0]:03d}'
            if b.note:
                return f'<node identifier="{nid}" xsi:type="Label" x="{b.x}" y="{b.y}" w="{b.w}" h="{b.h}"><label xml:lang="fi">{escape(b.note)}</label></node>'
            if b.elem: placed.setdefault(b.elem, {})[b.role] = nid
            inner = ''.join(node_xml(c) for c in b.children)
            if b.elem:
                return f'<node identifier="{nid}" elementRef="{b.elem}" xsi:type="Element" x="{b.x}" y="{b.y}" w="{b.w}" h="{b.h}">{inner}</node>'
            return f'<node identifier="{nid}" xsi:type="Container" x="{b.x}" y="{b.y}" w="{b.w}" h="{b.h}"><label xml:lang="fi">{escape(b.label)}</label>{inner}</node>'
        nodes = ''.join(node_xml(b) for b in boxes)
        conns = []
        for r in world['relationships']:
            ok = r['type'] in rel_types or ('Serving:platform' in rel_types and r['type'] == 'Serving'
                                            and r['source'] in platforms and r['target'] in focus.get(vname, ()))
            if not (ok and r['source'] in placed and r['target'] in placed): continue
            ps, pt = placed[r['source']], placed[r['target']]
            if arrange == 'integration' and r['type'] == 'Flow':
                src = ps.get('mine') if r['source'] in focus.get(vname, ()) else ps.get('sender')
                tgt = pt.get('mine') if r['source'] not in focus.get(vname, ()) else pt.get('receiver')
            elif arrange == 'integration':
                src, tgt = ps.get('main'), pt.get('mine')
            else:
                src, tgt = next(iter(ps.values())), next(iter(pt.values()))
            if src and tgt:
                conns.append(f'<connection identifier="{vid}-c{len(conns)+1:04d}" relationshipRef="{r["id"]}" xsi:type="Relationship" source="{src}" target="{tgt}"/>')
        out.append(f'<view identifier="{vid}" xsi:type="Diagram"><name xml:lang="fi">{escape(vname)}</name>{nodes}{"".join(conns)}</view>')
    out.append('</diagrams></views>')
    # folder tree for views (Archi "Views" folder)
    tree = {}
    for path_, vids in folders.items():
        node = tree
        for p in path_: node = node.setdefault(p, {})
        node.setdefault('__views__', []).extend(vids)
    def org(node):
        s = ''.join(f'<item identifierRef="{v}"/>' for v in node.get('__views__', []))
        for k in sorted(k for k in node if k != '__views__'):
            s += f'<item><label xml:lang="fi">{escape(k)}</label>{org(node[k])}</item>'
        return s
    orgs = f'<organizations><item><label xml:lang="en">Views</label>{org(tree)}</item></organizations>'
    return ''.join(out), orgs, len(views)
