with open('App/template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'class="modal-overlay"' in l or 'id="jsonModal"' in l:
        print(f"{i+1}: {l.strip()[:100]}")

