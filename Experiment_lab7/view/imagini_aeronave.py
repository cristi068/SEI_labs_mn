from pathlib import Path
import customtkinter as ctk
from PIL import Image, ImageOps
from view.tema_hangar import TemaHangar


class ImaginiAeronave:
    """Fotografii locale cu proportii pastrate si cache pentru card/detalii."""

    def __init__(self):
        self.folder = Path(__file__).resolve().parents[1] / 'imagini'
        self.imagini = {}

    def get_imagine(self, aeronava, dimensiune=(290, 174)):
        nume = getattr(aeronava, 'imagine', aeronava.IMAGINE)
        cheie = (nume, dimensiune)
        if cheie not in self.imagini:
            try:
                with Image.open(self.folder / nume) as sursa:
                    imagine = sursa.convert('RGB')
            except (OSError, ValueError):
                imagine = Image.new('RGB', dimensiune, TemaHangar.RIDICAT)
            imagine = ImageOps.pad(imagine, (dimensiune[0] * 2, dimensiune[1] * 2),
                                   method=Image.Resampling.LANCZOS, color=TemaHangar.RIDICAT)
            self.imagini[cheie] = ctk.CTkImage(light_image=imagine, dark_image=imagine,
                                              size=dimensiune)
        return self.imagini[cheie]
