x=10
class Test():

    def __init__(self):
        self.lst=[]
        #self.lastval=0
        for _ in range(x):
            self.lst.append(_)
    def addtest(self,val):
        self.lst[9]=val
        self.lastval=self.lst[9]
    def functest(self):
        return self.lastval+1



p=Test()
print(p.lst)
p.addtest(100)
print(p.lst)
print(p.lastval)
p.addtest(200)
print(p.lst)
print(p.functest())
print(p.lst)
print("********")

def localvar():
    global p
    p=Test()
    print(p.lst)
localvar()
print("********")
print(p.lst)