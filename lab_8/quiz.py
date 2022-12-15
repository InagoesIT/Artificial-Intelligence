import random as rand

from parser import Parser


class Quiz:
    def __init__(self, ontology, relationships_count):
        self.ontology = ontology
        self.relationships_count = relationships_count

    @staticmethod
    def wants_to_stop(question):
        answer = input(question)
        while True:
            if answer.lower() == "no" or answer.lower() == "n":
                return True
            elif answer.lower() == "yes" or answer.lower() == "y":
                return False
            print("You should type 'yes'/'y' or 'no'/'n'!")
            answer = input(question)

    def run(self):
        hello_text = "-> Hello, do you want to start the Quiz?\n"
        bye_text = "~~~Bye!~~~\n"
        continue_text = "-> Do you want to continue?\n"
        score = 0
        total_questions = 0

        if Quiz.wants_to_stop(hello_text):
            print(bye_text)
            return

        while True:
            given_answer, answer = self.ask()
            if Quiz.is_answer_right(given_answer, answer):
                total_questions += 1
                score += 1
            if Quiz.wants_to_stop(continue_text):
                break

        print(f"~~~Your score is: {score}/{total_questions}.~~~")
        print(bye_text)

    @staticmethod
    def is_answer_right(given_answer, answer):
        if given_answer.lower() == answer.lower():
            print("Yey, you are right!")
            return True
        print(f"You were wrong... The answer was {answer}.")
        return False

    @staticmethod
    def get_answer(possible_questions, question, relation):
        if question == 0:
            given_answer = input(possible_questions[question].format(relation[0], relation[2]))
            return given_answer, relation[1]
        elif question == 1:
            given_answer = input(possible_questions[question].format(relation[0]))
            return given_answer, relation[2]
        else:
            given_answer = input(possible_questions[question].format(relation[1], relation[0]))
            return given_answer, relation[2]

    def ask(self):
        possible_questions = ["-> What is the relationship between {0} and {1}? ",
                              "-> Who is in a relationship with {0}? ",
                              "-> Who is in a relationship {0} with {1}? "]

        while True:
            question = rand.randrange(0, len(possible_questions))
            relation_nr = rand.randrange(0, self.relationships_count)
            relation = self.ontology[relation_nr]
            if None not in relation:
                break

        return Quiz.get_answer(possible_questions, question, relation)
