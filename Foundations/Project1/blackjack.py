#----------------------------------------------------------
# blackjack.py
#
# Created by: Courtney Wilkins
#
# Text-based simulation of blackjack card game
#----------------------------------------------------------

import random
import re

# -----------------------------------------------------------------------
# Defines a structure to emulate a playing card.
# - Input: ID number (0 to 51) representing one card of a standard Deck
# - Variables: suit, rank, value
# - Methods: __init__, assignSuit, assignRank, assignValue, getSuit,
#           getRank, getValue, printShort, __str__
# -----------------------------------------------------------------------
class Card:
    # Creates a card object from the supplied unique identifier
    def __init__(self, card_id):
        self.card_id = card_id
        self.suit = self.assignSuit()
        self.rank = self.assignRank()
        self.value = self.assignValue()

    # Assign card a suit unique identifier
    def assignSuit(self):
        # 0-12 = C, 13-25 = D, 26-38 = H, 39-51 = S
        if self.card_id < 12:
            suit = 'C'
        elif self.card_id < 25:
            suit = 'D'
        elif self.card_id < 38:
            suit = 'H'
        else:
            suit = 'S'
        return(suit)

    # Assign card a suit unique identifier
    def assignRank(self):
        # 0 = A, 2-9 = numeric, 10 = J, 11 = Q, 12 = K
        numeric_rank = self.card_id % 13
        rank_dict = {0: 'A', 10: 'J', 11: 'Q', 12: 'K'}
        if numeric_rank in rank_dict:
            rank = rank_dict[numeric_rank]
        else:
            rank = numeric_rank + 1
        return(rank)

    # Assign card a value for scoring
    def assignValue(self):
        # Number cards (2-9) = Number on card
        # Face cards (10-12: J, Q, K) = 10 points
        # Ace (0) = 11 points (can also be 1 pt)
        numeric_rank = self.card_id % 13
        if numeric_rank >= 2 and numeric_rank < 10:
            score = numeric_rank + 1
        elif numeric_rank > 9 and numeric_rank < 13:
            score = 10
        else:
            score = 11
        return(score)

    # Define method to return suit
    def getSuit(self):
        return self.suit

    # Define method to return rank
    def getRank(self):
        return self.rank

    # Define method to return value
    def getValue(self):
        return self.value

    # Define method for printing short value
    def printShort(self):
        return "{}{}".format(self.rank, self.suit)

    # Define method for complete printing
    def __str__(self):
        faces_dict = {'A': 'Ace', 'J': 'Jack', 'Q': 'Queen', 'K': 'King'}
        if self.rank in faces_dict:
            full_rank = faces_dict[self.rank]
        else:
            full_rank = self.rank
        suit_dict = {'C': 'Clubs', 'D': 'Diamonds', 'H': 'Hearts', 'S': 'Spades'}
        full_suit = suit_dict[self.suit]
        return "{} of {}".format(full_rank, full_suit)


# -----------------------------------------------------------------------
# Defines a structure to emulate a deck of playing cards.
# - Input: None
# - Variables: cards
# - Methods: __init__, shuffleDeck, deal
# -----------------------------------------------------------------------
class Deck:
    # Create a deck object
    def __init__(self):
        self.cards = list(range(52))
        self.shuffleDeck()

    # Shuffle cards, resulting in new 52-card iterator
    def shuffleDeck(self):
        new_order = list(range(52))
        shuffle_order = random.shuffle(new_order)
        self.cards = new_order

    # Deal out next card in deck
    def deal(self, n = 1):
        next_cards = []
        for i in range (n):
            next_number = self.cards.pop()
            next_card = Card(next_number)
            next_cards.append(next_card)
        return next_cards

    # Define method for complete printing
    def __str__(self):
        deck_of_cards = [str(Card(x)) for x in self.cards]
        deck_string = "\n".join(deck_of_cards)
        return "{}".format(deck_string)


