#!/usr/bin/env python

import argparse
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


def inspect_guess(guess:str, secret_word:str, misses:List[str]=None, hits:List[str]=None) -> Tuple[List[Tuple[str,str]], List[str], List[str]]:
    """Inspect the parts of a guess that are correct.

    Args:
        guess (str):        the word the user has guessed
        secret_word (str):  the word you're trying to guess
        misses (List[str]): a list of characters the user guessed but were incorrect
        hits (List[str]): a list of characters the user guessed that were correct

    Returns:
        Tuple[List[Tuple[str,str]], List[str]]: 
            0: tuples of each char in guess and unicode result
            1: list of characters that are not in secret word that user guessed
            2: list of characters that are in the secret word that the user guessed

    """
    # first split the guess and secret word into list of characters
    guess_split = [char for char in guess]
    secret_word_split = [char for char in secret_word]

    # we'll bundle correct positions here
    positions = []

    # characters the user guessed but are not in the word
    if not misses: 
        misses = []

    # characters the user guessed that are in the word
    if not hits:
        hits = []

    # identify correct positions
    for i, val in enumerate(zip(guess_split, secret_word_split)):

        if val[0] == val[1]:
            # right char, right position -> green square
            positions.append((val[0], "\U0001F7E9"))
            hits.append(val[0])

        elif val[0] in secret_word_split:
            # right char, wrong position -> yellow square
            positions.append((val[0], "\U0001F7E8"))
            hits.append(val[0])

        else:
            # incorrect char -> black square
            positions.append((val[0], "\U00002B1B"))
            misses.append(val[0])

    # print result to terminal
    for pos in positions:
        print(f"{pos[0]} {pos[1]}")

    return positions, sorted(set(misses)) , sorted(set(hits))


def print_colored_letters( letter:str, misses:List[str], hits:List[str]) -> None:
    """print the letter with a color to match if it's a hit or miss"""

    if letter in misses:
        # print the misses in red
        print("  \033[91m {}\033[00m" .format(letter),end ="")
    
    elif letter in hits:
        # print the hits in yellow
        print("  \033[93m {}\033[00m" .format(letter),end ="")

    # letter hasn't been gussed so well use the defult color
    else: print("   " + letter,end ="")


def play_wordle(filepath:str, char_min:int=4, char_max:int=None, max_guesses:int=6, debug:bool=False):
    """Play a game of wordle.

    Play a game of wordle. We'll build a list of words.
    Then we'll select a word at secret. The user will make a guess
    until they either hit the max number of guesses or
    they guess the correct word. With each iteration,
    we'll let them know how how they're doing.

    Args:
        filepath (str):     path to TXT file with list of words
        char_min (int):     words must be at least this many chars long [default: 4]
        char_max (int):     words cannot longer than this many chars [default: None]
        max_guesses (int):  how many guesses the user gets [default: 6]
        debug (bool):       use functions in debug mode

    """

    # get word list
    word_list = build_word_list(filepath, char_min, char_max, debug)

    # get secret word
    secret_word = get_secret_word(word_list, debug)
    print(f"\nWelcome to PyWordle!") 
    print(f"\nYour secret word is {len(secret_word)} characters long.")
    print(f"You have {max_guesses} guesses.\n")

    # guess counter
    n_guess = 0

    # positions to print at the end
    position_emojis = []

    # get guess and check
    while n_guess < max_guesses:

        # request that the user guesses
        guess = request_guess(secret_word)

        # check if the guess is right or wrong
        check = check_guess(guess, secret_word)

        # the user hasn't guessed yet so no misses or hits
        if n_guess == 0: misses = hits = None
        
        # inspect guess and see which positions are correct
        positions, misses, hits = inspect_guess(guess, secret_word, misses, hits)

        # add emoji results to list
        position_emojis.append([p[1] for p in positions])

        # if the guess is correct then break else iterate
        if check:
            print("\n\U0001F389 You win! \U0001F389")
            break
        else:
            n_guess += 1

            # creating all the leeter in the same order as they appear on the keyboard seprated by rows
            key_board_letters = [['Q','W','E','R','T','Y','U','I','O','P'],['A','S','D','F','G','H','J','K','L'],['Z','X','C','V','B','N','M']]
            for row_num in range(0,3):

                # printing spaces in order to match the way the keyboard rows are skewed 
                print(" " * row_num, end="")
                for letter in key_board_letters[row_num]:
                    print_colored_letters(letter, misses, hits) 
                print("\n\n", end ="")
            print(f"{max_guesses-n_guess} guesses left!\n")

    # loss state
    if not check:
        print(f"Great try! Your word was {secret_word}.")

    # print final emoji result
    for row in position_emojis:
        print(''.join(row))


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="PyWordle")
    parser.add_argument("--filepath", type=str, dest="filepath", default="google-10000-english/google-10000-english-no-swears.txt", help="List of words to use.")
    parser.add_argument("--char_min", type=int, dest="char_min", default=5, help="Secret word must be at least this many characters.")
    parser.add_argument("--char_max", type=int, dest="char_max", default=5, help="Secret word cannot exceed this many characters.")
    parser.add_argument("--max_guesses", type=int, dest="max_guesses", default=6, help="Number of guesses you get.")
    parser.add_argument("--debug", dest="debug", action="store_true", help="Debug mode, will show secret word.")
    args = parser.parse_args()

    # play wordle -- default is a standard game of 6 tries at a 5-character word
    play_wordle(filepath=args.filepath, char_min=args.char_min, char_max=args.char_max, max_guesses=args.max_guesses, debug=args.debug)
