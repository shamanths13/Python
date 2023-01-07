points=10
graph_y=50
class Data:
    def __init__(self,read,buff):
        self.read = read
        self.buff=buff
        self.rate=243
        self.data=[0]
        for _ in range(1, points):
            self.data.append(0)

        self.data_limit=[read]
        for _ in range(1, points):
            self.data_limit.append(read)
        self.data_limit[1]=self.read - self.buff
        self.data_limit[2]=self.read + self.buff
    
    def log(self, avg):
        for _ in range(0, points-1):
            self.data_limit[_]=self.data_limit[_+1]
        self.data_limit[points-1] = avg

        self.l = min(self.data_limit) - self.buff
        self.u = max(self.data_limit) + self.buff

        for _ in range(0, points):
            self.red = ((graph_y-1) / (self.u - self.l)) * (self.data_limit[_] - self.l)
            self.r = round(self.red)
            self.data_list[_]=self.r

        if self.data_limit[points-1] is max(self.data_limit):
            self.rate=0
        elif self.data_limit[points-1] is min(self.data_limit):
            self.rate=1
        elif self.data_limit[points-1] > self.data_limit[points-2]:
            self.rate=2
        elif self.data_limit[points-1] < self.data_limit[points-2]:
            self.rate=3
        else:
            self.rate=243

class Graph:
    pass



pread=100
p=Data(pread)
