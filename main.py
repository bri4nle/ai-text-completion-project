from file_io import FileIO
from text_cleanser import TextCleanser
from text_gen import TextGenerator
import sys


def main(file_name):
    file_io = FileIO(file_name)
    corpus = file_io.read()
    tc = TextCleanser()

    corpus_words = tc.clean_text(corpus)  # Get a list of every words in corpus
    text_gen = TextGenerator(corpus_words)
    total_num_picked = 0
    total_correct_pick = 0
    # text_gen.generate_next_words("I am")
    # print(get_last_2_words('I am the king'))

    while True:
        user_input = input('Start typing: ')
        word_seq = get_last_2_words(user_input)
        predicted_words = text_gen.generate_next_words(word_seq)
        for i, word in enumerate(predicted_words):
            print('%d: %s\t' % (i + 1, word)),
            if i == 2:
                break
        if not predicted_words:
            input(user_input + ' ')


def get_last_2_words(str):
    string_vector = str.split()[-2:]
    return ' '.join(string_vector)


if __name__ == '__main__':
    fname = sys.argv[1]
    main(fname)
