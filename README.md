# Juego de Viaje — Un Viaje Tranquilo 🏯

Prototipo de juego de viaje por turnos para un proyecto academico de metodos numericos.
Dos jugadores (humano + IA) viajan por una ruta lineal visitando aldeas, mercados, templos y posadas.

---

## Como Ejecutar

### Requisitos
- Python 3.8+

### Ejecutar
```bash
cd TravelGame
pip install -r requirements.txt
python app.py
```
Luego abre **http://localhost:5000** en tu navegador.

### Script rapido (Windows)
```bash
scripts\run.bat
```

---

## Reglas del Juego

| Tipo    | Efecto                              |
|---------|--------------------------------------|
| Aldea   | Robar una carta de evento aleatoria |
| Mercado | +2 Monedas                          |
| Templo  | Desafio numerico (+3 Pts, +1 Bend)  |
| Posada  | +1 Bendicion                        |

**Puntaje Final** = Puntos + Monedas + (2 x Bendiciones)

---

## Metodos Numericos — Metodo de Biseccion

Cuando un jugador cae en un **Templo**, se ejecuta internamente el Metodo de Biseccion:

```
f(x) = x³ - 4x - 2 = 0    en [2, 3]
Tolerancia: 0.001 | Max iteraciones: 50
```

- Si **converge** → +3 Puntos, +1 Bendicion
- Si **no converge** → sin recompensa

Implementado manualmente en `src/temple.py` (sin librerias externas).

---

## Estructura

```
TravelGame/
├── app.py              # Servidor Flask
├── requirements.txt    # Dependencias
├── src/
│   ├── board.py        # Tablero (14 casillas)
│   ├── player.py       # Clase Jugador
│   ├── cards.py        # 10 cartas de evento
│   ├── temple.py       # Metodo de Biseccion
│   └── game.py         # Logica del juego
├── templates/
│   └── index.html      # Pagina del juego
├── static/
│   ├── style.css       # Estilos
│   └── game.js         # Frontend
└── scripts/
    ├── run.bat
    └── run.sh
```
