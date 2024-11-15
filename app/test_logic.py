import unittest
from .game_logic import RANKS, SUITS, AVG, Card, Player, Round, Game
import random

class TestCard(unittest.TestCase):
    def test_get_rank(self):
        card = Card("K", "H")
        self.assertEqual(card.get_card_rank(), 13)

        card = Card("A", "H")
        self.assertEqual(card.get_card_rank(), 14)

        card = Card("2", "H")
        self.assertEqual(card.get_card_rank(), 2)

        # card = Card("1", "H")
        # self.assertEqual(card.get_card_rank(), 13)

    def test_get_suit(self):
        card = Card("K", "H")
        self.assertEqual(card.get_card_suit(), 2)

        card = Card("A", "S")
        self.assertEqual(card.get_card_suit(), 3)

        card = Card("2", "D")
        self.assertEqual(card.get_card_suit(), 4)

        card = Card("1", "C")
        self.assertEqual(card.get_card_suit(), 1) 

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_initial_budget(self):   
        self.assertEqual(self.player.get_budget(), 500)
    
    def test_buy(self):
        result = self.player.buy(10, 20)
        self.assertEqual(self.player.get_budget(), 500)
        self.assertEqual(self.player.get_position(), 10)

        result = self.player.buy(10, 55)
        self.assertEqual(self.player.get_budget(), 450)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Insufficient funds. A penalty of $50 has been applied.")

    def test_increase_budget(self):
        self.player.budget = 500
        self.player.increase_budget(250)
        self.assertEqual(self.player.get_budget(), 750)

    def test_sell(self):
        self.player.budget = 500
        result = self.player.sell(10, 20)
        self.assertEqual(self.player.get_budget(), 500)
        self.assertEqual(self.player.get_position(), -10)

        result = self.player.sell(10, 1000)
        self.assertEqual(self.player.get_budget(), 450)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Insufficient funds. A penalty of $50 has been applied.")

    #TODO: finish this
    #def test_skip()

class TestRound(unittest.TestCase):
    def setUp(self):
        self.round = Round()
        self.player = Player()
        self.game = Game(3)

    def test_generate_cards(self):
        test_ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        test_suits = [1 , 2, 3, 4]
        cards = self.round.generate_cards()
        self.assertEqual(len(cards), 3)
        for i in range(0, len(cards)):
            self.assertIn(cards[i].get_card_rank(), test_ranks)
            self.assertIn(cards[i].get_card_suit(), test_suits)
    
    def test_make_market(self):
        self.round.make_market()
        self.assertEqual(len(self.round.market), 2)
        self.assertTrue(self.round.market[1] > self.round.market[0])
        self.assertTrue(self.round.market[1] - self.round.market[0] == 2)

    def test_calc_round_pnl_buy(self):
        self.game.start_game()
        self.game.start_round()
        self.game.curr_round.market = [10, 12]
        self.game.execute_action("buy", 10)
        pnl = self.game.curr_round.calc_round_pnl(self.game.player, "buy", 10)["pnl"]
        self.assertEqual(pnl, (self.game.curr_round.reveal_cards() - 12) * 10)


    def test_calc_round_pnl_sell(self):
        self.game.start_game()
        self.game.start_round()
        self.game.curr_round.market = [10, 12]
        self.game.execute_action("sell", 10)
        pnl = self.game.curr_round.calc_round_pnl(self.game.player, "sell", 10)["pnl"]
        self.assertEqual(pnl, (10 - self.game.curr_round.reveal_cards()) * 10)


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(3)

    def test_start_game(self):
        self.assertTrue(self.game.state == "lobby")
        self.game.start_game()
        self.assertEqual(self.game.round_num, 1)
        self.assertEqual(self.game.round_num, 1)
        self.assertTrue(self.game.state == "round")
        
    def test_execute_action_buy(self):
        self.game.start_game()
        self.game.curr_round.market = [27, 29]
    
        #valid buy order
        result = self.game.execute_action("buy", 10)
        self.assertEqual(result["position"], 10)

        #invalid buy order
        self.game.player.budget = 500
        self.game.player.position = 0
        result = self.game.execute_action("buy", 20)
        self.assertEqual(result["budget"], 450)
        self.assertIn("message", result)
    
    def test_eval_guess_buy(self):
        self.game.start_game()
        self.game.curr_round.market = [27,29]
        quantity = 10
        ask_price = 29
        self.game.execute_action("buy", quantity=quantity)
        self.assertEqual(self.game.player.position, quantity)

        self.game.curr_round.reveal_cards = lambda: 35 #manually setting realized value of cards to 35
        expected_pnl = (35 - ask_price) * quantity

        #test w/ correct guess
        result_of_correct_guess = self.game.eval_guess(expected_pnl)
        self.assertEqual(result_of_correct_guess["result"], "correct")
        self.assertEqual(result_of_correct_guess["budget"], 500 + expected_pnl)
        self.assertEqual(self.game.player.budget, 500 + expected_pnl)

        #test w/ incorrect guess
        self.game.player.budget = 500
        result_of_incorrect_guess = self.game.eval_guess(expected_pnl + 10)
        self.assertEqual(result_of_incorrect_guess["result"], "incorrect")
        self.assertEqual(result_of_incorrect_guess["budget"], 450)
        self.assertEqual(self.game.player.budget, 450)
 

    #TODO: think about mechanics of selling and how if affects budgeting
    def test_execute_action_sell(self):
        self.game.start_game()
        self.game.curr_round.market = [27, 29]
        result = self.game.execute_action("sell", 10)
        self.assertEqual(result["budget"], 500)
        self.assertEqual(result["position"], -10)
        self.assertIn("message", result)

    def test_eval_guess_sell(self):
        self.game.start_game()
        self.game.curr_round.market = [27,29]
        quantity = 10
        bid_price = 27
        self.game.execute_action("sell", quantity=quantity) 
        
        self.assertEqual(self.game.player.budget, 500) #test if budget changes after sell order
        self.assertEqual(self.game.player.position, -quantity)
        
        self.game.curr_round.reveal_cards = lambda: 35 #manually setting realized value of cards to 35
        expected_pnl = (bid_price - 35) * quantity 
        
        #correct guess
        result_correct_guess = self.game.eval_guess(expected_pnl)
        self.assertEqual(result_correct_guess["result"], "correct")
        self.assertEqual(result_correct_guess["budget"], 500 + expected_pnl)
        self.assertEqual(self.game.player.budget, 500 + expected_pnl)

        #incorrect guess
        self.game.player.budget = 500
        result_incorrect_guess = self.game.eval_guess(expected_pnl + 10)
        self.assertEqual(result_incorrect_guess["result"], "incorrect")
        self.assertEqual(result_incorrect_guess["budget"], 450)
        self.assertEqual(self.game.player.budget, 450)