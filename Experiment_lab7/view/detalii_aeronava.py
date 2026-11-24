import customtkinter as ctk
from view.tema_hangar import TemaHangar as T


class DetaliiAeronava(ctk.CTkFrame):
    """Panou de detalii pentru selectia curenta, cu actiuni delegate."""

    SPECIFICE = {
        'Avion': (('nr_pasageri', 'Pasageri', ''), ('nr_motoare', 'Motoare', ''),
                  ('altitudine_maxima', 'Altitudine maximă', 'm')),
        'Elicopter': (('nr_rotori', 'Rotori', ''), ('tip_motor', 'Tip motor', ''),
                      ('capacitate_cargo', 'Capacitate cargo', 'kg')),
        'Drona': (('greutate', 'Greutate', 'kg'), ('timp_zbor', 'Timp de zbor', 'min'),
                  ('tip_camera', 'Cameră', '')),
    }

    def __init__(self, master, imagini, modifica, sterge):
        super().__init__(master, width=322, fg_color=T.PANOU, corner_radius=14)
        self.imagini = imagini
        self.modifica = modifica
        self.sterge = sterge
        self.aeronava = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.continut = ctk.CTkScrollableFrame(self, width=322, fg_color=T.PANOU)
        self.continut.grid(row=0, column=0, sticky='nsew', padx=4, pady=(4, 0))
        self.continut.grid_columnconfigure(0, weight=1)
        actiuni = ctk.CTkFrame(self, fg_color='transparent')
        actiuni.grid(row=1, column=0, padx=14, pady=14, sticky='ew')
        actiuni.grid_columnconfigure((0, 1), weight=1)
        self.buton_editare = ctk.CTkButton(actiuni, text='Editează', command=self._modifica,
                                          width=130, height=38, font=('Arial', 14, 'bold'))
        self.buton_editare.grid(row=0, column=0, padx=(0, 6), sticky='ew')
        self.buton_stergere = ctk.CTkButton(actiuni, text='Șterge', command=self._sterge,
                                           width=130, height=38, fg_color='transparent',
                                           border_width=1, border_color=T.ROSU,
                                           text_color=T.ROSU, hover_color='#3B252B')
        self.buton_stergere.grid(row=0, column=1, padx=(6, 0), sticky='ew')
        self.afiseaza(None)

    def afiseaza(self, aeronava):
        self.aeronava = aeronava
        stare = "normal" if aeronava is not None else "disabled"
        self.buton_editare.configure(state=stare)
        self.buton_stergere.configure(state=stare)
        for copil in self.continut.winfo_children():
            copil.destroy()
        if aeronava is None:
            ctk.CTkLabel(self.continut, text='Nicio aeronavă selectată', font=('Arial', 18, 'bold'),
                         wraplength=280).grid(row=0, column=0, padx=14, pady=(80, 12))
            ctk.CTkLabel(self.continut, text='Selectează un card pentru detalii\nsau adaugă o aeronavă nouă.',
                         text_color=T.MUT).grid(row=1, column=0, pady=8)
            return
        tip = type(aeronava).__name__
        ctk.CTkLabel(self.continut, text='DETALII AERONAVĂ', text_color=T.MUT,
                     font=('Arial', 11, 'bold'), anchor='w').grid(
                         row=0, column=0, padx=14, pady=(14, 12), sticky='ew')
        ctk.CTkLabel(self.continut, text='', image=self.imagini.get_imagine(aeronava, (294, 190))).grid(
            row=1, column=0, padx=8)
        ctk.CTkLabel(self.continut, text=T.TIPURI[tip], text_color=T.ACCENT, anchor='w',
                     font=('Arial', 11, 'bold')).grid(row=2, column=0, padx=14, pady=(12, 0), sticky='ew')
        ctk.CTkLabel(self.continut, text=aeronava.get_model(), font=('Arial', 23, 'bold'),
                     wraplength=286, anchor='w', justify='left').grid(
                         row=3, column=0, padx=14, pady=(0, 12), sticky='ew')
        campuri = (('viteza', 'Viteză', 'km/h'), ('autonomie', 'Autonomie', 'km')) + self.SPECIFICE[tip]
        for rand, (camp, eticheta, unitate) in enumerate(campuri, start=4):
            linie = ctk.CTkFrame(self.continut, fg_color=T.RIDICAT, corner_radius=8)
            linie.grid(row=rand, column=0, padx=10, pady=3, sticky='ew')
            linie.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(linie, text=eticheta, text_color=T.MUT, font=('Arial', 12)).grid(
                row=0, column=0, padx=10, pady=8, sticky='w')
            ctk.CTkLabel(linie, text=f'{T.numar(getattr(aeronava, camp))} {unitate}'.strip(),
                         font=('Arial', 13, 'bold'), wraplength=165, justify='right').grid(
                             row=0, column=1, padx=10, pady=8, sticky='e')
        ctk.CTkLabel(self.continut, text=f'Fotografie: {aeronava.referinta_imagine}',
                     wraplength=285, text_color=T.MUT, font=('Arial', 11)).grid(
                         row=9, column=0, padx=10, pady=(12, 8))

    def _modifica(self):
        if self.aeronava is not None:
            self.modifica(self.aeronava)

    def _sterge(self):
        if self.aeronava is not None:
            self.sterge(self.aeronava)
