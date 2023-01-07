from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from ds3231 import DS3231_I2C
from bmp180 import BMP180
from htu21d import HTU21D
import uasyncio as asyncio
import framebuf
import utime
import math

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 16


i2c= I2C(0, scl=Pin(5), sda=Pin(4), freq=200000)
rtc=DS3231_I2C(i2c)


lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
lcd.custom_char(0, bytearray([0x04, 0x0E, 0x1B, 0x11, 0x04, 0x0E, 0x1B, 0x11]))
lcd.custom_char(1, bytearray([0x11, 0x1B, 0x0E, 0x04, 0x11, 0x1B, 0x0E, 0x04]))
lcd.custom_char(2, bytearray([0x00, 0x00, 0x04, 0x0E, 0x1B, 0x11, 0x00, 0x00]))
lcd.custom_char(3, bytearray([0x00, 0x00, 0x11, 0x1B, 0x0E, 0x04, 0x00, 0x00]))
lcd.custom_char(4, bytearray([0x00, 0x1B, 0x11, 0x04, 0x11, 0x1B, 0x00, 0x00]))
lcd.custom_char(5, bytearray([0x1F, 0x04, 0x0E, 0x1F, 0x04, 0x04, 0x04, 0x04]))
lcd.custom_char(6, bytearray([0x04, 0x04, 0x04, 0x04, 0x1F, 0x0E, 0x04, 0x1F]))
lcd.custom_char(7, bytearray([0x04, 0x0E, 0x1F, 0x00, 0x00, 0x1F, 0x0E, 0x04]))

bkl_state=1
bkl_counter=0
bkl_auto = 0
bkl_dur=5
lcd.display_on()
lcd.clear()

bmp180 = BMP180(i2c)
bmp180.oversample_sett = 3
bmp180.baseline = 101325

htu = HTU21D(i2c, read_delay=2)

oled= SSD1306_I2C(128, 64, i2c)
oled.contrast(0)#0-255
oled.fill(0)
oled.show()

led=Pin(25, Pin.OUT)

button_a=Pin(18,Pin.IN,Pin.PULL_UP)

pot_x=ADC(27)
pot_y=ADC(28)
pot_lower=4000
pot_higher=64000

t=rtc.read_time()
day="ini"
print("Date:%02x/%02x/20%x" %(t[4],t[5],t[6]))
print("Time:%02x:%02x:%02x" %(t[2],t[1],t[0]))

graph_x=120
graph_y=50
log_freq=1#In Minutes(1,2,3,5,6,10,15,30)
log_val=[1,2,3,5,6,10,15,30]
n = 0
points = 240


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
    
    pres = math.floor(bmp180.pressure)
    temp = round(asyncio.run(temp_read()),2)
    hum = round(asyncio.run(hum_read()),2)
    if hum > 99.99:
        hum=99.99
    if hum < 0:
        hum=0


