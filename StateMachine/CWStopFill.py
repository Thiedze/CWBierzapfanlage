'''
Created on Jun 1, 2016

@author: thiedze
'''
import time
from StateMachine.CWState import CWState

class CWStopFill(CWState):

	def run(self):
		self.printName()
		self.ExceptionRaised = not self.serialHandler.stopFill()
		time.sleep(1)
		
	def next(self):
		if self.ExceptionRaised == True:
			return self.errorState
		return self.nextState
		
		
		
		
