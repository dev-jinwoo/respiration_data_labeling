import sys
import os
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, Qt, QThread, QTimer

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.lbl1 = QLabel('파일:', self)
        self.lbl2 = QLabel('그래프:', self)
        self.lbl3 = QLabel('파일명:', self)
        self.le = QLineEdit(self)
        self.te = QTextEdit(self)
        self.se = QLineEdit(self)

        self.res_type1 = QRadioButton('정상호흡', self)
        self.res_type1.clicked.connect(self.radiobutton_clicked)

        self.res_type2 = QRadioButton('빈호흡', self)
        self.res_type2.clicked.connect(self.radiobutton_clicked)

        self.res_type3 = QRadioButton('수면', self)
        self.res_type3.clicked.connect(self.radiobutton_clicked)

        self.res_type4 = QRadioButton('움직임', self)
        self.res_type4.clicked.connect(self.radiobutton_clicked)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        self.pw = pg.PlotWidget(title="chart")
        self.pw.setBackground('w')
        self.pw.setYRange(-1, 1, padding=0)

        self.pl = self.pw.plot(pen='r')

        self.number = 0
        self.res_type = "none"

        self.file_open_btn = QPushButton('열기', self)
        self.next_data_btn = QPushButton('다음', self)
        self.play_data_btn = QPushButton('재생', self)
        self.previous_data_btn = QPushButton('이전', self)
        self.save_data_btn = QPushButton('저장', self)

        self.respiration_data = np.empty(4)

        self.initUI()

    def initUI(self):

        hbox = QHBoxLayout()
        hbox.addWidget(self.lbl1)
        hbox.addWidget(self.le)
        hbox.addWidget(self.file_open_btn)

        rbox = QVBoxLayout()
        rbox.addWidget(self.res_type1)
        rbox.addWidget(self.res_type2)
        rbox.addWidget(self.res_type3)
        rbox.addWidget(self.res_type4)


        sbox = QHBoxLayout()
        sbox.addWidget(self.lbl3)
        sbox.addWidget(self.se)
        sbox.addWidget(self.save_data_btn)
        sbox.addLayout(rbox)

        data_button = QHBoxLayout()
        data_button.addWidget(self.previous_data_btn)
        data_button.addWidget(self.play_data_btn)
        data_button.addWidget(self.next_data_btn)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.lbl2)
        vbox.addWidget(self.te)
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.pw)
        vbox.addLayout(data_button)
        vbox.addLayout(sbox)

        self.setLayout(vbox)

        self.file_open_btn.clicked.connect(self.btn_file_load)
        self.next_data_btn.clicked.connect(self.btn_next_data)
        self.play_data_btn.clicked.connect(self.btn_play_data)
        self.previous_data_btn.clicked.connect(self.btn_previous_data)
        self.save_data_btn.clicked.connect(self.btn_data_save)

        self.setWindowTitle('respiration label tool')
        self.setGeometry(300, 200, 900, 600)
        self.show()

    def btn_data_save(self):
        res_data = self.concat_data()
        data_path = os.path.join('./npy_data', self.res_type)
        os.makedirs(data_path, exist_ok=True)
        file_path = os.path.join(data_path, self.se.text())
        np.save(file_path, res_data)

    def concat_data(self):
        res_data = self.respiration_data[self.number]
        for i in range(self.number+660, len(self.respiration_data), 660):
            res_data = np.concatenate((res_data, self.respiration_data[i]), axis=0)
        return res_data

    def radiobutton_clicked(self):
        if self.res_type1.isChecked():
            self.res_type = 'eupnea'
        elif self.res_type2.isChecked():
            self.res_type = 'tachypnea'
        elif self.res_type3.isChecked():
            self.res_type = 'sleep'
        elif self.res_type4.isChecked():
            self.res_type = 'moving'

    def btn_file_load(self):
        fname = QFileDialog.getOpenFileName(self, '', '', 'respiration file(*.dat);; All File(*)')
        self.number = 0
        if fname[0]:
            self.le.setText(fname[0].split('/')[-1])
            self.respiration_data = np.loadtxt(fname[0])
            self.te.setText(str(self.respiration_data.shape))
            ax = self.fig.add_subplot(111)
            ax.set_ylim([-1, 1])
            ax.plot(self.respiration_data[0])
            self.canvas.draw()
            self.pl.setData(self.respiration_data[0])

    def btn_next_data(self):
        self.fig.clf()
        self.number += 1
        ax = self.fig.add_subplot(111)
        ax.set_ylim([-1, 1])
        ax.plot(self.respiration_data[self.number])
        self.canvas.draw()

    def btn_previous_data(self):
        self.fig.clf()
        self.number -= 1
        ax = self.fig.add_subplot(111)
        ax.set_ylim([-1, 1])
        ax.plot(self.respiration_data[self.number])
        self.canvas.draw()

    def btn_play_data(self):
        if self.play_data_btn.text() == '재생':
            self.play_data_btn.setText('멈춤')
            self.mytimer = QTimer()
            self.mytimer.start(10)  # 1000 = 1초
            self.mytimer.timeout.connect(self.get_data)
            self.draw_graph()
            self.show()

        elif self.play_data_btn.text() == '멈춤':
            self.fig.clf()
            self.mytimer.stop()
            res_data = self.concat_data()
            self.te.setText("데이터 길이: " + str(len(res_data)))
            print(len(res_data))
            ax = self.fig.add_subplot(111)
            ax.set_ylim([-1, 1])
            ax.plot(res_data)
            self.canvas.draw()
            self.play_data_btn.setText('재생')

    def draw_graph(self):
        self.pl.setData(self.respiration_data[self.number])


    @pyqtSlot()
    def get_data(self):
        self.number += 1
        self.draw_graph()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())