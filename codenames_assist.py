import numpy as np

import codenames as cd
import algs

board_words = np.array([
    ["Mint", "Embassy", "Crash", "Crane", "Club"],
    ["Mail", "Grace", "Orange", "Rome", "Nut"],
    ["String", "Princess", "Point", "Trip", "Millionaire"],
    ["Saturn", "Card", "Strike", "Lock", "Robot"],
    ["Staff", "Skyscraper", "War", "Grass", "Stock"]
])

board_colors = np.array([
    ["BLUE", "WHITE", "WHITE", "RED", "WHITE"],
    ["BLUE", "WHITE", "WHITE", "RED", "WHITE"],
    ["BLUE", "WHITE", "WHITE", "RED", "WHITE"],
    ["BLUE", "WHITE", "WHITE", "RED", "WHITE"],
    ["BLUE", "WHITE", "WHITE", "RED", "WHITE"]
])

board = cd.generate_board(words=board_words, color_map=board_colors)

def codemaster_assist(board, blue_first=True):
    past_clues = []

    while True:
        blue_words = [w for i, w in enumerate(board[0]) if board[1][i] == "True" and board[3][i] == "False"]
        #print(board[1]) 
        cd.print_hidden_board(board)

        clue, n, words = algs.ft_generate_clue_v2(board, past_clues)
        past_clues += [clue]

        print("Computer Says: ",clue, n, words)
        assert clue.lower() in algs.wordset

        guess = ""
        i = 0
        cd.print_player_board(board)
        while guess != "DONE" and i <= n:
            guess = input("BLUE GUESSES: ")
            if guess == "DONE":
                break
            if guess == "QUIT":
                cd.print_hidden_board(board)
                return

            board[3][board[0].tolist().index(guess)] = True
            cd.print_player_board(board)

            if guess not in blue_words:
                break
        
        red_words = [w for i, w in enumerate(board[0]) if board[2][i] == "True" and board[3][i] == "False"]
        print("RED CODEMASTER: GIVE CLUE NOW")
        guess = ""
        i = 0
        cd.print_player_board(board)
        while guess != "DONE" and i <= n:
            guess = input("RED GUESSES: ")
            if guess == "DONE":
                break
            if guess == "QUIT":
                cd.print_hidden_board(board)
                return

            board[3][board[0].tolist().index(guess)] = True
            cd.print_player_board(board)

            if guess not in red_words:
                break
        
        

codemaster_assist(board, blue_first=True)