def logfreq_set(temp_log_freq):
    global log_counter
    global log_freq
    global graph_data
    global pdata_list
    global pdata_list_limit
    global tdata_list
    global tdata_list_limit
    global hdata_list
    global hdata_list_limit
    global read_p
    global read_t
    global read_h
    global read_n
    global i
    global min_prev
    global hr_prev
    global read
    global incr
    global p_rate
    global t_rate
    global h_rate
    
    log_freq = temp_log_freq
    grid_locxspace = round(60/log_freq)
    grid_locxstartint = round(grid_locxspace/2)
    log_counter=log_freq
    n = 0
    count_graph_bigseg=0
    graph_data=[0]
    for n in range(1,points):
        graph_data.append(0)
    for n in range(0,points):
        mark=n%grid_locxstartint
        if mark==0:
            graph_data[n]=1
    for n in range(0,points):
        mark=n%grid_locxspace
        if mark==0:
            graph_data[n]=2
            if count_graph_bigseg == 0:
                graph_data[n]=3
                count_graph_bigseg=4
            count_graph_bigseg=count_graph_bigseg-1
            
    graph_data.append(3)    
    
    reading()

    pdata_list=[0]
    for n in range(1, points):
        pdata_list.append(0)

    pdata_list_limit=[pres]
    for n in range(1, points):
        pdata_list_limit.append(pres)
    pdata_list_limit[1]=pres-1
    pdata_list_limit[2]=pres+1
    read_p = pres

    tdata_list=[0]
    for n in range(1, points):
        tdata_list.append(0)

    tdata_list_limit=[temp]
    for n in range(1, points):
        tdata_list_limit.append(temp)
    tdata_list_limit[1]=temp-0.1
    tdata_list_limit[2]=temp+0.1
    read_t = temp

    hdata_list=[0]
    for n in range(1, points):
        hdata_list.append(0)

    hdata_list_limit=[hum]
    for n in range(1, points):
        hdata_list_limit.append(hum)
    hdata_list_limit[1]=hum-0.1
    hdata_list_limit[2]=hum+0.1
    read_h = hum

    read_n = 1
    i=61
    min_prev=61
    hr_prev=24
    read=1
    incr=0
    p_rate=243
    t_rate=243
    h_rate=243
    

def initialize():
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr(" WEATHER LOGGER ")
    utime.sleep(0.25)
    lcd.move_to(0,1)
    lcd.putstr("  Initializing  ")
    utime.sleep(1.5)
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("Set Logging Freq")
    lcd.move_to(0,1)
    lcd.move_to(2,1)
    lcd.putstr(chr(7)+"Select")
    lcd.move_to(11,1)    
    lcd.putstr(chr(4)+"Ok")
    
    log_sel=0

    while True:     
        pot_opt=pot_x.read_u16()
        if pot_opt > pot_higher:
            utime.sleep(0.1)
            log_sel +=1
        if pot_opt < pot_lower:
            utime.sleep(0.1)
            log_sel -=1
        if log_sel < 0:
            log_sel = 7
        if log_sel > 7:
            log_sel = 0
            
        oled.fill(0)
        oled.rect( 0, 0, 127, 63, 1)
        oled.text("Total Log Time",7,8)
        oled.text("Dur: "+str(4*(log_val[log_sel]))+" Hours",10,23)
        oled.fill_rect( 0, 38, 127, 15, 1)
        oled.text("Log Freq:"+str(log_val[log_sel])+" min",3,42,0)
        oled.show()
        
        if button_a.value()==0:
            logfreq_set(log_val[log_sel])
            lcd.clear()
            lcd.move_to(0,0)
            lcd.putstr("  Initialized")
            utime.sleep(1)
            lcd.clear()
            lcd.move_to(0,0)
            lcd.putstr("Log Every "+str(log_freq)+" min")
            lcd.move_to(0,1)
            lcd.putstr("Log Dur "+str(4*log_freq)+" hrs")
            oled.fill(0)
            oled.text("Initialized",19,27)
            oled.show()
            utime.sleep(5)
            lcd.backlight_off()
            oled.fill(0)
            oled.show()
            lcd.clear()
            break
        
        utime.sleep(0.2)


