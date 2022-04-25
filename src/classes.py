import time
import helper_functions
import random
from json import JSONEncoder

class Card:
    def __init__(self, suit, num):
        self.suit = suit
        self.num = num

    def __str__(self):
        return("{} of {}".format(self.num, self.suit))

class Hand:
    def __init__(self):
        self.cards = []
        self.numAce = 0
        self.score = 0

    def clearHand(self, deck):
        for x in self.cards:
            deck.discard_pile.append(x)
        self.cards = []

    def receiveCard(self, Card):
        self.cards.append(Card)
        self.addCards()

    def addCards(self):
        self.numAce = 0
        self.score = 0
        for c in self.cards:
            if (str(c.num).isnumeric()):
                self.score = self.score + c.num
            else:
                if (c.num == 'Ace'):
                    self.numAce = self.numAce + 1
                else:
                    self.score = self.score + 10
        for i in range(0,self.numAce):
            if (self.score+11<=21):
                self.score = self.score + 11
            else:
                self.score = self.score + 1
        return self.score

    def __str__(self):
        return ", ".join(str(c) for c in self.cards)

class Dealer:
    def __init__(self):
        self.hand = Hand()

    def firstReveal(self):
        print("Dealer has a " + str(self.hand.cards[0]) + " and one covered card.")

class Player():
    def __init__(self, name, money):
        self.money = money
        self.bet_amount = 0
        self.name = name
        self.hand = Hand()

    def bet(self, minimum_bet: int):
        self.bet_amount = helper_functions.input_int_with_limits(("{} enter your bet: ").format(self.name), minimum_bet-1, self.money+1)

    def calcBet(self, won, nat_blackjack_payout=False):
        if (nat_blackjack_payout):
            self.money = self.money + (1.5 * self.bet_amount)
        elif(won):
            self.money = self.money + self.bet_amount
        else:
            self.money = self.money - self.bet_amount

    def __str__(self):
        return("{}, money: ${}".format(self.name, self.money))

class PlayerEncoder(JSONEncoder):
    def default(self, obj):
        return {
            "name" : obj.name,
            "money" : obj.money
        }  

class Deck:
    def __init__(self, numDecks):
        self.deck = self.buildDeck(numDecks)
        self.discard_pile = []
        self.numCards = 52 * numDecks

    def buildDeck(self, numDecks):
        deck = []
        for i in range(0, int(numDecks)):
            for x in ["Spades","Clubs","Diamonds","Hearts"]:
                for y in range(2,11):
                    deck.append(Card(x,y))
                for y in ["Jack","Queen","King","Ace"]:
                    deck.append(Card(x,y))
        return deck

    def shuffle(self):
        print("Shuffling deck...")
        time.sleep(0.5)
        self.deck = self.deck + self.discard_pile
        self.numCards = self.numCards + len(self.discard_pile)
        self.discard_pile = []
        for i in range(0,3):
            random.shuffle(self.deck)

    def drawTopCard(self):
        if (len(self.deck)==0):
            self.shuffle()
        #return a card and it should go to a hand
        return(self.deck.pop(0))

    def discard_card(self, card):
        self.discard_pile.append(card)

    def __str__(self):
        return(", ".join(str(c) for c in self.deck))

class Game:
    #players is a list of all players
    #deck is a deck object
    #dealer is the dealer for the game
    def __init__(self, deck, min_bet):
        self.deck = deck
        self.minimum_bet = min_bet

    def round_of_betting(self, players):
        min_bet = self.minimum_bet
        for player in players:
            print()
            print(player)
            player.bet(min_bet)

    def player_action(self,player):
        print("\n" + player.name + " has " + str(player.hand) + ".",end="\n")
        if player.hand.score == 21:
            print("\nYou already have blackjack!")
            time.sleep(2.5)
            return
        arg = input("Hit or stand?: ").lower().strip()
        if (arg == 'hit'):
            card = self.deck.drawTopCard()
            player.hand.receiveCard(card)
            print("You drew a " + str(card), end=".\n")
            if (player.hand.score < 21):
                self.player_action(player)
            elif (player.hand.score == 21):
                print("Blackjack!")
                return
            else:
                print("Sorry, bust.")
                return
        elif (arg == 'stand'):
            print("Standing, okay")
            return
        else:
            print("Actions are: \"hit\" or \"stand\"")
            self.player_action(player)

    def dealer_action(self, dealer):
        while(dealer.hand.score < 17):
            card = self.deck.drawTopCard()
            dealer.hand.receiveCard(card)
            time.sleep(0.5)
            print("Hitting...\nDealer drew: " + str(card))
        if (dealer.hand.score>21):
            print("Busted.. ")
        else:
            print("Standing.. ")

    def whoWon(self, player, dealer):
        print("\nDealer has " + str(dealer.hand.score), end=".\n")
        for p in player:
            print(p.name + " has " + str(p.hand.score), end=", so ")
            if (p.hand.score == 21 and len(p.hand.cards)==2 and dealer.hand.score != 21):
                print("natural blackjack! 3:2 payout. they won ${} rounded up".format(int(1.5*p.bet_amount)))
                p.calcBet(True, True)
            elif((p.hand.score > dealer.hand.score and p.hand.score <= 21) or (dealer.hand.score > 21 and p.hand.score <=21)):
                print("they won $" + str(p.bet_amount))
                p.calcBet(True)
            elif(p.hand.score <= 21 and p.hand.score == dealer.hand.score):
                print("they pushed.")
            else:
                print("they lost $" + str(p.bet_amount))
                p.calcBet(False)

    def clearHands(self, deck, player, dealer):
        for p in player:
            p.hand.clearHand(deck)
        dealer.hand.clearHand(deck)

    def printPlayers(self):
        for p in self.players:
            p.showPlayer()
