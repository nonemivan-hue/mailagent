# -*- coding: utf-8 -*-
"""
Скрипт сборки исполняемого файла через PyInstaller.
Использование:
    pip install pyinstaller
    python setup.py
"""
import PyInstaller.__main__
import os

HERE = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    os.path.join(HERE, 'mail_auto_processor.py'),
    '--name=MailAutoProcessor',
    '--onefile',
    '--windowed',
    '--icon', os.path.join(HERE, 'icon.ico'),
    '--add-data', f'{os.path.join(HERE, "config_example.json")};.',
    '--add-data', f'{os.path.join(HERE, "README.md")};.',
    '--add-data', f'{os.path.join(HERE, "requirements.txt")};.',
    '--add-data', f'{os.path.join(HERE, "icon.png")};.',
    '--hidden-import', 'PIL._tkinter_finder',
    '--hidden-import', 'pystray._win32',
])
