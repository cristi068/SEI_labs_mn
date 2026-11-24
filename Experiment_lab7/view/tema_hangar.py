import customtkinter as ctk


class TemaHangar:
    """Paleta si configuratia comuna a widgeturilor; fara logica de domeniu."""

    FUNDAL = '#101417'
    PANOU = '#191F24'
    RIDICAT = '#222B32'
    LINIE = '#33414A'
    TEXT = '#F2F6F7'
    MUT = '#9DAEB9'
    ACCENT = '#27DFD3'
    HOVER = '#19BFB5'
    ROSU = '#FF747B'
    TIPURI = {'Avion': 'AVION', 'Elicopter': 'ELICOPTER', 'Drona': 'DRONĂ'}

    @classmethod
    def aplica(cls):
        ctk.DrawEngine.preferred_drawing_method = 'polygon_shapes'
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')
        tema = ctk.ThemeManager.theme
        tema['CTk']['fg_color'] = [cls.FUNDAL, cls.FUNDAL]
        tema['CTkToplevel']['fg_color'] = [cls.PANOU, cls.PANOU]
        tema['CTkFrame']['fg_color'] = [cls.PANOU, cls.PANOU]
        tema['CTkFrame']['top_fg_color'] = [cls.RIDICAT, cls.RIDICAT]
        tema['CTkFrame']['border_color'] = [cls.LINIE, cls.LINIE]
        tema['CTkLabel']['text_color'] = [cls.TEXT, cls.TEXT]
        for tip in ('CTkButton', 'CTkOptionMenu'):
            tema[tip]['fg_color'] = [cls.ACCENT, cls.ACCENT]
            tema[tip]['text_color'] = [cls.FUNDAL, cls.FUNDAL]
        tema['CTkButton']['hover_color'] = [cls.HOVER, cls.HOVER]
        tema['CTkEntry']['fg_color'] = [cls.FUNDAL, cls.FUNDAL]
        tema['CTkEntry']['border_color'] = [cls.LINIE, cls.LINIE]
        tema['CTkEntry']['text_color'] = [cls.TEXT, cls.TEXT]

    @staticmethod
    def numar(valoare):
        return f'{valoare:g}' if isinstance(valoare, (float, int)) else str(valoare)
