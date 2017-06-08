'''
Created on Jun 2, 2016

@author: thiedze
'''
from CWConstants import CWConstants


class CWParameterHandler(object):

	def __init__(self):
		#Von der Mitte des Bildes -> Linke und Rechte Kante (in %) bis die gefundenen Linien ignoriert werden
		left_border_ignor_percent = 10
		self.left_border_ignor = (float(left_border_ignor_percent) / 100) * CWConstants.FRAME_WIDTH
		self.left_border_ignor = int(self.left_border_ignor)

		right_border_ignor_percent = 10
		self.right_border_ignor = CWConstants.FRAME_WIDTH - (float(right_border_ignor_percent) / 100) * CWConstants.FRAME_WIDTH
		self.right_border_ignor = int(self.right_border_ignor)
	
		#Groesse des Glases (in %)
		border_glas_distance_percent = 60
		self.border_glas_distance = (float(border_glas_distance_percent) / 100) * CWConstants.FRAME_WIDTH
		self.border_glas_distance = int(self.border_glas_distance)

		#Tolleranz der Groesse des Glases (in %)
		border_glas_distance_div_percent = 5
		self.border_glas_distance_div = (float(border_glas_distance_div_percent) / 100) * self.border_glas_distance
		self.border_glas_distance_div = int(self.border_glas_distance_div)

		#Mittlerer Bereich der ignoriert werden soll
		middle_area_ignor_percent = 17
		middle_area_ignor = (float(middle_area_ignor_percent) / 100) * CWConstants.FRAME_WIDTH
		middle_area_ignor = int(middle_area_ignor)
		middle_point = CWConstants.FRAME_WIDTH / 2
		self.middle_left_point = middle_point - middle_area_ignor
		self.middle_right_point = middle_point + middle_area_ignor

		distance_top_to_bottom_line_percent = 20
		self.distance_top_to_bottom_line = (float(distance_top_to_bottom_line_percent) / 100) * CWConstants.FRAME_HEIGHT
		#self.distance_top_to_bottom_line = int(self.distance_top_to_bottom_line)
		self.distance_top_to_bottom_line = 55
		self.stopProgram = False
		self.demoModus = False
