FIRST_JUG = 0
SECOND_JUG = 1
MAX_JUG = 1
TAP = 2
GROUND = 3


def init():
    """
    state[0] = first jug current amount
    state[1] = second jug current amount
    """
    return [0, 0]


def get_transitions(state):
    """
    tr[0] = from which source
    tr[1] = to which source
    """
    tr_list = []
    for jug in capacities.keys():
        if state[jug] != capacities[jug]:
            tr_list.append([TAP, jug])
        if state[jug] != 0:
            tr_list.append([jug, GROUND])
            other_jug = MAX_JUG - jug
            if state[other_jug] != capacities[other_jug]:
                tr_list.append([jug, other_jug])
    return tr_list


def do_transition(state, tr):
    if tr[0] == TAP:
        state[tr[1]] = capacities[tr[1]]
        return state
    if tr[1] == GROUND:
        state[tr[0]] = 0
        return state

    from_jug = max(0, state[tr[1]] + state[tr[0]] - capacities[tr[1]])
    state[tr[1]] = min(capacities[state[tr[1]]], state[tr[1]] + state[tr[0]])
    state[tr[0]] = from_jug
    return state


def is_final(state):
    return state[0] == k or state[1] == k


def build_solution(state):
    tr_list = []
    while state in before_state:
        tr_list.append(state)
        state = before_state[state]
    else:
        tr_list.append(state)
    state_list = tr_list[::-1]
    for tr in tr_list:
        print("")


def bkt(state):
    global solution_found
    if is_final(state):
        solution_found = True
        build_solution(state)
        return

    marked_states.add(state)
    for transition in get_transitions(state):
        next_state = do_transition(state, transition)
        if next_state not in marked_states:
            before_state[next_state] = state
            bkt(next_state)
            if solution_found is True:
                return


def main():
    bkt(init())


if __name__ == "__main__":
    n = 3
    m = 5
    k = 2
    if n > m:
        n, m = m, n
    capacities = {
        FIRST_JUG: n,
        SECOND_JUG: m
    }
    marked_states = set()
    before_state = {}
    solution_found = False

    main()
