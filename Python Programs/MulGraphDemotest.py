import matplotlib.pyplot as plt 


fig, host = plt.subplots(figsize=(9,6))
    
par1 = host.twinx()
par2 = host.twinx()
    
host.set_xlabel("Time")
host.set_ylabel("Humidity")
par1.set_ylabel("Temperature")
par2.set_ylabel("Pressure")

color1 = plt.cm.viridis(0)
color2 = plt.cm.viridis(0.5)
color3 = plt.cm.viridis(.9)

par2.spines['left'].set_position(('outward', 50))
par2.yaxis.set_ticks_position('left')
par2.yaxis.set_label_position('left')

par1.spines['left'].set_position(('outward', 110))
par1.yaxis.set_ticks_position('left')
par1.yaxis.set_label_position('left')

host.yaxis.label.set_color(color1)
par1.yaxis.label.set_color(color2)
par2.yaxis.label.set_color(color3)

h,= host.plot([10, 11, 12,13],    color=color1, label="Humidity")
t,= par1.plot([10,13, 12,11],    color=color2, label="Temperature")
p,= par2.plot([90950, 90330, 90715,90420], color=color3, label="Pressure")
plt.show()

