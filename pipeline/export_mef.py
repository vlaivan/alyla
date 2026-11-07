"""Export the model variants as ArchiMate Model Exchange Format (MEF) XML for Archi:
the base version (perusversio) and the test version (testiversio, planted gaps and noise). Names in labels.py."""
import json, os
from xml.sax.saxutils import escape
from common import path, load
from views import render_views
from labels import VARIANTS, MODEL_TITLE, VERSION

NS = 'http://www.opengroup.org/xsd/archimate/3.0/'

def export(src, dst, variant, model_name, variant_line):
    world = json.load(open(path('build', src), encoding='utf-8'))
    world['variant'] = variant
    names = {e['id']: e['name'] for e in world['elements']}
    ACCESS = {'read': 'Read', 'write': 'Write', 'readwrite': 'ReadWrite'}
    PROP_ORDER = ['owner', 'owner_name', 'provider', 'external', 'source', 'last_confirmed', 'lifecycle', 'valid_from', 'valid_to', 'classification']
    pdefs = {}
    def pd(k):
        if k not in pdefs: pdefs[k] = f'pd-{len(pdefs)+1:02d}'
        return pdefs[k]
    def props(meta, attrs):
        items = []
        m = dict(meta)
        if 'owner' in m: m['owner_name'] = names.get(m['owner'], '')
        for k in PROP_ORDER:
            if k in m: items.append((k, m[k]))
        for k, v in attrs.items():
            if k not in ('access_type', 'via'): items.append((k, v))
            elif k == 'via': items.append((k, v))
        out = ['<properties>']
        for k, v in items:
            v = str(v).lower() if isinstance(v, bool) else str(v)
            out.append(f'<property propertyDefinitionRef="{pd(k)}"><value xml:lang="fi">{escape(v)}</value></property>')
        out.append('</properties>')
        return ''.join(out) if items else ''
    def text(tag, v): return f'<{tag} xml:lang="fi">{escape(v)}</{tag}>' if v else ''

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             f'<model xmlns="{NS}" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
             f'xsi:schemaLocation="{NS} http://www.opengroup.org/xsd/archimate/3.1/archimate3_Diagram.xsd" identifier="alyla-model">',
             text('name', model_name),
             text('documentation', f"{MODEL_TITLE}, versio {VERSION}. Kaikki sisältö on kuvitteellista. {variant_line} Maailman päivä {world['world_today']}, siemen {world['seed']}."),
             '<elements>']
    for e in world['elements']:
        lines.append(f'<element identifier="{e["id"]}" xsi:type="{e["type"]}">{text("name", e["name"])}{text("documentation", e.get("description"))}'
                     f'{props(e["meta"], e["attrs"])}</element>')
    lines.append('</elements><relationships>')
    for r in world['relationships']:
        extra = ''
        if r['type'] == 'Access': extra = f' accessType="{ACCESS[r["attrs"]["access_type"]]}"'
        if r['type'] == 'Association': extra = ' isDirected="true"'
        lines.append(f'<relationship identifier="{r["id"]}" source="{r["source"]}" target="{r["target"]}" xsi:type="{r["type"]}"{extra}>'
                     f'{text("name", r.get("name"))}{props(r["meta"], r["attrs"])}</relationship>')
    views_xml, orgs_xml, nviews = render_views(world, load('metamodel.yaml'), escape)
    lines.append('</relationships>')
    lines.append(orgs_xml)
    lines.append('<propertyDefinitions>')
    for k, i in pdefs.items():
        lines.append(f'<propertyDefinition identifier="{i}" type="string"><name xml:lang="fi">{k}</name></propertyDefinition>')
    lines.append('</propertyDefinitions>')
    lines.append(views_xml)
    lines.append('</model>')
    os.makedirs(path('export'), exist_ok=True)
    with open(path('export', dst), 'w', encoding='utf-8') as f: f.write('\n'.join(lines))
    print(dst + ':', len(world['elements']), 'elements,', len(world['relationships']), 'relationships,', len(pdefs), 'property definitions,', nviews, 'views')

for variant, (src, dst, model_name, line) in VARIANTS.items():
    if os.path.exists(path('build', src)): export(src, dst, variant, model_name, line)
