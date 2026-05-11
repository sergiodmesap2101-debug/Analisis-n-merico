"""
cards.py - Definiciones de cartas de evento y logica de robo.

10 cartas de evento simples con efectos en monedas, puntos o bendiciones.
Las cartas se roban aleatoriamente al caer en una casilla de Aldea.
"""

import random

EVENT_CARDS = [
    {
        "name": "Inspiracion",
        "desc": "Te sientes inspirado por el paisaje.",
        "effect": {"points": 2},
    },
    {
        "name": "Mercader Generoso",
        "desc": "Un mercader te regala algo por tu amabilidad.",
        "effect": {"coins": 3},
    },
    {
        "name": "Perdido en la Lluvia",
        "desc": "La lluvia retrasa tu viaje.",
        "effect": {"coins": -1},
    },
    {
        "name": "Encuentro Bendito",
        "desc": "Un monje bendice tu camino.",
        "effect": {"blessings": 1},
    },
    {
        "name": "Companero de Viaje",
        "desc": "Compartes historias y risas.",
        "effect": {"points": 2},
    },
    {
        "name": "Recuerdo Costoso",
        "desc": "Ese recuerdo costo mas de lo esperado.",
        "effect": {"coins": -2},
    },
    {
        "name": "Vista Panoramica",
        "desc": "Una vista impresionante te llena de alegria.",
        "effect": {"points": 1},
    },
    {
        "name": "Hallazgo Afortunado",
        "desc": "Encuentras algo valioso en el camino.",
        "effect": {"coins": 2},
    },
    {
        "name": "Anciano Sabio",
        "desc": "Un anciano comparte su sabiduria.",
        "effect": {"blessings": 1},
    },
    {
        "name": "Festival",
        "desc": "Te unes a una celebracion local!",
        "effect": {"points": 1, "coins": 1},
    },
]


def draw_card():
    """Robar una carta de evento aleatoria."""
    return random.choice(EVENT_CARDS)


def apply_card(player, card):
    """Aplicar los efectos de una carta a un jugador. Retorna lista de cadenas de resultado."""
    effect = card["effect"]
    results = []
    if "coins" in effect:
        player.add_coins(effect["coins"])
        sign = "+" if effect["coins"] >= 0 else ""
        results.append(f"{sign}{effect['coins']} Monedas")
    if "points" in effect:
        player.add_points(effect["points"])
        results.append(f"+{effect['points']} Puntos")
    if "blessings" in effect:
        player.add_blessings(effect["blessings"])
        results.append(f"+{effect['blessings']} Bendicion")
    return results
