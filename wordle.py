#!/usr/bin/bash python

import csv
import random
from typing import List, Tuple


def build_word_list(filepath:str, char_min:int=4, char_max:int=None, debug:bool=False) -> List[str]:
    """Import list with top English words and curate it.

    This method will import a txt file with the top 10,000 English words 
    (courtesy: https://github.com/first20hours/google-10000-english)
    and then perform basic QC to remove short and long words. 
    These words will then feed into our wordle game. 
    The txt file will have each word in its own row.
    Each word is converted to UPPER case.

    Args:
        filepath (str): path to TXT file with list of words
        char_min (int): words must be at least this many chars long [default: 4]
        char_max (int): words cannot longer than this many chars [default: None]
        debug (bool):   print word_list info [default: False]

    Returns:
        list(str):      list of words
    """
    # use csv.reader to go over each row and append
    initial_word_list = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            initial_word_list.append(row[0])

    # list comp to remove small words
    word_list = [w for w in initial_word_list if len(w) >= char_min]

    # if max given, remove words
    if char_max:
        word_list = [w.upper() for w in word_list if len(w) <= char_max]

    if debug:
        print(f"Removed {len(initial_word_list)-len(word_list)}/{len(initial_word_list)} words. {len(word_list)} remain.")

    return word_list


def get_secret_word(word_list:List[str], debug:bool=False) -> str:
    """Get a random word from list.

    Args:
        word_list (list):   list of words from build_word_list()
        debug (bool):       print secret word to terminal [default: False]

    Returns
        str: a word in word_list
    """
    secret_word = random.choice(word_list)

    if debug:
        print(f"Secret Word: {secret_word} ({len(secret_word)} chars).")

    return secret_word


def request_guess(secret_word:str) -> str:
    """Ask the user to make a guess.

    The user types a guess for what word they want.
    The input is converted to all uppercase 
    to match the word list.

    Args:
        input (str):    str the user inputs
        secret_word (str):  the word you're trying to guess

    Returns
        str: the user's guess
    """
    guess = input("Please make a guess: ").upper()

    if len(guess) != len(secret_word):
        print(f"Guess must be exactly {len(secret_word)} characters.")
        guess = request_guess(secret_word)

    return guess


def check_guess(guess:str, secret_word:str) -> bool:
    """Check if a guess is correct.

    Args:
        guess (str):        the word the user has guessed
        secret_word (str):  the word you're trying to guess

    Returns:
        bool: True if guess is totally correct, else False

    """
    if guess == secret_word:
        return True
    else:
        return False


def inspect_guess(guess:str, secret_word:str) -> List[Tuple[str, str]]:
    """Inspect the parts of a guess that are correct.

    Args:
        guess (str):        the word the user has guessed
        secret_word (str):  the word you're trying to guess

    Returns:
        List[Tuple[str,str]]: returns of list of tuples of each char in guess and unicode result

    """
    # first split the guess and secret word into list of characters
    guess_split = [char for char in guess]
    secret_word_split = [char for char in secret_word]

    # we'll bundle correct positions here
    positions = []

    # identify correct positions
    for i, val in enumerate(zip(guess_split, secret_word_split)):

        if val[0] == val[1]:
            # right char, right position -> green square
            positions.append((val[0], "\U0001F7E9"))

        elif val[0] in secret_word_split:
            # right char, wrong position -> yellow square
            positions.append((val[0], "\U0001F7E8"))

        else:
            # incorrect char -> black square
            positions.append((val[0], "\U00002B1B"))

    # print result to terminal
    for pos in positions:
        print(f"{pos[0]} {pos[1]}")

    return positions



def play_wordle(filepath:str=None, char_min:int=4, char_max:int=None, max_guesses:int=5, debug:bool=False):
    """Play a game of wordle.

    Play a game of wordle. We'll build a list of words.
    Then we'll select a word at secret. The user will make a guess
    until they either hit the max number of guesses or
    they guess the correct word. With each iteration,
    we'll let them know how how they're doing.

    Args:
        filepath (str):     path to TXT file with list of words [default: None]
        char_min (int):     words must be at least this many chars long [default: 4]
        char_max (int):     words cannot longer than this many chars [default: None]
        max_guesses (int):  how many guesses the user gets [default: 5]
        debug (bool):       use functions in debug mode

    """
    # get default filepath
    if not filepath:
        filepath="google-10000-english/google-10000-english-no-swears.txt"

    # get word list
    word_list = build_word_list(filepath, char_min, char_max, debug)

    # get secret word
    secret_word = get_secret_word(word_list, debug)
    print(f"Welcome to PyWordle! \nYour secret word is {len(secret_word)} characters long. \nYou have {max_guesses} guesses.\n")

    # guess counter
    n_guess = 0

    # positions to print at the end
    position_emojis = []

    # get guess and check
    while n_guess < max_guesses:

        # request that the user gueses
        guess = request_guess(secret_word)

        # check if the guess is right or wrong
        check = check_guess(guess, secret_word)

        # inspect guess and see which positions are correct
        positions = inspect_guess(guess, secret_word)

        # add emoji results to list
        position_emojis.append([p[1] for p in positions])

        # if the guess is correct then break else iterate
        if check:
            print("\n\U0001F389 You win! \U0001F389")
            break
        else:
            n_guess += 1
            print(f"{max_guesses-n_guess} guesses left!\n")

    # loss state
    if not check:
        print(f"Great try! Your word was {secret_word}.")

    # print final emoji result
    for row in position_emojis:
        print(''.join(row))


if __name__=="__main__":
    play_wordle(char_min=5, char_max=5, debug=False)