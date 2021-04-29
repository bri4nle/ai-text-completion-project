from scipy.sparse import dok_matrix, coo_matrix


class TextGenerator:
    def __init__(self, corpus_words):
        self.corpus_words = corpus_words
        self.distinct_words = []
        self.distinct_words_count = 0
        self.word_index_dict = dict
        self.distinct_words_count = 0
        self.set_of_2_words = []
        self.set_of_2_words_count = 0
        self.distinct_sets_of_2_words = []
        self.two_words_index_dict = dict
        self.next_after_2_words_matrix = None
        self.predicted_words = []
        self.setup_data()
        self.populate_matrix()

    def setup_data(self):
        self.distinct_words = list(set(self.corpus_words))
        self.distinct_words_count = len(self.distinct_words)
        self.word_index_dict = {word: i for i, word in enumerate(self.distinct_words)}
        self.set_of_2_words = [' '.join(self.corpus_words[i:i + 2]) for i, _ in enumerate(self.corpus_words[:-2])]
        self.set_of_2_words_count = len(list(set(self.set_of_2_words)))
        self.next_after_2_words_matrix = dok_matrix((self.set_of_2_words_count, self.distinct_words_count))
        self.distinct_sets_of_2_words = list(set(self.set_of_2_words))
        self.two_words_index_dict = {word: i for i, word in enumerate(self.distinct_sets_of_2_words)}
        self.populate_matrix(2)

    def populate_matrix(self, k_word=0):
        print(k_word)
        for i, word in enumerate(self.set_of_2_words[:-k_word]):
            word_seq_index = self.two_words_index_dict[word]
            next_word_index = self.word_index_dict[self.corpus_words[i + k_word]]
            # TODO: add if statements for different word sequence length
            self.next_after_2_words_matrix[word_seq_index, next_word_index] += 1

    def generate_next_words(self, word_seq, num_of_words=5, alpha=0):
        next_word_vector = self.next_after_2_words_matrix[self.two_words_index_dict[word_seq]] + alpha
        likelihoods = next_word_vector / next_word_vector.sum()
        likelihoods_coo = coo_matrix(likelihoods)
        sorted_likelihoods = self.sort_coo(likelihoods_coo)
        print(sorted_likelihoods[:5])

    def run_model(self):
        pass

    def sort_coo(self, m):
        tuples = zip(m.row, m.col, m.data)
        return sorted(tuples, key=lambda x: (x[0], x[2]), reverse=True)


corpus = ""
file_name = 'sherlock-holmes-corpus.txt'
with open(file_name, encoding='utf8', mode='r') as f:
    corpus += f.read()
corpus = corpus.replace('\n', ' ')
corpus = corpus.replace('\t', ' ')
corpus = corpus.replace('“', ' " ')
corpus = corpus.replace('”', ' " ')
for spaced in ['.', '-', ',', '!', '?', '(', '—', ')']:
    corpus = corpus.replace(spaced, ' {0} '.format(spaced))

words = corpus.split(' ')
words = [word for word in words if word != '']

text_gen = TextGenerator(words)
text_gen.generate_next_words('I will')
# distinct_words = list(set(corpus_words))
# word_idx_dict = {word: i for i, word in enumerate(distinct_words)}
# distinct_words_count = len(list(set(corpus_words)))
#
# k = 2  # adjustable
# sets_of_k_words = [' '.join(corpus_words[i:i + k]) for i, _ in enumerate(corpus_words[:-k])]
# sets_count = len(list(set(sets_of_k_words)))
# next_after_k_words_matrix = dok_matrix((sets_count, len(distinct_words)))
#
# distinct_sets_of_k_words = list(set(sets_of_k_words))
# k_words_idx_dict = {word: i for i, word in enumerate(distinct_sets_of_k_words)}
#
# for i, word in enumerate(sets_of_k_words[:]):
#     word_sequence_idx = k_words_idx_dict[word]
#     next_word_idx = word_idx_dict[corpus_words[i + k]]
#     next_after_k_words_matrix[word_sequence_idx, next_word_idx] += 1
#
#
# def sample_next_word_after_sequence(word_sequence, alpha=0):
#     next_word_vector = next_after_k_words_matrix[k_words_idx_dict[word_sequence]] + alpha
#     likelihoods = next_word_vector / next_word_vector.sum()
#     # print(likelihoods)
#     print(type(likelihoods))
#     likelihoods_len = len(likelihoods)
#     # print(len(likelihoods))
#     likelihoods_coo = coo_matrix(likelihoods)
#     sorted_likelihoods = sort_coo(likelihoods_coo)
#     print(sorted_likelihoods[:5])
#     # for i, j, k in zip(sorted_likelihoods.row, sorted_likelihoods.col, sorted_likelihoods.data):
#     #     print("row = %d, column = %d, value = %.2f" % (i, j, k))
#     # print(distinct_words[j])
#
#
# def sort_coo(m):
#     tuples = zip(m.row, m.col, m.data)
#     return sorted(tuples, key=lambda x: (x[0], x[2]), reverse=True)


# sample_next_word_after_sequence('I will')
