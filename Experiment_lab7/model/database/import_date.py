import json
import sqlite3
from pathlib import Path


class ImportDate:
    """Citeste sursa veche doar la primul import; SQLite nu mai este depozitul activ."""

    def __init__(self, cale=None):
        radacina = Path(__file__).resolve().parents[2]
        self.cale = Path(cale) if cale is not None else radacina / 'date' / 'aeronave.db'
        self.implicit = cale is None
        self.json_initial = radacina / 'aeronave.json'

    def citeste(self):
        cale = self.cale
        if self.implicit and not cale.exists():
            cale = self.json_initial
        if cale.suffix.lower() == '.json':
            date = json.loads(cale.read_text(encoding='utf-8'))
            if not isinstance(date, list) or not all(isinstance(r, dict) for r in date):
                raise ValueError('Format invalid pentru importul inițial.')
            return date
        # mode=ro exclude crearea/modificarea accidentala a sursei SQLite.
        conexiune = None
        try:
            conexiune = sqlite3.connect(cale.resolve().as_uri() + '?mode=ro', uri=True)
            conexiune.row_factory = sqlite3.Row
            return [dict(r) for r in conexiune.execute('SELECT * FROM aeronave ORDER BY id')]
        except sqlite3.Error as eroare:
            raise ValueError(f'Nu se poate importa sursa SQLite {cale.name}: {eroare}') from eroare
        finally:
            if conexiune is not None:
                conexiune.close()
