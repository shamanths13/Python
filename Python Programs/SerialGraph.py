import serial
import matplotlib.pyplot as plt
import numpy as np
import time

color1 = plt.cm.plasma(0)
color2 = plt.cm.viridis(0.7)
color3 = plt.cm.inferno(0.5)

def display_graph():
    fig, host = plt.subplots(figsize=(9,6))
        
    par1 = host.twinx()
    par2 = host.twinx()
        
    host.set_xlabel("Time(Scale= 1::10 min)")
    host.set_ylabel("Humidity %RH")
    par1.set_ylabel("Temperature °C")
    par2.set_ylabel("Pressure Pa")    

    par2.spines['left'].set_position(('outward', 60))
    par2.yaxis.set_ticks_position('left')
    par2.yaxis.set_label_position('left')

    par1.spines['left'].set_position(('outward', 125))
    par1.yaxis.set_ticks_position('left')
    par1.yaxis.set_label_position('left')

    host.yaxis.label.set_color(color2)
    par1.yaxis.label.set_color(color3)
    par2.yaxis.label.set_color(color1)    
    h_p,= host.plot(h, color=color2, label="Humidity")
    t_p,= par1.plot(t, color=color3, label="Temperature")
    p_p,= par2.plot(p, color=color1, label="Pressure")
    plt.show()

points=300
log_points=60


s=serial.Serial('COM3',9600)

n=0
p=np.array([])
h=np.array([])
t=np.array([])
reads=s.readline()
read=s.readline()
p_ini=int(read.decode())
read=s.readline()
t_ini=round(float(read.decode()),2)
read=s.readline()
h_ini=round(float(read.decode()),2)
for n in range(0,((log_points*3)-3)):
    reads=s.readline()

for n in range(0,points):
            p=np.append(p,p_ini)
            t=np.append(t,t_ini)
            h=np.append(h,h_ini)
pos=np.array([])
for n in range(0,log_points):
            pos=np.append(pos,((log_points-1)-n))
pos=np.array(pos,dtype=np.int16)


while True:

    reads=s.readline()
    pos_cur=int(reads.decode())
    pos_p=np.where(pos==pos_cur)
    iters=pos_p[0][0]+1
    iters_a=(log_points*3)-((iters)*3)
   
    while iters > 0:
        iters=iters-1
        pos_mem=pos[0]
        for n in range(0,points-1):
            p[n]=p[n+1]
            t[n]=t[n+1]
            h[n]=h[n+1]
        for n in range(0,(log_points-1)):
            pos[n]=pos[n+1]
        pos[log_points-1]=pos_mem
            
        read=s.readline()
        p[points-1]=int(read.decode())
        read=s.readline()
        t[points-1]=round(float(read.decode()),2)
        read=s.readline()
        h[points-1]=round(float(read.decode()),2)
    
    for n in range(0,iters_a):
        reads=s.readline()    
    print(p[points-1]," Pa")
    print(h[points-1]," %")
    print(t[points-1]," C")
    display_graph()
    
    time.sleep(1)
