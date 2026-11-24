from abc import ABC, abstractmethod


class Interface(ABC):
    @abstractmethod
    def set_model(self, model):
        pass

    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def set_viteza(self, viteza):
        pass

    @abstractmethod
    def get_viteza(self):
        pass

    @abstractmethod
    def set_autonomie(self, autonomie):
        pass

    @abstractmethod
    def get_autonomie(self):
        pass

    @abstractmethod
    def afisare(self):
        pass
