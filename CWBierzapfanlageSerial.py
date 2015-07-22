#!/usr/bin/env python

"""
Sebastian Thiems 
Campuswoche 2014

Serielle-Kommunikation zum steuern der Bierzapfanlage.
"""

import serial
import sys
import time

# Version of serial connection
CONST_SERIAL_CWBOARD = 0
CONST_SERIAL_RTSCTS = 1
CONST_SERIAL_VERSION = CONST_SERIAL_CWBOARD
#CONST_SERIAL_VERSION = CONST_SERIAL_RTSCTS


# const confirm
CONST_OK = '1'.decode('ascii')

# const handshake
CONST_HS_AK = '2'.decode('ascii')
CONST_HS_SYNC = '3'.decode('ascii')

# const 
CONST_FILL_START = 'z'.decode('ascii') 
CONST_FILL_STOP = 'a'.decode('ascii')
CONST_ROTATE_START = 'd'.decode('ascii')
CONST_ROTATE_STOP = 's'.decode('ascii')

DEBUG = False

class CWSerial:	
	def __init__(self):		
		if DEBUG == True:
			print "Init CWSerial"
		try:	
			if CONST_SERIAL_VERSION == CONST_SERIAL_CWBOARD:	
				self.ser = serial.Serial(
				port='/dev/ttyUSB0', 
				baudrate=9600, 
				parity=serial.PARITY_NONE, 
				stopbits=serial.STOPBITS_TWO,     
				bytesize=serial.EIGHTBITS,
				timeout=5 )
			elif CONST_SERIAL_VERSION == CONST_SERIAL_RTSCTS:
				self.ser = serial.Serial(
				port='/dev/ttyUSB0', 
				baudrate=9600, 
				parity=serial.PARITY_ODD, 
				stopbits=serial.STOPBITS_TWO,     
				bytesize=serial.SEVENBITS,
				timeout=5 )
			
			if self.ser.isOpen() != True:
				self.ser.open()
				self.FlushSerial()			
		except:
			if DEBUG == True:
				print "Can't open serial port!"
	
	def FlushSerial(self):
		self.ser.flushInput()
		self.ser.flushOutput()
	
	def ReadByte(self):
		incomingByte = self.ser.read().decode('ascii')
		if DEBUG == True:
			print ("ReadByte", incomingByte)
		return incomingByte

	def WriteByte(self, outgoingByte):
		if DEBUG == True:
			print ("WriteByte", outgoingByte)
		self.ser.write(outgoingByte)

	def StartRotation(self, secs):
		try:
			if CONST_SERIAL_VERSION == CONST_SERIAL_CWBOARD:
				return self.StartRotationCWBOARD()
			elif CONST_SERIAL_VERSION == CONST_SERIAL_RTSCTS:
				return self.StartRotationRTSCTS()
			else:
				return False
		except:			
			if DEBUG == True:
				print ("StartRotation fail", sys.exc_info())
			return False
		
	def StartRotationCWBOARD(self):
		self.FlushSerial()
		self.WriteByte(CONST_ROTATE_START)
		return self.ReadByte() == CONST_OK
		
	def StartRotationRTSCTS(self):
		self.StopFill()
		#time.sleep(0.5)
		self.ser.setRTS(level=True)
		return True

	def StopRotation(self):
		try:
			if CONST_SERIAL_VERSION == CONST_SERIAL_CWBOARD:
				return self.StopRotationCWBOARD()
			elif CONST_SERIAL_VERSION == CONST_SERIAL_RTSCTS:
				return self.StopRotationRTSCTS()
			else:
				return False
		except:			
			if DEBUG == True:
				print ("StopRotation fail", sys.exc_info())
			return False
		
	def StopRotationCWBOARD(self):
		self.FlushSerial()
		self.WriteByte(CONST_ROTATE_STOP)
		return self.ReadByte() == CONST_OK
		
	def StopRotationRTSCTS(self):
		self.ser.setRTS(level=False)
		return True

	def StartFill(self):
		try:
			if CONST_SERIAL_VERSION == CONST_SERIAL_CWBOARD:
				return self.StartFillCWBOARD()
			elif CONST_SERIAL_VERSION == CONST_SERIAL_RTSCTS:
				return self.StartFillRTSCTS()
			else:
				return False
		except:			
			if DEBUG == True:
				print ("StartFill fail", sys.exc_info())
			return False
		
	def StartFillCWBOARD(self):
		self.FlushSerial()
		self.WriteByte(CONST_FILL_START)		
		return self.ReadByte() == CONST_OK
		
	def StartFillRTSCTS(self):
		self.StopRotation()
		#time.sleep(0.10)
		self.ser.setDTR(level=True)
		return True
	
	def StopFill(self):
		try:
			if CONST_SERIAL_VERSION == CONST_SERIAL_CWBOARD:
				return self.StopFillCWBOARD()
			elif CONST_SERIAL_VERSION == CONST_SERIAL_RTSCTS:
				return self.StopFillRTSCTS()
			else:
				return False
		except:
			if DEBUG == True:
				print "StopFill fail"
			return False
				
	def StopFillCWBOARD(self):
		self.FlushSerial()
		self.WriteByte(CONST_FILL_STOP)
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
			if CONST_SERIAL_VERSION == CONST_SERIAL_CWBOARD:
				return self.HandshakeCWBOARD()
			elif CONST_SERIAL_VERSION == CONST_SERIAL_RTSCTS:
				return self.HandshakeRTSCTS()
			else:
				return False
		except:			
			if DEBUG == True:
				print ("Handshake fail", sys.exc_info())
			return False

	def HandshakeCWBOARD(self):
		self.FlushSerial()
		# waiting for hs request from CW board
		if self.ReadByte() == CONST_HS_AK:
			self.WriteByte(CONST_HS_SYNC)
			if DEBUG == True:			
				print("===========================")

			for count in range(500):
				incomingByte = self.ReadByte()
				print ("SERIAL: Handshake count", count, incomingByte)
				if incomingByte == CONST_OK:
					print ("SERIAL: Handshake ok")
					break

			return incomingByte == CONST_OK
		else: 
			return False
		
	def HandshakeRTSCTS(self):
		return True
		
