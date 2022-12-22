import json
import os.path
import random
import random as rand

from WordnetManager import WordnetManager, SYNONYM, MERONYM, HYPERNYM


class Quiz:
    possible_questions = ["-> What is the relationship between {0} and {1}? ",
                          "-> Who is in a relationship with {0}? ",
                          "-> Who is in a relationship {0} with {1}? "]

    def __init__(self, ontology, relationships_count, debug_mode=False):
        self.ontology = ontology
        self.relationships_count = relationships_count
        self.debug_mode = debug_mode
        self.is_right = False
        self.given_answer = ""
        self.answers = []
        self.current_solution = []
        self.are_meronyms_used = False
        self.are_hypernyms_used = False

    def wants_to_stop(self, question):
        if self.debug_mode:
            return
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

        if self.wants_to_stop(hello_text):
            print(bye_text)
            return

        while True:
            self.ask()
            total_questions += 1
            if self.is_answer_right():
                score += 1
            if self.wants_to_stop(continue_text):
                break

        print(f"~~~Your score is: {score}/{total_questions}.~~~")
        print(bye_text)

    def __check_given_answer__(self, subword_index: int) -> None:
        if subword_index == len(self.answers):
            str_solution = " ".join(self.current_solution)
            print(f"Solution tried {str_solution}")
            if str_solution.lower().strip() == self.given_answer.lower().strip():
                self.is_right = True
            return

        for type in [SYNONYM, MERONYM, HYPERNYM]:
            if type == MERONYM:
                self.are_meronyms_used = True
            if type == HYPERNYM:
                self.are_hypernyms_used = True

            for subword_syns in self.answers[subword_index][type]:
                self.current_solution.append(subword_syns)
                self.__check_given_answer__(subword_index + 1)
                if self.is_right is True:
                    return
                self.current_solution.pop()
            if type == MERONYM:
                self.are_meronyms_used = False
            if type == HYPERNYM:
                self.are_hypernyms_used = False

    def is_answer_right(self):
        self.is_right = False

        self.are_meronyms_used = False
        self.are_hypernyms_used = False

        self.__check_given_answer__(0)
        self.current_solution = []
        if self.is_right:
            print(f"Meronyms were used: {self.are_meronyms_used}")
            print(f"Hypernyms were used: {self.are_hypernyms_used}")
            print("Yey, you are right!")
        else:
            print(f"You were wrong!")
        return self.is_right

    @staticmethod
    def get_new_word(word: str) -> str:
        syns_lists = WordnetManager.get_synonims_for(word=word)
        new_words = []
        # pick a syn for every subword
        for syns_list in syns_lists:
            last_element = len(syns_list) - 1
            new_words.append(syns_list[random.randint(0, last_element)])
        return " ".join(new_words)

    def compute_possible_answers(self, question, relation):
        print(f"Initial relationship {relation[0], relation[1], relation[2]}")
        new_first = Quiz.get_new_word(word=relation[0])
        new_middle = Quiz.get_new_word(word=relation[1])
        new_last = Quiz.get_new_word(word=relation[2])
        if question == 0:
            self.answers = WordnetManager.get_nyms_for(word=relation[1])
            with open(os.path.join("resources", "answers"), mode='w') as fd:
                json.dump(self.answers, fd, indent=4)
            self.given_answer = input(Quiz.possible_questions[question].format(new_first, new_last))
        elif question == 1:
            self.answers = WordnetManager.get_nyms_for(word=relation[2])
            with open(os.path.join("resources", "answers"), mode='w') as fd:
                json.dump(self.answers, fd, indent=4)
            self.given_answer = input(Quiz.possible_questions[question].format(new_first))
        else:
            self.answers = WordnetManager.get_nyms_for(word=relation[2])
            with open(os.path.join("resources", "answers"), mode='w') as fd:
                json.dump(self.answers, fd, indent=4)
            self.given_answer = input(Quiz.possible_questions[question].format(new_first, new_middle))

    def ask(self):
        self.answers = []
        while True:
            question = rand.randrange(0, len(Quiz.possible_questions))
            relation_nr = rand.randrange(0, self.relationships_count)
            relation = self.ontology[relation_nr]
            if None not in relation:
                break

        self.compute_possible_answers(question, relation)
