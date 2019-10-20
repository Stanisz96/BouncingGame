from tkinter import *
import tkinter.messagebox
import time
import random



class GUI:
    def __init__(self,master):
        self.master = master
        # Properly closed window
        self.x = True
        self.master.protocol("WM_DELETE_WINDOW", self.update_x)
        # Top frame with informations
        self.topFrame = Frame(self.master,bd=3, relief=GROOVE)
        self.topFrame.pack(pady=2)

        #Top frame contains
        ##Score information
        self.label1 = Label(self.topFrame, text="SCORE:",height=2,width=8,relief=SUNKEN).grid(row=0,column=0)
        self.label2 = Label(self.topFrame, text="H.SCORE:",height=2,width=8,relief=SUNKEN).grid(row=1,column=0)
        self.label3 = Label(self.topFrame, text="XX",height=2,width=12,anchor=W,relief=SUNKEN,padx=4).grid(row=0,column=1)
        self.label4 = Label(self.topFrame, text="YY",height=2,width=12,anchor=W,relief=SUNKEN,padx=4).grid(row=1,column=1)
        ##New Game
        self.new_Game = False
        self.button1 = Button(self.topFrame,width=24,bg="#F7D952",pady=8,text="NEW GAME",relief=GROOVE,command=self.newGame).grid(row=0,column=2,columnspan=2)
        ##Speed and points information
        self.label5 = Label(self.topFrame, text=" SPEED:",height=2,width=12,relief=GROOVE,anchor=W).grid(row=1,column=2)
        self.label6 = Label(self.topFrame, text=" POINTS:",height=2,width=12,relief=GROOVE,anchor=W).grid(row=1,column=3)
        ##Level information
        self.label7 = Label(self.topFrame, text="LEVEL:",height=2,width=9,relief=SUNKEN).grid(row=0,column=4)
        self.label8 = Label(self.topFrame, text="H.LEVEL:",height=2,width=9,relief=SUNKEN).grid(row=1,column=4)
        self.label9 = Label(self.topFrame, text="XX",height=2,width=12,anchor=W,relief=SUNKEN,padx=4).grid(row=0,column=5)
        self.label10 = Label(self.topFrame, text="YY",height=2,width=12,anchor=W,relief=SUNKEN,padx=4).grid(row=1,column=5)

        # Canvas for game
        self.canvas = Canvas(self.master, width=500,height=500,bd=2,highlightthickness=1,bg="#E7DEFB",highlightbackground="#8BA16E",relief=SUNKEN)
        self.canvas.pack()

    def update_x(self):
        self.x = False

    def newGame(self):
        self.new_Game = True


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
            #tkinter.messagebox.showinfo(message="GAME OVER!")
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
        self.canvas.bind_all("<KeyRelease-Left>",self.leftRelease)
        self.canvas.bind_all("<KeyRelease-Right>", self.rightRelease)
        self.canvas.bind_all("<KeyRelease-Up>", self.upRelease)
        self.canvas.bind_all("<KeyRelease-Down>", self.downRelease)

    def draw(self):
        self.canvas.move(self.id,self.x,self.y)
        paddle_pos = self.canvas.coords(self.id)
        if paddle_pos[1] <= 6:
            self.y = 0
        if paddle_pos[3] >= self.canvas_height-6:
            self.y = 0
        if paddle_pos[0] <= 6:
            self.x = 0
        if paddle_pos[2] >= self.canvas_width-6:
            self.x = 0

    def leftKey(self, event):
        paddle_pos = self.canvas.coords(self.id)
        if paddle_pos[0] >= 6:
            self.x = -3
        else:
            self.x = 0
    def rightKey(self, event):
        paddle_pos = self.canvas.coords(self.id)
        if paddle_pos[2] <= (self.canvas_width - 6):
            self.x = 3
        else:
            self.x = 0
    def upKey(self, event):
        paddle_pos = self.canvas.coords(self.id)
        if paddle_pos[1] >= 6:
            self.y = -3
        else:
            self.y = 0
    def downKey(self, event):
        paddle_pos = self.canvas.coords(self.id)
        if paddle_pos[3] <= (self.canvas_height - 6):
            self.y = 3
        else:
            self.y = 0
    def leftRelease(self, event):
        paddle_pos = self.canvas.coords(self.id)
        if paddle_pos[0] >= 6:
            self.x *= 0.3
        else:
            self.x = 0
    def rightRelease(self, event):
        paddle_pos = self.canvas.coords(self.id)
        if paddle_pos[2] <= (self.canvas_width - 6):
            self.x *= 0.3
        else:
            self.x = 0
    def upRelease(self, event):
        paddle_pos = self.canvas.coords(self.id)
        if paddle_pos[1] >= 6:
            self.y *= 0.3
        else:
            self.y = 0
    def downRelease(self, event):
        paddle_pos = self.canvas.coords(self.id)
        if paddle_pos[3] <= (self.canvas_height - 6):
            self.y *= 0.3
        else:
            self.y = 0


# Main window for application
root = Tk()
root.title("Bounce!")
root.resizable(0, 0)
root.wm_attributes('-topmost', 1)

#Create gui object
gui = GUI(root)
root.update()
#Create paddle and ball
paddle = Paddle(gui.canvas,"green")
ball = Ball(gui.canvas,"red",paddle)


while gui.x == True:
    if gui.new_Game == True:
        del ball, paddle
        gui.canvas.delete("all")
        paddle = Paddle(gui.canvas, "green")
        ball = Ball(gui.canvas, "red", paddle)
        gui.new_Game = False
    ball.hit_paddle()
    paddle.draw()
    ball.draw()
    gui.master.update_idletasks()
    gui.master.update()
    time.sleep(0.02)

