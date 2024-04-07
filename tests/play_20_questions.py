from evaluator import *

DESCRIPTION = "Test if the model is able to ask questions to get to an answer."

TAGS = ['fun']

question = """
Let's play 20 questions! I'm thinking of %s. You have 20 questions to guess what it is. Ask me yes or no questions, about anything you want. Do not guess randomly or make overly specific guesses. Do not make your final guess until you are absolutely sure. (You can think out loud first, but your last sentence MUST be a question.)

Your answer should be of the format
[question number]. [internal thought]

Question: [your question]?

If think you know the answer it should say

Question: Is the answer [your guess]?
"
"""

def is_done_animal(guess):
    return "llama" in guess.lower()

def is_done_book(guess):
    return "diamond age" in guess.lower() or 'illustrated primer' in guess.lower()

def take_one_word(guess):
    return guess.split()[0]

def take_question(guess):
    if 'Question:' in guess:
        return guess.split("Question:")[-1]
    else:
        return guess

TestTwentyQuestionsLlama = question%("an animal")  >> LLMConversation() >> UntilDone(PyFunc(is_done_animal), (PyFunc(take_question) >> LLMRun("I'm playing 20 questions with someone. I'm thinking of a Llama. Here's their question: <A>.\nAnswer either 'Yes' or 'No'; do not answer anything else.") >> PyFunc(take_one_word) >> LLMConversation()), max_iters=20) >> PyFunc(is_done_animal)
TestTwentyQuestionsBook = question%("a book")  >> LLMConversation() >> UntilDone(PyFunc(is_done_book), (PyFunc(take_question) >> LLMRun("I'm playing 20 questions with someone. I'm thinking of the book The Diamond Age by Neal Stephenson. Here's their question: <A>.\nAnswer either 'Yes' or 'No'; do not answer anything else.") >> PyFunc(take_one_word) >> LLMConversation()), max_iters=20) >> PyFunc(is_done_book)
 
if __name__ == "__main__":
    print(run_test(TestTwentyQuestionsBook))
