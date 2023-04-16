import tkinter 
from tkinter import ttk
import math
from PIL import ImageTk, Image
from sys import platform

## Files
from brain import StupidBrain
from mic import MicTranscription
from vocalizer import Vocalizer

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
        self.sprite_window.geometry("250x300")   
        self.sprite_window.lift()
        self.sprite_window.wm_attributes("-topmost", True)

        ## Initalising other files/classes
        self.mic_transcriptor = MicTranscription()
        self.brain = StupidBrain()
        self.vocalizer = Vocalizer()

        if (platform == "win32"): 
            self.sprite_window.wm_attributes("-transparentcolor", "black")
            self.sprite_window.config(bg='black')
        if (platform == "darwin"): 
            self.sprite_window.wm_attributes("-transparent", True)
            self.sprite_window.config(bg='systemTransparent')
        
        ## DEBUG VISUALS
        image1 = Image.open("test_waifu_2.png").resize((250,250),Image.LANCZOS)
        self.testImage = ImageTk.PhotoImage(image1)  

        self.label = ttk.Label(self.sprite_window, image=self.testImage)
        self.label.config(background='black')
        self.label.pack()

        ## Root elements
        self.toggleBorderValue = tkinter.IntVar()
        self.toggleBorder = ttk.Checkbutton(
            self.root, 
            text="Toggle Border", 
            variable=self.toggleBorderValue,
            command=self.ToggleBorder
        )
        self.toggleBorder.pack()

        ## Initialise Update Loop
        self.sprite_window.after(self.frametime, self.Update)
        
        ## Start Main Loop
        self.root.mainloop()

        ## Tell the threads to stop
        self.mic_transcriptor.running = False

    def Update(self):
        ## Update milliseconds since startup
        self.ms_since_startup = math.floor((self.ms_since_startup + 1 * self.frametime) % self.startup_ms_max)

        ## DEBUG VISUALS
        self.label.place(y=math.sin(self.ms_since_startup * 0.001) * 10)

        reply = self.brain.UpdateSentence(self.mic_transcriptor.result_queue, self.brain.SIGNAL_BASED)

        if (reply != ""):
            self.vocalizer.Say(reply)

        ## Queue next update frame
        self.sprite_window.after(self.frametime, self.Update)

    def ToggleBorder(self):

        ## Sets Border of the window invisible or not
        if (self.toggleBorderValue.get() == 1):
            self.sprite_window.overrideredirect(True)
        else:
            self.sprite_window.overrideredirect(False)

Main()