@echo off
REM Telegram Bot Launcher
REM Простой скрипт для запуска бота на Windows

echo.
echo ========================================================
echo.
echo   TELEGRAM BOT LAUNCHER
echo.
echo   @testpodarkibotiksbot
echo.
echo ========================================================
echo.

REM Проверить наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python не установлен или недоступен
    echo Пожалуйста, установите Python 3.9+ с https://python.org
    pause
    exit /b 1
)

echo [OK] Python найден

REM Проверить зависимости
echo [*] Проверка зависимостей...
pip show aiogram >nul 2>&1
if errorlevel 1 (
    echo [!] aiogram не установлен, устанавливаю...
    pip install -r requirements.txt
)

echo [OK] Зависимости установлены

REM Запустить бота
echo.
echo [*] Запуск бота...
echo.
echo ========================================================
echo.

python bot/main.py

REM Если скрипт завершился с ошибкой
if errorlevel 1 (
    echo.
    echo [ERROR] Ошибка при запуске бота
    echo.
    pause
    exit /b 1
)
