from model.base_class.basse_class import BaseClass


class Drona(BaseClass):
    IMAGINE = "dji_phantom_4.jpg"

    def __init__(
        self,
        model,
        viteza,
        autonomie,
        greutate,
        timp_zbor,
        tip_camera,
    ):
        super().__init__(model, viteza, autonomie)
        self.greutate = greutate
        self.timp_zbor = timp_zbor
        self.tip_camera = tip_camera

    def afisare(self):
        return (
            f"{'Drona':<11} | "
            f"{self.model:<20} | "
            f"{self.viteza:>7} | "
            f"{self.autonomie:>9} | "
            f"Greutate: {self.greutate:.1f} kg, "
            f"Timp de zbor: {self.timp_zbor} minute, "
            f"Camera: {self.tip_camera}"
        )
