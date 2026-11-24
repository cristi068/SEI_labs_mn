from getpass import getpass
import psycopg
from psycopg import sql
from model.database.configurare_db import ConfigurareDB
from model.aeronave_model import AeronaveModel


class ConfigurarePostgreSQL:
    """Creeaza baza daca lipseste si initializeaza tabelele/importul."""

    @staticmethod
    def pregateste(parametri):
        administrare = dict(parametri, dbname='postgres')
        with psycopg.connect(**administrare, autocommit=True) as conexiune:
            exista = conexiune.execute('SELECT 1 FROM pg_database WHERE datname = %s',
                                       (parametri['dbname'],)).fetchone()
            if not exista:
                conexiune.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(parametri['dbname'])))
        model = AeronaveModel(parametri)
        try:
            return model.get_statistici()['total']
        finally:
            model.inchide()

    @classmethod
    def run(cls):
        try:
            parametri = ConfigurareDB().citeste()
            if not parametri['password']:
                parametri['password'] = getpass('Parola PostgreSQL (nu se afișează): ')
            total = cls.pregateste(parametri)
            print(f"Conectare reușită. Baza: {parametri['dbname']}; aeronave: {total}.")
            print('Pornește aplicația: py __main__.py')
            return 0
        except (psycopg.Error, OSError, ValueError) as eroare:
            print(f'Configurarea nu a reușit: {eroare}')
            print('Verifică serviciul PostgreSQL și config.ini. Pentru creare, utilizatorul trebuie să aibă dreptul CREATEDB.')
            return 1


if __name__ == '__main__':
    raise SystemExit(ConfigurarePostgreSQL.run())
