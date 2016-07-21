'''
Created on Jun 1, 2016

@author: thiedze
'''

from StateMachine.CWState import CWState

class CWStopRotate(CWState):

    def run(self):
        self.printName()
        self.ExceptionRaised = not self.serialHandler.stopRotation()
        
    def next(self):
        if self.ExceptionRaised == True:
            return self.errorState
        return self.nextState