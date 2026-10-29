with open('App/template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function switchSourceTab' in l:
        print(f"switchSourceTab starts at line {i+1}")
        for j in range(i, min(len(lines), i + 35)):
            print(f"{j+1}: {lines[j]}", end='')
        break
