# Ricostruisce index.html da src/: python3 build.py
import json
a = open('src/app.html', encoding='utf-8').read()
d = json.dumps(json.load(open('src/data1.json', encoding='utf-8')), ensure_ascii=False, separators=(',', ':'))
r = json.dumps(json.load(open('src/ric.json', encoding='utf-8')), ensure_ascii=False, separators=(',', ':'))
open('index.html', 'w', encoding='utf-8').write(a.replace('/*DATA*/', d).replace('/*RIC*/', r))
