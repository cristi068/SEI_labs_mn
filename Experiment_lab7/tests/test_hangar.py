from support_postgres import TestPostgresBase
import unittest
from unittest.mock import Mock
from model.aeronave_model import AeronaveModel
from presenter.aeronave_presenter import AeronavePresenter


class TestHangar(TestPostgresBase):
    def setUp(self):
        super().setUp()
        self.view = Mock()
        self.presenter = AeronavePresenter(self.model, self.view)

    def test_filtre_combinate_si_sortare_sql(self):
        self.model.filtreaza('Drona', 'model')
        lista = self.model.sortare_dupa_viteza(True)
        self.assertTrue(lista)
        self.assertTrue(all(type(a).__name__ == 'Drona' for a in lista))
        self.assertEqual([a.viteza for a in lista], sorted([a.viteza for a in lista], reverse=True))
        self.assertEqual(self.model.filtreaza('Drona', 'inexistent-xyz'), [])
        self.assertEqual(len(self.model.filtreaza()), 31)

    def test_cautare_literala_unicode_si_apostrof(self):
        date = self.model.get_date_aeronava(self.model.get_aeronave()[0])
        date['model'] = "ȘOIM O'Brien 100%_"
        a = self.model.adauga_aeronava(date)
        for text in ('șoim', "o'brien", '%_', '  ȘOIM  '):
            self.assertEqual([r.id for r in self.model.filtreaza('Toate', text)], [a.id])
        self.assertEqual(self.model.filtreaza('Toate', "' OR 1=1 --"), [])

    def test_crud_pastreaza_filtrul_si_sortarea(self):
        self.presenter.filtreaza('Drona', 'Model')
        self.presenter.schimba_sortarea('autonomie', True)
        a = self.model.get_aeronave()[0]
        date = self.model.get_date_aeronava(a)
        date['autonomie'] = 999
        self.assertTrue(self.presenter.modifica_aeronava(a, date))
        afisate = self.view.afiseaza_aeronave.call_args.args[1]
        self.assertEqual(afisate[0].id, a.id)
        self.assertTrue(all(type(r).__name__ == 'Drona' for r in afisate))
        self.presenter.sterge_aeronava(a)
        self.assertNotIn(a.id, [r.id for r in self.view.afiseaza_aeronave.call_args.args[1]])
        self.assertEqual(self.model.get_statistici()['total'], 30)


if __name__ == '__main__':
    unittest.main()
