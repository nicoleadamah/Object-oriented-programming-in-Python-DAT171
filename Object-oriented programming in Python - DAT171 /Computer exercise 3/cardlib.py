# Computer assignment 2
# A code written by Nicole Adamah & Sofia Nilsson

from enum import Enum, IntEnum
import abc
import random
from collections import Counter

## CREATING ALL THE CLASSES
class Suit(IntEnum):
    """ A class for the suits to make it possible to iterate and value the suits. """
    Hearts, Spades, Clubs, Diamonds = range(1,5)

class PlayingCard(metaclass=abc.ABCMeta): # class
    """
    Superclass PlayingCard that creates init for suit and the abstract method get_value.
    """
    def __init__(self, suit: Suit):
        """ Creating a playing card
        :param suit: The suit of the card
        """
        self.suit = suit

    @abc.abstractmethod
    def get_value(self):
        """Returns the value of the card. This one is overloaded. """

    def __lt__(self, other):
        """Comparing two cards as tuples. This one is overloaded.
        :param other: The cards that will be compared
        :return: a boolean, true or false
        """
        return(self.get_value(), self.suit.value) < (other.get_value(), other.suit.value)

    def __eq__(self, other):
        """Applies the equal to the operator.  This one is overloaded.
        :other: The Cards that will be compared
        :return: a boolean, true or false
        """
        return(self.get_value(), self.suit.value) == (other.get_value(), other.suit.value)

class NumberedCard(PlayingCard):
    """First subclass to PlayingCard. Implements values that can be between 2 and 10 """
    def __init__(self, value: int, suit: Suit):
        """
        :param value: The value of the card that will be created
        :param suit: inherits a suit from Suit
        """
        super().__init__(suit)
        self.value = value

    def get_value(self):
        """A method to get the rank (value) of numbered card.
        :return: An integer value of checked card"""
        return self.value

    def get_suit(self):
        """
        :return: the suit of the card.
        """
        return self.suit

    def __str__(self):
        """
        :return: A nicer representation of the Numbered Cards.
        """
        return "{} of {}".format(self.value, self.suit.name)


class JackCard(PlayingCard): #subclass
    """ Subclass to PlayingCard. Creates the Jack-card with all types of suits with the value 11. """

    def get_value(self):
        """
        :return: The value of the card
        """
        return 11

    def __str__(self):
        """
        :return: A nicer representation of the Jack Card.
        """
        return 'Jack of' + ' ' + format(self.suit.name)

class QueenCard(PlayingCard): # subclass
    """ Subclass to PlayingCard. Creates the Queen-card with all types of suits with the value 12. """

    def get_value(self):
        """
        :return: The value of the card
        """
        return 12

    def __str__(self):
        """
        :return: A nicer representation of the Queen card.
        """
        return 'Queen of' + ' ' + format(self.suit.name)

class KingCard(PlayingCard):
    """ Subclass to PlayingCard. Creates the King-card with all types of suits with the value 13. """

    def get_value(self):
        """
        :return: The value of the card.
        """
        return 13

    def __str__(self):
        """
        :return: A nicer presentation of the King card.
        """
        return 'King of' + ' ' + format(self.suit.name)

class AceCard(PlayingCard): # subclass
    """ Subclass to PlayingCard. Creates the Ace-card with all types of suits with the value 14. Note that in later on
    in the code, the value of Ace can either be 14 or 1. """

    def get_value(self):
        """
        :return: The value of the card.
        """
        return 14

    def __str__(self):
        """
        :return: A nicer presentation of the card.
        """
        return 'Ace of' + ' ' + format(self.suit.name)

# -----------------------------------------------------------------#
# CREATING A DECK
class StandardDeck:
    """ A class that creates the full standard deck of 52 cards."""
    def __init__(self):
        self.deck = []
        for suit in Suit:
            self.deck.append(JackCard(suit))
            self.deck.append(QueenCard(suit))
            self.deck.append(KingCard(suit))
            self.deck.append(AceCard(suit))
            for value in range(2,11):
                self.deck.append(NumberedCard(value, suit))
            self.shuffle()

    def __len__(self):
        """A method that returns how many cards the is left in the deck."""
        return len(self.deck)

    def draw(self):
        """
        A method to draw the top card. If there is no cards left, an error will occur.
        :return: The drawn card from the top of the deck.
        """
        if len(self.deck) < 1:
            raise NoMoreCards()
        drawn_card = self.deck[0]
        self.deck.remove(self.deck[0])
        return drawn_card

    def shuffle(self):
        """A method that shuffles the deck."""
        random.shuffle(self.deck)

    def __repr__(self):
        """A nice presentation of the full deck."""
        return str(self)

    def __str__(self):
        """A nicer presentation of the deck"""
        return str(self.deck)

