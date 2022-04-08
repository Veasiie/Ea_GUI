
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

import sys
import numpy as np



from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):

        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi("design.ui",self)

        # register all widgets
        self.P1 = self.findChild(QtWidgets.QLineEdit, 'P1LineEdit')
        self.P2 = self.findChild(QtWidgets.QLineEdit, 'P2LineEdit')

        self.L1 = self.findChild(QtWidgets.QLineEdit, 'L1LineEdit')
        self.L2 = self.findChild(QtWidgets.QLineEdit, 'L2LineEdit')

        self.Glue = self.findChild(QtWidgets.QLineEdit, 'glueLineEdit')
        self.Scuare = self.findChild(QtWidgets.QLineEdit, 'SquareLineEdit')

        self.Modulus = self.findChild(QtWidgets.QLCDNumber, 'ModulusLcdNumber')
        self.pushButtonModulus = self.findChild(QtWidgets.QPushButton, 'pushButtonModulus')
        self.pushButtonModulus.clicked.connect(self.calculate_modulus)

        self.OpenPushButton = self.findChild(QtWidgets.QPushButton, 'OpenPushButton')
        self.OpenPushButton.clicked.connect(self.browse_file)
        self.combo_box = self.findChild(QtWidgets.QComboBox, 'comboBox')
        self.combo_box.addItems([])
        self.combo_box.currentTextChanged.connect(self.on_combobox_changed)



        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        self.MplWidget.canvas.mpl_connect(s="button_press_event", func=self.get_coord)

        self.show()

    def browse_file(self):
        self.filenames = QFileDialog.getOpenFileNames(self, 'Open File', filter='TXT files (*txt)') 
        self.combo_list = self.filenames[0]
        self.combo_box.addItems(self.combo_list)
    def get_coord(self, event):
        if event.button == 1:
            print(event.xdata, event.ydata)
            self.P1.setText(str(event.ydata))
            self.L1.setText(str(event.xdata))
        elif event.button ==3:
            print(event.ydata, event.xdata)
            self.P2.setText(str(event.ydata))
            self.L2.setText(str(event.xdata))

    def on_combobox_changed(self, value):
        self.data = np.genfromtxt(self.combo_box.currentText(), encoding='utf-16', skip_header=48).T
        self.Temperature = self.data[1]
        self.Heat_flow = self.data[2]
        self.plotting()
        print("combobox changed", value)
         # do your code

    def plotting(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.Temperature,self.Heat_flow)
        self.MplWidget.canvas.axes.set_title('Сдвиг')
        self.MplWidget.canvas.axes.set_xlabel('Перемещение, мм')
        self.MplWidget.canvas.axes.set_ylabel('Нагрузка, кгс')
        self.MplWidget.canvas.draw()

    def calculate_modulus(self):
        P1 = float(self.P1.text())
        P2 = float(self.P2.text())
        L1 = float(self.L1.text())
        L2 = float(self.L2.text())
        H = float(self.Glue.text())
        S = float(self.Scuare.text())
        G = (P2-P1)*H/(S*(L2-L1))
        self.Modulus.display(G)
        print(G)


 




app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
