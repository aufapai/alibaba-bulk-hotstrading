# -*- coding: utf-8 -*-
with open('App/photobank_api_bridge.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '["AP 1", "AP 2003", "AP 2005", "AP 2006", "AP 2007", "AP 2011", "AP 2017", "AP 2018", "9303", "9506", "CLASSIC", "PRO GREEN", "XTR"]'
replacement = '["AP 1", "2003", "2005", "2006", "2007", "2011", "2017", "2018", "9303", "9506", "CLASSIC", "PRO GREEN", "XTR", "TRICOLOUR"]'

if target in text:
    text = text.replace(target, replacement)
    with open('App/photobank_api_bridge.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated categories successfully!")
else:
    print("Target not found, let's verify line")
