from tkinter import *
from PIL import ImageTk,Image
import tkinter.messagebox as tm
import time
import datetime
import random
import pandas as pd
import os.path


def centralize(win,width,height):
    width_win = width
    height_win = height
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width_win / 2)
    y_coordinate = (screen_height / 2) - (height_win / 2)

    win.geometry("%dx%d+%d+%d" % (width_win, height_win, x_coordinate, y_coordinate))


class Stats:
    def __init__(self):
        self.username = StringVar()
        self.username.set('Guest')
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

    def mainData(self,mode,username=None,password=None):
        if mode == "read_stats":
            try:
                file = pd.read_table('./data/main/data.csv',delimiter=',')
                self.h_score.set(file.get('Score').max())
                self.h_level.set(file.get('Level').max())
            except:
                file = pd.DataFrame({'Score': [self.score.get()],
                                    'Level': [self.level.get()],
                                    'Data': [datetime.date.today()],
                                     'Username': [username]})
                file.to_csv("./data/main/data.csv",index=False)

        if mode == "save_stats":
            try:
                file = pd.DataFrame({'Score': [self.score.get()],
                                     'Level': [self.level.get()],
                                     'Data': [datetime.date.today()],
                                     'Username': [username]})
                file.to_csv("./data/main/data.csv", index=False, mode='a', header=False)
            except:
                print("ERROR!")

        if mode == "read_account":
            try:
                file = pd.read_table('./data/main/accdata.csv',delimiter=',')
                file.dropna(inplace = True)
                file = file[file['Username'] == username]['Password'].max()
                return file
            except:
                print("No account created")

        if mode == "save_account":
            try:
                if os.path.exists('./data/main/accdata.csv'):
                    idAccount = pd.read_table('./data/main/accdata.csv', delimiter=',')
                    idAccount = idAccount['Id'].max() + 1
                    idAccount = str(idAccount).zfill(3)
                    file = pd.DataFrame({'Id': [idAccount],
                                    'Username': [username],
                                    'Password': [password],
                                    'Data': [datetime.date.today()]})
                    file.to_csv("./data/main/accdata.csv", index=False, mode='a', header=False)
                else:
                    file = pd.DataFrame({'Id': ['001'],
                                 'Username': [username],
                                 'Password': [password],
                                 'Data': [datetime.date.today()]})
                    file.to_csv("./data/main/accdata.csv", index=False, mode='a')
            except:
                print("Can't create account")

    def individualData(self,mode,username):
        if mode == "create":
            try:
                # Create new file for account
                idAccount = pd.read_table('./data/main/accdata.csv', delimiter=',')
                idAccount = idAccount[idAccount['Username'] == username]['Id'].values[0]
                idAccount = str(idAccount).zfill(3)

                file = pd.DataFrame({'Score': [],
                                     'Level': [],
                                     'Data': []})
                file.to_csv("./data/individual/" + idAccount + ".csv", index=False, mode='a')
            except:
                pass
        if mode == "save":
            if username != None:
                idAccount = pd.read_table('./data/main/accdata.csv', delimiter=',')
                idAccount = idAccount[idAccount['Username'] == username]['Id'].values[0]
                idAccount = str(idAccount).zfill(3)

                file = pd.DataFrame({'Score': [self.score.get()],
                                     'Level': [self.level.get()],
                                     'Data': [datetime.date.today()]})
                file.to_csv("./data/individual/" + idAccount + ".csv", index=False, mode='a', header=False)



