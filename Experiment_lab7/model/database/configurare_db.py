import configparser
import os
import sys
from pathlib import Path


class ConfigurareDB:
    """Citeste setarile locale; parola nu este inclusa in cod."""

    def __init__(self, cale=None):
        folder = (Path(sys.executable).parent if getattr(sys, 'frozen', False)
                  else Path(__file__).resolve().parents[2])
        self.cale = Path(cale) if cale else folder / 'config.ini'

    def citeste(self):
        parser = configparser.ConfigParser(interpolation=None)
        if not parser.read(self.cale, encoding='utf-8') or 'postgresql' not in parser:
            raise ValueError('Lipseste sectiunea [postgresql] din config.ini.')
        sectiune = parser['postgresql']
        try:
            port = sectiune.getint('port', 5432)
            if not 1 <= port <= 65535:
                raise ValueError
        except ValueError:
            raise ValueError(
                'Portul PostgreSQL trebuie sa fie un numar intre 1 si 65535.') from None
        rezultat = {camp: sectiune.get(camp, implicit).strip() for camp, implicit in (
            ('host', 'localhost'), ('dbname', 'hangar'), ('user', 'postgres'))}
        if not all(rezultat.values()):
            raise ValueError('Completeaza host, dbname si user in config.ini.')
        rezultat.update(
            port=port,
            password=os.environ.get(
                'HANGAR_DB_PASSWORD', sectiune.get('password', '')),
            connect_timeout=5)
        return rezultat
