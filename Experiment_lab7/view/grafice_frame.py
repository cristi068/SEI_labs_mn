import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
from view.tema_hangar import TemaHangar as T


class GraficeFrame(ctk.CTkFrame):
    """Deseneaza datele agregate primite exclusiv de la Presenter."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.presenter = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        ctk.CTkLabel(self, text="Profilul flotei", font=("Arial", 24, "bold")).grid(
            row=0, column=0, padx=20, pady=(16, 2), sticky="w")
        controale = ctk.CTkFrame(self, fg_color="transparent")
        controale.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.criteriu = ctk.CTkSegmentedButton(
            controale, values=["Viteză", "Autonomie", "Viteză–autonomie"],
            selected_color="#164947", selected_hover_color="#1C615D",
            unselected_color=T.RIDICAT, unselected_hover_color=T.LINIE, command=self._schimba_optiune)
        self.criteriu.pack(side="left", padx=(0, 20))
        self.criteriu.set("Viteză")
        self.filtru = ctk.CTkOptionMenu(controale, values=["Toate", "Avion", "Elicopter", "Drona"],
                                      command=self._schimba_optiune)
        self.filtru.pack(side="left")
        self.rezumat = ctk.CTkLabel(self, text="", anchor="w")
        self.rezumat.grid(row=2, column=0, padx=20, pady=(0, 8), sticky="ew")
        self.figura = Figure(figsize=(9, 4), dpi=100, layout="constrained", facecolor=T.PANOU)
        self.ax = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, master=self)
        self.canvas.get_tk_widget().grid(row=3, column=0, padx=20, pady=(0, 10), sticky="nsew")
        self._puncte = None
        self._creeaza_tooltip()
        self.canvas.mpl_connect("motion_notify_event", self._afiseaza_tooltip)
        ctk.CTkLabel(self, text="Date demonstrative • Actualizare automată la adăugare, modificare și ștergere").grid(
            row=4, column=0, padx=20, pady=(0, 12), sticky="w")

    def _creeaza_tooltip(self):
        self._tooltip = self.ax.annotate(
            "",
            xy=(0, 0),
            xytext=(12, 12),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#1976b9", alpha=0.95),
            arrowprops=dict(arrowstyle="->", color="#1976b9"),
        )
        self._tooltip.set_visible(False)

    def set_presenter(self, presenter):
        self.presenter = presenter

    def _schimba_optiune(self, _valoare):
        if self.presenter is not None:
            self.presenter.actualizeaza_grafice(self.criteriu.get(), self.filtru.get())

    def _afiseaza_tooltip(self, eveniment):
        if self._puncte is None or eveniment.inaxes is not self.ax:
            if self._tooltip.get_visible():
                self._tooltip.set_visible(False)
                self.canvas.draw_idle()
            return

        contine, informatii = self._puncte.contains(eveniment)
        if not contine:
            if self._tooltip.get_visible():
                self._tooltip.set_visible(False)
                self.canvas.draw_idle()
            return

        index = informatii["ind"][0]
        viteza = self._puncte.get_offsets()[index][0]
        autonomie = self._puncte.get_offsets()[index][1]
        pozitie_x = -12 if eveniment.x > self.ax.bbox.x0 + self.ax.bbox.width / 2 else 12
        pozitie_y = -12 if eveniment.y > self.ax.bbox.y0 + self.ax.bbox.height / 2 else 12
        self._tooltip.set_position((pozitie_x, pozitie_y))
        self._tooltip.set_ha("right" if pozitie_x < 0 else "left")
        self._tooltip.set_va("top" if pozitie_y < 0 else "bottom")
        self._tooltip.xy = (viteza, autonomie)
        self._tooltip.set_text(
            f"Model: {self._modele[index]}\n"
            f"Viteză: {viteza:g} km/h\nAutonomie: {autonomie:g} km"
        )
        self._tooltip.set_visible(True)
        self.canvas.draw_idle()

    def afiseaza_grafice(self, date, criteriu):
        self.rezumat.configure(text=(
            f"Aeronave: {date['total']}     |     Viteză medie: {date['viteza_medie']:.1f} km/h"
            f"     |     Autonomie medie: {date['autonomie_medie']:.1f} km"))
        self.ax.clear()
        self._puncte = None
        self._modele = date.get("modele", [])
        self._creeaza_tooltip()
        self.ax.set_facecolor(T.PANOU)
        self.figura.set_facecolor(T.PANOU)
        self.ax.tick_params(colors=T.MUT)
        for axe in (self.ax.xaxis, self.ax.yaxis):
            axe.label.set_color(T.MUT)
        self.ax.title.set_color(T.TEXT)
        for bordura in self.ax.spines.values():
            bordura.set_color(T.LINIE)
        for latura in ("top", "right"):
            self.ax.spines[latura].set_visible(False)
        if not date["total"]:
            self.ax.text(0.5, 0.5, "Nu există aeronave pentru filtrul selectat.\nAdaugă o aeronavă sau alege alt filtru.",
                         ha="center", va="center", color=T.TEXT, transform=self.ax.transAxes)
            self.ax.set_axis_off()
        elif criteriu == "Viteză–autonomie":
            self._puncte = self.ax.scatter(
                date["viteze"], date["autonomii"], s=65,
                c=T.ACCENT, edgecolors=T.TEXT, alpha=0.8,
            )
            self.ax.set_xlabel("Viteză (km/h)")
            self.ax.set_ylabel("Autonomie (km)")
            self.ax.set_title("Viteză și autonomie • fiecare punct reprezintă o aeronavă", pad=16)
            self.ax.grid(alpha=0.18)
        else:
            distributie = date[criteriu]
            bare = self.ax.bar(distributie["etichete"], distributie["numere"],
                               color=["#188F8C", "#21B7AC", "#27DFD3", "#70E3C6", "#B2EFE4"], width=0.65)
            self.ax.bar_label(bare, padding=5, color=T.TEXT)
            self.ax.set_ylim(0, max(distributie["numere"]) * 1.2 + 1)
            self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            unitate = "km/h" if criteriu == "Viteză" else "km"
            self.ax.set_xlabel(f"Intervale de {criteriu.lower()} ({unitate}) • limita din dreapta este exclusă")
            self.ax.set_ylabel("Număr de aeronave")
            self.ax.set_title(f"Repartizarea aeronavelor pe intervale de {criteriu.lower()}", pad=16)
            self.ax.grid(axis="y", alpha=0.18)
            self.ax.set_axisbelow(True)
        self.canvas.draw_idle()
