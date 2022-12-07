from collections import defaultdict
from random import random

FAIL_REWARD = -100
STANDARD_REWARD = -1
WIN_REWARD = 100
NR_ROWS = 6
NR_COLS = 14

ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]

class Algorithm:
    def __init__(self, n, m, discount, learning_rate):
        self.n = n
        self.m = m
        self.discount = discount
        self.learning_rate = learning_rate
        self.data = defaultdict(lambda: dict())
        self.frequency = defaultdict(lambda: 0)
        self.n_episodes = 1000

    def is_possible(self, line, column, transition):
        next_state = [line, column]
        if transition == "UP":
            next_state[0] -= 1

        if transition == "DOWN":
            next_state[0] += 1

        if transition == "LEFT":
            next_state[1] -= 1

        if transition == "RIGHT":
            next_state[1] += 1

        if not (0 <= next_state[0] < n) or \
                not (0 <= next_state[1] < m):
            return False
        return True

    def do_transition(self, state, transition):
        next_state = list(state)
        if transition == "UP":
            next_state[0] -= 1

        if transition == "DOWN":
            next_state[0] += 1

        if transition == "LEFT":
            next_state[1] -= 1

        if transition == "RIGHT":
            next_state[1] += 1

        # if not (0 <= next_state[0] < n) or \
        #         not (0 <= next_state[1] < m):
        #     return None
        return tuple(next_state)

    def set_playground(self):
        for line_index in range(self.n):
            for column_index in range(self.m):
                for action in ACTIONS:
                    if not self.is_possible(line_index, column_index, action):
                        continue
                    self.data[(line_index, column_index)][action] = random.randint(0, 100)

    def run(self):
        for e in range(self.n_episodes):
            current_state = env.reset()
