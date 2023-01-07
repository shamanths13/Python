from machine import I2C, Pin
from bmp180 import BMP180
from ssd1306 import SSD1306_I2C
import framebuf
import utime
import math

i2c =  I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)   # use gpio number
bmp180 = BMP180(i2c)
bmp180.oversample_sett = 3
bmp180.baseline = 101325

i2c= I2C(1, scl=Pin(3), sda=Pin(2), freq=200000)
add=i2c.scan()
oled= SSD1306_I2C(128, 64, i2c)
oled.fill(0)

while True:
    oled.fill(0)
    t = round(bmp180.temperature,2)
    p_a = math.floor(bmp180.pressure)
    p_b = p_a % 1000
    p_c =(p_a-p_b)/1000
    p_d = round(p_c)
    oled.text("Temp:",2,5)
    oled.text(str(t)+" C",42,5)
    oled.text("Pres:",2,20)
    oled.text(str(p_d)+"."+str(p_b)+" KPa",42,20)
    oled.show()
    print("Temp:",t,"C","   Pressure:", str(p_d)+"."+str(p_b),"KPa")
    utime.sleep(2)