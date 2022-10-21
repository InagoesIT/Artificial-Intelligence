import logging
from algorithm.model import ProblemModel


class HillClimbingAlgorithm:
    def __init__(self, model) -> None:
        self.solution_found = False
        self.model = model
        self.before_state = dict()
        self.before_transition = dict()
        self.tr_list = list()

    def build_solution(self, state):
        modified_state = tuple(state)
        while modified_state in self.before_state:
            self.tr_list.append(self.before_transition[modified_state])
            modified_state = self.before_state[modified_state]
        self.tr_list = self.tr_list[::-1]

    def pretty_print_solution(self):
        dict_data = ProblemModel.name_mapper
        for tr in self.tr_list:
            from_state = [i for i in dict_data if dict_data[i] == tr[0]]
            to_state = [i for i in dict_data if dict_data[i] == tr[1]]
            logging.info("Moving water from %s to %s" % (from_state[0], to_state[0]))

    def heuristic(self, state):
        return min(abs(state[0] - self.model.k), abs(state[1] - self.model.k))

    def __hill_climbing__(self, state):
        """
        first choice hill climbing
        """
        if self.model.is_final(state):
            self.solution_found = True
            self.build_solution(state)
            return

        tuple_state = tuple(state)
        for transition in self.model.get_transitions(state):
            next_state = self.model.do_transition(state, transition)
            tuple_next_state = tuple(next_state)

            if self.heuristic(tuple_next_state) < self.heuristic(tuple_state):
                self.before_state[tuple_next_state] = tuple_state
                self.before_transition[tuple_next_state] = transition
                self.__hill_climbing__(tuple_next_state)
                return

    def run(self):
        state = self.model.init()
        self.__hill_climbing__(state=state)
