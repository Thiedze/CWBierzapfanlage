'''
Created on Jun 2, 2016

@author: thiedze
'''
from os.path import sys

import cv2
from numpy import math
import numpy
from pyatspi.enum import Enum

from CWConstants import CWConstants

DEBUG = False

class LineOrientation(Enum):
	Vertical = 0
	Horizontal = 1
	
class CWFrameHandler(object):
		
	def __init__(self, capture, parameterHandler):
		self.parameterHandler = parameterHandler
		self.capture = capture
		self.frame = None
	
	def setGui(self, gui):
		self.gui = gui

	def release(self):
		self.capture.release()
		
	def printDebugInformations(self, info, left = None, right = None, top = None, bottom_foam = None):
		if DEBUG == False:
			if self.frame != None:
				self.gui.setFrame(self.frame, left, right, top, bottom_foam)
		else:
			cv2.imshow("Debug", self.frame)

	def getLinesFromNextFrame(self, lineOrientation):
		frame = self.getPreparedFrame(True)

		if frame != None:
			return self.getLinesFromFrame(frame, lineOrientation)
		else:
			return None

	def getPreparedFrame(self, returnPreparedFrame):
		retval, frame = self.capture.read()

		if retval == True:
			preparedFrame = self.rotateFrame(frame)
			preparedFrame = self.truncateFrame(preparedFrame)
			self.frame = preparedFrame
			if returnPreparedFrame == True:
				return preparedFrame
			else:
				return frame
		else:
			return None

	def rotateFrame(self, frame):
		if frame != None:
			rows, cols, channel = frame.shape
			M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
			self.rotatedFrame = cv2.warpAffine(frame, M ,(cols,rows))
			return self.rotatedFrame			
		else:
			return None
		
	def truncateFrame(self, frame):
		if frame != None:
			return frame[CWConstants.FRAME_TOP: CWConstants.FRAME_TOP + CWConstants.FRAME_HEIGHT, CWConstants.FRAME_TOP: CWConstants.FRAME_TOP + CWConstants.FRAME_WIDTH]
		else:
			return None

	def getLinesFromFrame(self, frame, lineOrientation, lowThreshold=50, ratio=3, kernel_size=3):
		lines = None 
		gray_image = cv2.adaptiveThreshold(self.getNextGrayFrame(frame),255,0,1,15,2)

		if lineOrientation == LineOrientation.Vertical and gray_image != None:
			kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
			gray_image_vertical = cv2.erode(gray_image, kernel)
			gray_image_canny_vertical = cv2.Canny(gray_image_vertical, lowThreshold, lowThreshold*ratio, apertureSize = kernel_size)
			lines =  cv2.HoughLinesP(gray_image_canny_vertical, 1, math.pi , 1, None, 10, 0)
			self.gui.setDebugFrame(gray_image_canny_vertical)
			
		elif lineOrientation == LineOrientation.Horizontal and gray_image != None:
			kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
			gray_image_horizontal = cv2.erode(gray_image, kernel)
			gray_image_canny_horizontal= cv2.Canny(gray_image_horizontal, lowThreshold, lowThreshold*ratio, apertureSize = kernel_size)
			lines = cv2.HoughLinesP(gray_image_canny_horizontal, 1, math.pi / 2, 1,	None,  10,   0)
			self.gui.setDebugFrame(gray_image_canny_horizontal)		

		return lines
	
	def getNextGrayFrame(self, frame):
		if frame != None:
			return cv2.cvtColor(frame ,cv2.COLOR_BGR2GRAY)
		else:
			return None
	
	def getContoursFromNextFrame(self, leftCutPoint, rightCutPoint):
		color_mask = numpy.zeros((CWConstants.FRAME_HEIGHT,CWConstants.FRAME_WIDTH), numpy.uint8)
		gray_image = self.getNextGrayFrame(self.getPreparedFrame(False))
		if gray_image != None:
			in_range_dst = cv2.inRange(gray_image, numpy.asarray(40), numpy.asarray(70), color_mask)
	
			kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(6,6))
			in_range_dst = cv2.erode(in_range_dst, kernel)			
	
			left_area = in_range_dst[0:CWConstants.FRAME_HEIGHT, leftCutPoint]
			right_area = in_range_dst[0:CWConstants.FRAME_HEIGHT, rightCutPoint]
			
			# append right area horizontally to left
			in_range_dst = numpy.concatenate((left_area, right_area), axis=1)
	
			contours, hierarchy = cv2.findContours(in_range_dst.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

			return contours
		else:
			return None
			
	def getLeftBorderFromGlass(self, lines):
		try:
			leftBorder = (self.parameterHandler.middle_left_point,0)
			for line in lines[0]:
				if line[0] < self.parameterHandler.middle_left_point:
					#Es wird geschaut, ob die gefundene Linie
					#weiter links liegt als die aktuelle :and: vertikal ist :and: nicht im ignoriertem Bereich liegt
					if line[0] < leftBorder[0] and line[0] == line[2] and line[0] > self.parameterHandler.left_border_ignor:
						leftBorder = (line[0], line[1])
						continue

			self.printDebugInformations("getLeftBorderFromGlass", left = leftBorder)
			return leftBorder
		except: 
			print("getLeftBorderFromGlass fail: : ", sys.exc_info())
		
	def getRightBorderFromGlass(self, lines):
		try:
			rightBorder = (self.parameterHandler.middle_right_point,0)
			for line in lines[0]:
				#length = math.sqrt((line[0]-line[2])**2+(line[1]-line[3])**2)
				if line[0] > self.parameterHandler.middle_right_point:
					#Es wird geschaut, ob die gefundene Linie
					#weiter rechts liegt als die aktuelle :and: vertikal ist :and: nicht im ignoriertem Bereich liegt
					if line[0] > rightBorder[0] and line[0] == line[2] and line[0] < self.parameterHandler.right_border_ignor:
						rightBorder = (line[0], line[1])
						continue

			self.printDebugInformations("getRightBorderFromGlass", right = rightBorder)
			return rightBorder
		except: 
			print("getRightBorderFromGlass fail: ", sys.exc_info())
			
			
	def getTopBorderFromGlass(self, lines):
		try:
			topBorder = (0, CWConstants.FRAME_HEIGHT)
			for line in lines[0]:
				#Es wird geschaut, ob die gefundene Linie
				#weiter oben liegt als die aktuelle :and: wagerecht ist :and: noch nicht initialisiert wurde		
				if line[1] < topBorder[1] and line[1] == line[3] and topBorder[1] == CWConstants.FRAME_HEIGHT:
					topBorder = (line[0], line[1])
				continue
			
			self.printDebugInformations("getTopBorderFromGlass", top = topBorder)
			return topBorder
		except:
			print("TopLine fail: ", sys.exc_info())
		
		
	def getFoamBorder(self, contours):
		try:
			foamBorder = (0, CWConstants.FRAME_HEIGHT)	
			for cnt in contours:
				x,y,w,h = cv2.boundingRect(cnt)
				#Es wird geschaut, ob die gefundene Kontur(Linie)
				#weiter oben liegt als die aktuelle	
				if (y < foamBorder[1] and w > 1):
					foamBorder = (x, y)
			
			self.printDebugInformations("getFoamBorder", bottom_foam = foamBorder)
			return foamBorder
		except: 
			print("BottomFoamLine: ", sys.exc_info())
