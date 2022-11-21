from colorama import Fore, Back, Style
import numpy as np
import pickle
import random

import algs

NUM_BLUE_WORDS = 5
NUM_RED_WORDS = 5

def generate_board():
    bwfl = open('board_words.bin', 'rb')
    board_words_list = pickle.load(bwfl)

    board_words = np.array(random.sample(board_words_list, 25))

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

def player_cluegiver(board):
    while True:
        print_hidden_board(board)

        clue = input(Fore.RESET + "Enter Clue: ")
        n = input("Enter Number: ")

        guesses = algs.w2v_guess_from_clue(board, clue, n)

        for g in guesses:
            board[3][board[0].tolist().index(g[0])] = True

        print("Computer Guessed", guesses)
        print_player_board(board)
        print("\n")


board = generate_board()
player_cluegiver(board)