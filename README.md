# Piano alimentare (dietapb)

Sito statico pubblicato su Netlify (dietapb.netlify.app): `index.html` alla radice, nessun comando di build.

- `src/app.html` interfaccia, `src/data1.json` pasti e spesa, `src/ric.json` ricette.
- `python3 build.py` rigenera `index.html`.
- Spunte, pesate e stima del consumo restano salvate nel browser (localStorage).
- `python3 tools/piatti.py` rigenera pranzi e cene condivisi (Roberto + Francesca), verdure e spesa in `src/data1.json`; poi `python3 build.py`.
