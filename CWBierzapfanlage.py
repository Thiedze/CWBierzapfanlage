#!/usr/bin/pyhton

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from CWBierzapfanlageGUI import CWConfigWindow
from CWBierzapfanlageCLI import CWDetection
from CWBierzapfanlageConstants import CWConstants
from CWBierzapfanlageProfileManager import CWProfileManager

app = QtGui.QApplication(sys.argv)

#Init der Konstanten (Schnittstelle zwischen GUI und CLI)
CWConstants = CWConstants()

#Init des Profile Managers (Erstellen/Aendern/Loeschen/Speichern von Profilen)
CWProfileManager = CWProfileManager(CWConstants)

#Init des ConfigWindows (Einstellen/Aendern und Speichern von Configs)
CWConfigWindow(CWConstants, CWProfileManager)

#Init der Kantenerkennung (+Init der Seriellen-Schnittstelle)
CWDetection = CWDetection(CWConstants)
CWDetection.run()

sys.exit(app.exec_())




