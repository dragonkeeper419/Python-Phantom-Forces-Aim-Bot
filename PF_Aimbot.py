# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 
#  Currently Set for 2560x1440 Monitor
# 
#  Use At Own Risk. It Is Your Fault If Banned or Terminated
# 
#  Requires Ballistic Tracker Attachment To Function
# 
#  Works Best With Low Recoil, High Fire Rate Weapons
# 
#  Use Fullscreen Option
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 
Monitor_Size = [2560, 1440] # Set This to you Monitor Size [Width, Height] in pixels. 
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import numpy as np
import cv2
import time
from math import dist
import keyboard
from pynput import mouse



loop_time = time.time()
w = int(Monitor_Size[0] / 4)
h = int(Monitor_Size[1] / 4)
crosshair_x = (w/2)
crosshair_y = (h/2)

fullmon_x = Monitor_Size[0] / 2
fullmon_y = Monitor_Size[1] / 2


#   scale for which the mouse is moved relative to Mouse DPI and game sensitivity
scale = 0.05


#   Settings for Text display of FPS on OpenCV window
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 25)
fontScale = 1
fontColor = (0,0,255)
thickness = 2
lineType = 2

dist_x = 0
dist_y = 0
status = False

# importing individual modules apparently increases performance a little
from win32gui import GetWindowDC, ReleaseDC, DeleteObject
from win32ui import CreateBitmap, CreateDCFromHandle
from win32con import SRCCOPY, MOUSEEVENTF_MOVE, MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
from win32api import mouse_event
from numpy import array, frombuffer, ascontiguousarray
from cv2 import GaussianBlur, inRange, findContours, boundingRect, rectangle, line, putText, imshow, waitKey, destroyAllWindows, RETR_LIST, CHAIN_APPROX_SIMPLE
from time import sleep, time

# Color range for Ballistic Tracker headshot square
lower = np.array([175, 245, 100], dtype="uint8")
upper = np.array([189, 255, 255], dtype="uint8")

maxDif = 5


off_set_x = int(w*1.5)
off_set_y = int(h*1.5)


def captureWindow():
    status = False
    # time at start of loop
    loop_time = time()
    # If mouse has side buttons, you can assign 0 and 9 to 2 of them and allow easier on/off of Aim Bot
    while 1:
        try:
            if keyboard.is_pressed('0'):
                status = True
        except:
            pass
        while status:
            try:
                if keyboard.is_pressed('9'):
                    status = False
            except:
                pass
            

         
            #  Capture wanted portion of screen
            hwnd = None
            wDC = GetWindowDC(hwnd)
            dcObj=CreateDCFromHandle(wDC)
            cDC=dcObj.CreateCompatibleDC()
            dataBitMap = CreateBitmap()
            dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
            cDC.SelectObject(dataBitMap)
            cDC.BitBlt((0,0),(w, h) , dcObj, (off_set_x, off_set_y), SRCCOPY)


            signedIntsArray = dataBitMap.GetBitmapBits(True)
            img = frombuffer(signedIntsArray, dtype='uint8')
            img.shape = (h, w, 4)

            # Free Resources
            dcObj.DeleteDC()
            cDC.DeleteDC()
            ReleaseDC(hwnd, wDC)
            DeleteObject(dataBitMap.GetHandle())


            img = img[...,:3]
            img = ascontiguousarray(img)

            # Creates mask of capture image to only show the colors of the tracker
            mask = inRange(img, lower, upper)

            # Draws box around tracker to give position of tracker
            contours, heichary = findContours(image=mask, mode=RETR_LIST, method=CHAIN_APPROX_SIMPLE)
            contourIMG = img

            # Gives x and y, and width and height of the box drawn around tracker
            for c in contours:
                (cx,cy,cw,ch) = boundingRect(c)

            # If there are too many boxes drawn for the tracker (ex. sun has same color and characters in specific lighting), it won't move mouse
            if 0<len(contours)<6:
                # Checks if width and height are too big or small, if so it will not move mouse
                if 5<cw<20 and 5<ch<20:
                    # Draw box around Tracker for Visual
                    rectangle(contourIMG, (cx,cy), (cx+cw,cy+ch), (255,0,0),2)

                    # Gets center of box
                    center_x, center_y = cx+(cw/2), cy+(ch/2)

                    # Pixel distance from crosshair to tracker
                    dist_x, dist_y = center_x-crosshair_x, center_y-crosshair_y

                    # Calculates how to move mouse, and if it still needs to moves when the values are below +/- 1, it will set to +/- 1
                    move_x, move_y = dist_x * scale, dist_y * scale
                    if dist_x > 3:
                        if 0.2 < move_x < 1:
                            move_x = 1
                        elif -0.2 > move_x > -1:
                            move_x = -1
                    if dist_y > 3:
                        if 0.2 < move_y <  1:
                            move_y = 1
                        elif -0.2 > move_y > -1:
                            move_y = -1

                    # Draw lines from crosshair to tracker
                    line(contourIMG, (int(crosshair_x), int(crosshair_y)), (int(center_x), int(center_y)), (1,250,1), thickness=3)

                    # Move mouse to tracker box
                    mouse_event(MOUSEEVENTF_MOVE, int(move_x), int(move_y), 0, 0)





                    # # # # # # # # # # # # # # Uncomment to Enable Auto-Fire # # # # # # # # # # # # # #

                    # if abs(crosshair_x - center_x)<maxDif and abs(crosshair_y - center_y)<maxDif:
                    #     mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    #     sleep(0.05)
                    #     mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                    #     status = False

                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


        


    
            # Display FPS on Window
            putText(contourIMG,str(round(1 / (time() - loop_time)))+' FPS',
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)

            # Creates Window to show what Aim Bot is seeing
            imshow('Aimbot', contourIMG)

            # Reset time of beggining of loop
            loop_time = time()

            # Allows you to close Aimbot by focusing window and pressing 'q'
            if waitKey(1) == ord('q'):
                destroyAllWindows()
                break
        # Allows you to close Aimbot by focusing window and pressing 'q'        
        if waitKey(1) == ord('q'):
            destroyAllWindows()
            break

# Function to call Program
captureWindow()




