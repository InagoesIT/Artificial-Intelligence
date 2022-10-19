import logging
from model import ProblemModel


def get_first_unexplored(priority_queue):
    for i in range(len(priority_queue)):
        if not priority_queue[i][2]:
            return priority_queue[i], i

    return None


class AStarAlgorithm:
    def __init__(self, model) -> None:
        self.solution_found = False
        self.model = model
        self.before_state = dict()
        self.before_transition = dict()
        self.tr_list = list()
        self.priority_queue = []  # every element is of the form: (heuristic, state, explored)
        self.best_score = self.model.capacities[0] * self.model.capacities[1] * 10

    def build_solution(self, state):
        self.priority_queue.sort(reverse=True)
        self.priority_queue.pop(0)
        for element in self.priority_queue:
            if element[0] >= state[0]:
                continue
            if not element[2]:
                continue
            transition = self.model.find_transition(element[1], state[1])
            if transition is not None:
                self.tr_list.append(transition)
                state = element

        self.tr_list.append(self.model.find_transition((0, 0), state[1]))
        self.tr_list = self.tr_list[::-1]

    def pretty_print_solution(self):
        dict_data = ProblemModel.name_mapper
        for tr in self.tr_list:
            from_state = [i for i in dict_data if dict_data[i] == tr[0]]
            to_state = [i for i in dict_data if dict_data[i] == tr[1]]
            logging.info("Moving water from %s to %s" % (from_state[0], to_state[0]))

    def heuristic(self, state):
        return min(abs(state[0] - self.model.k), abs(state[1] - self.model.k))

    def __a_star__(self, state):
        self.add_all_neighbours(state=state, score=1)
        first_unexplored, curr_index = get_first_unexplored(self.priority_queue)
        last_final_state = ()

        while first_unexplored is not None and first_unexplored[0] < self.best_score:
            if self.model.is_final(first_unexplored[1]):
                self.best_score = first_unexplored[0]
                self.solution_found = True
                self.priority_queue.pop(curr_index)
                self.priority_queue.append((first_unexplored[0] + 1, first_unexplored[1], True))
                last_final_state = (first_unexplored[0] + 1, first_unexplored[1], True)
                continue
            self.priority_queue.pop(curr_index)
            self.priority_queue.append((first_unexplored[0], first_unexplored[1], True))

            self.add_all_neighbours(first_unexplored[1], first_unexplored[0])
            self.clean_duplicates()
            self.priority_queue.sort()

            first_unexplored, curr_index = get_first_unexplored(self.priority_queue)

        if self.solution_found:
            self.build_solution(last_final_state)

    def add_all_neighbours(self, state, score):
        for transition in self.model.get_transitions(state):
            next_state = self.model.do_transition(state, transition)
            tuple_next_state = tuple(next_state)
            self.priority_queue.append((self.heuristic(tuple_next_state) + score, tuple_next_state, False))

    def clean_duplicates(self):
        resulting_dict = dict()

        for score, state, explored in self.priority_queue:
            if state in resulting_dict:
                if score >= resulting_dict[state][0]:
                    if explored:
                        resulting_dict[state] = (resulting_dict[state][0], True)
                        continue
                else:
                    resulting_dict[state] = (score, resulting_dict[state][1] or explored)
                    continue
                continue
            resulting_dict[state] = (score, explored)

        self.priority_queue = []
        for key in resulting_dict:
            self.priority_queue.append((resulting_dict[key][0], key, resulting_dict[key][1]))

    def run(self):
        state = self.model.init()
        self.__a_star__(state=state)
