#!/usr/bin/pyhton

"""
Sebastian Thiems 2014 

GUI fuer die Automatische-Bierzapfanlage
"""

import sys

from PyQt4 import QtGui, QtCore
import numpy as np
import cv2

from CWConstants import CWConstants
from GUI.CWBierzapfanlageGUI import Ui_CWBierzapfanlageGUI
from GUI.CWBierzapfanlageCLIDrawer import CWCLIDrawer

DEBUG = False

class CWBierzapfanlageGUIManager(QtGui.QMainWindow):
	def __init__(self, parameterHandler, profileManager):
		QtGui.QWidget.__init__(self, None)
		
		self.parameterHandler = parameterHandler
		self.cliDrawer = CWCLIDrawer(self.parameterHandler)
		self.profileManager = profileManager
		self.bierzapfanlageGUI = Ui_CWBierzapfanlageGUI()
		self.bierzapfanlageGUI.setupUi(self)
	
		self.ConnectSlots()
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.updateCam)
		self.left = None
		self.right = None
		self.top = None
		self.bottom_foam = None
		self.frame = None
		self.debugFrame = None
		self.timer.start(16)
		self.show()		
		
	def catchConfigs(self, comboBox):
		comboBox.clear()
		for section in self.profileManager.configParser.sections():
			comboBox.addItem(section)
		
	def ConnectSettingSlots(self):
		#Close Button
		self.bierzapfanlageGUI.btnExit.clicked.connect(self.stopScanning)
		
		#Left area left border
		self.bierzapfanlageGUI.hsLeftLeftBorder.sliderMoved.connect(self.profileManager.changeLeftBorderIgnorValue)
		self.bierzapfanlageGUI.hsLeftLeftBorder.setMaximum(CWConstants.FRAME_WIDTH)
		
		#Left area right border		
		self.bierzapfanlageGUI.hsLeftRightBorder.sliderMoved.connect(self.profileManager.changeLeftBorderIgnorValue)
		self.bierzapfanlageGUI.hsLeftRightBorder.setMaximum(CWConstants.FRAME_WIDTH)
		
		#Right area left border		
		self.bierzapfanlageGUI.hsRightLeftBorder.sliderMoved.connect(self.profileManager.changeLeftBorderIgnorValue)
		self.bierzapfanlageGUI.hsRightLeftBorder.setMaximum(CWConstants.FRAME_WIDTH)
		
		#Right area right border		
		self.bierzapfanlageGUI.hsRightRightBorder.sliderMoved.connect(self.profileManager.changeLeftBorderIgnorValue)
		self.bierzapfanlageGUI.hsRightRightBorder.setMaximum(CWConstants.FRAME_WIDTH)
		
		#Distance between foam and top horizontal glass edge
		self.bierzapfanlageGUI.hsDistance.sliderMoved.connect(self.profileManager.changeDistanceTopToBottomLineValue)
		self.bierzapfanlageGUI.hsDistance.setMaximum(CWConstants.FRAME_WIDTH)
		
	def ConnectConfigurationSlots(self):
		#Configuration combobox		
		self.bierzapfanlageGUI.cbConfiguration.currentIndexChanged.connect(self.changeConfiguration)
		self.catchConfigs(self.bierzapfanlageGUI.cbConfiguration)
		
		#Save configuration
		self.bierzapfanlageGUI.btnSaveConfiguration.clicked.connect(self.saveConfiguration)
		
		#Delete configuration
		self.bierzapfanlageGUI.btnDeleteConfiguration.clicked.connect(self.deleteConfiguration)

		#Demo Modus
		self.bierzapfanlageGUI.cbDemoModus.stateChanged.connect(self.changeDemoModus)
		
		#Resume
		self.bierzapfanlageGUI.btnResume.clicked.connect(self.resume)
				
	def ConnectSlots(self):
		self.ConnectSettingSlots()
		self.ConnectConfigurationSlots()

	def resume(self):
		self.parameterHandler.resume = True

	def changeDemoModus(self):
		self.parameterHandler.demoModus = not self.parameterHandler.demoModus

	#Slider auf den neuen Wert setzen
	#Alle neuen Slider muessen hier hinzugefuegt werden
	def changeConfiguration(self):
		if(self.bierzapfanlageGUI.cbConfiguration.currentText().size() > 0):
			if DEBUG == True:
				print ("GUI Change Setting: " + self.bierzapfanlageGUI.cbConfiguration.currentText())
			section = str(self.bierzapfanlageGUI.cbConfiguration.currentText())
			
			if DEBUG == True:
				print("leftBorderIgnor from config parser", int(self.profileManager.configParser.get(section, str(CWConstants.LEFT_BORDER_IGNORE_CAPTION),True)))
			
			self.bierzapfanlageGUI.hsLeftLeftBorder.setValue(int(self.profileManager.configParser.get(section, str(CWConstants.LEFT_BORDER_IGNORE_CAPTION),True)))
			self.bierzapfanlageGUI.hsLeftRightBorder.setValue(int(self.profileManager.configParser.get(section, str(CWConstants.MIDDLE_LEFT_POINT_CAPTION),True)))
			self.bierzapfanlageGUI.hsRightLeftBorder.setValue(int(self.profileManager.configParser.get(section, str(CWConstants.MIDDLE_RIGHT_POINT_CAPTION), True)))
			self.bierzapfanlageGUI.hsRightRightBorder.setValue(int(self.profileManager.configParser.get(section, str(CWConstants.RIGHT_BORDER_IGNORE_CAPTION),True)))
			self.bierzapfanlageGUI.hsDistance.setValue(int(self.profileManager.configParser.get(section, str(CWConstants.DISTANCE_TOP_TO_BOTTOM_LINE_CAPTION),True)))
				
	#Loeschen eines Profiles
	def deleteConfiguration(self):
		if(self.bierzapfanlageGUI.cbConfiguration.currentText().size() > 0):
			self.profileManager.deleteSection(self.bierzapfanlageGUI.cbConfiguration.currentText())
			self.catchConfigs(self.bierzapfanlageGUI.cbConfiguration)
			self.bierzapfanlageGUI.cbConfiguration.setCurrentIndex(int(self.bierzapfanlageGUI.cbConfiguration.count()-1))

	#Speichern eines Profiles
	def saveConfiguration(self):
		if self.bierzapfanlageGUI.edtConfigurationName.text().size() == 0:
			if DEBUG == True:
				print ("GUI Update Section: " + self.bierzapfanlageGUI.cbConfiguration.currentText())
			self.profileManager.updateSection(self.bierzapfanlageGUI.cbConfiguration.currentText())
		else:
			section = self.bierzapfanlageGUI.edtConfigurationName.text()
			if DEBUG == True:
				print ("GUI Save New Section: " + section)
			self.profileManager.saveSection(section)
			self.catchConfigs(self.bierzapfanlageGUI.cbConfiguration)
			self.bierzapfanlageGUI.cbConfiguration.setCurrentIndex(int(self.bierzapfanlageGUI.cbConfiguration.count()-1))
			self.changeConfiguration()

	def stopScanning(self):
		self.parameterHandler.stopProgram = True
		QtCore.QCoreApplication.instance().quit()

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

	def updateCam(self):
		if self.frame != None:
			self.cliDrawer.draw(self.frame, self.left, self.right, self.top, self.bottom_foam)

		if self.debugFrame != None:
			cv2.imshow("Debug", self.debugFrame)

	def setFrame(self, frame, left, right, top, bottom_foam):
		self.frame = frame
		if left != None:		
			self.left = left
		if right != None:		
			self.right = right
		if top != None:		
			self.top = top
		if bottom_foam != None:
			self.bottom_foam = bottom_foam
	
	def setDebugFrame(self, frame):
		self.debugFrame = frame

