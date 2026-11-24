class StatisticiModel:
    """Pregateste graficele; filtrarea si agregarile sunt realizate in SQL."""

    INTERVALE = {'Viteză': (150, 300, 600, 900), 'Autonomie': (100, 500, 1500, 5000)}

    def __init__(self, repository):
        self.repository = repository

    def calculeaza(self, tip='Toate'):
        randuri = self.repository.selecteaza(tip=tip)
        date = dict(self.repository.rezumat(tip))
        date.update(viteze=[r['viteza'] for r in randuri],
                    autonomii=[r['autonomie'] for r in randuri],
                    modele=[r['model'] for r in randuri])
        for criteriu, camp in (('Viteză', 'viteza'), ('Autonomie', 'autonomie')):
            praguri = self.INTERVALE[criteriu]
            limite = (0,) + praguri
            etichete = [f'[{a}, {b})' for a, b in zip(limite, limite[1:])]
            etichete.append(f'≥ {praguri[-1]}')
            date[criteriu] = {'etichete': etichete,
                              'numere': self.repository.distributie(camp, praguri, tip)}
        return date
