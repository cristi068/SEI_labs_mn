import json
import re
from pathlib import Path


class CatalogImagini:
    """Atribuie fotografii locale folosind numele si caracteristicile aeronavei."""

    def __init__(self):
        cale = Path(__file__).resolve().parents[1] / "imagini" / "catalog.json"
        self.fotografii = json.loads(cale.read_text(encoding="utf-8"))

    def atribuie_imagine(self, aeronava, excluse=None):
        tip = type(aeronava).__name__
        candidate = [foto for foto in self.fotografii if foto["tip"] == tip]
        disponibile = [foto for foto in candidate
                       if foto["imagine"] not in (excluse or set())]
        if disponibile:
            candidate = disponibile
        fotografie = min(candidate, key=lambda foto: self._scor(aeronava, foto))
        aeronava.imagine = fotografie["imagine"]
        aeronava.referinta_imagine = fotografie["referinta"]
        return fotografie["imagine"]

    @staticmethod
    def _normalizare(text):
        return re.sub(r"[^a-z0-9]", "", text.casefold())

    def _scor(self, aeronava, foto):
        model = self._normalizare(aeronava.get_model())
        referinta = self._normalizare(foto["referinta"])
        identificator = self._normalizare(" ".join(foto["referinta"].split()[1:]))
        if referinta in model or (len(identificator) >= 4 and identificator in model):
            return -1000
        p1, p2 = foto["parametri_asociere"]
        # Aceste valori sunt repere orientative ale exercitiului, nu fise tehnice.
        tip = foto["tip"]
        if tip == "Avion":
            return abs(aeronava.nr_motoare - p1) * 10 + abs(aeronava.nr_pasageri - p2) / 100
        if tip == "Elicopter":
            return abs(aeronava.nr_rotori - p1) + abs(aeronava.capacitate_cargo - p2) / 1000
        return abs(aeronava.greutate - p1) + abs(aeronava.timp_zbor - p2) / 30
