#!/usr/bin/env python

"""
Sebastian Thiems 
Campuswoche 2014

Serielle-Kommunikation zum steuern der Bierzapfanlage.
"""
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
			print "Can't open serial port!"

	def StartRotation(self, secs):
		try:
			#print ("Start Rotation")
			self.StopFill()
			time.sleep(secs)
			self.ser.setRTS(level=True)
		except:
			print "StartRotation fail"

	def StopRotation(self):
		try:
			#print ("Stop Rotation")
			self.ser.setRTS(level=False)
		except:
			print "StopRotation fail"

	def StartFill(self):
		try:
			#print ("Start Fill")
			self.StopRotation()
			#time.sleep(0.10)
			self.ser.setDTR(level=True)
		except:
			print "StartFill fail"

	def StopFill(self):
		try:
			#print ("Stop Fill")
			self.ser.setDTR(level=False)
		except:
			print "StopFill fail"

	def Close(self):
		try:
			if self.ser.isOpen() != True:
				self.ser.close()
		except:
			print "Close serial fail"
