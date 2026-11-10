# Genera in src/data1.json i pranzi e le cene condivisi (Roberto + Francesca),
# con verdure esplicite, kcal/macro calcolati e lista della spesa delle proteine,
# dei carboidrati e delle verdure. Uso: python3 tools/piatti.py && python3 build.py
import json, re
DB = {  # per 100 g crudi: kcal, P, C, G
 'Pasta integrale': (355, 13, 66, 2.5), 'Riso (basmati o integrale)': (355, 7.5, 78, 1), 'Farro o orzo': (335, 13, 67, 2.5),
 'Legumi secchi': (330, 22, 50, 2), 'Pane integrale': (250, 8.5, 47, 1.5), 'Pangrattato': (360, 12, 72, 4),
 'Straccetti di tacchino': (110, 23, 0, 1.5), 'Petto di pollo (o tacchino)': (110, 23, 0, 1.5), 'Macinato di pollo o tacchino': (120, 20, 0, 4.5),
 'Macinato di manzo magro (5% grassi)': (137, 21, 0, 5), 'Bistecca / vitello / manzo': (130, 22, 0, 4.5), 'Tofu naturale': (145, 15, 2, 9),
 'Salmone': (185, 20, 0, 12), 'Merluzzo o orata': (90, 18, 0, 1.5),
 'Uova': (140, 12.5, 0.5, 10), 'Albumi': (50, 11, 0.7, 0.2), 'Mozzarella light': (165, 20, 1, 9), 'Parmigiano': (392, 33, 0, 28),
 'Olio EVO': (900, 0, 0, 100), 'Passata di pomodoro': (23, 1.3, 4, 0.2), 'Salsa di soia': (60, 10, 5, 0),
 'Zucchine': (17, 1.3, 2, 0.1), 'Spinaci': (23, 2.9, 1.5, 0.4), 'Finocchi': (20, 1.2, 3, 0.2), 'Piselli': (70, 5.5, 9, 0.4),
}
VEGS = ['Zucchine', 'Spinaci', 'Finocchi', 'Piselli']
EGG = 50  # g per uovo
def item(n, g, u='g'):
  if n == 'Uova': return [n, '%d (%d g)' % (round(g / EGG), g), g]
  return [n, '%d %s' % (g, 'ml' if n in ('Olio EVO', 'Salsa di soia') else u), g]
def meal(label, time, ing, **kw):
  k = p = c = f = 0; items = []
  for n, g in ing:
    d = DB[n]; k += d[0] * g / 100; p += d[1] * g / 100; c += d[2] * g / 100; f += d[3] * g / 100
    items.append(item(n, g)[:2])
  m = {'time': time, 'label': label, 'kcal': round(k), 'p': round(p, 1), 'f': round(f, 1), 'c': round(c, 1), 'veg': None, 'items': items, 'ing': ing}
  m.update(kw); return m

