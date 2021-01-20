
def edit_list(l):
    l.append(3)

lis=[1,2,3,4]
print(f'before {lis}')
edit_list(lis)
print(f'after {lis}')

def edit_int(a):
    a=6

a=4
print(f"before a={a}")
edit_int(a)
print(f"after a={a}")

class ref_cls:
    def __init__(self):
        self.a=3
        self.b=4

a=ref_cls()
print(f"before a.a {a.a}")

def edit_cls(cl):
    cl.a=33

edit_cls(a)
print(f"after a.a {a.a}")



