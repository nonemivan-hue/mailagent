#!/bin/bash
# Скрипт обновления для Alt Linux / любого Linux с Python 3

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "======================================"
echo " Обновление Автопроцессинга почты"
echo "======================================"
echo ""

echo "1. Остановка приложения..."
pkill -f "mail_auto_processor.py"
sleep 2

echo "2. Резервное копирование..."
[ -f "$APP_DIR/mail_config.json" ] && cp "$APP_DIR/mail_config.json" "$APP_DIR/mail_config.json.bak"
[ -f "$APP_DIR/mail_stats.json" ] && cp "$APP_DIR/mail_stats.json" "$APP_DIR/mail_stats.json.bak"

echo "3. Копирование новой версии..."
if [ -d "$APP_DIR/new_version" ]; then
    cp -r "$APP_DIR/new_version/"* "$APP_DIR/"
fi

echo "4. Установка зависимостей..."
pip3 install --user pystray Pillow matplotlib

echo "5. Запуск приложения..."
cd "$APP_DIR"
nohup python3 "$APP_DIR/mail_auto_processor.py" > /dev/null 2>&1 &

echo ""
echo "Обновление завершено. PID: $!"
