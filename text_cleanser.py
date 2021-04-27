def clean_text(corpus):
    corpus = corpus.replace('\n', ' ')
    corpus = corpus.replace('\t', ' ')
    corpus = corpus.replace('“', ' " ')
    corpus = corpus.replace('”', ' " ')
    for spaced in ['.', '-', ',', '!', '?', '(', '—', ')']:
        corpus = corpus.replace(spaced, ' {0} '.format(spaced))
    corpus_words = corpus.split(' ')
    corpus_words = [word for word in corpus_words if word != '']
    distinct_words = list(set(corpus_words))                            # Filter distinct words
    return distinct_words
