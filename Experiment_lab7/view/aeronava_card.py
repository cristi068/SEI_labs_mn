import customtkinter as ctk
from view.tema_hangar import TemaHangar as T


class AeronavaCard(ctk.CTkFrame):
    """Card selectabil; fotografia si valorile provin din obiectul Model."""

    def __init__(self, master, aeronava, callback_selectare, imagine):
        super().__init__(master, fg_color=T.PANOU, border_width=2,
                         border_color=T.LINIE, corner_radius=14)
        self.aeronava = aeronava
        self.callback_selectare = callback_selectare
        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self, text='', image=imagine).grid(row=0, column=0, padx=10, pady=(10, 0))
        ctk.CTkLabel(self, text=T.TIPURI[type(aeronava).__name__], text_color=T.ACCENT,
                     font=('Arial', 10, 'bold'), anchor='w').grid(
                         row=1, column=0, padx=16, pady=(9, 0), sticky='ew')
        ctk.CTkLabel(self, text=aeronava.get_model(), font=('Arial', 18, 'bold'),
                     wraplength=280, anchor='w', justify='left').grid(
                         row=2, column=0, padx=16, pady=(0, 8), sticky='ew')
        valori = ctk.CTkFrame(self, fg_color='transparent')
        valori.grid(row=3, column=0, padx=16, pady=(0, 10), sticky='ew')
        valori.grid_columnconfigure((0, 1), weight=1)
        for col, (titlu, valoare, unitate) in enumerate((
                ('VITEZĂ', aeronava.get_viteza(), 'km/h'),
                ('AUTONOMIE', aeronava.get_autonomie(), 'km'))):
            ctk.CTkLabel(valori, text=titlu, text_color=T.MUT, font=('Arial', 10),
                         anchor='w').grid(row=0, column=col, sticky='ew')
            ctk.CTkLabel(valori, text=f'{T.numar(valoare)} {unitate}', font=('Arial', 15, 'bold'),
                         anchor='w').grid(row=1, column=col, sticky='ew')
        self.buton = ctk.CTkButton(self, text='Vezi detalii', command=self._selecteaza,
                                   fg_color=T.RIDICAT, text_color=T.TEXT,
                                   hover_color=T.LINIE, height=30)
        self.buton.grid(row=4, column=0, padx=14, pady=(0, 14), sticky='ew')
        self._conecteaza_click(self)

    def _conecteaza_click(self, widget):
        if isinstance(widget, (ctk.CTkLabel, ctk.CTkFrame)):
            widget.bind('<Button-1>', self._selecteaza)
            for copil in widget.winfo_children():
                self._conecteaza_click(copil)

    def _selecteaza(self, event=None):
        self.callback_selectare(self.aeronava)

    def seteaza_selectat(self, selectat):
        self.configure(border_color=T.ACCENT if selectat else T.LINIE)
        self.buton.configure(text='Selectată' if selectat else 'Vezi detalii',
                              text_color=T.ACCENT if selectat else T.TEXT)
