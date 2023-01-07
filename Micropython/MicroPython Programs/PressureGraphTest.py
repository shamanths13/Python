from machine import Pin, I2C
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
i=0

t=rtc.read_time()
print("Date:%02x/%02x/20%x" %(t[4],t[5],t[6]))
print("Time:%02x:%02x:%02x" %(t[2],t[1],t[0]))

graph_x=100
graph_y=64

pdata_list=[0]
n = 0
points = graph_x

for n in range(1, points):
    pdata_list.append(0)

p_a = math.floor(bmp180.pressure)
p_b = p_a % 1000
print(p_b)

pdata_list_limit=[p_b]
for n in range(1, points):
    pdata_list_limit.append(p_b-1) 


while True:
    p_a = math.floor(bmp180.pressure)
    p_b = p_a % 1000
    p_c =(p_a-p_b)/1000
    p_d = round(p_c)
    p_e = str(p_d)+"."+str(p_b)
    p_e = round(float(p_e),3)
    
    for n in range(0, points-1):
        pdata_list_limit[n]=pdata_list_limit[n+1]
    pdata_list_limit[points-1] = p_b
    
    p_l = min(pdata_list_limit)
    p_u = max(pdata_list_limit)
    print(p_d,p_b,p_e)
    print(p_l,p_u)    
       
    for n in range(0, points):
        red_pres = ((graph_y-1) / (p_u - p_l)) * (pdata_list_limit[n] - p_l)
        p_r = round(red_pres)
        pdata_list[n]=p_r
        
    oled.fill(0)
    for n in range(0, points):
        oled.pixel(n+24, 63-pdata_list[n], 1)
        oled.text(str(max(pdata_list_limit)),0,0)
        oled.text(str(p_b),0,28)
        oled.text(str(min(pdata_list_limit)),0,56)
    oled.show()
    utime.sleep(1)
"""
while True:
    t=rtc.read_time()
    ichkstr="%0x"%t[0] 
    ichk=int(ichkstr)
    if i!=ichk:
        oled.fill(0)
        t=rtc.read_time()
        print("Date:%02x/%02x/20%x" %(t[4],t[5],t[6]))
        print("Time:%02x:%02x:%02x" %(t[2],t[1],t[0]))
        istr="%0x"%t[0] #Hex to Int string
        i=int(istr)
        oled.text("Date:%02x/%02x/20%x" %(t[4],t[5],t[6]),5,5)
        oled.text("Time:%02x:%02x:%02x" %(t[2],t[1],t[0]),5,20)
        temp = round(bmp180.temperature,2)
        p_a = math.floor(bmp180.pressure)
        p_b = p_a % 1000
        p_c =(p_a-p_b)/1000
        p_d = round(p_c)
        oled.text("Temp:",5,35)
        oled.text(str(temp)+" C",45,35)
        oled.text("Pres:",5,50)
        oled.text(str(p_d)+"."+str(p_b)+" KPa",45,50)
        oled.show()
        print(str(p_d)+"."+str(p_b)+" KPa")
        utime.sleep(0.5)
        
        oled.fill(0)
        oled.text("Date:%02x/%02x/20%x" %(t[4],t[5],t[6]),5,5)
        oled.text("Time:%02x:%02x %02x" %(t[2],t[1],t[0]),5,20)
        oled.text("Temp:",5,35)
        oled.text(str(temp)+" C",45,35)
        oled.text("Pres:",5,50)
        oled.text(str(p_d)+"."+str(p_b)+" KPa",45,50)
        oled.show()
        utime.sleep(0.3)
"""     
        