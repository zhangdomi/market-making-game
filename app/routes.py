from flask import Blueprint, render_template, jsonify, request
from app.game_logic import Game


app = Blueprint('app',__name__)

game = Game(rounds=3)                   #set to 0 eventually

@app.route("/")
def lobby():
    game.game_reset()
    return render_template("lobby.html")  # Lobby page

@app.route("/round", methods=["GET", "POST"])
def round_page():
    if request.method == "GET":
        if game.state == "results":
            return render_template("results.html")
        if game.round_num == 0:
            market_info = game.start_game()
            return render_template(
            "round.html",
            market_info=market_info["market_info"],
            budget=game.player.budget,
            position=game.player.position,
            round=game.round_num
        )
        elif game.round_num != 0:
            market_info = game.start_round()
            return render_template(
                "round.html",
                market_info=market_info["market_info"],
                budget=game.player.budget,
                position=game.player.position,
                round=game.round_num
            )
    if request.method == "POST":
        data = request.json
        # pnl eval phase
        if "guess" in data:         
            guess = int(data.get("guess"))
            result = game.eval_guess(guess)
            if game.state == "results":
                result["redirect"] = "/results"  # Redirect to results if game ends
            #go to next round after eval
            else:
                market_info = game.start_round()
                result.update({
                    "next_round": True,
                    "market_info": market_info["market_info"],
                    "budget": game.player.budget,
                    "position": game.player.position,
                    "round": game.round_num,
                })
            return jsonify(result)
        # handle action phase (buy, sell, skip)
        else:
            action_type = data.get("action_type")
            if action_type == "skip":
                # Ensure market_info is defined for skip
                market_info = game.curr_round.market if game.curr_round else [None, None]

                # End of game check
                if game.round_num >= game.total_rounds:
                    game.state = "results"
                    result = {
                        "round": game.round_num,
                        "market": market_info,
                        "action": "skip",
                        "quantity": 0,
                        "pnl": 0,
                        "player_guess": None,
                        "correct_guess": None,
                        "budget": game.player.budget,
                        "cards": [f"{card.rank}{card.suit}" for card in game.curr_round.cards] if game.curr_round else [],
                    }
                    game.round_history.append(result)
                    return jsonify({"redirect": "/results"})

                # Ongoing game skip
                result = {
                    "round": game.round_num,
                    "market": market_info,
                    "action": "skip",
                    "quantity": 0,
                    "pnl": 0,
                    "player_guess": None,
                    "correct_guess": None,
                    "budget": game.player.budget,
                    "cards": [f"{card.rank}{card.suit}" for card in game.curr_round.cards],
                }
                game.round_history.append(result)
                market_info = game.start_round()
                return jsonify({
                    "next_round": True,
                    "market_info": market_info["market_info"],
                    "round": game.round_num,
                    "budget": game.player.budget,
                })

            quantity = int(data.get("quantity", 0))
            result = game.execute_action(action_type, quantity)
            if game.state == "results":
                result["redirect"] = "/results"
            return jsonify(result)


@app.route("/results", methods = ["GET", "POST"])
def results_page():
    global game
    if request.method == "POST":
        game = Game(3)
        return jsonify({"message": "Game reset successfully."})
    if game.state != "results":
        return render_template("round.html")
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"round_history": game.round_history})
    return render_template("results.html", round_history=game.round_history)
