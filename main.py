from file_io import FileIO
import text_cleanser
from text_cleanser import clean_text
import sys
from scipy.sparse import dok_matrix


def main(file_name):
    file_io = FileIO(file_name)
    corpus = file_io.read()
    print(type(corpus))
    distinct_words = clean_text(corpus)
    # print(distinct_words)


if __name__ == '__main__':
    fname = sys.argv[1]
    main(fname)
