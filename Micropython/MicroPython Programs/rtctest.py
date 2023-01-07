from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from ds3231 import DS3231_I2C
import framebuf
import utime

i2c=I2C(0, scl=Pin(5), sda=Pin(4))
rtc=DS3231_I2C(i2c)
oled= SSD1306_I2C(128, 64, i2c)
i=0
#current_time = b'\x00\x07\x01\x06\x02\x04\x22' # sec min hour week day mon year
#rtc.set_time(current_time)

while True:
    t=rtc.read_time()
    chk_str="%0x"%t[0]
    chk=int(chk_str)
    if i!= chk :
        oled.fill(0)
        t=rtc.read_time()
        print("Date:%02x/%02x/20%x" %(t[4],t[5],t[6]))
        print("Time:%02x:%02x:%02x" %(t[2],t[1],t[0]))
        print("%0x"%t[3])
        istr="%0x"%t[0] #Hex to Int string
        i=int(istr)
        oled.text("Date:%02x/%02x/20%x" %(t[4],t[5],t[6]),5,5)
        oled.text("Time:%02x:%02x:%02x" %(t[2],t[1],t[0]),5,20)
        oled.show()
        utime.sleep(0.5)
        oled.fill(0)
        oled.text("Date:%02x/%02x/20%x" %(t[4],t[5],t[6]),5,5)
        oled.text("Time:%02x:%02x %02x" %(t[2],t[1],t[0]),5,20)
        oled.show()
        utime.sleep(0.3)
    
