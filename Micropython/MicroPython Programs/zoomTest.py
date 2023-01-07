from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
from ds3231 import DS3231_I2C
from bmp180 import BMP180
import framebuf
import utime
import math


i2c= I2C(0, scl=Pin(5), sda=Pin(4), freq=200000)
rtc=DS3231_I2C(i2c)
bmp180 = BMP180(i2c)
bmp180.oversample_sett = 3
bmp180.baseline = 101325
oled= SSD1306_I2C(128, 64, i2c)
led=Pin(25, Pin.OUT)
i=0
button_a=machine.Pin(16,machine.Pin.IN,machine.Pin.PULL_DOWN)
button_b=machine.Pin(17,machine.Pin.IN,machine.Pin.PULL_DOWN)
pot=ADC(28)
pot_lower=1000
pot_higher=64000

t=rtc.read_time()
print("Date:%02x/%02x/20%x" %(t[4],t[5],t[6]))
print("Time:%02x:%02x:%02x" %(t[2],t[1],t[0]))

graph_x=120
graph_y=50
log_freq=6#In Minutes(1,2,3,5,6,10)
grid_locxspace = round(60/log_freq)
grid_locxstartint = round(grid_locxspace/2)
log_counter=log_freq
n = 0
points = 240

graph_data=[0]
for n in range(1,points):
    graph_data.append(0)
for n in range(0,points):
    mark=n%grid_locxstartint
    if mark==0:
        graph_data[n]=1
for n in range(0,points):
    mark=n%grid_locxspace
    if mark==0:
        graph_data[n]=2
graph_data.append(2)
print(len(graph_data))
        
print(graph_data)

pot_value=pot.read_u16()
if pot_value < pot_lower:
    pot_value=pot_lower
if pot_value > pot_higher:
    pot_value=pot_higher
pot_red=((pot_value-pot_lower)/(pot_higher-pot_lower))*100
pot_red=round(pot_red)
#print(pot_red)

while True:
    oled.fill(0)
    pot_value=pot.read_u16()
    if pot_value < pot_lower:
        pot_value=pot_lower
    if pot_value > pot_higher:
        pot_value=pot_higher
    pot_red=((pot_value-pot_lower)/(pot_higher-pot_lower))*100
    pot_red=round(pot_red)
    pot_red=100-pot_red
    print(pot_red)
    if pot_red<53:
        pot_red=53
    for n in range(0,points+1):
        n_red=(n*pot_red)/100
        n_red=round(n_red)
#        print(n_red)
        if (127-n_red) < 0:
#            print("break")
            break
        if graph_data[n]==1:
            oled.pixel(127-n_red, 60, 1)
            oled.pixel(127-n_red, 3, 1)
        if graph_data[n]==2:
            oled.pixel(127-n_red, 63, 1)
            oled.pixel(127-n_red, 62, 1)
            oled.pixel(127-n_red, 61, 1)
            oled.pixel(127-n_red, 60, 1)
            oled.pixel(127-n_red, 0, 1)
            oled.pixel(127-n_red, 1, 1)
            oled.pixel(127-n_red, 2, 1)
            oled.pixel(127-n_red, 3, 1)
    oled.show()
    utime.sleep(0.1)

