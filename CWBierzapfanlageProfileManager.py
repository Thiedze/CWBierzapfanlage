#!/usr/bin/env python

"""
Sebastian Thiems 
Campuswoche 2014

Profile Manager. Dient zum Erstellen/Aendern/Loeschen/Speichern von Profilen.
"""

import ConfigParser
import os
from CWBierzapfanlageConstants import CWConstants

DEBUG = True

class CWProfileManager:
	def __init__(self, CWConstants):
		self.CWConstants = CWConstants
		self.configParser = ConfigParser.ConfigParser()
		self.configParser.read(self.CWConstants.configFilename)

	def changeMiddleRightPointValue(self, value):
		self.CWConstants.middle_right_point = int(value)

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

	def openConfigFile(self):
		if os.path.exists(self.CWConstants.configFilename):
			return open(self.CWConstants.configFilename, "r+")
		else:
			return open(self.CWConstants.configFilename, "w")

	#Speichern eines "section" (Profiles)
	def saveSection(self, section):
		if not self.configParser.has_section(str(section)):
			if DEBUG == True:
				print ('Profile Manager New: ' + section)
			#Oeffnen der Profile-Datei
			cfgfile = self.openConfigFile()
			#Hinzufuegen einer neuen "section" (Profile)
			self.configParser.add_section(str(section))
			self.updateSection(str(section))
			#Speichern des neuen Profiles in die Profile-Datei
			self.configParser.write(cfgfile)
			cfgfile.close()

	#Loeschen einer "section" (Profiles)
	def deleteSection(self, section):
		if DEBUG == True:
			print ("Profile Manager Delete: " + section)
		cfgfile = self.openConfigFile()
		self.configParser.remove_section(str(section))
		self.configParser.write(cfgfile)
		cfgfile.close()

	#Updaten einer bereits vorhandene "section" (Profiles)
	def updateSection(self, section):
		#Oeffnen der Profile-Datei
		cfgfile = self.openConfigFile()
		if DEBUG == True:
			print ("Profile Manager Update: " + section)

		#Middle Right Point
		if DEBUG == True:
			print ("Middle Right Point: " + str(self.CWConstants.middle_right_point))
		self.configParser.set(str(section), self.CWConstants.middleRightPointString, self.CWConstants.middle_right_point)

		#Middle Left Point
		if DEBUG == True:
			print ("Middle Left Point: " + str(self.CWConstants.middle_left_point))
		self.configParser.set(str(section), self.CWConstants.middleLeftPointString, self.CWConstants.middle_left_point)

		#Distance Top To Bottom
		if DEBUG == True:
			print ("Distance Top To Bottom: " + str(self.CWConstants.distance_top_to_bottom_line))
		self.configParser.set(str(section), self.CWConstants.distanceTopToBottomLineString, self.CWConstants.distance_top_to_bottom_line)

		#Border Glas Distance Div
		if DEBUG == True:
			print ("Border Glas Distance Div: " + str(self.CWConstants.border_glas_distance_div))
		self.configParser.set(str(section), self.CWConstants.borderGlasDistanceDivString, self.CWConstants.border_glas_distance_div)

		#Border Glas Distance
		if DEBUG == True:
			print ("Border Glas Distance: " + str(self.CWConstants.border_glas_distance))
		self.configParser.set(str(section), self.CWConstants.borderGlasDistanceString, self.CWConstants.border_glas_distance)

		#Right Border Ignor
		if DEBUG == True:
			print ("Right Border Ignor: " + str(self.CWConstants.right_border_ignor))
		self.configParser.set(str(section), self.CWConstants.rightBorderIgnorString, self.CWConstants.right_border_ignor)

		#Left Border Ignor
		if DEBUG == True:
			print ("Left Border Ignor: " + str(self.CWConstants.left_border_ignor))
		self.configParser.set(str(section), self.CWConstants.leftBorderIgnorString, self.CWConstants.left_border_ignor)
		
		#Speichern des neuen Profiles in die Profile-Datei
		self.configParser.write(cfgfile)
		cfgfile.close()

