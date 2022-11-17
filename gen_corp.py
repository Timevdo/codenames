from nltk import FreqDist
from nltk.corpus import brown
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

import pickle

board_frequency_list = FreqDist(i.lower() for i in brown.words())
nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}

board_words = [
    w[0] for w in board_frequency_list.most_common()[500:1500] if w[0] in nouns and w[0] not in stopwords.words('english')
]
print(len(board_words))
print(board_words[0:20])

flname = 'board_words.bin'
fl = open(flname,'wb')
pickle.dump(board_words, fl)
fl.close()