def reading_log():
    global pdata_list
    global pdata_list_limit
    global tdata_list
    global tdata_list_limit
    global hdata_list
    global hdata_list_limit
    global p_rate
    global t_rate
    global h_rate
            
    for n in range(0, points-1):
        pdata_list_limit[n]=pdata_list_limit[n+1]
    pdata_list_limit[points-1] = avg_p
            
    p_l = min(pdata_list_limit)-1
    p_u = max(pdata_list_limit)+1    
               
    for n in range(0, points):
        red_pres = ((graph_y-1) / (p_u - p_l)) * (pdata_list_limit[n] - p_l)
        p_r = round(red_pres)
        pdata_list[n]=p_r

            
    for n in range(0, points-1):
        tdata_list_limit[n]=tdata_list_limit[n+1]
    tdata_list_limit[points-1] = avg_t
            
    t_l = min(tdata_list_limit)-0.01
    t_u = max(tdata_list_limit)+0.01    
               
    for n in range(0, points):
        red_temp = ((graph_y-1) / (t_u - t_l)) * (tdata_list_limit[n] - t_l)
        t_r = round(red_temp)
        tdata_list[n]=t_r
    
    
    for n in range(0, points-1):
        hdata_list_limit[n]=hdata_list_limit[n+1]
    hdata_list_limit[points-1] = avg_h
            
    h_l = min(hdata_list_limit)-0.01
    h_u = max(hdata_list_limit)+0.01    
               
    for n in range(0, points):
        red_hum = ((graph_y-1) / (h_u - h_l)) * (hdata_list_limit[n] - h_l)
        h_r = round(red_hum)
        hdata_list[n]=h_r
                
    print("Log Time:%02x:%02x:%02x" %(t[2],t[1],t[0]))
    print("Temp:",avg_t," C")
    print("Pres:",avg_p," Pa")
    print("Hum:",avg_h," %")
    
    if pdata_list_limit[points-1] == max(pdata_list_limit):
        p_rate=0
    elif pdata_list_limit[points-1] == min(pdata_list_limit):
        p_rate=1
    elif pdata_list_limit[points-1] > pdata_list_limit[points-2]:
        p_rate=2
    elif pdata_list_limit[points-1] < pdata_list_limit[points-2]:
        p_rate=3
    else:
        p_rate=243
        
    if tdata_list_limit[points-1] == max(tdata_list_limit):
        t_rate=0
    elif tdata_list_limit[points-1] == min(tdata_list_limit):
        t_rate=1
    elif tdata_list_limit[points-1] > tdata_list_limit[points-2]:
        t_rate=2
    elif tdata_list_limit[points-1] < tdata_list_limit[points-2]:
        t_rate=3
    else:
        t_rate=243
    
    if hdata_list_limit[points-1] == max(hdata_list_limit):
        h_rate=0
    elif hdata_list_limit[points-1] == min(hdata_list_limit):
        h_rate=1
    elif hdata_list_limit[points-1] > hdata_list_limit[points-2]:
        h_rate=2
    elif hdata_list_limit[points-1] < hdata_list_limit[points-2]:
        h_rate=3
    else:
        h_rate=243


def disp_pressure(pot_red):    
    oled.fill(0)
    oled.fill_rect( 1, 27, 127, 11, 1)
    oled.text("Pressure",32,29,0)
    oled.show()
    
    utime.sleep(0.1)    
    
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("P:"+str(pdata_list_limit[points-1])+" Pa")
    lcd.move_to(0,1)
    lcd.putstr(" "+chr(5)+str(max(pdata_list_limit))+"  "+chr(6)+str(min(pdata_list_limit)))
    
    auto_esc=0
    while True:
        oled.fill(0)    
        pot_value=pot_y.read_u16()
        pot_opt=pot_x.read_u16()
        if pot_value < pot_lower:
            pot_red=pot_red-(2)
            auto_esc=0
        if pot_value > pot_higher:
            pot_red=pot_red+(2)
            auto_esc=0
        if pot_red < 0:
            pot_red=0
        if pot_red>100:
            pot_red=100
        if pot_red<26:
            pot_red=26
        ctr=-1    
        for n in range(0,(points*2)+1):
            
            n_red=(n*pot_red)/100
            n_red=round(n_red)
            if (127-n_red) < 0:
                break
            if n%2==0:
                n_sub=round(n/2)
                if n_sub<points:
                    oled.pixel(127-n_red, 63-pdata_list[points-1-n_sub]-7, 1)
                if graph_data[n_sub]==1:
                    oled.pixel(127-n_red, 63, 1)
                    oled.pixel(127-n_red, 0, 1)
                if graph_data[n_sub]==2:
                    ctr+=1
                    oled.pixel(127-n_red, 62, 1)
                    oled.pixel(127-n_red, 61, 1)
                    oled.pixel(127-n_red, 1, 1)
                    oled.pixel(127-n_red, 2, 1)
                if graph_data[n_sub]==3:
                    ctr+=1
                    oled.pixel(127-n_red, 63, 1)
                    oled.pixel(127-n_red, 62, 1)
                    oled.pixel(127-n_red, 61, 1)
                    oled.pixel(127-n_red, 60, 1)
                    oled.pixel(127-n_red, 59, 1)
                    oled.pixel(127-n_red, 0, 1)
                    oled.pixel(127-n_red, 1, 1)
                    oled.pixel(127-n_red, 2, 1)
                    oled.pixel(127-n_red, 3, 1)
                    oled.pixel(127-n_red, 4, 1)
            else:
                if n<((2*points)-2):                    
                    int_value=(pdata_list[points-1-round(((n-1)/2)+1)]+pdata_list[points-1-round(((n-3)/2)+1)])/2
                    int_value=round(int_value)
                    oled.pixel(127-n_red, 63-int_value-7, 1)
        
        lcd.move_to(12,0)
        lcd.putstr(str(ctr)+"h ")
            
        oled.show()
        utime.sleep(0.05)
        auto_esc += 1
        if button_a.value()==0 or auto_esc > 100:
            return pot_red


