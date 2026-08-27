# Известные ошибки и их решения

## Исправленные ошибки

### 1. SyntaxWarning: invalid escape sequence '\S' / '\D'
**Причина:** Строки с IMAP-флагами `\Seen` и `\Deleted` интерпретировались как escape-последовательности Python.

**Решение:** Использование raw-строк (`r'\Seen'`, `r'\Deleted'`).

**Строки в коде:**
- `self.imap_conn.append(..., r'\Seen', ...)`
- `self.imap_conn.store(..., r'\Deleted')`

---

### 2. TclError: invalid command name ".!toplevel2.!frame.!canvas"
**Причина:** `canvas.bind_all("<MouseWheel>", ...)` привязывал обработчик глобально ко всему приложению. При закрытии окна настроек Canvas уничтожался, но бинд оставался активным. При повторном открытии окна прокрутка колесом вызывала обращение к уже несуществующему виджету.

**Решение:**
1. Замена `bind_all` на `bind` к конкретному окну (`self.window.bind("<MouseWheel>", ...)`)
2. Добавлена защита `try/except` + `winfo_exists()` в обработчике `_on_mousewheel`

**Код:**
```python
def _on_mousewheel(self, event):
    try:
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    except tk.TclError:
        pass
```

---

### 3. SMTPUTF8 capability — "One or more source or delivery addresses require internationalized email support"
**Причина:** `send_message()` автоматически определяет, нужен ли SMTPUTF8, и если адрес или тема содержат не-ASCII символы (кириллица, умлауты и т.д.), требует от сервера поддержки SMTPUTF8. Серверы Mail.ru, Yandex и многие другие не объявляют эту возможность.

**Решение:** Замена `send_message()` на `sendmail()` + переход с `MIMEMultipart`/`MIMEText`/`Header` (старый API с `Compat32`) на `EmailMessage` (современный API с `policy.default`). `EmailMessage` корректно кодирует UTF-8 в заголовках через RFC 2047, а `sendmail()` просто передаёт готовые байты без требования SMTPUTF8.

**Код:**
```python
from email.message import EmailMessage

msg = EmailMessage()
msg['From'] = sender
msg['To'] = recipient
msg['Subject'] = subject  # EmailMessage сам кодирует UTF-8
msg.set_content(body)
msg.add_attachment(data, maintype='application', subtype='octet-stream', filename=filename)

self.smtp_conn.sendmail(sender, [recipient], msg.as_bytes())
```

---

### 4. 'utf8' is an invalid keyword argument for Compat32
**Причина:** В Python 3.14 (и некоторых других версиях) старый email-API (`MIMEText`, `MIMEMultipart` с политикой `Compat32`) не корректно обрабатывает строковый аргумент `charset='utf-8'`. Внутри вызывается `Charset('utf-8')`, который передаёт `utf8` (без дефиса) в `Compat32`, вызывая `TypeError`.

**Решение:** Тот же, что и для ошибки SMTPUTF8 — переход на `EmailMessage` с `set_content()` и `add_attachment()`. Новый API не использует `Compat32` и корректно работает с UTF-8 нативно.

---

## Типичные проблемы при запуске

### 3. ModuleNotFoundError: No module named 'pystray'
**Причина:** Не установлены зависимости.

**Решение:**
```bash
pip install pystray Pillow matplotlib
```

---

### 4. ModuleNotFoundError: No module named 'tkinter'
**Причина:** В Linux tkinter часто не входит в базовую установку Python.

**Решение:**
```bash
# Debian / Ubuntu
sudo apt-get install python3-tk

# Alt Linux
sudo apt-get install python3-modules-tkinter

# Fedora / RHEL
sudo dnf install python3-tkinter
```

---

### 5. Ошибка подключения к IMAP/SMTP
**Возможные причины:**
- Неверный пароль (для Mail.ru, Yandex и Gmail нужен **пароль приложения**, а не пароль от аккаунта)
- Неверный порт или тип шифрования
- Брандмауэр блокирует соединение
- Сервер требует OAuth2 (не поддерживается)

**Решение:**
1. Проверьте настройки через кнопку **"Перетестировать"** в окне настроек
2. Убедитесь, что используете пароль приложения, а не основной пароль
3. Проверьте настройки SSL/STARTTLS для вашего провайдера

---

### 6. Не отображается график статистики
**Причина:** Не установлен matplotlib.

**Решение:**
```bash
pip install matplotlib
```

Программа будет работать и без matplotlib — график просто не отобразится, остальной функционал сохранится.

---

### 7. Проблемы с кодировкой писем (кракозябры в теме/теле)
**Причина:** Письмо использует нестандартную кодировку.

**Решение:** Проверьте файл `письмо.txt` в папке полученного письма — программа пытается декодировать в UTF-8 с fallback. Если проблема повторяется, проверьте исходную кодировку письма в почтовом клиенте.

---

### 8. Проблемы с путями на Windows
**Причина:** Использование прямых слэшей `/` вместо обратных `\` в путях.

**Решение:** Программа автоматически нормализует пути через `os.path.normpath()`. Указывайте пути в любом формате — программа преобразует их корректно.

---

### 9. Иконка в трее не отображается
**Причина:**
- Файл `icon.png` отсутствует в папке с программой
- Не установлены `pystray` или `Pillow`

**Решение:**
1. Убедитесь, что `icon.png` находится в одной папке с `mail_auto_processor.py`
2. Установите зависимости: `pip install pystray Pillow`

---

### 10. Программа не сворачивается в трей
**Причина:** `pystray` не установлен или не поддерживается в данной среде.

**Решение:**
- Установите `pystray` и `Pillow`
- На Linux может потребоваться дополнительная настройка системного трея (зависит от DE)
- Программа продолжит работу даже без трея — просто закрытие окна будет полным выходом

---

## Сообщить об ошибке

Если вы столкнулись с ошибкой, не описанной в этом файле:
1. Сохраните текст ошибки из консоли / журнала событий
2. Проверьте файл `mail_app.log` в папке логов
3. Опишите шаги для воспроизведения проблемы
