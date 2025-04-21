import time
from miio import Yeelight
from datetime import datetime, timedelta
from sys import argv

# If IP and token are passed as arguments, use them; otherwise, use default values.
if len(argv) > 2:
    ip = argv[1]
    token = argv[2]
else:
    # Replace with your lamp's IP and token.
    ip = "192.168.0.106"
    token = "c44781bc9ff68a477e980ced7228bdf5"

# Create the lamp object.
light = Yeelight(ip, token)
print(light)

# Average sunrise and sunset times for Moscow by month.
sun_times = {
    1:  {"sunrise": (8, 30), "sunset": (16, 0)},
    2:  {"sunrise": (8, 0),  "sunset": (16, 30)},
    3:  {"sunrise": (7, 30), "sunset": (17, 0)},
    4:  {"sunrise": (7, 0),  "sunset": (18, 0)},
    5:  {"sunrise": (6, 30), "sunset": (19, 0)},
    6:  {"sunrise": (5, 30), "sunset": (20, 0)},
    7:  {"sunrise": (5, 30), "sunset": (20, 0)},
    8:  {"sunrise": (6, 0),  "sunset": (19, 30)},
    9:  {"sunrise": (6, 30), "sunset": (18, 30)},
    10: {"sunrise": (7, 0),  "sunset": (17, 30)},
    11: {"sunrise": (7, 30), "sunset": (16, 30)},
    12: {"sunrise": (8, 0),  "sunset": (16, 0)},
}

def get_sun_times(now):
    """Get sunrise and sunset times for the current month based on preset values."""
    times = sun_times.get(now.month)
    if times:
        sunrise = now.replace(hour=times["sunrise"][0], minute=times["sunrise"][1],
                              second=0, microsecond=0)
        sunset = now.replace(hour=times["sunset"][0], minute=times["sunset"][1],
                             second=0, microsecond=0)
        return sunrise, sunset
    return None, None

def adjust_brightness():
    now = datetime.now()
    sunrise, sunset = get_sun_times(now)
    if not (sunrise and sunset):
        return

    # Define transition period boundaries:
    dusk_start = sunset - timedelta(hours=1)  # start of dusk transition
    dawn_start = sunrise - timedelta(hours=1)   # start of dawn transition

    if dawn_start <= now < sunrise:
        # Dawn: one hour before sunrise, the lamp gradually dims from 100% to 1%.
        total_seconds = (sunrise - dawn_start).total_seconds()
        elapsed_seconds = (now - dawn_start).total_seconds()
        fraction = elapsed_seconds / total_seconds  # from 0 to 1
        brightness = int(100 - fraction * 99)  # 100 at the beginning, 1 at sunrise
        light.on()
        light.set_color_temp(3700)
        # If brightness reaches the minimum, it's better to turn off the lamp (to avoid sending 0).
        if brightness <= 1:
            light.off()
            print("Lamp turned off (dawn).")
        else:
            light.set_brightness(brightness)
            print(f"Lamp turned on. Dimming brightness to {brightness}% (dawn).")
    elif dusk_start <= now < sunset:
        # Dusk: one hour before sunset, the lamp gradually brightens from 1% to 100%.
        total_seconds = (sunset - dusk_start).total_seconds()
        elapsed_seconds = (now - dusk_start).total_seconds()
        fraction = elapsed_seconds / total_seconds  # from 0 to 1
        brightness = int(1 + fraction * 99)  # 1 at the beginning, 100 at sunset
        light.on()
        light.set_color_temp(3700)
        light.set_brightness(brightness)
        print(f"Lamp turned on. Increasing brightness to {brightness}% (dusk).")
    elif sunrise <= now < dusk_start:
        # Daytime: lamp turned off.
        light.off()
        print("Lamp turned off (daytime).")
    else:
        # Night phase (between sunset and dawn transition): lamp at full brightness.
        light.on()
        light.set_color_temp(3700)
        light.set_brightness(100)
        print("Lamp turned on at full brightness (night).")

# Main loop: check the state every 5 minutes.
while True:
    try:
        adjust_brightness()
    except Exception as e:
        print(f"Error adjusting brightness: {e}")
    time.sleep(300)
