'''
Created on Jun 1, 2016

@author: thiedze
'''

from os.path import sys

import cv2
import traceback

from CLI.CWFrameHandler import LineOrientation
from CWConstants import CWConstants
from StateMachine.CWState import CWState

class CWStartFill(CWState):

	def run(self):
		try:
			self.printName()
			foundTopBorder = False
			startFillCounter = 0
			while True:
				if self.parameterHandler.stopProgram == True:
					break
				if foundTopBorder == False:
					lines = self.frameHandler.getLinesFromNextFrame(LineOrientation.Horizontal)
		
				if foundTopBorder == False:
					topBorder = self.frameHandler.getTopBorderFromGlass(lines)
					if topBorder[1] != CWConstants.FRAME_HEIGHT:
						foundTopBorder = True
					
				if foundTopBorder == True:
					contours = self.frameHandler.getContoursFromNextFrame((self.parameterHandler.left_border_ignor, self.parameterHandler.middle_left_point), (self.parameterHandler.middle_right_point, self.parameterHandler.right_border_ignor))
					
					if contours != None:
						foamBorder = self.frameHandler.getFoamBorder(contours)
					
						if foamBorder[1] - topBorder[1] <= self.parameterHandler.distance_top_to_bottom_line or (foamBorder[1] > topBorder[1] and foamBorder[1] != CWConstants.FRAME_HEIGHT):
							break
						else:
							startFillCounter = startFillCounter + 1
						
							if startFillCounter == 30:
								self.ExceptionRaised = not self.serialHandler.startFill()
					
						if self.ExceptionRaised == True:
							break
		except:
			traceback.print_exc()
			self.ExceptionRaised = True
		
	def next(self):
		if self.ExceptionRaised == True:
			return self.errorState
		return self.nextState
		
