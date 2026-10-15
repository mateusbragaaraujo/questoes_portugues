# -*- mode: python ; coding: utf-8 -*-
"""Empacota o treino num único .exe de Windows.

O PyInstaller executa este arquivo com SPECPATH apontando para scripts/.
Os caminhos partem da pasta do projeto, acima deste arquivo.
"""

from pathlib import Path

raiz = Path(SPECPATH).resolve().parent

a = Analysis(
    [str(raiz / "main.py")],
    pathex=[str(raiz)],
    binaries=[],
    datas=[(str(raiz / "banco"), "banco")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="QuestoesDePortugues",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
)
