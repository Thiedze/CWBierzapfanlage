'''
Created on Jun 1, 2016

@author: thiedze
'''
from os.path import sys
import traceback
import time

from CLI.CWFrameHandler import LineOrientation
from StateMachine.CWState import CWState


class CWStartRotate(CWState):

    def run(self):
        try:
            self.printName()
            self.ExceptionRaised = not self.serialHandler.startRotation()
            if self.ExceptionRaised == False:
                self.SkipBorderCount = 0
                while True:
                    lines = self.frameHandler.getLinesFromNextFrame(LineOrientation.Vertical)
                    
                    if lines != None:
                        if self.frameHandler.getLeftBorderFromGlass(lines)[0] == self.parameterHandler.middle_left_point:
                            self.SkipBorderCount = self.SkipBorderCount + 1
                        
                        if self.SkipBorderCount == 2:
                            break
            else:
                print("start rotate failed \n=========================")
                self.ExceptionRaised = True 
        except:
            traceback.print_exc()
            self.ExceptionRaised = True
                
    def next(self):
        if self.ExceptionRaised == True:
            print("Error State: " + self.errorState.__class__.__name__)
            return self.errorState
        return self.nextState
