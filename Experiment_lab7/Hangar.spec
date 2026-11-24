from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_delvewheel_libs_directory

root = Path(SPECPATH)
data = [(str(root / name), dest) for name, dest in
        [('imagini', 'imagini'), ('date', 'date'), ('aeronave.json', '.')]]
data += collect_data_files('customtkinter')
data, binaries = collect_delvewheel_libs_directory(
    'psycopg_binary', datas=data, binaries=[]
)
analysis = Analysis(
    [str(root / '__main__.py')], pathex=[str(root)], datas=data,
    binaries=binaries, hiddenimports=['psycopg_binary.pq', 'psycopg_binary._psycopg'],
    excludes=['PIL._avif'],
    hooksconfig={'matplotlib': {'backends': ['TkAgg']}}
)
exe = EXE(PYZ(analysis.pure), analysis.scripts, analysis.binaries, analysis.datas,
          name='Hangar', console=True, hide_console='hide-early', upx=False)
