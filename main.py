from ota import OTAUpdater
from WIFI_CONFIG import SSID, PSK

import time
from cosmic import CosmicUnicorn
from picographics import PicoGraphics, DISPLAY_COSMIC_UNICORN as DISPLAY

machine.freq(200000000)

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
    firmware_url = "https://raw.githubusercontent.com/pierreyvesbaloche/kevinmca_ota/main/"

    ota_updater = OTAUpdater(SSID, PSK, firmware_url, "test_ota.py")

    ota_updater.download_and_install_update_if_available()

def BOB():
    graphics.set_pen(YELLOW)
    graphics.circle(centerx, centery, 10)

    graphics.set_pen(BLACK)
    graphics.circle(centerx, centery, 8)
    
def clear():
    graphics.set_pen(BLACK)
    graphics.clear()
    
checkVER()

while True:
    BOB()
    time.sleep(1)
    cu.update(graphics)
    time.sleep(1)
    clear()
    time.sleep(1)
    cu.update(graphics)
    time.sleep(1)


