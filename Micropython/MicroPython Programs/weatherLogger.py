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

data_list=[100]
n = 0
points = 120
log_freq=1 # In Minutes
log_counter=log_freq

for n in range(1, points):
    data_list.append(100)
p_a = math.floor(bmp180.pressure)
p_b = p_a % 1000
p_l = min(data_list)-50
p_u = max(data_list)+50
red_pres = (60 / (p_u - p_l)) * (p_b - p_l)
p_r = round(red_pres)
data_list[points-1] = p_r

min_prev=61

read=1
incr=0
while True:
    t=rtc.read_time()
    min_str="%0x"%t[1]
    min_n=int(min_str)
    if min_n != min_prev:
        min_prev = min_n
        if log_counter==log_freq:
            p_a = math.floor(bmp180.pressure)
            p_b = p_a % 1000
            p_l = min(data_list)-50
            p_u = max(data_list)+50
            red_pres = (60 / (p_u - p_l)) * (p_b - p_l)
            p_r = round(red_pres)
            for n in range(0, points-1):
                data_list[n]=data_list[n+1]
            data_list[points-1] = p_r
            print("Log Time:%02x:%02x:%02x" %(t[2],t[1],t[0]))
            log_counter=0
        
        oled.fill(0)
        for n in range(0, points):
            oled.text(str(p_u),0,0)
            oled.text(str(p_l),0,56)
            oled.pixel(n+2, 61-data_list[n], 1)
        oled.show()
        log_counter=log_counter+1
        utime.sleep(5)
        
    if (read == 1):
        temp = round(bmp180.temperature,2)
        p_a = math.floor(bmp180.pressure)
        p_b = p_a % 1000
        p_c =(p_a-p_b)/1000
        p_d = round(p_c)
        read=0
           
    t=rtc.read_time()
    ichkstr="%0x"%t[0] 
    ichk=int(ichkstr)
    if i!=ichk:
        i=ichk
        oled.fill(0)
#        print("Date:%02x/%02x/20%x" %(t[4],t[5],t[6]))
#        print("Time:%02x:%02x:%02x" %(t[2],t[1],t[0]))
        oled.text("Date:%02x/%02x/20%x" %(t[4],t[5],t[6]),5,5)
        oled.text("Time:%02x:%02x:%02x" %(t[2],t[1],t[0]),5,20)
        oled.text("Temp:",5,35)
        oled.text(str(temp)+" C",45,35)
        oled.text("Pres:",5,50)
        oled.text(str(p_d)+"."+str(p_b)+" KPa",45,50)
        oled.show()
#        print(str(p_d)+"."+str(p_b)+" KPa")

        if incr==1:
            read=1
            incr=0
        else:
            incr=1        
        
        utime.sleep(0.9)
"""       
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
    