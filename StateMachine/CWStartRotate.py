'''
Created on Jun 1, 2016

@author: thiedze
'''
from os.path import sys
import traceback

from CLI.CWFrameHandler import LineOrientation
from StateMachine.CWState import CWState


class CWStartRotate(CWState):

    def getLeftBorderFromGlass(self, lines):
        try:
            leftBorder = (self.parameterHandler.middle_left_point,0)
            for line in lines[0]:
                if line[0] < self.parameterHandler.middle_left_point:
                    #Es wird geschaut, ob die gefundene Linie
                    #weiter links liegt als die aktuelle :and: vertikal ist :and: nicht im ignoriertem Bereich liegt
                    if line[0] < leftBorder[0] and line[0] == line[2] and line[0] > self.parameterHandler.left_border_ignor:
                        leftBorder = (line[0], line[1])
                        continue
                    
            return leftBorder
        except: 
            print("getLeftBorderFromGlass fail: : ", sys.exc_info())
        
    def getRightBorderFromGlass(self, lines):
        try:
            rightBorder = (self.parameterHandler.middle_right_point,0)
            for line in lines[0]:
                #length = math.sqrt((line[0]-line[2])**2+(line[1]-line[3])**2)
                if line[0] > self.parameterHandler.middle_right_point:
                    #Es wird geschaut, ob die gefundene Linie
                    #weiter rechts liegt als die aktuelle :and: vertikal ist :and: nicht im ignoriertem Bereich liegt
                    if line[0] > rightBorder[0] and line[0] == line[2] and line[0] < self.parameterHandler.right_border_ignor:
                        rightBorder = (line[0], line[1])
                        continue
                    
            return rightBorder
        except: 
            print("getRightBorderFromGlass fail: ", sys.exc_info())


    def run(self):
        try:
            self.printName()
            if self.serialHandler.handshake() == True:
                self.ExceptionRaised = not self.serialHandler.startRotation()
                if self.ExceptionRaised == False:
                    while True:
                        lines = self.frameHandler.getLinesFromNextFrame(LineOrientation.Vertical)
                        
                        if lines != None:
                            if self.getLeftBorderFromGlass(lines)[0] != self.parameterHandler.middle_left_point and self.getRightBorderFromGlass(lines)[0] != self.parameterHandler.middle_right_point:
                                break
                else:
                    print("start rotate failed \n=========================")
                    self.ExceptionRaised = True 
            else:
                print("handshake failed \n=========================")
                self.ExceptionRaised = True 
        except:
            traceback.print_exc()
            self.ExceptionRaised = True
                
    def next(self):
        if self.ExceptionRaised == True:
            print("Error State: " + self.errorState.__class__.__name__)
            return self.errorState
        return self.nextState
