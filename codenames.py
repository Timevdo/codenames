from colorama import Fore, Back, Style
import numpy as np
import pickle
import random

import algs

NUM_BLUE_WORDS = 9
NUM_RED_WORDS = 8

def generate_board():
    #bwfl = open('board_words.bin', 'rb')
    #board_words_list = pickle.load(bwfl)

    bwfl = open('wordlist-eng.txt', 'r')
    board_words_list = bwfl.readlines()
    board_words_list = [w[0:len(w)-1].lower() for w in board_words_list]

    board_words = np.array(random.sample(board_words_list, 25))
    #print(board_words)

    blue_idx = set(random.sample(range(25), NUM_BLUE_WORDS))
    red_idx = set(random.sample(set(range(25)) - blue_idx, NUM_RED_WORDS))

    blue_arr = np.full(25, False)
    red_arr = np.full(25, False)
    revealed = np.full(25, False)

    for i in blue_idx:
        blue_arr[i] = True
    for i in red_idx:
        red_arr[i] = True

    board = np.stack([board_words, blue_arr, red_arr, revealed])

    return board

def print_hidden_board(input_board):

    board = np.stack([np.reshape(l, (5,5)) for l in input_board])

    for i, row in enumerate(board[0]):
        rowstr = ""     
        for j, word in enumerate(row):
            if board[1][i][j] == "True":
                rowstr += Fore.LIGHTBLUE_EX + f"{word:<15}"
            elif board[2][i][j] == "True":
                rowstr += Fore.LIGHTRED_EX + f"{word:<15}"
            else:
                rowstr += Fore.RESET+ f"{word:<15}"
        print(rowstr)
    print(Fore.RESET)
        
def print_player_board(input_board):
    board = np.stack([np.reshape(l, (5,5)) for l in input_board])

    for i, row in enumerate(board[0]):
        rowstr = ""     
        for j, word in enumerate(row):
            if board[3][i][j] == "True":
                if board[1][i][j] == "True":
                    rowstr += Fore.LIGHTBLUE_EX + f"{word:<15}"
                elif board[2][i][j] == "True":
                    rowstr += Fore.LIGHTRED_EX + f"{word:<15}"
                else:
                    rowstr += Fore.LIGHTYELLOW_EX + f"{word:<15}"
            else:
                rowstr += Fore.RESET+ f"{word:<15}"
        print(rowstr)
    print(Fore.RESET)

def player_cluegiver(board):
    while True:
        print_hidden_board(board)

        clue = input(Fore.RESET + "Enter Clue: ")
        n = input("Enter Number: ")

        guesses = algs.ft_guess_from_clue_prob(board, clue, int(n))

        for g in guesses:
            board[3][board[0].tolist().index(g)] = True

        print("Computer Guessed", guesses)
        print_player_board(board)
        print("\n")

def player_guesser(board):
    blue_words = [w for i, w in enumerate(board[0]) if board[1][i] == "True"]
    past_clues = []

    while True:
        print_player_board(board)

        clue, n, _ = algs.ft_generate_clue_v2(board, past_clues)
        past_clues += [clue]
        #print(past_clues)

        print("Computer Says: ",clue, n)
        assert clue.lower() in algs.wordset

        guess = ""
        i = 0
        while guess != "DONE" and i <= n:
            guess = input("Guess: ")
            if guess == "DONE":
                break
            if guess == "QUIT":
                print_hidden_board(board)
                return

            board[3][board[0].tolist().index(guess)] = True
            print_player_board(board)

            if guess not in blue_words:
                break
        print('\n\n')

def single_player(board):
    past_clues = []

    while True:
        blue_words = [w for i, w in enumerate(board[0]) if board[1][i] == "True" and board[3][i] == "False"]
        print("BLUE TEAM PLAYS:")
        print_player_board(board)
        clue, n, _ = algs.ft_generate_clue_v2(board, past_clues, blue_team=True)
        past_clues += [clue]

        print("BLUE TEAM CLUE: ",clue, n)
        assert clue.lower() in algs.wordset

        guess = ""
        i = 0
        while guess != "DONE" and i <= n:
            guess = input("Guess: ")
            if guess == "DONE":
                break
            if guess == "QUIT":
                print_hidden_board(board)
                return

            board[3][board[0].tolist().index(guess)] = True
            print_player_board(board)

            if guess not in blue_words:
                break

        blue_words = [w for i, w in enumerate(board[0]) if board[1][i] == "True" and board[3][i] == "False"]
        if blue_words == []:
            print("BLUE TEAM WINS")
            break
        print('\n\n')

        red_words = [w for i, w in enumerate(board[0]) if board[2][i] == "True" and board[3][i] == "False"]

        print("RED TEAM PLAYS:")
        print_player_board(board)
        clue, n, _ = algs.ft_generate_clue_v2(board, past_clues, blue_team=False)
        past_clues += [clue]
        print("RED TEAM CLUE: ",clue, n)
        assert clue.lower() in algs.wordset

        guesses = algs.ft_guess_from_clue_prob(board, clue, n)
        print("RED TEAM GUESSES: ", guesses)
        for g in guesses:
            board[3][board[0].tolist().index(g)] = True
            if g not in red_words:
                break
        print_player_board(board)
        red_words = [w for i, w in enumerate(board[0]) if board[2][i] == "True" and board[3][i] == "False"]
        if red_words == []:
            print("RED TEAM WINS")
            break
        print('\n\n')

    print_hidden_board(board)


board = generate_board()
#player_guesser(board)
#player_cluegiver(board)
single_player(board)
