#!/usr/bin/python

import sys
import thread

from PyQt4 import QtGui

from GUI.CWBierzapfanlageGUIManager import CWBierzapfanlageGUIManager
from Profile.CWProfileManager import CWProfileManager
from StateMachine.CWTabMachine import CWTabMachine

DEBUG = False

if DEBUG == False:
	app = QtGui.QApplication(sys.argv)

tabMachine = CWTabMachine();

# Init des Profile Managers (Erstellen/Aendern/Loeschen/Speichern von Profilen)
profileManager = CWProfileManager(tabMachine.parameterHandler)

if DEBUG == False:
	bierzapfanlageGUIManager = CWBierzapfanlageGUIManager(tabMachine.parameterHandler, profileManager)
	tabMachine.setGui(bierzapfanlageGUIManager)

# Kantenerkennung
tabMachine.start()

if DEBUG == False:
	sys.exit(app.exec_())







