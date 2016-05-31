#!/usr/bin/pyhton

"""
Sebastian Thiems 2014 

GUI fuer die Automatische-Bierzapfanlage
"""

import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

from CWBierzapfanlageGUI import Ui_CWBierzapfanlageGUI
from CWBierzapfanlageConstants import CWConstants
from CWBierzapfanlageProfileManager import CWProfileManager


DEBUG = True

'''class Button(QtGui.QWidget):
	def __init__(self,parent=None,callback=None,text="New Button",x=0,y=0,w=60,h=30):
		QtGui.QWidget.__init__(self, parent)
		self.button = QtGui.QPushButton(text, parent)
		self.button.setGeometry(x, y, w, h)
		
		if text == "Close":
			self.button.connect(self.button, QtCore.SIGNAL('clicked()'), QtGui.qApp, callback)
		else:
			self.button.connect(self.button, QtCore.SIGNAL('clicked()'), callback)

class Slider(QtGui.QWidget):
	def __init__(self,parent=None,callback=None,text="New Label",x=0,y=0,w=100,h=30):
		QtGui.QWidget.__init__(self, parent)
		self.CWConstants = parent.CWConstants
		self.section = parent.combo.combo.currentText()

		self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, parent)
		self.slider.setFocusPolicy(QtCore.Qt.NoFocus)
		self.slider.setGeometry(x,y,w,h)
		self.slider.setMinimum(0)
		self.slider.setMaximum(self.CWConstants.w)
		self.slider.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'), callback)
		if(self.section.size() > 0):
			self.slider.setValue(parent.CWProfileManager.configParser.getint(str(self.section), str(text)))
		
		Label(parent=parent,title=text,x=x,y=(y-30),w=w)

class ComboBox(QtGui.QWidget):
	def __init__(self,parent=None,callback=None,CWProfileManager=None,x=0,y=0,w=100,h=30):
		QtGui.QWidget.__init__(self, parent)
		self.CWProfileManager = CWProfileManager
		self.combo = QtGui.QComboBox(parent)
		self.combo.activated[str].connect(callback)
		self.combo.setGeometry(x,y,w,h)
		self.catchConfigs()
		
	def catchConfigs(self):
		self.combo.clear()
		for section in self.CWProfileManager.configParser.sections():
			self.combo.addItem(section)

class TextField(QtGui.QWidget):
	def __init__(self, parent=None,x=0,y=0,w=100,h=30):
		QtGui.QWidget.__init__(self, parent)
		self.textField = QtGui.QLineEdit(parent)
		self.textField.setGeometry(x,y,w,h)

class Label(QtGui.QWidget):
	def __init__(self,parent=None,title="New Label",x=0,y=0,w=60,h=30):
		self.parent = parent
		QtGui.QWidget.__init__(self, parent)
		self.label = QtGui.QLabel(title,parent)
		self.label.setGeometry(x,y,w,h)

class StatusField(QtGui.QWidget):
	def __init__(self,parent=None, x=0,y=0,w=100,h=30):
		self.parent = parent
		QtGui.QWidget.__init__(self, parent)
		self.status = QtGui.QWidget(parent)
		
		#self.color = QtGui.QColor(255, 0, 0)
		self.status.setGeometry(x,y,w,h)
		self.status.setStyleSheet("QWidget { background-color: %s }" % QtGui.QColor(255, 0, 0).name() )'''


