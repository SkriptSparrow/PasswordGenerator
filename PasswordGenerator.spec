# PasswordGenerator.spec

# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_submodules

# Собираем все подпакеты password_gen
hiddenimports = collect_submodules("password_gen")

# Ассеты (src, dst)
datas = [
    ("password_gen/assets/images/password_icon.ico", "password_gen/assets/images"),
    ("password_gen/assets/images/logo.png", "password_gen/assets/images"),
    ("password_gen/assets/fonts/rubik/Rubik-Medium.ttf", "password_gen/assets/fonts/rubik"),
]

block_cipher = None

a = Analysis(
    ["password_gen/ui/main.py"],
    pathex=["."],   # используем текущую директорию
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PasswordGenerator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="password_gen/assets/images/password_icon.ico",  # ← твоя иконка exe
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="PasswordGenerator",
)
