# Python-Phantom-Forces-Aim-Bot
Python Computer Vision Aim Bot for Roblox's Phantom Forces

! ! ! USE AT YOUR OWN RISK ! ! !
I will not be at fault if your account is banned

Should be somewhat undetectable by anti-cheat, others players are the problem

Read comments at top of script

Edit for your monitor and then run the python file. I use VSCode to edit and run with debug.

Requires installation of Python 3 and some libraries:
 - win32gui
 - win32ui
 - win32con
 - win32api
 - numpy
 - cv2 (openCV)
 - time
 - math
 - keyboard

 * * * Will NOT Be Making It An EXE File Due To Safety * * *

Tested on a Desktop:
 - Nvidia 3080 10g GPU 
 - Ryzen 5 5900x CPU
 - 32gb 3600mhz c18 RAM
 - 1440p Monitor

On those tested specs, The bot was able to manage 60+ FPS (take image, find target, and move mouse all in 1/60th of a second), sometimes going over 150+ FPS.

How it works (KEEPS LOOPING FOLLOWING STEPS):
 1. Take screenshot of specific area on your screen where center is crosshair, and only capture the amount it needs (Not the whole screen, about 1/4th)
 2. Mask the image to search for the specific colors of the in-game Ballistic Tracker attachment (yellow)
 3. Find contours of the masked image (find where the image goes through drastic change in color, in this case black to white)
 4. Determine if the size of the contour's box is reasonable (box is always the same size, too small or big means its not the tracker)
 5. Get the center of the contour's box from the x, y, width, and height
 6. Find distance between the center and your crosshair (center of screen, but implement tracking for recoil)
 7. Take that distance and multiply it by a scale value (one pixel moved of your mouse does not equal one pixel moved in game (2D plane does not have the same distance as a 3D   space/ center of sphere to edge of sphere)
 8. Move mouse by that value (Won't immediatly get to it, requires more math to determine exact amount. Also may look too suspicious)
 9. {OPTIONALLY} Fire mouse when aiming at target (within a certain distance to center)

Requires Ballistic Tracker attachment
Works best with low recoil, high firerate weapons (Such as L22 and Honey Badger), but can also work with Sniper Rifles (May need a little more fine tuning for One-Shot long range)

If you don't use a 1440p monitor, you will HAVE to change 2 values in the script (at top surrounded by hashtags that reads: Monitor_Size = [2560, 1440]), you also may gain more performance.

List of values for different monitor sizes:
720p - [1280, 720]
1080p - [1920, 1080]
1440p - [2560, 1440]
4k - [3840, 2160]
1080p ultrawide - [2560 or 3840, 1080]
1440p ultrawide - [3440, 1440]

May be updated here-and-there when I decided to come back and work on it some more to optimize performance and accuracy
