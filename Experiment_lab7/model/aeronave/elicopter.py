from model.base_class.basse_class import BaseClass


class Elicopter(BaseClass):
    IMAGINE = "airbus_ec135.jpg"

    def __init__(
        self,
        model,
        viteza,
        autonomie,
        nr_rotori,
        tip_motor,
        capacitate_cargo,
    ):
        super().__init__(model, viteza, autonomie)
        self.nr_rotori = nr_rotori
        self.tip_motor = tip_motor
        self.capacitate_cargo = capacitate_cargo

    def afisare(self):
        return (
            f"{'Elicopter':<11} | "
            f"{self.model:<20} | "
            f"{self.viteza:>7} | "
            f"{self.autonomie:>9} | "
            f"Rotori: {self.nr_rotori} buc., Motor: {self.tip_motor}, "
            f"Capacitate cargo: {self.capacitate_cargo} kg"
        )
