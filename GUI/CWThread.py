'''
Created on Jun 23, 2016

@author: thiedze
'''
from __main__ import sys

from PyQt4 import QtCore, QtGui

from GUI.CWBierzapfanlageGUIManager import CWBierzapfanlageGUIManager

class GUIThread(QtCore.QThread):

    def __init__(self, parameterHandler, profileManager):
        QtCore.QThread.__init__(self)
        self.app = QtGui.QApplication(sys.argv)
        self.mainWindow = CWBierzapfanlageGUIManager(parameterHandler, profileManager)
        
    def run(self):
        self.mainWindow.show()
        self.app.exec_loop()
        
        