# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui
from chatroom import ChatRoom
from ui_mainwindow import Ui_MainWindow
from math import floor

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    APITokenUpdated = QtCore.Signal(str)
    UserMessageSent = QtCore.Signal(str)

    def __init__(self, parent:QtCore.QObject|None = None):
        super().__init__(parent)
        self.setupUi(self)

        # Setup some constants
        self.messageAutoGrowPadding = 30
        self.messageMaximumStep = 2
        self.messageStepSize = 40

        # Setup chatroom
        self.chatroom = ChatRoom("")

        # Connect signals
        self.messageField.textChanged.connect(self.resizeField)
        self.messageField.SendMessage.connect(self.sendMessage)
        self.sendButton.clicked.connect(self.sendMessage)
        self.chatroom.received.connect(self.displayMessage)
        self.actionReset.triggered.connect(self.chatroom.resetSession)
        self.actionReset.triggered.connect(self.clearMessageHistory)
        self.actionSetAPIToken.triggered.connect(self.setAPIToken)
        self.actionSaveChatHistory.triggered.connect(self.saveChatHistory)
        self.APITokenUpdated.connect(self.chatroom.updateApiToken)
        self.APITokenUpdated.connect(self.clearMessageHistory)
        self.UserMessageSent.connect(self.chatroom.userMessage)

        # Setup worker thread
        self.worker_thread = QtCore.QThread()
        self.worker_thread.start()
        self.chatroom.moveToThread(self.worker_thread)

        self.setAPIToken()

    def closeEvent(self, event:QtGui.QCloseEvent):
        if self.worker_thread:
            self.worker_thread.exit()

    @QtCore.Slot()
    def setAPIToken(self):
        val, state = QtWidgets.QInputDialog.getText(self, "Set API Token", "API Token")
        if not state: # user clicked cancel
            return

        if val == '':
            return

        self.APITokenUpdated.emit(val)

    @QtCore.Slot()
    def saveChatHistory(self):
        if self.messageList.count() > 0:
            messages = []
            for i in range(self.messageList.count()):
                messages.append(self.messageList.item(i).text())

            filename, filetype = QtWidgets.QFileDialog.getSaveFileName(self, "Save Chat History", "", "Text Files (*.txt)")
            if filename == '' and filetype == '':
                return

            # If user actually selected a file:
            with open(filename, 'w') as f:
                f.write('\n'.join(messages))

    @QtCore.Slot()
    def clearMessageHistory(self):
        self.messageList.clear()

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
            self.displayMessage(msg, "user")
            self.UserMessageSent.emit(msg)
            self.messageField.setPlainText("")


    @QtCore.Slot(str, str)
    def displayMessage(self, content:str, role:str):
        item = QtWidgets.QListWidgetItem(f"{role}: {content}")
        self.messageList.addItem(item)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    qapp = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(qapp.exec())
