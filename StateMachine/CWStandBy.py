'''
Created on Jul 21, 2016

@author: thiedze
'''
from os.path import sys
import traceback

from StateMachine.CWState import CWState


class CWStandBy(CWState):

	def run(self):
		try:
			self.printName()
			while self.serialHandler.handshake() == False:
				if self.parameterHandler.stopProgram == True or self.parameterHandler.resume == True:
					break
				continue
		except:
			traceback.print_exc()
			self.ExceptionRaised = True
				
	def next(self):
		if self.ExceptionRaised == True:
			print("Error State: " + self.errorState.__class__.__name__)
			return self.errorState
		return self.nextState
