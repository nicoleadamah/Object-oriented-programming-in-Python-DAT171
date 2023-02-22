# Computer assignment 3
# A code written by Nicole Adamah & Sofia Nilsson

from cardlib import *
from PyQt5.QtCore import *
from abc import abstractmethod
import sys

###################
# Models-only state and logic. No graphical elements at all.
###################

class CardModel(QObject):
    """ Base class that described what is expected from the CardView widget """
    new_cards = pyqtSignal()  #: Signal should be emited when cards change.

    @abstractmethod
    def __iter__(self):
        """Returns an iterator of card objects"""

    @abstractmethod
    def flipped(self):
        """Returns true of cards should be drawn face down"""

class PokerHandModel(Hand, CardModel):
    """ A model for the players hand. It can add cards, flip cards, etc."""

    def __init__(self):
        Hand.__init__(self)
        CardModel.__init__(self)
        # Additional state needed by the UI

        self.marked_cards = [False]*len(self.cards)
        self.flipped_cards = True

    def __iter__(self):
        return iter(self.cards)

    def flip(self):
        """ Flips over the cards to hide them. """
        self.flipped_cards = not self.flipped_cards
        self.new_cards.emit()

    def marked(self, i):
        """
        :param i: Index.
        :return: The marked cards.
        """
        return self.marked_cards[i]

    def flipped(self, i):
        """Flips all or no cards. """
        return self.flipped_cards

    def clicked_position(self, i):
        self.marked_cards[i] = not self.marked_cards[i]
        self.new_cards.emit()

    def add_card(self, card):
        super().add_card(card)
        self.new_cards.emit()

    def clear(self):
        self.cards.clear()
        self.new_cards.emit()

class PlayerModel(QObject):# widget for or a player area (which can be reused for each player),
    """ Where one can see e.g. the cards, money, name, total bet, for that particular player
    """

    new_money = pyqtSignal()
    new_active = pyqtSignal()
    player_no_money = pyqtSignal()

    def __init__(self, start_money: int, name: str):
        super().__init__()
        self.hand = PokerHandModel() #cards
        self.money = int(start_money) #money
        self.name = name #name
        self.total_bet = 0 #total bet
        self.active = False

    def set_active(self, active):
        """
        :param active: Activates the player
        """
        self.active = active
        self.new_active.emit()

    def get_name(self):
        """ Players name """
        return self.name

    def get_cards(self):
        """ Players cards """
        return self.hand.cards

    def reset(self):
        """ Resets the total """
        self.total_bet = 0
        self.new_total_bet.emit()

    def bet_player(self, amount: int): #players bet
        """ Players bet
        :param amount: Total amount of money
        """
        self.money -= amount
        self.total_bet += amount
        self.new_money.emit()

    def win(self, amount: int):
        self.money += amount
        self.new_money.emit()
        self.total_bet = 0

class TableModel(QObject, Hand):
    """ A model for the poker table holding up to five cards. It can clear the table, flip the cards or add cards. """
    new_cards = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.cards = []
        self.marked_cards = [False]*len(self.cards)
        self.flipped_cards = True

    def add_card(self, card):
        super().add_card(card)
        self.new_cards.emit()

    def clear(self):
        self.cards.clear()
        self.new_cards.emit()

    def flip(self):
        self.flipped_cards = not self.flipped_cards
        self.new_cards.emit()

    def marked(self, i):
        return self.marked_cards[i]

    def flipped(self, i):
        return self.flipped_cards

    def clicked_position(self, i):
        self.marked_cards[i] = not self.marked_cards[i]
        self.new_cards.emit()

class PotModel(QObject):
    """ Creates a model for the pot. """
    new_pot = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.money = 0

    def get_value(self):
        return self.money

    def __iadd__(self, other):
        self.money += other
        self.new_pot.emit()
        return self

    def clear(self):
        """ Clears the pot. """
        self.money = 0
        self.new_pot.emit()

