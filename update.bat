@echo off
chcp 65001 >nul
echo ==========================================
echo  Обновление Автопроцессинга почты
echo ==========================================
echo.
echo 1. Остановка текущего процесса...
taskkill /F /IM MailAutoProcessor.exe 2>nul
timeout /t 2 /nobreak >nul

echo 2. Резервное копирование настроек...
if exist mail_config.json copy /Y mail_config.json mail_config.json.bak
if exist mail_stats.json copy /Y mail_stats.json mail_stats.json.bak

echo 3. Копирование новой версии...
xcopy /Y /E "%~dp0new_version\*" "%~dp0" 2>nul

echo 4. Запуск приложения...
start "" "%~dp0MailAutoProcessor.exe"

echo.
echo Обновление завершено.
timeout /t 3
