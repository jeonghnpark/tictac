class Judger:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def change(self):
        self.p1.epsilon=0.001
        self.p2.epsilon=0.001

    def print(self):
        self.p1.print_epsilon()
        self.p2.print_epsilon()


class Player:
    def __init__(self, epsilon=0.1):
        self.epsilon=0.01
    def print_epsilon(self):
        print(self.epsilon)

# p1, p2 = 1, 2
p1=Player()
p2=Player()

j1 = Judger(p1, p2)
j1.print()
j1.change()
j1.print()

#try to edit p1, p2 externally
p1.epsilon=0.02
p2.epsilon=0.02

j1.print()
print("member class can be modified externally")


class Judger_int:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def change(self):
        self.p1=0.001
        self.p2=0.001

    def print(self):
        print(self.p1,self.p2)

p1,p2=1,2
j=Judger_int(p1,p2)
j.print()
j.change()
j.print()
p1=0.07
p2=0.07
j.print()
print("멤버 변수가 python native 인 경우는 깊은복사")


# j1.change()
# j1.p1, j1.p2= 7,8
# j1.print()