class CWBierzapfanlageGUIManager(QtGui.QMainWindow):
	def __init__(self,CWConstants, CWProfileManager):
		QtGui.QWidget.__init__(self, None)
		
		self.CWConstants = CWConstants
		self.CWProfileManager = CWProfileManager
		self.CWBierzapfanlageGUI = Ui_CWBierzapfanlageGUI()
		self.CWBierzapfanlageGUI.setupUi(self)
	
		self.ConnectSlots()		
		self.show()
		
	def catchConfigs(self, comboBox):
		comboBox.clear()
		for section in self.CWProfileManager.configParser.sections():
			comboBox.addItem(section)
		
	def ConnectSettingSlots(self):
		#Close Button
		self.CWBierzapfanlageGUI.btnExit.clicked.connect(self.quit)
		
		#Left area left border
		self.CWBierzapfanlageGUI.hsLeftLeftBorder.sliderMoved.connect(self.CWProfileManager.changeLeftBorderIgnorValue)
		self.CWBierzapfanlageGUI.hsLeftLeftBorder.setMaximum(self.CWConstants.w)
		
		#Left area right border		
		self.CWBierzapfanlageGUI.hsLeftRightBorder.sliderMoved.connect(self.CWProfileManager.changeLeftBorderIgnorValue)
		self.CWBierzapfanlageGUI.hsLeftRightBorder.setMaximum(self.CWConstants.w)
		
		#Right area left border		
		self.CWBierzapfanlageGUI.hsRightLeftBorder.sliderMoved.connect(self.CWProfileManager.changeLeftBorderIgnorValue)
		self.CWBierzapfanlageGUI.hsRightLeftBorder.setMaximum(self.CWConstants.w)
		
		#Right area right border		
		self.CWBierzapfanlageGUI.hsRightRightBorder.sliderMoved.connect(self.CWProfileManager.changeLeftBorderIgnorValue)
		self.CWBierzapfanlageGUI.hsRightRightBorder.setMaximum(self.CWConstants.w)
		
		#Distance between foam and top horizontal glass edge
		self.CWBierzapfanlageGUI.hsDistance.sliderMoved.connect(self.CWProfileManager.changeDistanceTopToBottomLineValue)
		self.CWBierzapfanlageGUI.hsDistance.setMaximum(self.CWConstants.w)
		
	def ConnectConfigurationSlots(self):
		#Configuration combobox		
		self.CWBierzapfanlageGUI.cbConfiguration.currentIndexChanged.connect(self.changeConfiguration)
		self.catchConfigs(self.CWBierzapfanlageGUI.cbConfiguration)
		
		#Save configuration
		self.CWBierzapfanlageGUI.btnSaveConfiguration.clicked.connect(self.saveConfiguration)
		
		#Delete configuration
		self.CWBierzapfanlageGUI.btnDeleteConfiguration.clicked.connect(self.deleteConfiguration)
				
	def ConnectSlots(self):
		self.ConnectSettingSlots()
		self.ConnectConfigurationSlots()
		
	def createAndAddGUIElements(self):

		'''#self.statusField = StatusField(parent=self, x=80, y=(self.h-40))

		#Debug Start Rotate
		#Button(parent=self, callback=self.startRotate, text="Start Rotate", x=10, y=(self.h-620), w=80)

		#Debug Stop Rotate
		#Button(parent=self, callback=self.stopRotate, text="Stop Rotate", x=100, y=(self.h-620), w=80)

		#Debug Start Fill
		#Button(parent=self, callback=self.startFill, text="Start Fill", x=190, y=(self.h-620), w=80)

		#Debug Stop Fill
		#Button(parent=self, callback=self.stopFill, text="Stop Fill", x=280, y=(self.h-620), w=80)

		#Glass detected label
		self.glassDetectedLabel = Label(parent=self, title="Glass detected",x=10,y=(self.h-90), w=100)

		#Fill glass label
		self.fillGlassLabel = Label(parent=self, title="Fill glass",x=140,y=(self.h-90), w=100)

		#Rotate platform label
		self.rotatePlatformLabel = Label(parent=self, title="Rotate platform",x=230,y=(self.h-90), w=150)
			
		#Detect Button
		Button(parent=self,callback=self.detectingSetting,text="Detect",x=(self.w-210),y=(self.h-40))

		#Border Glas Distance Div Slider
		self.borderGlasDistanceDivSlider = Slider(parent=self, callback=self.CWProfileManager.changeBorderGlasDistanceDivValue,  text=self.CWConstants.borderGlasDistanceDivString, x=10, y=(self.h-340), w=(self.w-20))

		#Border Glas Distance Slider
		self.borderGlasDistanceSlider = Slider(parent=self, callback=self.CWProfileManager.changeBorderGlasDistanceValue, text=self.CWConstants.borderGlasDistanceString, x=10, y=(self.h-410), w=(self.w-20))

		'''

	#Slider auf den neuen Wert setzen
	#Alle neuen Slider muessen hier hinzugefuegt werden
	def changeConfiguration(self):
		if(self.CWBierzapfanlageGUI.cbConfiguration.currentText().size() > 0):
			if DEBUG == True:
				print ("GUI Change Setting: " + self.CWBierzapfanlageGUI.cbConfiguration.currentText())
			section = str(self.CWBierzapfanlageGUI.cbConfiguration.currentText())
			
			if DEBUG == True:
				print("leftBorderIgnor from config parser", int(self.CWProfileManager.configParser.get(section, str(self.CWConstants.leftBorderIgnorString),True)))
			
			self.CWBierzapfanlageGUI.hsLeftLeftBorder.setValue(int(self.CWProfileManager.configParser.get(section, str(self.CWConstants.leftBorderIgnorString),True)))
			self.CWBierzapfanlageGUI.hsLeftRightBorder.setValue(int(self.CWProfileManager.configParser.get(section, str(self.CWConstants.middleLeftPointString),True)))
			self.CWBierzapfanlageGUI.hsRightLeftBorder.setValue(int(self.CWProfileManager.configParser.get(section, str(self.CWConstants.middleRightPointString), True)))
			self.CWBierzapfanlageGUI.hsRightRightBorder.setValue(int(self.CWProfileManager.configParser.get(section, str(self.CWConstants.rightBorderIgnorString),True)))
			self.CWBierzapfanlageGUI.hsDistance.setValue(int(self.CWProfileManager.configParser.get(section, str(self.CWConstants.distanceTopToBottomLineString),True)))
				
	#Loeschen eines Profiles
	def deleteConfiguration(self):
		if(self.CWBierzapfanlageGUI.cbConfiguration.currentText().size() > 0):
			self.CWProfileManager.deleteSection(self.CWBierzapfanlageGUI.cbConfiguration.currentText())
			self.catchConfigs(self.CWBierzapfanlageGUI.cbConfiguration)
			self.CWBierzapfanlageGUI.cbConfiguration.setCurrentIndex(int(self.CWBierzapfanlageGUI.cbConfiguration.count()-1))

	#Speichern eines Profiles
	def saveConfiguration(self):
		if self.CWBierzapfanlageGUI.edtConfigurationName.text().size() == 0:
			if DEBUG == True:
				print ("GUI Update Section: " + self.CWBierzapfanlageGUI.cbConfiguration.currentText())
			self.CWProfileManager.updateSection(self.CWBierzapfanlageGUI.cbConfiguration.currentText())
		else:
			section = self.CWBierzapfanlageGUI.edtConfigurationName.text()
			if DEBUG == True:
				print ("GUI Save New Section: " + section)
			self.CWProfileManager.saveSection(section)
			self.catchConfigs(self.CWBierzapfanlageGUI.cbConfiguration)
			self.CWBierzapfanlageGUI.cbConfiguration.setCurrentIndex(int(self.CWBierzapfanlageGUI.cbConfiguration.count()-1))
			self.changeConfiguration()

	def stopScanning(self):
		self.CWConstants.stopProgram = True

	def quit(self):
		sys.exit(0)

	def detectingSetting(self):
		print ("GUI Detecting Setting")

	def glasDetected(self, detected = False):
		if detected == True:
			self.glassDetectedLabel.label.setStyleSheet('color: %s' % QtGui.QColor(0, 255, 0).name())
		else:
			self.glassDetectedLabel.label.setStyleSheet('color: %s' % QtGui.QColor(255, 0, 0).name())

	def fillGlass(self, fill = False):
		if fill == True:
			self.fillGlassLabel.label.setStyleSheet('color: %s' % QtGui.QColor(0, 255, 0).name())
		else:
			self.fillGlassLabel.label.setStyleSheet('color: %s' % QtGui.QColor(255, 0, 0).name())

	def rotatePlatform(self, rotate = False):
		if rotate == True:
			self.rotatePlatformLabel.label.setStyleSheet('color: %s' % QtGui.QColor(0, 255, 0).name())
		else:
			self.rotatePlatformLabel.label.setStyleSheet('color: %s' % QtGui.QColor(255, 0, 0).name())

	#def startRotate(self):
	#	self.CWDetection.CWSerial.StartRotation(0.0)

	#def stopRotate(self):
	#	self.CWDetection.CWSerial.StopRotation()

	#def stopFill(self):
	#	self.CWDetection.CWSerial.StopFill()
		
	#def startFill(self):
	#	self.CWDetection.CWSerial.StartFill()

