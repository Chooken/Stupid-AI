from PyQt6.QtWidgets import QLabel, QWidget, QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt, QRectF
import math

class ChickenRenderer(QGraphicsView):

    def __init__(self):

        ## Graphics Setup
        self.canvas = QGraphicsScene()
        super(QGraphicsView, self).__init__(self.canvas, None)

        ## Window Setup
        self.setWindowTitle("Stupid 2 - AI Companion")
        self.resize(500,500)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent")
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
    
        ## Loading and Placing Images
        self.body_pixmap = QPixmap("test_ercle")
        self.body = self.canvas.addPixmap(self.body_pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.body.setPos(10, self.height() - self.body.boundingRect().height() - 10)

        self.face_pixmap = QPixmap("test_face")
        self.face = self.canvas.addPixmap(self.face_pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.face.setPos(10, self.height() - self.face.boundingRect().height() - 10)

        ## Setting SceneRect to fixed position
        rect = QRectF(self.rect())
        self.fitInView(rect)
        self.setSceneRect(rect)

    def Update(self, ms_since_startup):

        ## DEBUG VISUALS - Animations
        self.face.setTransformOriginPoint(125,125)
        self.face.moveBy(0, self.SinPos(ms_since_startup, 2, 0.5, 0.2))
        self.body.moveBy(0, self.SinPos(ms_since_startup, 2, 0, 0.2))
        self.face.setRotation(self.SinPos(ms_since_startup, 4, 0, 45))

    def SinPos(self, ms_since_startup, period_in_seconds, offset_in_seconds, magnitude):
        return math.sin(((ms_since_startup - (offset_in_seconds * 1000)) * 0.001) / period_in_seconds * 2) * magnitude

    def SetBorderless(self, state):

        if (state):
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowTransparentForInput)
            self.showMaximized()

            self.body.setPos(10, self.height() - self.body.boundingRect().height() - 10)
            self.face.setPos(10, self.height() - self.face.boundingRect().height() - 10)

            ## Setting SceneRect to fixed position
            rect = QRectF(self.rect())
            self.fitInView(rect)
            self.setSceneRect(rect)

            self.show()
        else:
            self.resize(500,500)
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
            self.setWindowFlag(Qt.WindowType.WindowTransparentForInput, False)

            self.body.setPos(10, self.height() - self.body.boundingRect().height() - 10)
            self.face.setPos(10, self.height() - self.face.boundingRect().height() - 10)

            ## Setting SceneRect to fixed position
            rect = QRectF(self.rect())
            self.fitInView(rect)
            self.setSceneRect(rect)

            self.show()
