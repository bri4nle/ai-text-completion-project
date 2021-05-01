# ai-text-completion-project

List of Files:
  - README.txt (this file)
  - corpus.txt (input file)
  - requirements.txt
  - file_io.py (gets the file corpus.txt)
  - main.py (starts the program)
  - text_cleanser.py (cleans up and tokenizing text)
  - text_gen.py (generates predictive words with markov chains)
  - user_interface.py (does the AI-user interactions of the program)
  - Report.pdf (Explains the background, method, results, conclusion of the project)
 
 Compiling the Program:
  No compilition required in Python
  
 Running the Program:
  In the command line, go to the project directory and type "python main.py corpus.txt" and press enter to start the program. corpus.txt is the input text file that the predictive words will be based on.
  
 How the Program Works:
  The program tokenizes corpus.txt. The program asks the user to type a phrase. The program then takes the last two words of the user input and generates next predictive words using markov chains and transition matricies and suggests them to the user. 
  The user can then select one of them by enter the number next to the predicted word, in which case, the AI performance rate increases. Or the user can continue the phrase with their own word, in which case, the AI performance rate decreases. 
  To start a new sentence, the user can enter "." at the end of a sentence and continue with a new one. To end the program, the user can end sentence with ".", press enter and type "-1" and press enter. 
