"""Construieste si publica arhiva de predare LL7 dintr-un mediu temporar."""

import os
from pathlib import Path
import subprocess
import tempfile
import venv
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parent
FOLDERE = ('model', 'view', 'presenter', 'tests', 'imagini', 'date')
FISIERE = (
    '__main__.py', 'configurare_postgresql.py', 'requirements.txt', 'aeronave.json',
    'Hangar.spec', 'Construieste_LL7.bat', 'construieste.py', 'Citeste_LL7.txt',
)
CONFIG = (
    '[postgresql]\nhost = localhost\nport = 5432\n'
    'dbname = hangar\nuser = postgres\npassword =\n'
)


def surse():
    for nume in FISIERE:
        yield ROOT / nume
    for nume in FOLDERE:
        for cale in sorted((ROOT / nume).rglob('*')):
            if cale.is_file() and '__pycache__' not in cale.parts and cale.suffix not in ('.pyc', '.pyo'):
                yield cale


def publica_arhiva(executabil, destinatie):
    destinatie.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destinatie.parent, suffix='.tmp', delete=False) as fisier:
        temporar = Path(fisier.name)
    try:
        with ZipFile(temporar, 'w', ZIP_DEFLATED, compresslevel=9) as arhiva:
            for cale in surse():
                arhiva.write(cale, 'Experiment_lab7/' + cale.relative_to(ROOT).as_posix())
            arhiva.writestr('Experiment_lab7/config.ini', CONFIG)
            arhiva.write(executabil, 'Executabil/Hangar.exe')
            arhiva.writestr('Executabil/config.ini', CONFIG)
        with ZipFile(temporar) as arhiva:
            if arhiva.testzip() is not None:
                raise OSError('Arhiva generata nu a trecut verificarea de integritate.')
        temporar.replace(destinatie)
    finally:
        temporar.unlink(missing_ok=True)


def main():
    if os.name != 'nt':
        raise SystemExit('Executabilul trebuie construit pe Windows.')
    destinatie = ROOT / 'Livrare' / 'LL7_Hangar_Optimizat.zip'
    with tempfile.TemporaryDirectory(prefix='hangar_ll7_') as director:
        lucru = Path(director)
        mediu = lucru / 'venv'
        venv.EnvBuilder(with_pip=True).create(mediu)
        python = mediu / 'Scripts' / 'python.exe'
        subprocess.run(
            [str(python), '-m', 'pip', 'install',
             '--disable-pip-version-check', '--no-cache-dir',
             '-r', str(ROOT / 'requirements.txt'), 'pyinstaller>=6.11,<7'],
            cwd=ROOT, check=True,
        )
        dist = lucru / 'dist'
        subprocess.run(
            [str(python), '-m', 'PyInstaller', '--noconfirm',
             '--workpath', str(lucru / 'build'), '--distpath', str(dist), str(ROOT / 'Hangar.spec')],
            cwd=ROOT, env={**os.environ, 'PYINSTALLER_CONFIG_DIR': str(lucru / 'pyinstaller')}, check=True,
        )
        publica_arhiva(dist / 'Hangar.exe', destinatie)
    print(f'Arhiva de predare: {destinatie} ({destinatie.stat().st_size / 1_000_000:.2f} MB)')


if __name__ == '__main__':
    main()
