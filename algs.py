from nltk.corpus import wordnet as wn
from nltk.corpus import words

#from nltk.data import find
#from nltk.test.gensim_fixt import setup_module
#import gensim

import itertools
import numpy as np
import math

import pyprog

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

def is_valid_clue(clue, board, past_clues=[]):
    valid = True
    for b in board[0]:
        if clue.lower() not in wordset or b.lower() in clue.lower() or clue.lower() in b.lower() or clue in past_clues:
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
        

def ft_generate_clue_v2(board, past_clues=[], show_progress=True, blue_team=True):
    if blue_team:
        good_words = [w for i, w in enumerate(board[0]) if board[1][i] == "True" and board[3][i] == "False"]
    else:
        good_words = [w for i, w in enumerate(board[0]) if board[2][i] == "True" and board[3][i] == "False"]
    #print(board[3])

    if show_progress:
        prog = pyprog.ProgressBar("", "")

    clues = []
    iter = 0
    N = min(len(good_words) + 1, 6)
    
    best_match = ft_model.most_similar(positive=good_words, k=500)
    for b in best_match:
        if is_valid_clue(b[0], board, past_clues):
            clues.append(b[0])
    #print(clues)
    if show_progress:
        prog.end()

    best = ("NO CLUE", 0, [])
    for j, c in enumerate(clues):
        for i in range(1, len(good_words)):
            guess = ft_guess_from_clue(board, c, i)
            #print(guess)
            correct = True

            new_weights = []
            for g in guess:
                new_weights.append(g[1])
                if g[0] not in good_words:
                    correct = False

            old_weights = []
            for g in best[2]:
                old_weights.append(g[1])

            if (correct and i > best[1]) or \
            (correct and i == best[1] and np.mean(new_weights) > np.mean(old_weights)) or \
            (correct and i > best[1] - 1 and np.mean(new_weights) - np.mean(old_weights) > 0.2):
                best = (c, i, guess)
    
    if best[1] == 0:
        best = (clues[0], 1, [])

    return best

def sigmoid(x, a=1, b=0):
    x_a = a*(x - b)
    return 1/(1 + np.exp(-(x_a)))

def ft_guess_from_clue_prob(board, clue, n):
    guesses = []
    for i, option in enumerate(board[0]):
        if board[3][i] == "True":
            guesses += [0]
        else:
            guesses += [ft_model.similarity(clue, option)]

    guesses = np.array(guesses)
    
    #make a stochastic vector
    q5_guesses = np.quantile(guesses, 0.8)
    filtered_guesses = np.array([g if g > q5_guesses else 0 for g in guesses])
    sigm_guesses = sigmoid(filtered_guesses, a=20, b=0.3)
    stoch_guesses =  sigm_guesses / np.linalg.norm(sigm_guesses, ord=1)

    #for i, w in enumerate(board[0]):
    #    print(w, guesses[i], filtered_guesses[i], stoch_guesses[i])

    #choose based on weights
    guess = np.random.choice(board[0], n, p=stoch_guesses, replace=False)
    return guess

