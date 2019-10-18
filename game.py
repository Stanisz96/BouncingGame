from tkinter import *
import time

# Main window of an application
root = Tk()
root.title("Bounce!")
root.resizable(0,0)
root.wm_attributes('-topmost',1)

# Properly closed window
x = True

def update_x():
    global x
    x = False

root.protocol("WM_DELETE_WINDOW", update_x)

# Top frame with informations
topFrame = Frame(root,bd=3, relief=SUNKEN)
topFrame.pack(pady=2)

#Top frame contains
##Score information
label1 = Label(topFrame, text="SCORE:",height=2,width=15,relief=RIDGE).grid(row=0,column=0,sticky=W)
label2 = Label(topFrame, text="H.SCORE:",height=2,width=15,relief=RIDGE).grid(row=1,column=0,sticky=W)
label3 = Label(topFrame, text="XX",height=2,width=14,anchor=W,relief=RIDGE,padx=4).grid(row=0,column=1,sticky=W)
label4 = Label(topFrame, text="YY",height=2,width=14,anchor=W,relief=RIDGE,padx=4).grid(row=1,column=1,sticky=W)
##Separation
label = Label(topFrame,height=4,width=8,bg="green",pady=3).grid(row=0,column=2,rowspan=2)
##Level information
label5 = Label(topFrame, text="LEVEL:",height=2,width=15,relief=RIDGE).grid(row=0,column=3,sticky=E)
label6 = Label(topFrame, text="H.LEVEL:",height=2,width=15,relief=RIDGE).grid(row=1,column=3,sticky=E)
label7 = Label(topFrame, text="XX",height=2,width=14,anchor=W,relief=RIDGE,padx=4).grid(row=0,column=4,sticky=E)
label8 = Label(topFrame, text="YY",height=2,width=14,anchor=W,relief=RIDGE,padx=4).grid(row=1,column=4,sticky=E)


# Canvas for game
canvas = Canvas(root, width=500,height=500,bd=2,highlightthickness=1,bg="#E7DEFB",highlightbackground="#8BA16E",relief=SUNKEN)
canvas.pack()
root.update()



while x == True:
    root.update_idletasks()
    root.update()
    time.sleep(0.02)