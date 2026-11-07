"""Validate every built world variant (clean, planted, test) against metamodel.yaml, and the records.
Deviations that planted findings break on purpose are declared in plants.yaml and accepted."""
import json, re, sys
from collections import Counter
from common import load, path, slug

import os
mm = load('metamodel.yaml')
from labels import VERSION
assert str(mm['version']) == VERSION, f"metamodel version {mm['version']} != {VERSION}"
VARIANTS = [('clean', 'world.json'), ('planted', 'world-planted.json'), ('test', 'world-test.json')]
def run(variant, fname):
  w = json.load(open(path('build', fname), encoding='utf-8'))
  declared = set()          # deviations declared by planted findings
  if variant != 'clean' and os.path.exists(path('build', 'plants.json')):
      for p in json.load(open(path('build', 'plants.json'), encoding='utf-8')):
          for code in p['expected_deviations']: declared |= {(x, code) for x in p['elements']}
  errors = []
  types = mm['elements']; allowed = {(t.capitalize(), s, d) for t, pairs in mm['relationships'].items() for s, d in pairs}
  enum_life = set(mm['metadata']['required']['lifecycle']); enum_cls = set(mm['metadata']['required']['classification'])
  E = {e['id']: e for e in w['elements']}
  for e in w['elements']:
      t = e['type']
      if t not in types: errors.append(f"{e['id']}: unknown type {t}"); continue
      if not re.fullmatch(types[t]['prefix'] + r'-\d{4}', e['id']): errors.append(f"{e['id']}: bad id for {t}")
      if e['key'] != slug(e['name']) and t != 'BusinessActor' or (t == 'BusinessActor' and e['key'] not in ('alyla',) and e['key'] != slug(e['name'])):
          errors.append(f"{e['id']}: key {e['key']} does not match name")
      m = e['meta']
      for k in ('source', 'last_confirmed', 'lifecycle', 'valid_from', 'classification'):
          if k not in m: errors.append(f"{e['id']}: missing {k}")
      if m.get('last_confirmed', '9') < m.get('valid_from', '0'): errors.append(f"{e['id']}: confirmed before it came into use")
      if not m.get('owner') and not m.get('provider') and (e['id'], 'no_owner') not in declared: errors.append(f"{e['id']}: neither owner nor provider")
      if m.get('owner') and E.get(m['owner'], {}).get('type') != 'BusinessRole': errors.append(f"{e['id']}: owner is not a role")
      if m.get('lifecycle') not in enum_life: errors.append(f"{e['id']}: lifecycle")
      if m.get('classification') not in enum_cls: errors.append(f"{e['id']}: classification")
      for k, spec in (types[t].get('attributes') or {}).items():
          if isinstance(spec, list) and k in e['attrs'] and e['attrs'][k] not in spec:
              errors.append(f"{e['id']}: {k}={e['attrs'][k]} not in {spec}")
  for r in w['relationships']:
      s, d = E.get(r['source']), E.get(r['target'])
      if not s or not d: errors.append(f"{r['id']}: dangling"); continue
      if (r['type'], s['type'], d['type']) not in allowed: errors.append(f"{r['id']}: {r['type']} {s['type']} -> {d['type']} not allowed")
  # organisation hierarchy: every division, unit, subunit and political body has a parent
  child = {r['target'] for r in w['relationships'] if r['type'] == 'Composition' and E[r['source']]['type'] == 'BusinessActor'}
  for e in w['elements']:
      if e['type'] == 'BusinessActor' and e['attrs'].get('actor_kind') in ('division', 'unit', 'subunit', 'political_body', 'steering_group') and e['id'] not in child:
          errors.append(f"{e['id']}: {e['name']} has no parent in the organisation")
  # duplicate keys within type
  for (t, k), n in Counter((e['type'], e['key']) for e in w['elements']).items():
      if n > 1: errors.append(f"duplicate key {t}:{k}")
  # ---------------------------------------------------------------- records (if built)

  DOC_ONLY = {'user_count'}          # facts that exist only in a document, not in the model
  nrec = 0
  if variant == 'clean' and os.path.exists(path('build', 'records.json')):
      rec = json.load(open(path('build', 'records.json'), encoding='utf-8'))
      spec = mm['records']['PRI']['fields']
      for p in rec['principles']:
          nrec += 1
          if not re.fullmatch(r'PRI-\d{4}', p['id']): errors.append(f"{p['id']}: bad id")
          if p['key'] != slug(p['title']): errors.append(f"{p['id']}: key does not match title")
          if p['category'] not in spec['category']: errors.append(f"{p['id']}: category")
          if p['status'] not in spec['status']: errors.append(f"{p['id']}: status")
          if E.get(p['owner'], {}).get('type') != 'BusinessRole': errors.append(f"{p['id']}: owner is not a role")
          if E.get(p['approved_by'], {}).get('attrs', {}).get('actor_kind') != 'steering_group': errors.append(f"{p['id']}: approver is not a steering group")
      kinds = mm['records']['DOC']['fields']['kind']
      for d in rec['documents']:
          nrec += 1
          if d['kind'] not in kinds: errors.append(f"{d['id']}: kind")
          for m in d['mentions']:
              if m not in E: errors.append(f"{d['id']}: mentions unknown {m}")
          for f in d['facts']:
              e = E.get(f['subject'])
              if not e: errors.append(f"{d['id']}: fact about unknown {f['subject']}"); continue
              if f['field'] in DOC_ONLY: continue
              actual = e['name'] if f['field'] == 'name' else e['meta'].get(f['field'], e['attrs'].get(f['field']))
              if actual != f['value']:
                  errors.append(f"{d['id']}: fact {f['subject']}.{f['field']} = {f['value']!r}, world has {actual!r}")
  print(f"validate {variant}: {len(w['elements'])} elements, {len(w['relationships'])} relationships, {nrec} records, {len(errors)} errors"
        + (f", {len(declared)} declared deviations" if declared else ''))
  for x in errors[:40]: print('  ', x)
  return len(errors)
fails = sum(run(v_, f) for v_, f in VARIANTS if os.path.exists(path('build', f)))
sys.exit(1 if fails else 0)
