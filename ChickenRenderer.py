from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt, QRectF
import math

class ChickenRenderer(QGraphicsView):

    def __init__(self) -> None:

        ## Graphics Setup
        self.canvas = QGraphicsScene()
        super(QGraphicsView, self).__init__(self.canvas, None)

        ## Window Setup
        self.setWindowTitle("Stupid 2 - AI Companion")
        self.resize(500,500)
        self.setStyleSheet("background: transparent")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        ## Loading and Placing Images
        self.body_pixmap = self.LoadPixmap("text_ercle", 250, 250)
        self.body = self.canvas.addPixmap(self.body_pixmap)
        self.body.setPos(10, self.height() - self.body.boundingRect().height() - 10)

        self.face_pixmap = self.LoadPixmap("test_face", 250, 250)
        self.face = self.canvas.addPixmap(self.face_pixmap)
        self.face.setPos(10, self.height() - self.face.boundingRect().height() - 10)

        ## Setting SceneRect to fixed position
        rect = QRectF(self.rect())
        self.fitInView(rect)
        self.setSceneRect(rect)

    def LoadPixmap(self, path: str, xScale: int, yScale: int) -> QPixmap:
        return QPixmap(path).scaled(
            xScale, 
            yScale, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )

    def Update(self, ms_since_startup: int) -> None:

        ## DEBUG VISUALS - Animations
        self.face.setTransformOriginPoint(125,125)
        self.face.moveBy(0, self.SinPos(ms_since_startup, 2, 0.5, 0.2))
        self.body.moveBy(0, self.SinPos(ms_since_startup, 2, 0, 0.2))
        self.face.setRotation(self.SinPos(ms_since_startup, 4, 0, 45))

    def SinPos(self, ms_since_startup: int, period_in_seconds: float, offset_in_seconds: float, magnitude: float) -> float:
        return math.sin(((ms_since_startup - (offset_in_seconds * 1000)) * 0.001) / period_in_seconds * 2) * magnitude

    def SetBorderless(self, state: int) -> None:

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
