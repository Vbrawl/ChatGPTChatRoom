# This Python file uses the following encoding: utf-8
from PySide6 import QtWidgets, QtCore, QtGui


class PlainMessageField(QtWidgets.QPlainTextEdit):
    SendMessage = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event:QtGui.QKeyEvent):
        if event.modifiers() not in [QtCore.Qt.ShiftModifier, QtCore.Qt.ControlModifier] and event.key() == QtCore.Qt.Key_Return:
            # (Ctrl|Shift) + Return
            self.SendMessage.emit()
        else:
            super().keyPressEvent(event)
