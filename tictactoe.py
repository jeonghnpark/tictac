import numpy as np
import pickle
import os.path
import random

BOARD_ROWS = 3
BOARD_COLS = 3
BOARD_SIZE = BOARD_COLS * BOARD_ROWS

random.seed(42)


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

    def print_state(self):
        print('--------')
        for i in range(BOARD_ROWS):
            str = " "
            for j in range(BOARD_COLS):
                if self.data[i, j] == 1:
                    str += "  1 "
                elif self.data[i, j] == -1:
                    str += " -1 "
            print(str)


class Player:
    def __init__(self, symbol, epsilon=0.01):
        self.symbol = symbol
        self.states = []  # list that saves history of player's states
        self.greedy = []  # list that saves history of its moves
        self.epsilon = epsilon
        self.estimation = dict()

    def act(self):
        # return action, the next moving position (i,j), a tuple
        state = self.states[-1]
        next_states = []  # hash values of possible next states
        next_positions = []  # possible next position
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if state.data[i, j] == 0:
                    pass


def get_all_states_impl(state, symbol, all_states, print_status=False):
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if print_status:
                print(f'{i}{j}')
            if state.data[i, j] == 0:
                new_state = state.next_state(i, j, symbol)
                is_end = new_state.is_end()
                all_states[new_state.hash()] = (new_state, is_end)
                if not is_end:
                    get_all_states_impl(new_state, -symbol, all_states)


def get_all_states():
    # pass
    if os.path.isfile('all_states.bin'):
        with open('all_states.bin', 'rb') as f:
            return pickle.load(f)
    else:
        state = State()
        hash_value = state.hash()
        # all_states = dict()
        all_states[hash_value] = (state, state.is_end())  # is_end()에서  winner와 end 여부를 결정
        symbol = 1
        get_all_states_impl(state, symbol, all_states, print_status=True)


class Player:
    def __init__(self, step_size=0.1, epsilon=0.1):
        # step_size, epsilon, estimation, 경험하는 states와 greedy 여부, symbol정의
        self.estimations = dict()
        self.step_size = step_size
        self.epsilon = epsilon
        self.states = []  # list of states the player has experienced so far
        self.greedy = []
        self.symbol = None

    def reset(self):
        # stetes, greedy 재초기화
        self.states = []
        self.greedy = []
        # pass

    def set_state(self, state):
        self.states.append(state)
        self.greedy.append(True)
        # state와 greedy(디폴트 T)를 추가
        # pass

    def set_symbol(self, symbol):
        # symbol을 초기화, value를 초기화, all_states들의  win-lose초기화 win=1, lose 0, tie or undetermined 0.5
        self.symbol = symbol  # TODO __init__으로 보내면? => 안됨,  winner를 초기화 하는데 쓰임
        for hash_key in all_states:
            state, is_end = all_states[hash_key]
            if is_end:
                if state.winner == symbol:
                    self.estimations[hash_key] = 1.0
                elif state.winner == -symbol:
                    self.estimations[hash_key] = 0.0
                else:
                    self.estimations[hash_key] = 0.5
            else:
                self.estimations[hash_key] = 0.5

    def backup(self):
        # 한 게임이 끝난후에 greedy move 에 대해서 td update
        hashes = [state.hash() for state in self.states]
        for i in reversed(range(len(hashes) - 1)):
            if self.greedy[i]:
                self.estimations[hashes[i]] += self.step_size * (
                        self.estimations[hashes[i + 1]] - self.estimations[hashes[i]])

    def act(self):
        # 최근 상태에서 가능한 다음 포지션과 state를 구하고 epsilon확률로 탐험함. greedy여부를 결정하고
        # [[i,j],T/F] 형태의 action 을 리턴함.
        recent_state = self.states[-1]
        next_states_hash = []
        next_position = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if recent_state.data[i, j] == 0:
                    next_states_hash.append(recent_state.next_state(i, j, self.symbol).hash())
                    next_position.append([i, j])

        if np.random.randn() < self.epsilon:
            select = random.randint(0,len(next_states_hash)-1)
            self.greedy[-1] = False
            action=next_position[select]
            action.append(self.symbol)
            return action

        #greedy move
        values=[]
        for next_state_hash, position in zip(next_states_hash,next_position):
            values.append((self.estimations[next_state_hash],next_position))

        np.random.shuffle(values)
        values.sort(key=lambda x:x[0],reverse=True)
        action=values[0][1]
        action.append(self.symbol)
        return action




    def save_policy(self):
        # value 함수 저장
        pass

    def load_policy(self):
        # value 함수 로드
        pass


import os.path

all_states = dict()
if os.path.isfile("all_states.bin"):
    with open("all_states.bin", 'rb') as f:
        all_states = pickle.load(f)
else:
    get_all_states()
    with open("all_states.bin", 'wb') as f:
        pickle.dump(all_states, f)

# file=open('all_states.bin','rb')
# all=pickle.load(file)

# print(len(all))
# a=State()
# a.data=np.array([[1,1,1],[0,-1,1],[1,0,1]])
# a.print_state()
