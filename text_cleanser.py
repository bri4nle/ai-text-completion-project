class TextCleanser:
    def __init__(self):
        self.corpus_words = ''

    def clean_text(self, corpus):
        corpus = corpus.replace('\n', ' ')
        corpus = corpus.replace('\t', ' ')
        corpus = corpus.replace('“', ' " ')
        corpus = corpus.replace('”', ' " ')
        for spaced in ['.', '-', ',', '!', '?', '(', '—', ')']:
            corpus = corpus.replace(spaced, ' {0} '.format(spaced)) 
        self.corpus_words = corpus.split(' ')
        self.corpus_words = [word for word in self.corpus_words if word != ''] 
        return self.corpus_words

    def get_corpus_distinct_words(self):
        return list(set(self.corpus_words))  # Filter distinct words
