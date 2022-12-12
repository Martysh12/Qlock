from PyQt6.QtGui import QAction, QActionGroup
from PyQt6.QtWidgets import QMenu

class QlockContextMenu(QMenu):
    def __init__(self, main_window):
        super().__init__()

        settingsAction = self.addAction("Settings")
        settingsAction.triggered.connect(main_window.open_settings)

        lockAction = self.addAction("Lock")
        lockAction.setCheckable(True)
        lockAction.triggered.connect(main_window.lock)

        topBottomActionGroup = QActionGroup(main_window)
        topBottomActionGroup.setExclusive(True)

        self.addSeparator()

        AOTAction = self.addAction("Always On Top")
        AOTAction.setCheckable(True)
        AOTAction.setChecked(main_window.is_always_on_top)
        AOTAction.triggered.connect(lambda: main_window.do_set_flags(0))
        topBottomActionGroup.addAction(AOTAction)

        LOWAction = self.addAction("Like Other Windows")
        LOWAction.setCheckable(True)
        LOWAction.setChecked(main_window.is_like_other_windows)
        LOWAction.triggered.connect(lambda: main_window.do_set_flags(1))
        topBottomActionGroup.addAction(LOWAction)

        AOBAction = self.addAction("Always On Bottom")
        AOBAction.setCheckable(True)
        AOBAction.setChecked(main_window.is_always_on_bottom)
        AOBAction.triggered.connect(lambda: main_window.do_set_flags(2))
        topBottomActionGroup.addAction(AOBAction)

        self.addSeparator()

        exitAction = self.addAction("Exit")
        exitAction.triggered.connect(main_window.close)
