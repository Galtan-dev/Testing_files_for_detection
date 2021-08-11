import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QMessageBox, QToolTip, QPushButton)
from PyQt5.QtGui import (QIcon, QFont)

class Tab(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont("SansSerif", 10))
        self.setToolTip("This is a <b>QWidget</b> widget")

        btn = QPushButton("Quit", self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.clicked.connect(QApplication.instance().quit)

        btn.resize(btn.sizeHint())
        btn.move(50,50)

        self.setGeometry(400, 400, 500, 500)
        self.setWindowTitle("Icon")
        self.setWindowIcon(QIcon("WWW.jpg"))
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Message", "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
def main():

    aplikace = QApplication(sys.argv)
    ex = Tab()
    sys.exit(aplikace.exec_())

if __name__=="__main__":
    main()