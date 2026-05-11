"""
app.py - Servidor web Flask para el Juego de Viaje.
Ejecutar: python app.py
"""

from flask import Flask, render_template, jsonify, request
from src.game import GameState

app = Flask(__name__)
game = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/nuevo", methods=["POST"])
def nuevo_juego():
    global game
    game = GameState()
    return jsonify(game.to_dict())


@app.route("/api/estado")
def estado():
    if game is None:
        return jsonify({"error": "sin juego"}), 400
    return jsonify(game.to_dict())


@app.route("/api/mover", methods=["POST"])
def mover():
    if game is None:
        return jsonify({"error": "sin juego"}), 400
    pos = request.json.get("position")
    game.select_move(pos)
    return jsonify(game.to_dict())


@app.route("/api/continuar", methods=["POST"])
def continuar():
    if game is None:
        return jsonify({"error": "sin juego"}), 400
    game.continue_pressed()
    return jsonify(game.to_dict())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
