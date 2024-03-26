echo "Compiling the UI file..."
pyside6-uic ../mainwindow.ui -o ../ui_mainwindow.py

echo "Compiling the onefile..."
pyinstaller --noconfirm --onefile --windowed --name ChatGPTChatRoom --icon ../logo.png --add-data ../logo.png:. ../MainWindow.py