class NoMoreCards(ValueError):
    """If there are no cards left in the deck, there will be an error. """
    def __str__(self):
        return "There are no cards left"


# -----------------------------------------------------------------#
# CREATING A HAND
class Hand:
    """Creates the class Hand. The hand has methods to add, drop and sort cards. """
    def __init__(self):
        self.cards = []

    def __str__(self):
        """A nicer represenation of the cards on hand. """
        return "A hand with the cards: " + ', '.join([str(x) for x in self.cards])

    def add_card(self, card):
         """Add cards to the hand"""
         self.cards.append(card)

    def drop_cards(self, index_cards):
        """

        :param index_cards: a list
        :return: the card that will be dropped and it removes it from the index
        """
        index_cards = list(set(index_cards))

        if max(index_cards) >= len(self.cards):
            raise Exception('You cant drop more cards, there are too few on the hand')
        index_cards.sort(reverse=True)
        for i in index_cards:
            del self.cards[i]

    def sort(self):
        """Sorts the card in the hand. """
        self.cards.sort()

    def best_poker_hand(self, cards=[]):
        """ A method that checks the hand after the best combination of cards.
        :return: the best poker hand. """
        return PokerHand(self.cards + cards)

# -----------------------------------------------------------------#
class PokerHandRank(IntEnum):
    """A class that creates the Poker Hands and ranking them where 9 is the best."""

    straight_flush = 9
    four_of_a_kind = 8
    full_house = 7
    flush = 6
    straight = 5
    three_of_a_kind = 4
    two_pairs = 3
    one_pair = 2
    high_card = 1

    def __str__(self) -> str:
        return self.name.replace('_', ' ')

