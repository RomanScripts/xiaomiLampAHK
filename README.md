# xiaomiLampAHK
Ready to use script to control Xiaomi Lamp with hotkeys using Autohotkey and Python-Miio.  
![Image](https://github.com/user-attachments/assets/d15fc5ad-5ed3-4339-a117-675d829d56ce)
  

# How to use:
1. Download all files. Make sure they all in the same folder.  
2. Replace ip and token of your lamp in MainXiaomiLamp.ahk and run it. (see my video on how to get ip and token ... or python-miio repository ...)

Done!

Ctrl + Win + Q - toggle  
Ctrl + Win + W - regular light  
Ctrl + Win + E - fast colors rotation    
Ctrl + Win + R - slow colors rotation  
Ctrl + Win + T - candle imitation  
Ctrl + Win + Y - special mode. more keyboard/mouse presses = more brightness. Starts to fade out in 5 seconds of inactivity.  (runs keepPressingForBrightness.py)

Ctrl + Win + U - make bulb light brighter the more darker outside based on mid sunrise/sunset time for your city. You can get those values for your city by asking ai chat bot. (runs lightSensorImitation.py)
