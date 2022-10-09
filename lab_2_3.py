
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
        if (state[jug] !=  capacities[jug]):
            tr_list.append([TAP, jug])
        if (state[jug] != 0):
            tr_list.append([jug, GROUND])
            other_jug = MAX_JUG - jug
            if (state[other_jug] != capacities[other_jug]):
                tr_list.append([jug, other_jug])
    return tr_list

def do_transition(state, tr):
    if (tr[0] == TAP):
        state[tr[1]] = capacities[tr[1]]
        return state
    if (tr[1] == GROUND):
        state[tr[0]] = 0
        return state

    from_jug  = max(0, state[tr[1]] + state[tr[0]] - capacities[tr[1]])
    state[tr[1]] = min(capacities[state[tr[1]]], state[tr[1]] + state[tr[0]])
    state[tr[0]] = from_jug
    return state

def is_final(state):
    return state[0] == k or state[1] == k

def main():
    pass

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
    main()