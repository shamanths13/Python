from machine import Pin, I2C, ADC
from utime import sleep
button_a=Pin(18,Pin.IN,Pin.PULL_UP)
pot_x=ADC(27)
pot_y=ADC(28)
pot_lower=5000
pot_higher=60000
pot_red=0
pot_value=pot_y.read_u16()
print(pot_value)
while True:
    potx_value=pot_y.read_u16()
    poty_value=pot_x.read_u16()
    print("potx_value:",potx_value,"poty_value:",poty_value)
    """
    if pot_value > pot_higher:
        pot_red=pot_red+(1)
    if pot_value < pot_lower:
        pot_red=pot_red-(1)
    if pot_red < 0:
        pot_red=0
    if pot_red>100:
        pot_red=100

    print(pot_red)
    """
    #print(button_a.value())
    sleep(0.2)
    
    