#!/usr/bin/env python

"""
Sebastian Thiems 
Campuswoche 2014

Profile Manager. Dient zum Erstellen/Aendern/Loeschen/Speichern von Profilen.
"""

import ConfigParser
from CWBierzapfanlageConstants import CWConstants

class CWProfileManager:
	def __init__(self, CWConstants):
		self.CWConstants = CWConstants
		self.configParser = ConfigParser.ConfigParser()
		self.configParser.read(self.CWConstants.configFilename)

	def changeMiddleRightPointValue(self, value):
		print self.CWConstants.middle_right_point

	def changeMiddleLeftPointValue(self, value):
		self.CWConstants.middle_left_point = int(value)

	def changeDistanceTopToBottomLineValue(self, value):
		self.CWConstants.distance_top_to_bottom_line = int(value)

	def changeBorderGlasDistanceDivValue(self, value):
		self.CWConstants.border_glas_distance_div = int(value)

	def changeBorderGlasDistanceValue(self, value):
		self.CWConstants.border_glas_distance = int(value)

	def changeRightBorderIgnorValue(self, value):
		self.CWConstants.right_border_ignor = int(value)

	def changeLeftBorderIgnorValue(self, value):
		self.CWConstants.left_border_ignor = int(value)

	def changeSetting(self, section):
		self.CWConstants.changeMiddleRightPointValue(self.configParser.getint(str(section), self.CWConstants.middleRightPointString))
		self.CWConstants.changeMiddleLeftPointValue(self.configParser.getint(str(section), self.CWConstants.middleLeftPointString))
		self.CWConstants.changeDistanceTopToBottomLineValue(self.configParser.getint(str(section), self.CWConstants.distanceTopToBottomLineString))
		self.CWConstants.changeBorderGlasDistanceDivValue(self.configParser.getint(str(section), self.borderGlasDistanceDivString))
		self.CWConstants.changeBorderGlasDistanceValue(self.configParser.getint(str(section), self.CWConstants.borderGlasDistanceString))
		self.CWConstants.changeRightBorderIgnorValue(self.configParser.getint(str(section), self.CWConstants.rightBorderIgnorString))
		self.CWConstants.changeLeftBorderIgnorValue(self.configParser.getint(str(section), self.CWConstants.leftBorderIgnorString))

	#Speichern eines "section" (Profiles)
	def saveSection(self, section):
		if not self.configParser.has_section(str(section)):
			print ('New: ' + section)
			#Oeffnen der Profile-Datei
			cfgfile = open(self.CWConstants.configFilename,'w')
			#Hinzufuegen einer neuen "section" (Profile)
			self.configParser.add_section(str(section))
			self.updateSection(str(section))
			#Speichern des neuen Profiles in die Profile-Datei
			self.configParser.write(cfgfile)
			cfgfile.close()

	#Loeschen einer "section" (Profiles)
	def deleteSection(self, section):
		print ("Delete: " + section)
		cfgfile = open(self.CWConstants.configFilename,'w')
		self.configParser.remove_section(str(section))
		self.configParser.write(cfgfile)
		cfgfile.close()

	#Updaten einer bereits vorhandene "section" (Profiles)
	def updateSection(self, section):
		print ("Update: " + section)
		self.configParser.set(str(section), self.CWConstants.middleRightPointString, self.CWConstants.middle_right_point)
		self.configParser.set(str(section), self.CWConstants.middleLeftPointString, self.CWConstants.middle_left_point)
		self.configParser.set(str(section), self.CWConstants.distanceTopToBottomLineString, self.CWConstants.distance_top_to_bottom_line)
		self.configParser.set(str(section), self.CWConstants.borderGlasDistanceDivString, self.CWConstants.border_glas_distance_div)
		self.configParser.set(str(section), self.CWConstants.borderGlasDistanceString, self.CWConstants.border_glas_distance)
		self.configParser.set(str(section), self.CWConstants.rightBorderIgnorString, self.CWConstants.right_border_ignor)
		self.configParser.set(str(section), self.CWConstants.leftBorderIgnorString, self.CWConstants.left_border_ignor)