def disp_temp(pot_red):  
    oled.fill(0)
    oled.fill_rect( 1, 27, 127, 11, 1)
    oled.text("Temperature",20,29,0)
    oled.show()
    
    utime.sleep(0.1)
    
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("T:"+str(tdata_list_limit[points-1])+chr(223)+"C")
    lcd.move_to(0,1)
    lcd.putstr(" "+chr(5)+str(max(tdata_list_limit)))
    lcd.move_to(9,1)
    lcd.putstr(chr(6)+str(min(tdata_list_limit)))
        
    auto_esc=0
    while True:
        oled.fill(0)    
        pot_value=pot_y.read_u16()
        pot_opt=pot_x.read_u16()
        if pot_value < pot_lower:
            pot_red=pot_red-(2)
            auto_esc=0
        if pot_value > pot_higher:
            pot_red=pot_red+(2)
            auto_esc=0
        if pot_red < 0:
            pot_red=0
        if pot_red>100:
            pot_red=100
        if pot_red<26:
            pot_red=26
        ctr=-1
        for n in range(0,(points*2)+1):
            n_red=(n*pot_red)/100
            n_red=round(n_red)
            if (127-n_red) < 0:
                break
            
            if n%2==0:
                n_sub=round(n/2)
                if n_sub<points:
                    oled.pixel(127-n_red, 63-tdata_list[points-1-n_sub]-7, 1)
                if graph_data[n_sub]==1:
                    oled.pixel(127-n_red, 63, 1)
                    oled.pixel(127-n_red, 0, 1)
                if graph_data[n_sub]==2:
                    ctr+=1
                    oled.pixel(127-n_red, 62, 1)
                    oled.pixel(127-n_red, 61, 1)
                    oled.pixel(127-n_red, 1, 1)
                    oled.pixel(127-n_red, 2, 1)
                if graph_data[n_sub]==3:
                    ctr+=1
                    oled.pixel(127-n_red, 63, 1)
                    oled.pixel(127-n_red, 62, 1)
                    oled.pixel(127-n_red, 61, 1)
                    oled.pixel(127-n_red, 60, 1)
                    oled.pixel(127-n_red, 59, 1)
                    oled.pixel(127-n_red, 0, 1)
                    oled.pixel(127-n_red, 1, 1)
                    oled.pixel(127-n_red, 2, 1)
                    oled.pixel(127-n_red, 3, 1)
                    oled.pixel(127-n_red, 4, 1)
            else:
                if n<((2*points)-2):                    
                    int_value=(tdata_list[points-1-round(((n-1)/2)+1)]+tdata_list[points-1-round(((n-3)/2)+1)])/2
                    int_value=round(int_value)
                    oled.pixel(127-n_red, 63-int_value-7, 1)
        
        lcd.move_to(12,0)
        lcd.putstr(str(ctr)+"h ")
        
        oled.show()
        utime.sleep(0.05)
        auto_esc += 1
        if button_a.value()==0 or auto_esc > 100:
            return pot_red


