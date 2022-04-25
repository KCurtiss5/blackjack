import configparser
import os

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
    os.system('cls' if os.name == 'nt' else 'clear')

def change_dir():
    if(os.name == 'nt' and os.getcwd().endswith("\\blackjack")):#running from top-level directory
        os.chdir("src")

def print_banner():
    clear_terminal()
    change_dir()
    [print(line, end = "") for line in open(".banner.txt", "r").readlines()]

def read_config(config_filename: str) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(os.path.join('.', config_filename))
        return config