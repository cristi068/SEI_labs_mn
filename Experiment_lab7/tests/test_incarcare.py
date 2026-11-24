from support_postgres import TestPostgresBase
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch
from model.aeronave_model import AeronaveModel
from presenter.aeronave_presenter import AeronavePresenter
from view.app import AeronaveApp


class TestIncarcare(TestPostgresBase):
    def test_import_pornire_fara_matplotlib(self):
        rezultat = subprocess.run([sys.executable, '-c',
            'import runpy, sys; runpy.run_path("__main__.py", run_name="test_import"); '
            'assert not any(n == "matplotlib" or n.startswith("matplotlib.") for n in sys.modules)'],
            capture_output=True, text=True)
        self.assertEqual(rezultat.returncode, 0, rezultat.stderr)

    def test_date_modificate_inainte_de_deschidere(self):
        model = self.model
        presenter = AeronavePresenter(model, Mock())
        presenter.sterge_aeronava(model.get_aeronave()[0])
        grafice = Mock()
        presenter.conecteaza_grafice(grafice)
        self.assertEqual(grafice.afiseaza_grafice.call_args.args[0]['total'], 30)

    def test_cadru_creat_o_singura_data(self):
        app = Mock()
        app.grafice_frame = None
        app.file.get.return_value = 'Aeronave'
        with patch('view.grafice_frame.GraficeFrame') as cadru:
            AeronaveApp._schimba_fila(app)
            cadru.assert_not_called()
            app.file.get.return_value = 'Grafice'
            AeronaveApp._schimba_fila(app)
            AeronaveApp._schimba_fila(app)
            cadru.assert_called_once()
            app.presenter.conecteaza_grafice.assert_called_once_with(cadru.return_value)


if __name__ == '__main__':
    unittest.main()
