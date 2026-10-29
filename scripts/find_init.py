import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('App/template.html', 'r', encoding='utf-8') as f:
    text = f.read()

for term in ['window.onload', 'DOMContentLoaded', 'initApp', 'loadStats', 'loadProducts']:
    idx = 0
    while True:
        pos = text.find(term, idx)
        if pos == -1:
            break
        print(f"Found {term} at {pos}:")
        print(text[max(0, pos-50):min(len(text), pos+200)])
        print("---")
        idx = pos + len(term)
        if idx > pos + 1000:
            break
