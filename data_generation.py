import sys
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
import time
from random import uniform
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, Qt, QThread, QTimer

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.lbl1 = QLabel('파일:', self)
        self.lbl2 = QLabel('그래프:', self)
        self.le = QLineEdit(self)
        self.te = QTextEdit(self)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        self.generation_btn = QPushButton('생성', self)
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.lbl1)
        hbox.addWidget(self.le)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl2)
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.te)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.generation_btn.clicked.connect(self.generation_data)

        self.setWindowTitle('respiration label tool')
        self.setGeometry(300, 200, 900, 600)
        self.show()

    def generation_data(self):
        data_list = []
        for i in range(660):
            a = uniform(-1, 1)
            data_list.append((round(a, 8)))
        result = ' '.join(str(s) for s in data_list)

        self.te.setText(result)
        ax = self.fig.add_subplot(111)
        ax.set_ylim([-1, 1])
        ax.plot(data_list)
        self.canvas.draw()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())