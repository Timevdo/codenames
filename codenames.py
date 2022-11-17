from colorama import Fore, Back, Style
import numpy as np
import pickle
import random

NUM_BLUE_WORDS = 5
NUM_RED_WORDS = 5

def generate_board():
    bwfl = open('board_words.bin', 'rb')
    board_words_list = pickle.load(bwfl)

    board_words = np.reshape(np.array(random.sample(board_words_list, 25)), (5,5))

    blue_idx = set(random.sample(range(25), NUM_BLUE_WORDS))
    red_idx = set(random.sample(set(range(25)) - blue_idx, NUM_RED_WORDS))

    blue_arr = np.full(25, False)
    red_arr = np.full(25, False)

    for i in blue_idx:
        blue_arr[i] = True
    for i in red_idx:
        red_arr[i] = True

    board = np.stack([board_words, np.reshape(blue_arr, (5,5)), np.reshape(red_arr, (5,5))])

    return board

def print_hidden_board(board):
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
        
def print_player_board(board):
    for i, row in enumerate(board[0]):
        rowstr = ""     
        for j, word in enumerate(row):
            rowstr += f"{word:<15}"
        print(rowstr)

def player_cluegiver():
    pass


board = generate_board()
print_hidden_board(board)
print()
print_player_board(board)   