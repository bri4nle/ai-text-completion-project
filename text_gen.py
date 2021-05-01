import threading
from scipy.sparse import dok_matrix, coo_matrix


class TextGenerator:
    """
    This class generates a set of predicted next words based on a input word sequence
    """
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
        """
        This function processes the corpus furthermore. It maps each k-word (1 and 2) sequence
        to an index to provide O(1) lookup time.
        It also creates the 2 Transitional Probabilistic Matrices, which allows us to calculate
        the next word probability based on an input word sequence.
        :param addon:
        :return:
        """
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
        """
        This function populates the next_after_2_words_matrix based on the frequency of a word
        appearing after a specific word sequence
        :return:
        """
        # Go through the list of 2-word to populate the Transitional Matrix
        for i, word in enumerate(self.set_of_2_words[:-2]):
            word_seq_index = self.two_words_index_dict[word]
            next_word_index = self.word_index_dict[self.corpus_words[i + 2]]
            self.next_after_2_words_matrix[word_seq_index, next_word_index] += 1

    def populate_1_word_matrix(self):
        """
        This function populates the next_after_1_word_matrix based on the frequency of a word
        appearing after a specific word sequence
        :return:
        """
        for i, word in enumerate(self.set_of_1_word[:-1]):
            word_seq_index = self.one_word_index_dict[word]  # Fine the index of word
            next_word_index = self.word_index_dict[self.corpus_words[i + 1]]
            self.next_after_1_word_matrix[word_seq_index, next_word_index] += 1

    def generate_next_words(self, word_seq):
        """
        This function uses the 2 matrices to calculate the next word probability for word_seq.
        If the 2-word sequence is not found, the 1-word sequence will be opted in.
        :param word_seq: A word sequence used to get predict the next words
        :return: A set of predicted next words
        """
        next_word_vector = None
        try:
            next_word_vector = self.next_after_2_words_matrix[self.two_words_index_dict[word_seq]]
        except KeyError as e:  # Failed looking for the 2-word word_seq. Start looking at the last word
            new_word_seq = word_seq.split()[-1:][0]
            try:
                next_word_vector = self.next_after_1_word_matrix[self.one_word_index_dict[new_word_seq]]
            except KeyError as e2:
                return []
        likelihoods = next_word_vector / next_word_vector.sum()  # Calculate the likelihoods of the next words
        likelihoods_coo = coo_matrix(likelihoods)   # Convert to coo_matrix to iterate easily
        sorted_likelihoods = self.sort_coo(likelihoods_coo)
        return self.list_of_predicted_words(sorted_likelihoods)

    def sort_coo(self, m):
        """
        This function converts and sorts the matrix m by descending order and returns it
        :param m:
        :return:
        """
        tuples = zip(m.row, m.col, m.data)
        return sorted(tuples, key=lambda x: (x[0], x[2]), reverse=True)

    def list_of_predicted_words(self, likelihood_tuples):
        """
        This function looks up a the predicted by the indexes from likelihood_tuples
        :param likelihood_tuples: Predicted words' indexes
        :return: A set of next words
        """
        next_word_index = 1
        next_word_list = []
        for tup in likelihood_tuples:
            next_word_list.append(self.distinct_words[tup[next_word_index]])
            # print(self.distinct_words[tup[next_word_index]])
        return next_word_list

    def update(self, addon=[]):
        """
        This function takes in a new sentence, spawn a threat, and reruns the model with
        that new sentence
        :param addon: New sentence, split into a list of words
        :return: None
        """
        t = threading.Thread(target=self.setup_data, args=(addon,))
        t.start()
