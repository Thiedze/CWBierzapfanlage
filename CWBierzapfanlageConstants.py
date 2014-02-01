#!/usr/bin/env python

"""
Sebastian Thiems 
Campuswoche 2014

Konstanten der Bierzapfanlage.
"""

import ConfigParser
import os.path

class CWConstants:
	def __init__(self):		
		#Groesse des Bildes
		self.w = 640
		self.h = 480
		self.total_number_of_pixel = self.h * self.w
		self.configFilename = "CWBierzapfanlage.cfg"
		#self.cfgfile = open(self.configFilename, 'w')
		self.configParser = ConfigParser.ConfigParser()
		self.configParser.read(self.configFilename)
		
		self.middleRightPointString = 'Middle Right Point'
		self.middleLeftPointString = 'Middle Left Point'
		self.distanceTopToBottomLineString = 'Distance Top To Bottom Line'
		self.borderGlasDistanceDivString = 'Border Glas Distance Div'
		self.borderGlasDistanceString = 'Border Glas Distance'
		self.rightBorderIgnorString = 'Right Border Ignor'
		self.leftBorderIgnorString = 'Left Border Ignor'

		self.initBorderConstants()

	def initBorderConstants(self):
		#Von der Mitte des Bildes -> Linke und Rechte Kante (in %) bis die gefundenen Linien ignoriert werden
		left_border_ignor_percent = 10
		self.left_border_ignor = (float(left_border_ignor_percent) / 100) * self.w
		self.left_border_ignor = int(self.left_border_ignor)

		right_border_ignor_percent = 10
		self.right_border_ignor = self.w - (float(right_border_ignor_percent) / 100) * self.w
		self.right_border_ignor = int(self.right_border_ignor)
	
		#Groesse des Glases (in %)
		border_glas_distance_percent = 60
		self.border_glas_distance = (float(border_glas_distance_percent) / 100) * self.w
		self.border_glas_distance = int(self.border_glas_distance)

		#Tolleranz der Groesse des Glases (in %)
		border_glas_distance_div_percent = 5
		self.border_glas_distance_div = (float(border_glas_distance_div_percent) / 100) * self.border_glas_distance
		self.border_glas_distance_div = int(self.border_glas_distance_div)

		#Mittlerer Bereich der ignoriert werden soll
		middle_area_ignor_percent = 17
		middle_area_ignor = (float(middle_area_ignor_percent) / 100) * self.w
		middle_area_ignor = int(middle_area_ignor)
		middle_point = self.w / 2
		self.middle_left_point = middle_point - middle_area_ignor
		self.middle_right_point = middle_point + middle_area_ignor

		distance_top_to_bottom_line_percent = 20
		self.distance_top_to_bottom_line = (float(distance_top_to_bottom_line_percent) / 100) * self.h
		self.distance_top_to_bottom_line = int(self.distance_top_to_bottom_line)

	def changeMiddleRightPointValue(self, value):
		self.middle_right_point = int(value)

	def changeMiddleLeftPointValue(self, value):
		self.middle_left_point = int(value)

	def changeDistanceTopToBottomLineValue(self, value):
		self.distance_top_to_bottom_line = int(value)

	def changeBorderGlasDistanceDivValue(self, value):
		self.border_glas_distance_div = int(value)

	def changeBorderGlasDistanceValue(self, value):
		self.border_glas_distance = int(value)

	def changeRightBorderIgnorValue(self, value):
		self.right_border_ignor = int(value)

	def changeLeftBorderIgnorValue(self, value):
		self.left_border_ignor = int(value)

	def changeSetting(self, section):
		self.changeMiddleRightPointValue(self.configParser.getint(str(section), self.middleRightPointString))
		self.changeMiddleLeftPointValue(self.configParser.getint(str(section), self.middleLeftPointString))
		self.changeDistanceTopToBottomLineValue(self.configParser.getint(str(section), self.distanceTopToBottomLineString))
		self.changeBorderGlasDistanceDivValue(self.configParser.getint(str(section), self.borderGlasDistanceDivString))
		self.changeBorderGlasDistanceValue(self.configParser.getint(str(section), self.borderGlasDistanceString))
		self.changeRightBorderIgnorValue(self.configParser.getint(str(section), self.rightBorderIgnorString))
		self.changeLeftBorderIgnorValue(self.configParser.getint(str(section), self.leftBorderIgnorString))

	def saveSetting(self, section):
		if not self.configParser.has_section(str(section)):
			print ('New: ' + section)
			self.addNewSection(section)

	def deleteSection(self, section):
		cfgfile = open(self.configFilename,'w')
		self.configParser.remove_section(str(section))
		self.configParser.write(cfgfile)
		cfgfile.close()

	def addNewSection(self, section):
		cfgfile = open(self.configFilename,'w')
		self.configParser.add_section(str(section))
		self.updateSection(str(section))
		self.configParser.write(cfgfile)
		cfgfile.close()

	def updateSection(self, section):
		print ("Update: " + section)
		self.configParser.set(str(section), self.middleRightPointString, self.middle_right_point)
		self.configParser.set(str(section), self.middleLeftPointString, self.middle_left_point)
		self.configParser.set(str(section), self.distanceTopToBottomLineString, self.distance_top_to_bottom_line)
		self.configParser.set(str(section), self.borderGlasDistanceDivString, self.border_glas_distance_div)
		self.configParser.set(str(section), self.borderGlasDistanceString, self.border_glas_distance)
		self.configParser.set(str(section), self.rightBorderIgnorString, self.right_border_ignor)
		self.configParser.set(str(section), self.leftBorderIgnorString, self.left_border_ignor)
		
	
	
