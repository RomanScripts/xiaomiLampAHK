import time
from miio import Yeelight
from datetime import datetime, timedelta
from sys import argv

# If arguments are passed to this script, then we take IP and token from them. Otherwise, use the specified values.
if len(argv) > 1:
    ip = argv[1]
    token = argv[2]
else:
    # Uncomment and replace with your IP and token to start the script without AHK.
    ip = "192.168.31.57"
    token = "2fa6166c978b8f3984bf00a0d79b81c5"

# Create a bulb object
light = Yeelight(ip, token)
print(light)

# Change light based on monthly illumination
# Approximate sunrise and sunset times for Moscow. Replace with data for your city.
sun_times = {
    1:  {"sunrise": (8, 30), "sunset": (16, 0)},
    2:  {"sunrise": (7, 50), "sunset": (17, 0)},
    3:  {"sunrise": (6, 30), "sunset": (18, 0)},
    4:  {"sunrise": (5, 30), "sunset": (19, 0)},
    5:  {"sunrise": (4, 30), "sunset": (20, 0)},
    6:  {"sunrise": (3, 45), "sunset": (21, 15)},
    7:  {"sunrise": (4, 0),  "sunset": (21, 0)},
    8:  {"sunrise": (5, 0),  "sunset": (20, 0)},
    9:  {"sunrise": (6, 0),  "sunset": (19, 0)},
    10: {"sunrise": (7, 0),  "sunset": (18, 0)},
    11: {"sunrise": (7, 50), "sunset": (16, 30)},
    12: {"sunrise": (8, 30), "sunset": (16, 0)},
}

# Function to get sunrise and sunset times
def get_sun_times(month):
    times = sun_times.get(month)
    if times:
        sunrise = datetime.now().replace(hour=times["sunrise"][0], minute=times["sunrise"][1], second=0, microsecond=0)
        sunset = datetime.now().replace(hour=times["sunset"][0], minute=times["sunset"][1], second=0, microsecond=0)
        return sunrise, sunset
    return None, None

# Function to adjust brightness
def adjust_brightness():
    now = datetime.now()
    sunrise, sunset = get_sun_times(now.month)
    
    if sunrise and sunset:
        if now > sunset or now < sunrise:
            # Night: increase brightness
            if now > sunset:
                time_since_sunset = (now - sunset).total_seconds()
            else:
                time_since_sunset = (now + timedelta(days=1) - sunset).total_seconds()
            
            # Maximum brightness 2 hours after sunset
            if time_since_sunset < 2 * 3600:
                brightness = min(100, (time_since_sunset / (2 * 3600)) * 100)
            else:
                brightness = 100
        else:
            brightness = 100
        
        # Set brightness
        print(f"Brightness adjusted to: {int(brightness)}%")
        light.set_brightness(int(brightness))

# Main loop
while True:
    try:
        light.on()
        light.set_color_temp(3700)
        adjust_brightness()
    except Exception as e:
        print(f"Error adjusting brightness: {e}")
    time.sleep(300)  # Check every 5 minutes
