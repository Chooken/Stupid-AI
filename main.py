import tkinter 
from tkinter import ttk
import math

class Main:

    fps = 24
    frametime = math.floor(1000 / fps)
    
    startup_ms_max = math.pi * 2000000

    def __init__(self):
        ## Initialise Main Window (Controls)
        self.root = tkinter.Tk()
        self.root.title("Stupid - AI Companion")
        self.root.geometry("250x250")

        ## Initialise Sprite Window (Bot Window)
        self.sprite_window = tkinter.Toplevel(self.root)
        self.sprite_window.title("Stupid - AI Companion")
        self.sprite_window.geometry("250x250")

        ## Initialise the time since program start (ms)
        self.ms_since_startup = tkinter.IntVar(value=0)
        
        ## DEBUG VISUALS
        self.label = ttk.Label(self.sprite_window, textvariable=self.ms_since_startup)
        self.label.pack()

        ## Initialise Update Loop
        self.root.after(self.frametime, self.Update)
        
        ## Start Main Loop
        self.root.mainloop()

    def Update(self):
        ## Update milliseconds since startup
        self.ms_since_startup.set(math.floor((self.ms_since_startup.get() + 1 * self.frametime) % self.startup_ms_max))

        ## DEBUG VISUALS
        self.label.place(y=math.sin(self.ms_since_startup.get() * 0.001) * 110 + 110)

        ## Queue next update frame
        self.root.after(self.frametime, self.Update)

Main()