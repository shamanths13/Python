import serial
import matplotlib.pyplot as plt
import numpy as np
import time

plt.close('all')
plt.figure()
plt.ion()
plt.show()
plt.xlabel("Angle")
plt.ylabel("Magnitude")
plt.title("Sine and Cosine functions")


i=0

s=serial.Serial('COM3',9600)


n=0
x=1
p=np.array([])
h=np.array([])
t=np.array([])
pos=np.array([])
for n in range(0,10):
            p=np.append(p,0)
            t=np.append(t,0)
            h=np.append(h,0)
            pos=np.append(pos,9-n)
pos=np.array(pos,dtype=np.int16)
print(pos)

pos_cur=9
      
while True:

    reads=s.readline()
    pos_cur=int(reads.decode())
    print(pos_cur)
    pos_p=np.where(pos==pos_cur)
    iters=pos_p[0][0]+1
#    print(pos_p)
    print(iters)
    iters_a=30-((iters)*3)
    print(iters_a)
#    time.sleep(2)
   
    while iters > 0:
        iters=iters-1
        pos_mem=pos[0]
        for n in range(0,9):
            p[n]=p[n+1]
            t[n]=t[n+1]
            h[n]=h[n+1]
            pos[n]=pos[n+1]
        pos[9]=pos_mem
            
        read=s.readline()
        p[9]=float(read.decode())
        read=s.readline()
        t[9]=float(read.decode())
        read=s.readline()
        h[9]=float(read.decode())
    
    for n in range(0,iters_a):
        reads=s.readline()

    print(p)
    print(t)
    print(h)
    time.sleep(0.1)

''' 
    data=np.append(data,b)
    plt.cla()
    plt.plot(data)
    plt.show()
    plt.pause(1)

'''    
