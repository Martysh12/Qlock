import sys
from datetime import datetime

from PyQt6.QtCore import QPoint, Qt, QTimer
from PyQt6.QtGui import QAction, QActionGroup, QColor, QCursor, QFont, QPainter, QPainterPath
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu, QVBoxLayout, QWidget

from qlock_config_manager import load_config, save_config
from qlock_renderer import QlockRenderer
from qlock_settings_dialog import QlockSettingsDialog
from qlock_context_menu import QlockContextMenu


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

        self.update_labels_timer = QTimer()
        self.update_labels_timer.timeout.connect(self.update_labels)
        self.update_labels_timer.start()

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

        self.main_widget = QWidget()

        self.labels_column = QVBoxLayout()

        self.hello_label = QLabel("")
        self.hello_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labels_column.addWidget(self.hello_label)

        self.main_label = QLabel("")
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labels_column.addWidget(self.main_label)

        self.date_label = QLabel("")
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labels_column.addWidget(self.date_label)

        self.main_widget.setLayout(self.labels_column)

        self.menu = QlockContextMenu(self)

        self.oldPos = self.pos()

        self.setCentralWidget(self.main_widget)

    def setup_config(self, not_renderer=False):
        self.config = load_config()

        self.setFixedSize(*self.config["size"])

        self.font = QFont(self.config["font_face"], self.config["font_size"])


        for i in (self.hello_label, self.main_label, self.date_label):
            i.setFont(self.font)

            i.setStyleSheet(
                f"QLabel {{ color: rgb{tuple(self.config['text_color'])}; }}"
            )

        if not not_renderer:
            self.renderer.update_config(self.config)
            self.repaint()

    def paintEvent(self, event=None):
        painter = QPainter(self)

        painter.setOpacity(self.config["opacity"])
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

    def update_labels(self):
        now = datetime.now()
        self.hello_label.setText(self.renderer.render_hello(now))
        self.main_label.setText(self.renderer.render_clock(now))
        self.date_label.setText(self.renderer.render_date(now))

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
