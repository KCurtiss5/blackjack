import random
import sys
import time
import os
import re
import menu

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
            deck.deck.append(x)
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
    def __init__(self, name):
        self.money = 100
        self.bet = 0
        self.name = name
        self.hand = Hand()

    def getName(self):
        return self.name

    def doBet(self, minimum_bet):
        self.bet = minimum_bet
        print(self.name, end=", ")
        try:
            self.bet = int(input("enter your bet: "))
            assert(self.bet >= minimum_bet and self.bet <= self.money)
        except AssertionError as e:
            print("That is not a valid bet.")
            self.doBet(minimum_bet)
        except ValueError as e:
            print("Please enter a positive integer.")
            self.doBet(minimum_bet)

    def calcBet(self, won, nat_blackjack_payout=False):
        if (nat_blackjack_payout):
            self.money = self.money + (1.5 * self.bet)
        elif(won):
            self.money = self.money + self.bet
        else:
            self.money = self.money - self.bet

    def __str__(self):
        return("Money: ${}, Current bet: ${}, Hand: {}".format(self.money, self.bet, self.hand))

class Deck:
    def __init__(self, numDecks):
        self.deck = self.buildDeck(numDecks)

    def buildDeck(self, numDecks):
        deck = []
        for i in range(0, numDecks):
            for x in ["Spades","Clubs","Diamonds","Hearts"]:
                for y in range(2,11):
                    deck.append(Card(x,y))
                for y in ["Jack","Queen","King","Ace"]:
                    deck.append(Card(x,y))
        return deck

    def shuffle(self):
        for i in range(0,3):
            random.shuffle(self.deck)

    def __str__(self):
        return(", ".join(str(c) for c in self.deck))

    def drawTopCard(self):
        #return a card and it should go to a hand
        return(self.deck.pop(0))

class Game:
    #players is a list of all players
    #deck is a deck object
    #dealer is the dealer for the game
    def __init__(self, deck):
        self.players = []
        self.deck = deck
        self.dealer = Dealer()
        self.minimum_bet = 1
        self.start()

    def start(self):
        while(True):
            try:
                numOfPlayers = int(input("How many players?: "))
                self.minimum_bet = int(input("What is the minimum bet?: "))
                assert(numOfPlayers >= 1 and self.minimum_bet >= 1)
                break
            except ValueError as e:
                print("Please enter a positive integer.")
            except AssertionError as e:
                print("Please enter a positive integer.")
        for i in range(0,int(numOfPlayers)):
            while(True):
                try:
                    self.addPlayer(i)
                    break
                except Exception as e:
                    print(e)
                except AssertionError as e:
                    print("Please enter a name with only letters, please.")
        print()
        self.doARound()

    def doARound(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        #Display how much money everyone has
        for p in self.players:
            print(p.name + " has $" + str(p.money))
        #shuffle decks
        print("\nShuffling...\n")
        time.sleep(1.5)
        self.deck.shuffle()
        #make players bet
        print("Everyone, make a bet.\n")
        #deal cards to players
        self.tableBetting()
        for i in range(0,2):
            for player in self.players:
                player.hand.receiveCard(self.deck.drawTopCard())
            #deal cards to dealer
            self.dealer.hand.receiveCard(self.deck.drawTopCard())
        print("\nDealing...\n")
        time.sleep(1)
        #reveal dealer first card
        self.dealer.firstReveal()
        #Let players hit or stand
        for p in self.players:
            self.hitOrMiss(p)
        #dealer reveals his second card
        print("\nDealers turn...\n\nDealer has " + str(self.dealer.hand))
        time.sleep(1.5)
        #dealer does his thing
        self.dealerHitOrMiss(self.dealer)
        #who won?
        self.whoWon(self.players,self.dealer)
        #clear hands
        self.clearHands(self.deck,self.players,self.dealer)
        #check if anyone has no money
        for p in reversed(self.players):
            if p.money == 0:
                print("I'm sorry " + p.getName() + ". You don't have any money. Please leave the table.")
                self.players.remove(p)
        #If there are no more players, end the game
        if len(self.players) == 0:
            self.endGame()
        while (True):
            playAgain = input("\nWant to play again? (y/n): ").lower().strip()
            if(playAgain == 'y' or playAgain == 'n' or playAgain == "yes" or playAgain == "no"):
                break
        if(playAgain == 'y' or playAgain == "yes"):
            self.doARound()
        else:
            self.endGame()

    def addPlayer(self, num):
        regex = re.compile("^[A-Za-z]+( {1}[A-Za-z]+)*$")
        name = input("What is player "+str(num+1)+"'s name?: ").strip().title()
        assert(regex.search(name))
        new_player = Player(name)
        for p in self.players:
            if(p.name == name):
                raise Exception("Sorry, no duplicate names.")
        self.players.append(new_player)

    def tableBetting(self):
        for p in self.players:
            p.doBet(self.minimum_bet)

    def hitOrMiss(self,player):
        print("\n" + player.getName() + " has " + str(player.hand) + ".",end="\n")
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
                self.hitOrMiss(player)
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
            self.hitOrMiss(player)

    def dealerHitOrMiss(self, dealer):
        while(self.dealer.hand.score < 17):
            card = self.deck.drawTopCard()
            self.dealer.hand.receiveCard(card)
            time.sleep(0.5)
            print("Hitting...\nDealer drew: " + str(card))
        print("Standing.. ")

    def whoWon(self, player, dealer):
        print("\nDealer has " + str(dealer.hand.score), end=".\n")
        for p in player:
            print(p.getName() + " has " + str(p.hand.score), end=", so ")
            if (p.hand.score == 21 and len(p.hand.cards)==2 and dealer.hand.score != 21):
                print("natural blackjack! 3:2 payout. they won ${}".format(1.5*p.bet))
                p.calcBet(True, True)
            elif((p.hand.score > dealer.hand.score and p.hand.score <= 21) or (dealer.hand.score > 21 and p.hand.score <=21)):
                print("they won $" + str(p.bet))
                p.calcBet(True)
            elif(p.hand.score <= 21 and p.hand.score == dealer.hand.score):
                print("they pushed.")
            else:
                print("they lost $" + str(p.bet))
                p.calcBet(False)

    def clearHands(self, deck, player, dealer):
        for p in player:
            p.hand.clearHand(deck)
        dealer.hand.clearHand(deck)

    def printPlayers(self):
        for p in self.players:
            p.showPlayer()

    def endGame(self):
        print("Goodbye!")
        quit()

def blackjack_main() -> None:
    deck = Deck(3)
    game = Game(deck)

if __name__ == '__main__':
    menu.menu_main()
