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
        self.sprite_window.geometry("250x300")   
        self.sprite_window.lift()
        self.sprite_window.wm_attributes("-topmost", True)

        self.mic_transcriptor = MicTranscription()

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

        self.TryPrintQueue()

        ## Queue next update frame
        self.sprite_window.after(self.frametime, self.Update)

    def TryPrintQueue(self):

        ## Try get any results from transriber without blocking main thread
        try:
            print(self.mic_transcriptor.result_queue.get(False))
        except queue.Empty:
            return

    def ToggleBorder(self):

        ## Sets Border of the window invisible or not
        if (self.toggleBorderValue.get() == 1):
            self.sprite_window.overrideredirect(True)
        else:
            self.sprite_window.overrideredirect(False)

import speech_recognition as sr
import whisper
import queue
import threading
import torch
import numpy as np

class MicTranscription():

    running = True

    def __init__(self):

        ## Init Model Type
        self.audio_model = whisper.load_model("tiny.en")

        ## Init Queues for Threading
        self.audio_queue = queue.Queue()
        self.result_queue = queue.Queue()

        ## Start the threads
        threading.Thread(target=self.record_audio).start()
        threading.Thread(target=self.transcribe_forever).start()
        
    def record_audio(self):

        #load the speech recognizer and set the initial energy threshold and pause threshold
        r = sr.Recognizer()
        r.energy_threshold = 300
        r.pause_threshold = 0.8
        r.dynamic_energy_threshold = True

        ## Grab the mic
        with sr.Microphone(sample_rate=16000) as source:
            print("Say something!")
            while True:

                ## Stop Thread when application is closed
                if not self.running:
                    break

                ## Listen to mic for input
                audio = r.listen(source)

                ## Do stuff to audio
                torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
                audio_data = torch_audio

                ## Put Audio data into the queue to be transcribed
                self.audio_queue.put_nowait(audio_data)


    def transcribe_forever(self):
        while True:

            ## Stop Thread when application is closed
            if not self.running:
                    break

            ## Grab audio from queue
            audio_data = self.audio_queue.get()

            ## Transcribe Audio from data
            result = self.audio_model.transcribe(audio_data, fp16=False, language='english')

            ## Grab the transcribed text and put in results queue
            predicted_text = result["text"]
            self.result_queue.put_nowait("You said: " + predicted_text)


Main()