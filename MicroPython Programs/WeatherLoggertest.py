from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from ds3231 import DS3231_I2C
from bmp180 import BMP180
import framebuf
import utime
import math


i2c= I2C(1, scl=Pin(3), sda=Pin(2), freq=200000)
rtc=DS3231_I2C(i2c)
bmp180 = BMP180(i2c)
bmp180.oversample_sett = 3
bmp180.baseline = 101325
oled= SSD1306_I2C(128, 64, i2c)
i=0

oled.fill(0)
oled.text("INITIALIZING",5,28)
oled.show()
utime.sleep(0.5)
oled.fill(0)
oled.text("INITIALIZING.",5,28)
oled.show()
utime.sleep(0.5)
oled.fill(0)
oled.text("INITIALIZING..",5,28)
oled.show()
utime.sleep(0.5)
oled.fill(0)
oled.text("INITIALIZING...",5,28)
oled.show()
utime.sleep(1)
oled.fill(0)
oled.text("Hello",5,28)
oled.show()
utime.sleep(0.25)
oled.fill(0)
oled.text("Hello Mummy",5,28)
oled.show()
utime.sleep(0.25)
oled.fill(0)
oled.text("Hello Mummy!",5,28)
oled.show()
utime.sleep(0.25)
oled.fill(0)
oled.text("Hello Mummy!!",5,28)
oled.show()
utime.sleep(1)
t=rtc.read_time()

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
        
        