class TexasHoldEm(QObject):
    """ A Texas Hold'em class that contains all the logics and rules of the poker game. """

    new_active_player = pyqtSignal()
    winner = pyqtSignal((str,))
    message = pyqtSignal((str,))
    player_no_money = pyqtSignal((str,))
    game_finished = pyqtSignal()

    def __init__(self, players):
        """
        :param players: Players in the game.
        """
        super().__init__()
        self.running = False
        self.players = players
        self.table_cards = TableModel()
        self.pot = PotModel()
        self.last_bets = []
        self.deck = None
        self.new_round()
        self.active_player = 0

    def new_round(self):
        """ Starting a new round. """
        self.running = True
        self.pot.clear()
        self.deck = StandardDeck()
        self.deck.shuffle()
        self.calling = 0
        self.players[0].set_active(True)
        self.last_bets = []

        # Deal cards:
        for i in range(2):
            self.players[0].hand.add_card(self.deck.draw())
            self.players[1].hand.add_card(self.deck.draw())

    def active_player(self):
        """
        :return: The current active player.
        """
        return self.players[self.active_player]

    def next_player(self):
        """ Moves on to the next player. """
        self.active_player = (1 + self.active_player) % 2
        self.new_active_player.emit()

    def fold(self):
        """ Folding occurs when you give up on the hand when it is your turn to act. """
        fold = True
        self.evaluating_winner(fold)

    def call(self):
        """ Putting in the same amount of money as the previous player. If both player calls, there is a new card on the table. """

        if len(self.last_bets) == 0:
            self.message.emit(" Can't call before betting! ")
            return
        self.calling += 1

        if self.calling == 2:
            self.calling = 0
            if len(self.table_cards.cards) == 0:
                for more_cards in range(3):
                    self.table_cards.add_card(self.deck.draw())
            elif len(self.table_cards.cards) < 5:
                self.table_cards.add_card(self.deck.draw())
            else:
                self.player = self.players[self.active_player]
                self.player.bet_player(self.last_bets[-1])
                self.pot += self.last_bets[-1]
                self.evaluating_winner()
                return

        self.player = self.players[self.active_player]
        self.player.bet_player(self.last_bets[-1])
        self.pot += self.last_bets[-1]
        self.next_player()

    def bet(self, amount: int):
        """ Putting in money into the game.
        :param amount: The amount of money.
        """
        self.player = self.players[self.active_player]
        self.pot += amount
        self.player.bet_player(amount)
        self.calling = 0 # call_count
        self.last_bets.append(amount)
        self.next_player()

        if self.player.money < 0:
            self.player_no_money.emit(" You don't have any money left! ")
            self.exit_game()
            return

    def evaluating_winner(self, fold: bool = False):
        ''' Evaluates the winner, distributes the money and gets ready for the next round.
        :params: fold = boolean.
        '''
        self.fold = fold
        a = self.active_player
        b = self.active_player = (1 + self.active_player) % 2
        player1 = self.players[a]
        player2 = self.players[b]

        player1_pokerhand = player1.hand.best_poker_hand(self.table_cards.cards)
        player2_pokerhand = player2.hand.best_poker_hand(self.table_cards.cards)

        if self.fold:
                player2.win(self.pot.get_value())
                self.message.emit("Winner is: " + str(player2.get_name()))
                print("Winner is: " + str(player2.get_name()))
        else:  # Checking the best hand if no one chose to fold.
            if  player1_pokerhand > player2_pokerhand:
                player1.win(self.pot.get_value())
                self.message.emit("Winner is: " + str(player1.get_name()))
                print("Winner is: " + str(player1.get_name()))
            else:
                player2.win(self.pot.get_value())
                self.message.emit("Winner is: " + str(player2.get_name()))
                print("Winner is: " + str(player2.get_name()))

        self.table_cards.clear()
        player1.hand.clear()
        player2.hand.clear()
        self.new_round()

    @staticmethod
    def exit_game():
        """ Exits the game if a player doesn't have any money left. """
        sys.exit()