class PokerHand:
    """Class just to collect all the check_poker_hand functions. All functions are static
    All functions can take more than 5 cards as input and yet find the best poker hand
    """
    def __init__(self, cards):


        """ Checks after the best poker hand of all cards in the hand
        :return: : the best poker hand with the highest card in the poker hand and highest card in the hand.
        """
        self.hand_type = None
        self.card_value = None

        functions = [PokerHand.straight_flush, PokerHand.four_of_a_kind,
                           PokerHand.full_house, PokerHand.flush,
                           PokerHand.straight, PokerHand.three_of_a_kind,
                           PokerHand.two_pairs, PokerHand.one_pair, PokerHand.high_card]


        for hand_type, best_cards in zip(PokerHandRank, functions):
            if best_cards(cards):
                self.card_value = best_cards(cards)
                self.hand_type = hand_type
                break

    def __lt__(self, other):
        return [self.hand_type, self.card_value] < [other.hand_type, other.card_value]

    def __gt__(self, other):
        return [self.hand_type, self.card_value] > [other.hand_type, other.card_value]

    def __eq__(self, other):
        return [self.hand_type, self.card_value] == [other.hand_type, other.card_value]
    def __repr__(self):
        return f"Your best pokerhand is a {(self.hand_type.name)}!"
    def __str__(self):
        return f"Your best pokerhand is a {(self.hand_type.name)}!"


    @staticmethod
    def s_number(cards): # A method to count the numer of suit in cards
        return Counter([c.suit for c in cards])

    @staticmethod
    def v_number(cards): # A method to count the number regarding the values in cards
        return Counter([c.get_value() for c in cards])

    @staticmethod
    def straight_flush(cards):
        """
        Checks for the best straight flush in a list of cards (may be more than just 5)
        :param cards: A list of playing cards sorted by value.
        :return: None if no straight flush is found, else the value of the top card and a list of the cards in the hand
        sorted.
        """
        vals = [(c.get_value(), c.suit) for c in cards] \
               + [(1, c.suit) for c in cards if c.get_value() == 14]  # Add the aces!
        for c in reversed(cards):  # Starting point (high card)
            # Check if we have the value - k in the set of cards:
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k, c.suit) not in vals:
                    found_straight = False
                    break
            if found_straight:
                return c.get_value(), sorted(cards, reverse=True)

    @staticmethod
    def four_of_a_kind(cards):
        """
        :param cards: Playing cards in a list
        :return: Pokerhand object, the value of four cards and a list of the cards in the hand sorted.
        """
        v_number = PokerHand.v_number(cards)
        pairs = [v[0] for v in v_number.items() if v[1] >= 4]
        if pairs:
            return pairs[0], sorted(cards, reverse=True)

    @staticmethod
    def full_house(cards):
        """
        Checks for the best full house in a list of cards (may be more than just 5)
        :param cards: A list of playing cards
        :return: None if no full house is found, else a tuple of the values of the triple and pair and a list of the
        cards in the hand sorted.
        """
        value_count = Counter()
        for c in cards:
            value_count[c.get_value()] += 1
        # Find the card ranks that have at least three of a kind
        threes = [v[0] for v in value_count.items() if v[1] >= 3]
        threes.sort()
        # Find the card ranks that have at least a pair
        twos = [v[0] for v in value_count.items() if v[1] >= 2]
        twos.sort()
        # Threes are dominant in full house, lets check that value first:
        for three in reversed(threes):
            for two in reversed(twos):
                if two != three:
                    return three, two, sorted(cards, reverse=True)

    @staticmethod
    def flush(cards):
        """ Checking if a flush can be created with the given cards.
        :param cards: Playing cards in a list
        :return: Pokerhand object, value of the highest card and a list of the cards in the hand sorted.
        """
        s_number = PokerHand.s_number(cards)
        if len(set(s_number)) == 1:
            return max(sorted(s_number, reverse=True)), sorted(cards, reverse=True)

    @staticmethod
    def straight(cards):
        """ Checking if a straight can be created with the given cards.
        :param cards: Playing cards in a list
        :return: PokerHand object, value of the top card and a list of the cards in the hand sorted. """

        cards = sorted(cards, key=lambda card: card.get_value())  # Sort cards after card number
        vals = [c.get_value() for c in cards] \
                + [1 for c in cards if c.get_value() == 14]  # Add the aces with value 1 as well
        for c in reversed(cards):  # Starting point (high card)
            # Check if we have the value - k in the set of cards:
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k) not in vals:
                    found_straight = False
                    break
            if found_straight:
                highest = max(cards)
                return highest.get_value(), sorted(cards, reverse=True)

    @staticmethod
    def three_of_a_kind(cards):
        """ Checking if a three of a kind can be created with the given cards.
        :cards: Playing cards in a list
        :return: Pokerhand object, value of three cards and a list of the cards in the hand sorted.
        """
        v_number = PokerHand.v_number(cards)
        threes = [v[0] for v in v_number.items() if v[1] >= 3]
        threes.sort()
        if threes:
            return threes[0], sorted(cards, reverse=True)

    @staticmethod
    def two_pairs(cards):
        """ Checking if two pairs can be created with the given cards.
        :param cards: Playing cards in a list
        :return: Pokerhand object, the value of the best pair and a list of the cards in the hand sorted.
        """
        v_number = PokerHand.v_number(cards)
        pair = [v[0] for v in v_number.items() if v[1] >= 2]
        pair.sort()
        if len(pair) > 1:
            return pair[1], sorted(cards, reverse=True)

    @staticmethod
    def one_pair(cards):
        """ Checking if one pair can be created with the given cards.
        :param cards: Playing cards in a list
        :return: Pokerhand object, the value of two cards in the pair and a list of the cards in the hand sorted.
        """

        counts = dict()
        values = [x.get_value() for x in cards]
        for v in values:
            counts[values.count(v)] = v
        if 2 in counts.keys():
            return counts[2], sorted(cards, reverse=True)


    @staticmethod
    def high_card(cards):
        """
        :param cards: Playing cards from a list
        :return: A list of all the cards in the hand sorted from the highest card.
        """
        return sorted(cards, reverse=True)