# piatto: (nome, [ingredienti Roberto], [ingredienti Francesca], extra)
PRA = {
 'pastaTacchino': ('Pasta e straccetti di tacchino', [('Pasta integrale', 70), ('Straccetti di tacchino', 130), ('Olio EVO', 5), ('Zucchine', 200)],
                   [('Pasta integrale', 60), ('Straccetti di tacchino', 90), ('Olio EVO', 5), ('Zucchine', 150)], {'carb': True}),
 'lcUova': ('Uova e mozzarella', [('Uova', 150), ('Mozzarella light', 125), ('Olio EVO', 5), ('Finocchi', 250)],
            [('Uova', 100), ('Mozzarella light', 60), ('Olio EVO', 5), ('Finocchi', 150), ('Pane integrale', 50)], {'carb': False, 'notaF': 'Per Francesca con 50 g di pane integrale'}),
 'risoPollo': ('Riso, pollo e piselli', [('Riso (basmati o integrale)', 70), ('Petto di pollo (o tacchino)', 130), ('Olio EVO', 5), ('Piselli', 100), ('Zucchine', 100)],
               [('Riso (basmati o integrale)', 60), ('Petto di pollo (o tacchino)', 90), ('Olio EVO', 5), ('Piselli', 80), ('Zucchine', 70)], {'carb': True}),
 'lcPollo': ('Pollo e parmigiano', [('Petto di pollo (o tacchino)', 170), ('Parmigiano', 20), ('Olio EVO', 10), ('Spinaci', 250)],
             [('Petto di pollo (o tacchino)', 120), ('Parmigiano', 15), ('Olio EVO', 5), ('Spinaci', 150), ('Pane integrale', 50)], {'carb': False, 'notaF': 'Per Francesca con 50 g di pane integrale'}),
 'prcL': ('Legumi e cereale', [('Farro o orzo', 60), ('Legumi secchi', 30), ('Parmigiano', 10), ('Petto di pollo (o tacchino)', 80), ('Olio EVO', 5), ('Zucchine', 100), ('Spinaci', 100)],
          [('Farro o orzo', 50), ('Legumi secchi', 30), ('Parmigiano', 10), ('Petto di pollo (o tacchino)', 50), ('Olio EVO', 5), ('Zucchine', 80), ('Spinaci', 70)], {'carb': True}),
 'pastaRagu': ('Pasta al ragù magro', [('Pasta integrale', 100), ('Macinato di manzo magro (5% grassi)', 120), ('Passata di pomodoro', 150), ('Parmigiano', 15), ('Olio EVO', 5), ('Finocchi', 200)],
               [('Pasta integrale', 70), ('Macinato di manzo magro (5% grassi)', 80), ('Passata di pomodoro', 120), ('Parmigiano', 10), ('Olio EVO', 5), ('Finocchi', 150)], {'carb': True}),
}
CEN = {
 'cenUova': ('Frittata', [('Uova', 100), ('Albumi', 200), ('Parmigiano', 15), ('Olio EVO', 5), ('Spinaci', 200)],
             [('Uova', 50), ('Albumi', 150), ('Parmigiano', 10), ('Olio EVO', 5), ('Spinaci', 150)], {}),
 'cenTofu': ('Tofu saltato', [('Tofu naturale', 250), ('Olio EVO', 5), ('Salsa di soia', 15), ('Zucchine', 100), ('Piselli', 100)], None, {}),
 'cenPolp': ('Polpette di pollo al sugo', [('Macinato di pollo o tacchino', 180), ('Parmigiano', 10), ('Pangrattato', 10), ('Passata di pomodoro', 150), ('Olio EVO', 5), ('Zucchine', 200)],
             [('Macinato di pollo o tacchino', 130), ('Parmigiano', 8), ('Pangrattato', 8), ('Passata di pomodoro', 120), ('Olio EVO', 4), ('Zucchine', 150)], {}),
 'cenCar': ('Carne rossa', [('Bistecca / vitello / manzo', 180), ('Olio EVO', 10), ('Finocchi', 200)],
            [('Bistecca / vitello / manzo', 120), ('Olio EVO', 8), ('Finocchi', 150)], {}),
 'cenPol': ('Pollo / tacchino', [('Petto di pollo (o tacchino)', 190), ('Olio EVO', 12), ('Zucchine', 100), ('Spinaci', 100)],
            [('Petto di pollo (o tacchino)', 140), ('Olio EVO', 10), ('Zucchine', 80), ('Spinaci', 70)], {}),
}
# pesce per Francesca: stessa verdura del piatto di Roberto
FISH = {'Martedì': ('Salmone', [('Salmone', 140), ('Zucchine', 80), ('Piselli', 70)]),
        'Venerdì': ('Merluzzo o orata', [('Merluzzo o orata', 200), ('Olio EVO', 8), ('Zucchine', 80), ('Spinaci', 70)])}
WEEK = {'Lunedì': ('pastaTacchino', 'cenUova'), 'Martedì': ('lcUova', 'cenTofu'), 'Mercoledì': ('risoPollo', 'cenPolp'),
        'Giovedì': ('lcPollo', 'cenCar'), 'Venerdì': ('prcL', 'cenPol'), 'Sabato': ('pastaRagu', 'cenLib'), 'Domenica': ('libero', 'cenPol')}

D = json.load(open('src/data1.json', encoding='utf-8'))
lib_r = D['PRA_R']['libero']; lib_r['items'] = [['Pasto libero — macro indicativi', '']]; lib_r.update(kcal=584, p=29.5, f=21.7, c=60.5)
D['PRA_R'] = {'libero': lib_r}
for k, (n, r, f, x) in PRA.items():
  D['PRA_R'][k] = meal('Pranzo 12:30 — ' + n + ('' if x.get('carb', True) else ' (senza carboidrati)'), '12:30', r, carb=x.get('carb', True))
