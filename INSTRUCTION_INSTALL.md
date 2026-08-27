# Инструкция по созданию установщика Windows

## 1. Подготовка окружения

Установите Python 3.10+ и pip на Windows.

```bash
pip install pyinstaller pystray Pillow matplotlib
```

## 2. Сборка исполняемого файла (EXE)

### Вариант А — через setup.py
```bash
python setup.py
```

### Вариант Б — через spec-файл
```bash
pyinstaller mail_processor.spec
```

Результат: папка `dist\MailAutoProcessor.exe`

## 3. Создание установщика через Inno Setup

1. Скачайте и установите **Inno Setup 6.x**: https://jrsoftware.org/isinfo.php
2. Откройте файл `setup.iss` в Inno Setup Compiler.
3. Нажмите **Build → Compile** (или F9).
4. Готовый установщик появится в папке `installer\MailAutoProcessor_Setup.exe`.

## 4. Файлы, включаемые в установщик

- `MailAutoProcessor.exe` — основная программа
- `config_example.json` — пример конфигурации
- `README.md` — описание программы
- `requirements.txt` — зависимости Python
- `icon.png` — иконка для трея
- `icon.ico` — иконка приложения
- `update.bat` — скрипт обновления (Windows)

## 5. Обновление программы

### Windows (update.bat)
Запустите `update.bat` рядом с программой. Скрипт:
1. Останавливает текущий процесс
2. Копирует файлы из папки `new_version\`
3. Перезапускает программу

### Alt Linux (update.sh)
```bash
chmod +x update.sh
./update.sh
```

Скрипт останавливает приложение, копирует новые файлы и перезапускает.

## 6. Примечания

- Для работы в системном трее требуется `pystray` и `Pillow`
- Для графика статистики требуется `matplotlib`
- При установке через Inno Setup программа появится в меню Пуск
- Обновления возможны как в Windows, так и в Alt Linux
