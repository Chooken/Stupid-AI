import math
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QCheckBox 
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtCore import QTimer

## Files
from Brain import StupidBrain
from Mic import MicTranscription
from Vocalizer import Vocalizer
from ChickenRenderer import ChickenRenderer

class Main(QMainWindow):

    FPS = 24
    FRAMETIME = math.floor(1000 / FPS)

    startup_ms_max = math.pi * 2000000
    ms_since_startup = 0

    def __init__(self) -> None:
        super(QMainWindow, self).__init__()

        ## Initialise Main Window (Controls)
        self.setWindowTitle("Stupid - AI Companion")
        self.resize(250,250)

        self.ChickenRenderer = ChickenRenderer()

        ## Initalising other files/classes
        self.mic_transcriptor = MicTranscription()
        self.brain = StupidBrain()
        self.vocalizer = Vocalizer()

        ## Root elements
        self.toggleBorder = QCheckBox("Toggle Border", self)
        self.toggleBorder.stateChanged.connect(self.ToggleBorder)
        self.toggleBorder.setGeometry(10,0,100,20)

        self.toggleFullscreen = QCheckBox("Toggle Fullscreen", self)
        self.toggleFullscreen.stateChanged.connect(self.ToggleFullscreen)
        self.toggleFullscreen.setGeometry(10,30,100,20)

        ## Initialise Update Loop
        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(self.FRAMETIME)
        self.timer.timeout.connect(self.Update)
        self.timer.start()

        self.show()
        self.ChickenRenderer.show()

    def End(self):
        ## Tell the threads to stop
        self.mic_transcriptor.running = False

    def closeEvent(self, event: QCloseEvent) -> None:
        self.ChickenRenderer.close()
        return super().closeEvent(event)

    def Update(self) -> None:

         ## Update milliseconds since startup
        self.ms_since_startup = math.floor((self.ms_since_startup + 1 * self.FRAMETIME) % self.startup_ms_max)

        ## Update the Brain
        reply = self.brain.UpdateSentence(self.mic_transcriptor.result_queue, self.brain.SIGNAL_BASED)

        ## Update the Chicken Visuals
        self.ChickenRenderer.Update(self.ms_since_startup)

        ## Vocalize the response from Chat Model
        if (reply != ""):
            self.vocalizer.Say(reply)

    def ToggleBorder(self, state) -> None:

        ## Sets Border of the window invisible or not
        if (state == 2):
            self.ChickenRenderer.SetBorderless(True)
        else:
            self.ChickenRenderer.SetBorderless(False)

    def ToggleFullscreen(self, state) -> None:

        ## Sets Border of the window invisible or not
        if (state == 2):
            self.ChickenRenderer.SetFullscreen(True)
        else:
            self.ChickenRenderer.SetFullscreen(False)

## Application Initialisation
app = QApplication([])
root = Main()

## Starts Loop
app.exec()

## Exits Threads and Application
root.End()
sys.exit()