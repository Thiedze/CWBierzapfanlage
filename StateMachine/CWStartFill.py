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

DEBUG = False

class CWStartFill(CWState):

    def getTopBorderFromGlass(self, lines):
        if DEBUG == True:
            print("getTopBorderFromGlass")        
        try:
            topBorder = (0, CWConstants.FRAME_HEIGHT)
            for line in lines[0]:
                #Es wird geschaut, ob die gefundene Linie
                #weiter oben liegt als die aktuelle :and: wagerecht ist :and: noch nicht initialisiert wurde        
                if line[1] < topBorder[1] and line[1] == line[3] and topBorder[1] == CWConstants.FRAME_HEIGHT:
                    topBorder = (line[0], line[1])
                continue
            
            return topBorder
        except:
            print("TopLine fail: ", sys.exc_info())
        
        
    def getFoamBorder(self, contours):
        if DEBUG == True:
            print("getFoamBorder")
        try:
            foamBorder = (0, CWConstants.FRAME_HEIGHT)    
            for cnt in contours:
                x,y,w,h = cv2.boundingRect(cnt)
                #Es wird geschaut, ob die gefundene Kontur(Linie)
                #weiter oben liegt als die aktuelle :and: groesser als 40 Pixel breit ist    
                if (y < foamBorder[1] and w > 1):
                    foamBorder = (x, y)
                    
            return foamBorder
        except: 
            print("BottomFoamLine: ", sys.exc_info())

    def run(self):
        try:
            self.printName()
            foundTopBorder = False
            while True:
                if foundTopBorder == False:
                    lines = self.frameHandler.getLinesFromNextFrame(LineOrientation.Horizontal)
            
                if foundTopBorder == False:
                    topBorder = self.getTopBorderFromGlass(lines)
                    if topBorder[1] != CWConstants.FRAME_HEIGHT:
                        self.ExceptionRaised = not self.serialHandler.startFill()
                        if self.ExceptionRaised == True:
                            break
                        foundTopBorder = True
                        
                if foundTopBorder == True:
                    contours = self.frameHandler.getContoursFromNextFrame((self.parameterHandler.left_border_ignor, self.parameterHandler.middle_left_point), (self.parameterHandler.middle_right_point, self.parameterHandler.right_border_ignor))
                    
                    if contours != None:
                        foamBorder = self.getFoamBorder(contours)
                        
                        print(foamBorder)
                        print(topBorder)
                        
                        if foamBorder[1] - topBorder[1] <= self.parameterHandler.distance_top_to_bottom_line:
                            break
        except:
            traceback.print_exc()
            self.ExceptionRaised = True
        
    def next(self):
        if self.ExceptionRaised == True:
            return self.errorState
        return self.nextState
        