class GUI(Stats):
    def __init__(self, master, stats):
        super().__init__()
        self.master = master
        self.stats = stats
        # Variable
        self.stop = 1
        self.x = True
        # Properly closed window
        self.master.protocol("WM_DELETE_WINDOW", self.update_x)

        # Menu
        self.menubar = Menu(self.master)
        ## Account
        self.account = Menu(self.menubar, tearoff=0)
        self.account.add_command(label="Login",command=self.login)
        self.account.add_command(label="Registration", command=self.registration)
        self.menubar.add_cascade(label="Account", menu=self.account)
        ## Pause
        self.menubar.add_command(label="Pause", command=lambda:self.pause("change"))
        ## Set menu visible
        self.master.config(menu=self.menubar)

        # Top frame with informations
        self.topFrame = Frame(self.master,bd=2,bg='#304366')
        self.topFrame.pack(fill=X)
        # Canvas for image background
        self.canvas1 = Canvas(self.topFrame, bd=0, bg='#304366')
        self.canvas1.pack()
        ## Score information
        self.label1 = Label(self.canvas1, image=image03,bd=0,bg='#304366').grid(row=0,column=0,sticky='nse')
        self.label2 = Label(self.canvas1, image=image04,bd=0,bg='#304366').grid(row=2,column=0,sticky='nse')
        self.label3 = Label(self.canvas1, textvariable=self.stats.score,height=2,bg='#304346',relief='ridge',width=8).grid(row=0,column=1,sticky='nswe')
        self.label4 = Label(self.canvas1, textvariable=self.stats.h_score,bg='#304346',relief='ridge',width=8).grid(row=2,column=1,sticky='nswe')
        ## New Game
        self.new_Game = True
        self.button1 = Button(self.canvas1,image=image02,command=self.newGame,bd=0,relief='solid',
                              activebackground='#162032',bg='#304366').grid(row=0,column=3,columnspan=4,sticky='nswe')
        ## Level up
        self.button2 = Button(self.canvas1, image=image01,command=self.stats.levelUp,bd=0,
                              relief='solid',activebackground='#304366',bg='#304366').grid(row=0, column=8,columnspan=2,sticky='nswe')
        ## Border
        self.border1 = Label(self.canvas1, bg='#304366', image=image12).grid(row=1, column=0, columnspan=2,sticky='nswe')
        self.border2 = Label(self.canvas1, bg='#304366',image=image10).grid(row=0,rowspan=3, column=2)
        self.border3 = Label(self.canvas1,bg='#304366',image=image11).grid(row=1,column=3,columnspan=7,sticky='nswe')
        self.border4 = Label(self.canvas1,bg='#304366').grid(row=0,column=7,sticky='nswe')
        self.border5 = Label(self.canvas1, bg='#304366',image=image10).grid(row=0,rowspan=3, column=10)
        self.border6 = Label(self.canvas1, bg='#304366', image=image12).grid(row=1, column=11, columnspan=3,sticky='nse')

        ## Speed and points information
        self.label5 = Label(self.canvas1, image=image05,bd=0,bg='#304366').grid(row=2,column=3,columnspan=2,sticky='nswe')
        self.label5_2 = Label(self.canvas1,textvariable=self.stats.speed,bg='#304346',relief='ridge').grid(row=2,column=5,sticky='nswe')
        self.label6 = Label(self.canvas1, image=image06,bd=0,bg='#304366').grid(row=2,column=6,columnspan=3,sticky='nswe')
        self.label6_2 = Label(self.canvas1,textvariable=self.stats.points,bg='#304346',relief='ridge').grid(row=2,column=9,sticky='nswe')
        ## Level information
        self.label7 = Label(self.canvas1, image=image07,bd=0,bg='#304366').grid(row=0,column=11,sticky='nswe')
        self.label8 = Label(self.canvas1, image=image08,bd=0,bg='#304366').grid(row=2,column=11,sticky='nswe')
        self.label9 = Label(self.canvas1, textvariable=self.stats.level,bg='#304346',relief='ridge',width=8).grid(row=0,column=12,columnspan=2,sticky='nswe')
        self.label10 = Label(self.canvas1, textvariable=self.stats.h_level,bg='#304346',relief='ridge').grid(row=2,column=12,columnspan=2,sticky='nswe')

        # Canvas for game
        self.canvas = Canvas(self.master, width=500,height=550,highlightthickness=1,bg="#304346",highlightbackground="#8BA16E",relief=SUNKEN)
        self.canvas.pack()

    def update_x(self):
        self.x = False

    def newGame(self):
        self.new_Game = True

    def login(self):
        # Setup main configuration
        self.master.attributes("-disabled",1)
        self.pause("stop")
        self.logWindow = Toplevel(self.master,width=1,height=1)
        self.logWindow.lift()
        centralize(self.logWindow,200,140)
        self.logWindow.protocol("WM_DELETE_WINDOW", lambda:self.winDestroy(self.logWindow))
        self.logWindow.title("Login")
        self.logWindow.resizable(0,0)

        # Frame
        self.Frame = Frame(self.logWindow)
        self.Frame.pack(pady=20)
        ## Frame content
        self.label_username = Label(self.Frame, text="Username")
        self.label_password = Label(self.Frame, text="Password")

        self.entry_username = Entry(self.Frame)
        self.entry_password = Entry(self.Frame, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.checkbox = Checkbutton(self.Frame, text="Keep me logged in")
        self.checkbox.grid(columnspan=2)

        self.logbutton = Button(self.Frame, text="Login", command=self.loginCheck)
        self.logbutton.grid(columnspan=2)
        self.Frame.pack()

    def loginCheck(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if password == self.stats.mainData("read_account",username,password):
            tm.showinfo("Login info", "Welcome "+username)
            self.stats.username.set(username)
            self.winDestroy(self.logWindow)
            self.master.attributes("-disabled", 0)
            self.master.title(username)
        else:
            tm.showerror("Login error", "Incorrect username or password")
            self.logWindow.lift()

    def registration(self):
        # Setup main configuation
        self.master.attributes("-disabled",1)
        self.pause("stop")
        self.registWindow = Toplevel(self.master,width=1,height=1)
        self.registWindow.lift()
        centralize(self.registWindow,200,140)
        self.registWindow.protocol("WM_DELETE_WINDOW", lambda:self.winDestroy(self.registWindow))
        self.registWindow.title("Login")
        self.registWindow.resizable(0,0)

        # Frame
        self.Frame2 = Frame(self.registWindow)
        self.Frame2.pack(pady=20)
        ## Frame content
        self.label_username = Label(self.Frame2, text="Username")
        self.label_password = Label(self.Frame2, text="Password")

        self.entry_username = Entry(self.Frame2)
        self.entry_password = Entry(self.Frame2, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.checkbox = Checkbutton(self.Frame2, text="Show signs")
        self.checkbox.grid(columnspan=2)

        self.logbutton = Button(self.Frame2, text="Register", command=self.registrationCheck)
        self.logbutton.grid(columnspan=2)
        self.Frame2.pack()

    def registrationCheck(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if password == None:
            tm.showerror("Registration error", "Incorrect password")
            self.registWindow.lift()
        else:
            self.stats.mainData("save_account",username,password)
            self.stats.individualData("create",username)
            tm.showinfo("Successful registration", "Registration complete! Please login :)")
            self.winDestroy(self.registWindow)
            self.master.attributes("-disabled", 0)

    def pause(self,option):
        if option == "start":
            self.stop = 1
        if option == "stop":
            self.stop = -1
        if option == "change":
            self.stop *= -1

    def winDestroy(self,win):
        self.master.attributes("-disabled", 0)
        win.destroy()
        self.pause("start")


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
            self.stats.mainData("save_stats",self.stats.username.get())
            self.stats.individualData("save",self.stats.username.get())
            tm.showinfo(message="GAME OVER!")
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
root.wm_attributes('-topmost', False)
centralize(root,500,655)

#Images
image01 = PhotoImage(file="images/levelup.gif")
image02 = PhotoImage(file="images/newgame.gif")
image03 = PhotoImage(file="images/score.gif")
image04 = PhotoImage(file="images/hscore.gif")
image05 = PhotoImage(file="images/speed.gif")
image06 = PhotoImage(file="images/points.gif")
image07 = PhotoImage(file="images/level.gif")
image08 = PhotoImage(file="images/hlevel.gif")
image10 = ImageTk.PhotoImage(Image.open("images/border02.jpg"))
image11 = ImageTk.PhotoImage(Image.open("images/border03.jpg"))
image12 = ImageTk.PhotoImage(Image.open("images/border04.jpg"))

#Create gui and stats object
stats = Stats()
stats.mainData("read_stats")
gui = GUI(root, stats)
root.update()

#Create paddle and ball
paddle = Paddle(gui.canvas,"green")
ball = Ball(gui.canvas,"red",paddle,stats)


while gui.x == True:
    if gui.stop == 1:
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
    elif gui.stop == -1:
        pass

    gui.master.update_idletasks()
    gui.master.update()
    time.sleep(0.02)

