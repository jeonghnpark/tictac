
class Parent:
    def __init__(self, p1,p2):
        self.p1=p1
        self.p2=p2

class Child(Parent):
    def __init__(self,c1,**kwargs):
        super().__init__(**kwargs)
        self.c1=c1
        self.c2="this is Child's c2"
        self.c3="this is child's c3"

child=Child(p1="this is Parent's p1",
            p2="this is parent's p2",
            c1="this is child's c1")

print(child.p1)
print(child.p2)
print(child.c1)
print(child.c2)
print(child.c3)
