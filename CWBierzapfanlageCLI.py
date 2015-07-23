#!/usr/bin/env python

from sys import argv

import cv2
import math
#import Image
from PIL import Image
import numpy
import sys
import time
import pdb
#import zbar
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

		self.CWConstants = CWConstants
		self.CWCLIDrawer = CWCLIDrawer(self.CWConstants)
		
		# serial synchronization status 
		self.is_synched = False

		# counter for frame delays
		self.start_count = 0
		self.stop_count = 0
		self.rotat_count = 0
		
		# process variables
		self.is_glass_detection_active = True
		self.current_full_skip_count = 0
		
		self.white_pixel_in_percent = 0

		self.top = (0, self.CWConstants.h)
		self.left = (self.CWConstants.middle_right_point,0)
		self.right = (self.CWConstants.middle_left_point,0)
		self.bottom_beer = (0, self.CWConstants.h)
		self.bottom_foam = (0, self.CWConstants.h)

	
	def LeftLine(self, lines):
		try:
			self.left = (self.CWConstants.middle_left_point,0)
			for line in lines[0]:
				if line[0] < self.CWConstants.middle_left_point:
					#Es wird geschaut, ob die gefundene Linie
					#weiter links liegt als die aktuelle :and: vertikal ist :and: nicht im ignoriertem Bereich liegt
					if line[0] < self.left[0] and line[0] == line[2] and line[0] > self.CWConstants.left_border_ignor:
						self.left = (line[0], line[1])
						continue
			
			# activate glass detection after left line is no longer detected
			if self.is_glass_detection_active == False and self.left[0] == self.CWConstants.middle_left_point:
				self.is_glass_detection_active = True
				if DEBUG == True:
					print("============Glass detection activated")
		except: 
			print("LeftLine fail: : ", sys.exc_info())

	def RightLine(self, lines):
		try:
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
		except: 
			print("RightLine fail: ", sys.exc_info())

	def TopLine(self, lines):
		try:
			for line in lines[0]:
				#Es wird geschaut, ob die gefundene Linie
				#weiter oben liegt als die aktuelle :and: wagerecht ist :and: noch nicht initialisiert wurde		
				if line[1] < self.top[1] and line[1] == line[3] and self.top[1] == self.CWConstants.h:
					self.top = (line[0], line[1])
				continue
		except:
			print("TopLine fail: ", sys.exc_info())
			
	def LinesRecognized(self):
		if (self.top[1] < self.CWConstants.h 
			and self.left[0] < self.CWConstants.middle_left_point
			and self.right[0] > self.CWConstants.middle_right_point):
			return True
		else:
			return False

	def BottomFoamLine(self, lowThreshold, ratio, kernel_size):
		try:
			self.bottom_foam = (0, self.CWConstants.h)	
			
			# use gray_only if one line is not correctly recognized
			cropped_img = self.gray_only
			
			# calculate area: within glass, exclusive limited middle area			
			if self.LinesRecognized():
				# cut borders for false recognition
				left_x = self.left[0] + self.CWConstants.foam_recognition_limit				
				right_x = self.right[0] - self.CWConstants.foam_recognition_limit
				top_y = self.top[1] + self.CWConstants.foam_recognition_limit
				left_area = cropped_img[top_y:self.CWConstants.h, left_x:self.CWConstants.middle_left_point]
				right_area = cropped_img[top_y:self.CWConstants.h, self.CWConstants.middle_right_point:right_x]
				# append right area horizontally to left
				cropped_img = numpy.concatenate((left_area, right_area), axis=1)
						
			#Erstellen der Farbmaske, aus dem Bild rausrechnen, Kanten erkennen, Konturen finden
			color_mask = numpy.zeros((self.CWConstants.h,self.CWConstants.w), numpy.uint8)
			in_range_dst = cv2.inRange(cropped_img, numpy.asarray(40), numpy.asarray(70), color_mask)

			kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(6,6))
			in_range_dst = cv2.erode(in_range_dst, kernel)

			if DEBUG == True:
				cv2.imshow("Foam" , in_range_dst)

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
		except: 
			print("BottomFoamLine: ", sys.exc_info())

	def StopFilling(self):
		# increase stop counter, make sure full glass is recognized
		self.stop_count = self.stop_count + 1
		if self.stop_count == self.CWConstants.wait_frames_count:
			self.CWConfigWindow.fillGlass(False)
			if DEBUG == True:
					print ("--> StopFill")
			self.is_synched = self.CWSerial.StopFill()			
			# reset start / stop counters			
			self.start_count = 0
			self.stop_count = 0	
			
	def StartFilling(self):
		# increase start counter, make sure glass is recognized and not full
		self.start_count = self.start_count + 1
		if self.start_count == self.CWConstants.wait_frames_count * 3:
			self.CWConfigWindow.fillGlass(True)		
			if DEBUG == True:
					print ("--> StartFill")	
			self.is_synched = self.CWSerial.StartFill()
			self.start_count = 0
			self.stop_count = 0
			
	def StopRotation(self):
		self.CWConfigWindow.rotatePlatform(False)
		if DEBUG == True:
					print ("--> StopRotation")
		self.is_synched = self.CWSerial.StopRotation()			

	def GlassFilled(self):
		#Kontrolle, ob die Schaum- oder Bierkante die definierte Hoehe erreicht hat
		if  self.bottom_foam[1] - self.top[1] <= self.CWConstants.distance_top_to_bottom_line or self.bottom_beer[1] - self.top[1] <= self.CWConstants.distance_top_to_bottom_line:
			self.stop_count = self.stop_count + 1
			if DEBUG == True:
					print ("GlassFilled: True")
			return True
		else:
			if DEBUG == True:
					print ("GlassFilled: False")
			return False
				
	def StartRotation(self, instantStart=False):
		self.rotat_count = self.rotat_count + 1
		if instantStart or self.rotat_count == self.CWConstants.wait_frames_count * 2:							
			self.CWConfigWindow.rotatePlatform(True)
			if DEBUG == True:
					print ("--> StartRotation")
			self.rotat_count = 0
			self.is_synched = self.CWSerial.StartRotation(0.0)
			self.top = (0, self.CWConstants.h)
	
	def GlassDetected(self):
		# Erkennung aktiv + Linke und rechte Linie muessen erkannt worden sein
		if (self.is_glass_detection_active == True
			and self.left[0] != self.CWConstants.middle_left_point 
			and self.right[0] != self.CWConstants.middle_right_point):
			self.CWConfigWindow.glasDetected(True)
			if DEBUG == True:
					print ("GlassDetected: True")			
			return True
		else:
			self.CWConfigWindow.glasDetected(False)
			if DEBUG == True:
					print ("GlassDetected: False", ("No glass" if self.is_glass_detection_active else "Same glass"))
			return False
			
	def HitDetection(self):		
		# process for glass detection and filling
		try:
			if self.GlassDetected():			
				self.StopRotation()
				if self.GlassFilled():
					self.StopFilling()
					self.current_full_skip_count += 1									
					# flag for next glass detection
					self.is_glass_detection_active = False
					self.StartRotation()
				else:
					self.current_full_skip_count = 0
					self.StartFilling()				
			else:
				self.StartRotation()
		except:
			if DEBUG == True:
				print ("HitDetection fail: ", sys.exc_info())
				
	def StandbyDetection(self):
		# new synch (handshake) required after too many full glasses w/o refill
		if self.current_full_skip_count >= self.CWConstants.limit_full_glass_detection:
			self.current_full_skip_count = 0
			self.StartRotation(True)
			self.is_synched = False
			if DEBUG == True:
					print ("StandbyDetection: Going into standby mode.")
				
	def GetVerticalLines(self, prepared_frame):
		# image, rho, theta, thres, lines, lenght, stn
		return cv2.HoughLinesP(prepared_frame, 1, math.pi , 1, None, 10, 0)
		
	def GetHorizontalLines(self, prepared_frame):
		# image, rho, theta, thres, lines, lenght, stn
		return cv2.HoughLinesP(prepared_frame, 1, math.pi / 2, 1,    None,  10,   0)

	def PrepareFrame(self, lowThreshold, ratio, kernel_size):
		detected_edges = []
		self.gray = cv2.cvtColor(self.img ,cv2.COLOR_BGR2GRAY)
		self.gray_only = self.gray
		self.gray = cv2.adaptiveThreshold(self.gray,255,0,1,15,2)

		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
		self.gray_vertical = cv2.erode(self.gray, kernel)
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
		self.gray_horizontal = cv2.erode(self.gray, kernel)

		detected_edges.append(cv2.Canny(self.gray_vertical, lowThreshold, lowThreshold*ratio, apertureSize = kernel_size))
		detected_edges.append(cv2.Canny(self.gray_horizontal, lowThreshold, lowThreshold*ratio, apertureSize = kernel_size))

		if DEBUG == True:
			cv2.imshow("Gray Vertical", detected_edges[0])
			cv2.imshow("Gray Horizontal", detected_edges[1])

		return detected_edges

	def edgeDetection(self, lowThreshold=50, ratio=3, kernel_size=3):			
		try:
			prepared_frames = self.PrepareFrame(lowThreshold, ratio, kernel_size)
			vertical_lines = self.GetVerticalLines(prepared_frames[0])
			horizontal_lines = self.GetHorizontalLines(prepared_frames[1])	
			if vertical_lines != None:					
				self.LeftLine(vertical_lines)
				self.RightLine(vertical_lines)
				if horizontal_lines != None:					
					self.TopLine(horizontal_lines)
					# find foam line, requires left, right and top line!
					self.BottomFoamLine(lowThreshold, ratio, kernel_size)					
				elif DEBUG == True:
					print("horizontal_lines", type(horizontal_lines))
			elif DEBUG == True:
				print("vertical_lines", type(vertical_lines))			
		except TypeError:
			if DEBUG == True:
				print ("LineSearching fail: ", sys.exc_info())				
		except:
			if DEBUG == True:
				print (sys.exc_info())

	def DrawOriginal(self):
		try:
			self.CWCLIDrawer.Draw(image=self.img, left=self.left, right=self.right, top=self.top, bottom_foam=self.bottom_foam)
		except:
			if DEBUG == True:			
				print ("Draw fail: ", sys.exc_info())
			
		if DEBUG == True:
			cv2.imshow("Original", self.img)

	'''def extractBarcode(self):
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
				print 'Barcode scanner error: ', sys.exc_info()[0]'''
			
	def rotateImage(self):
		try:
			rows, cols, depth = self.img.shape
			M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
			self.img = cv2.warpAffine(self.img, M ,(cols,rows))
		except:
			if DEBUG == True:
				print ("Rotate failed: ", sys.exc_info())
	
	def Handshake(self):
		try:
			self.is_synched = self.CWSerial.Handshake()
			if DEBUG == True:
				print ("Handshake", self.is_synched)
		except:
			if DEBUG == True:
				print ("CWSerial Handshake / SYNC fail: ", sys.exc_info())
				
	def run(self):
		capture = cv2.VideoCapture(0)
		while True:
			try:	
				# running, no error; else handshake
				if self.is_synched:					
					ret, self.img = capture.read()

					if ret == True:
						
						#cv2.imshow("Hi", self.img)					
						#self.extractBarcode()				
						self.rotateImage()

						#cv2.putText(self.img, str(self.bottom_foam[1]), (self.CWConstants.w/2 + 60, self.CWConstants.h/2), cv2.FONT_HERSHEY_PLAIN, 1.0, 255, thickness=1, lineType=cv2.CV_AA)
						#y: y + h, x: x + w	
						self.img = self.img[self.CWConstants.y: self.CWConstants.y + self.CWConstants.h, self.CWConstants.x: self.CWConstants.x + self.CWConstants.w]		
						
						# get lines for detection
						self.edgeDetection()
						
						# start detection process
						self.HitDetection()
						# go into standby mode (waiting for hs) after full glass limit
						self.StandbyDetection()
						
						if DEBUG == True:
							self.DrawOriginal()

						#cv2.putText(self.img,"Hello World!!!", (self.CWConstants.w/2, self.CWConstants.h/2), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
				else:
					self.Handshake()

			except TypeError:
				if DEBUG == True:
					print ("You have no \"glass\": ", sys.exc_info())		
				self.StartRotation()

			except:
				if DEBUG == True:
					print ("Main loop exception: ", sys.exc_info())
		
			# Listen for ESC key
			c = cv2.waitKey(7) % 0x100
			#if c == 27:
			if self.CWConstants.stopProgram == True:
				self.StartRotation()
				self.CWSerial.Close()
				capture.release()
				break










