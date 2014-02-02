#!/usr/bin/env python

"""
Sebastian Thiems 
Campuswoche 2014

Dient zum Zeichnen der Hilflinien.
"""

import cv2

class CWCLIDrawer:
	def __init__(self, CWConstants = None):
		self.CWConstants = CWConstants

	def Draw(self, image, left, right, top, bottom_foam):
		pt1 = (self.CWConstants.left_border_ignor,0)
		pt2 = (self.CWConstants.left_border_ignor,self.CWConstants.h)
		cv2.line(image, pt1, pt2, (0, 64, 186), 3)		

		pt1 = (self.CWConstants.right_border_ignor,0)
		pt2 = (self.CWConstants.right_border_ignor,self.CWConstants.h)
		cv2.line(image, pt1, pt2, (0, 64, 186), 3)	

		pt1 = (self.CWConstants.middle_left_point,0)
		pt2 = (self.CWConstants.middle_left_point,self.CWConstants.h)
		cv2.line(image, pt1, pt2, (0, 64, 186), 3)		

		pt1 = (self.CWConstants.middle_right_point,0)
		pt2 = (self.CWConstants.middle_right_point,self.CWConstants.h)
		cv2.line(image, pt1, pt2, (0, 64, 186), 3)	
		
		# Left line
		pt1 = (self.left[0],0)
		pt2 = (self.left[0],self.CWConstants.h)
		if self.IsInRange():
			cv2.line(image, pt1, pt2, (255,0,255), 3)
	
		# Right line
		pt1 = (self.right[0],0)
		pt2 = (self.right[0],self.CWConstants.h)
		if self.IsInRange():
		    	cv2.line(image, pt1, pt2, (0,0,255), 3)

		# Top line
		pt1 = (0,self.top[1])
		pt2 = (self.CWConstants.w, self.top[1])
		if self.IsInRange():		
		    	cv2.line(image, pt1, pt2, (0,255,0), 3)
			
		"""# bottom_beer line
		pt1 = (0,self.bottom_beer[1])
	    	pt2 = (self.w, self.bottom_beer[1])
		if self.IsInRange():
			cv2.line(self.img, pt1, pt2, (0,255,255), 3)"""
	
		# bottom_foam line
		pt1 = (self.left[0],self.bottom_foam[1])
		pt2 = (self.right[0], self.bottom_foam[1])
		if self.IsInRange() and self.bottom_foam[1] != self.CWConstants.h:
			cv2.line(image, pt1, pt2, (255,0,0), 3)

	def IsInRange(self):
		#return  self.left[0] != self.middle_right_point and self.right[0] != self.middle_left_point
		return True


