@echo off
title Наполнение базы данных Армстрим
color 0A

echo ==========================================
echo    ПОДГОТОВКА БАЗЫ ДАННЫХ АРМСТРИМ
echo ==========================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Python не найден!
    pause
    exit
)

echo [1/2] Запуск скрипта наполнения...
python seed.py

if %errorlevel% neq 0 (
    echo.
    echo [ОШИБКА] Ошибка при выполнении скрипта.
    pause
    exit
)

echo.
echo [2/2] База данных успешно обновлена!
echo ==========================================
echo Теперь запускай run_server.bat
echo ==========================================
pause