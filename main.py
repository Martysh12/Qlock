import sys
from datetime import datetime

from PyQt6.QtCore import QPoint, Qt, QTimer
from PyQt6.QtGui import QAction, QActionGroup, QColor, QCursor, QFont, QPainter, QPainterPath
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu

from qlock_config_manager import load_config, save_config
from qlock_renderer import QlockRenderer
from qlock_settings_dialog import QlockSettingsDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.locked = False
        self.is_always_on_top = False
        self.is_like_other_windows = True
        self.is_always_on_bottom = False

        self.setup_window()
        self.setup_widgets()
        self.setup_config(not_renderer=True)

        self.do_set_flags(1)

        self.renderer = QlockRenderer(self.config)

        self.update_label_timer = QTimer()
        self.update_label_timer.timeout.connect(self.update_label)
        self.update_label_timer.start()

        # allow r/unixporn people to create the most absolutely epically epic things i've ever seen
        self.update_config_timer = QTimer()
        self.update_config_timer.timeout.connect(self.setup_config)
        self.update_config_timer.setInterval(int(0.5 * 1000))
        self.update_config_timer.start()

    def setup_window(self):
        self.setWindowTitle("Qlock")
        # self.setGeometry(0, 0, 400, 200)

        # self.setStyleSheet("QMainWindow { background-color: rgb(25, 25, 46); }")

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def setup_widgets(self):
        # self.font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 0)
        # self.font.setBold(True)

        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.menu = QMenu()

        settingsAction = self.menu.addAction("Settings")
        settingsAction.triggered.connect(self.open_settings)

        lockAction = self.menu.addAction("Lock")
        lockAction.setCheckable(True)
        lockAction.triggered.connect(self.lock)

        topBottomActionGroup = QActionGroup(self)
        topBottomActionGroup.setExclusive(True)

        self.menu.addSeparator()

        AOTAction = self.menu.addAction("Always On Top")
        AOTAction.setCheckable(True)
        AOTAction.setChecked(self.is_always_on_top)
        AOTAction.triggered.connect(lambda: self.do_set_flags(0))
        topBottomActionGroup.addAction(AOTAction)

        LOWAction = self.menu.addAction("Like Other Windows")
        LOWAction.setCheckable(True)
        LOWAction.setChecked(self.is_like_other_windows)
        LOWAction.triggered.connect(lambda: self.do_set_flags(1))
        topBottomActionGroup.addAction(LOWAction)

        AOBAction = self.menu.addAction("Always On Bottom")
        AOBAction.setCheckable(True)
        AOBAction.setChecked(self.is_always_on_bottom)
        AOBAction.triggered.connect(lambda: self.do_set_flags(2))
        topBottomActionGroup.addAction(AOBAction)

        self.menu.addSeparator()

        exitAction = self.menu.addAction("Exit")
        exitAction.triggered.connect(self.close)

        self.oldPos = self.pos()

        self.setCentralWidget(self.label)

    def setup_config(self, not_renderer=False):
        self.config = load_config()

        self.setFixedSize(*self.config["size"])

        self.font = QFont(self.config["font_face"], self.config["font_size"])

        self.label.setFont(self.font)
        self.label.setStyleSheet(
            f"QLabel {{ color: rgb{tuple(self.config['text_color'])}; }}"
        )

        if not not_renderer:
            self.renderer.update_config(self.config)

    def paintEvent(self, event=None):
        painter = QPainter(self)

        painter.setOpacity(self.config["opacity"])
        # painter.setBrush(QColor(*self.config["background_color"]))
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(
            self.rect().x() - 1,
            self.rect().y() - 1,
            self.rect().width() + 1,
            self.rect().height() + 1,
            *self.config["radius"]
        )

        painter.fillPath(path, QColor(*self.config["background_color"]))

    def mousePressEvent(self, event):
        if not self.locked:
            self.oldPos = event.globalPosition()

    def mouseMoveEvent(self, event):
        if not self.locked:
            delta = event.globalPosition() - self.oldPos
            delta = QPoint(int(delta.x()), int(delta.y()))

            self.move(self.x() + delta.x(), self.y() + delta.y())

            self.oldPos = event.globalPosition()

    def contextMenuEvent(self, event):
        self.menu.popup(QCursor.pos())

    def update_label(self):
        now = datetime.now()
        self.label.setText(self.renderer.render(now))

    def open_settings(self):
        dialog = QlockSettingsDialog()
        dialog.exec()
        self.config = load_config()

    def lock(self, checked):
        self.locked = checked

    def do_set_flags(self, what):
        new_flags = Qt.WindowType.FramelessWindowHint #| Qt.WindowType.Tool

        self.is_always_on_top = False
        self.is_like_other_windows = False
        self.is_always_on_bottom = False

        if what == 0:
            new_flags |= Qt.WindowType.WindowStaysOnTopHint
            self.is_always_on_top = True
        elif what == 1:
            new_flags |= 0 # None to add.
            self.is_like_other_windows = True
        elif what == 2:
            new_flags |= Qt.WindowType.WindowStaysOnBottomHint
            self.is_always_on_bottom = True

        # QT always adds 1 to the window flags. I'm presuming it's just adding Qt.WindowType.Window.
        if self.windowFlags() != (new_flags | Qt.WindowType.Window):
            self.setWindowFlags(new_flags)
            self.show()

app = QApplication(sys.argv)

window = MainWindow()
window.show()
# Start the event loop.
app.exec()
