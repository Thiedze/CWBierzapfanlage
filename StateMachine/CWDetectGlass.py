'''
Created on Jun 1, 2016

@author: thiedze
'''
from os.path import sys
import traceback
import time

from CLI.CWFrameHandler import LineOrientation
from StateMachine.CWState import CWState

class CWDetectGlass(CWState):

	def run(self):
		try:
			self.printName()
			while True:
				if self.parameterHandler.stopProgram == True:
					print("exit")
					break
				lines = self.frameHandler.getLinesFromNextFrame(LineOrientation.Vertical)
				
				if lines != None:
					if self.frameHandler.getLeftBorderFromGlass(lines)[0] != self.parameterHandler.middle_left_point and self.frameHandler.getRightBorderFromGlass(lines)[0] != self.parameterHandler.middle_right_point:
						break 
		except:
			traceback.print_exc()
			self.ExceptionRaised = True
				
	def next(self):
		if self.ExceptionRaised == True:
			print("Error State: " + self.errorState.__class__.__name__)
			return self.errorState
		return self.nextState
