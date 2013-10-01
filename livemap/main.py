# -*- coding: utf-8 -*-
"""
Created on Sun May 19 16:37:49 2013

@author: florian
"""
import sys
import numpy as np
from PyQt4 import QtCore, QtGui, uic
import matplotlib as mpl
mpl.use('Qt4Agg')
import matplotlib.pyplot as plt
import pandas as pd
import datetime

from get_paris_data_api_style import VelibDataDownloader

try:
    from PyQt4.QtCore import QString
except ImportError:
    QtCore.QString = str

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        # load the UI
        self.ui = uic.loadUi("interface.ui", self)
        
        # customize the UI
        self.initUI()

        # init class data
        self.initData()
        
        # connect slots
        self.connectSlots()
        
    def initUI(self):
        self.ui.mplwidget.figure.set_facecolor('white')
        
    def initData(self):
        self.data_object = VelibDataDownloader()
        
    def connectSlots(self):
        self.ui.pushButton.clicked.connect(self.updateEverything)
        self.ui.checkBox.stateChanged.connect(self.checkboxUpdated)

    def checkboxUpdated(self, state):
        if state == 0:
            bikestands=True
        else:
            bikestands=False
        self.updatePlot(bikestands=bikestands)
    

    def updateInternalData(self):
        self.stations = self.data_object.get_data()
        
    def updateEverything(self):
        self.updateInternalData()
        self.updatePlot(bikestands= not bool(self.ui.checkBox.isChecked()))

    def updatePlot(self, bikestands=True):
        stations = self.stations
        positions = np.array([(d['position']['lng'], d['position']['lat']) for d in stations])
        indices = positions.min(axis=1) != 0.0
        positions = positions[indices,:]
        x, y = positions.T
        stations_df = pd.DataFrame(stations)
        timestamp = stations_df.last_update.max()
        date = datetime.datetime.fromtimestamp(timestamp / 1000.).strftime('%Y-%m-%d %H:%M:%S')
        sizes = stations_df.bike_stands[indices]
        # select data        
        if bikestands:        
            data = stations_df.available_bike_stands[indices]
        else:
            data = stations_df.available_bikes[indices]
        
        ax = self.ui.mplwidget.figure.add_subplot(111)        
        ax.cla()
        sc = ax.scatter(x, y, c=data, s=sizes, 
                    edgecolors='none', cmap=plt.get_cmap('RdYlGn'));
#        ax.set_xticks([]);
#        ax.set_yticks([]);
        if bikestands:
            ax.set_title("Available bike stands in Paris Velib' stations, {0:s}".format(date));
        else:
            ax.set_title("Available bikes in Paris Velib' stations, {0:s}".format(date));
            
        
        cax = self.ui.mplwidget.figure.add_axes([0.9, 0.1, 0.05, 0.8])    
        cax.cla()
        self.ui.mplwidget.figure.colorbar(sc, cax=cax)
#        self.ui.mplwidget.figure.tight_layout()
        self.ui.mplwidget.draw()
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())