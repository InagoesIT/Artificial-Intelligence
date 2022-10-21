import logging
import networkx as nx
from algorithm.model import ProblemModel


class BfsAlgorithm:
    def __init__(self, model) -> None:
        self.solution_found = False
        self.model = model
        self.states_graph = nx.DiGraph()
        self.transitions_list = list()
        self.visited_states = list()

    def build_solution(self, state):
        graph = nx.reverse(self.states_graph)
        ancestors = [state]
        while True:
            edges = list(graph.edges(state))
            if len(edges) == 0:
                break
            state = list(edges[0])[1]
            ancestors.append(state)
        ancestors = ancestors[::-1]
        for i in range(len(ancestors) - 1):
            self.transitions_list.append(self.model.find_transition(list(ancestors[i]), list(ancestors[i + 1])))

    def pretty_print_solution(self):
        logging.info("SOLUTION FOUND: %s with algorithm bfs" % self.solution_found)
        logging.info(f"n = {self.model.capacities[0]}; m = {self.model.capacities[1]}; k = {self.model.k}")
        dict_data = ProblemModel.name_mapper
        for tr in self.transitions_list:
            from_state = [i for i in dict_data if dict_data[i] == tr[0]]
            to_state = [i for i in dict_data if dict_data[i] == tr[1]]
            logging.info("-> Moving water from %s to %s" % (from_state[0], to_state[0]))

    def bfs_recursive(self, parents):
        new_parents = list()

        for parent in parents:
            for transition in self.model.get_transitions(parent):
                child = tuple(self.model.do_transition(parent, transition))
                if child in self.visited_states:
                    continue
                self.states_graph.add_edge(tuple(parent), tuple(child))

                if self.model.is_final(child):
                    self.solution_found = True
                    self.build_solution(child)
                    return

                new_parents.append(child)
                self.visited_states.append(child)
        if len(new_parents) > 0:
            self.bfs_recursive(new_parents)

    def run(self):
        state = self.model.init()
        root_state_array = list()
        root_state_array.append(state)
        self.visited_states.append(tuple(state))
        self.bfs_recursive(root_state_array)