def disp_hum(pot_red):
    oled.fill(0)
    oled.fill_rect( 1, 27, 127, 11, 1)
    oled.text("Humidity",32,29,0)
    oled.show()
    
    utime.sleep(0.1)    
    
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("H:"+str(hdata_list_limit[points-1])+" %")
    lcd.move_to(0,1)
    lcd.putstr(" "+chr(5)+str(max(hdata_list_limit))+"  "+chr(6)+str(min(hdata_list_limit)))    

    auto_esc=0
    while True:
        oled.fill(0)    
        pot_value=pot_y.read_u16()
        pot_opt=pot_x.read_u16()
        if pot_value < pot_lower:
            pot_red=pot_red-(2)
            auto_esc=0
        if pot_value > pot_higher:
            pot_red=pot_red+(2)
            auto_esc=0
        if pot_red < 0:
            pot_red=0
        if pot_red>100:
            pot_red=100
        if pot_red<26:
            pot_red=26
        ctr=-1    
        for n in range(0,(points*2)+1):
            n_red=(n*pot_red)/100
            n_red=round(n_red)
            if (127-n_red) < 0:
                break
            if n%2==0:
                n_sub=round(n/2)
                if n_sub<points:
                    oled.pixel(127-n_red, 63-hdata_list[points-1-n_sub]-7, 1)
                if graph_data[n_sub]==1:
                    oled.pixel(127-n_red, 63, 1)
                    oled.pixel(127-n_red, 0, 1)
                if graph_data[n_sub]==2:
                    ctr+=1
                    oled.pixel(127-n_red, 62, 1)
                    oled.pixel(127-n_red, 61, 1)
                    oled.pixel(127-n_red, 1, 1)
                    oled.pixel(127-n_red, 2, 1)
                if graph_data[n_sub]==3:
                    ctr+=1
                    oled.pixel(127-n_red, 63, 1)
                    oled.pixel(127-n_red, 62, 1)
                    oled.pixel(127-n_red, 61, 1)
                    oled.pixel(127-n_red, 60, 1)
                    oled.pixel(127-n_red, 59, 1)
                    oled.pixel(127-n_red, 0, 1)
                    oled.pixel(127-n_red, 1, 1)
                    oled.pixel(127-n_red, 2, 1)
                    oled.pixel(127-n_red, 3, 1)
                    oled.pixel(127-n_red, 4, 1)
            else:
                if n<((2*points)-2):                    
                    int_value=(hdata_list[points-1-round(((n-1)/2)+1)]+hdata_list[points-1-round(((n-3)/2)+1)])/2
                    int_value=round(int_value)
                    oled.pixel(127-n_red, 63-int_value-7, 1)
        
        lcd.move_to(12,0)
        lcd.putstr(str(ctr)+"h ")
        
        oled.show()
        utime.sleep(0.05)
        auto_esc += 1
        if button_a.value()==0 or auto_esc > 100:
            return pot_red
        
def lcd_display():      
    lcd.move_to(0,0)
    lcd.putstr(day+" %02x:%02x:%02x" %(t[2],t[1],t[0]))
    lcd.move_to(13,0)
    lcd.putstr("Pr"+ chr(p_rate))
    lcd.move_to(0,1)    
    lcd.putstr(chr(t_rate)+'{0:.2f}'.format(temp)+chr(223)+"C")
    lcd.move_to(9,1)
    lcd.putstr(chr(h_rate)+'{0:.2f}'.format(hum)+"%")


