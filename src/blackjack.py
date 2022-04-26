import helper_functions
import classes
from sys import exit
from time import sleep
from json import dumps,load
from re import compile

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
            print(f"\n{self.display_msg}\n")
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
        exit(0)

    def customize_options(self) -> None:
        option=-1
        while(option!=0):
            config_parser = helper_functions.read_config("config.ini")
            option_list=list(config_parser.items('GAME_CONFIGS'))
            print("0: Exit")
            for option in enumerate(option_list,1):
                print(f"{option[0]}: {option[1]}")
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
        if (option_num==1):
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
            print("\nCurrent players: ")
            self.__printPlayers()
            num_of_new_players=helper_functions.input_int_with_limits("\nEnter the number of players you'd like to add: ", -1, 8-len(self.players))
            self.addPlayer(num_of_new_players)
        elif (option_num==4):
            self.remove_player()
        return

    def addPlayer(self, num):
        if (num == 0):
            self.display_msg = "You did not add any players."
            return
        regex = compile("^[A-Za-z]+( {1}[A-Za-z]+)*$")
        for i in range(0,num):
            while(True):
                name = input(f"What is player {i+1}'s name?: ").strip().title()
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
        self.display_msg = f"Added {num} Players!"
        return

    def __printPlayers(self) -> None:
        for i, player in enumerate(self.players,1):
                print(f"{i}: {str(player)}")
        return 

    def remove_player(self):
        if (len(self.players)==0):
            self.display_msg = "There are no players to remove! Nobody removed."
            return
        option=-1
        orig_num_players = len(self.players)
        while((option!=0) and (len(self.players) != 0)):
            print("0: Exit")
            self.__printPlayers()
            option=helper_functions.input_int_with_limits("\nEnter a player to remove: ", -1, len(self.players)+1)
            if (option!=0):
                print(f"Removed: {str(self.players.pop(option-1))}\n")
        self.display_msg = f"Removed {str(orig_num_players-len(self.players))} players!"
        return

    def export_players(self):
        try:
            fp = open("players.json","w")
            fp.truncate(0)
        except PermissionError:
            return
        fp.write(dumps([player for player in self.players],cls=classes.PlayerEncoder))

    def make_blackjack_table(self):
        config_parser = helper_functions.read_config("config.ini")
        game_configs = config_parser["GAME_CONFIGS"]
        number_of_decks = int(game_configs["number_of_decks"])
        number_of_hands_before_shuffle = int(game_configs["number_of_hands_before_shuffle"])
        number_of_shuffles = int(game_configs["number_of_shuffles"])
        minimum_bet = int(game_configs["minimum_bet"])
        sleep_time = int(game_configs["sleep_time"])
        return Table(number_of_decks, number_of_hands_before_shuffle, minimum_bet, self.players, number_of_shuffles, sleep_time)


class Table():
    def __init__(self, num_decks, num_hands_bef_shuff, min_bet, players, num_of_shuffles, sleep_time):
        self.number_of_hands_before_shuffle = num_hands_bef_shuff
        self.game = classes.Game(num_decks, min_bet, num_of_shuffles)
        self.dealer = classes.Dealer()
        self.passed_hands = 0
        self.players = players
        self.sleep_time = sleep_time
        self.play_a_round()

    def play_a_round(self):
        helper_functions.clear_terminal()
        if (self.passed_hands == self.number_of_hands_before_shuffle):
            self.passed_hands == 0
            self.game.deck.shuffle()
        self.passed_hands = self.passed_hands + 1
        print("\nEveryone, make a bet.\n")
        self.game.round_of_betting(self.players)
        print("\nDealing...\n")
        for i in range(0,2):
            for player in self.players:
                player.hand[0].receiveCard(self.game.deck)
            self.dealer.hand.receiveCard(self.game.deck)
        sleep(self.sleep_time)
        self.dealer.firstReveal()
        for player in self.players:
            self.game.player_action(player,self.game.deck)
        print(f"\nDealers turn...\nDealer has {str(self.dealer.hand)}")
        dealer_score = self.game.dealer_action(self.dealer)
        self.game.whoWon(self.players, dealer_score)
        self.game.clearHands(self.game.deck,self.players,self.dealer)
        for p in reversed(self.players):
            if p.money == 0:
                print(f"I'm sorry {p.name}. You don't have any money. Please leave the table.")
                self.players.remove(p)
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
    except PermissionError:
        print("Cannot read players. Data will not be used if it exists.")
        sleep(3)
    raw_json = load(fp)
    for player in raw_json:
        players.append(classes.Player(player["name"],player["money"]))
    return players

if __name__ == '__main__':
    casino_main("",read_players_JSON("players.json"))
