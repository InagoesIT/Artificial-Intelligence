import random as rand

from parser import Parser


class Quiz:
    def __init__(self, ontology):
        self.ontology = ontology

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
            is_answer_right = self.is_answer_right()
            if is_answer_right is None:
                continue
            if is_answer_right:
                total_questions += 1
                score += 1
            if Quiz.wants_to_stop(continue_text):
                break

        print(f"~~~Your score is: {score}/{total_questions}.~~~")
        print(bye_text)

    @staticmethod
    def process_answer(given_answer, answer):
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
        else:
            given_answer = input(possible_questions[question].format(relation[0]))
            return given_answer, relation[2]

    def is_answer_right(self):
        possible_questions = ["-> What is the relationship between {0} and {1}? ",
                              "-> Who is in a relationship with {0}? "]

        question = rand.randrange(0, len(possible_questions))
        concept_nr = rand.randrange(0, len(self.ontology))
        iteration = 0

        for concept1, predicate, concept2 in self.ontology:
            if concept_nr != iteration:
                iteration += 1
                continue

            processed_relation = Parser.get_processed_relation((concept1, concept2, predicate))
            if None in processed_relation:
                concept_nr = rand.randrange(iteration, len(self.ontology))
                iteration += 1
                continue

            given_answer, answer = Quiz.get_answer(possible_questions, question, processed_relation)
            return Quiz.process_answer(given_answer, answer)

        print("Sorry, we didn't find a question...")
        print("We will try to find a question again.")
        return None
