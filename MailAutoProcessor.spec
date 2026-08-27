# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(
    ['mail_auto_processor.py'],
    pathex=[],
    binaries=[],
    datas=[('config_example.json', '.'), ('README.md', '.'), ('requirements.txt', '.'), ('icon.png', '.')],
    hiddenimports=['PIL._tkinter_finder', 'pystray._win32'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MailAutoProcessor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
