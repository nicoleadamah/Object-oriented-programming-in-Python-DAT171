from enum import Enum
import pytest
from cardlib import *

# Test given in the assignment
# This test assumes you call your suit class "Suit" and the suits "Hearts and "Spades"
def test_cards():
    h5 = NumberedCard(4, Suit.Hearts)
    assert isinstance(h5.suit, Enum)

    sk = KingCard(Suit.Spades)
    assert sk.get_value() == 13

    assert h5 < sk
    assert h5 == h5

    with pytest.raises(TypeError):
        pc = PlayingCard(Suit.Clubs)


# This test assumes you call your shuffle method "shuffle" and the method to draw a card "draw"
def test_deck():
    d = StandardDeck()
    c1 = d.draw()
    c2 = d.draw()
    assert not c1 == c2

    d2 = StandardDeck()
    d2.shuffle()
    c3 = d2.draw()
    c4 = d2.draw()
    assert not ((c3, c4) == (c1, c2))

# This test builds on the assumptions above and assumes you store the cards in the hand in the list "cards",
# and that your sorting method is called "sort" and sorts in increasing order
def test_hand():
    h = Hand()
    assert len(h.cards) == 0
    d = StandardDeck()
    d.shuffle()
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    assert len(h.cards) == 5

    h.sort()
    for i in range(4):
        assert h.cards[i] < h.cards[i + 1] or h.cards[i] == h.cards[i + 1]

    cards = h.cards.copy()
    h.drop_cards([3, 0, 1])
    assert len(h.cards) == 2
    assert h.cards[0] == cards[2]
    assert h.cards[1] == cards[4]


# This test builds on the assumptions above. Add your type and data for the commented out tests
# and uncomment them!
def test_pokerhands():
    h1 = Hand()
    h1.add_card(QueenCard(Suit.Diamonds))
    h1.add_card(KingCard(Suit.Hearts))

    h2 = Hand()
    h2.add_card(QueenCard(Suit.Hearts))
    h2.add_card(AceCard(Suit.Hearts))

    cl = [NumberedCard(10, Suit.Diamonds), NumberedCard(9, Suit.Diamonds),
          NumberedCard(8, Suit.Clubs), NumberedCard(6, Suit.Spades)]

    ph1 = h1.best_poker_hand(cl)
    assert isinstance(ph1, PokerHand)
    ph2 = h2.best_poker_hand(cl)
    # assert # Check ph1 handtype class and data here>
    # assert # Check ph2 handtype class and data here>

    assert ph1 < ph2

    cl.pop(0)
    cl.append(QueenCard(Suit.Spades))
    ph3 = h1.best_poker_hand(cl)
    ph4 = h2.best_poker_hand(cl)


    assert ph3 < ph4
    assert ph1 < ph2

    # assert # Check ph3 handtype class and data here>
    # assert # Check ph4 handtype class and data here>

    cl = [QueenCard(Suit.Clubs), QueenCard(Suit.Spades), KingCard(Suit.Clubs), KingCard(Suit.Spades)]
    ph5 = h1.best_poker_hand(cl)

    # assert # Check ph5 handtype class and data here>

# -----------------------------------------------------------------#
# This part of the testing has been created by us and contains different test with inspiration from the instructions
# from the assignment:

# a. More card types and their methods
# b. More hand methods
# c. Further testing the deck and its methods
# d. Card combinations giving the different poker hands
# e. Comparison between different poker-hands
# f. Comparison between hands with card combinations giving the same poker hand, but different card values


# Test more card types to assure that it's printing correctly and that the ranking is correct(covers task a)
def test_card_more():
    c1 = AceCard(Suit.Hearts)
    c2 = NumberedCard(8, Suit.Diamonds)

    assert c1.suit.name == 'Hearts'
    assert c1.suit.value == 1
    assert c1.get_value() == 14
    assert isinstance(c1, AceCard)

    assert c2.get_suit().name == 'Diamonds'
    assert c2.get_suit().value == 4
    assert c2.get_value() == 8
    assert isinstance(c2, NumberedCard)

    assert c1 > c2
    assert str(c2) == '8 of Diamonds'

