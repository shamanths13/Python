from machine import I2C, Pin
i2c= I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)
add=i2c.scan()
print(add)