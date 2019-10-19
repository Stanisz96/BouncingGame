from tkinter import *
import tkinter.messagebox
import time
import random

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
label1 = Label(topFrame, text="SCORE:",height=2,width=9,relief=SUNKEN).grid(row=0,column=0)
label2 = Label(topFrame, text="H.SCORE:",height=2,width=9,relief=SUNKEN).grid(row=1,column=0)
label3 = Label(topFrame, text="XX",height=2,width=12,anchor=W,relief=SUNKEN,padx=4).grid(row=0,column=1)
label4 = Label(topFrame, text="YY",height=2,width=12,anchor=W,relief=SUNKEN,padx=4).grid(row=1,column=1)
##New Game
button1 = Button(topFrame,width=24,bg="#F7D952",pady=8,text="NEW GAME",relief=GROOVE).grid(row=0,column=2,columnspan=2)
##Speed and points information
label5 = Label(topFrame, text=" SPEED:",height=2,width=12,relief=GROOVE,anchor=W).grid(row=1,column=2)
label6 = Label(topFrame, text=" POINTS:",height=2,width=12,relief=GROOVE,anchor=W).grid(row=1,column=3)
##Level information
label7 = Label(topFrame, text="LEVEL:",height=2,width=9,relief=SUNKEN).grid(row=0,column=4)
label8 = Label(topFrame, text="H.LEVEL:",height=2,width=9,relief=SUNKEN).grid(row=1,column=4)
label9 = Label(topFrame, text="XX",height=2,width=12,anchor=W,relief=SUNKEN,padx=4).grid(row=0,column=5)
label10 = Label(topFrame, text="YY",height=2,width=12,anchor=W,relief=SUNKEN,padx=4).grid(row=1,column=5)


# Canvas for game
canvas = Canvas(root, width=500,height=500,bd=2,highlightthickness=1,bg="#E7DEFB",highlightbackground="#8BA16E",relief=SUNKEN)
canvas.pack()
root.update()


class Ball:
    def __init__(self,canvas,color,paddle):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(244,44,256,56, fill=color)
        #self.canvas.move(self.id,43,93)
        self.x = random.choice([-4,4])
        self.y = random.choice([-4,4])
        self.change_dir = False
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    def hit_paddle(self):
        ball_pos = self.canvas.coords(self.id)
        paddle_pos = self.paddle.canvas.coords(self.paddle.id)
        if ball_pos[3] >= paddle_pos[1] and ball_pos[3] <= paddle_pos[3]:
            if ball_pos[2] >= paddle_pos[0]+6 and ball_pos[0] <= paddle_pos[2]-6 and self.change_dir == False:
                self.y *= -1
                self.change_dir = True
            else: pass
        else: self.change_dir = False

    def draw(self):
        self.canvas.move(self.id,self.x,self.y)
        ball_pos = self.canvas.coords(self.id)
        if ball_pos[1] <= 0:
            self.y = 4
        if ball_pos[3] >= self.canvas_height:
            self.canvas.coords(self.id,[244,44,256, 56])
            self.x = 0
            self.y = 0
            tkinter.messagebox.showinfo(message="GAME OVER!")
        if ball_pos[0] <= 0:
            self.x = 4
        if ball_pos[2] >= self.canvas_width:
            self.x = -4


class Paddle:
    def __init__(self,canvas,color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0,120,15, fill=color)
        self.canvas.move(self.id,190,340)
        self.x = 0
        self.y = 0
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all("<KeyPress-Left>",self.leftKey)
        self.canvas.bind_all("<KeyPress-Right>", self.rightKey)
        self.canvas.bind_all("<KeyPress-Up>", self.upKey)
        self.canvas.bind_all("<KeyPress-Down>", self.downKey)
        self.canvas.bind_all("<KeyRelease-Left>",self.let_right_Release)
        self.canvas.bind_all("<KeyRelease-Right>", self.let_right_Release)
        self.canvas.bind_all("<KeyRelease-Up>", self.up_down_Release)
        self.canvas.bind_all("<KeyRelease-Down>", self.up_down_Release)

    def draw(self):
        self.canvas.move(self.id,self.x,self.y)
        paddle_pos = self.canvas.coords(self.id)
        if paddle_pos[1] <= 0:
            self.y = 0
        if paddle_pos[3] >= self.canvas_height:
            self.y = 0
        if paddle_pos[0] <= 0:
            self.x = 0
        if paddle_pos[2] >= self.canvas_width:
            self.x = 0

    def leftKey(self, event):
        paddle_pos = self.canvas.coords(self.id)
        if paddle_pos[0] >= 0:
            self.x = -3
        else:
            self.x = 0
    def rightKey(self, event):
        paddle_pos = self.canvas.coords(self.id)
        if paddle_pos[2] <= self.canvas_width:
            self.x = 3
        else:
            self.x = 0
    def upKey(self, event):
        paddle_pos = self.canvas.coords(self.id)
        if paddle_pos[1] >= 0:
            self.y = -3
        else:
            self.y = 0
    def downKey(self, event):
        paddle_pos = self.canvas.coords(self.id)
        if paddle_pos[3] <= self.canvas_height:
            self.y = 3
        else:
            self.y = 0
    def let_right_Release(self, event):
        self.x *= 0.3
    def up_down_Release(self, event):
        self.y *= 0.3


paddle = Paddle(canvas,"green")
ball = Ball(canvas,"red",paddle)


while x == True:
    ball.hit_paddle()
    paddle.draw()
    ball.draw()
    root.update_idletasks()
    root.update()
    time.sleep(0.02)