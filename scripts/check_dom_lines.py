with open('App/template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'DOMContentLoaded' in l:
        print(f"DOMContentLoaded at line {i+1}")
        for j in range(i, min(len(lines), i + 25)):
            print(f"{j+1}: {lines[j]}", end='')
        break
