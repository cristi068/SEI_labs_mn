from tkinter import messagebox, simpledialog
import psycopg
from model.aeronave_model import AeronaveModel
from model.database.configurare_db import ConfigurareDB
from presenter.aeronave_presenter import AeronavePresenter
from view.app import AeronaveApp


class Program:
    @staticmethod
    def run():
        aplicatie = AeronaveApp()
        aplicatie.title('HANGAR | Se conecteaza la PostgreSQL...')
        aplicatie.update_idletasks()
        model = None
        try:
            parametri = ConfigurareDB().citeste()
            if not parametri['password']:
                parola = simpledialog.askstring('Conectare PostgreSQL',
                    f"Parola pentru {parametri['user']} la {parametri['host']}:",
                    show='*', parent=aplicatie)
                if parola is None:
                    return
                parametri['password'] = parola
            model = AeronaveModel(parametri)
            view = aplicatie.get_aeronave_frame()
            presenter = AeronavePresenter(model=model, view=view)
            view.set_presenter(presenter)
            aplicatie.set_presenter(presenter)
            presenter.afiseaza_lista_initiala()
            aplicatie.title('HANGAR | Catalogul aeronavelor')
            aplicatie.deiconify()
            aplicatie.mainloop()
        except (psycopg.Error, OSError, ValueError) as eroare:
            messagebox.showerror('Conectare PostgreSQL',
                f'Nu s-a putut deschide baza de date.\n\n{eroare}\n\n'
                'Verifică config.ini și serviciul PostgreSQL. La prima utilizare rulează:\n'
                'py configurare_postgresql.py', parent=aplicatie)
        finally:
            if model is not None:
                model.inchide()
            try:
                aplicatie.destroy()
            except Exception:
                pass


if __name__ == '__main__':
    Program.run()
