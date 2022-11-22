import fasttext.util

ft = fasttext.load_model('cc.en.300.bin')
fasttext.util.reduce_model(ft, 100)
ft.save_model('cc.en.100.bin')