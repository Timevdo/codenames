from nltk.corpus import wordnet as wn
from nltk.corpus import words

#from nltk.data import find
#from nltk.test.gensim_fixt import setup_module
#import gensim

import itertools
import numpy as np

from pyfasttext import FastText

def wp_guess_from_clue(board, clue, n):
    clue_syn = wn.synsets(clue)[0]

    guesses = []
    for i, option in enumerate(board[0]):
        if board[3][i] == "True":
            continue

        guesses += [(option, clue_syn.wup_similarity(wn.synsets(option)[0]))]

    #print(guesses)
    return sorted(guesses, key= lambda g : g[1], reverse=True)[0:int(n)]

#w2v_model = gensim.models.Word2Vec.load('brown.embedding').wv
#def w2v_guess_from_clue(board, clue, n):
    try:
        len(w2v_model[clue])
    except KeyError:
        print("Clue not in model")
        return []

    guesses = []
    for i, option in enumerate(board[0]):
        if board[3][i] == "True":
            continue
        
        try:
            guesses += [(option, w2v_model.similarity(clue, option))]
        except KeyError:
            print(f"word {option} not in model")
        except:
            print('ERROR')

    guesses = sorted(guesses, key= lambda g : g[1], reverse=True)
    print(guesses)
    return guesses[0:int(n)]


    try:
        len(w2v_model[clue])
    except KeyError:
        print("Clue not in model")
        return []

    guesses = []
    for s in itertools.combinations(board[0], n):
        possible_guess = list(s)
        guesses += [(possible_guess, cluster_similarity(possible_guess + [clue]))]

    guesses = sorted(guesses, key= lambda g : g[1], reverse=True)
    print(guesses[0])
    return guesses[0][0]

ft_model = FastText('cc.en.300.bin')
def ft_guess_from_clue(board, clue, n):
    guesses = []
    for i, option in enumerate(board[0]):
        if board[3][i] == "True":
            continue
    
        guesses += [(option, ft_model.similarity(clue, option))]

    guesses = sorted(guesses, key= lambda g : g[1], reverse=True)
    #print(guesses)
    return guesses[0:int(n)]

wordset = set(words.words())

def is_valid_clue(clue, board):
    valid = True
    for b in board[0]:
        if clue.lower() not in wordset or b.lower() in clue.lower() or clue.lower() in b.lower():
            valid = False
    return valid

def ft_generate_clue_v1(board):
    blue_words = [w for i, w in enumerate(board[0]) if board[1][i] == "True"]

    clues = []
    for i in range(2, len(blue_words) + 1):
        for c in itertools.combinations(blue_words, i):
            print("Iteration: ", i, c)
            c = list(c)
            best_match = ft_model.most_similar(positive=c, k=20)
            for b in best_match:
                if is_valid_clue(b[0], board):
                    clues += [(b[0], b[1], c, len(c))]
                    break

    clues = sorted(clues, key= lambda g : g[1], reverse=True)
    print(clues)
    return clues[0]
        

def ft_generate_clue_v2(board):
    blue_words = [w for i, w in enumerate(board[0]) if board[1][i] == "True"]
    red_words = [w for i, w in enumerate(board[0]) if board[2][i] == "True"]

    clues = []
    for i in range(1, len(blue_words) + 1):
        for c in itertools.combinations(blue_words, i):
            print("Iteration: ", i, c)
            c = list(c)
            best_match = ft_model.most_similar(positive=c, k=30)
            for b in best_match:
                if is_valid_clue(b[0], board):
                    clues.append(b[0])

    #print(clues)

    best = ("Fuck off", 0)
    for j, c in enumerate(clues):
        print(j, end='\r')
        for i in range(1, len(blue_words) + 1):
            guess = ft_guess_from_clue(board, c, i)
            #print(guess)
            correct = True
            for g in guess:
                if g[0] not in blue_words:
                    correct = False
            if correct and i > best[1]:
                best = (c, i, guess)
    
    return best
        

