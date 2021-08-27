import sys
from PyQt5.QtWidgets import (QTableWidget,QTableWidgetItem, QWidget, QApplication, QInputDialog, QLineEdit, QFileDialog, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog, QTextEdit, QAction, qApp, QDesktopWidget, QMainWindow, QWidget, QMessageBox, QToolTip, QPushButton)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5.QtCore import pyqtSlot
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import padasip as pa
import math
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Detekce(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.m = None
        self.q = None

        self.y = None
        self.w = None
        self.e = None
        self.d = None
        self.x = None
        self.initUI()

    def initUI(self):
        self.setGeometry(100,100,600,620)
        self.setWindowTitle("Detekce")
        self.tabulka()
        self.menu()
        self.menufil()
        self.show()

    def menufil(self):
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&Filters")

        SSLMS = QAction(QIcon("WWW.jpg"), "SSLMS", self)
        SSLMS.setShortcut("Ctrl+F")
        SSLMS.setStatusTip("Sign-sign Least-mean-squares (SSLMS)")
        SSLMS.triggered.connect(self.filterSSLMS)

        RLS = QAction(QIcon("WWW.jpg"), "RLS", self)
        RLS.setShortcut("Ctrl+R")
        RLS.setStatusTip("Recursive Least Squares (RLS)")
        RLS.triggered.connect(self.filterRLS)

        NSSLMS = QAction(QIcon("WWW.jpg"), "NSSLMS", self)
        NSSLMS.setShortcut("Ctrl+Q")
        NSSLMS.setStatusTip("Normalized Sign-sign Least-mean-squares (NSSLMS)")
        NSSLMS.triggered.connect(self.filterNSSLMS)

        AP = QAction(QIcon("WWW.jpg"), "AP", self)
        AP.setShortcut("Ctrl+A")
        AP.setStatusTip("Affine Projection (AP)")
        AP.triggered.connect(self.filterAP)

        GNGD = QAction(QIcon("WWW.jpg"), "GNGD", self)
        GNGD.setShortcut("Ctrl+G")
        GNGD.setStatusTip("Generalized Normalized Gradient Descent (GNGD)")
        GNGD.triggered.connect(self.filterGNGD)

        NLMS = QAction(QIcon("WWW.jpg"), "NLMS", self)
        NLMS.setShortcut("Ctrl+N")
        NLMS.setStatusTip("Normalized Least-mean-squares (NLMS)")
        NLMS.triggered.connect(self.filterNLMS)

        NLMF = QAction(QIcon("WWW.jpg"), "NLMF", self)
        NLMF.setShortcut("Ctrl+F")
        NLMF.setStatusTip("Normalized Least-mean-fourth (NLMF)")
        NLMF.triggered.connect(self.filterNLMF)

        LMS = QAction(QIcon("WWW.jpg"), "LMS", self)
        LMS.setShortcut("Ctrl+S")
        LMS.setStatusTip("Least-mean-fourth (LMS)")
        LMS.triggered.connect(self.filterLMS)

        LMF = QAction(QIcon("WWW.jpg"), "LMF", self)
        LMF.setShortcut("Ctrl+M")
        LMF.setStatusTip("Least-mean-fourth (LMF)")
        LMF.triggered.connect(self.filterLMF)

        fileMenu.addAction(SSLMS)
        fileMenu.addAction(RLS)
        fileMenu.addAction(AP)
        fileMenu.addAction(NSSLMS)
        fileMenu.addAction(GNGD)
        fileMenu.addAction(NLMS)
        fileMenu.addAction(NLMF)
        fileMenu.addAction(LMS)
        fileMenu.addAction(LMF)

    def menu(self):
        opfil = QAction(QIcon("WWW.jpg"), "open", self)
        opfil.setShortcut("Ctrl+O")
        opfil.setStatusTip("Open a file")
        opfil.triggered.connect(self.loading)

        gra = QAction(QIcon("WWW.jpg"), "graf", self)
        gra.setShortcut("Ctrl+g")
        gra.setStatusTip("Make a graph")
        gra.triggered.connect(self.grafy)

        gra = QPushButton("Graf", self)
        gra.clicked.connect(self.grafy)
        gra.resize(100, 20)
        gra.move(50, 560)

        #filt = QPushButton("Filtr", self)
        #filt.clicked.connect(self.filter())
        #filt.resize(100, 20)
        #filt.move(300, 560)

        selbt = QPushButton("Výběr",self)
        selbt.clicked.connect(self.vyber)
        selbt.resize(100, 20)
        selbt.move(200, 560)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&Tools")
        fileMenu.addAction(opfil)
        #fileMenu.addAction(gra)

    def loading(self):
        basefile = str(Path.home())
        jmeno = QFileDialog.getOpenFileName(self,"open file", basefile)
        hodnoty = open(jmeno[0],"r")
        mat1 =(np.genfromtxt(hodnoty, delimiter=",", skip_header=0))
        n = mat1.shape
        if len(n) == 1:
            m = (n[0], 1)
        else:
            m = n
        self.tableWidget.setRowCount(m[0])
        self.tableWidget.setColumnCount(m[1])
        for i in range(0,m[0]):
            for j in range(0,m[1]):
                try:
                    if len(n) == 1:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(mat1[i])))
                    else:
                        self.tableWidget.setItem(i,j,QTableWidgetItem(str(mat1[i, j])))
                except Exception as ex:
                    print(ex)
        self.m = m

    def vyber(self):
        alt = self.tableWidget.selectedItems()
        u = []
        n = self.m[0]
        for item in alt:
            u.append(float(item.text()))
        U = np.asarray(u)
        x = U.shape[0]
        f = x / n
        try:
            p = np.reshape(U,(int(f),n))
            q = p.T
            #print(q)
            #print(q.shape)
            #print(type(q))
            self.q = q
        except Exception as ex:
            print(ex)
        #self.filterNLMS()

    def uprava(self):
        s = self.q
        n = self.m[0]

        x = []
        d = []

        for i in range(5, n, 1):
            d = np.append(d, s[i])
        for i in range(0, n - 5, 1):
            x = np.append(x, s[i])
        l = np.asarray([x])
        f = np.asarray([d])
        self.x = l.T
        self.d = f.T

    def filterSSLMS(self):
        self.uprava()
        try:
            f = pa.filters.FilterSSLMS(n=1, mu=0.7, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e

    def filterRLS(self):
        self.uprava()
        try:
            f = pa.filters.FilterRLS(n=1, mu=0.7, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e


    def filterNSSLMS(self):
        self.uprava()
        try:
            f = pa.filters.FilterNSSLMS(n=1, mu=0.7, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e

    def filterAP(self):
        self.uprava()
        try:
            f = pa.filters.FilterAP(n=1, mu=0.7, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e

    def filterNLMS(self):
        self.uprava()
        try:
            f = pa.filters.FilterNLMS(n=1, mu=0.7, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e

    def filterGNGD(self):
        self.uprava()
        try:
            f = pa.filters.FilterGNGD(n=1, mu=0.7, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e


    def filterNLMF(self):
        self.uprava()
        try:
            f = pa.filters.FilterNLMF(n=1, mu=0.7, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e

    def filterLMS(self):
        self.uprava()
        try:
            f = pa.filters.FilterLMS(n=1, mu=0.7, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e

    def filterLMF(self):
        self.uprava()
        try:
            f = pa.filters.FilterLMF(n=1, mu=0.7, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e

    def tabulka(self):
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setGeometry(50, 50, 500, 500)

    def grafy(self):

        plt.plot(self.y)
        plt.plot(self.w)                #pyqtgraph
        plt.plot(self.e)
        plt.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            pass

def main():
    app = QApplication(sys.argv)
    ex = Detekce()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()


