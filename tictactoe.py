import numpy as np
import pickle
import os.path
# import random

BOARD_ROWS = 3
BOARD_COLS = 3
BOARD_SIZE = BOARD_COLS * BOARD_ROWS

np.random.seed(42)


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



class Judger:
    def __init__(self, player1, player2):
        self.p1 = player1
        self.p2 = player2
        self.p1_symbol = 1
        self.p2_symbol = -1
        self.p1.set_symbol(self.p1_symbol)
        self.p2.set_symbol(self.p2_symbol)
        self.current_player = None
        self.current_state = State()

    def reset(self):
        """
        reset players' states and greedy
        """
        self.p1.reset()
        self.p2.reset()

    def alternate(self):
        '''yield each player alternatively'''
        while True:
            yield self.p1
            yield self.p2

    def play(self, print_state=False):
        """
        play one game until end
        :param print_state:
        :return: winner 1 or -1
        """
        alternator = self.alternate()
        self.reset()
        current_state = State()
        self.p1.set_state(current_state)
        self.p2.set_state(current_state)
        if print_state:
            current_state.print_state()
        while True:
            player = next(alternator)
            i, j, symbol = player.act()
            current_state = current_state.next_state(i, j, symbol)
            self.p1.set_state(current_state)
            self.p2.set_state(current_state)
            if print_state:
                current_state.print_state()
            if current_state.is_end():
                return current_state.winner


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
    def __init__(self, all_states, step_size=0.1, epsilon=0.1):
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
                # V(S_t) <- V(S_t)+alpha*(V(S_t+1)-V(S_t))
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

        if np.random.rand() < self.epsilon:
            select = np.random.randint(len(next_states_hash))
            self.greedy[-1] = False
            action = next_position[select]
            action.append(self.symbol)
            return action

        # greedy move
        values = []
        for hash_val, position in zip(next_states_hash, next_position):
            values.append((self.estimations[hash_val], position))

        np.random.shuffle(values)
        values.sort(key=lambda x: x[0], reverse=True)
        action = values[0][1]
        action.append(self.symbol)
        return action

    def save_policy(self):
        # value 함수 저장
        with open(f"policy_{'first' if self.symbol == 1 else 'second'}.bin", 'wb') as f:
            pickle.dump(self.estimations, f)

    def load_policy(self):
        # value 함수 로드
        with open(f"policy_{'first' if self.symbol == 1 else 'second'}.bin", 'rb') as f:
            self.estimations = pickle.load(f)


class HumanPlayer:
    def __init__(self, **kwargs):
        self.symbol = None
        self.keys = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']
        self.state = None

    def reset(self):
        pass

    def set_state(self, state):
        self.state = state

    def set_symbol(self, symbol):
        self.symbol = symbol

    def act(self):
        self.state.print_state()
        key = input("Input your position")
        data = self.keys.index(key)
        i = data // BOARD_COLS
        j = data % BOARD_COLS
        return i, j, self.symbol


def train(epochs, print_every=500):
    p1 = Player(step_size=0.1, epsilon=0.01, all_states=all_states)
    p2 = Player(step_size=0.1, epsilon=0.01, all_states=all_states)
    judger = Judger(p1, p2)  # symbol is set in Judger.__init__()
    win_cnt1 = 0
    win_cnt2 = 0

    for i in range(1,epochs+1):
        p1.reset()
        p2.reset()
        winner = judger.play(print_state=False)
        if winner == 1:
            win_cnt1 += 1
        elif winner == -1:
            win_cnt2 += 1

        if i % print_every == 0:
            print(f'epoch {i}, player1 win rate={win_cnt1 / (i):.2f}, player2 win rate={win_cnt2 / (i):.2f}')
        p1.backup()
        p2.backup()

    p1.save_policy()
    p2.save_policy()


def compete(turns):
    p1 = Player(epsilon=0, all_states=all_states)  # epsilon=0 always greedy move
    p2 = Player(epsilon=0, all_states=all_states)

    judger = Judger(p1, p2)  # symbol is set in Judger.__init__()
    p1.load_policy()
    p2.load_policy()

    win_cnt1 = 0
    win_cnt2 = 0

    for i in range(turns):
        p1.reset()  # judge can be modified externally !!
        p2.reset()
        winner = judger.play(print_state=False)
        if winner == 1:
            win_cnt1 += 1
        elif winner == -1:
            win_cnt2 += 1
    print(f"{turns} turns, player1 rate ={win_cnt1 / turns}, player2 rate={win_cnt2 / turns}")


def play():
    """
    human vs machine
    :return:
    """
    pass


import os.path


if __name__ == "__main__":

    all_states = dict()
    if os.path.isfile("all_states.bin"):
        with open("all_states.bin", 'rb') as f:
            all_states = pickle.load(f)
    else:
        get_all_states()
        with open("all_states.bin", 'wb') as f:
            pickle.dump(all_states, f)

    train(int(100000), print_every=500)
    # compete(int(1e3))
