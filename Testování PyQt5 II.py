import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QInputDialog, QLineEdit, QFileDialog, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog, QTextEdit, QAction, qApp, QDesktopWidget, QMainWindow, QWidget, QMessageBox, QToolTip, QPushButton)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5.QtCore import QRect
from pathlib import Path


class Example(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.initUI()

    def initUI(self):
        self.resize(500, 500)
        QToolTip.setFont(QFont("SansSerif", 10))

        qbtn = QPushButton("quit", self)
        qbtn.setToolTip('This is a <b>QPushButton</b> widget')
        qbtn.clicked.connect(self.closeEvent)
        qbtn.resize(100, 20)
        qbtn.move(50, 50)

        btn = QPushButton("Info", self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.clicked.connect(self.my_func)
        btn.resize(100, 20)
        btn.move(200,50)
        self.textEdit = QTextEdit(self.central_widget)
        self.textEdit.setGeometry(QRect(10, 10, 300, 300))

        self.bar()
        self.poloha()
        self.menu()


        self.center()
        self.setWindowTitle('Moje aplikace')
        self.setWindowIcon(QIcon("WWW.jpg"))
        self.show()

    def showDialog(self):
        home_dir = str(Path.home())
        frame = QFileDialog.getOpenFileName(self,"open file", home_dir)
        if frame[0]:
            f = open(frame[0], "r")
            with f:
                data = f.read()
                self.textEdit.setText(data)

    def poloha(self):
        sl1 = QLabel("Vypnutí",self)
        sl1.move(80,30)

        sl2 = QLabel("Info", self)
        sl2.move(240, 30)

    def menu(self):
        exm = QAction(QIcon("WWW.jpg"),"&Exit",self)
        exm.setShortcut("Ctrl+Q")
        exm.setStatusTip("Exit Application")
        exm.triggered.connect(self.closeEvent)
        exm.triggered.connect(qApp.quit)




        opfil = QAction(QIcon("WWW.jpg"),"open",self)
        opfil.setShortcut("Ctrl+O")
        opfil.setStatusTip("Open a file")
        opfil.triggered.connect(self.showDialog)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(exm)
        fileMenu.addAction(opfil)

    def bar(self):
        br = self.statusBar().showMessage("Vytvořeno na VŠCHT")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def my_func(self):
        print("Aplikace")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            pass

def main():
    aplikace = QApplication(sys.argv)
    try:
        ex = Example()
    except Exception as ex:
        print(ex)
    sys.exit(aplikace.exec_())

if __name__=="__main__":
    main()
