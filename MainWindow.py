# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from ui_mainwindow import Ui_MainWindow
from math import floor

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent:QtCore.QObject|None = None):
        super().__init__(parent)
        self.setupUi(self)

        # Setup some constants
        self.messageAutoGrowPadding = 30
        self.messageMaximumStep = 2

        # Connect signals
        self.messageField.textChanged.connect(self.resizeField)


    @QtCore.Slot()
    def resizeField(self):
        fm = self.messageField.fontMetrics()
        totalLines = 0

        # Calculate with padding
        messageFieldWidth = self.messageField.width() - self.messageAutoGrowPadding # we have a padding to increase the widget faster.
        avgCharNum = floor(messageFieldWidth / fm.averageCharWidth())

        # Count lines
        lines = self.messageField.toPlainText().splitlines()
        for line in lines:
            totalLines += 1 + (1 * floor(len(line) / avgCharNum))
            if totalLines >= self.messageMaximumStep:
                break # Stop iterating above the number of {self.messageMaximumStep}

        # Set stretch
        spol = self.messageFrame.sizePolicy()
        spol.setVerticalStretch(max(min(totalLines, self.messageMaximumStep), 0))
        self.messageFrame.setSizePolicy(spol)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    qapp = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(qapp.exec())
