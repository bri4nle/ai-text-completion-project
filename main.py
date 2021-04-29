from file_io import FileIO
from text_cleanser import TextCleanser
import sys
from scipy.sparse import dok_matrix


def main(file_name):
    file_io = FileIO(file_name)
    corpus = file_io.read()
    tc = TextCleanser()

    distinct_words = tc.clean_text(corpus)  # Get distinct words from corpus
    corpus_words = tc.get_corpus_words()  # Get a list of every words in corpus
    # Map each word to an index from distinct words list
    word_idx_dict = {word: i for i, word in enumerate(distinct_words)}
    # print(word_idx_dict)

    k = 2  # adjustable
    # Make a list of k words, eg. ['I will', 'He is', ... ]
    sets_of_k_words = [' '.join(corpus_words[i:i + k]) for i, _ in enumerate(corpus_words[:-k])]
    distinct_sets_of_k_words = list(set(sets_of_k_words))  # Distinct list of the above list
    # Map each k-word to an index from distinct k-word list
    k_words_idx_dict = {word: i for i, word in enumerate(distinct_sets_of_k_words)}
    sets_count = len(distinct_sets_of_k_words)  # Length of the distinct set of k-word
    next_after_k_words_matrix = dok_matrix((sets_count, len(distinct_words)))  # Create the Transitional Matrix
    print(str(sets_count) + ", " + str(len(distinct_words)))

    for i, word in enumerate(sets_of_k_words[:-k]):
        word_sequence_idx = k_words_idx_dict[word]
        # print(word_sequence_idx)
        next_word_idx = word_idx_dict[corpus_words[i + k]]  # Extract the next word index for a specifically k-word
        # print(next_word_idx)
        next_after_k_words_matrix[word_sequence_idx, next_word_idx] += 1  # Populating the Translation Matrix
        # print(next_after_k_words_matrix[word_sequence_idx, next_word_idx])
        # print(next_after_k_words_matrix.todense())
    # print(next_after_k_words_matrix.todense())

    # print(sets_of_k_words[:5])
    next_word_arr = next_after_k_words_matrix[k_words_idx_dict['she is']]
    likelihoods = next_word_arr/next_word_arr.sum()
    print(likelihoods)



if __name__ == '__main__':
    fname = sys.argv[1]
    main(fname)
