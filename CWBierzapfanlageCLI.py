#!/usr/bin/env python

from sys import argv

import cv2
import math
import Image
import numpy
import sys
import time
import pdb
import zbar
import subprocess
from thread import start_new_thread
from CWBierzapfanlageSerial import CWSerial
from CWBierzapfanlageConstants import CWConstants
from CWBierzapfanlageCLIDrawer import CWCLIDrawer

DEBUG = True

class CWDetection:

	def __init__ (self, CWConstants, CWConfigWindow):
		self.CWConfigWindow = CWConfigWindow
		self.CWSerial = CWSerial()
		self.CWSerial.StopFill()
		self.CWSerial.StopRotation()

		self.CWConstants = CWConstants
		self.CWCLIDrawer = CWCLIDrawer(self.CWConstants)

		self.start_count = 0
		self.stop_count = 0
		self.rotat_count = 0
		self.stop_after_fill = False
		self.stop_after_fill_count = 0
		self.full = True
		self.white_pixel_in_percent = 0
		self.full = False
		self.empty = True
		self.ready_to_fill = True

		self.top = (0, self.CWConstants.h)
		self.left = (self.CWConstants.middle_right_point,0)
		self.right = (self.CWConstants.middle_left_point,0)
		self.bottom_beer = (0, self.CWConstants.h)
		self.bottom_foam = (0, self.CWConstants.h)

	
	def LeftLine(self, lines):
		self.left = (self.CWConstants.middle_left_point,0)
		for line in lines[0]:
			if line[0] < self.CWConstants.middle_left_point:
				#Es wird geschaut, ob die gefundene Linie
				#weiter links liegt als die aktuelle :and: vertikal ist :and: nicht im ignoriertem Bereich liegt
				if line[0] < self.left[0] and line[0] == line[2] and line[0] > self.CWConstants.left_border_ignor:
					self.left = (line[0], line[1])
					continue

	def RightLine(self, lines):
		self.right = (self.CWConstants.middle_right_point,0)
		for line in lines[0]:
			#length = math.sqrt((line[0]-line[2])**2+(line[1]-line[3])**2)
			if line[0] > self.CWConstants.middle_right_point:
				#Es wird geschaut, ob die gefundene Linie
				#weiter rechts liegt als die aktuelle :and: vertikal ist :and: nicht im ignoriertem Bereich liegt
				if line[0] > self.right[0] and line[0] == line[2] and line[0] < self.CWConstants.right_border_ignor:
					#Passt die Distanze
					#if line[0] - self.left[0] >= self.CWConstants.border_glas_distance - self.CWConstants.border_glas_distance_div:
						#if line[0] - self.left[0] <= self.CWConstants.border_glas_distance + self.CWConstants.border_glas_distance_div:
					self.right = (line[0], line[1])
					continue

	def TopLine(self, lines):
		for line in lines[0]:
			#Es wird geschaut, ob die gefundene Linie
			#weiter oben liegt als die aktuelle :and: wagerecht ist :and: noch nicht initialisiert wurde		
			if line[1] < self.top[1] and line[1] == line[3] and self.top[1] == self.CWConstants.h:
				self.top = (line[0], line[1])
			continue

	"""def BottomBeerLine(self, lowThreshold, ratio, kernel_size):
		self.bottom_beer = (0, self.h)

		#Gelber Bereich
		MIN = numpy.array([50, 140, 175],numpy.uint8) - 20
		MAX = numpy.array([30, 90, 110],numpy.uint8)

		#Erstellen der Farbmaske, aus dem Bild rausrechnen, Kanten erkennen, Konturen finden
		color_mask = numpy.zeros((self.h,self.w,3), numpy.uint8)
		in_range_dst = cv2.inRange(self.img, MIN, MAX, color_mask)

		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4))
		in_range_dst = cv2.erode(in_range_dst, kernel)
		
		self.in_range_beer = in_range_dst.copy()

		contours, hierarchy = cv2.findContours(in_range_dst,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		#cv2.imshow("Beer", in_range_dst)

		for cnt in contours:
			x,y,w,h = cv2.boundingRect(cnt)
			#Es wird geschaut, ob die gefundene Kontur(Linie)
			#weiter unten liegt als die aktuelle :and: im Messbereich liegt :and: groesser als 15 Pixel breit ist	
			if y < self.bottom_beer[1] and w > 5:
				self.bottom_beer = (x, y)"""

	def BottomFoamLine(self, lowThreshold, ratio, kernel_size):
		self.bottom_foam = (0, self.CWConstants.h)		
		
		#Erstellen der Farbmaske, aus dem Bild rausrechnen, Kanten erkennen, Konturen finden
		color_mask = numpy.zeros((self.CWConstants.h,self.CWConstants.w), numpy.uint8)
		in_range_dst = cv2.inRange(self.gray_only, numpy.asarray(40), numpy.asarray(70), color_mask)

		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(6,6))
		in_range_dst = cv2.erode(in_range_dst, kernel)

		#cv2.imshow("Foam" , in_range_dst)

		contours, hierarchy = cv2.findContours(in_range_dst,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		number_of_black_pixel = self.CWConstants.total_number_of_pixel - cv2.countNonZero(in_range_dst)
		white_pixel_in_percent_image =  (1 -float(number_of_black_pixel)/ float(self.CWConstants.total_number_of_pixel))*100

		if white_pixel_in_percent_image >= self.white_pixel_in_percent:
			for cnt in contours:
				x,y,w,h = cv2.boundingRect(cnt)
				#Es wird geschaut, ob die gefundene Kontur(Linie)
				#weiter oben liegt als die aktuelle :and: groesser als 40 Pixel breit ist	
				if y < self.bottom_foam[1] and w > 1 and  (x > self.CWConstants.left_border_ignor or x < self.CWConstants.right_border_ignor) and (x < self.CWConstants.middle_left_point or x > self.CWConstants.middle_right_point):
					self.bottom_foam = (x, y)


	def HitDetection(self):

		x = 5

		#Linke und rechte Linie muessen erkannt worden sein
		if self.left[0] != self.CWConstants.middle_left_point and self.right[0] != self.CWConstants.middle_right_point and self.left[0] != self.CWConstants.left_border_ignor and self.right[0] != self.CWConstants.right_border_ignor:
			
			if DEBUG == True:
				print ("=================Found side")			

			self.CWSerial.StopRotation()	
			self.stop_after_fill = False
			self.empty = True
			
			#Kontrolle, ob die Schaum- oder Bierkante die definierte Hoehe erreicht hat
			if  self.bottom_foam[1] - self.top[1] <= self.CWConstants.distance_top_to_bottom_line or self.bottom_beer[1] - self.top[1] <= self.CWConstants.distance_top_to_bottom_line:
				self.stop_count = self.stop_count + 1

				if self.stop_after_fill == False and self.stop_count == x:
					self.CWSerial.StopFill()
					self.stop_after_fill = True
					self.start_count = 0
					self.stop_count = 0	
			else:
				self.start_count = self.start_count + 1

				if self.stop_after_fill == False and self.start_count == x * 3 and self.empty == True:
					self.CWConfigWindow.glasDetected(True)
					self.CWSerial.StartFill()
					self.start_count = 0
					self.stop_count = 0
		
		else:
			self.rotat_count = self.rotat_count + 1
			if self.rotat_count == x * 2:
				self.CWConfigWindow.glasDetected(False)
				self.rotat_count = 0
				if DEBUG == True:
					print ("=================Found no side")
				self.CWSerial.StartRotation(0.0)
				self.top = (0, self.CWConstants.h)
				
					

		if self.stop_after_fill == True:
			if DEBUG == True:
				print ("=================Stop after fill")
			self.CWSerial.StartRotation(0.0)
			self.stop_after_fill_count = self.stop_after_fill_count + 1
			
			if self.stop_after_fill_count == x and self.ready_to_fill == False:
				self.stop_after_fill = False
				self.empty = True
				self.stop_after_fill_count = 0

	def edgeDetection(self, lowThreshold=50, ratio=3, kernel_size=3):
		self.gray = cv2.cvtColor(self.img ,cv2.COLOR_BGR2GRAY)
		self.gray_only = self.gray
		self.gray = cv2.adaptiveThreshold(self.gray,255,0,1,15,2)

		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
		self.gray_vertical = cv2.erode(self.gray, kernel)
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
		self.gray_horizontal = cv2.erode(self.gray, kernel)

		detected_edges_vertical = cv2.Canny(self.gray_vertical, lowThreshold, lowThreshold*ratio, apertureSize = kernel_size)
		detected_edges_horizontal = cv2.Canny(self.gray_horizontal, lowThreshold, lowThreshold*ratio, apertureSize = kernel_size)

		if DEBUG == True:
			cv2.imshow("Gray Vertical", detected_edges_vertical)
			cv2.imshow("Gray Horizontal", detected_edges_horizontal)

		#					image		     rho  theta      thres  lines  lenght   stn
		horizontal_lines = cv2.HoughLinesP(detected_edges_horizontal, 1, math.pi / 2, 1,    None,  10,   0)
		vertical_lines = cv2.HoughLinesP(detected_edges_vertical, 1, math.pi , 1, None, 10, 0)

		#Test-Ausgabe aller gefundenen Linien
		if DEBUG == True:
			for line in vertical_lines[0]:
				pt1 = (line[0], line[1])
				pt2 = (line[2], line[3])
				cv2.line(self.img, pt1, pt2, (0,0,255), 3)
			
		try:
			self.LeftLine(vertical_lines)
			self.RightLine(vertical_lines)
			self.TopLine(horizontal_lines)
			#self.BottomBeerLine(lowThreshold, ratio, kernel_size)
			self.BottomFoamLine(lowThreshold, ratio, kernel_size)
			
		except TypeError:
			if DEBUG == True:
				print ("LineSearching fail")

		try:
			self.HitDetection()
		except:
			if DEBUG == True:
				print ("HitDetection fail")

		try:
			self.CWCLIDrawer.Draw(image=self.img, left=self.left, right=self.right, top=self.top, bottom_foam=self.bottom_foam)
		except:
			if DEBUG == True:			
				print ("Draw fail")
			

		if DEBUG == True:
			cv2.imshow("Original", self.img)

	def extractBarcode(self):
		try:
			if DEBUG == True:
				cv2.imshow("Barcode Image", self.img)			
			scanner = zbar.ImageScanner()
			scanner.parse_config('enable')
			barcodeImage = Image.fromarray(self.img).convert('L')
			width, height = barcodeImage.size
			raw = barcodeImage.tostring()
			barcodeScanned = zbar.Image(width, height, 'Y800', raw)
			scanner.scan(barcodeScanned)
		
			for symbol in barcodeScanned:
				if symbol.data == '1234567890128':
					print 'Hit' + now()
		except:
			if DEBUG == True:
				print 'Barcode scanner error: ', sys.exc_info()[0]
			
	def rotateImage(self):
		try:
			rows, cols, depth = self.img.shape
			M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
			self.img = cv2.warpAffine(self.img, M ,(cols,rows))
		except:
			if DEBUG == True:
				print ("Rotate failed: ", sys.exc_info())
	def run(self):
		capture = cv2.VideoCapture(0)
		while True:
			try:	
				ret, self.img = capture.read()

				if ret == True:
					#cv2.imshow("Hi", self.img)					
					#self.extractBarcode()				
					self.rotateImage()
					#y: y + h, x: x + w	
					self.img = self.img[self.CWConstants.y: self.CWConstants.y + self.CWConstants.h, self.CWConstants.x: self.CWConstants.x + self.CWConstants.w]		
					self.edgeDetection()

			except TypeError:
				if DEBUG == True:
					print ("You have no \"glass\"")
				self.CWSerial.StartRotation(0)

			except:
				capture = cv2.VideoCapture(0)
				if DEBUG == True:
					print ("No Cam: ", sys.exc_info()[0])

				#self.CWSerial.Close()
				#print 'Start script'
				#start_new_thread(subprocess.call(['./CWBierzapfanlage.py']))
				#print 'Kill myself'
				#sys.exit(0)				
		
			# Listen for ESC key
			c = cv2.waitKey(7) % 0x100
			#if c == 27:
			if self.CWConstants.stopProgram == True:
				self.CWSerial.Close()
				capture.release()
				break










