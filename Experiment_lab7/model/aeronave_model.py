import math

from model.statistici_model import StatisticiModel
from model.aeronave.avion import Avion
from model.aeronave.elicopter import Elicopter
from model.aeronave.drona import Drona
from model.catalog_imagini import CatalogImagini
from model.database.baza_date import BazaDate
from model.database.import_date import ImportDate
from model.database.aeronave_repository import AeronaveRepository


class AeronaveModel:
    """Valideaza obiectele de domeniu si delega persistenta repository-ului."""

    def __init__(self, configurare=None, cale_import=None):
        self.catalog_imagini = CatalogImagini()
        self.baza = BazaDate(configurare)
        self.repository = AeronaveRepository(self.baza)
        self._sortare = ('id', False)
        self._tip = 'Toate'
        self._cautare = ''
        try:
            if not self.repository.este_initializat():
                date = ImportDate(cale_import).citeste()
                self.repository.initializeaza(self._date_import(d) for d in date)
        except Exception:
            self.inchide()
            raise

    def _date_import(self, date):
        aeronava = self._creeaza_din_date(date)
        self.catalog_imagini.atribuie_imagine(aeronava)
        aeronava.imagine = date.get('imagine') or aeronava.imagine
        aeronava.referinta_imagine = date.get('referinta_imagine') or aeronava.referinta_imagine
        rezultat = self._date(aeronava)
        if 'id' in date:
            if not isinstance(date['id'], int) or date['id'] <= 0:
                raise ValueError('ID invalid în sursa importului.')
            rezultat['id'] = date['id']
        return rezultat

    @staticmethod
    def _date(aeronava):
        return {'tip': type(aeronava).__name__, **vars(aeronava)}

    def _din_rand(self, rand):
        date = dict(rand)
        aeronava = self._creeaza_din_date(date)
        aeronava.id = date['id']
        aeronava.imagine = date['imagine']
        aeronava.referinta_imagine = date['referinta_imagine']
        return aeronava

    def get_aeronave(self):
        return [self._din_rand(r) for r in self.repository.selecteaza(*self._sortare, tip=self._tip, cautare=self._cautare)]

    def filtreaza(self, tip='Toate', cautare=''):
        if tip not in ('Toate', 'Avion', 'Elicopter', 'Drona'):
            raise ValueError('Tip de aeronava invalid.')
        self._tip, self._cautare = tip, cautare
        return self.get_aeronave()

    def seteaza_sortarea(self, criteriu, reverse=False):
        if criteriu not in self.repository.SORTARI:
            raise ValueError('Criteriu de sortare invalid.')
        self._sortare = (criteriu, reverse)

    def sortare_dupa_model(self, reverse=False):
        self._sortare = ('model', reverse)
        return self.get_aeronave()

    def sortare_dupa_viteza(self, reverse=True):
        self._sortare = ('viteza', reverse)
        return self.get_aeronave()

    def sortare_dupa_autonomie(self, reverse=True):
        self._sortare = ('autonomie', reverse)
        return self.get_aeronave()

    def adauga_aeronava(self, date):
        aeronava = self._creeaza_din_date(date)
        self.catalog_imagini.atribuie_imagine(aeronava)
        aeronava.id = self.repository.adauga(self._date(aeronava))
        return aeronava

    def _creeaza_din_date(self, date):
        tip = date.get("tip")
        campuri = {
            "Avion": (Avion, ("nr_pasageri", "nr_motoare", "altitudine_maxima")),
            "Elicopter": (Elicopter, ("nr_rotori", "tip_motor", "capacitate_cargo")),
            "Drona": (Drona, ("greutate", "timp_zbor", "tip_camera")),
        }
        if tip not in campuri:
            raise ValueError("Selectati un tip valid de aeronava.")
        clasa, specifice = campuri[tip]
        valori = []
        for camp in ("model", "viteza", "autonomie") + specifice:
            text = str(date.get(camp, "")).strip()
            if camp in ("model", "tip_motor", "tip_camera"):
                if not text:
                    raise ValueError("Completati toate campurile text.")
                valori.append(text)
                continue
            try:
                valoare = float(text.replace(",", "."))
            except ValueError:
                raise ValueError(f"{camp}: introduceti un numar valid.") from None
            minim = 0 if camp in ("nr_pasageri", "capacitate_cargo") else 1
            if not math.isfinite(valoare) or valoare < 0 or (minim == 1 and valoare <= 0):
                raise ValueError(f"{camp}: valoarea trebuie sa fie " +
                                 ("pozitiva." if minim else "nenegativa."))
            if camp in ("nr_pasageri", "nr_motoare", "nr_rotori"):
                if not valoare.is_integer():
                    raise ValueError(f"{camp}: introduceti un numar intreg.")
                valoare = int(valoare)
            valori.append(valoare)
        return clasa(*valori)

    def get_date_aeronava(self, aeronava):
        rand = self.repository.gaseste(getattr(aeronava, 'id', None))
        if rand is None:
            raise ValueError('Aeronava nu mai exista in baza de date.')
        return dict(rand)

    def modifica_aeronava(self, aeronava, date):
        vechi = self.get_date_aeronava(aeronava)
        if date.get('tip') != vechi['tip']:
            raise ValueError('Tipul aeronavei nu poate fi schimbat la modificare.')
        nou = self._creeaza_din_date(date)
        self.catalog_imagini.atribuie_imagine(nou)
        self.repository.modifica(aeronava.id, self._date(nou))
        nou.id = aeronava.id
        return nou

    def sterge_aeronava(self, aeronava):
        return self.repository.sterge(getattr(aeronava, 'id', None))

    def get_statistici(self, tip='Toate'):
        return StatisticiModel(self.repository).calculeaza(tip)

    def inchide(self):
        self.baza.inchide()