def set_day():
    day="%0x"%t[3]
    if day=='7':
        day="Sun"
    elif day=='1':
        day="Mon"
    elif day=='2':
        day="Tue"
    elif day=='3':
        day="Wed"
    elif day=='4':
        day="Thu"
    elif day=='5':
        day="Fri"
    elif day=='6':
        day="Sat"
    return day


def oled_menu():
    oled.rect( 0, 1, 128, 63, 1)
    oled.fill_rect( 1, 27, 127, 11, 1)
    oled.pixel(63,58,1)
    oled.hline(62,57,3,1)
    oled.hline(61,56,5,1)
    oled.hline(60,55,7,1)
    oled.hline(59,54,9,1)
    oled.pixel(63,6,1)
    oled.hline(62,7,3,1)
    oled.hline(61,8,5,1)
    oled.hline(60,9,7,1)
    oled.hline(59,10,9,1)

def lcd_dispmenu():
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr(" Selection Menu ")
    lcd.move_to(0,1)
    lcd.putstr(chr(127)+"Exit")
    lcd.move_to(7,1)    
    lcd.putstr(chr(7)+"Sel")
    lcd.move_to(13,1)
    lcd.putstr("Ok"+chr(126))


def disp_logfreq():
    global log_freq
    lcd.move_to(15,1)    
    lcd.putstr(chr(4))
    oled.fill(0)
    oled.fill_rect( 1, 27, 127, 11, 1)
    oled.text("Logging Freq",16,29,0)
    oled.show()
    utime.sleep(0.6)
    log_sel=0
    auto_esc=0
    while True:     
        pot_opt=pot_x.read_u16()
        pot_sel=pot_y.read_u16()
        if pot_opt > pot_higher:
            utime.sleep(0.1)
            log_sel +=1
            auto_esc=0
        if pot_opt < pot_lower:
            utime.sleep(0.1)
            log_sel -=1
            auto_esc=0
        if log_sel < 0:
            log_sel = 7
        if log_sel > 7:
            log_sel = 0
            
        oled.fill(0)
        oled.rect( 0, 0, 127, 63, 1)
        oled.text("Frq: "+str(log_freq)+" Min",5,6)
        oled.text("Dur: "+str(4*log_freq)+" Hrs",5,19)
        oled.fill_rect( 0, 32, 127, 32, 1)
        oled.text("New Frq:"+str(log_val[log_sel])+" Min",4,37,0)
        oled.text("New Dur:"+str(4*log_val[log_sel])+" Hrs",4,50,0)
        oled.show()
        auto_esc += 1        
        if pot_sel > pot_higher or auto_esc > 50:
            utime.sleep(0.2)
            lcd.move_to(15,1)    
            lcd.putstr(chr(126))
            return 0
            break
        if button_a.value()==0:
            logfreq_set(log_val[log_sel])
            lcd.clear()
            lcd.move_to(0,0)
            lcd.putstr("  Device Reset")
            lcd.move_to(2,1)
            lcd.putstr("Log Every "+str(log_freq)+"m")
            oled.fill(0)
            oled.text("Device Reset",15,27)
            oled.show()
            utime.sleep(5)
            return 1
        
        utime.sleep(0.2)


