import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from model.database.configurare_db import ConfigurareDB


class TestConfigurare(unittest.TestCase):
    def test_parola_cu_procente_si_port(self):
        with tempfile.TemporaryDirectory() as d:
            cale = Path(d) / 'config.ini'
            cale.write_text('[postgresql]\npassword = test%#123\nport = 5432\n')
            with patch.dict('os.environ', {}, clear=True):
                date = ConfigurareDB(cale).citeste()
            self.assertEqual(date['password'], 'test%#123')
            self.assertEqual(date['port'], 5432)
            cale.write_text('[postgresql]\nport = abc\n')
            with self.assertRaises(ValueError):
                ConfigurareDB(cale).citeste()


if __name__ == '__main__':
    unittest.main()
