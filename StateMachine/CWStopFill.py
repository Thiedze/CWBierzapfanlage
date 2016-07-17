'''
Created on Jun 1, 2016

@author: thiedze
'''

from StateMachine.CWState import CWState

class CWStopFill(CWState):

    def run(self, image):
        self.ExceptionRaised = not self.serialHandler.stopFill()
        
    def next(self):
        if self.ExceptionRaised == True:
            return self.errorState
        return self.nextState
        
        
        
        