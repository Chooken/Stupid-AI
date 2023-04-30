from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap, QPainter, QResizeEvent, QTransform
from PyQt6.QtCore import Qt, QRectF
import math

class ChickenRenderer(QGraphicsView):

    borderless = False
    fullscreen = False

    parts: dict[str, QGraphicsPixmapItem] = {}

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
        self.LoadSprites()

        self.DisplaySprite("comb", self.comb_pixmap)
        self.DisplaySprite("wing L", self.wing_L_pixmap)
        self.DisplaySprite("legs", self.legs_pixmap)
        self.DisplaySprite("body", self.body_pixmap)
        self.DisplaySprite("chestpuff small", self.chestpuff_small_pixmap)
        self.DisplaySprite("chestpuff big", self.chestpuff_big_pixmap)
        self.DisplaySprite("chestpuff tiny", self.chestpuff_tiny_pixmap)
        self.DisplaySprite("hairpuff small", self.hairpuff_small_pixmap)
        self.DisplaySprite("hairpuff big", self.hairpuff_big_pixmap)
        self.DisplaySprite("wattle", self.wattle_pixmap)
        self.DisplaySprite("wing R small", self.wing_R_small_pixmap)
        self.DisplaySprite("wing R big", self.wing_R_big_pixmap)

    def DisplaySprite(self, name: str, pixmap: QPixmap):
        self.parts[name] = self.canvas.addPixmap(pixmap)

    def LoadSprites(self) -> None:

        ## Regular Face
        self.regular_face_pixmap = self.LoadPixmap("sprites/chicken_regular_face", 250, 250)
        self.regular_face_highlights_pixmap = self.LoadPixmap("sprites/chicken_regular_face_highlights", 250, 250)
        self.regular_face_eyebrows_pixmap = self.LoadPixmap("sprites/chicken_regular_face_eyebrows", 250, 250)
        self.regular_face_blink_pixmap = self.LoadPixmap("sprites/chicken_happy_face_blink", 250, 250)

        ## Happy Face
        self.happy_face_pixmap = self.LoadPixmap("sprites/chicken_happy_face", 250, 250)
        self.happy_face_highlights_pixmap = self.LoadPixmap("sprites/chicken_happy_face_highlights", 250, 250)
        self.happy_face_eyebrows_pixmap = self.LoadPixmap("sprites/chicken_happy_face_eyebrows", 250, 250)
        self.happy_face_blink_pixmap = self.LoadPixmap("sprites/chicken_happy_face_blink", 250, 250)

        ## Sick Face
        self.sick_face_pixmap = self.LoadPixmap("sprites/chicken_sick_face", 250, 250)
        self.sick_face_therm_pixmap = self.LoadPixmap("sprites/chicken_sick_face_therm", 250, 250)

        ## Sleep Face
        self.sleep_face_pixmap = self.LoadPixmap("sprites/chicken_sleep_face", 250, 250)
        self.sleep_face_eyebrows_pixmap = self.LoadPixmap("sprites/chicken_sleep_face_eyebrows", 250, 250)
        self.sleep_face_z_small_pixmap = self.LoadPixmap("sprites/chicken_sleep_face_z_small", 250, 250)
        self.sleep_face_z_big_pixmap = self.LoadPixmap("sprites/chicken_sleep_face_z_big", 250, 250)

        ## Tired Face
        self.tired_face_pixmap = self.LoadPixmap("sprites/chicken_tired_face", 250, 250)
        self.tired_face_highlights_pixmap = self.LoadPixmap("sprites/chicken_tired_face_highlights", 250, 250)
        self.tired_face_eyebrows_pixmap = self.LoadPixmap("sprites/chicken_tired_face_eyebrows", 250, 250)
        self.tired_face_blink_pixmap = self.LoadPixmap("sprites/chicken_tired_face_blink", 250, 250)

        ## Body
        self.body_pixmap = self.LoadPixmap("sprites/chicken_body", 250, 250)
        self.chestpuff_small_pixmap = self.LoadPixmap("sprites/chicken_chestpuff_small", 250, 250)
        self.chestpuff_big_pixmap = self.LoadPixmap("sprites/chicken_chestpuff_big", 250, 250)
        self.chestpuff_tiny_pixmap = self.LoadPixmap("sprites/chicken_chestpuff_tiny", 250, 250)
        self.comb_pixmap = self.LoadPixmap("sprites/chicken_comb", 250, 250)
        self.hairpuff_small_pixmap = self.LoadPixmap("sprites/chicken_hairpuff_small", 250, 250)
        self.hairpuff_big_pixmap = self.LoadPixmap("sprites/chicken_hairpuff_big", 250, 250)
        self.legs_pixmap = self.LoadPixmap("sprites/chicken_legs", 250, 250)
        self.wattle_pixmap = self.LoadPixmap("sprites/chicken_wattle", 250, 250)
        self.wing_L_pixmap = self.LoadPixmap("sprites/chicken_wing_L", 250, 250)
        self.wing_R_small_pixmap = self.LoadPixmap("sprites/chicken_wing_R_small", 250, 250)
        self.wing_R_big_pixmap = self.LoadPixmap("sprites/chicken_wing_R_big", 250, 250)

    def resizeEvent(self, event: QResizeEvent) -> None:

        super().resizeEvent(event)

        for part in self.parts.values():

            ## Calculate Original Offset
            if (event.oldSize().height() == -1):
                offset = part.boundingRect().height() + 10
            else:
                offset = event.oldSize().height() - part.pos().y()

            ## Sets New Position
            part.setPos(10, self.height() - offset)

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
        
        self.parts["comb"].moveBy(0, self.SinPos(ms_since_startup, 1, 0.5, 0.1))
        self.parts["wing L"].moveBy(0, self.SinPos(ms_since_startup, 1, 0.2, 0.1))
        self.parts["body"].moveBy(0, self.SinPos(ms_since_startup, 1, 0, 0.1))
        self.parts["chestpuff small"].moveBy(0, self.SinPos(ms_since_startup, 1, 0.2, 0.1))
        self.parts["chestpuff big"].moveBy(0, self.SinPos(ms_since_startup, 1, 0.2, 0.1))
        self.parts["chestpuff tiny"].moveBy(0, self.SinPos(ms_since_startup, 1, 0.2, 0.1))
        self.parts["hairpuff small"].moveBy(0, self.SinPos(ms_since_startup, 1, 0.2, 0.1))
        self.parts["hairpuff big"].moveBy(0, self.SinPos(ms_since_startup, 1, 0.2, 0.1))
        self.parts["wattle"].moveBy(0, self.SinPos(ms_since_startup, 1, 0.5, 0.1))
        self.parts["wing R small"].moveBy(0, self.SinPos(ms_since_startup, 1, 0.2, 0.1))
        self.parts["wing R big"].moveBy(0, self.SinPos(ms_since_startup, 1, 0.2, 0.1))

        return

    def SinPos(self, ms_since_startup: int, period_in_seconds: float, offset_in_seconds: float, magnitude: float) -> float:
        return math.sin(((ms_since_startup - (offset_in_seconds * 1000)) * 0.001) / period_in_seconds * 2) * magnitude

    def setState(self, index: int):

        ## Check for Index of state
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