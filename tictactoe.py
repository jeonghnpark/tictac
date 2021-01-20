import numpy as np
import pickle
import os.path

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
        with open('all_states.bin','rb') as f:
            return pickle.load(f)
    else:
        state = State()
        hash_value = state.hash()
        all_states = dict()
        all_states[hash_value] = (state, state.is_end())  # is_end()에서  winner와 end 여부를 결정
        symbol = 1
        get_all_states_impl(state, symbol, all_states, print_status=True)


class Player:
    def __init__(self,step_size=0.1, epsilon=0.1):
        #step_size, epsilon, estimation, 경험하는 states와 greedy 여부, symbol정의
        self.estimations=dict()
        self.step_size=step_size
        self.epsilon=epsilon
        self.states=[]
        self.greedy=[]
        self.symbol=None

    def reset(self):
        #stetes, greedy 재초기화
        self.states=[]
        self.greedy=[]
        # pass

    def set_state(self,state):
        self.states.append(state)
        self.greedy.append(True)
        #state와 greedy(디폴트 T)를 추가
        # pass

    def set_symbol(self,symbol):
        #symbol을 초기화, value를 초기화, win=1, lose 0, tie or undetermined 0.5
        self.symbol=symbol # TODO __init__으로 보내면?
        for state in all:
            pass
        # pass

    def backup(self):
        #한 게임이 끝난후에 greedy move 에 대해서 td update
        pass
    def act(self):
        #가능한 포지션과 state를 구하고 epsilon확률로 탐험함. greedy여부를 결정하고
        #[[i,j],T/F] 형태의 action 을 리턴함.
        pass
    def save_policy(self):
        #value 함수 저장
        pass
    def load_policy(self):
        #value 함수 로드
        pass

file=open('all_states.bin','rb')
all=pickle.load(file)

# print(len(all))
a=State()
a.data=np.array([[1,1,1],[0,-1,1],[1,0,1]])
a.print_state()





