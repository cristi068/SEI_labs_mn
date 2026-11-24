from model.interface.interface import Interface


class BaseClass(Interface):
    def __init__(self, model, viteza, autonomie):
        self.model = model
        self.viteza = viteza
        self.autonomie = autonomie

    def set_model(self, model):
        self.model = model

    def get_model(self):
        return self.model

    def set_viteza(self, viteza):
        self.viteza = viteza

    def get_viteza(self):
        return self.viteza

    def set_autonomie(self, autonomie):
        self.autonomie = autonomie

    def get_autonomie(self):
        return self.autonomie

    def afisare(self):
        return (
            f"{self.model} | Viteza: {self.viteza} | "
            f"Autonomie: {self.autonomie}"
        )
