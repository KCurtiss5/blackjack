import sys, os
import configparser
import blackjack
import input_validation

class Menu:
    def __init__(self):
        self.display_option_menu()

    def read_config(self, config_filename: str) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(os.path.join('.', config_filename))
        return config

    def display_option_menu(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(''' ___  _     ___   ___  _  __    _  ___   ___  _  __
| _ )| |   /   \ / __|| |/ / _ | |/   \ / __|| |/ /
| _ \| |__ | - || (__ |   < | || || - || (__ |   <
|___/|____||_|_| \___||_|\_\ \__/ |_|_| \___||_|\_\\
        \n''')
        print("1. Play Game")
        print("2. Set Options")
        print("3. Leave Game")
        option=input_validation.input_int_with_limits("\nEnter your option: ", 0, 4)
        self.handle_menu_options(option)

    def customize_options(self) -> None:
        config_parser = self.read_config("config.ini")
        option_list=list(config_parser.items('GAME_CONFIGS'))
        print("0: Exit")
        for option in enumerate(option_list,1):
            print('{0}: {1}'.format(option[0],option[1]))
        option=input_validation.input_int_with_limits("\nEnter a setting you want to change: ", None, None)
        value=input_validation.input_int_with_limits("\nEnter a value you'd like to change it to: ", 0, 99999)
        config_parser.set('GAME_CONFIGS',str(option_list[option-1][0]), str(value))
        with open('config.ini', 'wb') as configfile:
           parser.write(configfile)

    def handle_menu_options(self, option_num: int) -> None:
        if (option_num==1): #if play game
            blackjack.blackjack_main()
        if (option_num==2):
            self.customize_options()
        if (option_num==3):
            print("Thanks for playing!")
            sys.exit(0)

def menu_main() -> None:
    my_menu = Menu()
