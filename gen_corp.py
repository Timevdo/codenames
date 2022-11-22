from nltk import FreqDist
from nltk.corpus import brown
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

from nltk.data import find
from nltk.test.gensim_fixt import setup_module
import gensim

import pickle

board_frequency_list = FreqDist(i.lower() for i in brown.words())
nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}

train_set = brown.sents()
model = gensim.models.Word2Vec(train_set)
print(len(model.wv))
model.save('brown.embedding')

board_words = [
    w[0] for w in board_frequency_list.most_common()[500:1500] if w[0] in nouns and w[0] not in stopwords.words('english') and w[0] in model.wv
]
print(len(board_words))
print(board_words[0:20])

flname = 'board_words.bin'
fl = open(flname, 'wb')
pickle.dump(board_words, fl)
fl.close()
