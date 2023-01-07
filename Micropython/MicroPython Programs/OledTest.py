from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf


i2c= I2C(0, scl=Pin(5), sda=Pin(4), freq=200000)
add=i2c.scan()
oled= SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text("Hello World!",0,0)
oled.show()
oled.contrast(0)

log_freq=6

oled.fill(0)
oled.rect( 0, 0, 127, 63, 1)
oled.text("Frq: "+str(log_freq)+" Min",5,6)
oled.text("Dur: "+str(4*log_freq)+" Hrs",5,19)
oled.fill_rect( 0, 32, 127, 32, 1)
oled.text("New Frq:"+str(log_freq)+" Min",4,37,0)
oled.text("New Dur:"+str(4*log_freq)+" Hrs",4,50,0)
oled.show()
