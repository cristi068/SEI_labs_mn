import customtkinter as ctk

from view.aeronave_frame import AeronaveFrame
from view.tema_hangar import TemaHangar as T


class AeronaveApp(ctk.CTk):
    """Fereastra principala a aplicatiei."""

    def __init__(self):
        T.aplica()
        super().__init__()


        self.title("HANGAR | Catalogul aeronavelor")
        self.geometry("1360x860")
        self.minsize(1040, 660)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        antet = ctk.CTkFrame(self, fg_color=T.FUNDAL, height=62)
        antet.grid(row=0, column=0, padx=28, pady=(14, 0), sticky='ew')
        antet.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(antet, text='✈  HANGAR', text_color=T.ACCENT,
                     font=('Arial', 25, 'bold')).grid(row=0, column=0, sticky='w')
        ctk.CTkLabel(antet, text='CATALOGUL AERONAVELOR', text_color=T.MUT,
                     font=('Arial', 11)).grid(row=0, column=1, padx=24, sticky='w')
        ctk.CTkLabel(antet, text='Avioane / Elicoptere / Drone', text_color=T.MUT,
                     font=('Arial', 12)).grid(row=0, column=2, sticky='e')
        self.presenter = None
        self.grafice_frame = None
        self.file = ctk.CTkTabview(self, command=self._schimba_fila, fg_color=T.FUNDAL,
                                    segmented_button_fg_color=T.PANOU,
                                    segmented_button_selected_color='#164947',
                                    segmented_button_selected_hover_color='#1C615D',
                                    segmented_button_unselected_color=T.PANOU,
                                    segmented_button_unselected_hover_color=T.LINIE)
        self.file.grid(row=1, column=0, padx=20, pady=(0, 12), sticky="nsew")
        for nume in ("Aeronave", "Grafice"):
            fila = self.file.add(nume)
            fila.grid_columnconfigure(0, weight=1)
            fila.grid_rowconfigure(0, weight=1)
        self.aeronave_frame = AeronaveFrame(self.file.tab("Aeronave"))
        self.aeronave_frame.grid(
            row=0,
            column=0,
            padx=4,
            pady=8,
            sticky="nsew",
        )

    def get_aeronave_frame(self):
        return self.aeronave_frame

    def get_grafice_frame(self):
        return self.grafice_frame

    def set_presenter(self, presenter):
        self.presenter = presenter

    def _schimba_fila(self):
        if (self.file.get() != "Grafice" or self.grafice_frame is not None
                or self.presenter is None):
            return
        # Importul local amana inclusiv incarcarea Matplotlib pana la primul clic.
        from view.grafice_frame import GraficeFrame

        self.grafice_frame = GraficeFrame(self.file.tab("Grafice"))
        self.grafice_frame.grid(row=0, column=0, sticky="nsew")
        self.grafice_frame.set_presenter(self.presenter)
        self.presenter.conecteaza_grafice(self.grafice_frame)
