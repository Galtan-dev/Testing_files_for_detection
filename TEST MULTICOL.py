import sys
from PyQt5.QtWidgets import (QTableWidget,QTableWidgetItem, QWidget, QApplication, QInputDialog, QLineEdit, QFileDialog, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog, QTextEdit, QAction, qApp, QDesktopWidget, QMainWindow, QWidget, QMessageBox, QToolTip, QPushButton)
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
#from PyQt5.QtGui import (QIcon, QFont)
#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import padasip as pa
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
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
        self.f = None
        self.det = None
        self.rl = None
        self.initUI()

    def initUI(self):
        self.setGeometry(100,100,700,635)
        self.setWindowTitle("Detekce")
        #self.vnitrograf()
        self.tabulka()
        self.menugraf()
        self.menufil()
        self.menuDET()
        #self.statusbar()
        self.combobox()
        self.lspeed()
        self.show()

    #def vnitrograf(self):

        #self.graphWidget = pg.PlotWidget(self)
        #self.graphWidget.setXRange(100,500)
        #self.graphWidget.setYRange(100,500)
       # self.se
        #self.graphWidget = pg.PlotWidget()
        #self.graphWidget.setGeometry(600, 50, 500, 500)
        #plt = pg.plot()

    def combobox(self):
        self.comboI = QComboBox(self)
        self.comboI.addItem("Choose filter")
        self.comboI.addItem("SSLMS")
        self.comboI.addItem("RLS")
        self.comboI.addItem("NSSLMS")
        self.comboI.addItem("AP")
        self.comboI.addItem("GNGD")
        self.comboI.addItem("NLMF")
        self.comboI.addItem("NLMS")
        self.comboI.addItem("LMS")
        self.comboI.addItem("LMF")
        self.comboI.setGeometry(550,80,100,25)

        self.comboII = QComboBox(self)
        self.comboII.addItem("Choose detection")
        self.comboII.addItem("LE")
        self.comboII.addItem("ELBND")
        self.comboII.setGeometry(550, 130, 100, 25)

        self.spoust = QPushButton("Execute",self)
        self.spoust.setGeometry(550,525,100,25)
        self.spoust.clicked.connect(self.uzel)

    def uzel(self):
        self.lspeedchoose()
        self.vyber()
        self.vyberfiltr()
        self.vyberdet()
        self.grafy()

    def vyberfiltr(self):
        filt = self.comboI.currentText()
        if (filt == "SSLMS"):
            self.filterSSLMS()
        if (filt == "RLS"):
            self.filterRLS()
        elif (filt == "NSSLMS"):
            self.filterNSSLMS()
        elif (filt == "AP"):
            self.filterAP()
        elif (filt == "GNGD"):
            self.filterGNGD()
        elif (filt == "NLMF"):
            self.filterNLMF()
        elif (filt == "NLMS"):
            self.filterNLMS()
        elif (filt == "LMS"):
            self.filterLMS()
        elif (filt == "LMF"):
            self.filterLMF()

    def vyberdet(self):
        det = self.comboII.currentText()
        if (det == "LE"):
            self.detLE()
        elif (det == "ELBND"):
            self.detELBND()

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

    def menuDET(self):
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&Detection")

        ELBND = QAction(QIcon("WWW.jpg"), "ELBND", self)
        ELBND.setShortcut("Ctrl+1")
        ELBND.setStatusTip("Error and Learning Based Novelty Detection (ELBND)")
        ELBND.triggered.connect(self.detELBND)

        LE = QAction(QIcon("WWW.jpg"), "LE", self)
        LE.setShortcut("Ctrl+2")
        LE.setStatusTip("Learning Entropy (LE)")
        LE.triggered.connect(self.detLE)

        fileMenu.addAction(ELBND)
        fileMenu.addAction(LE)

    def menugraf(self):
        opfil = QAction(QIcon("WWW.jpg"), "open", self)
        opfil.setShortcut("Ctrl+9")
        opfil.setStatusTip("Open a file")
        opfil.triggered.connect(self.loading)

        ofiltl = QPushButton("Open a file",self)
        ofiltl.setGeometry(550,200,100,25)
        ofiltl.clicked.connect(self.loading)

        grafil = QAction(QIcon("WWW.jpg"), "Graph filter", self)
        grafil.setShortcut("Ctrl+8")
        grafil.setStatusTip("Open a graph")
        grafil.triggered.connect(self.grafyfilt)

        gradet = QAction(QIcon("WWW.jpg"), "Graph detection", self)
        gradet.setShortcut("Ctrl+7")
        gradet.setStatusTip("Open a graph")
        gradet.triggered.connect(self.grafdet)

        vyb = QAction(QIcon("WWW.jpg"), "Selection", self)
        vyb.setShortcut("Ctrl+6")
        vyb.setStatusTip("Selected a column")
        vyb.triggered.connect(self.vyber)

        #self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&Tools")
        fileMenu.addAction(opfil)
        fileMenu.addAction(grafil)
        fileMenu.addAction(gradet)
        fileMenu.addAction(vyb)

    #def statusbar(self):
        #self.label_1 = QLabel("Status Bar", self)
        #self.label_1.move(580, 50)
        #self.label_1.setStyleSheet("border :5px solid blue;")
        #self.label_1.resize(100, 150)
        #self.show()

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
        self.statusBar().showMessage("Files are loaded")

    def vyber(self):
        alt = self.tableWidget.selectedItems()
        u = []
        n = self.m[0]
        print(n)


        for item in alt:
            u.append(float(item.text()))
        U = np.asarray(u)
        x = U.shape[0]
        f = x / n
        self.f = f
        print(self.f)
        try:
            p = np.reshape(U,(int(f),n))    #zařizuje přetvoření matice tak aby sloupec matice odpovídal sloupci vybranému z tabulky
            q = p.T
            print(q)
            print(np.shape(q))
            self.q = q
        except Exception as ex:
            print(ex)
        self.statusBar().showMessage("Input column are selected")
    def uprava(self):
        s = self.q
        n = self.m[0]

        x = []
        d = []

        #for i in range()
            #for j in range()
                    




        for j in range(0,(int(self.f)),1):
            for i in range(5, n, 1):
                d = np.append(d, s[i,j])      #je potřeba upravit ak aby se nebrali hodnoty ze všech sloupců ale udělali se nové matice pos loupcích
            for i in range(0, n - 5, 1):
                x = np.append(x, s[i,j])
        L = np.asarray([x])
        F = np.asarray([d])
        l = np.reshape(L,(int(self.f),n-5))
        f = np.reshape(F,(int(self.f),n-5))
        self.x = l.T
        self.d = f.T
        print(self.x)
        print(np.shape(x))
        print(self.d)
        print(np.shape(d))

    def lspeed(self):
        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(550,250,50,25)
        self.show()

    def lspeedchoose(self):
        try:
            speedvalue = int(self.textbox.text())
            self.rl = speedvalue
        except:
            self.rl = 1


    def filterSSLMS(self):
        self.uprava()
        try:
            f = pa.filters.FilterSSLMS(n=1, mu=self.rl, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e
        self.statusBar().showMessage("SSLMS filter aplicated")

    def filterRLS(self):
        self.uprava()
        try:
            f = pa.filters.FilterRLS(n=1, mu=self.rl, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e
        self.statusBar().showMessage("RLS filter aplicated")

    def filterNSSLMS(self):
        self.uprava()
        try:
            f = pa.filters.FilterNSSLMS(n=1, mu=self.rl, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e
        self.statusBar().showMessage("NSSLMS filter aplicated")

    def filterAP(self):
        self.uprava()
        try:
            f = pa.filters.FilterAP(n=1, mu=self.rl, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e
        self.statusBar().showMessage("AP filter aplicated")

    def filterNLMS(self):
        self.uprava()
        try:
            f = pa.filters.FilterNLMS(n=1, mu=self.rl, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e
        self.statusBar().showMessage("NLMS filter aplicated")

    def filterGNGD(self):
        self.uprava()
        print("kulový 1")
        try:
            f = pa.filters.FilterGNGD(n=int(self.f), mu=self.rl, w="zeros")
            print("kulový2")
            y, e, w = f.run(self.d, self.x)
            print("kulový3")
        except Exception as ex:
            print("kulový4")
            print(ex)
        print(y)
        print("kulový")
        self.y = y
        self.w = w
        self.e = e
        self.statusBar().showMessage("GNGD filter aplicated")

    def filterNLMF(self):
        self.uprava()
        try:
            f = pa.filters.FilterNLMF(n=1, mu=self.rl, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e
        self.statusBar().showMessage("NLMF filter aplicated")

    def filterLMS(self):
        self.uprava()
        try:
            f = pa.filters.FilterLMS(n=1, mu=self.rl, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e
        self.statusBar().showMessage("LMS filter aplicated")

    def filterLMF(self):
        self.uprava()
        try:
            f = pa.filters.FilterLMF(n=1, mu=self.rl, w="zeros")
            y, e, w = f.run(self.d, self.x)
        except Exception as ex:
            print(ex)
        self.y = y
        self.w = w
        self.e = e
        self.statusBar().showMessage("LMF filter aplicated")

    def detELBND(self):

        elbnd = pa.detection.ELBND(self.w, self.e, function="max")
        self.det = elbnd
        self.statusBar().showMessage("ELBND detection aplicated")

    def detLE(self):

        le = pa.detection.learning_entropy(self.w, m=30, order=1)
        self.det = le
        self.statusBar().showMessage("LE detection aplicated")

    def tabulka(self):
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setGeometry(25, 50, 500, 500)

    def grafdet(self):

        plt.plot(self.det)
        plt.show()

    def grafyfilt(self):

        fig, axs = plt.subplots(3, 1)
        axs[0].plot(self.e)
        axs[1].plot(self.y)
        axs[2].plot(self.w)
        axs[0].grid(True)
        axs[1].grid(True)
        axs[2].grid(True)

        fig.tight_layout()
        plt.show()

    def grafy(self):

        fig, axs = plt.subplots(4, 1)
        axs[0].plot(self.e)
        axs[1].plot(self.y)
        axs[2].plot(self.w)
        axs[3].plot(self.det)

        #axs[0].subtitle("Filter error for every sample")
        #axs[1].subtitle("Output value")
        #axs[2].subtitle("History of all weights")
        #axs[3].subtitle("Detection values")

        axs[0].grid(True)
        axs[1].grid(True)
        axs[2].grid(True)
        axs[3].grid(True)

        fig.tight_layout()
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


