@echo off
echo ========================================
echo   Juego de Viaje - Un Viaje Tranquilo
echo ========================================
echo.
cd /d "%~dp0\.."
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3 no esta instalado o no esta en el PATH.
    pause
    exit /b 1
)
pip install -r requirements.txt --quiet
echo Iniciando servidor web...
echo Abre tu navegador en: http://localhost:5000
echo.
python app.py
pause
