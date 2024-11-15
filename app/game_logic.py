import random


RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUITS = ['C', 'H', 'S', 'D']
AVG = 8

class Card:
    def __init__(self, rank, suit):
        self.rank = rank #A(1) to K(13)
        self.suit = suit #C, H, S, D
        self.face_up = False
    
    def get_card_rank(self):
        if self.rank == 'J':
            return 11
        elif self.rank == 'Q': return 12
        elif self.rank == 'K': return 13
        elif self.rank == 'A':
            return 14
        else:
            return int(self.rank)
        

    def get_card_suit(self):
        if self.suit == 'C':
            return 1
        elif self.suit == 'H':
            return 2
        elif self.suit == 'S':
            return 3
        else:
            return 4

    def __repr__(self) -> str:
        if self.face_up == True:
            return f"{self.rank}{self.suit}"
        else:
            return f"X"         #representation of a face-down card


class Player:
    def __init__(self):
        self.budget = 500
        self.position = 0
        self.sell_price = None
        self.buy_price = None

    def get_budget(self): return self.budget
    def get_position(self): return self.position
    # def get_buy_price(self): return self.buy_price
    # def get_sell_price(self): return self._price 

    def buy(self, quantity, price):
        if quantity * price > self.budget:
            self.budget -= 50
            return {
            "status": "error",
            "message": "Insufficient funds. A penalty of $50 has been applied.",
            }
        else:
            self.position = quantity
            self.buy_price = price

    def sell(self, quantity, bid_price):
        if quantity * bid_price > self.budget:
            self.budget -= 50
            return {
            "status": "error",
            "message": "Insufficient funds. A penalty of $50 has been applied.",
            }
        else:
            # self.budget -= quantity * price
            self.position = -quantity
            self.sell_price = bid_price

    def increase_budget(self, amt):
        self.budget += amt


class Round:
    def __init__(self):
        self.face_up_amt = 0
        self.cards = self.generate_cards()
        self.market = []

    #generates 3 cards for the round
    def generate_cards(self):
        cards = []
        for _ in range(3):
            rank = random.choice(RANKS)
            suit = random.choice(SUITS)
            card = Card(rank, suit)
            cards.append(card)

        no_face_up = random.choice([0, 1])

        if no_face_up == 1:
            self.face_up_amt = 1
            card_to_be_face_up = random.choice(cards)
            card_to_be_face_up.face_up = True
        
        return cards

    #make a bid/ask market
    #sets market
    def make_market(self):
        if self.face_up_amt == 0:
            mid_point = 3 * AVG
            if random.random() < 0.3:
                offset = random.uniform(-0.3, 0.3) * mid_point  # +/- up to 30% of mid_point
                mid_point += offset
                round(mid_point)
                if mid_point < 0:
                    return "market is negative."
            self.market = [mid_point - 1, mid_point + 1]
        else:
            face_up_card = next(card for card in self.cards if card.face_up == True)  
            face_up_value = face_up_card.get_card_rank()
            mid_point = 3 * AVG - face_up_value

            if random.random() < 0.3:
                offset = random.uniform(-0.3, 0.3) * mid_point  # +/- up to 30% of mid_point
                mid_point += offset
            self.market = [mid_point - 1, mid_point + 1] 


    #reveal and calculate value of cards
    def reveal_cards(self):
        realized_value = sum(card.get_card_rank() for card in self.cards)
        return realized_value
    
    #calculate actual pnl, based on player's action
    #param: player's action, quantity, market_price
    def calc_round_pnl(self, player, player_action, input_quantity):
        realized_value = self.reveal_cards()

        if player_action == 'buy':
            pnl = (realized_value - player.buy_price) * input_quantity
            # print("GAME - Buy Price:", player.buy_price)
            # print("GAME - Realized val:", realized_value)
            market_price = player.buy_price
        elif player_action == 'sell':
            pnl = (player.sell_price - realized_value) * input_quantity
            market_price = player.sell_price
        else:
            pnl = 0
            market_price = None

        return {
            "pnl": pnl,
            "realized_value": realized_value,
            "market_price": market_price,
            "player_action": player_action
        }


class Game:
    def __init__(self, rounds):
        self.player = Player()
        self.total_rounds = rounds
        self.curr_round = None       #stores a Round class
        self.round_num = 0
        self.state = "lobby"
        self.last_action = None
        self.round_history = []

    def start_game(self):
        self.round_num = 0
        self.state = "round"
        return self.start_round()
    
    def start_round(self):
        self.round_num += 1
        self.curr_round = Round()
        self.curr_round.make_market()

        return {
            "message": f"Round {self.round_num}",
            "market_info": self.curr_round.market,
            "budget": self.player.budget,
            "position": self.player.position
        }


    def execute_action(self, action_type, quantity):
        bid_price, ask_price = self.curr_round.market
        self.last_action = action_type

        if action_type == "buy":
            action_result = self.player.buy(quantity, ask_price)
        elif action_type == "sell":
            action_result = self.player.sell(quantity, bid_price) 
        else:
            action_result = {"message": "Round skipped."}
        
        return {
            "message": action_result["message"] if isinstance(action_result, dict) else "Action completed.",
            "budget": self.player.budget,
            "position": self.player.position
        }

    def eval_guess(self, guess):
        quantity = abs(self.player.position)

        actual_pnl = self.curr_round.calc_round_pnl(self.player, self.last_action, quantity)["pnl"]

        # if self.last_action == "buy":
        #     actual_pnl = self.curr_round.calc_round_pnl(self.last_action, self.player.position, self.curr_round.market[1])["pnl"]
        # elif self.last_action == "sell":
        #     actual_pnl = self.curr_round.calc_round_pnl(self.last_action, self.player.position, self.curr_round.market[0])["pnl"]
            
        if actual_pnl == guess:
            self.player.increase_budget(actual_pnl)
            result = {
                "result": "correct",
                "message": "Correct guess! PnL has been added to your budget.",
                "budget": self.player.budget
            }
        else:
            self.player.increase_budget(-50)
            result = {
                "result": "incorrect",
                "message": "Incorrect guess. A penalty of $50 has been applied, and you do not receive the profit.",
                "budget": self.player.budget
            }
        
        if self.round_num >= self.total_rounds:
            self.state = "results"

        action_qty = abs(self.player.position)
        self.player.position = 0
        self.round_history.append({
            "round": self.round_num,
            "market": [self.curr_round.market[0], self.curr_round.market[1]],
            "action": self.last_action,
            "quantity": action_qty,
            "pnl": actual_pnl,
            "player_guess": guess,  
            "correct_guess": actual_pnl == guess,
            "budget": self.player.budget
        })
        return result
    