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


    def __init__(self, n, m) -> None:
        if n > m:
            n, m = m, n
        
        self.capacities = {
            ProblemModel.FIRST_JUG: n,
            ProblemModel.SECOND_JUG: m
        }
    

    def init(self):
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
        if tr[0] == ProblemModel.TAP:
            state[tr[1]] = self.capacities[tr[1]]
            return state
        if tr[1] == ProblemModel.GROUND:
            state[tr[0]] = 0
            return state

        from_jug = max(0, state[tr[1]] + state[tr[0]] - self.capacities[tr[1]])
        state[tr[1]] = min(self.capacities[state[tr[1]]], state[tr[1]] + state[tr[0]])
        state[tr[0]] = from_jug
        return state


    def is_final(self, state):
        return state[0] == k or state[1] == k

class BktAlgorithm:
    def __init__(self, model) -> None:
        self.model = model
        self.before_state = dict()
        self.before_transition = dict()
        self.marked_states = set()
        self.tr_list = list()

    def build_solution(self, state):
        while state in self.before_state:
            self.tr_list.append(self.before_transition[state])
            state = self.before_state[state]
        self.tr_list = self.tr_list[::-1]

    def pretty_print_solution(self):
        for tr in self.tr_list:
            from_index =  ProblemModel.name_mapper.index(tr[0])
            to_index =  ProblemModel.name_mapper.index(tr[1])
            print("Moving water from %s to %s" % (ProblemModel.name_mapper[from_index], ProblemModel.name_mapper[to_index]))

    def __bkt__(self, state):
        if self.model.is_final(state):
            self.solution_found = True
            self.build_solution(state)
            return

        self.marked_states.add(tuple(state))
        for transition in self.model.get_transitions(state):
            next_state = self.model.do_transition(state, transition)
            if tuple(next_state) not in self.marked_states:
                self.before_state[tuple(next_state)] = state
                self.before_transition[tuple(next_state)] = transition
                self.__bkt__(next_state)
                if self.solution_found is True:
                    return

    def bkt(self):
        state = self.model.init()
        self.solution_found = False
        self.__bkt__(state = state)
    
def main():
    n = 3
    m = 5
    model = ProblemModel(n=n, m=m)
    algorithm = BktAlgorithm(model=model)
    algorithm.bkt()
    algorithm.pretty_print_solution()


if __name__ == "__main__":
    n = 3
    m = 5
    k = 2
    if n > m:
        n, m = m, n
    main()
