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
        for jug in self.capacities.keys():
            other_jug = ProblemModel.MAX_JUG - jug
            if state_from[jug] == state_to[jug]:
                if state_to[other_jug] == self.capacities[other_jug]:
                    return [ProblemModel.TAP, other_jug]
                elif state_to[other_jug] == 0:
                    return [other_jug, ProblemModel.GROUND]
            if (state_from[jug] > state_to[jug] and
                    state_from[jug] - state_to[jug] == state_to[other_jug] - state_from[other_jug]):
                return [jug, other_jug]
            elif (state_from[jug] < state_to[jug] and
                  state_to[jug] - state_from[jug] == state_from[other_jug] - state_to[other_jug]):
                return [other_jug, jug]
        return None

    def is_final(self, state):
        return state[0] == self.k or state[1] == self.k
