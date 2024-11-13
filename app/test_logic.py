import unittest
from game_logic import RANKS, SUITS, AVG, ROUNDS, Card, Player, Round, Game
import random

class TestCard(unittest.TestCase):
    def test_get_rank(self):
        card = Card("K", "H")
        self.assertEqual(card.get_card_rank(), "13")

        card = Card("A", "H")
        self.assertEqual(card.get_card_rank(), "14")

        card = Card("2", "H")
        self.assertEqual(card.get_card_rank(), "2")

        card = Card("1", "H")
        self.assertEqual(card.get_card_rank(), "13")

    def test_get_suit(self):
        card = Card("K", "H")
        self.assertEqual(card.get_card_suit(), "H")

        card = Card("A", "S")
        self.assertEqual(card.get_card_suit(), "S")

        card = Card("2", "D")
        self.assertEqual(card.get_card_suit(), "D")

        card = Card("1", "C")
        self.assertEqual(card.get_card_suit(), "C") 

class TestPlayer(unittest.TestCase):
    player = Player()

    def test_initial_budget(self):
        self.assertEqual(self.player.get_budget(), 500)
    
    def test_buy(self):
        result = self.player.buy(10, 20)
        self.assertEqual(self.player.get_budget(), 300)
        self.assertEqual(self.player.get_position(), 10)

        result = self.player.buy(10, 45)
        self.assertEqual(self.player.get_budget(), 250)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Insufficient funds. A penalty of $50 has been applied.")

    def test_increase_budget(self):
        self.player.increase_budget(250)
        self.assertEqual(self.player.get_budget(), 500)

    def test_sell(self):
        result = self.player.sell(10, 20)
        self.assertEqual(self.player.get_budget(), 700)
        self.assertEqual(self.player.get_position(), -10)

        result = self.player.sell(10, 1000)
        self.assertEqual(self.player.get_budget(), 650)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Insufficient funds. A penalty of $50 has been applied.")

    #TODO: finish this
    #def test_skip()

class TestRound(unittest.TestCase):
    round = Round()

    def test_generate_cards(self):
        cards = self.round.generate_cards()
        self.assertEqual(len(cards), 3)
        for i in len(cards):
            self.assertIn(cards[i].get_card_rank(), RANKS)
            self.assertIn(cards[i].get_card_suit(), SUITS)
    
    def test_make_market(self):
        self.round.make_market()
        self.assertEqual(len(self.round.market), 2)
        self.assertTrue(self.round.market[1] > self.round.market[0])
        self.assertTrue(self.round.market[1] - self.round.market[0] == 2)

    def test_calc_round_pnl_buy(self):
        self.round.market = [10, 12]
        pnl = self.round.calc_round_pnl("buy", 10, 12)["pnl"]
        self.assertEqual(pnl, (self.round.reveal_cards() - 12) * 10)

    def test_calc_round_pnl_sell(self):
        self.round.market = [10, 12]
        pnl = self.round.calc_round_pnl("sell", 10, 10)["pnl"]
        self.assertEqual(pnl, (10 - self.round.reveal_cards()) * 10)


class TestGame(unittest.TestCase):
    game = Game(3)

    def test_start_game(self):
        self.assertTrue(self.game.state == "lobby")
        self.game.start_game()
        self.assertEqual(self.game.round_num, 1)
        self.assertEqual("message", "Round 1")
        self.assertTrue(self.game.state == "round")
        
    def test_execute_action_buy(self):
        self.game.start_game()
        self.game.curr_round.market = [27, 29]
        result = self.game.execute_action("buy", 10)
        self.assertEqual(result["budget"], 210)
        self.assertEqual(result["position"], 10)
        self.assertIn("message", result)
    
    #TODO: finish
    def test_eval_guess_buy(self):
        return #delete this

    #TODO: think about mechanics of selling and how if affects budgeting
    game = Game(3)
    def test_execute_action_sell(self):
        self.game.start_game()
        self.game.curr_round.market = [27, 29]
        result = self.game.execute_action("sell", 10)
        self.assertEqual(result["budget"], 210)
        self.assertEqual(result["position"], 10)
        self.assertIn("message", result)

   #TODO: test execution(skip)