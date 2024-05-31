### Import Zone ###
import time
import unicornhathd as unicorn
import numpy as np
from picamera2 import Picamera2
import cv2
from tkinter import *
from tkinter.ttk import *
import os

"""the goal is to calibrate the microscope so we will light up all the leds as once to use it as a conventional microscope
then we are going to stream the video and then you will be able to ajust the screw to change the distance between the glass blade and the lens
"""

### Script ###

## Variables selection with tkinter

# Window configuration
window = Tk()
window.title("Camera acquisition app")
#window.attributes('-fullscreen', True)
window.geometry('640x320')


# Format choice section
lbl = Label(window, text="Record video or shoot picture")
lbl.grid(column=0, row=0)
comboFormat = Combobox(window)
comboFormat['values']= ("Video", "Jpeg", "Png")
comboFormat.current(0)
comboFormat.grid(column=1, row=0)

# Color choice section
lbl2 = Label(window, text="Choose the color of the led array")
lbl2.grid(column=0, row=1)
comboColor = Combobox(window)
comboColor['values']= ("White", "Red", "Green", "Blue")
comboColor.current(0)
comboColor.grid(column=1, row=1)
color=comboColor.get()

# Name of the saved file
fileName = Entry(window,width=10)
fileName.grid(column=0, row=2)

# Section to lauch acquisition
def clicked():
    global format
    global color
    global filenameStr
    format=comboFormat.get()
    color=comboColor.get()
    filenameStr=fileName.get()
    if filenameStr=='':
        filenameStr="default"
    window.quit()
    window.destroy()
lauchButton = Button(window, text="Start acquisition", command=clicked)
lauchButton.grid(column=1, row=3)


window.mainloop()

print(format,color)

## Starting the record

# Setting the color
colorDic = {'White': (255,255,255), 'Red': (255,0,0), 'Green': (0,255,0), 'Blue': (0,0,255)}
unicorn.set_all(*colorDic[color])
unicorn.show()

# acquisition
if format=="Video":
    # camera configuration for video
    picam2=Picamera2()
    picam2.preview_configuration.main.format="RGB888" # good format for the library opencv
    picam2.start()
    running=True
    while running :
        im=picam2.capture_array()
        cv2.imshow("Press ECHAP to exit",im)
        key=cv2.waitKey(1)#
        if key==27:
            running=False
    picam2.stop()
else:  
    # Camera config for picture
    picam2pic=Picamera2()
    camera_config = picam2pic.create_preview_configuration()
    picam2pic.configure(camera_config)
    picam2pic.start()
    if format== "Jpeg":
        time.sleep(2)
        picam2pic.capture_file(filenameStr+".jpg")
    else : # so it is png picture
        time.sleep(2)
        picam2pic.capture_file(filenameStr+".png") 
    picam2pic.stop()


# Ending correctly the program
unicorn.set_all(0,0,0)
unicorn.show()
cv2.destroyAllWindows()

