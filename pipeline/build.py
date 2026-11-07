"""Build everything in order: clean world, records, planted findings, noise, answers, validation, exports, truth card."""
import subprocess, sys, os
STEPS = ['generate.py', 'records.py', 'plant.py', 'noise.py', 'answers.py', 'validate.py', 'export_mef.py', 'truthcard.py', 'readme.py']
here = os.path.dirname(os.path.abspath(__file__))
for s in STEPS:
    print(f'== {s}')
    r = subprocess.run([sys.executable, os.path.join(here, s)], cwd=here)
    if r.returncode: sys.exit(f'{s} failed')
print('done')
