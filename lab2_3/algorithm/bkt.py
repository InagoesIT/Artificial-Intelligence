import logging
from model import ProblemModel


class BktAlgorithm:
    def __init__(self, model) -> None:
        self.solution_found = False
        self.model = model
        self.before_state = dict()
        self.before_transition = dict()
        self.tr_list = list()
        self.current_path = set()

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
            logging.info("-> Moving water from %s to %s" % (from_state[0], to_state[0]))

    def __bkt__(self, state):
        if self.model.is_final(state):
            self.solution_found = True
            self.build_solution(state)
            return

        tuple_state = tuple(state)
        for transition in self.model.get_transitions(state):
            next_state = self.model.do_transition(state, transition)
            tuple_next_state = tuple(next_state)
            if tuple_next_state not in self.current_path:
                self.before_state[tuple_next_state] = tuple_state
                self.before_transition[tuple_next_state] = transition
                self.current_path.add(tuple_next_state)
                self.__bkt__(next_state)
                if self.solution_found is True:
                    return
                self.current_path.remove(tuple_next_state)

    def run(self):
        state = self.model.init()
        self.current_path = {tuple(state)}
        self.__bkt__(state=state)
