# codenames
Codenames AI project for LX496 Computational Linguistics

This version of the project uses the pretrained generic English vectorization that comes with fastText.

Please install all the python dependencies by running `pip install -r requirements.txt`
To use, first run `download_ft_model.py`
It downloads about 6GB of vectors so please be patient

Then run, `codenames.py` to play against the computer. It also has functions to just give clues or just guess words, you can use those functions by uncommenting the appropriate lines in the fiie.

The file `codenames_assist.py` contains the code to allow one AI codemaster to play in an otherwise human game.

The actual algorithms that the computer uses to play codenames is in the file `algs.py`
