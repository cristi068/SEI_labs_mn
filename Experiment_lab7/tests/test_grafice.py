from support_postgres import TestPostgresBase
import unittest
from unittest.mock import Mock
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from model.aeronave_model import AeronaveModel
from model.statistici_model import StatisticiModel
from presenter.aeronave_presenter import AeronavePresenter
from view.grafice_frame import GraficeFrame


class TestGrafice(TestPostgresBase):
    def setUp(self):
        super().setUp()
        self.view = Mock()
        self.grafice = Mock()
        self.presenter = AeronavePresenter(self.model, self.view, self.grafice)

    def test_intervale_la_limite(self):
        for a in self.model.get_aeronave():
            self.model.sterge_aeronava(a)
        for v in (1, 149.9, 150, 300, 600, 900, 1200):
            self.model.adauga_aeronava(dict(tip='Drona', model='Test', viteza=v,
                autonomie=20, greutate=2, timp_zbor=30, tip_camera='HD'))
        self.assertEqual(self.model.get_statistici()['Viteză']['numere'], [2, 1, 1, 1, 2])

    def test_filtrare_si_total(self):
        for tip, total in [('Toate', 31), ('Avion', 11), ('Drona', 10), ('Elicopter', 10)]:
            date = self.model.get_statistici(tip)
            self.assertEqual(date['total'], total)
            self.assertEqual(len(date['modele']), total)
            for criteriu in ('Viteză', 'Autonomie'):
                self.assertEqual(sum(date[criteriu]['numere']), total)

    def test_editare_stergere_adaugare_actualizeaza(self):
        self.presenter.actualizeaza_grafice('Autonomie', 'Avion')
        aeronava = self.model.get_aeronave()[0]
        date = self.model.get_date_aeronava(aeronava)
        date['viteza'] = '150'
        self.assertTrue(self.presenter.modifica_aeronava(aeronava, date))
        self.assertEqual(self.grafice.afiseaza_grafice.call_args.args[0]['Viteză']['numere'][1], 1)
        self.presenter.sterge_aeronava(aeronava)
        self.assertEqual(self.grafice.afiseaza_grafice.call_args.args[0]['total'], 10)
        self.assertTrue(self.presenter.adauga_aeronava(date))
        self.assertEqual(self.grafice.afiseaza_grafice.call_args.args[0]['total'], 11)
        self.assertEqual(self.grafice.afiseaza_grafice.call_args.args[1], 'Autonomie')
        date['viteza'] = 'nan'
        self.assertFalse(self.presenter.adauga_aeronava(date))
        self.assertEqual(self.model.get_statistici()['total'], 31)

    def test_lista_goala(self):
        for a in self.model.get_aeronave():
            self.model.sterge_aeronava(a)
        date = self.model.get_statistici()
        self.assertEqual(date['total'], 0)
        self.assertEqual(date['viteza_medie'], 0)
        self.presenter.actualizeaza_grafice()
        self.grafice.afiseaza_grafice.assert_called_once()

    def test_desenare_toate_graficele_fara_display(self):
        # Executa metoda reala de desenare cu un canvas Agg (fara fereastra Tk).
        cadru = Mock()
        cadru.figura = Figure(figsize=(10, 4), layout='constrained')
        cadru.ax = cadru.figura.add_subplot(111)
        cadru.canvas = FigureCanvasAgg(cadru.figura)
        for criteriu in ('Viteză', 'Autonomie', 'Viteză–autonomie'):
            GraficeFrame.afiseaza_grafice(cadru, self.model.get_statistici(), criteriu)
            self.assertTrue(cadru.ax.axison)
        gol = self.model.get_statistici('Inexistent')
        GraficeFrame.afiseaza_grafice(cadru, gol, 'Viteză')
        self.assertFalse(cadru.ax.axison)
        GraficeFrame.afiseaza_grafice(cadru, self.model.get_statistici(), 'Viteză')
        self.assertTrue(cadru.ax.axison)


if __name__ == '__main__':
    unittest.main()
