#!/usr/bin/env python

"""
Sebastian Thiems 
Campuswoche 2014

Serielle-Kommunikation zum steuern der Bierzapfanlage.
"""

import sys

import serial


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

class CWSerialHandler:
		
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
				bytesize=serial.SEVENBITS)
			
			if self.ser.isOpen() != True:
				self.ser.open()
				self.flushSerial()			
		except:
			if DEBUG == True:
				print "Can't open serial port!"
	
	def flushSerial(self):
		self.ser.flushInput()
		self.ser.flushOutput()
		if DEBUG == True:
			print "FlushSerial"
	
	def readByte(self):
		incomingByte = self.ser.read().decode('ascii')
		if DEBUG == True:
			print ("ReadByte", incomingByte)
		return incomingByte

	def writeByte(self, outgoingByte):
		if DEBUG == True:
			print ("WriteByte", outgoingByte)
		self.ser.write(outgoingByte)

	def startRotation(self):
		try:
			if CONST_SERIAL_VERSION == CONST_SERIAL_CWBOARD:
				return self.startRotationCWBOARD()
			elif CONST_SERIAL_VERSION == CONST_SERIAL_RTSCTS:
				return self.startRotationRTSCTS()
			else:
				return False
		except:			
			if DEBUG == True:
				print ("StartRotation fail", sys.exc_info())
			return False
		
	def startRotationCWBOARD(self):
		self.flushSerial()
		self.writeByte(CONST_ROTATE_START)
		return self.readByte() == CONST_OK
		
	def startRotationRTSCTS(self):
		self.stopFill()
		#time.sleep(0.5)
		self.ser.setRTS(level=True)
		return True

	def stopRotation(self):
		try:
			if CONST_SERIAL_VERSION == CONST_SERIAL_CWBOARD:
				return self.stopRotationCWBOARD()
			elif CONST_SERIAL_VERSION == CONST_SERIAL_RTSCTS:
				return self.stopRotationRTSCTS()
			else:
				return False
		except:			
			if DEBUG == True:
				print ("StopRotation fail", sys.exc_info())
			return False
		
	def stopRotationCWBOARD(self):
		self.flushSerial()
		self.writeByte(CONST_ROTATE_STOP)
		return self.readByte() == CONST_OK
		
	def stopRotationRTSCTS(self):
		self.ser.setRTS(level=False)
		return True

	def startFill(self):
		try:
			if CONST_SERIAL_VERSION == CONST_SERIAL_CWBOARD:
				return self.startFillCWBOARD()
			elif CONST_SERIAL_VERSION == CONST_SERIAL_RTSCTS:
				return self.startFillRTSCTS()
			else:
				return False
		except:			
			if DEBUG == True:
				print ("StartFill fail", sys.exc_info())
			return False
		
	def startFillCWBOARD(self):
		self.flushSerial()
		self.writeByte(CONST_FILL_START)		
		return self.readByte() == CONST_OK
		
	def startFillRTSCTS(self):
		self.StopRotation()
		#time.sleep(0.10)
		self.ser.setDTR(level=True)
		return True
	
	def stopFill(self):
		try:
			if CONST_SERIAL_VERSION == CONST_SERIAL_CWBOARD:
				return self.stopFillCWBOARD()
			elif CONST_SERIAL_VERSION == CONST_SERIAL_RTSCTS:
				return self.stopFillRTSCTS()
			else:
				return False
		except:
			if DEBUG == True:
				print "StopFill fail"
			return False
				
	def stopFillCWBOARD(self):
		self.flushSerial()
		self.writeByte(CONST_FILL_STOP)
		return self.readByte() == CONST_OK
		
	def stopFillRTSCTS(self):
		self.ser.setDTR(level=False)
		return True

	def close(self):
		try:
			if self.ser.isOpen() != True:
				self.ser.close()
		except:
			if DEBUG == True:
				print ("Close serial fail", sys.exc_info())
				
	def handshake(self):
		try:
			if CONST_SERIAL_VERSION == CONST_SERIAL_CWBOARD:
				return self.handshakeCWBOARD()
			elif CONST_SERIAL_VERSION == CONST_SERIAL_RTSCTS:
				return self.handshakeRTSCTS()
			else:
				return False
		except:			
			if DEBUG == True:
				print ("Handshake fail", sys.exc_info())
			return False

	def handshakeCWBOARD(self):
		self.flushSerial()
		# waiting for hs request from CW board
		if self.readByte() == CONST_HS_AK:
			self.writeByte(CONST_HS_SYNC)
			if DEBUG == True:			
				print("===========================")

			for count in range(500):
				incomingByte = self.readByte()
				if DEBUG == True:
					print ("SERIAL: Handshake count", count, incomingByte)
				if incomingByte == CONST_OK:
					if DEBUG == True:
						print ("SERIAL: Handshake ok")
					break

			return incomingByte == CONST_OK
		else: 
			return False
		
	def handshakeRTSCTS(self):
		return True
		
