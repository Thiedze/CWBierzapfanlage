#!/usr/bin/env python

"""
Sebastian Thiems 
Campuswoche 2014

Profile Manager. Dient zum Erstellen/Aendern/Loeschen/Speichern von Profilen.
"""

import ConfigParser
import os
from CWConstants import CWConstants

DEBUG = False

class CWProfileManager:
	def __init__(self, parameterHandler):
		self.parameterHandler = parameterHandler
		self.configParser = ConfigParser.ConfigParser()
		self.configParser.read(CWConstants.CONFIGURATION_FILENAME)

	def changeMiddleRightPointValue(self, value):
		self.parameterHandler.middle_right_point = int(value)

	def changeMiddleLeftPointValue(self, value):
		self.parameterHandler.middle_left_point = int(value)

	def changeDistanceTopToBottomLineValue(self, value):
		self.parameterHandler.distance_top_to_bottom_line = int(value)

	def changeBorderGlasDistanceDivValue(self, value):
		self.parameterHandler.border_glas_distance_div = int(value)

	def changeBorderGlasDistanceValue(self, value):
		self.parameterHandler.border_glas_distance = int(value)

	def changeRightBorderIgnorValue(self, value):
		self.parameterHandler.right_border_ignor = int(value)

	def changeLeftBorderIgnorValue(self, value):
		self.parameterHandler.left_border_ignor = int(value)

	def openConfigFile(self):
		if os.path.exists(CWConstants.CONFIGURATION_FILENAME):
			return open(CWConstants.CONFIGURATION_FILENAME, "r+")
		else:
			return open(CWConstants.CONFIGURATION_FILENAME, "w")

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
			print ("Middle Right Point: " + str(self.parameterHandler.middle_right_point))
		self.configParser.set(str(section), CWConstants.MIDDLE_RIGHT_POINT_CAPTION, self.parameterHandler.middle_right_point)

		#Middle Left Point
		if DEBUG == True:
			print ("Middle Left Point: " + str(self.parameterHandler.middle_left_point))
		self.configParser.set(str(section), CWConstants.MIDDLE_LEFT_POINT_CAPTION, self.parameterHandler.middle_left_point)

		#Distance Top To Bottom
		if DEBUG == True:
			print ("Distance Top To Bottom: " + str(self.parameterHandler.distance_top_to_bottom_line))
		self.configParser.set(str(section), CWConstants.DISTANCE_TOP_TO_BOTTOM_LINE_CAPTION, self.parameterHandler.distance_top_to_bottom_line)

		#Border Glas Distance Div
		if DEBUG == True:
			print ("Border Glas Distance Div: " + str(self.parameterHandler.border_glas_distance_div))
		self.configParser.set(str(section), CWConstants.BORDER_GLASS_DISTANCE_DIFFERENCE_CAPTION, self.parameterHandler.border_glas_distance_div)

		#Border Glas Distance
		if DEBUG == True:
			print ("Border Glas Distance: " + str(self.parameterHandler.border_glas_distance))
		self.configParser.set(str(section), CWConstants.BORDER_GLASS_DISTANCE_CAPTION, self.parameterHandler.border_glas_distance)

		#Right Border Ignor
		if DEBUG == True:
			print ("Right Border Ignor: " + str(self.parameterHandler.right_border_ignor))
		self.configParser.set(str(section), CWConstants.RIGHT_BORDER_IGNORE_CAPTION, self.parameterHandler.right_border_ignor)

		#Left Border Ignor
		if DEBUG == True:
			print ("Left Border Ignor: " + str(self.parameterHandler.left_border_ignor))
		self.configParser.set(str(section), CWConstants.LEFT_BORDER_IGNORE_CAPTION, self.parameterHandler.left_border_ignor)
		
		#Speichern des neuen Profiles in die Profile-Datei
		self.configParser.write(cfgfile)
		cfgfile.close()

