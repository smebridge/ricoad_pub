try:
 import usocket as socket        #importing socket
except:
 import socket
import network            #importing network
import gc
gc.collect()

from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD

import time

from cosmic import CosmicUnicorn
from picographics import PicoGraphics, DISPLAY_COSMIC_UNICORN as DISPLAY

machine.freq(200000000)

#test 5

cu = CosmicUnicorn()
graphics = PicoGraphics(DISPLAY)

cu.set_brightness(0.25)

BLACK = graphics.create_pen(0, 0, 0)
YELLOW = graphics.create_pen(255, 255, 0)
GREEN = graphics.create_pen(0, 255, 0)
GREY = graphics.create_pen(50,50,50)
RED = graphics.create_pen(255, 0, 0)

WIDTH, HEIGHT = graphics.get_bounds()
centerx=(WIDTH//2)
centery=(HEIGHT//2)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)              #WIFI ACTIVATING 

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Connecting.... .')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('Failed to join WIFI')
    machine.sreset()
else:
    print('CONNECTED!')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('RICO Access IP', addr)

def checkVER():
    graphics.set_pen(GREY)
    graphics.pixel(1,1)
    cu.update(graphics)
    
    firmware_url = "https://raw.githubusercontent.com/smebridge/ricoad_pub/main/"

    ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")

    ota_updater.download_and_install_update_if_available()
    
    graphics.set_pen(BLACK)
    graphics.pixel(1,1)
    cu.update(graphics)

def BOB():
#     graphics.set_pen(YELLOW)
#     graphics.circle(centerx, centery, 10)
# 
#     graphics.set_pen(BLACK)
#     graphics.circle(centerx, centery, 8)
    graphics.set_pen(YELLOW)
    graphics.polygon([
  (0, 8),
  (8, -1),
  (24, -1),
  (32, 8),
  (32, 24),
  (23, 32),
  (7, 31),
  (0, 24),
])
    graphics.set_pen(BLACK)
    graphics.text("BEBE", 5, 5, 18,1,0,1)
    graphics.text("A", 13, 12, 18,1,0,1)
    graphics.text("BORD", 5, 19, 18,1,0,1)
#    cu.update(graphics)
    
def CLEARDISP():
    graphics.set_pen(BLACK)
    graphics.clear()
    
#checkVER()
time.sleep(4)
import ntptime
ntptime.settime()
machine.RTC().datetime()
import utime
starttime = utime.time()

#def PERIODCHECKVER():
#    checkVER()
    #print("5 seconds have passed")

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>RICO AD</title>
    </head>
    <body>
        <h1 style="text-align: center;"><span style="background-color: #999999; color: #ffffff;"><span style="color: #ffcc99;">RICO A</span>FFICHAGE <span style="color: #ffcc99;">D</span>YNAMIQUE</span></h1>
        <p>&nbsp;</p>
        <table style="border-collapse: collapse; width: 100%; height: 100px;" border="0">
        <tbody>
        <tr style="height: 100px;">
        <td style="width: 100%; text-align: center; height: 18px;"><span style="color: #808080;"><form action="http://172.20.10.2" method="get"><input type="hidden" id="BOB" name="BOB" value="BOB"><input type="submit" value="BEBE A BORD" style="font-size : 80px; width: 100%; height: 300px; background-color: yellow; color: black"/></form></span></td>
        </tr>
        <tr style="height: 100px;">
        <td style="width: 100%; text-align: center; height: 18px;"><span style="color: #808080;"><form action="http://172.20.10.2" method="get"><input type="hidden" id="STOP" name="STOP" value="STOP"><input type="submit" value="STOP" style="font-size : 80px; width: 100%; height: 300px; background-color: white; color: red"/></form></span></td>
        </tr>        
        </tbody>
        </table>
    </body>
</html>
"""
BOB()
time.sleep(1)
cu.update(graphics) 

while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)
        requeststr = str(request)
        #search = requeststr.find("BOB")
        if requeststr.find("BOB",0,15) > 0:
            CLEARDISP()
            time.sleep(1)
            cu.update(graphics)             
            BOB()
            time.sleep(1)
            cu.update(graphics)
            requeststr = ""
        #search = requeststr.find("STOP")
        elif requeststr.find("STOP",0,15) > 0:
            CLEARDISP()
            time.sleep(1)
            cu.update(graphics)
            requeststr = ""

        response = html #% stateis
        
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')

#     if cu.is_pressed(CosmicUnicorn.SWITCH_BRIGHTNESS_UP):
#         cu.adjust_brightness(+0.1)
# 
#     if cu.is_pressed(CosmicUnicorn.SWITCH_BRIGHTNESS_DOWN):
#         cu.adjust_brightness(-0.1)    
    #print("EOF")    
    nowtime = utime.time()
    timelapse = nowtime - starttime
    if (timelapse > 60):
        checkVER()
        starttime = nowtime

