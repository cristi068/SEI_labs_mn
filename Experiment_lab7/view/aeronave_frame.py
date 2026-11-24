import customtkinter as ctk
from tkinter import messagebox
from view.aeronava_card import AeronavaCard
from view.detalii_aeronava import DetaliiAeronava
from view.adaugare_aeronava import AdaugareAeronava
from view.modificare_aeronava import ModificareAeronava
from view.imagini_aeronave import ImaginiAeronave
from view.tema_hangar import TemaHangar as T


class AeronaveFrame(ctk.CTkFrame):
    """Catalog Hangar; filtrele sunt delegate Presenter-ului si Model-ului."""

    TIPURI = {'Toate': 'Toate', 'Avioane': 'Avion', 'Elicoptere': 'Elicopter', 'Drone': 'Drona'}
    SORTARI = {'Ordine inițială': ('id', False), 'Model A–Z': ('model', False),
               'Model Z–A': ('model', True), 'Viteză ↑': ('viteza', False),
               'Viteză ↓': ('viteza', True), 'Autonomie ↑': ('autonomie', False),
               'Autonomie ↓': ('autonomie', True)}

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=T.FUNDAL, **kwargs)
        self.presenter = None
        self.formular = None
        self.aeronava_editata = None
        self.selectat_id = None
        self.carduri = []
        self._coloane = 0
        self._cautare_job = None
        self.imagini_aeronave = ImaginiAeronave()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        antet = ctk.CTkFrame(self, fg_color='transparent')
        antet.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(6, 18))
        antet.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(antet, text='Explorează flota', font=('Arial', 32, 'bold'),
                     anchor='w').grid(row=0, column=0, sticky='ew')
        self.titlu = ctk.CTkLabel(antet, text='Catalogul aeronavelor', text_color=T.MUT, anchor='w')
        self.titlu.grid(row=1, column=0, sticky='ew', pady=(4, 0))
        ctk.CTkButton(antet, text='+  Adaugă aeronavă', height=42, width=190,
                      font=('Arial', 14, 'bold'), command=self._callback_adaugare).grid(
                          row=0, column=1, rowspan=2, padx=(15, 0))
        controale = ctk.CTkFrame(self, fg_color='transparent')
        controale.grid(row=1, column=0, sticky='ew', padx=(0, 16), pady=(0, 12))
        controale.grid_columnconfigure(0, weight=1)
        self.cautare = ctk.CTkEntry(controale, placeholder_text='Caută după model...', height=38)
        self.cautare.grid(row=0, column=0, sticky='ew', padx=(0, 8))
        self.cautare.bind('<KeyRelease>', self._programeaza_cautare)
        ctk.CTkButton(controale, text='×', width=34, height=36, fg_color=T.RIDICAT,
                      text_color=T.MUT, hover_color=T.LINIE, command=self._goleste_cautare).grid(
                          row=0, column=1, padx=(0, 10))
        self.sortare = ctk.CTkOptionMenu(controale, values=list(self.SORTARI),
                                       width=160, height=38, fg_color=T.RIDICAT,
                                       text_color=T.TEXT, button_color=T.LINIE,
                                       button_hover_color='#45565F', command=self._schimba_sortarea)
        self.sortare.grid(row=0, column=2)
        self.filtru = ctk.CTkSegmentedButton(self, values=list(self.TIPURI), height=34,
                                           selected_color='#164947', selected_hover_color='#1C615D',
                                           unselected_color=T.PANOU, unselected_hover_color=T.LINIE,
                                           fg_color=T.PANOU, command=self._aplica_filtre)
        self.filtru.set('Toate')
        self.filtru.grid(row=2, column=0, sticky='w', pady=(0, 14))
        self.lista = ctk.CTkScrollableFrame(self, fg_color=T.FUNDAL, corner_radius=0)
        self.lista.grid(row=3, column=0, sticky='nsew', padx=(0, 12))
        self.lista.bind('<Configure>', self._redimensioneaza, add='+')
        self.panou_detalii = DetaliiAeronava(self, self.imagini_aeronave,
                                           self._callback_modificare, self._callback_stergere)
        self.panou_detalii.grid(row=1, column=1, rowspan=3, sticky='nsew')

    def set_presenter(self, presenter):
        self.presenter = presenter

    def afiseaza_aeronave(self, titlu, aeronave):
        self.titlu.configure(text=f'{len(aeronave)} aeronave afișate  ·  Selectează un card pentru detalii')
        for copil in self.lista.winfo_children():
            copil.destroy()
        self.carduri = []
        selectata = None
        for aeronava in aeronave:
            card = AeronavaCard(self.lista, aeronava, self._selecteaza,
                                self.imagini_aeronave.get_imagine(aeronava))
            self.carduri.append(card)
            if aeronava.id == self.selectat_id:
                selectata = aeronava
        if not aeronave:
            ctk.CTkLabel(self.lista, text='Nicio aeronavă găsită', font=('Arial', 23, 'bold')).grid(
                row=0, column=0, padx=30, pady=(70, 10))
            ctk.CTkLabel(self.lista, text='Schimbă filtrele, șterge căutarea\nsau adaugă o aeronavă nouă.',
                         text_color=T.MUT).grid(row=1, column=0, padx=30, pady=10)
        self._coloane = 0
        self._aranjeaza(self.lista.winfo_width())
        self._selecteaza(selectata or (aeronave[0] if aeronave else None))

    def _selecteaza(self, aeronava):
        self.selectat_id = aeronava.id if aeronava is not None else None
        for card in self.carduri:
            card.seteaza_selectat(card.aeronava.id == self.selectat_id)
        self.panou_detalii.afiseaza(aeronava)

    def _redimensioneaza(self, event):
        self._aranjeaza(event.width)

    def _aranjeaza(self, latime):
        coloane = max(1, min(3, int(latime) // 335))
        if coloane == self._coloane:
            return
        self._coloane = coloane
        for col in range(3):
            self.lista.grid_columnconfigure(col, weight=1 if col < coloane else 0,
                                           minsize=0, uniform='carduri' if col < coloane else '')
        for index, card in enumerate(self.carduri):
            card.grid(row=index // coloane, column=index % coloane,
                      padx=6, pady=(0, 14), sticky='nsew')

    def _programeaza_cautare(self, event=None):
        if self._cautare_job is not None:
            self.after_cancel(self._cautare_job)
        self._cautare_job = self.after(250, self._aplica_filtre)

    def _aplica_filtre(self, valoare=None):
        if self._cautare_job is not None:
            self.after_cancel(self._cautare_job)
            self._cautare_job = None
        if self.presenter is not None:
            self.presenter.filtreaza(self.TIPURI[self.filtru.get()], self.cautare.get())

    def _goleste_cautare(self):
        self.cautare.delete(0, 'end')
        self._aplica_filtre()

    def _schimba_sortarea(self, valoare):
        if self.presenter is not None:
            self.presenter.schimba_sortarea(*self.SORTARI[valoare])

    def seteaza_culoare_sortare(self, criteriu, reverse):
        for eticheta, alegere in self.SORTARI.items():
            if alegere == (criteriu, reverse):
                self.sortare.set(eticheta)
                break

    def _callback_adaugare(self):
        if self.presenter is not None:
            self.presenter.deschide_adaugare()

    def _callback_stergere(self, aeronava):
        if self.presenter is not None and messagebox.askyesno(
                'Ștergere aeronavă', f'Ștergi aeronava „{aeronava.get_model()}”?',
                parent=self.winfo_toplevel()):
            self.presenter.sterge_aeronava(aeronava)

    def _callback_modificare(self, aeronava):
        if self.presenter is not None:
            self.presenter.deschide_modificare(aeronava)

    def deschide_formular(self):
        if self.formular is None or not self.formular.winfo_exists():
            self.aeronava_editata = None
            self.formular = AdaugareAeronava(self.winfo_toplevel(), self._callback_salvare)
        else:
            self.formular.lift()
            self.formular.focus_force()

    def deschide_formular_modificare(self, aeronava, date):
        if self.formular is None or not self.formular.winfo_exists():
            self.aeronava_editata = aeronava
            self.formular = ModificareAeronava(self.winfo_toplevel(), self._callback_salvare, date)
        else:
            self.formular.lift()
            self.formular.focus_force()

    def _callback_salvare(self, date):
        if self.aeronava_editata is not None:
            return self.presenter.modifica_aeronava(self.aeronava_editata, date)
        return self.presenter.adauga_aeronava(date)

    def afiseaza_eroare_formular(self, mesaj):
        self.formular.afiseaza_eroare(mesaj)

    def afiseaza_eroare(self, mesaj):
        messagebox.showerror('Eroare', mesaj, parent=self.winfo_toplevel())
