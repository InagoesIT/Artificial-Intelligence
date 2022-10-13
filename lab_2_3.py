import random

import networkx as nx


class ProblemModel:
    FIRST_JUG = 0
    SECOND_JUG = 1
    MAX_JUG = 1
    TAP = 2
    GROUND = 3

    name_mapper = {
        "FIRST_JUG": 0,
        "SECOND_JUG": 1,
        "MAX_JUG": 1,
        "TAP": 2,
        "GROUND": 3
    }

    def __init__(self, n, m, k) -> None:
        if n > m:
            n, m = m, n

        self.capacities = {
            ProblemModel.FIRST_JUG: n,
            ProblemModel.SECOND_JUG: m
        }
        self.k = k

    @staticmethod
    def init():
        """
        state[0] = first jug current amount
        state[1] = second jug current amount
        """
        return [0, 0]

    def get_transitions(self, state):
        """
        tr[0] = from which source
        tr[1] = to which source
        """
        tr_list = []
        for jug in self.capacities.keys():
            if state[jug] != self.capacities[jug]:
                tr_list.append([ProblemModel.TAP, jug])
            if state[jug] != 0:
                tr_list.append([jug, ProblemModel.GROUND])
                other_jug = ProblemModel.MAX_JUG - jug
                if state[other_jug] != self.capacities[other_jug]:
                    tr_list.append([jug, other_jug])
        return tr_list

    def do_transition(self, state, tr):
        return_state = list(state)
        if tr[0] == ProblemModel.TAP:
            return_state[tr[1]] = self.capacities[tr[1]]
            return return_state
        if tr[1] == ProblemModel.GROUND:
            return_state[tr[0]] = 0
            return return_state

        return_state[tr[1]] = min(self.capacities[tr[1]], state[tr[1]] + state[tr[0]])
        return_state[tr[0]] = max(0, state[tr[1]] + state[tr[0]] - self.capacities[tr[1]])
        return return_state

    def find_transition(self, state_from, state_to):
        transition = []

        for jug in self.capacities.keys():
            other_jug = ProblemModel.MAX_JUG - jug
            if state_from[jug] == state_to[jug]:
                transition = [ProblemModel.TAP, other_jug]
                if state_to[other_jug] == 0:
                    transition = [other_jug, ProblemModel.GROUND]
                    break
                break

        if len(transition) != 0:
            return transition

        if (state_from[ProblemModel.FIRST_JUG] > state_to[ProblemModel.FIRST_JUG] and
                state_from[ProblemModel.SECOND_JUG] < state_to[ProblemModel.SECOND_JUG]):
            return [ProblemModel.FIRST_JUG, ProblemModel.SECOND_JUG]

        return [ProblemModel.SECOND_JUG, ProblemModel.FIRST_JUG]

    def is_final(self, state):
        return state[0] == self.k or state[1] == self.k


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
            print("Moving water from %s to %s" % (from_state[0], to_state[0]))

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
        print("SOLUTION FOUND:", self.solution_found)
        dict_data = ProblemModel.name_mapper
        for tr in self.transitions_list:
            from_state = [i for i in dict_data if dict_data[i] == tr[0]]
            to_state = [i for i in dict_data if dict_data[i] == tr[1]]
            print("-> Moving water from %s to %s" % (from_state[0], to_state[0]))

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


class Tester:
    def __init__(self, max_n, max_m, max_k, model_class, algorithm_class):
        self.max_n = max_n
        self.max_m = max_m
        self.max_k = max_k
        self.model_class = model_class
        self.algorithm_class = algorithm_class

    @staticmethod
    def gcd(a, b):
        while b != 0:
            r = a % b
            a = b
            b = r
        return a

    def run_test(self):
        actual_n = random.randint(1, self.max_n)
        actual_m = random.randint(1, self.max_m)
        actual_k = random.randint(1, min(actual_n, actual_m))
        must_pass = False
        if actual_k % Tester.gcd(actual_n, actual_m) == 0:
            must_pass = True

        model = self.model_class(n=actual_n, m=actual_m, k=actual_k)
        algorithm = self.algorithm_class(model=model)
        algorithm.run()

        print("Actual n: %d actual m: %d actual k: %d and must pass: %s" % (actual_n, actual_m, actual_k, must_pass))
        print("Solution found: %s" % algorithm.solution_found)
        assert must_pass == algorithm.solution_found


def main():
    for algorithm in [BktAlgorithm, BfsAlgorithm]:
        tester = Tester(max_n=20, max_m=20, max_k=10, model_class=ProblemModel, algorithm_class=algorithm)
        for i in range(200):
            tester.run_test()
            print()

if __name__ == "__main__":
    main()
