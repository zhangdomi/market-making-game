import random


RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUITS = ['C', 'H', 'S', 'D']
AVG = 8
ROUNDS = 0

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
    
    def buy(self, quantity, price):
        if quantity * price > self.budget:
            self.budget -= 50
            return {
            "status": "error",
            "message": "Insufficient funds. A penalty of $50 has been applied.",
            }
        else:
            self.budget -= quantity * price
            self.position = quantity

    def sell(self, quantity, price):
        if quantity * price > self.budget:
            self.budget -= 50
            return {
            "status": "error",
            "message": "Insufficient funds. A penalty of $50 has been applied.",
            }
        else:
            self.budget -= quantity * price
            self.position = -quantity

    def skip(quantity, price):
        ROUNDS += 1
    
    def increase_budget(self, amt):
        self.budget += amt







class Round:
    def __init__(self):
        self.cards = self.generate_cards()
        self.face_up_amt = 0

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
    def make_market(self):
        if self.face_up_amt == 0:
            mid_point = 3 * AVG
            if random.random() < 0.3:
                offset = random.uniform(-0.3, 0.3) * mid_point  # +/- up to 30% of mid_point
                mid_point += offset
            return [mid_point - 1, mid_point + 1]
        else:
            face_up_card = next(card for card in self.cards if card.face_up)  
            face_up_value = face_up_card.get_card_rank()
            mid_point = 3 * AVG - face_up_value

            if random.random() < 0.3:
                offset = random.uniform(-0.3, 0.3) * mid_point  # +/- up to 30% of mid_point
                mid_point += offset
            return [mid_point - 1, mid_point + 1] 


    #reveal and calculate value of cards
    def reveal_cards(self):
        realized_value = sum(card.get_card_rank() for card in self.cards)
        return realized_value
 
    def calc_round_pnl(self, player_action, quantity, price):
        realized_value = self.reveal_cards()

        if player_action == 'buy':
            pnl = (realized_value - price) * quantity
        elif player_action == 'sell':
            pnl = (price - realized_value) * quantity
        else:
            pnl = 0

        return {
            "pnl": pnl,
            "realized_value": realized_value,
            "market_price": price,
            "player_action": player_action
        }

    def pnl_guess(self,player, pnl, guess):
        if pnl == guess:
            player.increase_budget(pnl)
            return {
                "result": "correct",
                "message": "Correct guess! PnL has been added to your budget.",
                "budget": player.budget
            }

        else:
            player.increase_budget(-50)
            return {
                "result": "incorrect",
                "message": "Incorrect guess. A penalty of $50 has been applied, and you do not receive the profit.",
                "budget": player.budget
            }






class Game:
    def __init__(self, rounds):
        ROUNDS = rounds
        