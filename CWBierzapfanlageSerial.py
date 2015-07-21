#!/usr/bin/env python

"""
Sebastian Thiems 
Campuswoche 2014

Serielle-Kommunikation zum steuern der Bierzapfanlage.
"""

DEBUG = False

import serial
from enum import Enum

# const confirm
CONST_OK = 1

# const handshake
CONST_HS_AK = 2
CONST_HS_SYNC = 3

# const 
CONST_FILL_START = 'z'.decode('ascii') 
CONST_FILL_STOP = 'a'.decode('ascii')
CONST_ROTATE_START = 'd'.decode('ascii')
CONST_ROTATE_STOP = 's'.decode('ascii')

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
				
	def ReadByte(self):
		return self.ser.read().decode('ascii')

	def StartRotation(self, secs):
		try:
			if self.serialVersion == CWSerialVersion.CWBOARD:
				return StartRotationCWBOARD()
			elif self.serialVersion == CWSerialVersion.RTSCTS:
				return StartRotationRTSCTS()
			else:
				return False
		except:			
			if DEBUG == True:
				print ("StartRotation fail", sys.exc_info())
			return False
		
	def StartRotationCWBOARD(self, secs):
		self.ser.write(CONST_ROTATE_START)
		return self.ReadByte() == CONST_OK
		
	def StartRotationRTSCTS(self, secs):
		self.StopFill()
		#time.sleep(0.5)
		self.ser.setRTS(level=True)
		return True

	def StopRotation(self):
		try:
			if self.serialVersion == CWSerialVersion.CWBOARD:
				return StopRotationCWBOARD()
			elif self.serialVersion == CWSerialVersion.RTSCTS:
				return StopRotationRTSCTS()
			else:
				return False
		except:			
			if DEBUG == True:
				print ("StopRotation fail", sys.exc_info())
			return False
		
	def StopRotationCWBOARD(self):
		self.ser.write(CONST_ROTATE_STOP)
		return self.ReadByte() == CONST_OK
		
	def StopRotationRTSCTS(self):
		self.ser.setRTS(level=False)
		return True

	def StartFill(self):
		try:
			if self.serialVersion == CWSerialVersion.CWBOARD:
				return StartFillCWBOARD()
			elif self.serialVersion == CWSerialVersion.RTSCTS:
				return StartFillRTSCTS()
			else:
				return False
		except:			
			if DEBUG == True:
				print ("StartFill fail", sys.exc_info())
			return False
		
	def StartFillCWBOARD(self):
		self.ser.write(CONST_FILL_START)		
		return self.ReadByte() == CONST_OK
		
	def StartFillRTSCTS(self):
		self.StopRotation()
		#time.sleep(0.10)
		self.ser.setDTR(level=True)
		return True
	
	def StopFill(self):
		try:
			if self.serialVersion == CWSerialVersion.CWBOARD:
				return StopFillCWBOARD()
			elif self.serialVersion == CWSerialVersion.RTSCTS:
				return StopFillRTSCTS()
			else:
				return False
		except:
			if DEBUG == True:
				print "StopFill fail"
			return False
				
	def StopFillCWBOARD(self):
		self.ser.write(CONST_FILL_STOP)
		return self.ReadByte() == CONST_OK
		
	def StopFillRTSCTS(self):
		self.ser.setDTR(level=False)
		return True

	def Close(self):
		try:
			if self.ser.isOpen() != True:
				self.ser.close()
		except:
			if DEBUG == True:
				print ("Close serial fail", sys.exc_info())
				
	def Handshake(self):
		try:
			if self.serialVersion == CWSerialVersion.CWBOARD:
				return HandshakeCWBOARD()
			elif self.serialVersion == CWSerialVersion.RTSCTS:
				return HandshakeRTSCTS()
			else:
				return False
		except:			
			if DEBUG == True:
				print ("Handshake fail", sys.exc_info())
			return False

	def HandshakeCWBOARD(self):
		# waiting for hs request from CW board
		incomingByte = self.ReadByte();
		if incomingByte = CONST_HS_AKAK:
			self.ser.write(CONST_HS_SYNC)
			return self.ReadByte() == CONST_OK
		else: 
			return False
		
	def HandshakeRTSCTS(self):
		return True
		
