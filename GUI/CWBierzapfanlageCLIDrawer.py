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
		cv2.line(image, pt1, pt2, (0, 64, 186), 2)

		pt1 = (self.parameterHandler.right_border_ignor,0)
		pt2 = (self.parameterHandler.right_border_ignor, CWConstants.FRAME_WIDTH)
		cv2.line(image, pt1, pt2, (0, 64, 186), 2)	

		pt1 = (self.parameterHandler.middle_left_point,0)
		pt2 = (self.parameterHandler.middle_left_point, CWConstants.FRAME_WIDTH)
		cv2.line(image, pt1, pt2, (0, 64, 186), 2)		
		
		pt1 = (self.parameterHandler.middle_right_point,0)
		pt2 = (self.parameterHandler.middle_right_point, CWConstants.FRAME_WIDTH)
		cv2.line(image, pt1, pt2, (0, 64, 186), 2)

		pt1 = (0,155)
		pt2 = (CWConstants.FRAME_WIDTH, 155)
		cv2.line(image, pt1, pt2, (255, 64, 186), 2)

		# Left line
		if left != None:
			self.left = left
		if self.left != None:
			left = self.left

		if left != None:
			pt1 = (left[0],0)
			pt2 = (left[0], CWConstants.FRAME_WIDTH)
			cv2.line(image, pt1, pt2, (255,0,255), 3)

		# Right line
		if right != None:
			self.right = right
		if self.right != None:
			right = self.right
		
		if right != None:
			pt1 = (right[0],0)
			pt2 = (right[0], CWConstants.FRAME_WIDTH)
			cv2.line(image, pt1, pt2, (0,0,255), 3)

		# Top line
		if top != None:
			self.top = top		
		if self.top != None:
			top = self.top
		
		if top != None:
			pt1 = (0,top[1])
			pt2 = (CWConstants.FRAME_WIDTH, top[1])
			cv2.line(image, pt1, pt2, (0,255,0), 3)
	
		# bottom_foam line
		if bottom_foam != None:
			self.bottom_foam = bottom_foam
		if self.bottom_foam != None:
			bottom_foam = self.bottom_foam
		
		if bottom_foam != None:
			pt1 = (0,bottom_foam[1])
			pt2 = (CWConstants.FRAME_WIDTH, bottom_foam[1])
			cv2.line(image, pt1, pt2, (255,0,0), 8)

		if image != None:
			cv2.imshow("Lines", image)



