import sys
import helper_functions
import classes
import re
import time
import json

class Casino:
    def __init__(self, msg, players):
        self.players = players
        self.display_msg = msg
        self.display_option_menu()
        self.Table = self.make_blackjack_table()

    def display_option_menu(self) -> None:
        option=0
        while(option!=5):
            helper_functions.print_banner()
            print("\n" + self.display_msg + "\n")
            print("1. Play Game")
            print("2. Set Options")
            print("3. Add Player")
            print("4. Remove Player")
            print("5. Leave Game")
            option=helper_functions.input_int_with_limits("\nEnter your option: ", 0, 6)
            self.handle_menu_options(option)
            if(option==1):
                return
        self.export_players()
        print("Thanks for playing!")
        sys.exit(0)

    def customize_options(self) -> None:
        option=-1
        while(option!=0):
            config_parser = helper_functions.read_config("config.ini")
            option_list=list(config_parser.items('GAME_CONFIGS'))
            print("0: Exit")
            for option in enumerate(option_list,1):
                print('{0}: {1}'.format(option[0],option[1]))
            option=helper_functions.input_int_with_limits("\nEnter a setting you want to change: ", -1, len(option_list)+1)
            if(option==0):
                break
            value=helper_functions.input_int_with_limits("\nEnter a value you'd like to change it to: ", 0, 5000)
            config_parser.set('GAME_CONFIGS',str(option_list[option-1][0]), str(value))
            with open('config.ini', 'w') as configfile:
               config_parser.write(configfile)
            print("\nSetting changed!\n")
        return

    def handle_menu_options(self, option_num: int) -> None:
        if (option_num==1): #if play game
            if (len(self.players) == 0):
                print("There are no players, you have to add some!")
                num_of_new_players=helper_functions.input_int_with_limits("\nEnter the number of players you'd like to add: ", 0, 8)
                self.addPlayer(num_of_new_players)
            return
        elif (option_num==2):
            self.customize_options()
        elif (option_num==3):
            if((len(self.players)) >= int(helper_functions.read_config("config.ini")["GAME_CONFIGS"]["max_players"])):
                self.display_msg = "Table is full!"
                return
            num_of_new_players=helper_functions.input_int_with_limits("\nEnter the number of players you'd like to add: ", -1, 8-len(self.players))
            self.addPlayer(num_of_new_players)
        elif (option_num==4):
            self.remove_player()
        return

    def addPlayer(self, num):
        if (num == 0):
            self.display_msg = "You did not add any players."
            return
        regex = re.compile("^[A-Za-z]+( {1}[A-Za-z]+)*$")
        for i in range(0,num):
            while(True):
                name = input("What is player "+str(i+1)+"'s name?: ").strip().title()
                try:
                    assert(regex.search(name))
                    for p in self.players:
                        if(p.name == name):
                            raise Exception("Sorry, no duplicate names.")
                    break
                except AssertionError as e:
                    print("Name does not fit desired format")
                except Exception as e:
                    print(e)
            new_player = classes.Player(name, int(helper_functions.read_config("config.ini")["GAME_CONFIGS"]["starting_cash"]))
            self.players.append(new_player)
        self.display_msg = "Added " + str(num) + " Players!"
        return

    def remove_player(self):
        if (len(self.players)==0):
            self.display_msg = "There are no players to remove! Nobody removed."
            return
        option=-1
        orig_num_players = len(self.players)
        while((option!=0) and (len(self.players) != 0)):
            print("0: Exit")
            for i, player in enumerate(self.players,1):
                print('{0}: {1}'.format(i,player))
            option=helper_functions.input_int_with_limits("\nEnter a player to remove: ", -1, len(self.players)+1)
            if (option!=0):
                print("Removed: " + str(self.players.pop(option-1))+"\n")
        self.display_msg = "Removed " + str(orig_num_players-len(self.players)) + " players!"
        return

    def export_players(self):
        try:
            fp = open("players.json","w")
            fp.truncate(0)
        except PermissionError:
            return
        fp.write(json.dumps([player for player in self.players],cls=classes.PlayerEncoder))

    def make_blackjack_table(self):
        config_parser = helper_functions.read_config("config.ini")
        game_configs = config_parser["GAME_CONFIGS"]
        number_of_decks = int(game_configs["number_of_decks"])
        number_of_hands_before_shuffle = int(game_configs["number_of_hands_before_shuffle"])
        minimum_bet = int(game_configs["minimum_bet"])
        return Table(number_of_decks, number_of_hands_before_shuffle, minimum_bet, self.players)


class Table():
    def __init__(self, num_decks, num_hands_bef_shuff, min_bet, players):
        self.number_of_hands_before_shuffle = num_hands_bef_shuff
        self.deck = classes.Deck(num_decks)
        self.deck.shuffle()
        self.game = classes.Game(self.deck, min_bet)
        self.dealer = classes.Dealer()
        self.passed_hands = 0
        self.players = players
        self.play_a_round()

    def play_a_round(self):
        helper_functions.clear_terminal()
        if (self.passed_hands == self.number_of_hands_before_shuffle):
            self.passed_hands == 0
            self.deck.shuffle()
        self.passed_hands = self.passed_hands + 1
        print("\nEveryone, make a bet.\n")
        self.game.round_of_betting(self.players)
        #deal cards to the players
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
            self.game.player_action(p)
        #dealer reveals his second card
        print("\nDealers turn...\n\nDealer has " + str(self.dealer.hand))
        time.sleep(1.5)
        #dealer does his thing
        self.game.dealer_action(self.dealer)
        #who won?
        self.game.whoWon(self.players,self.dealer)
        #clear hands
        self.game.clearHands(self.deck,self.players,self.dealer)
        #check if anyone has no money
        for p in reversed(self.players):
            if p.money == 0:
                print("I'm sorry " + p.name + ". You don't have any money. Please leave the table.")
                self.players.remove(p)
        #If there are no more players, end the game
        if len(self.players) == 0:
            casino_main("There are no more players.. create some more and play again!")
        while (True):
            playAgain = input("\nWant to play again? (y/n): ").lower().strip()
            if(playAgain == 'y' or playAgain == 'n' or playAgain == "yes" or playAgain == "no"):
                break
        if(playAgain == 'y' or playAgain == "yes"):
            self.play_a_round()
        else:
            casino_main("",self.players)

def casino_main(msg="",players=[]) -> None:
    casino = Casino(msg, players)

def read_players_JSON(filename: str) -> list:
    players = []
    try:
        helper_functions.change_dir()
        fp = open("players.json","r")
    except FileNotFoundError:
        return players
    raw_json = json.load(fp)
    for player in raw_json:
        players.append(classes.Player(player["name"],player["money"]))
    return players

if __name__ == '__main__':
    casino_main("",read_players_JSON("players.json"))
