import psycopg


class AeronavePresenter:
    """Face legatura dintre Model si View."""

    def __init__(self, model, view, grafice_view=None):
        self.grafice_view = grafice_view
        self._criteriu_grafic = "Viteză"
        self._filtru_grafic = "Toate"
        self.model = model
        self.view = view
        self._sortare_activa = None

        self._sortare_reverse = {
            "model": False,
            "viteza": True,
            "autonomie": True,
        }

    def afiseaza_lista_initiala(self):
        self.actualizeaza_grafice()
        aeronave = self.model.get_aeronave()
        self.view.afiseaza_aeronave(
            "Lista initiala a aeronavelor",
            aeronave,
        )

    def sortare_dupa_model(self):
        reverse = self._sortare_reverse["model"]
        self._sortare_activa = ("model", reverse)
        aeronave = self.model.sortare_dupa_model(reverse=reverse)
        self._sortare_reverse["model"] = not reverse
        self.view.seteaza_culoare_sortare("model", reverse)

        directie = "descrescator" if reverse else "crescator"
        self.view.afiseaza_aeronave(
            f"Sortare dupa model ({directie})",
            aeronave,
        )

    def sortare_dupa_viteza(self):
        reverse = self._sortare_reverse["viteza"]
        self._sortare_activa = ("viteza", reverse)
        aeronave = self.model.sortare_dupa_viteza(reverse=reverse)
        self._sortare_reverse["viteza"] = not reverse
        self.view.seteaza_culoare_sortare("viteza", reverse)

        directie = "descrescator" if reverse else "crescator"
        self.view.afiseaza_aeronave(
            f"Sortare dupa viteza ({directie})",
            aeronave,
        )

    def sortare_dupa_autonomie(self):
        reverse = self._sortare_reverse["autonomie"]
        self._sortare_activa = ("autonomie", reverse)
        aeronave = self.model.sortare_dupa_autonomie(reverse=reverse)
        self._sortare_reverse["autonomie"] = not reverse
        self.view.seteaza_culoare_sortare("autonomie", reverse)

        directie = "descrescator" if reverse else "crescator"
        self.view.afiseaza_aeronave(
            f"Sortare dupa autonomie ({directie})",
            aeronave,
        )

    def deschide_adaugare(self):
        self.view.deschide_formular()

    def adauga_aeronava(self, date):
        try:
            self.model.adauga_aeronava(date)
        except (ValueError, psycopg.Error) as eroare:
            self.view.afiseaza_eroare_formular(str(eroare))
            return False
        self._actualizeaza_lista()
        return True

    def sterge_aeronava(self, aeronava):
        try:
            self.model.sterge_aeronava(aeronava)
        except psycopg.Error as eroare:
            self.view.afiseaza_eroare(str(eroare))
            return
        self._actualizeaza_lista()

    def deschide_modificare(self, aeronava):
        date = self.model.get_date_aeronava(aeronava)
        self.view.deschide_formular_modificare(aeronava, date)

    def modifica_aeronava(self, aeronava, date):
        try:
            self.model.modifica_aeronava(aeronava, date)
        except (ValueError, psycopg.Error) as eroare:
            self.view.afiseaza_eroare_formular(str(eroare))
            return False
        self._actualizeaza_lista()
        return True

    def filtreaza(self, tip='Toate', cautare=''):
        try:
            aeronave = self.model.filtreaza(tip, cautare)
            self.view.afiseaza_aeronave('Catalog aeronave', aeronave)
        except (ValueError, psycopg.Error) as eroare:
            self.view.afiseaza_eroare(str(eroare))

    def schimba_sortarea(self, criteriu, reverse=False):
        try:
            self.model.seteaza_sortarea(criteriu, reverse)
            self._sortare_activa = (criteriu, reverse)
            self.view.afiseaza_aeronave('Catalog aeronave', self.model.get_aeronave())
        except (ValueError, psycopg.Error) as eroare:
            self.view.afiseaza_eroare(str(eroare))

    def _actualizeaza_lista(self):
        self.view.afiseaza_aeronave('Catalog aeronave', self.model.get_aeronave())
        self.actualizeaza_grafice()

    def actualizeaza_grafice(self, criteriu=None, tip=None):
        if criteriu is not None:
            self._criteriu_grafic = criteriu
        if tip is not None:
            self._filtru_grafic = tip
        if self.grafice_view is not None:
            date = self.model.get_statistici(self._filtru_grafic)
            self.grafice_view.afiseaza_grafice(date, self._criteriu_grafic)

    def conecteaza_grafice(self, grafice_view):
        """Conecteaza cadrul creat la cerere si afiseaza datele curente."""
        self.grafice_view = grafice_view
        self.actualizeaza_grafice()
