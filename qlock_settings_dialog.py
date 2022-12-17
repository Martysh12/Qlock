from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (QColorDialog, QDialog, QDialogButtonBox,
                             QDoubleSpinBox, QFontDialog, QGridLayout, QLabel,
                             QPushButton, QSlider, QSpinBox, QVBoxLayout,
                             QWidget)

from qlock_config_manager import load_config, save_config


class QlockSettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Qlock Settings")
        # self.setFixedSize(500, 250)

        self.current_config = load_config()

        button_box_buttons = (
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Apply
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.grid_layout_container = QWidget()

        self.grid_layout = QGridLayout()

        # =====

        self.text_color_label = QLabel("Text color")
        self.text_color_button = QPushButton("Pick color")
        self.text_color_button.pressed.connect(self.text_color_button_pressed)

        self.grid_layout.addWidget(self.text_color_label, 0, 0)
        self.grid_layout.addWidget(self.text_color_button, 0, 1, 1, 2)

        # =====

        self.background_color_label = QLabel("Background color")
        self.background_color_button = QPushButton("Pick color")
        self.background_color_button.pressed.connect(
            self.background_color_button_pressed
        )

        self.grid_layout.addWidget(self.background_color_label, 1, 0)
        self.grid_layout.addWidget(self.background_color_button, 1, 1, 1, 2)

        # =====

        self.opacity_label = QLabel("Opacity")

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(int(self.current_config["opacity"] * 100))
        self.opacity_slider.valueChanged.connect(self.opacity_slider_value_changed)

        self.opacity_slider_spin_box = QDoubleSpinBox()
        self.opacity_slider_spin_box.setMinimum(0)
        self.opacity_slider_spin_box.setMaximum(1)
        self.opacity_slider_spin_box.setSingleStep(0.1)
        self.opacity_slider_spin_box.setValue(self.current_config["opacity"])
        self.opacity_slider_spin_box.valueChanged.connect(
            self.opacity_slider_spin_box_value_changed
        )

        self.grid_layout.addWidget(self.opacity_label, 2, 0)
        self.grid_layout.addWidget(self.opacity_slider, 2, 1)
        self.grid_layout.addWidget(self.opacity_slider_spin_box, 2, 2)

        # =====

        self.font_label = QLabel("Font")

        self.font_button = QPushButton("Set font")
        self.font_button.pressed.connect(self.font_button_pressed)

        self.grid_layout.addWidget(self.font_label, 3, 0)
        self.grid_layout.addWidget(self.font_button, 3, 1, 1, 2)

        # =====

        self.size_label = QLabel("Size")

        self.size_x_spin_box = QSpinBox()
        self.size_x_spin_box.setMinimum(0)
        self.size_x_spin_box.setMaximum(1000000)
        self.size_x_spin_box.setValue(self.current_config["size"][0])
        self.size_x_spin_box.valueChanged.connect(
            self.size_x_spin_box_value_changed
        )

        self.size_y_spin_box = QSpinBox()
        self.size_y_spin_box.setMinimum(0)
        self.size_y_spin_box.setMaximum(1000000)
        self.size_y_spin_box.setValue(self.current_config["size"][1])
        self.size_y_spin_box.valueChanged.connect(
            self.size_y_spin_box_value_changed
        )

        self.grid_layout.addWidget(self.size_label, 5, 0, 2, 1)
        self.grid_layout.addWidget(self.size_x_spin_box, 5, 1, 1, 2)
        self.grid_layout.addWidget(self.size_y_spin_box, 6, 1, 1, 2)

        # =====
        self.radius_label = QLabel("Radius")

        self.radius_x_spin_box = QSpinBox()
        self.radius_x_spin_box.setMinimum(0)
        self.radius_x_spin_box.setMaximum(1000000)
        self.radius_x_spin_box.setValue(self.current_config["radius"][0])
        self.radius_x_spin_box.valueChanged.connect(
            self.radius_x_spin_box_value_changed
        )

        self.radius_y_spin_box = QSpinBox()
        self.radius_y_spin_box.setMinimum(0)
        self.radius_y_spin_box.setMaximum(1000000)
        self.radius_y_spin_box.setValue(self.current_config["radius"][1])
        self.radius_y_spin_box.valueChanged.connect(
            self.radius_y_spin_box_value_changed
        )

        self.grid_layout.addWidget(self.radius_label, 7, 0, 2, 1)
        self.grid_layout.addWidget(self.radius_x_spin_box, 7, 1, 1, 2)
        self.grid_layout.addWidget(self.radius_y_spin_box, 8, 1, 1, 2)

        # =====

        self.digits_info_label = QLabel("<i>To customise digits, you must edit the conf.json file manually.</i>")
        self.digits_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grid_layout.addWidget(self.digits_info_label, 9, 0, 1, 3)

        # =====

        self.grid_layout_container.setLayout(self.grid_layout)

        self.button_box = QDialogButtonBox(button_box_buttons)
        self.button_box.setCenterButtons(True)

        self.button_box.button(QDialogButtonBox.StandardButton.Save).clicked.connect(
            self.save
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(
            self.apply
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(
            self.close
        )

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.grid_layout_container)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def text_color_button_pressed(self):
        color = QColorDialog.getColor(QColor(*self.current_config["text_color"]))

        if color.isValid():
            self.current_config["text_color"] = color.getRgb()[:3]

    def background_color_button_pressed(self):
        color = QColorDialog.getColor(QColor(*self.current_config["background_color"]))

        if color.isValid():
            self.current_config["background_color"] = color.getRgb()[:3]

    def opacity_slider_value_changed(self, new_value):
        self.current_config["opacity"] = new_value / 100

        self.opacity_slider_spin_box.setValue(self.current_config["opacity"])

    def opacity_slider_spin_box_value_changed(self, new_value):
        self.current_config["opacity"] = new_value

        self.opacity_slider.setValue(int(self.current_config["opacity"] * 100))

    def font_button_pressed(self):
        font, ok = QFontDialog.getFont(
            QFont(self.current_config["font_face"], self.current_config["font_size"])
        )

        if ok:
            self.current_config["font_face"] = font.family()
            self.current_config["font_size"] = font.pointSize()

    def size_x_spin_box_value_changed(self, new_value):
        self.current_config["size"][0] = new_value

    def size_y_spin_box_value_changed(self, new_value):
        self.current_config["size"][1] = new_value

    def radius_x_spin_box_value_changed(self, new_value):
        self.current_config["radius"][0] = new_value

    def radius_y_spin_box_value_changed(self, new_value):
        self.current_config["radius"][1] = new_value

    def apply(self):
        save_config(self.current_config)

    def save(self):
        self.apply()
        self.close()
