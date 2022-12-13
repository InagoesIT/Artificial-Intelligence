import random
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy
import numpy as np

ABSOLUTE_MINIMUM = -100_000

FINAL_STATE_VALUE = 100

INSIDE_PLAYGROUND_VALUE = -1

OUTSIDE_PLAYGROUND_VALUE = -100

FAIL_REWARD = -100
STANDARD_REWARD = -1
WIN_REWARD = 100
NR_ROWS = 6
NR_COLS = 14

ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]


class Algorithm:
    delta_line = [-1, 0, 1, 0]
    delta_column = [0, 1, 0, -1]

    def __init__(self, n, m, discount, learning_rate):
        self.n = n
        self.m = m
        self.discount = discount
        self.learning_rate = learning_rate
        self.q = defaultdict(lambda: dict())

        self.frequency = defaultdict(lambda: 0)
        self.n_episodes = 100
        self.eps = 0
        self.reward = dict()
        self.episodes_rewards = list()
        self.episodes_indexes = list()
        self.before_state = dict()
        self.episodes_paths = list()

    def is_possible(self, line, column, transition):
        pass

    def do_transition(self, current_state, action) -> tuple[int, int]:
        next_state = list(current_state)
        if action == "UP":
            next_state[0] -= 1

        if action == "DOWN":
            next_state[0] += 1

        if action == "LEFT":
            next_state[1] -= 1

        if action == "RIGHT":
            next_state[1] += 1
        return tuple(next_state)

    def is_acceptable_state(self, line_index, column_index):
        if line_index == 0 or line_index == self.n + 1:
            return False
        if column_index == 0 or column_index == self.m + 1:
            return False

        if line_index == self.n and 2 <= column_index <= self.m - 1:
            return False
        return True

    def set_playground(self):
        for line_index in range(self.n + 2):
            for column_index in range(self.m + 2):
                for action in ACTIONS:
                    self.q[(line_index, column_index)][action] = random.randint(0, 100)
                    if self.is_acceptable_state(line_index, column_index):
                        self.reward[line_index, column_index] = INSIDE_PLAYGROUND_VALUE
                    else:
                        self.reward[line_index, column_index] = OUTSIDE_PLAYGROUND_VALUE
        self.reward[self.n, self.m] = FINAL_STATE_VALUE

    def get_initial_state(self) -> tuple[int, int]:
        return self.n, 1

    def is_final(self, state: tuple[int, int]) -> bool:
        return state[0] == self.n and state[1] == self.m

    def get_best_q_from_state(self, state):
        max_value = ABSOLUTE_MINIMUM
        for action in self.q[state]:
            if self.q[state][action] > max_value:
                max_value = self.q[state][action]
        return max_value

    def argmax_action(self, state):
        best_action = None
        best_value = ABSOLUTE_MINIMUM
        for action in self.q[state]:
            if self.q[state][action] > best_value:
                best_value = self.q[state][action]
                best_action = action

        if best_action is None:
            raise Exception("Best action not found")
        return best_action

    def get_random_action(self, state):
        choice_list = list(self.q[state].keys())
        choice_size = len(choice_list)
        choice_index = random.randint(0, choice_size - 1)
        return choice_list[choice_index]

    def run(self):
        self.episodes_rewards = list()
        self.episodes_indexes = list()
        for e in range(self.n_episodes):
            self.episodes_indexes.append(e)
            episode_reward = 0
            is_solution_found = False
            episode_path = []
            while not is_solution_found:
                current_state = self.get_initial_state()
                self.before_state = dict()
                episode_path = [current_state]
                while True:
                    if np.random.uniform(0, 1) < self.eps:
                        action = self.get_random_action(state=current_state)
                    else:
                        action = self.argmax_action(state=current_state)

                    next_state = self.do_transition(current_state=current_state, action=action)
                    episode_path.append(next_state)
                    reward = self.reward[next_state]

                    best_next_action = self.argmax_action(state=next_state)
                    best_next_q = self.q[next_state][best_next_action]

                    self.q[current_state][action] += self.learning_rate * (
                                reward + self.discount * best_next_q - self.q[current_state][action])

                    episode_reward += reward

                    if self.eps > 0.1:
                        self.eps -= 0.05

                    if reward == -100:
                        break
                    self.before_state[next_state] = current_state
                    if self.is_final(state=next_state):
                        is_solution_found = True
                        break
                    current_state = next_state
            # self.episodes_paths.append(self.get_episode_path())
            self.episodes_paths.append(episode_path)
            self.episodes_rewards.append(episode_reward)

    def pretty_print_stats(self):
        for index, episode_path in enumerate(self.episodes_paths):
            print(episode_path)
            print(self.episodes_rewards[index])
        print(self.q)
        data = numpy.clip(self.episodes_rewards, -10, 10_000)
        plt.plot(self.episodes_indexes, data)
        plt.xlabel('Episode Index')
        plt.ylabel('Episode Reward')
        plt.title('Q-Learning Statistics')
        plt.show()
