with open('App/template.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'\.source-tab\b', text)
for m in matches:
    print(text[m.start():m.start()+400])
    print('---')

