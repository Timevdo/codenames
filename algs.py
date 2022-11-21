from nltk.corpus import wordnet as wn

from nltk.data import find
from nltk.test.gensim_fixt import setup_module
import gensim

def wp_guess_from_clue(board, clue, n):
    clue_syn = wn.synsets(clue)[0]

    guesses = []
    for i, option in enumerate(board[0]):
        if board[3][i] == "True":
            continue

        guesses += [(option, clue_syn.wup_similarity(wn.synsets(option)[0]))]

    #print(guesses)
    return sorted(guesses, key= lambda g : g[1], reverse=True)[0:int(n)]

model = gensim.models.Word2Vec.load('brown.embedding').wv

def w2v_guess_from_clue(board, clue, n):
    try:
        len(model[clue])
    except KeyError:
        print("Clue not in model")
        return []

    guesses = []
    for i, option in enumerate(board[0]):
        if board[3][i] == "True":
            continue
        
        try:
            guesses += [(option, model.similarity(clue, option))]
        except KeyError:
            print(f"word {option} not in model")
        except:
            print('ERROR')

    guesses = sorted(guesses, key= lambda g : g[1], reverse=True)
    print(guesses)
    return guesses[0:int(n)]