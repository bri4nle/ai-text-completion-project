
class UserInterface:
    def __init__(self, text_gen):
        self.instructions()
        self.user_input = ''
        self.get_last_2_words(self.user_input)
        self.total_num_picked = 0
        self.total_correct_pick = 0
        self.text_gen = text_gen

    def runProgram(self):
        """
        This function provides an command line interface for users.
        :return:
        """
        self.instructions  # print instructions

        while True:
            self.user_input = input('Start typing: ')
            if self.user_input[:2] == '-1':
                break
            while True:
                word_seq = self.get_last_2_words(self.user_input)
                predicted_words = self.text_gen.generate_next_words(word_seq)
                if not predicted_words:  # AI couldn't comes up with predicted words
                    # print('*** AI looses points ***')
                    new_user_input = input(self.user_input)
                    if new_user_input == "":
                        pass
                    elif new_user_input[-1] == ".":
                        self.user_input += new_user_input
                        # Take the user's new input and update the model
                        self.text_gen.update(self.user_input.split(' '))
                        break
                    self.user_input += new_user_input
                    self.total_num_picked += 1

                else:  # AI came up with predictive words
                    user_choice = ''
                    index = 0
                    user_entered_new_words = False
                    done = False
                    do_nothing = False
                    # Displays the predicted words
                    for i, word in enumerate(predicted_words):
                        print('%d: %s\t' % (i + 1, word)),
                        if i == 2:
                            break
                    while True:  # Input validation
                        try:
                            user_choice = input(self.user_input)
                            if user_choice == "":
                                do_nothing = True
                                break
                            if user_choice[-1] == ".":
                                self.user_input += user_choice
                                # Take the user's new input and update the model
                                self.text_gen.update(self.user_input.split(' '))
                                done = True
                                break
                            index = int(user_choice)
                            if index < 1 or index > len(predicted_words):
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
                        self.user_input += user_choice
                        self.total_num_picked += 1
                    elif do_nothing:
                        pass
                    else:  # The predicted list has the desired word, appends that word to the sentence.
                        self.user_input += ' ' + predicted_words[index - 1]
                        self.total_correct_pick += 1
                        self.total_num_picked += 1
                        if self.user_input[:-1] == ".":
                            break
                print('-----------------------------------------------------')
                try:
                    print('AI performance rate: {:.2}'.format(self.total_correct_pick / self.total_num_picked))
                except ZeroDivisionError as e:
                    pass

    def get_last_2_words(self, user_input):
        """
        This function extract the last 2 word of the input and returns them.
        :param user_input:
        :return:
        """
        string_vector = user_input.split()[-2:]
        return ' '.join(string_vector)

    def instructions(self):
        """
        Instruction message.
        :return:
        """
        print("""
                    *** This is an AI Text Completion Program ***

        Instructions:

        Type a phrase and press enter to see AI's suggested predictive words. 
        TO SELECT A PREDICTIVE WORD: Type the number next to the predictive word and press enter.
            - AI performance rate increases as you select more predictive words 
              and decreases if predictive words are not selected.
            - If AI can not predict any words, it will lose points.
        TO START A NEW SENTENCE: Enter "." at the end of the sentene and continue typing
        TO END PROGRAM: End sentence with ".", press enter and type "-1" and press enter.
     
        """)
