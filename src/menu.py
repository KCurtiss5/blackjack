import sys, os
import configparser
import blackjack
import helper_functions

class Menu:
    def __init__(self):
        self.display_option_menu()

    def read_config(self, config_filename: str) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(os.path.join('.', config_filename))
        return config

    def display_option_menu(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        helper_functions.print_banner()
        print("1. Play Game")
        print("2. Set Options")
        print("3. Leave Game")
        option=helper_functions.input_int_with_limits("\nEnter your option: ", 0, 4)
        self.handle_menu_options(option)

    def customize_options(self) -> None:
        option=-1
        while(option!=0):
            config_parser = self.read_config("config.ini")
            option_list=list(config_parser.items('GAME_CONFIGS'))
            print("0: Exit")
            for option in enumerate(option_list,1):
                print('{0}: {1}'.format(option[0],option[1]))
            option=helper_functions.input_int_with_limits("\nEnter a setting you want to change: ", None, None)
            if(option==0):
                break
            value=helper_functions.input_int_with_limits("\nEnter a value you'd like to change it to: ", 0, 99999)
            config_parser.set('GAME_CONFIGS',str(option_list[option-1][0]), str(value))
            with open('config.ini', 'w') as configfile:
               config_parser.write(configfile)
            print("\nSetting changed!\n")
        self.display_option_menu()

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
