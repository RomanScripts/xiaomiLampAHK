import time
import sys
import threading
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from miio import Yeelight
from sys import argv

# Settings
min_brightness = 1
max_brightness = 100
initial_brightness = 30
initial_warmth = 3600
brightness = initial_brightness

idleTimeout = 5  # Wait seconds until light reset
lightDecreaseSpeed = 0.3  # Seconds (higher - slower)
brightness_update_interval = 0.2  # Min time between brightness updates (prevents lag)

# If arguments were passed, take ip from them
if len(argv) > 1:
    ip = argv[1]
    token = argv[2]
else:
    # Uncomment and replace with your data if you want to start script separately without ahk.
    ip = "192.168.0.101"
    token = "41625d2ecc02d8e0c07ed363b9f77512"


###################################################

# Connect to Yeelight bulb
light = Yeelight(ip, token)
light.on()
light.set_color_temp(initial_warmth)

last_activity_time = time.time()
last_brightness_update = 0  # Timestamp of last brightness update
lock = threading.Lock()  # Prevents race conditions in brightness updates


def print_progress_bar(value, max_value, length=50):
    """Prints a progress bar to the console."""
    percent = int((value / max_value) * 100)
    bar_length = int((value / max_value) * length)
    bar = "#" * bar_length + "-" * (length - bar_length)
    percent_str = f"{percent} %   "

    sys.stdout.write(f"\r[{bar}] {percent_str}")
    sys.stdout.flush()


def set_brightness(value):
    """Sets the brightness with rate limiting to prevent lag."""
    global brightness, last_brightness_update

    new_brightness = max(min(value, max_brightness), min_brightness)
    current_time = time.time()

    if new_brightness != brightness and (current_time - last_brightness_update) > brightness_update_interval:
        try:
            with lock:  # Ensures only one brightness update at a time
                light.set_brightness(new_brightness)
                brightness = new_brightness
                last_brightness_update = current_time
                print_progress_bar(brightness, max_brightness)
        except Exception:
            pass  # Ignore errors


def monitor_activity():
    """Monitors idle time and gradually decreases brightness."""
    global last_activity_time, brightness
    while True:
        time.sleep(lightDecreaseSpeed)
        if time.time() - last_activity_time > idleTimeout:
            if brightness > 5:
                set_brightness(brightness - 5)
            elif brightness > 1:
                set_brightness(1)


def on_activity():
    """Updates last activity time and increases brightness smoothly."""
    global last_activity_time, brightness
    last_activity_time = time.time()

    if brightness < max_brightness:
        set_brightness(brightness + 1)


def on_press(key):
    """Handles key presses."""
    on_activity()


def on_click(x, y, button, pressed):
    """Handles mouse clicks."""
    if pressed:
        on_activity()


# Set initial brightness
set_brightness(initial_brightness)

# Start monitoring thread
monitor_thread = threading.Thread(target=monitor_activity, daemon=True)
monitor_thread.start()

# Start event listeners
with MouseListener(on_click=on_click), KeyboardListener(on_press=on_press):
    while True:
        time.sleep(1)  # Prevents script from exiting
