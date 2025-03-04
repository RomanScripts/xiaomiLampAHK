import time, random
from miio import Yeelight
from datetime import datetime, timedelta
from sys import argv


# If arguments was passed to this script, then we take ip from them. Otherwise take specified values
if len(argv)>1:
    ip = argv[1]
    token = argv[2]
else:
    # Specify the IP address and token of the bulb. If you want to run script separately.
    ip = "192.168.0.101"  # IP of your bulb
    token = "41795d2ecc02d8e0c07ed363b9f77512"  # Token of the bulb

# Создайте объект лампочки
light = Yeelight(ip, token)

# print(light)
# help(light)
# argv=[1,'mode1']

if len(argv) > 1:
    if argv[3]=="on": # Turn On
        light.on()
    elif argv[3]=="off":
        light.off()
    elif argv[3]=="toggle":
        light.toggle()
    
    elif argv[3]=="mode1": # simple middle light
        light.on()
        light.set_color_temp(3500)  # warmth
        light.set_brightness(100)   # brightness

    elif argv[3]=="mode2": # fast color change
        light.on()
        flow_params = "1000, 1, 16711680, 100, 1000, 1, 65280, 100, 1000, 1, 255, 100"
        response = light.send("start_cf", [0, 0, flow_params])
        print("Color flow started:", response)        

    elif argv[3]=="mode3": # slow color change
        light.on() 
        flow_params = "2000, 1, 16744576, 100, 2000, 1, 16711680, 100, 2000, 1, 16753920, 100, 2000, 1, 16776960, 100, 2000, 1, 8453888, 100, 2000, 1, 65535, 100, 2000, 1, 255, 100, 2000, 1, 8388736, 100, 2000, 1, 16711935, 100, 2000, 1, 16761035, 100, 2000, 1, 16744576, 100"
        response = light.send("start_cf", [0, 0, flow_params])
        print("Color flow started:", response)       

    elif argv[3]=="mode4": #  TORCH
        light.on()
        light.set_color_temp(2000)  # Set warm light
        print("The torch has been lit.")

        try:
            while True:
                brightness = random.randint(60, 100)  # Changing brightness
                light.set_brightness(brightness)
                time.sleep(random.uniform(0.1, 0.3))  # Set speed of brightness change
        except KeyboardInterrupt:
            light.off()  