"""
pdata_list=[0]
for n in range(1, points):
    pdata_list.append(0)

p_a = math.floor(bmp180.pressure)
p_b = p_a % 1000
p_c =(p_a-p_b)/1000
p_d = round(p_c)

pdata_list_limit=[p_b]
for n in range(1, points):
    pdata_list_limit.append(p_b)
pdata_list_limit[1]=p_b-1
pdata_list_limit[2]=p_b+1
read_p = p_b

tdata_list=[0]
for n in range(1, points):
    tdata_list.append(0)

temp = round(bmp180.temperature,2)

tdata_list_limit=[temp]
for n in range(1, points):
    tdata_list_limit.append(temp)
tdata_list_limit[1]=temp-0.1
tdata_list_limit[2]=temp+0.1
read_t = temp

read_n = 1

min_prev=61
read=1
incr=0

def reading():
    global temp
    global p_b
    global p_d
    global t
    temp = round(bmp180.temperature,2)
    p_a = math.floor(bmp180.pressure)
    p_b = p_a % 1000
    p_c =(p_a-p_b)/1000
    p_d = round(p_c)
#    print("Read Time:%02x:%02x:%02x" %(t[2],t[1],t[0]))
    print("Temp:",temp)


def reading_log():

    global p_u
    global p_l
    global avg_p
    global read_p
    global pdata_list
    global pdata_list_limit
    global t_u
    global t_l
    global avg_t
    global read_t
    global tdata_list
    global tdata_list_limit
    global read_n
    global points
    global t

    avg_p=(read_p)/read_n
    avg_p=round(avg_p)
            
    for n in range(0, points-1):
        pdata_list_limit[n]=pdata_list_limit[n+1]
    pdata_list_limit[points-1] = avg_p
            
    p_l = min(pdata_list_limit)-1
    p_u = max(pdata_list_limit)+1    
               
    for n in range(0, points):
        red_pres = ((graph_y-1) / (p_u - p_l)) * (pdata_list_limit[n] - p_l)
        p_r = round(red_pres)
        pdata_list[n]=p_r
            
    avg_t=(read_t)/read_n
    avg_t=round(avg_t,2)
            
    for n in range(0, points-1):
        tdata_list_limit[n]=tdata_list_limit[n+1]
    tdata_list_limit[points-1] = avg_t
            
    t_l = min(tdata_list_limit)-0.01
    t_u = max(tdata_list_limit)+0.01    
               
    for n in range(0, points):
        red_temp = ((graph_y-1) / (t_u - t_l)) * (tdata_list_limit[n] - t_l)
        t_r = round(red_temp)
        tdata_list[n]=t_r
                
#    print("Log Time:%02x:%02x:%02x" %(t[2],t[1],t[0]))


def disp_pressure():
    global p_d
    global p_u
    global p_l
    global avg_p
    oled.fill(0)
    oled.text("Pressure Log",16,5)
    oled.text("Pmax: "+str(p_d)+"."+str(p_u)+" KPa",0,20)
    oled.text("Pmin: "+str(p_d)+"."+str(p_l)+" KPa",0,35)
    oled.text("Pnow: "+str(p_d)+"."+str(avg_p)+" KPa",0,50)
    oled.show()
    
    while True:
        utime.sleep(0.1)
        if button_a.value() == 1:
            break
    
    utime.sleep(0.2)
    global points
    global pdata_list
    global grid_locxspace
    global grid_locxstartint
    oled.fill(0)
    for n in range(0, points):
        oled.pixel(n+(128-points), 63-pdata_list[n]-7, 1)
    grid_locx = 127
    while grid_locx >=(128-points) :
        oled.pixel(grid_locx, 63, 1)
        oled.pixel(grid_locx, 62, 1)
        oled.pixel(grid_locx, 61, 1)
        oled.pixel(grid_locx, 60, 1)
        oled.pixel(grid_locx, 0, 1)
        oled.pixel(grid_locx, 1, 1)
        oled.pixel(grid_locx, 2, 1)
        oled.pixel(grid_locx, 3, 1)
        if (grid_locx-grid_locxstartint)>=(128-graph_x):
            oled.pixel(grid_locx-grid_locxstartint, 60, 1)
            oled.pixel(grid_locx-grid_locxstartint, 3, 1)
        grid_locx=grid_locx-grid_locxspace
    oled.show()
    
    while True:
        utime.sleep(0.1)
        if button_a.value() == 1:
            break


def disp_temp():
    global t_u
    global t_l
    global avg_t
    oled.fill(0)
    oled.text("Temperature Log",2,5)
    oled.text("Tmax : "+str(t_u)+" C",2,20)
    oled.text("Tmin : "+str(t_l)+" C",2,35)
    oled.text("Tnow : "+str(avg_t)+" C",2,50)
    oled.show()
    while True:
        utime.sleep(0.1)
        if button_b.value() == 1:
            break
        
    utime.sleep(0.2)
    global points
    global tdata_list
    global grid_locxspace
    global grid_locxstartint
    oled.fill(0)
    for n in range(0, points):
        oled.pixel(n+(128-points), 63-tdata_list[n]-7, 1)
    grid_locx = 127
    while grid_locx >=(128-points) :
        oled.pixel(grid_locx, 63, 1)
        oled.pixel(grid_locx, 62, 1)
        oled.pixel(grid_locx, 61, 1)
        oled.pixel(grid_locx, 60, 1)
        oled.pixel(grid_locx, 0, 1)
        oled.pixel(grid_locx, 1, 1)
        oled.pixel(grid_locx, 2, 1)
        oled.pixel(grid_locx, 3, 1)
        if (grid_locx-grid_locxstartint)>=(128-graph_x):
            oled.pixel(grid_locx-grid_locxstartint, 60, 1)
            oled.pixel(grid_locx-grid_locxstartint, 3, 1)
        grid_locx=grid_locx-grid_locxspace
    oled.show()
    
    while True:
        utime.sleep(0.1)
        if button_b.value() == 1:
            break

    
while True:
    t=rtc.read_time()
    min_str="%0x"%t[1]
    min_n=int(min_str)
    if min_n != min_prev:
        min_prev = min_n
        if log_counter==log_freq:
            reading_log()
            read_p=0
            read_t=0
            read_n=0
            log_counter=0
        log_counter=log_counter+1
        
    if (read == 1):
        reading()
        read_n=read_n + 1
        read_t=read_t + temp
        read_p=read_p + p_b
        read=0
        
    t=rtc.read_time()
    ichkstr="%0x"%t[0] 
    ichk=int(ichkstr)
    if i!=ichk:
        i=ichk
        oled.fill(0)
        oled.text("Date:%02x/%02x/20%x" %(t[4],t[5],t[6]),5,5)
        oled.text("Time:%02x:%02x:%02x" %(t[2],t[1],t[0]),5,20)
        oled.text("Temp:",5,35)
        oled.text(str(temp)+" C",45,35)
        oled.text("Pres:",5,50)
        oled.text(str(p_d)+"."+str(p_b)+" KPa",45,50)
        oled.show()

        if incr==1:
            read=1
            incr=0
        else:
            incr=1        
     
    if button_a.value()==1:
        utime.sleep(0.25)
        disp_pressure()
        utime.sleep(0.25)

    if button_b.value()==1:
        utime.sleep(0.25)
        disp_temp()
        utime.sleep(0.25)

    utime.sleep(0.1)

"""


