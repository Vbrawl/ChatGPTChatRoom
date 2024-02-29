# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from chatroom import ChatRoom
from ui_mainwindow import Ui_MainWindow
from math import floor

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent:QtCore.QObject|None = None):
        super().__init__(parent)
        self.setupUi(self)

        # Setup some constants
        self.messageAutoGrowPadding = 30
        self.messageMaximumStep = 2
        self.messageStepSize = 40

        # Setup chatroom
        self.chatroom = ChatRoom("")#"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")

        # Connect signals
        self.messageField.textChanged.connect(self.resizeField)
        self.sendButton.clicked.connect(self.sendMessage)
        self.chatroom.received.connect(self.displayMessage)


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
        self.messageFrame.setMinimumHeight(self.messageStepSize * max(min(totalLines, self.messageMaximumStep), 1))

    @QtCore.Slot()
    def sendMessage(self):
        msg = self.messageField.toPlainText()

        if msg != '':
            self.chatroom.userMessage(msg)


    @QtCore.Slot(str, str)
    def displayMessage(self, content:str, role:str):
        print(f"{role}: {content}")


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    qapp = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(qapp.exec())
