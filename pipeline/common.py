"""Shared helpers for the Älylä pipeline."""
import re, os, yaml, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def path(*p): return os.path.join(ROOT, *p)
def load(*p):
    with open(path(*p), encoding='utf-8') as f: return yaml.safe_load(f)
def slug(n):
    n = n.lower().replace('ä', 'a').replace('ö', 'o').replace('å', 'a')
    return re.sub(r'[^a-z0-9]+', '_', n).strip('_')

class IdRegistry:
    """Stable IDs: (type prefix, key) -> PREFIX-NNNN, persisted in state/ids.yaml and never reused."""
    def __init__(self, file=('state', 'ids.yaml')):
        self.file = path(*file)
        self.ids = {}
        if os.path.exists(self.file):
            self.ids = load(*file) or {}
    def get(self, prefix, key):
        table = self.ids.setdefault(prefix, {})
        if key not in table:
            n = max([int(v.split('-')[1]) for v in table.values()] or [0]) + 1
            table[key] = f'{prefix}-{n:04d}'
        return table[key]
    def save(self):
        with open(self.file, 'w', encoding='utf-8') as f:
            f.write('# Stable ID registry. Generated; edit only to retire or migrate keys. IDs are never reused.\n')
            yaml.safe_dump(self.ids, f, allow_unicode=True, sort_keys=True)
