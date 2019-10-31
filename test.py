from tkinter import *
import tkinter.ttk

root = Tk()

style = tkinter.ttk.Style()
style.map("C.TButton",
    foreground=[('pressed', 'red'), ('active', 'blue')],
    background=[('pressed', '!disabled', 'black'), ('active', 'white')]
    )

colored_btn = tkinter.ttk.Button(text="Test", style="C.TButton").pack()

root.mainloop()