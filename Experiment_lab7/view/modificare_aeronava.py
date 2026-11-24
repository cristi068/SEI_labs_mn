from view.adaugare_aeronava import AdaugareAeronava


class ModificareAeronava(AdaugareAeronava):
    """Reutilizeaza formularul de adaugare cu valorile aeronavei selectate."""

    def __init__(self, master, callback_salvare, date_initiale):
        super().__init__(master, callback_salvare, date_initiale)
        self.title("Modifica aeronava")
