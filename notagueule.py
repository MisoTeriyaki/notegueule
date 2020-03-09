import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QTableView, QApplication, QSlider, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.figure
import pandas
import numpy as np
import scipy.stats as stats


#####################################
################################
class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]
    
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


#####################################

class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        ###################

        self.fig = matplotlib.figure.Figure()
        self.sc = FigureCanvas(self.fig)


        layout.addWidget(self.sc)
        ###################
        layoutH = QHBoxLayout()
        self.noteMaxLabel = QLabel("Note maximale : ")
        self.baremeMax = 20
        self.noteMax = QLineEdit(str(self.baremeMax))
        layoutH.addWidget(self.noteMaxLabel)
        layoutH.addWidget(self.noteMax)
        layout.addLayout(layoutH)

        self.noteMax.textChanged.connect(self.nouvMax)
        ###################

        self.moyLabel = QLabel("Moyenne")
        self.sliderMoy = QSlider(Qt.Horizontal)
        self.sliderMoy.setFocusPolicy(Qt.StrongFocus)
        self.sliderMoy.setTickPosition(QSlider.TicksBothSides)
        self.sliderMoy.setTickInterval(1)
        self.sliderMoy.setSingleStep(0.5)
        self.sliderMoy.setMaximum(20)

        layout.addWidget(self.moyLabel)
        layout.addWidget(self.sliderMoy)
        #######
        ecartLabel = QLabel("Ecart-type")
        self.sliderEcart = QSlider(Qt.Horizontal)
        self.sliderEcart.setFocusPolicy(Qt.StrongFocus)
        self.sliderEcart.setTickPosition(QSlider.TicksBothSides)
        self.sliderEcart.setTickInterval(1)
        self.sliderEcart.setSingleStep(0.1)
        self.sliderEcart.setMaximum(10)

        layout.addWidget(ecartLabel)
        layout.addWidget(self.sliderEcart)
        #####################

        self.table = QTableView()
        self.data = pandas.read_csv('listeNote.csv', delimiter=';', decimal=',')
        self.data.insert(2, 'notagueule', self.data['Evaluation'])
        self.model = TableModel(self.data.iloc[:len(self.data)])
        self.table.setModel(self.model)
        layout.addWidget(self.table)

        self.ax1 = self.fig.add_subplot(211)
        self.ax1.hist(self.data['Evaluation'], bins=range(0, 20, 1))

        
        self.setLayout(layout)

        self.sliderMoy.setValue(np.mean(self.data.iloc[:,1]))
        self.sliderEcart.setValue(np.std(self.data.iloc[:,1]))
        self.maj()

        self.sliderMoy.valueChanged.connect(self.nouvMoy)
        self.sliderEcart.valueChanged.connect(self.nouvEcart)

    def nouvMax(self):
        if self.noteMax.text() != "":
            self.baremeMax = float(self.noteMax.text())
        self.maj()
        
    def nouvMoy(self):
        self.data['notagueule'] = self.data['Evaluation'] + self.sliderMoy.value() - np.mean(self.data.iloc[:,1])
        self.maj()
      
        
    def nouvEcart(self):
        nouveauEcartType = self.sliderEcart.value()
        self.data['notagueule'] = (np.power(self.data['Evaluation'], 2)*nouveauEcartType**2/np.std(self.data.iloc[:,1])**2 - (nouveauEcartType**2/np.std(self.data.iloc[:,1])**2 -1 )*np.mean(self.data.iloc[:,1])**2)**0.5
        self.maj()

        
    def maj(self):
        for i in range(len(self.data.iloc[:,2])):
            if self.data.iloc[i,2] > self.baremeMax :
                self.data.iloc[i,2] = self.baremeMax
            if self.data.iloc[i,2] < 0 :
                self.data.iloc[i,2] = 0
        self.model = TableModel(self.data.iloc[:len(self.data)])
        self.table.setModel(self.model)

        self.moyLabel.setText("Moyenne : " + str( np.mean(self.data.iloc[:,2])))
        # gaussienne
        x = np.linspace(0, 20, 500)
        y = stats.norm.pdf(x, np.mean(self.data.iloc[:,2]), np.std(self.data.iloc[:,2]))
        self.ax2 = self.fig.add_subplot(212)
        self.ax2.cla()
        self.ax2.plot(x, y, "r", label="notagueule")
        yEvaluation = stats.norm.pdf(x, np.mean(self.data.iloc[:,1]), np.std(self.data.iloc[:,1]))
        self.ax2.plot(x, yEvaluation, "g", label="Initial")
        self.ax2.legend()
        self.sc.draw_idle()
#############################################

app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
