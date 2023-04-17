import tkinter 
from tkinter import ttk
import math
from PIL import ImageTk, Image
import copy

class ChickenRenderer():

    def __init__(self, sprite_window):

        ## DEBUG VISUALS
        self.body = Image.open("test_ercle.png").resize((250,250),Image.LANCZOS) 

        self.face = Image.open("test_face.png").resize((250,250),Image.LANCZOS)

        self.sprite = ImageTk.PhotoImage(self.body)  

        self.FaceImage = ImageTk.PhotoImage(self.face)

        self.canvas = tkinter.Canvas(sprite_window, width=250, height=250, bg="black", bd=0, highlightthickness=0, relief='ridge')

        self.body = self.canvas.create_image(125, 125, image=self.sprite)
        self.face = self.canvas.create_image(125, 125, image=self.FaceImage)

        self.canvas.pack(anchor = "w", side = "bottom")

    def Update(self, ms_since_startup):

        ## DEBUG VISUALS
        self.canvas.move(self.face, 0, math.sin((ms_since_startup - 500) * 0.002) * 0.15)
        self.canvas.move(self.body, 0, math.sin(ms_since_startup * 0.002) * 0.2)