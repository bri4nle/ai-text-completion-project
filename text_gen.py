import threading

from scipy.sparse import dok_matrix, coo_matrix


class TextGenerator:
    def __init__(self, corpus_words):
        self.corpus_words = corpus_words
        self.distinct_words = []
        self.distinct_words_count = 0
        self.word_index_dict = dict
        self.distinct_words_count = 0
        self.set_of_2_words = []
        self.set_of_1_word = []
        self.set_of_2_words_count = 0
        self.set_of_1_word_count = 0
        self.distinct_sets_of_2_words = []
        self.distinct_sets_of_1_word = []
        self.two_words_index_dict = dict
        self.one_word_index_dict = dict
        self.next_after_2_words_matrix = None
        self.next_after_1_word_matrix = None
        self.predicted_words = []
        self.lock = threading.Lock()
        self.setup_data()

    def setup_data(self, addon=[]):
        self.lock.acquire()
        self.corpus_words.extend(addon)
        self.distinct_words = list(set(self.corpus_words))  # Get a list of every words in corpus
        self.distinct_words_count = len(self.distinct_words)  # Get the distinct word count
        # Map each word to an index from distinct words list
        self.word_index_dict = {word: i for i, word in enumerate(self.distinct_words)}
        # Make a k-words list, eg. ['I will', 'she is', ... ]
        self.set_of_2_words = [' '.join(self.corpus_words[i:i + 2]) for i, _ in enumerate(self.corpus_words[:-2])]
        self.set_of_1_word = [' '.join(self.corpus_words[i:i + 1]) for i, _ in enumerate(self.corpus_words[:-1])]
        # Get a distinct set of k-word list
        self.distinct_sets_of_2_words = list(set(self.set_of_2_words))
        self.distinct_sets_of_1_word = list(set(self.set_of_1_word))
        # Get the set count from the list above
        self.set_of_2_words_count = len(self.distinct_sets_of_2_words)
        self.set_of_1_word_count = len(self.distinct_sets_of_1_word)
        # Create the Transitional Matrices
        self.next_after_2_words_matrix = dok_matrix((self.set_of_2_words_count, self.distinct_words_count))
        self.next_after_1_word_matrix = dok_matrix((self.set_of_1_word_count, self.distinct_words_count))
        # Map each 2-word to an index from distinct 2-word list
        self.two_words_index_dict = {word: i for i, word in enumerate(self.distinct_sets_of_2_words)}
        self.one_word_index_dict = {word: i for i, word in enumerate(self.distinct_sets_of_1_word)}
        self.populate_2_words_matrix()
        self.populate_1_word_matrix()
        self.lock.release()

    def populate_2_words_matrix(self):
        # Go through the list of 2-word to populate the Transitional Matrix
        for i, word in enumerate(self.set_of_2_words[:-2]):
            word_seq_index = self.two_words_index_dict[word]
            next_word_index = self.word_index_dict[self.corpus_words[i + 2]]
            self.next_after_2_words_matrix[word_seq_index, next_word_index] += 1

    def populate_1_word_matrix(self):
        for i, word in enumerate(self.set_of_1_word[:-1]):
            word_seq_index = self.one_word_index_dict[word]
            next_word_index = self.word_index_dict[self.corpus_words[i + 1]]
            self.next_after_1_word_matrix[word_seq_index, next_word_index] += 1

    def generate_next_words(self, word_seq, alpha=0):
        next_word_vector = None
        try:
            next_word_vector = self.next_after_2_words_matrix[self.two_words_index_dict[word_seq]] + alpha
        except KeyError as e:  # Failed looking for the 2-word word_seq. Start looking at the last word
            new_word_seq = word_seq.split()[-1:][0]
            try:
                next_word_vector = self.next_after_1_word_matrix[self.one_word_index_dict[new_word_seq]] + alpha
            except KeyError as e2:
                return []
        likelihoods = next_word_vector / next_word_vector.sum()
        likelihoods_coo = coo_matrix(likelihoods)
        sorted_likelihoods = self.sort_coo(likelihoods_coo)
        return self.list_of_predicted_words(sorted_likelihoods)

    def sort_coo(self, m):
        tuples = zip(m.row, m.col, m.data)
        return sorted(tuples, key=lambda x: (x[0], x[2]), reverse=True)

    def list_of_predicted_words(self, likelihood_tuples):
        next_word_index = 1
        next_word_list = []
        for tup in likelihood_tuples:
            next_word_list.append(self.distinct_words[tup[next_word_index]])
            # print(self.distinct_words[tup[next_word_index]])
        return next_word_list

    def update(self, addon=[]):
        t = threading.Thread(target=self.setup_data, args=(addon,))
        t.start()
