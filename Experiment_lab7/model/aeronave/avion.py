from model.base_class.basse_class import BaseClass


class Avion(BaseClass):
    IMAGINE = "airbus_a320.jpg"

    def __init__(
        self,
        model,
        viteza,
        autonomie,
        nr_pasageri,
        nr_motoare,
        altitudine_maxima,
    ):
        super().__init__(model, viteza, autonomie)
        self.nr_pasageri = nr_pasageri
        self.nr_motoare = nr_motoare
        self.altitudine_maxima = altitudine_maxima

    def afisare(self):
        return (
            f"{'Avion':<11} | "
            f"{self.model:<20} | "
            f"{self.viteza:>7} | "
            f"{self.autonomie:>9} | "
            f"Pasageri: {self.nr_pasageri} persoane, "
            f"Motoare: {self.nr_motoare} buc., "
            f"Altitudine maxima: {self.altitudine_maxima} m"
        )
