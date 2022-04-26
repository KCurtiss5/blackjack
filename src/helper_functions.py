from configparser import ConfigParser
from os import name, system, getcwd, chdir, path

config = None

def input_int_with_limits(message: str, lower_bound: int, upper_bound: int) -> int:
    while(True):
        try:
            option = int(input(message))
            if ((option <= lower_bound) or (option >= upper_bound)):
                print("Please enter a number between {0} and {1}.".format(lower_bound+1, upper_bound-1))
                continue
            return(option)
        except ValueError as e:
            print("Please enter a positive integer.")

def clear_terminal():
    system('cls' if name == 'nt' else 'clear')

def change_dir():
    if(name == 'nt' and getcwd().endswith("\\blackjack")):#running from top-level directory
        chdir("src")

def print_banner():
    clear_terminal()
    change_dir()
    [print(line, end = "") for line in open("assets/.banner.txt", "r").readlines()]

def read_config(config_filename: str) -> ConfigParser:
    global config
    if (not config):
        config = ConfigParser()
        config.read(path.join('.', config_filename))
    return config