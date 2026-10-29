import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('App/template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ['class="tab', 'class="nav', '<nav', 'switchTab', 'tab-button']):
        print(f"{i+1}: {l.strip()[:100]}")
