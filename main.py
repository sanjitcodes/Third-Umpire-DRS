# SANJIT ANAND 

import tkinter
from tkinter.constants import ANCHOR
import cv2 
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import imutils
import time
import numpy as np

# Width and height of our main screen
SET_WIDTH = 1000
SET_HEIGHT = 650

# Tkineter GUI starts here
window = tkinter.Tk()
window.title("SANJIT's Third Umpire Decision Review System")

cv_img = cv2.cvtColor(cv2.imread("media/drs2.png"),cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width = SET_WIDTH, height = SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image = photo)
canvas.pack()

stream = (cv2.VideoCapture("clips/clip1.mp4"))
flag = True
# Functions
def play(speed):
    global flag
    print(f"You clicked on play, Speed is {speed}")

    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    
    # IMPORTANT LINE to convert frame back to rgb
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image = frame, anchor = tkinter.NW)

    if flag:
        canvas.create_text(120, 25, fill = "red", font="Times 20 italic bold", text = "Decision Pending")
    flag = not flag

def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is Out")

def not_out():
    thread = threading.Thread(target=pending, args=("not out", ))
    thread.daemon = 1
    thread.start()
    print("Player is Not Out")

def pending(decision):
    # 1. Display Decision Pending screen
    frame = cv2.cvtColor(cv2.imread("media/pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image = frame, anchor = tkinter.NW)
    # 2. Wait for 2 sec
    time.sleep(2)
    # 3. Diplay Out / Not Out screen
    if decision == 'out':
        decision_img = "media/out.png"
    else:
        decision_img = "media/not_out.png"

    frame = cv2.cvtColor(cv2.imread(decision_img), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image = frame, anchor = tkinter.NW)

# Buttons
btn = tkinter.Button(window, text = " << Previous (fast)", width= 50, command = partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text = " << Previous (slow)", width= 50, command = partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text = " >> Next (slow)", width= 50, command = partial(play, 1))
btn.pack()

btn = tkinter.Button(window, text = " >> Next (fast)", width= 50, command = partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text = " Decision Out", width= 50, command = out)
btn.pack()

btn = tkinter.Button(window, text = " Decision Not Out", width= 50, command = not_out)
btn.pack()

window.mainloop()