def disp_auto():
    global bkl_dur
    menu_sel=1
    break_val=0
    auto_esc=0
    while True:      
        pot_opt=pot_x.read_u16()
        pot_sel=pot_y.read_u16()
        if pot_opt > pot_higher:
            utime.sleep(0.2)
            menu_sel +=1
            auto_esc=0
        if pot_opt < pot_lower:
            utime.sleep(0.2)
            menu_sel -=1
            auto_esc=0
        if menu_sel < 1:
            menu_sel = 3
        if menu_sel > 3:
            menu_sel = 1
        
        if menu_sel == 1:
            oled.fill(0)
            oled_menu()
            oled.text("15 seconds",24,15)
            oled.text("5 seconds",28,29,0)
            oled.text("10 seconds",24,43)
            oled.show()
        
        if menu_sel == 2:
            oled.fill(0)
            oled_menu()
            oled.text("5 seconds",28,15)
            oled.text("10 seconds",24,29,0)
            oled.text("15 seconds",24,43)
            oled.show()
            
        if menu_sel == 3:
            oled.fill(0)
            oled_menu()
            oled.text("10 seconds",24,15)
            oled.text("15 seconds",24,29,0)
            oled.text("5 seconds",28,43)
            oled.show()
        
        if button_a.value()==0:
            if menu_sel == 1:
                oled.fill(0)
                oled.fill_rect( 1, 27, 127, 11, 1)
                oled.text("5 seconds",28,29,0)
                oled.show()
                bkl_dur=5
                utime.sleep(0.5)
                break_val=1
                break
            if menu_sel == 2:
                oled.fill(0)
                oled.fill_rect( 1, 27, 127, 11, 1)
                oled.text("10 seconds",24,29,0)
                oled.show()
                bkl_dur=10
                utime.sleep(0.5)
                break_val=1
                break
            if menu_sel == 3:
                oled.fill(0)
                oled.fill_rect( 1, 27, 127, 11, 1)
                oled.text("15 seconds",24,29,0)
                oled.show()
                bkl_dur=15
                utime.sleep(0.5)
                break_val=1
                break

        auto_esc += 1
        if pot_sel > pot_higher or break_val==1 or auto_esc > 50:
            break
        utime.sleep(0.2)
    

def disp_bklt():
    global bkl_auto
    menu_sel=1
    break_val=0
    lcd.move_to(15,1)    
    lcd.putstr(chr(4))
    oled.fill(0)
    oled.fill_rect( 1, 27, 127, 11, 1)
    oled.text("Backlight",28,29,0)
    oled.show()
    utime.sleep(0.5)
    auto_esc=0
    while True:      
        pot_opt=pot_x.read_u16()
        pot_sel=pot_y.read_u16()
        if pot_opt > pot_higher:
            utime.sleep(0.2)
            menu_sel +=1
            auto_esc=0
        if pot_opt < pot_lower:
            utime.sleep(0.2)
            menu_sel -=1
            auto_esc=0
        if menu_sel < 1:
            menu_sel = 3
        if menu_sel > 3:
            menu_sel = 1
        
        if menu_sel == 1:
            oled.fill(0)
            oled_menu()
            oled.text("Off",52,15)
            oled.text("Auto",48,29,0)
            oled.text("On",56,43)
            oled.show()
        
        if menu_sel == 2:
            oled.fill(0)
            oled_menu()
            oled.text("Auto",48,15)
            oled.text("On",56,29,0)
            oled.text("Off",52,43)
            oled.show()
            
        if menu_sel == 3:
            oled.fill(0)
            oled_menu()
            oled.text("On",56,15)
            oled.text("Off",52,29,0)
            oled.text("Auto",48,43)
            oled.show()
        
        if button_a.value()==0:
            if menu_sel == 1:
                oled.fill(0)
                oled.fill_rect( 1, 27, 127, 11, 1)
                oled.text("Auto",48,29,0)
                oled.show()
                bkl_auto=1
                utime.sleep(0.5)
                disp_auto()
                lcd.backlight_on()
                break_val=1
                break
            if menu_sel == 2:
                oled.fill(0)
                oled.fill_rect( 1, 27, 127, 11, 1)
                oled.text("On",56,29,0)
                oled.show()
                bkl_auto=0
                utime.sleep(0.5)
                lcd.backlight_on()
                break_val=1
                break
            if menu_sel == 3:
                oled.fill(0)
                oled.fill_rect( 1, 27, 127, 11, 1)
                oled.text("Off",52,29,0)
                oled.show()
                bkl_auto=0
                utime.sleep(0.5)
                lcd.backlight_off()
                break_val=1
                break

        auto_esc += 1
        if pot_sel > pot_higher or break_val==1 or auto_esc > 50:
            break
        utime.sleep(0.2)
            
    
