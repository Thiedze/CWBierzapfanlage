#!/usr/bin/pyhton

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from CWBierzapfanlageGUI import CWConfigWindow
from CWBierzapfanlageCLI import CWDetection
from CWBierzapfanlageConstants import CWConstants

app = QtGui.QApplication(sys.argv)

#Init der Konstanten (Schnittstelle zwischen GUI und CLI)
cwConstants = CWConstants()

#Init des ConfigWindows (Einstellen/Aendern und Speichern von Configs)
CWConfigWindow(cwConstants)

#Init der Kantenerkennung (+Init der Seriellen-Schnittstelle)
#cwDetection = CWDetection(cwConstants)
#cwDetection.run()

sys.exit(app.exec_())




