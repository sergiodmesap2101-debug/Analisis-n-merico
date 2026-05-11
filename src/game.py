"""
game.py - Maquina de estados del juego y logica principal.
"""

import random
from src.board import BOARD, BOARD_SIZE, get_legal_moves, get_space
from src.player import Player
from src.cards import draw_card, apply_card
from src.temple import metodo_biseccion

PHASE_MOVE = "movimiento"
PHASE_EFFECT = "efecto"
PHASE_TEMPLE = "templo"
PHASE_GAME_OVER = "fin_del_juego"


class GameState:

    def __init__(self):
        self.human = Player("Tu")
        self.ai = Player("Rival", is_ai=True)
        self.current_is_human = True
        self.phase = PHASE_MOVE
        self.turn = 1
        self.log = ["~ El viaje comienza! ~", "Tu turno - elige a donde moverte."]
        self.legal_moves = get_legal_moves(0)
        self.card_result = None
        self.effect_text = []

    def to_dict(self):
        def p(player):
            return {"name": player.name, "position": player.position,
                    "coins": player.coins, "points": player.points,
                    "blessings": player.blessings, "score": player.final_score(),
                    "finished": player.finished}
        return {
            "phase": self.phase, "turn": self.turn,
            "human": p(self.human), "ai": p(self.ai),
            "legal_moves": self.legal_moves,
            "effect_text": self.effect_text,
            "card": self.card_result,
            "log": self.log[-15:],
            "board": [{"name": s["name"], "type": s["type"]} for s in BOARD],
        }

    def select_move(self, target_pos):
        if self.phase != PHASE_MOVE or target_pos not in self.legal_moves:
            return
        self._execute_move(self.human, target_pos)

    def continue_pressed(self):
        if self.phase == PHASE_GAME_OVER:
            return
        if self.phase in (PHASE_EFFECT, PHASE_TEMPLE):
            self._next_turn()

    def _execute_move(self, player, target_pos):
        space = get_space(target_pos)
        player.move_to(target_pos)
        self.card_result = None
        self.effect_text = []
        self.log.append(f"{player.name} se movio a {space['name']}.")

        if target_pos >= BOARD_SIZE - 1:
            player.finished = True
            self.log.append(f"{player.name} llego al Fin del Viaje!")
            self.effect_text.append(f"{player.name} ha completado el viaje!")
            if self.human.finished and self.ai.finished:
                self._end_game()
                return
            self.phase = PHASE_EFFECT
            return

        stype = space["type"]

        if stype == "village":
            card = draw_card()
            results = apply_card(player, card)
            self.card_result = card
            self.effect_text.append(f"Carta: {card['name']}")
            self.effect_text.append(card["desc"])
            self.effect_text.append("Efecto: " + ", ".join(results))
            self.log.append(f"  Carta: {card['name']} ({', '.join(results)})")
            self.phase = PHASE_EFFECT

        elif stype == "market":
            player.add_coins(2)
            self.effect_text.append("Un mercado lleno de oportunidades!")
            self.effect_text.append("+2 Monedas")
            self.log.append("  Mercado: +2 Monedas")
            self.phase = PHASE_EFFECT

        elif stype == "temple":
            raiz, convergio, iters, pasos = metodo_biseccion(2.0, 3.0)
            if convergio:
                player.add_points(3)
                player.add_blessings(1)
                self.effect_text.append("Desafio del Templo")
                self.effect_text.append("Has encontrado el equilibrio de la ofrenda!")
                self.effect_text.append("+3 Puntos, +1 Bendicion")
                self.log.append(f"  Templo: +3 Pts, +1 Bend")
            else:
                self.effect_text.append("Desafio del Templo")
                self.effect_text.append("No lograste encontrar el equilibrio...")
                self.effect_text.append("Sin recompensa.")
                self.log.append("  Templo: sin convergencia.")
            self.phase = PHASE_TEMPLE

        elif stype == "inn":
            player.add_blessings(1)
            self.effect_text.append("Descansas y te recuperas en la posada.")
            self.effect_text.append("+1 Bendicion")
            self.log.append("  Posada: +1 Bendicion")
            self.phase = PHASE_EFFECT
        else:
            self.phase = PHASE_EFFECT

    def _next_turn(self):
        if self.current_is_human:
            self.current_is_human = False
            if not self.ai.finished:
                self._do_ai_turn()
            else:
                self._start_human_turn()
        else:
            self._start_human_turn()

    def _start_human_turn(self):
        self.current_is_human = True
        if self.human.finished:
            self.current_is_human = False
            if not self.ai.finished:
                self._do_ai_turn()
            return
        self.turn += 1
        self.legal_moves = get_legal_moves(self.human.position)
        self.phase = PHASE_MOVE
        self.log.append(f"--- Turno {self.turn} ---")
        self.log.append("Tu turno - elige a donde moverte.")

    def _do_ai_turn(self):
        moves = get_legal_moves(self.ai.position)
        if not moves:
            self.ai.finished = True
            self._start_human_turn()
            return
        target = random.choice(moves)
        self.log.append("--- Turno del Rival ---")
        self._execute_move(self.ai, target)

    def _end_game(self):
        ps = self.human.final_score()
        ais = self.ai.final_score()
        self.phase = PHASE_GAME_OVER
        self.effect_text = [
            "VIAJE COMPLETADO!",
            "",
            f"Tu:    {ps} pts  (P:{self.human.points}  M:{self.human.coins}  B:{self.human.blessings})",
            f"Rival: {ais} pts  (P:{self.ai.points}  M:{self.ai.coins}  B:{self.ai.blessings})",
            "",
        ]
        if ps > ais:
            self.effect_text.append("GANASTE!")
        elif ais > ps:
            self.effect_text.append("El Rival gana!")
        else:
            self.effect_text.append("Es un empate!")
        self.log.append("=" * 30)
        for line in self.effect_text:
            self.log.append(line)
