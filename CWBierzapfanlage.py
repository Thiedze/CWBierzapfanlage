#!/usr/bin/python

import sys
import thread

from PyQt4 import QtGui

from GUI.CWBierzapfanlageGUIManager import CWBierzapfanlageGUIManager
from Profile.CWProfileManager import CWProfileManager
from StateMachine.CWTabMachine import CWTabMachine

app = QtGui.QApplication(sys.argv)

tabMachine = CWTabMachine();

# Init des Profile Managers (Erstellen/Aendern/Loeschen/Speichern von Profilen)
profileManager = CWProfileManager(tabMachine.parameterHandler)

bierzapfanlageGUIManager = CWBierzapfanlageGUIManager(tabMachine.parameterHandler, profileManager)

# Kantenerkennung
tabMachine.start()

sys.exit(app.exec_())







