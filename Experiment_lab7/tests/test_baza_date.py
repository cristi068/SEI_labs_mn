import json
import psycopg
import re
from support_postgres import TestPostgresBase
import tempfile
import unittest
from pathlib import Path
from model.aeronave_model import AeronaveModel


class TestBazaDate(TestPostgresBase):
    def test_import_identitate_si_persistenta(self):
        initial = self.model.get_date_aeronava(self.model.get_aeronave()[0])
        initial['model'] = "O'Brien'); DROP TABLE aeronave; --"
        a = self.model.adauga_aeronava(initial)
        b = self.model.adauga_aeronava(initial)
        self.assertNotEqual(a.id, b.id)
        initial['viteza'] = 777
        self.model.modifica_aeronava(a, initial)
        self.model.sterge_aeronava(b)
        self._reporneste()
        self.assertEqual(len(self.model.get_aeronave()), self.total_initial + 1)
        self.assertEqual(self.model.get_date_aeronava(a)['viteza'], 777)
        self.assertEqual(self.model.get_date_aeronava(a)['model'], initial['model'])
        with self.assertRaises(ValueError):
            self.model.get_date_aeronava(b)

    def test_baza_goala_ramane_goala(self):
        for a in self.model.get_aeronave():
            self.model.sterge_aeronava(a)
        self._reporneste()
        self.assertEqual(self.model.get_aeronave(), [])
        self.assertEqual(self.model.get_statistici()['viteza_medie'], 0)

    def test_sortari_sql_si_ordine_naturala(self):
        for camp in ('model', 'viteza', 'autonomie'):
            for invers in (False, True):
                lista = getattr(self.model, 'sortare_dupa_' + camp)(invers)
                valori = [getattr(a, camp) for a in lista]
                cheie = self._cheie if camp == 'model' else None
                self.assertEqual(valori, sorted(valori, key=cheie, reverse=invers))
        self.assertEqual(self.model.get_statistici('Drona')['total'], 10)

    @staticmethod
    def _cheie(text):
        return tuple((0, int(p)) if p.isdigit() else (1, p.lower())
                     for p in re.split(r'(\d+)', text))

    def test_date_invalide_nu_modifica_baza(self):
        a = self.model.get_aeronave()[0]
        date = self.model.get_date_aeronava(a)
        date['viteza'] = 'nan'
        with self.assertRaises(ValueError):
            self.model.modifica_aeronava(a, date)
        self.assertEqual(self.model.get_date_aeronava(a)['viteza'], a.viteza)
        with self.assertRaises(psycopg.IntegrityError):
            with self.model.baza.conexiune.transaction():
                self.model.baza.conexiune.execute('UPDATE aeronave SET viteza = -1')
        self.assertEqual(len(self.model.get_aeronave()), self.total_initial)

    def test_import_esuat_rollback(self):
        cale = Path(self.temp.name) / 'import.json'
        valid = self.model.get_date_aeronava(self.model.get_aeronave()[0])
        cale.write_text(json.dumps([valid, {'tip': 'Invalid'}]))
        baza = self.baza_noua()
        with self.assertRaises(ValueError):
            AeronaveModel(baza, cale)
        cale.write_text(json.dumps([valid]))
        model = AeronaveModel(baza, cale)
        try:
            self.assertEqual(len(model.get_aeronave()), 1)
        finally:
            model.inchide()

    def test_commit_vizibil_dintr_o_alta_conexiune(self):
        date = self.model.get_date_aeronava(self.model.get_aeronave()[0])
        a = self.model.adauga_aeronava(date)
        with psycopg.connect(**self.config) as alta:
            self.assertEqual(alta.execute('SELECT model FROM aeronave WHERE id = %s',
                                         (a.id,)).fetchone()[0], a.model)

    def test_import_sqlite_pastreaza_id_si_secventa(self):
        import sqlite3
        sursa = Path(self.temp.name) / 'sursa.db'
        with sqlite3.connect(sursa) as c:
            c.execute('CREATE TABLE aeronave (id INTEGER, tip TEXT, model TEXT, viteza REAL, autonomie REAL, greutate REAL, timp_zbor REAL, tip_camera TEXT)')
            c.execute("INSERT INTO aeronave VALUES (500, 'Drona', 'Import', 80, 20, 2, 30, 'HD')")
        m = AeronaveModel(self.baza_noua(), sursa)
        try:
            self.assertEqual(m.get_aeronave()[0].id, 500)
            date = m.get_date_aeronava(m.get_aeronave()[0])
            self.assertGreater(m.adauga_aeronava(date).id, 500)
        finally:
            m.inchide()


if __name__ == '__main__':
    unittest.main()
