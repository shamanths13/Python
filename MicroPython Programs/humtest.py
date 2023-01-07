# htu_test.py Demo program for portable asynchronous HTU21D driver

# Author: Peter Hinch
# Copyright Peter Hinch 2018 Released under the MIT license

import uasyncio as asyncio
from machine import Pin, I2C
from htu21d import HTU21D



i2c = I2C(0, scl=Pin(5), sda=Pin(4),freq=200000)
    # Loboris port (soon this special treatment won't be needed).
    # https://forum.micropython.org/viewtopic.php?f=18&t=3553&start=390
    #i2c = I2C(scl=scl_pin, sda=sda_pin)

htu = HTU21D(i2c, read_delay=2)  # read_delay=2 for test purposes
async def hum_read():
    await htu
    print(htu.temperature, htu.humidity)


asyncio.run(hum_read())