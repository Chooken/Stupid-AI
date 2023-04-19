from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPixmap, QPainter, QResizeEvent
from PyQt6.QtCore import Qt, QRectF
import math

class ChickenRenderer(QGraphicsView):

    borderless = False
    fullscreen = False

    def __init__(self) -> None:

        ## Graphics Setup
        self.canvas = QGraphicsScene()
        super(QGraphicsView, self).__init__(self.canvas, None)

        ## Window Setup
        self.setWindowTitle("Stupid - AI Companion")
        self.resize(500,500)
        self.setStyleSheet("background: transparent")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        ## Loading and Placing Images
        self.body_pixmap = self.LoadPixmap("test_ercle", 250, 250)
        self.body = self.canvas.addPixmap(self.body_pixmap)

        self.face_pixmap = self.LoadPixmap("test_face", 250, 250)
        self.face = self.canvas.addPixmap(self.face_pixmap)
        self.face.setTransformOriginPoint(125,125)

    def resizeEvent(self, event: QResizeEvent) -> None:

        super().resizeEvent(event)

        face_offset = 0
        body_offset = 0

        ## Calculate Original Offset
        if (event.oldSize().height() == -1):
            face_offset = self.face.boundingRect().height() + 10
            body_offset = self.body.boundingRect().height() + 10
        else:
            face_offset = event.oldSize().height() - self.face.pos().y()
            body_offset = event.oldSize().height() - self.body.pos().y()

        ## Sets New Position
        self.body.setPos(10, self.height() - body_offset)
        self.face.setPos(10, self.height() - face_offset)

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
        
        self.face.moveBy(0, self.SinPos(ms_since_startup, 2, 0.5, 0.2))
        self.body.moveBy(0, self.SinPos(ms_since_startup, 2, 0, 0.2))
        self.face.setRotation(self.SinPos(ms_since_startup, 4, 0, 45))

    def SinPos(self, ms_since_startup: int, period_in_seconds: float, offset_in_seconds: float, magnitude: float) -> float:
        return math.sin(((ms_since_startup - (offset_in_seconds * 1000)) * 0.001) / period_in_seconds * 2) * magnitude

    def setState(self, index: int):

        if (index == 0):
            self.resize(500,500)
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
            self.setWindowFlag(Qt.WindowType.WindowTransparentForInput, False) 
        elif (index == 1):
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowTransparentForInput | Qt.WindowType.NoDropShadowWindowHint)
            self.showMaximized()
        else:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowTransparentForInput | Qt.WindowType.NoDropShadowWindowHint)
            self.showFullScreen()
        
        self.show()