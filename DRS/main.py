import functools
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
# this will make command think as play has no argument.
from functools import partial
import imutils
import threading
import time
stream=cv2.VideoCapture("clip.mp4")
flag=True
def play(speed):
    global flag
    #play the video in reverse.
    frame1=stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES,speed+frame1)

    grabbed,frame=stream.read()
    if not grabbed:
        exit()
    frame=imutils.resize(frame, width=2364,height=1113)
    frame=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(1000,1000,anchor=tkinter.S, image=frame)
    if flag:

        canvas.create_text(900,300,fill="red",font="Times 30 bold",text="Decision Pending")
    flag= not flag
def pending(decision):
    #1.Display decision pending image.
    frame=cv2.cvtColor(cv2.imread("pending.png"),cv2.COLOR_BGR2RGB)

    frame= imutils.resize(frame,width=2364,height=1113)
    #this will create frame into photo image object.
    frame=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(900,1200,anchor=tkinter.S,image=frame)
    
    #2.Wait for 1 second.

    time.sleep(1)

    #3. Display sponser image

    frame=cv2.cvtColor(cv2.imread("sponsor.png"),cv2.COLOR_BGR2RGB)

    frame= imutils.resize(frame,width=2364,height=1113)
    frame=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(900,1200,anchor=tkinter.S,image=frame)

    #4. wait for 1.5 sec
    time.sleep(1)
    #5. display out/notout image.
    if decision=="out":
        decisionImg="out.png"

    else:
        decisionImg='not_out.png'
    frame=cv2.cvtColor(cv2.imread(decisionImg),cv2.COLOR_BGR2RGB)
    frame= imutils.resize(frame,width=2364,height=1113)
    frame=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(900,1200,anchor=tkinter.S,image=frame)
    pass
def out():
    #we use thread because it will help in preventing of blocking.
    #it will control image changing on screen.
    thread=threading.Thread(target=pending,args=('out',))
    thread.daemon=1
    thread.start()
    print("Player is out.")
def not_out():
    thread=threading.Thread(target=pending,args=('not out',))
    thread.daemon=1
    thread.start()
    print("Player is not out.")

SET_WIDTH = 650

SET_HEIGHT = 368
#Tkinter gui starts here.
window= tkinter.Tk()
window.title("Striko Third Umpire Decision Review Kit")
cv_img=cv2.cvtColor(cv2.imread("welcome.png"),cv2.COLOR_BGR2RGB)
canvas=tkinter.Canvas(window, width= 2364, height=1113 )
photo=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
#packing images in canvas
image_on_canvas= canvas.create_image(900,1200,anchor=tkinter.S, image=photo)
canvas.pack()


#Buttons to control playback
btn=tkinter.Button(window,text="<<Previous (fast)",width=50,command=partial(play, -25))
btn.place(x=100, y=20)
btn=tkinter.Button(window,text="<<Previous (slow)",width=50,command=partial(play, -2))
btn.place(x=800, y=20)
btn=tkinter.Button(window,text="Next>> (slow)",width=50,command=partial(play, 2))
btn.place(x=1500, y=20)
btn=tkinter.Button(window,text="Next>> (fast)",width=50 ,command=partial(play, 25))
btn.place(x=100, y=60)
btn=tkinter.Button(window,text="Give Out ",width=50,command=out)
btn.place(x=800, y=60)
btn=tkinter.Button(window,text="Give Not Out ",width=50,command=not_out)
btn.place(x=1500, y=60)

window.mainloop()