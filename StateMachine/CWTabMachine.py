'''
Created on Jun 1, 2016

@author: thiedze
'''
from CLI.CWFrameHandler import CWFrameHandler
from CWStartFill import CWStartFill
from CWStartRotate import CWStartRotate
from CWStateMachine import CWStateMachine
from CWStopFill import CWStopFill
from CWStopRotate import CWStopRotate
from Profile.CWParameterHandler import CWParameterHandler
from Serial.CWSerialHandler import CWSerialHandler


class CWTabMachine(CWStateMachine):

    def __init__(self):
        self.initHandler()        
        self.initStates()
        self.setNextStates()
        self.setErrorStates()
        
        CWStateMachine.__init__(self, self.startRotate)
        
    def initHandler(self):
        self.frameHandler = CWFrameHandler() 
        self.serialHandler = CWSerialHandler()
        self.parameterHandler = CWParameterHandler()
        
    def initStates(self):
        self.stopFill = CWStopFill(self.frameHandler, self.serialHandler, self.parameterHandler)
        self.startFill = CWStartFill(self.frameHandler, self.serialHandler, self.parameterHandler)
        self.stopRotate = CWStopRotate(serialHandler = self.serialHandler)
        self.startRotate = CWStartRotate(self.frameHandler, self.serialHandler, self.parameterHandler)
        
    def setNextStates(self):
        self.stopFill.nextState = self.startRotate
        self.startFill.nextState = self.stopFill
        self.startRotate.nextState = self.stopRotate
        self.stopRotate.nextState = self.startFill
        
    def setErrorStates(self):
        self.stopFill.errorState = self.startRotate
        self.startFill.errorState = self.startRotate
        self.startRotate.errorState = self.startRotate
        self.stopRotate.errorState = self.startRotate
        
    def run(self):
        print("Tabmachine run")
        while True:
            self.currentState.run()
            self.currentState = self.currentState.next()
            
        self.frameHandler.release()
        self.serialHandler.close()
            