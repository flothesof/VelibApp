# -*- coding: utf-8 -*-
"""
Created on Sun May 19 16:37:49 2013

@author: florian
"""
import sys
import sqlite3

from PyQt4 import QtCore, QtGui, uic
import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from get_station import get_station_data

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
         # generate the plot
        self.fig = Figure(figsize=(300,300), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        self.ax = self.fig.add_subplot(111)
        # generate the canvas to display the plot
        self.canvas = FigureCanvas(self.fig)
        self.ui.centralwidget.layout().addWidget(self.canvas)
        
    def initData(self):
        self.timer = QtCore.QBasicTimer()
        self.database = {}
        
    def connectSlots(self):
        QtCore.QObject.connect(self.ui.pushButton,
                               QtCore.SIGNAL('clicked()'),
                                self.startAcquisition) 
        
        QtCore.QObject.connect(self.ui.pushButton_2,
                               QtCore.SIGNAL('clicked()'),
                                self.stopAcquisition) 
        
    def startAcquisition(self):
        self.timer.start(int(self.ui.spinBox.value()) * 1000, self)
        self.ui.checkBox.setChecked(True)
        
    def stopAcquisition(self):
        self.timer.stop()
        self.ui.checkBox.setChecked(False)
        
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.updateStations()

    def updateStations(self):
        self.ui.textBrowser.setText("")        
        station = 14019       
        self.getStationData(station)
        self.ui.textBrowser.setText(QtCore.QString(self.getStatusText(station)))
        self.updatePlot(station)        
        
    def getStationData(self, station):
        data = get_station_data(station)
        if station not in self.database:
            self.database[station] = [data]
        else:
            if self.database[station][-1][0] != data[0]:
                self.database[station].append(data)

    def getStatusText(self, station):
        if station in self.database:
            return "Station %s: last update %s, bikes: %s, free: %s, total: %s." % ((station,) + self.database[station][-1])            
        else:
            return ""
            
    def updatePlot(self, station):
        if station in self.database:
            items = self.database[station]

            t = [item[0] for item in items]
            
            bikes = [item[1] for item in items]           
            free = [item[2] for item in items]
            total = [item[3] for item in items]            

            self.ax.plot(t, bikes, 'ro-')
            self.ax.plot(t, free, 'bo-')
            self.ax.plot(t, total, 'go-')
            
            self.ax.set_ylim(ymin=0)
            self.canvas.draw()
    
    def writeToDatabase(self):
        station = 14019
        conn = sqlite3.connect("database.sqlite")
        cursor = conn.cursor()
        data = self.database[station]
        for row in data:
            cursor.execute('INSERT INTO velib VALUES (?,?,?,?,?)',
                           (station,) + row)
        conn.commit()
        conn.close()
    
    def closeEvent(self, e):
        self.writeToDatabase()
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())