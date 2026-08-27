# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\mail3\\mail_auto_processor.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\mail3\\config_example.json', '.'), ('C:\\mail3\\README.md', '.'), ('C:\\mail3\\requirements.txt', '.'), ('C:\\mail3\\icon.png', '.')],
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
    icon=['C:\\mail3\\icon.ico'],
)
