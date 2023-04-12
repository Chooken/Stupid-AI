import tkinter 
from tkinter import ttk
import math
from PIL import ImageTk, Image
from sys import platform

class Main:

    fps = 24
    frametime = math.floor(1000 / fps)

    startup_ms_max = math.pi * 2000000
    ms_since_startup = 0

    def __init__(self):
        ## Initialise Main Window (Controls)
        self.root = tkinter.Tk()
        self.root.title("Stupid - AI Companion")
        self.root.geometry("250x250")

        ## Initialise Sprite Window (Bot Window)
        self.sprite_window = tkinter.Toplevel(self.root)
        self.sprite_window.title("Stupid - AI Companion")
        self.sprite_window.geometry("250x250")   
        self.sprite_window.lift()
        self.sprite_window.wm_attributes("-topmost", True)

        if (platform == "windows"): 
            self.sprite_window.wm_attributes("-transparentcolor", "#00ff32")
            self.sprite_window.config(bg='00ff32')
        if (platform == "darwin"): 
            self.sprite_window.wm_attributes("-transparent", True)
            self.sprite_window.config(bg='systemTransparent')
        
        ## DEBUG VISUALS
        image1 = Image.open("test.png").resize((150,150), Image.LANCZOS)
        self.testImage = ImageTk.PhotoImage(image1, width=50, height=50)  

        self.label = ttk.Label(self.sprite_window, image=self.testImage)
        self.label.pack()

        ## Initialise Update Loop
        self.sprite_window.after(self.frametime, self.Update)
        
        ## Start Main Loop
        self.root.mainloop()

    def Update(self):
        ## Update milliseconds since startup
        self.ms_since_startup = math.floor((self.ms_since_startup + 1 * self.frametime) % self.startup_ms_max)

        ## DEBUG VISUALS
        self.label.place(y=math.sin(self.ms_since_startup * 0.001) * 50 + 50)

        ## Queue next update frame
        self.sprite_window.after(self.frametime, self.Update)

Main()