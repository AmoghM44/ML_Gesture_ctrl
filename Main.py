import subprocess
from tkinter import *

def callmouse():
    subprocess.Popen('python Mouse.py',shell=True)

def callkeyboard():
    subprocess.Popen('python virtualkeyboard.py',shell=True)

def callmedia():
    subprocess.Popen('python Handgesture.py',shell=True)
def main():
    Mainwin=Tk()
    Mainwin.geometry('700x505')
    Mainwin.title("Detector")
    Mainwin["bg"]='#D9D9D9'
    canvas=Canvas(Mainwin,width=700,height=505)
    canvas.pack()

    bge=PhotoImage(file='./Images/bge.png')
    gge=PhotoImage(file='./Images/gge.png')
    hnd=PhotoImage(file='./Images/HAND.png')
    ges=PhotoImage(file='./Images/GESTURE.png')
    det=PhotoImage(file='./Images/DETECTION.png')
    med=PhotoImage(file='./Images/M.png')
    mou=PhotoImage(file='./Images/Mouse.png')
    key=PhotoImage(file='./Images/key.png')

    canvas.create_image(150,130,image=bge)
    canvas.create_image(550,130,image=gge)
    canvas.create_image(350,50,image=hnd)
    canvas.create_image(350,140,image=ges)
    canvas.create_image(350,230,image=det)

    btn1=Button(canvas,image=med,command=callmedia).place(x=495,y=320)
    btn2=Button(canvas,image=key,command=callkeyboard).place(x=95,y=320)
    btn3=Button(canvas,image=mou,command=callmouse).place(x=290,y=320)

    lbl1=Label(text="Media Control").place(x=500,y=400)
    lbl2=Label(text="Virtual Keyboard").place(x=98,y=400)
    lbl3=Label(text="Virtual Mouse").place(x=301,y=400)


    Mainwin.mainloop()



if __name__== '__main__':
    main()
