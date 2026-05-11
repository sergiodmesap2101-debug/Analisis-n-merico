#!/bin/bash
echo "========================================"
echo "  Juego de Viaje - Un Viaje Tranquilo"
echo "========================================"
echo
cd "$(dirname "$0")/.."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no esta instalado."
    exit 1
fi
pip3 install -r requirements.txt --quiet
echo "Iniciando servidor web..."
echo "Abre tu navegador en: http://localhost:5000"
echo
python3 app.py
