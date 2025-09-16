# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['password_gen/ui/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('password_gen/assets/fonts/rubik/Rubik-Medium.ttf', 'password_gen/assets/fonts/rubik'),
        ('password_gen/assets/images/logo.png', 'password_gen/assets/images'),
    ],
    hiddenimports=[],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PasswordGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='password_gen/assets/images/password_icon.ico',
    onefile=True,  # ← добавляем эту строчку
)
