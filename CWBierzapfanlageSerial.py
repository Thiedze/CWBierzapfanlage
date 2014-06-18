#!/usr/bin/env python

"""
Sebastian Thiems 
Campuswoche 2014

Serielle-Kommunikation zum steuern der Bierzapfanlage.
"""

DEBUG = True

import serial
class CWSerial:
	def __init__(self):
		try:		
			self.ser = serial.Serial(
			port='/dev/ttyUSB0', 
			baudrate=9600, 
			parity=serial.PARITY_ODD, 
			stopbits=serial.STOPBITS_TWO,     
			bytesize=serial.SEVENBITS )
			
			if self.ser.isOpen() != True:
					self.ser.open()
		except:
			if DEBUG == True:
				print "Can't open serial port!"

	def StartRotation(self, secs):
		try:
			self.StopFill()
			#time.sleep(0.5)
			self.ser.setRTS(level=True)
		except:
			if DEBUG == True:
				print "StartRotation fail"

	def StopRotation(self):
		try:
			if DEBUG == True:
				print ("Stop Rotation")

			self.ser.setRTS(level=False)
		except:
			if DEBUG == True:
				print "StopRotation fail"

	def StartFill(self):
		try:
			self.StopRotation()
			#time.sleep(0.10)
			self.ser.setDTR(level=True)
		except:
			if DEBUG == True:
				print "StartFill fail"

	def StopFill(self):
		try:
			self.ser.setDTR(level=False)
		except:
			if DEBUG == True:
				print "StopFill fail"

	def Close(self):
		try:
			if self.ser.isOpen() != True:
				self.ser.close()
		except:
			if DEBUG == True:
				print "Close serial fail"