# Testing so when assigning two cards the same value but different suit that it ranks the cards not equal(covers task a)
    c3 = NumberedCard(8, Suit.Hearts)
    assert c2 != c3

#This test assumes you use the add_card method from Hand class and the draw method from StandardDeck class
#(covers task b & c)
def test_hand_and_deck_more():
    h = Hand()
    assert len(h.cards) == 0
    d = StandardDeck()
    d.shuffle()
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())

    assert len(h.cards) == 10

#This test assumes you use the add_card method from Hand class and test the len functions for the deck(covers task b)
def test_hand_more1():
    h1 = Hand()
    h2 = Hand()
    d = StandardDeck()
    h1.add_card(NumberedCard(1,Suit.Spades))
    h1.add_card(NumberedCard(1,Suit.Spades))
    h2.add_card(NumberedCard(2,Suit.Hearts))
    h2.add_card(NumberedCard(2,Suit.Hearts))

    assert len(d) == 52 - len(h1.cards) + len(h2.cards)

# This test the amount of cards in the deck after one has been drawn(covers task c)
def test_deck_more2():
    d = StandardDeck()
    d.draw()

# This test two pokerhands with high card as best poker hand(covers task d)

def test_pokerhand_more():
    h1 = Hand()
    h2 = Hand()
    table = Hand()

    h1.add_card(NumberedCard(6, Suit.Diamonds))
    h1.add_card(NumberedCard(2, Suit.Spades))
    h2.add_card(NumberedCard(3, Suit.Spades))
    h2.add_card(NumberedCard(2, Suit.Diamonds))

    table.add_card(NumberedCard(7, Suit.Hearts))
    table.add_card(JackCard(Suit.Hearts))
    table.add_card(KingCard(Suit.Diamonds))
    table.add_card(NumberedCard(4, Suit.Hearts))
    table.add_card(NumberedCard(9, Suit.Spades))

# This test the pokerhand with the best hand flush(covers task d)
def test_pokerhand_more2():
    p1 = Hand()
    p1.add_card(JackCard(Suit.Hearts))
    p1.add_card(QueenCard(Suit.Hearts))
    table = [NumberedCard(5, Suit.Hearts), AceCard(Suit.Hearts), NumberedCard(3, Suit.Hearts)]
    d = p1.best_poker_hand(table)


# This rest creates two different poker hands compare them, a straight and Three of a kind is expected
# (covers task e)

def test_poker_hand_compare1():

    table = [NumberedCard(5, Suit.Hearts), NumberedCard(5, Suit.Hearts),AceCard(Suit.Spades),
             KingCard(Suit.Clubs), QueenCard(Suit.Diamonds)]
    h1 = Hand()
    h2 = Hand()

    h1.add_card(NumberedCard(10, Suit.Diamonds))
    h1.add_card(JackCard(Suit.Hearts))
    h2.add_card(NumberedCard(5, Suit.Clubs))
    h2.add_card(NumberedCard(4, Suit.Diamonds))

    pokerhand1 = h1.best_poker_hand(table)   # This should return poker hand 'Straight'
    pokerhand2 = h2.best_poker_hand(table)   # This Should return poker hand 'Three of a kind'

    assert pokerhand2 < pokerhand1 # testing for comparison


# This tests the hand straight flush and compares with same hand straight flush
def test_poker_hand_compare3():
    p1 = Hand()
    p1.add_card(NumberedCard(2, Suit.Spades))
    p1.add_card(NumberedCard(5, Suit.Spades))

    p2 = Hand()
    p2.add_card(NumberedCard(5, Suit.Spades))
    p2.add_card(NumberedCard(2, Suit.Spades))

    table = [NumberedCard(3, Suit.Spades), QueenCard(Suit.Spades), NumberedCard(3, Suit.Spades), AceCard(Suit.Spades)]

    b = p1.best_poker_hand(table)
    c = p1.best_poker_hand(table)

    assert b == c  # Exactly the same poker hand

