# Инструкция по установке и настройке на Alt Linux

## Содержание
1. [Установка Python и зависимостей](#1-установка-python-и-зависимостей)
2. [Первый запуск и настройка](#2-первый-запуск-и-настройка)
3. [Автозапуск при входе в систему](#3-автозапуск-при-входе-в-систему)
4. [Сборка бинарного файла (опционально)](#4-сборка-бинарного-файла-опционально)
5. [Создание RPM-пакета (опционально)](#5-создание-rpm-пакета-опционально)
6. [Обновление программы](#6-обновление-программы)
7. [Устранение неполадок](#7-устранение-неполадок)

---

## 1. Установка Python и зависимостей

### 1.1 Установка Python 3

Alt Linux обычно поставляется с Python 3. Проверьте версию:

```bash
python3 --version
```

Если Python не установлен:

```bash
su -
apt-get update
apt-get install python3 python3-modules-tkinter
```

### 1.2 Установка pip

```bash
su -
apt-get install python3-module-pip
```

### 1.3 Установка зависимостей программы

Перейдите в папку с программой:

```bash
cd /путь/к/MailAutoProcessor
```

Установите зависимости:

```bash
pip3 install --user pystray Pillow matplotlib
```

Или через requirements.txt:

```bash
pip3 install --user -r requirements.txt
```

> **Примечание:** Флаг `--user` устанавливает пакеты в домашнюю директорию пользователя, не требуя прав root.

### 1.4 Проверка установки tkinter

```bash
python3 -c "import tkinter; print(tkinter.Tcl().eval('info patchlevel'))"
```

Если выводит версию (например, `8.6.12`) — tkinter установлен корректно.

---

## 2. Первый запуск и настройка

### 2.1 Запуск программы

```bash
cd /путь/к/MailAutoProcessor
python3 mail_auto_processor.py
```

### 2.2 Первоначальная настройка

При первом запуске программа создаст пустой файл `mail_config.json`.

1. Нажмите кнопку **«⚙ Настройки»**
2. Заполните вкладку **«Подключение»**:
   - **Ваше имя** — имя, которое будет отображаться у получателей
   - **Адрес эл. почты** — ваш email
   - **Пароль** — пароль от почты (для Mail.ru/Yandex/Gmail используйте пароль приложения)
   - Нажмите кнопку **«Авто»** рядом с email для автоматического определения настроек сервера
   - Нажмите **«Перетестировать»** для проверки подключения
3. Перейдите на вкладку **«Папки»**:
   - **Папка отправки** — папка, где подпапки = email адресам получателей
   - **Папка получения** — куда сохранять входящие письма
   - **Папка логирования** — куда сохранять журналы
4. Нажмите **«Готово»**

### 2.3 Создание структуры папок

```bash
mkdir -p ~/MailProcessor/{Отправка,Получение,Логи,Архив/{Отправленные,Полученные}}
```

### 2.4 Пример структуры папки отправки

```
~/MailProcessor/Отправка/
├── boss@company.ru/
│   └── отчет.xlsx
├── client@partner.ru/
│   └── договор.pdf
└── nonem@list.ru/
    └── файл1.txt
    └── файл2.txt
```

Каждая подпапка — это email получателя. Файлы внутри подпапок будут отправлены на соответствующий адрес.

---

## 3. Автозапуск при входе в систему

### 3.1 Через автозагрузку рабочего стола (KDE/GNOME/XFCE)

Создайте файл автозапуска:

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/mailprocessor.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Автопроцессинг почты
Comment=Автоматическая отправка и прием писем
Exec=python3 /путь/к/MailAutoProcessor/mail_auto_processor.py
Icon=/путь/к/MailAutoProcessor/icon.png
Terminal=false
Categories=Office;Network;
StartupNotify=false
X-GNOME-Autostart-enabled=true
EOF
```

> **Важно:** замените `/путь/к/MailAutoProcessor/` на реальный путь.

### 3.2 Через systemd (для серверов без GUI)

Если программа работает на сервере без графического интерфейса, используйте systemd:

```bash
su -
cat > /etc/systemd/system/mailprocessor.service << 'EOF'
[Unit]
Description=Автопроцессинг электронной почты
After=network.target

[Service]
Type=simple
User=%USER%
WorkingDirectory=/путь/к/MailAutoProcessor
ExecStart=/usr/bin/python3 /путь/к/MailAutoProcessor/mail_auto_processor.py
Restart=on-failure
RestartSec=30
Environment=DISPLAY=:0

[Install]
WantedBy=multi-user.target
EOF
```

Замените `%USER%` на имя пользователя и `/путь/к/` на реальный путь.

```bash
systemctl daemon-reload
systemctl enable mailprocessor.service
systemctl start mailprocessor.service
systemctl status mailprocessor.service
```

---

## 4. Сборка бинарного файла (опционально)

Для создания исполняемого файла без зависимости от Python:

### 4.1 Установка PyInstaller

```bash
pip3 install --user pyinstaller
```

### 4.2 Сборка

```bash
cd /путь/к/MailAutoProcessor
python3 -m PyInstaller mail_processor.spec
```

Или через setup.py:

```bash
python3 setup.py
```

Результат будет в папке `dist/MailAutoProcessor`.

### 4.3 Запуск бинарного файла

```bash
./dist/MailAutoProcessor/MailAutoProcessor
```

---

## 5. Создание RPM-пакета (опционально)

### 5.1 Установка инструментов

```bash
su -
apt-get install rpm-build rpmdevtools
```

### 5.2 Создание структуры

```bash
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
```

### 5.3 Создание spec-файла

```bash
cat > ~/rpmbuild/SPECS/mailprocessor.spec << 'EOF'
Name:           mailauto-processor
Version:        1.4.2
Release:        1%{?dist}
Summary:        Автопроцессинг электронной почты
License:        MIT
URL:            https://github.com/nonemivan-hue/MailAutoProcessor
Source0:        mailauto-processor-%{version}.tar.gz
BuildArch:      noarch
Requires:       python3, python3-module-tkinter

%description
Приложение для автоматической отправки и приема электронной почты
через IMAP/SMTP. Разработано для УЗСН Краснодарского края.

%prep
%setup -q

%install
mkdir -p %{buildroot}/opt/mailauto-processor
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/pixmaps
cp -r * %{buildroot}/opt/mailauto-processor/
cp mailauto-processor.desktop %{buildroot}/usr/share/applications/
cp icon.png %{buildroot}/usr/share/pixmaps/mailauto-processor.png

%files
/opt/mailauto-processor/
/usr/share/applications/mailauto-processor.desktop
/usr/share/pixmaps/mailauto-processor.png

%changelog
* Wed Aug 13 2026 Трощенко Иван <nonem@list.ru> - 1.4.2-1
- Автоматическое переподключение SMTP/IMAP
- Вкладки с фильтрами и сортировкой
- Резервное копирование и восстановление
EOF
```

### 5.4 Создание desktop-файла

```bash
cat > /путь/к/MailAutoProcessor/mailauto-processor.desktop << 'EOF'
[Desktop Entry]
Name=Автопроцессинг почты
Comment=Автоматическая отправка и прием писем
Exec=python3 /opt/mailauto-processor/mail_auto_processor.py
Icon=mailauto-processor
Type=Application
Categories=Office;Network;
Terminal=false
StartupNotify=true
EOF
```

### 5.5 Сборка пакета

```bash
cd /путь/к/MailAutoProcessor
tar -czf ~/rpmbuild/SOURCES/mailauto-processor-1.4.2.tar.gz .
cd ~/rpmbuild
rpmbuild -ba SPECS/mailprocessor.spec
```

Готовый RPM будет в `~/rpmbuild/RPMS/noarch/`.

### 5.6 Установка RPM

```bash
su -
rpm -i ~/rpmbuild/RPMS/noarch/mailauto-processor-1.4.2-1.noarch.rpm
```

---

## 6. Обновление программы

### 6.1 Автоматическое обновление (через кнопку в программе)

1. Нажмите **«⬆ Обновить»** на главном экране
2. Выберите ZIP-архив с новой версией
3. Программа создаст резервную копию и распакует обновление
4. Перезапустите программу

### 6.2 Ручное обновление

```bash
cd /путь/к/MailAutoProcessor

# Резервная копия текущих настроек
cp mail_config.json mail_config.json.bak
cp mail_stats.json mail_stats.json.bak

# Распаковка новой версии
unzip -o MailAutoProcessor_new.zip

# Запуск
python3 mail_auto_processor.py
```

### 6.3 Обновление через скрипт update.sh

```bash
cd /путь/к/MailAutoProcessor
chmod +x update.sh
./update.sh
```

---

## 7. Устранение неполадок

### 7.1 Ошибка: No module named 'tkinter'

```bash
su -
apt-get install python3-modules-tkinter
```

### 7.2 Ошибка: No module named 'pystray'

```bash
pip3 install --user pystray Pillow
```

### 7.3 Ошибка: cannot connect to X server

Программа требует графического интерфейса (X11). Для сервера без GUI используйте виртуальный дисплей:

```bash
su -
apt-get install xorg-xvfb
Xvfb :99 -screen 0 1024x768x16 &
export DISPLAY=:99
python3 mail_auto_processor.py
```

### 7.4 Ошибка подключения к почтовому серверу

1. Проверьте настройки через кнопку **«Перетестировать»**
2. Убедитесь, что используете **пароль приложения**, а не основной пароль:
   - **Mail.ru:** Настройки → Безопасность → Пароли приложений
   - **Yandex:** Паспорт → Безопасность → Пароли приложений
   - **Gmail:** Настройки аккаунта → Безопасность → Двухэтапная аутентификация → Пароли приложений
3. Проверьте брандмауэр:
   ```bash
   iptables -L | grep -E '25|465|587|993|995'
   ```

### 7.5 Логи для диагностики

```bash
# Технический лог
cat mail_app.log

# Лог отправки
cat sent_log.txt

# Лог получения
cat received_log.txt
```

### 7.6 Сброс настроек

```bash
cd /путь/к/MailAutoProcessor
mv mail_config.json mail_config.json.old
python3 mail_auto_processor.py
```

---

## Автор

**Трощенко Иван**

В случае вопросов — группа MAX:
https://max.ru/join/--5-pGF8J3toTewT3tRikNa8yF-P0O6XLSbEvSgLTHk
