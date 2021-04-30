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

    print('Enter "." at the of the sentence to start a new sentence.')
    while True:
        user_input = input('Start typing: ')
        if user_input == '-1':
            break
        while True:
            word_seq = get_last_2_words(user_input)
            predicted_words = text_gen.generate_next_words(word_seq)
            if not predicted_words:
                print('*** AI looses points ***')
                new_user_input = input(user_input)
                if new_user_input[0] == ".":
                    break
                user_input += new_user_input
                total_num_picked += 1
                # AI looses points
            else:
                user_choice = ''
                index = 0
                user_entered_new_words = False
                done = False
                for i, word in enumerate(predicted_words):
                    print('%d: %s\t' % (i + 1, word)),
                    if i == 2:
                        break
                while True:  # Input validation
                    try:
                        user_choice = input(user_input)
                        if user_choice[0] == ".":
                            done = True
                            break
                        index = int(user_choice)
                        if index < 1 or index > 3:
                            print('Invalid choice. Try again')
                        else:
                            break
                    except ValueError as e:
                        user_entered_new_words = True
                        break
                if done:
                    break
                if user_entered_new_words:  # The predicted list doesn't have to desired word
                    # AI looses point
                    user_input += user_choice
                    total_num_picked += 1
                else:  # The predicted list has the desired word, appends that word to the sentence.
                    user_input += ' ' + predicted_words[index - 1]
                    total_correct_pick += 1
                    total_num_picked += 1
            print('-----------------------------------------------------')
            print('AI performance rate: {:.2}'.format(total_correct_pick / total_num_picked))


def get_last_2_words(user_input):
    string_vector = user_input.split()[-2:]
    return ' '.join(string_vector)


if __name__ == '__main__':
    fname = sys.argv[1]
    main(fname)