cen_lib = D['CEN_R']['cenLib']; D['CEN_R'] = {'cenLib': cen_lib}
for k, (n, r, f, x) in CEN.items(): D['CEN_R'][k] = meal('Cena — ' + n, '19:30', r)
for w in D['WEEK']:
  pk, ck = WEEK[w['day']]; w['praRk'], w['cenR'] = pk, ck
  if pk in PRA:
    n, r, f, x = PRA[pk]; w['praFm'] = meal('Pranzo — ' + n, '13:00', f); w['praFm']['slot'] = 'praL' if pk == 'prcL' else None
    if x.get('notaF'): w['praFm']['hint'] = x['notaF']
  else: w['praFm'] = dict(D['PRA_F']['libero'], ing=[])
  if w['day'] in FISH:
    n, ing = FISH[w['day']]; w['cenFm'] = meal('Cena — ' + n, '20:00', ing); w['cenFm']['slot'] = 'cenSal' if n == 'Salmone' else None
    w['cenFm']['hint'] = 'Pesce solo per Francesca, stessa verdura di Roberto.'; w['fishF'] = n
  elif ck in CEN:
    n, r, f, x = CEN[ck]; w['cenFm'] = meal('Cena — ' + n, '20:00', f); w['cenFm']['slot'] = ck if ck in ('cenPol', 'cenCar', 'cenPolp') else None
  else: w['cenFm'] = dict(D['CEN_F']['cenLib'], ing=[])
# lista della spesa: proteine, carboidrati, verdure (somma settimanale dei due)
tot = {}
def add(ing, who):
  for n, g in ing: tot.setdefault(n, {'R': 0, 'F': 0})[who] += g
for w in D['WEEK']:
  for key, src in (('praRk', 'PRA_R'), ('cenR', 'CEN_R')):
    add(D[src][w[key]].get('ing', []), 'R')
  add(w['praFm'].get('ing', []), 'F'); add(w['cenFm'].get('ing', []), 'F')
def fmt(n):
  t = tot.get(n); g = t['R'] + t['F']
  s = ('%d pz' % round(g / EGG)) if n == 'Uova' else ('%.1f kg' % (g / 1000)).replace('.', ',') if g >= 1000 else '%d g' % (round(g / 10) * 10)
  who = ' (solo Rob)' if not t['F'] else ' (solo Fra)' if not t['R'] else ''
  return ['Pesce: ' + n.lower() if n in ('Salmone', 'Merluzzo o orata') else n, '~' + s + who]
CARB = ['Pasta integrale', 'Riso (basmati o integrale)', 'Farro o orzo', 'Legumi secchi', 'Pane integrale']
PROT = ['Petto di pollo (o tacchino)', 'Straccetti di tacchino', 'Macinato di pollo o tacchino', 'Macinato di manzo magro (5% grassi)', 'Bistecca / vitello / manzo',
        'Tofu naturale', 'Salmone', 'Merluzzo o orata', 'Uova', 'Albumi', 'Mozzarella light']
for cat in D['SHOP']:
  if cat['cat'].startswith('🌾'): cat['items'] = [fmt(n) for n in CARB if n in tot]
  if cat['cat'].startswith('🥩'):
    cat['items'] = [fmt(n) for n in PROT if n in tot]
    u = tot['Uova']; cat['items'][[x[0] for x in cat['items']].index('Uova')][1] = '~%d pz (+ quelle delle colazioni di Fra)' % round((u['R'] + u['F']) / EGG)
    cat['items'] += [['Parmigiano', '~250 g'], ['Ricotta light', '~80 g (Fra)']]
  if cat['cat'].startswith('🥦'):
    cat['cat'] = '🥦 Verdura della settimana'; cat['items'] = [fmt(n) for n in VEGS]
  if cat['cat'].startswith('🧴'):
    cat['items'] = [x for x in cat['items'] if not x[0].startswith(('Passata', 'Olio'))] + [['Passata di pomodoro', '~%d g' % (tot['Passata di pomodoro']['R'] + tot['Passata di pomodoro']['F'])], ['Olio EVO', '~250 ml'], ['Salsa di soia', 'piccola bottiglia']]
for src in ('PRA_R', 'CEN_R'):
  for m in D[src].values(): m.pop('ing', None)
for w in D['WEEK']: w['praFm'].pop('ing', None); w['cenFm'].pop('ing', None)
json.dump(D, open('src/data1.json', 'w', encoding='utf-8'), ensure_ascii=False)
for w in D['WEEK']: print(w['day'], w['praFm']['label'], w['praFm']['kcal'], '|', w['cenFm']['label'], w['cenFm']['kcal'])
for c in D['SHOP'][2:6]: print(c['cat'], c['items'])
