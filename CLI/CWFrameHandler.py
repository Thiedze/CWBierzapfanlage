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
        
    def __init__(self, capture):
        self.capture = capture
	
    def release(self):
        self.capture.release()
        
    def rotateFrame(self, frame):
        if DEBUG == True:
            print("rotateFrame")
    	if frame != None:
            rows, cols, channel = frame.shape
            M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
            return cv2.warpAffine(frame, M ,(cols,rows))
        else:
            return None
        
    def truncateFrame(self, frame):
        if DEBUG == True:
            print("truncateFrame")
        if frame != None:
            return frame[CWConstants.FRAME_TOP: CWConstants.FRAME_TOP + CWConstants.FRAME_HEIGHT, CWConstants.FRAME_TOP: CWConstants.FRAME_TOP + CWConstants.FRAME_WIDTH]
        else:
            return None
        
    def getPreparedFrames(self, frame, lineOrientation, lowThreshold=50, ratio=3, kernel_size=3):
        if DEBUG == True:
            print("getPreparedFrames")
        preparedFrame = None 
        gray_image = cv2.adaptiveThreshold(self.getNextGrayFrame(frame),255,0,1,15,2)

        if lineOrientation == LineOrientation.Vertical and gray_image != None:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
            gray_image_vertical = cv2.erode(gray_image, kernel)
            gray_image_canny_vertical = cv2.Canny(gray_image_vertical, lowThreshold, lowThreshold*ratio, apertureSize = kernel_size)
            preparedFrame =  cv2.HoughLinesP(gray_image_canny_vertical, 1, math.pi , 1, None, 10, 0)
            
        elif lineOrientation == LineOrientation.Horizontal and gray_image != None:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
            gray_image_horizontal = cv2.erode(gray_image, kernel)
            gray_image_canny_horizontal= cv2.Canny(gray_image_horizontal, lowThreshold, lowThreshold*ratio, apertureSize = kernel_size)
            preparedFrame = cv2.HoughLinesP(gray_image_canny_horizontal, 1, math.pi / 2, 1,    None,  10,   0)        

        return preparedFrame
    
    def getNextGrayFrame(self, frame = None):
        if DEBUG == True:
            print("getNextGrayFrame")
        if frame == None:
            retval, frame = self.capture.read()
        else:
            retval = True
        
        if retval == True:
            return cv2.cvtColor(frame ,cv2.COLOR_BGR2GRAY)
        else:
            return None
    
    def getContoursFromNextFrame(self, leftCutPoint, rightCutPoint):
        if DEBUG == True:
            print("getContoursFromNextFrame")
        color_mask = numpy.zeros((CWConstants.FRAME_HEIGHT,CWConstants.FRAME_WIDTH), numpy.uint8)
        gray_image = self.getNextGrayFrame()
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

        
    def getLinesFromNextFrame(self, lineOrientation):
        if DEBUG == True:
            print("getLinesFromNextFrame")
        retval, frame = self.capture.read()
        
        if retval == True:
            frame = self.rotateFrame(frame)
            frame = self.truncateFrame(frame)        		
    
            if frame != None:
                return self.getPreparedFrames(frame, lineOrientation)
            else:
                return None
        else:
            return None
            
            
            
