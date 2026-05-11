"""
board.py - Definicion del tablero y logica de movimiento.

El tablero es una ruta lineal de 14 casillas (indice 0 a 13).
La casilla 0 es Inicio, la casilla 13 es Fin del Viaje.
Cuatro tipos de ubicacion: Aldea, Mercado, Templo, Posada.
"""

# Disposicion del tablero: lista de casillas de Inicio a Fin
BOARD = [
    {"name": "Inicio",            "type": "start"},
    {"name": "Aldea del Bambu",   "type": "village"},
    {"name": "Mercado del Rio",   "type": "market"},
    {"name": "Templo Montana",    "type": "temple"},
    {"name": "Posada Farol",      "type": "inn"},
    {"name": "Aldea del Arce",    "type": "village"},
    {"name": "Mercado Puerto",    "type": "market"},
    {"name": "Templo Nube",       "type": "temple"},
    {"name": "Posada Jardin",     "type": "inn"},
    {"name": "Aldea de la Grulla","type": "village"},
    {"name": "Mercado de Seda",   "type": "market"},
    {"name": "Templo Luna",       "type": "temple"},
    {"name": "Posada Atardecer",  "type": "inn"},
    {"name": "Fin del Viaje",     "type": "end"},
]

BOARD_SIZE = len(BOARD)  # 14


def get_legal_moves(position):
    """Retorna lista de posiciones legales a las que el jugador puede moverse (1, 2 o 3 adelante)."""
    moves = []
    for step in range(1, 4):
        new_pos = position + step
        if new_pos < BOARD_SIZE:
            moves.append(new_pos)
    return moves


def get_space(position):
    """Retorna el diccionario de la casilla en la posicion dada."""
    if 0 <= position < BOARD_SIZE:
        return BOARD[position]
    return None
