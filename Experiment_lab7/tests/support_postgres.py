import os
import tempfile
import unittest
import uuid
import psycopg
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict
from model.aeronave_model import AeronaveModel


class TestPostgresBase(unittest.TestCase):
    """Baze temporare dedicate; nu foloseste niciodata config.ini al aplicatiei."""

    def setUp(self):
        self.dsn = os.environ.get('HANGAR_TEST_DSN')
        if not self.dsn:
            self.skipTest('Setează HANGAR_TEST_DSN pentru testele PostgreSQL reale.')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = self.baza_noua()
        self.model = AeronaveModel(self.config)
        self.addCleanup(self._inchide)
        self.total_initial = len(self.model.get_aeronave())

    def baza_noua(self):
        nume = 'hangar_test_' + uuid.uuid4().hex
        with psycopg.connect(self.dsn, autocommit=True) as c:
            c.execute(sql.SQL('CREATE DATABASE {} TEMPLATE template0').format(sql.Identifier(nume)))
        self.addCleanup(self._sterge_baza, nume)
        parametri = conninfo_to_dict(self.dsn)
        parametri['dbname'] = nume
        return parametri

    def _sterge_baza(self, nume):
        with psycopg.connect(self.dsn, autocommit=True) as c:
            c.execute(sql.SQL('DROP DATABASE {} WITH (FORCE)').format(sql.Identifier(nume)))

    def _inchide(self):
        self.model.inchide()

    def _reporneste(self):
        self.model.inchide()
        self.model = AeronaveModel(self.config)
