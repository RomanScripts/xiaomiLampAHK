﻿#SingleInstance, Force

; Get path to scripts
xiaomiMainLampScript := """" . A_ScriptDir "\xiaomiScripts.py" . """"
pressScriptPath := """" . A_ScriptDir "\keepPressingForBrightness.py" . """"



; Lamp 1
model1 = yeelink.light.color5 
ip1 = 192.168.31.57
token1 = 2fa6166c978b8f3984bf00a0d79b81c5

^#q::run, %comspec% /c miiocli yeelight --model %model1% --ip %ip1% --token %token1% toggle,,hide
^#w::run, %comspec% /c miiocli yeelight --model %model1% --ip %ip1% --token %token1% on && miiocli yeelight --model %model1% --ip %ip1% --token %token1% set_color_temp 3600 && miiocli yeelight --model %model1% --ip %ip1% --token %token1% set_brightness 100,,hide
^#e::Run, cmd /k python.exe %xiaomiMainLampScript% %ip1% %token1% "mode2",,hide
^#r::Run, cmd /k python.exe %xiaomiMainLampScript% %ip1% %token1% "mode3",,hide
^#t::Run, cmd /k python.exe %xiaomiMainLampScript% %ip1% %token1% "mode4"
^#y::Run, cmd /k python.exe %pressScriptPath% %ip1% %token1%


; Lamp 2
model2 = yeelink.light.color5
ip2 = 192.168.32.58
token2 = abcdef1234567890abcdef1234567890

^#a::run, %comspec% /c miiocli yeelight --model %model2% --ip %ip2% --token %token2% toggle,,hide
^#s::run, %comspec% /c miiocli yeelight --model %model2% --ip %ip2% --token %token2% on && miiocli yeelight --model %model2% --ip %ip2% --token %token2% set_color_temp 3600 && miiocli yeelight --model %model2% --ip %ip2% --token %token2% set_brightness 100,,hide
^#d::Run, cmd /k python.exe %xiaomiMainLampScript% %ip2% %token2% "mode2",,hide
^#f::Run, cmd /k python.exe %xiaomiMainLampScript% %ip2% %token2% "mode3",,hide
^#g::Run, cmd /k python.exe %xiaomiMainLampScript% %ip2% %token2% "mode4"
^#h::Run, cmd /k python.exe %pressScriptPath% %ip2% %token2%


; Lamp 3
model3 = yeelink.light.color5
ip3 = 192.168.32.59
token3 = 123456abcdef123456abcdef12345678

^#z::run, %comspec% /c miiocli yeelight --model %model3% --ip %ip3% --token %token3% toggle,,hide
^#x::run, %comspec% /c miiocli yeelight --model %model3% --ip %ip3% --token %token3% on && miiocli yeelight --model %model3% --ip %ip3% --token %token3% set_color_temp 3600 && miiocli yeelight --model %model3% --ip %ip3% --token %token3% set_brightness 100,,hide
^#c::Run, cmd /k python.exe %xiaomiMainLampScript% %ip3% %token3% "mode2",,hide
^#v::Run, cmd /k python.exe %xiaomiMainLampScript% %ip3% %token3% "mode3",,hide
^#b::Run, cmd /k python.exe %xiaomiMainLampScript% %ip3% %token3% "mode4"
^#n::Run, cmd /k python.exe %pressScriptPath% %ip3% %token3%




;;; Other modes example
; run, %comspec% /c miiocli yeelight --model %model% --ip %ip% --token %token% set_rgb 231 57 200,,hide
