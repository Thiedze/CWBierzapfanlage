#!/usr/bin/env python

"""
Sebastian Thiems 
Campuswoche 2014

Konstanten der Bierzapfanlage.
"""

import os.path

DEBUG = False

class CWConstants:
	def __init__(self):		
		#Groesse des Bildes
		self.w = 380
		self.h = 300
		self.x = 140
		self.y = 100

		#self.img = self.img[100:400, 140:520]

		self.total_number_of_pixel = self.h * self.w
		self.configFilename = "CWBierzapfanlage.cfg"
		self.stopProgram = False

		self.middleRightPointString = 'Middle Right Point'
		self.middleLeftPointString = 'Middle Left Point'
		self.distanceTopToBottomLineString = 'Distance Top To Bottom Line'
		self.borderGlasDistanceDivString = 'Border Glass Distance Div'
		self.borderGlasDistanceString = 'Border Glass Distance'
		self.rightBorderIgnorString = 'Right Border Ignore'
		self.leftBorderIgnorString = 'Left Border Ignore'

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
		
	
	
