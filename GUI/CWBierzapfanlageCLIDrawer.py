#!/usr/bin/env python

"""
Sebastian Thiems 
Campuswoche 2014

Dient zum Zeichnen der Hilflinien.
"""

import cv2
from CWConstants import CWConstants

DEBUG = True

class CWCLIDrawer:
	def __init__(self, parameterHandler):
		self.parameterHandler = parameterHandler
		self.left = None
		self.right = None
		self.top = None
		self.bottom_foam = None

	def draw(self, image, left = None, right = None, top = None, bottom_foam = None):		
		pt1 = (self.parameterHandler.left_border_ignor,0)
		pt2 = (self.parameterHandler.left_border_ignor, CWConstants.FRAME_WIDTH)
		cv2.line(image, pt1, pt2, (0, 64, 186), 3)

		pt1 = (self.parameterHandler.right_border_ignor,0)
		pt2 = (self.parameterHandler.right_border_ignor, CWConstants.FRAME_WIDTH)
		cv2.line(image, pt1, pt2, (0, 64, 186), 3)	

		pt1 = (self.parameterHandler.middle_left_point,0)
		pt2 = (self.parameterHandler.middle_left_point, CWConstants.FRAME_WIDTH)
		cv2.line(image, pt1, pt2, (0, 64, 186), 3)		
		
		pt1 = (self.parameterHandler.middle_right_point,0)
		pt2 = (self.parameterHandler.middle_right_point, CWConstants.FRAME_WIDTH)
		cv2.line(image, pt1, pt2, (0, 64, 186), 3)	

		# Left line
		if left != None:
			self.left = left
			pt1 = (left[0],0)
			pt2 = (left[0], CWConstants.FRAME_WIDTH)
			cv2.line(image, pt1, pt2, (255,0,255), 3)

		# Right line
		if right != None:
			self.right = right
			pt1 = (right[0],0)
			pt2 = (right[0], CWConstants.FRAME_WIDTH)
			cv2.line(image, pt1, pt2, (0,0,255), 3)

		# Top line
		if top != None:
			self.top = top
			pt1 = (0,top[1])
			pt2 = (CWConstants.FRAME_HEIGHT, top[1])
			cv2.line(image, pt1, pt2, (0,255,0), 3)
	
		# bottom_foam line
		if self.left != None and self.right != None and bottom_foam != None:
			self.bottom_foam = bottom_foam
			pt1 = (self.left[0],bottom_foam[1])
			pt2 = (self.right[0], bottom_foam[1])
			cv2.line(image, pt1, pt2, (255,0,0), 3)

		if image != None:
			cv2.imshow("Lines", image)



