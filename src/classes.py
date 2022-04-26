import helper_functions
from random import shuffle
from time import sleep
from json import JSONEncoder

class Card:
    def __init__(self, suit, num):
        self.suit = suit
        self.num = num

    def __str__(self):
        return(f"{self.num} of {self.suit}")

class Hand:
    def __init__(self, bet):
        self.cards = []
        self.bet = bet
        self.score = 0
        self.finished = False

    def clearHand(self, deck):
        self.__init__(0)
        return

    def splitCards(self, deck):
        card = self.cards.pop()
        self.cards.append(deck.drawTopCard())
        self.score = self.scoreHand()
        return card
    
    def receiveCard(self, deck, card=None):
        if not card:
            self.cards.append(deck.drawTopCard())
        else:
            self.cards.append(card)
        self.score = self.scoreHand()
        return

    def scoreHand(self):
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
    
    def setFinished(self):
        self.finished=True
        return

    def __str__(self):
        return ", ".join(str(c) for c in self.cards)

class Dealer:
    def __init__(self):
        self.hand = Hand(0)

    def firstReveal(self):
        print("Dealer has a " + str(self.hand.cards[0]) + " and one covered card.")

class Player():
    def __init__(self, name, money):
        self.money = money
        self.name = name
        self.hand = [Hand(0)]

    def bet(self, minimum_bet: int):
        self.hand[0].bet = helper_functions.input_int_with_limits((f"Enter your bet: "), minimum_bet-1, self.money+1)

    def __str__(self):
        return(f"{self.name}, you have ${self.money}.")

class PlayerEncoder(JSONEncoder):
    def default(self, obj):
        return {
            "name" : obj.name,
            "money" : obj.money
        }  

class Deck:
    def __init__(self, numDecks, number_of_shuffles):
        self.numDecks = numDecks
        self.number_of_shuffles = number_of_shuffles
        self.deck = self.buildDeck(numDecks)

    def buildDeck(self, numDecks):
        deck = []
        for i in range(0, int(numDecks)):
            for x in ["Spades","Clubs","Diamonds","Hearts"]:
                for y in range(2,11):
                    deck.append(Card(x,y))
                for y in ["Jack","Queen","King","Ace"]:
                    deck.append(Card(x,y))
        for i in range(0,self.number_of_shuffles):
            shuffle(deck)
        return deck

    def shuffle(self):
        print("Shuffling deck...")
        self.__init__(self.numDecks,self.number_of_shuffles)
        return

    def drawTopCard(self):
        if (len(self.deck)==0):
            self.shuffle()
        return(self.deck.pop(0))
    
    def __len__(self) -> int:
        return len(self.deck)

    def __str__(self):
        return(", ".join(str(c) for c in self.deck))

class Game:
    def __init__(self, num_decks, min_bet, num_of_shuffles):
        self.deck = Deck(num_decks, num_of_shuffles)
        self.deck.shuffle()
        self.minimum_bet = min_bet
        self.sleep_time = int(helper_functions.read_config("config.ini")["GAME_CONFIGS"]["sleep_time"])

    def round_of_betting(self, players):
        min_bet = self.minimum_bet
        for player in players:
            print(f"\n{player}")
            player.bet(min_bet)

    def player_action(self, player, deck):
        index = 0
        while index != len(player.hand):
            if(player.hand[index].finished):
                index+=1
                continue
            if player.hand[index].score == 21 and len(player.hand[index].cards)==2:
                print(f"\n{player.name} has {str(player.hand[index])}.\nNatural Blackjack!")
                player.hand[index].setFinished()
                continue
            print("\n" + player.name + " has " + str(player.hand[index]) + ".",end="\n")
            arg = input(f"What do you want to do, {player.name}?: ").lower().strip()
            if (arg == "split"):
                if(len(player.hand[index].cards)== 2 and player.hand[index].cards[0].num == player.hand[index].cards[1].num 
                and len(player.hand)<3 and player.money-2*player.hand[index].bet>0):
                    print("Successfully split:\n")
                    newHand = Hand(player.hand[index].bet)
                    transfer_card = player.hand[index].splitCards(deck)
                    newHand.receiveCard(deck, transfer_card)
                    print(f"You drew a {str(player.hand[index].cards[-1])} for your first hand.")
                    newHand.receiveCard(deck)
                    print(f"You drew a {str(newHand.cards[-1])} for your second hand.")
                    player.hand.append(newHand)
                    continue
                else:
                    print("You can't split.")
            if (arg == 'hit' or arg == "double"):
                if (arg == "double"):
                    print(f"{player.name} must bet ${player.hand[index].bet} more.")
                    player.hand[index].bet*=2
                player.hand[index].receiveCard(deck)
                print(f"You drew a {str(player.hand[index].cards[-1])}.")
                if (arg == "hit" and player.hand[index].score < 21):
                    continue
                if (player.hand[index].score > 21):
                    print("Oops, you busted.")
                if (player.hand[index].score == 21):
                    print("Blackjack!\n")
                player.hand[index].setFinished()
            elif (arg == 'stand'):
                print("Standing.")
                player.hand[index].setFinished()
            else:
                print("Actions are: \"hit\" or \"stand\" or \"double\" or \"split\"")
        return

    def dealer_action(self, dealer):
        while(dealer.hand.score < 17):
            dealer.hand.receiveCard(self.deck)
            print(f"Hitting... Dealer drew: {str(dealer.hand.cards[-1])}")
            sleep(self.sleep_time)
        if (dealer.hand.score > 21):
            print("Dealer busted.")
        return dealer.hand.score

    def whoWon(self, players, dealer_score):
        print(f"\nDealer has {dealer_score}.")
        for player in players:
            sleep(self.sleep_time)
            for hand in player.hand:
                if (hand.score > 21 or hand.score < dealer_score and dealer_score <= 21):
                    print(f"With {hand.score}, {player.name} {'busted and ' if hand.score > 21 else ''}lost ${hand.bet}.")
                    player.money-=hand.bet
                elif (hand.score == dealer_score):
                    print(f"With {hand.score}, {player.name} pushed and breaks even.")
                else:
                    if (hand.score == 21 and len(hand.cards)==2):
                        print(f"{player.name} has a natural blackjack! They win ${int(1.5*hand.bet)}!")
                        player.money+=int(1.5*hand.bet)
                    else:
                        print(f"With {hand.score}, {player.name} wins ${hand.bet}.")
                        player.money+=hand.bet

    def clearHands(self, deck, player, dealer):
        for p in player:
            for hand in p.hand:
                hand.clearHand(deck)
        dealer.hand.clearHand(deck)

    def printPlayers(self):
        for p in self.players:
            p.showPlayer()
