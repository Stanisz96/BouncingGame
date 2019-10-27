from tkinter import *
import tkinter.messagebox
import time
import datetime
import random
import pandas as pd



class Stats:
    def __init__(self):
        self.score = StringVar()
        self.score.set('0')
        self.speed = StringVar()
        self.speed.set('40')
        self.level = StringVar()
        self.level.set('0')
        self.points = StringVar()
        self.points.set('10')
        self.h_score = StringVar()
        self.h_score.set('0')
        self.h_level = StringVar()
        self.h_level.set('0')

    def reset(self):
        self.score.set('0')
        self.speed.set('40')
        self.level.set('0')
        self.points.set('10')

    def addPoints(self):
        self.score.set(str(int(self.score.get()) + int(self.points.get())))
    def levelUp(self):
        self.speed.set(str(int(self.speed.get()) + 1))
        self.points.set(str(int(self.points.get()) + 2))
        self.level.set(str(int(self.level.get()) + 1))
        self.level_up = False
    def updateStats(self):
        if int(self.score.get()) > int(self.h_score.get()):
            self.h_score.set(self.score.get())
        if int(self.level.get()) > int(self.h_level.get()):
            self.h_level.set(self.level.get())

    def readData(self):
        try:
            file = pd.read_table('data.csv',delimiter=',')
            self.h_score.set(file.get('Score').max())
            self.h_level.set(file.get('Level').max())
        except:
            file = pd.DataFrame({'Score': [self.score.get()],
                                'Level': [self.level.get()],
                                'Data': [datetime.date.today()]})
            file.to_csv("data.csv",index=False)
    def saveData(self):
        try:
            file = pd.DataFrame({'Score': [self.score.get()],
                                 'Level': [self.level.get()],
                                 'Data': [datetime.date.today()]})
            file.to_csv("data.csv", index=False, mode='a', header=False)
        except:
            print("ERROR!")

class GUI(Stats):
    def __init__(self, master, stats):
        super().__init__()
        self.master = master
        self.stats = stats
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
        self.label3 = Label(self.topFrame, textvariable=self.stats.score,height=2,width=12,anchor=W,relief=SUNKEN,padx=4).grid(row=0,column=1)
        self.label4 = Label(self.topFrame, textvariable=self.stats.h_score,height=2,width=12,anchor=W,relief=SUNKEN,padx=4).grid(row=1,column=1)
        ##New Game
        self.new_Game = True
        self.button1 = Button(self.topFrame,width=16,bg="#F7D952",height=1,pady=6,text="NEW GAME",relief=GROOVE,command=self.newGame).grid(row=0,column=2,columnspan=4)
        ##Level up
        self.button2 = Button(self.topFrame, width=8, bg="#4DE67C",height=1,pady=6, text="LevelUp",wraplength=34, relief=GROOVE,command=self.stats.levelUp).grid(row=0, column=6,columnspan=2)
        ##Speed and points information
        self.label5 = Label(self.topFrame, text="SPEED",height=2,width=8,relief=GROOVE).grid(row=1,column=2,columnspan=2)
        self.label5_2 = Label(self.topFrame,textvariable=self.stats.speed,height=2,width=4,relief=GROOVE).grid(row=1,column=4)
        self.label6 = Label(self.topFrame, text="POINTS",height=2,width=8,relief=GROOVE).grid(row=1,column=5,columnspan=2)
        self.label6_2 = Label(self.topFrame,textvariable=self.stats.points,height=2,width=4,relief=GROOVE).grid(row=1,column=7)
        ##Level information
        self.label7 = Label(self.topFrame, text="LEVEL:",height=2,width=9,relief=SUNKEN).grid(row=0,column=8)
        self.label8 = Label(self.topFrame, text="H.LEVEL:",height=2,width=9,relief=SUNKEN).grid(row=1,column=8)
        self.label9 = Label(self.topFrame, textvariable=self.stats.level,height=2,width=10,anchor=W,relief=SUNKEN,padx=4).grid(row=0,column=9)
        self.label10 = Label(self.topFrame, textvariable=self.stats.h_level,height=2,width=10,anchor=W,relief=SUNKEN,padx=4).grid(row=1,column=9)

        # Canvas for game
        self.canvas = Canvas(self.master, width=500,height=550,bd=2,highlightthickness=1,bg="#E7DEFB",highlightbackground="#8BA16E",relief=SUNKEN)
        self.canvas.pack()

    def update_x(self):
        self.x = False

    def newGame(self):
        self.new_Game = True


class Ball(Stats):
    def __init__(self, canvas, color, paddle, stats):
        super().__init__()
        self.stats = stats
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(244,44,256,56, fill=color)
        self.x = random.choice([-int(self.stats.speed.get()) / 10,int(self.stats.speed.get()) / 10])
        self.y = random.choice([-int(self.stats.speed.get()) / 10,int(self.stats.speed.get()) / 10])
        self.change_dir = False
        self.add_points = False
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    def hit_paddle(self):
        ball_pos = self.canvas.coords(self.id)
        paddle_pos = self.paddle.canvas.coords(self.paddle.id)
        if ball_pos[3] >= paddle_pos[1] and ball_pos[3] <= paddle_pos[3]:
            if ball_pos[2] >= paddle_pos[0]+6 and ball_pos[0] <= paddle_pos[2]-6 and self.change_dir == False:
                self.y *= -1
                self.change_dir = True
                self.add_points = True
            else:
                self.add_points = False
        else:
            self.change_dir = False
            self.add_points = False

    def draw(self):
        self.canvas.move(self.id,self.x,self.y)
        ball_pos = self.canvas.coords(self.id)
        if ball_pos[1] <= 0:
            self.y = int(self.stats.speed.get()) / 10
        if ball_pos[3] >= self.canvas_height:
            self.canvas.coords(self.id,[244,44,256,56])
            self.x = 0
            self.y = 0
            self.stats.saveData()
            tkinter.messagebox.showinfo(message="GAME OVER!")
        if ball_pos[0] <= 0:
            self.x = int(self.stats.speed.get()) / 10
        if ball_pos[2] >= self.canvas_width:
            self.x = -int(self.stats.speed.get()) / 10


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

#Create gui and stats object
stats = Stats()
stats.readData()
gui = GUI(root, stats)
root.update()
#Create paddle and ball
paddle = Paddle(gui.canvas,"green")
ball = Ball(gui.canvas,"red",paddle,stats)


while gui.x == True:
    if gui.new_Game == True:
        #delate objects and reset variable
        del ball, paddle
        gui.canvas.delete("all")
        stats.reset()
        #create new objects
        paddle = Paddle(gui.canvas, "green")
        ball = Ball(gui.canvas, "red", paddle,stats)
        gui.new_Game = False
    ball.hit_paddle()
    if ball.add_points == True:
        stats.addPoints()
        stats.updateStats()
    paddle.draw()
    ball.draw()
    gui.master.update_idletasks()
    gui.master.update()
    time.sleep(0.02)

