"""
player.py - Clase de datos del jugador.

Rastrea posicion, recursos (monedas, puntos, bendiciones) y estado de finalizacion.
"""


class Player:
    """Representa un jugador (humano o IA) en el juego de viaje."""

    def __init__(self, name, is_ai=False):
        self.name = name
        self.is_ai = is_ai
        self.position = 0       # Inicia en la posicion 0
        self.coins = 0
        self.points = 0
        self.blessings = 0
        self.finished = False

    def move_to(self, position):
        """Mover al jugador a la posicion dada del tablero."""
        self.position = position

    def add_coins(self, amount):
        """Agregar (o restar) monedas. Minimo 0."""
        self.coins = max(0, self.coins + amount)

    def add_points(self, amount):
        """Agregar puntos."""
        self.points += amount

    def add_blessings(self, amount):
        """Agregar bendiciones."""
        self.blessings += amount

    def final_score(self):
        """Calcular puntaje final: puntos + monedas + (2 * bendiciones)."""
        return self.points + self.coins + (2 * self.blessings)
