from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD

import time
from cosmic import CosmicUnicorn
from picographics import PicoGraphics, DISPLAY_COSMIC_UNICORN as DISPLAY

machine.freq(200000000)

#test 2

cu = CosmicUnicorn()
graphics = PicoGraphics(DISPLAY)

cu.set_brightness(0.22)

BLACK = graphics.create_pen(0, 0, 0)
YELLOW = graphics.create_pen(255, 255, 0)
GREEN = graphics.create_pen(0, 255, 0)
GREY = graphics.create_pen(50,50,50)
RED = graphics.create_pen(255, 0, 0)

WIDTH, HEIGHT = graphics.get_bounds()
centerx=(WIDTH//2)
centery=(HEIGHT//2)

def checkVER():
    graphics.set_pen(GREY)
    graphics.text(".", 0, 0, scale=1)
    cu.update(graphics)
    
    firmware_url = "https://raw.githubusercontent.com/smebridge/ricoad_pub/main/"

    ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")

    ota_updater.download_and_install_update_if_available()

def BOB():
    graphics.set_pen(YELLOW)
    graphics.circle(centerx, centery, 10)

    graphics.set_pen(BLACK)
    graphics.circle(centerx, centery, 8)
    
def CLEARDISP():
    graphics.set_pen(BLACK)
    graphics.clear()
    
#checkVER()

import ntptime
ntptime.settime()
machine.RTC().datetime()
import utime
starttime = utime.time()

def PERIODCHECKVER():
    checkVER()
    #print("5 seconds have passed")


while True:
    BOB()
    time.sleep(1)
    cu.update(graphics)
    time.sleep(1)
    CLEARDISP()
    nowtime = utime.time()
    if (nowtime - starttime)>60:
        PERIODCHECKVER()
        starttime = nowtime
    time.sleep(1)
    cu.update(graphics)
    time.sleep(1)