def menu():
    menu_sel=1
    break_val=0
    lcd_dispmenu()
    auto_esc=0
    zoom_lvl= 100
    while True:      
        pot_opt=pot_x.read_u16()
        pot_sel=pot_y.read_u16()
        if pot_opt > pot_higher:
            utime.sleep(0.1)
            menu_sel +=1
            auto_esc=0
        if pot_opt < pot_lower:
            utime.sleep(0.1)
            menu_sel -=1
            auto_esc=0
        if menu_sel < 1:
            menu_sel = 5
        if menu_sel > 5:
            menu_sel = 1
        
        if menu_sel == 1:
            oled.fill(0)
            oled_menu()
            oled.text("Temperature",20,15)
            oled.text("Pressure",32,29,0)
            oled.text("Humidity",32,43)
            oled.show()
            
        if menu_sel == 2:
            oled.fill(0)
            oled_menu()
            oled.text("Pressure",32,15)
            oled.text("Humidity",32,29,0)
            oled.text("Logging Freq",16,43)
            oled.show()
            
        if menu_sel == 3:
            oled.fill(0)
            oled_menu()
            oled.text("Humidity",32,15)
            oled.text("Logging Freq",16,29,0)
            oled.text("Backlight",28,43)
            oled.show()
            
        if menu_sel == 4:
            oled.fill(0)
            oled_menu()
            oled.text("Logging Freq",16,15)
            oled.text("Backlight",28,29,0)
            oled.text("Temperature",20,43)
            oled.show()
            
        if menu_sel == 5:
            oled.fill(0)
            oled_menu()
            oled.text("Backlight",28,15)
            oled.text("Temperature",20,29,0)
            oled.text("Pressure",32,43)
            oled.show()
            
        if pot_sel < pot_lower:
            auto_esc=0
            if menu_sel == 1:
                zoom_lvl=disp_pressure(zoom_lvl)
                lcd_dispmenu()
            if menu_sel == 2:
                zoom_lvl=disp_hum(zoom_lvl)
                lcd_dispmenu()
            if menu_sel == 3:
                break_val=disp_logfreq()
            if menu_sel == 4:
                disp_bklt()
            if menu_sel == 5:
                zoom_lvl=disp_temp(zoom_lvl)
                lcd_dispmenu()                    
    
        auto_esc += 1
        if pot_sel > pot_higher or break_val==1 or auto_esc > 50:
            break
        utime.sleep(0.2)
        
    
initialize()    
oled.poweroff()

while True:
    t=rtc.read_time()
    hr_str="%0x"%t[2]
    hr_n=int(hr_str)
    if hr_n != hr_prev:
        hr_prev = hr_n
        day=set_day()
    min_str="%0x"%t[1]
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
        
    t=rtc.read_time()
    ichkstr="%0x"%t[0] 
    ichk=int(ichkstr)
    if i!=ichk:
        i=ichk
        lcd_display()
        
        if bkl_auto == 1:
            if bkl_state == 1:
                bkl_counter += 1
                
        if incr==1:
            read=1
            incr=0
        else:
            incr=1        
     
    if button_a.value()==0:
        lcd.backlight_on()
        bkl_counter=0
        bkl_state=1
        
        oled.poweron()
        menu()
        oled.fill(0)
        oled.show()
        oled.poweroff()
        lcd.clear()
        utime.sleep(0.25)
    
    if bkl_auto == 1:
        pot_bklx=pot_x.read_u16()
        pot_bkly=pot_y.read_u16()
        if (pot_bklx > pot_higher or pot_bklx < pot_lower or pot_bkly > pot_higher or pot_bkly < pot_lower) and (bkl_state == 0):
            lcd.backlight_on()
            bkl_counter=0
            bkl_state=1
        
    if bkl_counter > bkl_dur:
        lcd.backlight_off()
        bkl_state=0
    
    utime.sleep(0.2)

class Graph:
    pass






