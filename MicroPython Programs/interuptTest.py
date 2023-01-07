from machine import Pin, I2C, ADC
import utime

led=machine.Pin(25,Pin.OUT)
led.value(0)
button_a=machine.Pin(16,machine.Pin.IN,machine.Pin.PULL_DOWN)
button_b=machine.Pin(17,machine.Pin.IN,machine.Pin.PULL_DOWN)
pot=ADC(28)
pot_lower=1000
pot_higher=64000
def case_a():
    while True:
        
        print("case a1")
        utime.sleep(0.1)
        if button_a.value()==1:
            print("stop")
            utime.sleep(0.5)
            break
def case_b():
    
    print("case b")
    utime.sleep(0.25)
while True:
#    print(pot.read_u16())
    pot_value=pot.read_u16()
    if pot_value < pot_lower:
        pot_value=pot_lower
    if pot_value > pot_higher:
        pot_value=pot_higher
    pot_red=((pot_value-pot_lower)/(pot_higher-pot_lower))*100
    pot_red=round(pot_red)
    print(pot_red)
    if button_a.value()==1:
        utime.sleep(0.25)
        print("case a")
        case_a()
    if button_b.value()==1:
        
        print("case b1")
        case_b()
    utime.sleep(0.1)