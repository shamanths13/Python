import matplotlib.pyplot as plt 

# Create figure and subplot manually
fig = plt.figure()
host = fig.add_subplot(111)

# More versatile wrapper
#fig, host = plt.subplots(figsize=(8,5)) # (width, height) in inches
# (see https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.pyplot.subplots.html)
    
par1 = host.twinx()
par2 = host.twinx()
    
#host.set_xlim(0, 2)
#host.set_ylim(0, 3)
#par1.set_ylim(0, 4)
#par2.set_ylim(1, 65)
    
host.set_xlabel("Time")
host.set_ylabel("Humidity")
par1.set_ylabel("Temperature")
par2.set_ylabel("Pressure")

color1 = plt.cm.plasma(0.1)
color2 = plt.cm.viridis(0.7)
color3 = plt.cm.inferno(0.5)

h,= host.plot([0, 1, 2,3],    color=color1, label="Humidity")
t,= par1.plot([0, 3, 2,1],    color=color2, label="Temperature")
p,= par2.plot([50, 30, 15,20], color=color3, label="Pressure")

#lns = [p1, p2, p3]
#host.legend(handles=lns, loc='best')

# right, left, top, bottom
par2.spines['left'].set_position(('outward', 50))

# no x-ticks                 
#par2.xaxis.set_ticks([])

# Sometimes handy, same for xaxis
par2.yaxis.set_ticks_position('left')

# Move "Velocity"-axis to the left
# par2.spines['left'].set_position(('outward', 60))
# par2.spines['left'].set_visible(True)
par2.yaxis.set_label_position('left')
# par2.yaxis.set_ticks_position('left')

par1.spines['left'].set_position(('outward', 100))
par1.yaxis.set_ticks_position('left')
par1.yaxis.set_label_position('left')


host.yaxis.label.set_color(h.get_color())
par1.yaxis.label.set_color(t.get_color())
par2.yaxis.label.set_color(p.get_color())

