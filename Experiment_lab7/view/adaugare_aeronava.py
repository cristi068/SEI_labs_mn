import customtkinter as ctk
from view.tema_hangar import TemaHangar as T


class AdaugareAeronava(ctk.CTkToplevel):
    """Formularul colecteaza datele; validarea si crearea sunt in Model."""

    CAMPURI = {
        "Avion": (("nr_pasageri", "Numar pasageri (persoane)"),
                  ("nr_motoare", "Numar motoare (buc.)"),
                  ("altitudine_maxima", "Altitudine maxima (m)")),
        "Elicopter": (("nr_rotori", "Numar rotori (buc.)"), ("tip_motor", "Tip motor"),
                      ("capacitate_cargo", "Capacitate cargo (kg)")),
        "Drona": (("greutate", "Greutate (kg)"), ("timp_zbor", "Timp zbor (minute)"),
                  ("tip_camera", "Tip camera")),
    }

    def __init__(self, master, callback_salvare, date_initiale=None):
        super().__init__(master)
        self.callback_salvare = callback_salvare
        self.title("HANGAR | Adaugă aeronavă")
        self.geometry("520x570")
        self.minsize(460, 530)
        self.transient(master)
        self.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self, text="Tip aeronava").grid(row=0, column=0, padx=20, pady=15)
        self.tip = ctk.CTkOptionMenu(self, values=list(self.CAMPURI),
                                    command=self._schimba_tip)
        self.tip.grid(row=0, column=1, padx=20, pady=15, sticky="ew")
        self.intrari = {}
        for rand, (cheie, eticheta) in enumerate(
                (("model", "Model"), ("viteza", "Viteza (km/h)"),
                 ("autonomie", "Autonomie (km)")), start=1):
            ctk.CTkLabel(self, text=eticheta).grid(row=rand, column=0, padx=20, pady=8)
            entry = ctk.CTkEntry(self)
            entry.grid(row=rand, column=1, padx=20, pady=8, sticky="ew")
            self.intrari[cheie] = entry
        self.specifice = ctk.CTkFrame(self)
        self.specifice.grid(row=4, column=0, columnspan=2, padx=20, pady=15, sticky="ew")
        self.specifice.grid_columnconfigure(1, weight=1)
        self.intrari_specifice = {}
        self.eroare = ctk.CTkLabel(self, text="", text_color=("#A82222", "#FF8585"),
                                  wraplength=450)
        self.eroare.grid(row=5, column=0, columnspan=2, padx=20, pady=5)
        ctk.CTkButton(self, text="Salvează", height=38, font=("Arial", 14, "bold"), command=self._salveaza).grid(
            row=6, column=0, padx=20, pady=15, sticky="ew")
        ctk.CTkButton(self, text="Anulează", height=38, fg_color=T.RIDICAT, text_color=T.TEXT, hover_color=T.LINIE, command=self.destroy).grid(
            row=6, column=1, padx=20, pady=15, sticky="ew")
        self._schimba_tip("Avion")
        if date_initiale is not None:
            self._completeaza_date(date_initiale)
            self.tip.configure(state="disabled")
        self.bind("<Escape>", self._anuleaza)
        self.after(100, self._activeaza)

    def _activeaza(self):
        self.grab_set()
        self.intrari["model"].focus_set()

    def _completeaza_date(self, date):
        self.tip.set(date["tip"])
        self._schimba_tip(date["tip"])
        for cheie, entry in {**self.intrari, **self.intrari_specifice}.items():
            entry.insert(0, str(date[cheie]))

    def _schimba_tip(self, tip):
        for widget in self.specifice.winfo_children():
            widget.destroy()
        self.intrari_specifice = {}
        for rand, (cheie, eticheta) in enumerate(self.CAMPURI[tip]):
            ctk.CTkLabel(self.specifice, text=eticheta).grid(
                row=rand, column=0, padx=10, pady=10)
            entry = ctk.CTkEntry(self.specifice)
            entry.grid(row=rand, column=1, padx=10, pady=10, sticky="ew")
            self.intrari_specifice[cheie] = entry
        self.eroare.configure(text="")

    def _salveaza(self):
        date = {"tip": self.tip.get()}
        for cheie, entry in {**self.intrari, **self.intrari_specifice}.items():
            date[cheie] = entry.get()
        if self.callback_salvare(date):
            self.destroy()

    def afiseaza_eroare(self, mesaj):
        self.eroare.configure(text=mesaj)

    def _anuleaza(self, event):
        self.destroy()
