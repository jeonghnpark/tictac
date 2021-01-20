import numpy as np
import pickle

BOARD_ROWS = 3
BOARD_COLS = 3
BOARD_SIZE = BOARD_COLS * BOARD_ROWS


class State:
    def __init__(self):
        self.end = None
        self.data = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.hash_value = None
        self.winner = None

    def hash(self):
        self.hash_value = 0
        for x in np.nditer(self.data):
            self.hash_value = self.hash_value * 3 + x + 1
        return self.hash_value

    def is_end(self):
        if self.end is not None:
            return self.end

        results = []  # row, col, diag, anti-diag
        for i in range(BOARD_ROWS):
            results.append(np.sum(self.data[i, :]))
        for i in range(BOARD_COLS):
            results.append(np.sum(self.data[:, i]))
        diag = 0
        for i in range(BOARD_ROWS):
            diag += self.data[i, i]
        results.append(diag)

        anti_diag = 0
        for i in range(BOARD_ROWS):
            anti_diag += self.data[i, BOARD_COLS - 1 - i]
        results.append(anti_diag)

        for result in results:
            if result == 3:
                self.end = True
                self.winner = 1
                return self.end
            if result == -3:
                self.end = True
                self.winner = -1
                return self.end

        # 게임이 비김으로 끝났을때는 self.end=1, self.winner=0
        # 게임이 끝나지 않았을때 self.end=0, self.winner=None
        if np.sum(np.abs(self.data)) == BOARD_SIZE:
            self.end = True
            self.winner = 0
            return self.end
        # else:
        #     self.end=False
        #     return self.end =>  이렇게 해도 되지만 return이 컴파일 타임에 결정 x

        self.end = False
        return self.end

    def next_state(self, i, j, symbol):
        new_state = State()
        new_state.data = np.copy(self.data)
        new_state.data[i, j] = symbol
        # TODO hash value를 업데이트 하지 않아도 되나?
        new_state.hash()
        return new_state


class Player:
    def __init__(self, symbol, epsilon=0.01):
        self.symbol = symbol
        self.states = []  # list that saves history of player's states
        self.greedy = []  # list that saves history of its moves
        self.epsilon = epsilon

    def act(self):
        # return action, the next moving position (i,j), a tuple
        state = self.states[-1]
        next_states = []  # hash values of possible next states
        next_positions = []  # possible next position
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if state.data[i, j] == 0:
                    pass


all_states = []


def get_all_states_impl(state, symbol):
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            # print(f'{i}{j}')
            if state.data[i, j] == 0:
                # next_hash = state.hash_value * 3 + symbol + 1
                # if next_hash not in all_states:
                #     print('new state found')
                new_state = state.next_state(i, j, symbol)
                all_states.append(new_state.hash())
                if new_state.is_end():
                    return
                else:
                    get_all_states_impl(new_state, -symbol)


def get_all_states():
    state = State()
    all_states.append(state.hash())
    symbol = 1
    get_all_states_impl(state, symbol)


astate = State()

s = np.array([[1, 0, 1], [-1, 0, -1], [1, 1, -1]])
astate.data = s

# print(f"End?{astate.is_end()}, Winner{astate.winner}")

get_all_states()

print(len(all_states))
import math

print(f'{len(all_states)} of {math.factorial(9)}(9!) are ended before 9 moves')

all_states_unique = set(all_states)
print(len(all_states_unique))
