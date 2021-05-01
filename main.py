from file_io import FileIO
from text_cleanser import TextCleanser
from text_gen import TextGenerator
from user_interface import UserInterface
import sys


def main(file_name):
    file_io = FileIO(file_name)
    corpus = file_io.read()
    tc = TextCleanser()

    corpus_words = tc.clean_text(corpus)  # Get a list of every words in corpus
    text_gen = TextGenerator(corpus_words)
    
    ui = UserInterface(text_gen) 
    ui.runProgram()  # Starts the program


if __name__ == '__main__':
    fname = sys.argv[1]
    main(fname)
