from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from ds3231 import DS3231_I2C
from bmp180 import BMP180
from htu21d import HTU21D
import uasyncio as asyncio
import framebuf
from utime import sleep
from math import floor

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 16


i2c= I2C(0, scl=Pin(5), sda=Pin(4), freq=200000)
rtc=DS3231_I2C(i2c)


lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

lcd.backlight_off()
bmp180 = BMP180(i2c)
bmp180.oversample_sett = 3
bmp180.baseline = 101325

htu = HTU21D(i2c, read_delay=2)


led=Pin(25, Pin.OUT)

button_a=Pin(18,Pin.IN,Pin.PULL_UP)

pot_x=ADC(27)
pot_y=ADC(28)
pot_lower=4000
pot_higher=64000
points=60
log_freq=10
log_counter=log_freq

def lcd_display():
    lcd.clear()
    lcd.move_to(9,0)
    lcd.putstr(str(avg_p)+"Pa")
    lcd.move_to(0,1)    
    lcd.putstr('{0:.2f}'.format(avg_t)+chr(223)+"C  "+'{0:.2f}'.format(avg_h)+"%")

    
async def temp_read():
        await htu
        return htu.temperature
    

async def hum_read():
        await htu
        return htu.humidity
    

def reading():
    global temp
    global pres
    global hum
    
    pres = floor(bmp180.pressure)
    temp = round(asyncio.run(temp_read()),2)
    hum = round(asyncio.run(hum_read()),2)
    if hum > 99.99:
        hum=99.99
    if hum < 0:
        hum=0

def reading_log():

    global p
    global t
    global h
            
    for n in range(0, points-1):
        p[n]=p[n+1]
    p[points-1] = avg_p

    for n in range(0, points-1):
        t[n]=t[n+1]
    t[points-1] = avg_t
    
    for n in range(0, points-1):
        h[n]=h[n+1]
    h[points-1] = avg_h
    lcd_display()

i=61
min_prev=61
read=1
incr=0

reading()
p=[pres]
h=[hum]
t=[temp]
pos=[0]
read_p = pres
read_t = temp
read_h = hum
read_n = 1
for n in range(0,points-1):
            p.append(pres)
            t.append(temp)
            h.append(hum)
            pos.append(n+1)
#print (pos)
pos_n=59

while True:
    time=rtc.read_time()
    min_str="%0x"%time[1]
    min_n=int(min_str)
    if min_n != min_prev:
        min_prev = min_n
        avg_p=(read_p)/read_n
        avg_p=round(avg_p)
        avg_t=(read_t)/read_n
        avg_t=round(avg_t,2)
        avg_h=(read_h)/read_n
        avg_h=round(avg_h,2)
        
        if log_counter==log_freq:
            reading_log()
            if pos_n < 0:
                pos_n=59
            print(pos_n)
            for n in range(0,60):
                print(p[59-n])
                print(t[59-n])
                print(h[59-n])
            pos_n -=1
            log_counter=0
        log_counter=log_counter+1
        read_p=0
        read_t=0
        read_h=0
        read_n=0
        
    if (read == 1):
        reading()
        read_n=read_n + 1
        read_t=read_t + temp
        read_p=read_p + pres
        read_h=read_h + hum
        read=0
        
    ichkstr="%0x"%time[0] 
    ichk=int(ichkstr)
    if i!=ichk:
        i=ichk
        lcd.move_to(0,0)
        lcd.putstr("%02x:%02x:%02x" %(time[2],time[1],time[0]))
        
        if incr==1:
            read=1
            incr=0
        else:
            incr=1        
       
    sleep(0.9)