# -----------------------------------------------------------------------
# Defines a structure to emulate a deck of playing cards.
# - Input: name, first_deal
# - Variables: name, score, hand, blackjack, isBust
# - Methods: __init__, getName, getHand, getScore, hasBust, assignScore,
#            addCards, hasBlackjack, hasBust, hideCard, __str__
# -----------------------------------------------------------------------
class Player:
    # Create a player object from name (Dealer, Player) and first deal
    def __init__(self, name, first_deal):
        self.name = name
        self.hand = first_deal
        self.score = self.assignScore()
        self.blackjack = False
        self.isBust = False

    # Define method to return name
    def getName(self):
        return self.name

    # Define method to return cards in hand
    def getHand(self):
        return self.hand

    # Define method to return score
    def getScore(self):
        return self.score

    # Define method to return boolean: does player have blackjack?
    def hasBlackjack(self):
        return self.blackjack

    # Define method to return boolean: has player bust (crossed 21 points)?
    def hasBust(self):
        return self.isBust

    # Define method to assign score for hand
    def assignScore(self):
        values = [card.value for card in self.hand]
        total_value = sum(values)
        return(total_value)

    # Add card to hand
    def addCards(self, cards):
        for card in cards:
            self.hand.append(card)
            self.score += card.getValue()
        if self.score > 21:
            self.bust = true

    # Define method for printing
    def hideCard(self):
        header = "Name: {}".format(self.name)
        card_info = [str(card) for card in self.hand]
        card_info[0] = "?" # 'Hide first card'
        hand_info = "\n  ".join(card_info)
        return "{}\n  {}\n".format(header, hand_info)

    # Define method for printing
    def __str__(self):
        header = "Name: {}, Score: {}".format(self.name, self.score)
        card_info = [str(card) for card in self.hand]
        hand_info = "\n  ".join(card_info)
        return "{}\n  {}".format(header, hand_info)


# -----------------------------------------------------------------------
# Defines a structure to emulate a blackjack game.
# - Input: player
# - Variables: deck, player, dealer, gameOver, winner
# - Methods: __init__, getPlayer, isOver, printStatus, takeTurn,
#            checkWin, gameOver
# -----------------------------------------------------------------------
class Game:
    # Create a game object from Player name
    def __init__(self, player_name):
        self.deck = Deck()
        self.player = Player(player_name, self.deck.deal(2))
        self.dealer = Player('Dealer', self.deck.deal(2))
        self.gameOver = False
        self.winner = None

    # Define method to return human player
    def getPlayer(self):
        return self.player

    # Define method to return game over status
    def isOver(self):
        return self.gameOver

    # Define method to print status of game (dealer with hidden card)
    def printStatus(self):
        print("Here's where we stand, {}:".format(self.player.getName()))
        print(self.player)
        print("")
        print(self.dealer.hideCard())

    # Define method to print full game status (no hidden cards)
    def printAll(self):
        print("Here's where we stand, {}:".format(self.player.getName()))
        print(self.player)
        print("")
        print(self.dealer)

    # Define method for one game turn
    def takeTurn(self):
        # Get action decision from user
        while True:
            try:
                decision = input("Would you like to hit (h) or stand (s)? ")
                detected = re.match(r'^h|s', decision.lower())
                if detected != None: break
            except ValueError:
                print("Please enter a valid input.")
                continue

        # Take action based on user decision
        action = detected[0] # 'h' or 's' based on match
        if action == 'h':
            # deal card to player. deal card to dealer if score < 17
            self.player.addCards(self.deck.deal(1))
            if self.dealer.getScore() < 17:
                self.dealer.addCards(self.deck.deal(1))
            self.checkWin() # is game over?
            if not self.gameOver:
                self.printStatus()
        else:
            # Determine winner based on score
            if self.player.getScore() > self.dealer.getScore():
                self.winner = self.player.getName()
            elif self.dealer.getScore() > self.player.getScore():
                self.winner = self.dealer.getName()
            else:
                self.winner = "It's a tie!"
            self.gameOver = True

    # Define method to determine if game has a winner
    def checkWin(self):
        player_hasBlackjack = self.player.hasBlackjack()
        dealer_hasBlackjack = self.dealer.hasBlackjack()
        player_hasBust = self.player.hasBust()
        dealer_hasBust = self.dealer.hasBust()
        if (player_hasBlackjack and not dealer_hasBlackjack) or dealer_hasBust:
            self.winner = self.player.getName()
            self.gameOver = True
        elif (dealer_hasBlackjack and not player_hasBlackjack) or player_hasBust:
            self.winner = self.dealer.getName()
            self.gameOver = True

    # Define method to end game
    def end(self):
        # Print final hands
        self.printAll()

        # Announce winner
        if self.winner == 'Dealer':
            print("Sorry, House wins!")
        else:
            print("Congratulations, {}! You win!".format(self.player.getName()))



# -----------------------------------------------------------------------
# Runs the blackjack game
# -----------------------------------------------------------------------
def main():
    # Intro and setup
    print("Welcome to the Blackjack table!\n")
    player_name = input("What's your name? ")
    print("Good luck, {}!".format(player_name))

    # Start game
    game = Game(player_name)
    game.printStatus()

    # Run game
    while not game.isOver():
        game.takeTurn()
    game.end()

main()
