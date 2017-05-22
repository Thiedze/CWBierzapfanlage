'''
Created on Jun 1, 2016

@author: thiedze
'''
from os.path import sys
import cv2

from CLI.CWFrameHandler import CWFrameHandler
from CWStartFill import CWStartFill
from CWStartRotate import CWStartRotate
from CWStateMachine import CWStateMachine
from CWStopFill import CWStopFill
from CWStopRotate import CWStopRotate
from CWStandBy import CWStandBy
from CWDetectGlass import CWDetectGlass
from Profile.CWParameterHandler import CWParameterHandler
from Serial.CWSerialHandler import CWSerialHandler

class CWTabMachine(CWStateMachine):

	def __init__(self):
		self.capture = cv2.VideoCapture(0)
		self.initHandler()		
		self.initStates()
		self.setNextStates()
		self.setErrorStates()
		
		CWStateMachine.__init__(self, self.standBy)
		
	def setGui(self, gui):
		self.frameHandler.setGui(gui)

	def initHandler(self):
		self.parameterHandler = CWParameterHandler()
		self.frameHandler = CWFrameHandler(self.capture, self.parameterHandler) 
		self.serialHandler = CWSerialHandler()
		
	def initStates(self):
		self.stopFill = CWStopFill(self.frameHandler, self.serialHandler, self.parameterHandler)
		self.startFill = CWStartFill(self.frameHandler, self.serialHandler, self.parameterHandler)
		self.stopRotate = CWStopRotate(serialHandler=self.serialHandler)
		self.startRotate = CWStartRotate(self.frameHandler, self.serialHandler, self.parameterHandler)
		self.standBy = CWStandBy(self.frameHandler, self.serialHandler, self.parameterHandler)
		self.detectGlass = CWDetectGlass(self.frameHandler, self.serialHandler, self.parameterHandler)
		
	def setNextStates(self):
		self.stopFill.nextState = self.startRotate
		self.startFill.nextState = self.stopFill
		self.startRotate.nextState = self.detectGlass
		self.detectGlass.nextState = self.stopRotate 
		self.stopRotate.nextState = self.startFill
		self.standBy.nextState = self.startRotate
		
	def setErrorStates(self):
		self.stopFill.errorState = self.standBy
		self.startFill.errorState = self.standBy
		self.startRotate.errorState = self.standBy
		self.stopRotate.errorState = self.standBy
		self.detectGlass.errorState = self.standBy
		self.standBy.errorState = self.standBy
		
	def run(self):
		try:
			while True:
				self.currentState.run()
				self.currentState = self.currentState.next()
				
				if self.parameterHandler.stopProgram == True:
					self.frameHandler.release()
					self.serialHandler.close()
					break
			sys.exit(0)
		except:
			print (sys.exc_info())
			self.frameHandler.release()
			self.serialHandler.close()
			
