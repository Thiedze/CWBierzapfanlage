#!/usr/bin/python

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from CWBierzapfanlageGUI import CWConfigWindow
from CWBierzapfanlageCLI import CWDetection
from CWBierzapfanlageConstants import CWConstants
from CWBierzapfanlageProfileManager import CWProfileManager

DEBUG = True

app = QtGui.QApplication(sys.argv)
if DEBUG == True:
	print "--- Application created ---"

#Init der Konstanten (Schnittstelle zwischen GUI und CLI)
CWConstants = CWConstants()
if DEBUG == True:
	print "--- CWConstants created ---"

#Init des Profile Managers (Erstellen/Aendern/Loeschen/Speichern von Profilen)
CWProfileManager = CWProfileManager(CWConstants)
if DEBUG == True:
	print "--- CWProfileManager created ---"

#Init des ConfigWindows (Einstellen/Aendern und Speichern von Configs)
CWConfigWindow = CWConfigWindow(CWConstants, CWProfileManager)
if DEBUG == True:
	print "--- CWConfigWindow created ---"

#Init der Kantenerkennung (+Init der Seriellen-Schnittstelle)
CWDetection = CWDetection(CWConstants, CWConfigWindow)
if DEBUG == True:
	print "--- CWDetection created ---"

if DEBUG == True:
	print "--- Run detection ---"
CWDetection.run()
if DEBUG == True:
	print "--- Close detection ---"

sys.exit(app.exec_())




