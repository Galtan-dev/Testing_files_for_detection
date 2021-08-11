from PyQt5 import QtWidgets
import sys

aplikace = QtWidgets.QApplication(sys.argv)
formular = QtWidgets.QWidget()
boxlayout = QtWidgets.QHBoxLayout()
popisek = QtWidgets.QLabel("Ahoj Světe!", parent=formular)

formular.setWindowTitle("První aplikace")
formular.setGeometry(300, 300, 500, 500)

boxlayout.addStretch()
boxlayout.addWidget(popisek)
boxlayout.addStretch()

formular.setLayout(boxlayout)
formular.show()
sys.exit(aplikace.exec_())