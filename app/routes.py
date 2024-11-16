from flask import Blueprint, render_template, jsonify, request
from app.game_logic import Game


app = Blueprint('app',__name__)

game = Game(rounds=3)

@app.route("/lobby")
def lobby():
    return render_template("lobby.html")  # Lobby page

@app.route("/round", methods=["GET", "POST"])
def round_page():
    if request.method == "GET":
        if game.state == "results":
            return render_template("results.html")
        if game.round_num == 0:
            game.start_game()
        market_info = game.start_round()
        return jsonify({
            "market_info": market_info,
            "budget": game.player.budget,
            "position": game.player.position,
            "round": game.round_num
        })
    if request.method == "POST":
        data = request.json
        # pnl eval phase
        if "guess" in data:         
            guess = int(data.get("guess"))
            result = game.eval_guess(game.player, guess)
            if game.state == "results":
                result["redirect"] = "/results"  # Redirect to results if game ends
            return jsonify(result)
        # handle action phase (buy, sell, skip)
        else:
            action_type = data.get("action_type")
            quantity = int(data.get("quantity", 0))
            result = game.execute_action(action_type, quantity)
            if game.state == "results":
                result["redirect"] = "/results"
            return jsonify(result)


@app.route("/results", methods = ["GET"])
def results_page():
    if game.state != "results":
        return render_template("round.html")
    return render_template("results.html", round_history=game.round_history)
