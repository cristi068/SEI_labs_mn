class AeronaveRepository:
    """SQL parametrizat, fara lista persistenta in memorie."""

    CAMPURI = ('tip', 'model', 'viteza', 'autonomie', 'nr_pasageri', 'nr_motoare',
               'altitudine_maxima', 'nr_rotori', 'tip_motor', 'capacitate_cargo',
               'greutate', 'timp_zbor', 'tip_camera', 'imagine', 'referinta_imagine')
    SORTARI = {'id': 'id', 'model': 'hangar_cheie_model(model) COLLATE "C"',
               'viteza': 'viteza', 'autonomie': 'autonomie'}

    def __init__(self, baza):
        self.conexiune = baza.conexiune

    def este_initializat(self):
        return self.conexiune.execute("SELECT 1 FROM configurare WHERE cheie = 'import_initial'").fetchone() is not None

    def initializeaza(self, date):
        with self.conexiune.transaction():
            self.conexiune.execute('LOCK TABLE configurare IN EXCLUSIVE MODE')
            if not self.este_initializat():
                if self.conexiune.execute('SELECT COUNT(*) AS n FROM aeronave').fetchone()['n']:
                    raise ValueError('Baza are deja aeronave fără marcaj de import. Importul a fost oprit pentru a evita dublarea.')
                for element in date:
                    self._insereaza(element, pastreaza_id=True)
                self.conexiune.execute("SELECT setval(pg_get_serial_sequence('aeronave', 'id'), COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM aeronave")
                self.conexiune.execute("INSERT INTO configurare VALUES ('import_initial', '1')")

    def _insereaza(self, date, pastreaza_id=False):
        campuri = self.CAMPURI
        if pastreaza_id and 'id' in date:
            campuri = ('id',) + campuri
        coloane = ', '.join(campuri)
        parametri = ', '.join('%s' for _ in campuri)
        return self.conexiune.execute(
            f'INSERT INTO aeronave ({coloane}) VALUES ({parametri}) RETURNING id',
            tuple(date.get(c) for c in campuri)).fetchone()['id']

    def adauga(self, date):
        with self.conexiune.transaction():
            return self._insereaza(date)

    def selecteaza(self, criteriu='id', reverse=False, tip='Toate', cautare=''):
        if criteriu not in self.SORTARI:
            raise ValueError('Criteriu de sortare invalid.')
        ordine = self.SORTARI[criteriu]
        directie = 'DESC' if reverse else 'ASC'
        filtru, parametri = self._filtru(tip)
        if cautare.strip():
            filtru += (' AND ' if filtru else 'WHERE ') + 'strpos(lower(model), lower(%s)) > 0'
            parametri += (cautare.strip(),)
        return self.conexiune.execute(
            f'SELECT * FROM aeronave {filtru} ORDER BY {ordine} {directie}, id ASC', parametri).fetchall()

    def gaseste(self, identificator):
        return self.conexiune.execute('SELECT * FROM aeronave WHERE id = %s', (identificator,)).fetchone()

    def modifica(self, identificator, date):
        atribuiri = ', '.join(f'{c} = %s' for c in self.CAMPURI)
        with self.conexiune.transaction():
            rezultat = self.conexiune.execute(
                f'UPDATE aeronave SET {atribuiri} WHERE id = %s',
                tuple(date.get(c) for c in self.CAMPURI) + (identificator,))
            if rezultat.rowcount != 1:
                raise ValueError('Aeronava nu mai exista in baza de date.')

    def sterge(self, identificator):
        with self.conexiune.transaction():
            return self.conexiune.execute('DELETE FROM aeronave WHERE id = %s', (identificator,)).rowcount == 1

    @staticmethod
    def _filtru(tip):
        return ('', ()) if tip == 'Toate' else ('WHERE tip = %s', (tip,))

    def rezumat(self, tip):
        filtru, parametri = self._filtru(tip)
        return self.conexiune.execute(
            f'''SELECT COUNT(*) AS total, COALESCE(AVG(viteza), 0) AS viteza_medie,
            COALESCE(AVG(autonomie), 0) AS autonomie_medie FROM aeronave {filtru}''', parametri).fetchone()

    def distributie(self, camp, praguri, tip):
        if camp not in ('viteza', 'autonomie'):
            raise ValueError('Camp statistic invalid.')
        filtru, parametri = self._filtru(tip)
        expresii = [f'COUNT(*) FILTER (WHERE {camp} < %s)']
        valori = [praguri[0]]
        for stanga, dreapta in zip(praguri, praguri[1:]):
            expresii.append(f'COUNT(*) FILTER (WHERE {camp} >= %s AND {camp} < %s)')
            valori.extend((stanga, dreapta))
        expresii.append(f'COUNT(*) FILTER (WHERE {camp} >= %s)')
        valori.append(praguri[-1])
        return list(self.conexiune.execute(
            f"SELECT {', '.join(e + ' AS n' + str(i) for i, e in enumerate(expresii))} FROM aeronave {filtru}", tuple(valori) + parametri).fetchone().values())
