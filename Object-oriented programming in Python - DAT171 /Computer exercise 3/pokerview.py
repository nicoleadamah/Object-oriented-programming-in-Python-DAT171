# Computer assignment 3
# A code written by Nicole Adamah & Sofia Nilsson

from pokermodel import *
from cardlib import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *

###################
# GUI-only graphical elements and no state and logic.
###################

class TableScene(QGraphicsScene):
    """ A scene with a table cloth background """
    def __init__(self):
        super().__init__()
        self.tile = QPixmap('cards/table.png')
        self.setBackgroundBrush(QBrush(self.tile))

class CardItem(QGraphicsSvgItem):
    """ This class is a overloaded QGraphicsSvgItem. It also stores the position of the card."""

    def __init__(self, renderer, position):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = position

class CardView(QGraphicsView): # from assignment
    """ A View widget that represents the table area displaying a players cards. """

    def read_cards():
        """
        Reads all the 52 cards from files.
        :return: Dictionary of SVG renderers
        """
        all_cards = dict()  # Dictionaries let us have convenient mappings between cards and their images
        for suit_file, suit in zip('HDSC', Suit):  # Check the order of the suits here!!!
            for value_file, value in zip(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
                                         range(2, 15)):
                file = value_file + suit_file
                key = (value, suit)  # I'm choosing this tuple to be the key for this dictionary
                all_cards[key] = QSvgRenderer('cards/' + file + '.svg')
        return all_cards
    # We read all the card graphics as static class variables
    back_card = QSvgRenderer('cards/Red_Back_2.svg')
    all_cards = read_cards()

    def __init__(self, card_model: CardModel, card_spacing: int = 250, padding: int = 10):
        """
        Initializes the view to display the content of the given model
        :param cards_model: A model that represents a set of cards. Needs to support the CardModel interface.
        :param card_spacing: Spacing between the visualized cards.
        :param padding: Padding of table area around the visualized cards.
        """
        self.scene = TableScene()
        super().__init__(self.scene)

        self.card_spacing = card_spacing
        self.padding = padding

        self.model = card_model
        # Whenever the this window should update, it should call the "change_cards" method.
        # This can, for example, be done by connecting it to a signal.
        # The view can listen to changes:
        card_model.new_cards.connect(self.change_cards)
        # It is completely optional if you want to do it this way, or have some overreaching Player/GameState
        # call the "change_cards" method instead. z

        # Add the cards the first time around to represent the initial state.
        self.change_cards()

    def change_cards(self):
        # Add the cards from scratch
        self.scene.clear()
        for i, card in enumerate(self.model.cards):
            # The ID of the card in the dictionary of images is a tuple with (value, suit), both integers
            graphics_key = (card.get_value(), card.suit.value)
            renderer = self.back_card if self.model.flipped(i) else self.all_cards[graphics_key]
            c = CardItem(renderer, i)

            # Shadow effects are cool!
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))  # Semi-transparent black!
            c.setGraphicsEffect(shadow)

            # Place the cards on the default positions
            c.setPos(c.position * self.card_spacing, 0)
            # We could also do cool things like marking card by making them transparent if we wanted to!
            # c.setOpacity(0.5 if self.model.marked(i) else 1.0)
            self.scene.addItem(c)

        self.update_view()

    def update_view(self):
        scale = (self.viewport().height()-2*self.padding)/313
        self.resetTransform()
        self.scale(scale, scale)
        # Put the scene bounding box
        self.setSceneRect(-self.padding//scale, -self.padding//scale,
                          self.viewport().width()//scale, self.viewport().height()//scale)

    def resizeEvent(self, painter):
        # This method is called when the window is resized.
        # If the widget is resize, we gotta adjust the card sizes.
        # QGraphicsView automatically re-paints everything when we modify the scene.
        self.update_view()
        super().resizeEvent(painter)

    def mouseDoubleClickEvent(self, event):
        self.model.flip()

class PlayerView(QGroupBox):
    """The PlayerView class shows the players' hand and the amount of money each player has"""
    def __init__(self, player, game):
        super().__init__(player.name)
        self.game = game
        self.player = player

        # Creates the players window.
        vbox_players = QVBoxLayout()
        self.setLayout(vbox_players)

        # Shows the player's cards
        hand_view = CardView(player.hand)
        #hand_view.setAlignment(Qt.AlignCenter)
        vbox_players.addWidget(hand_view)

        # Shows how much money the player has left.
        self.money = QLabel('Money:')
        vbox_players.addWidget(self.money)

        # Adjusting the alignment & updating the view
        vbox_players.setAlignment(Qt.AlignCenter)
        player.new_money.connect(self.update)
        self.update()

    def update(self):
        '''Updates the player's starting money'''
        self.money.setText("Money: " + str(self.player.money))

class ButtonView(QGraphicsView): # alla knappar
    """ Creates all the buttons and putting them into a common window."""

    def __init__(self, game):
        self.scene = TableScene()
        super().__init__(self.scene)
        self.game = game

        # Creates buttons
        self.FoldButton = QPushButton("FOLD")
        self.CallButton = QPushButton("CALL")
        self.BetButton = QPushButton("BET")
        self.Bet_money = QSpinBox()
        self.Bet_money.setMinimum(10)

        # Inserts buttons in a window
        vbox = QVBoxLayout()
        vbox.addWidget(self.CallButton)
        vbox.addWidget(self.BetButton)
        vbox.addWidget(self.FoldButton)
        vbox.addWidget(self.Bet_money)

        def betting():
            """ Placing the bet. """
            self.game.bet(self.Bet_money.value())

        # Connects the buttons to an action.
        self.FoldButton.clicked.connect(self.game.fold)
        self.CallButton.clicked.connect(self.game.call)
        self.BetButton.clicked.connect(betting)

        self.game.pot.new_pot.connect(self.update)
        self.setLayout(vbox)
        self.show()
        self.update()

class Pot_active_View(QGraphicsView):
    """ A class that creates and shows the current pot and which player who is about to make the next move."""
    def __init__(self, game):
        self.scene = TableScene()
        super().__init__(self.scene)
        self.game = game

        # Creating a vertical box for the active player
        vbox = QVBoxLayout()
        active_box = QHBoxLayout()

        # Creating a label for the active player.
        self.active_player = QLabel()
        active_box.addWidget(self.active_player)
        vbox.addLayout(active_box)
        self.game.new_active_player.connect(self.update)

        # Creating a horisontal box for the pot.
        pot_box = QHBoxLayout()
        self.pot = QLabel()
        pot_box.addWidget(self.pot)
        self.game.pot.new_pot.connect(self.update)
        vbox.addLayout(pot_box)
        self.setLayout(vbox)
        self.update()

    def update(self):
        '''Updates the pot and tells us who is the active player'''
        self.active_player.setText("It's your turn: " + str(self.game.players[self.game.active_player].name))
        self.pot.setText("Pot: " + str(self.game.pot.get_value()))

class TableView(QWidget): #table med cards
    """ A class that creates the view of the cards on the tab """
    def __init__(self, game: TexasHoldEm):
        super().__init__()
        self.game = game

        # Creating a horisontal box
        hbox = QHBoxLayout()
        card_view = CardView(self.game.table_cards)
        hbox.addWidget(card_view, stretch = 3)
        hbox.addWidget(Pot_active_View(game), stretch = 1)
        self.setLayout(hbox)

class Table_and_player_View(QGroupBox):
    """ A class that specifies more precisely how the final layout should be built. """
    def __init__(self, game: TexasHoldEm):
        super().__init__()
        self.game = game
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        vbox.addWidget(PlayerView(game.players[0], game))
        vbox.addWidget(TableView(game))
        vbox.addWidget(PlayerView(game.players[1], game))

class GameView(QWidget):
    """ The main view with all the players, table with cards, buttons, etc."""
    def __init__(self, game: TexasHoldEm):
        super().__init__()
        self.game = game

        # Creating the main view
        self.box = QHBoxLayout()
        self.setWindowTitle('Texas Holdem Poker Game')
        self.box.addWidget(Table_and_player_View(game))
        self.box.addWidget(ButtonView(game))
        self.setLayout(self.box)
        self.show()

        self.game.message.connect(self.alert_user)
        self.game.player_no_money.connect(self.alert_user)
        self.game.winner.connect(self.update)
        self.update()

    def alert_user(self, text):
        """
        :param text: A pop-up box with an message.
        """
        box = QMessageBox()
        box.setText(text)
        box.exec_()