# This test two different poker hands and ranks them
def test_poker_hand_compare4():

    table = [NumberedCard(3, Suit.Spades), QueenCard(Suit.Spades), NumberedCard(3, Suit.Spades), AceCard(Suit.Spades)]


    p3 = Hand()
    p3.add_card(JackCard(Suit.Hearts))
    p3.add_card(QueenCard(Suit.Hearts))

    p4 = Hand()
    p4.add_card(NumberedCard(4, Suit.Hearts))
    p4.add_card(NumberedCard(3, Suit.Hearts))

    d = p3.best_poker_hand(table)
    e = p4.best_poker_hand(table)

    assert d < e  # Ranks a three of a kind higher than two pairs


# This test the highest card in two poker hands

def test_poker_hand_compare5():
    p1 = Hand()
    p2 = Hand()

    p1.add_card(NumberedCard(2, Suit.Spades))
    p1.add_card(AceCard(Suit.Hearts))
    p2 = Hand()
    p2.add_card(NumberedCard(7, Suit.Diamonds))
    p2.add_card(QueenCard(Suit.Hearts))

    table = [KingCard(Suit.Hearts), NumberedCard(2, Suit.Diamonds), NumberedCard(8, Suit.Diamonds),
             NumberedCard(4, Suit.Diamonds), NumberedCard(7, Suit.Clubs)]

    c = p2.best_poker_hand(table)
    b = p1.best_poker_hand(table)

    # This operation checks if player 2 has a lower high card than player 1
    assert b < c

# This test two equal Poker hands with one pair but different card values(task f)
def test_poker_hand_compare6():
    p1 = Hand()
    p2 = Hand()
    p1.add_card(NumberedCard(6,Suit.Spades))
    p1.add_card(NumberedCard(6,Suit.Hearts))
    p2.add_card(NumberedCard(2,Suit.Diamonds))
    p2.add_card(KingCard(Suit.Spades))

    table = [NumberedCard(5, Suit.Clubs), KingCard(Suit.Hearts), NumberedCard(4, Suit.Spades),
             QueenCard(Suit.Spades), AceCard(Suit.Spades)]

    b = p1.best_poker_hand(table)
    c = p2.best_poker_hand(table)
    assert c > b
# This test two hands with the exact same two pairs but the fifth card is different
def test_poker_hand_compare7():
    p1 = Hand()
    p2 = Hand()
    p1.add_card(QueenCard(Suit.Spades))
    p1.add_card(QueenCard(Suit.Hearts))
    p1.add_card(NumberedCard(6,Suit.Spades))
    p1.add_card(NumberedCard(6,Suit.Hearts))
    p1.add_card(KingCard(Suit.Hearts))

    p2.add_card(QueenCard(Suit.Clubs))
    p2.add_card(QueenCard(Suit.Diamonds))
    p2.add_card(NumberedCard(6,Suit.Clubs))
    p2.add_card(NumberedCard(6,Suit.Diamonds))
    p2.add_card(NumberedCard(7,Suit.Diamonds))

    a = p1.best_poker_hand()
    b = p2.best_poker_hand()
    assert a > b
# This compares two exact same pokerhands with two pairs and the same fifth cards
def test_poker_hand_compare8():
    p1 = Hand()
    p2 = Hand()
    p1.add_card(QueenCard(Suit.Spades))
    p1.add_card(QueenCard(Suit.Hearts))
    p1.add_card(NumberedCard(6,Suit.Spades))
    p1.add_card(NumberedCard(6,Suit.Hearts))
    p1.add_card(KingCard(Suit.Hearts))

    p2.add_card(QueenCard(Suit.Clubs))
    p2.add_card(QueenCard(Suit.Diamonds))
    p2.add_card(NumberedCard(6,Suit.Clubs))
    p2.add_card(NumberedCard(6,Suit.Diamonds))
    p2.add_card(KingCard(Suit.Diamonds))

    a = p1.best_poker_hand()
    b = p2.best_poker_hand()
    assert a == b
