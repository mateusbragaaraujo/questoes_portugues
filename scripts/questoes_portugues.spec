# -*- mode: python ; coding: utf-8 -*-
"""Empacota o treino para Windows. Rode a partir da pasta do projeto."""

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[("banco", "banco")],
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
)
