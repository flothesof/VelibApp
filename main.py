# -*- coding: utf-8 -*-
"""
Created on Sun May 19 16:37:49 2013

@author: florian
"""
import sys

from PyQt4 import QtCore, QtGui, uic

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
        
        # maximize window
#        self.setWindowState(QtCore.Qt.WindowMaximized)
       

    def initUI(self):
        # display tab
        pass

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
            
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())