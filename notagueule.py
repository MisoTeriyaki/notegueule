# -*-coding:Utf-8 -*

import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QTableView, QApplication, QSlider, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit, QDoubleSpinBox, QPushButton, QFileDialog)
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
        self.ax1 = self.fig.add_subplot(111)

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
        self.sliderMoy.setTickInterval(10)
        self.sliderMoy.setSingleStep(1)
        self.sliderMoy.setMaximum(10 * self.baremeMax)

        layout.addWidget(self.moyLabel)
        layout.addWidget(self.sliderMoy)
        #######
        ecartLabel = QLabel("Ecart-type")

        layoutH2 = QHBoxLayout()
        self.sliderEcart = QDoubleSpinBox()
        self.sliderEcart.setSingleStep(0.1)
        self.sliderEcart.setMaximum(10)

        self.boutonOuvrir = QPushButton("Ouvrir")
        self.boutonOuvrir.clicked.connect(self.ouvrir)
        self.boutonExport = QPushButton("Export")
        self.boutonExport.clicked.connect(self.export)
        
        layoutH2.addWidget(self.sliderEcart)
        layoutH2.addWidget(self.boutonOuvrir)
        layoutH2.addWidget(self.boutonExport)
        
        layout.addWidget(ecartLabel)
        layout.addLayout(layoutH2)

        #####################

        self.table = QTableView()
        # ouverture de listeNote.csv par défaut
        self.data = pandas.read_csv('listeNote.csv', delimiter=';', decimal=',')
        self.data.insert(len(self.data.columns), 'notagueule', self.data.iloc[:,-1])
        self.model = TableModel(self.data.iloc[:len(self.data)])
        self.table.setModel(self.model)

        layout.addWidget(self.table)

        self.setLayout(layout)

        self.sliderMoy.setValue(int(np.nanmean(self.data.iloc[:,-1]) * 10))
        self.sliderEcart.setValue(np.nanstd(self.data.iloc[:,-1]))
        self.maj()

        self.sliderMoy.valueChanged.connect(self.nouvMoy)
        self.sliderEcart.valueChanged.connect(self.nouvEcart)

    def remplissageTableau(self, nom):
        self.data = pandas.read_csv(nom, delimiter=';', decimal=',')
        self.data.insert(len(self.data.columns), 'notagueule', self.data.iloc[:,-1])
        self.model = TableModel(self.data.iloc[:len(self.data)])
        self.table.setModel(self.model)
        
    
    def nouvMax(self):
        if self.noteMax.text() != "":
            self.baremeMax = float(self.noteMax.text())
        self.maj()

    def ouvrir(self):
        nomFichier = QFileDialog.getOpenFileName(self, 'Ouvrir', "", "*.csv")
        self.remplissageTableau(nomFichier[0])
        self.maj()

    def export(self):
        self.data.to_csv("NTGexport.csv", sep=';', decimal=",", encoding='utf-8')
        
    def nouvMoy(self):
        self.data.iloc[:, -1] = round(self.data.iloc[:,-2] + self.sliderMoy.value() / 10 - np.nanmean(self.data.iloc[:,-2]), 2)
        self.maj()
      
        
    def nouvEcart(self):
        nouveauEcartType = self.sliderEcart.value()
        ancienEcartType = np.nanstd(self.data.iloc[:,-1])
        moy = np.nanmean(self.data.iloc[:,-1])
        self.data.iloc[:,-1] = round(self.data.iloc[:,-1] * nouveauEcartType / ancienEcartType - (nouveauEcartType / ancienEcartType - 1) * moy, 2)
        self.maj()

        
    def maj(self):
        for i in range(len(self.data.iloc[:,-1])):
            if self.data.iloc[i,-1] > self.baremeMax:
                self.data.iloc[i,-1] = self.baremeMax
            if self.data.iloc[i,-1] < 0 :
                self.data.iloc[i,-1] = 0
        self.model = TableModel(self.data.iloc[:len(self.data)])
        self.table.setModel(self.model)

        self.moyLabel.setText("Moyenne : " + str(round(np.nanmean(self.data.iloc[:,-1]), 2)))
        self.sliderEcart.setValue(np.nanstd(self.data.iloc[:,-1]))
        # gaussienne
        x = np.linspace(0, int(self.baremeMax), 500)
        y = stats.norm.pdf(x, np.nanmean(self.data.iloc[:,-1]), np.nanstd(self.data.iloc[:,-1]))
        self.ax1.cla()
        self.ax1.hist(self.data.iloc[:, -2], bins=range(0, int(self.baremeMax), 1), density=True, color='gray', alpha=0.2)
        self.ax1.plot(x, y, "r", label="notagueule")
        yEvaluation = stats.norm.pdf(x, np.nanmean(self.data.iloc[:,-2]), np.nanstd(self.data.iloc[:,-2]))
        self.ax1.plot(x, yEvaluation, "g", label="Initial")
        self.ax1.legend()
        self.sc.draw_idle()
#############################################

app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
