#!/usr/bin/pyhton

"""
Sebastian Thiems 2014 

GUI fuer die Automatische-Bierzapfanlage
"""

from PyQt4 import QtGui
from PyQt4 import QtCore
from CWBierzapfanlageConstants import CWConstants
from CWBierzapfanlageProfileManager import CWProfileManager

DEBUG = True

class Button(QtGui.QWidget):
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

class CWConfigWindow(QtGui.QWidget):
	def __init__(self,CWConstants, CWProfileManager,parent=None,w=400,h=600):
		self.CWConstants = CWConstants
		self.CWProfileManager = CWProfileManager
		self.w=w
		self.h=h
		QtGui.QWidget.__init__(self, parent)
		self.resize(self.w,self.h)
		self.setWindowTitle('Automatische Bierzapfanlage')
		self.createAndAddGUIElements()
		self.show()

	def createAndAddGUIElements(self):
		#Saved Settings ComboBox
		self.combo = ComboBox(parent=self, callback=self.changeSetting,CWProfileManager=self.CWProfileManager, x=10,y=(self.h-580),w=(self.w-150))
		
		#TextField for saving
		self.textField = TextField(parent=self,  x=(self.w/2+60),y=(self.h-580),w=130)
		
		#Close Button
		Button(parent=self,callback=QtCore.SLOT('quit()'), text="Close",x=10,y=(self.h-40))

		Button(parent=self, callback=self.stopScanning, text="Stop", x=80, y=(self.h-40))

		#Detect Button
		Button(parent=self,callback=self.detectingSetting,text="Detect",x=(self.w-210),y=(self.h-40))

		#Save Button
		Button(parent=self,callback=self.saveSetting,text="Save",x=(self.w-140),y=(self.h-40))

		#Delete Button
		Button(parent=self,callback=self.deleteSetting,text="Delete",x=(self.w-70),y=(self.h-40))

		#Middle Right Point Slider
		self.middleRightPointSlider = Slider(parent=self, callback=self.CWProfileManager.changeMiddleRightPointValue, text=self.CWConstants.middleRightPointString, x=10, y=(self.h-100), w=(self.w-20))

		#Middle Left Point Slider		
		self.middleLeftPointSlider = Slider(parent=self, callback=self.CWProfileManager.changeMiddleLeftPointValue, text=self.CWConstants.middleLeftPointString, x=10, y=(self.h-170), w=(self.w-20))

		#Distance Top To Bottom Line Slider
		self.distanceTopToBottomLineSlider = Slider(parent=self, callback=self.CWProfileManager.changeDistanceTopToBottomLineValue, text=self.CWConstants.distanceTopToBottomLineString,x=10,y=(self.h-240), w=(self.w-20))

		#Border Glas Distance Div Slider
		self.borderGlasDistanceDivSlider = Slider(parent=self, callback=self.CWProfileManager.changeBorderGlasDistanceDivValue,  text=self.CWConstants.borderGlasDistanceDivString, x=10, y=(self.h-310), w=(self.w-20))

		#Border Glas Distance Slider
		self.borderGlasDistanceSlider = Slider(parent=self, callback=self.CWProfileManager.changeBorderGlasDistanceValue, text=self.CWConstants.borderGlasDistanceString, x=10, y=(self.h-380), w=(self.w-20))

		#Right Border Ignoer Slider
		self.rightBorderIgnorSlider = Slider(parent=self, callback=self.CWProfileManager.changeRightBorderIgnorValue, text=self.CWConstants.rightBorderIgnorString, x=10, y=(self.h-450), w=(self.w-20))

		#Left Border Ignor Slider
		self.leftBorderIgnorSlider = Slider(parent=self, callback=self.CWProfileManager.changeLeftBorderIgnorValue, text=self.CWConstants.leftBorderIgnorString, x=10, y=(self.h-520), w=(self.w-20))

	#Slider auf den neuen Wert setzen
	#Alle neuen Slider muessen hier hinzugefuegt werden
	def changeSetting(self):
		if(self.combo.combo.currentText().size() > 0):
			if DEBUG == True:
				print ("GUI Change Setting")
			section = str(self.combo.combo.currentText())
			self.middleRightPointSlider.slider.setValue(int(self.CWProfileManager.configParser.get(section, str(self.CWConstants.middleRightPointString), True)))
			self.middleLeftPointSlider.slider.setValue(int(self.CWProfileManager.configParser.get(section, str(self.CWConstants.middleLeftPointString),True)))
			self.distanceTopToBottomLineSlider.slider.setValue(int(self.CWProfileManager.configParser.get(section, str(self.CWConstants.distanceTopToBottomLineString),True)))
			self.borderGlasDistanceDivSlider.slider.setValue(int(self.CWProfileManager.configParser.get(section, str(self.CWConstants.borderGlasDistanceDivString),True)))
			self.borderGlasDistanceSlider.slider.setValue(int(self.CWProfileManager.configParser.get(section, str(self.CWConstants.borderGlasDistanceString),True)))
			self.rightBorderIgnorSlider.slider.setValue(int(self.CWProfileManager.configParser.get(section, str(self.CWConstants.rightBorderIgnorString),True)))
			self.leftBorderIgnorSlider.slider.setValue(int(self.CWProfileManager.configParser.get(section, str(self.CWConstants.leftBorderIgnorString),True)))
				
	#Loeschen eines Setting (Profiles)
	def deleteSetting(self):
		if(self.combo.combo.currentText().size() > 0):
			self.CWProfileManager.deleteSection(self.combo.combo.currentText())
			self.combo.catchConfigs()
			self.combo.combo.setCurrentIndex(int(self.combo.combo.count()-1))

	#Speichern eines Setting (Profiles)
	def saveSetting(self):
		if self.textField.textField.text().size() == 0:
			if DEBUG == True:
				print ("GUI Update Section: " + self.combo.combo.currentText())
			self.CWProfileManager.updateSection(self.combo.combo.currentText())
		else:
			section = self.textField.textField.text()
			if DEBUG == True:
				print ("GUI Save New Section: " + section)
			self.CWProfileManager.saveSection(section)
			self.combo.catchConfigs()
			self.combo.combo.setCurrentIndex(int(self.combo.combo.count()-1))
			self.changeSetting()

	def stopScanning(self):
		self.CWConstants.stopProgram = True

	def detectingSetting(self):
		print ("GUI Detecting Setting")

