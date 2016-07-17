#!/usr/bin/env python

"""
Sebastian Thiems 
Campuswoche 2014

Konstanten der Bierzapfanlage.
"""

class CWConstants:
	
	FRAME_HEIGHT = 330
	FRAME_WIDTH = 380
	FRAME_TOP = 100
	FRAME_LEFT = 140
	
	FOAM_RECOGNITION_LIMIT = 20
	
	LIMIT_FULL_GLASS_DETECTION = 12
	
	WAIT_FRAMES = 0
	
	TOTAL_NUMBER_OF_PIXELS = FRAME_HEIGHT * FRAME_WIDTH

	CONFIGURATION_FILENAME = "CWBierzapfanlage.cfg"
	
	MIDDLE_RIGHT_POINT_CAPTION = 'Middle Right Point' 
	MIDDLE_LEFT_POINT_CAPTION  = 'Middle Left Point'
	DISTANCE_TOP_TO_BOTTOM_LINE_CAPTION = 'Distance Top To Bottom Line'
	BORDER_GLASS_DISTANCE_DIFFERENCE_CAPTION = 'Border Glass Distance Div'
	BORDER_GLASS_DISTANCE_CAPTION  = 'Border Glass Distance'
	RIGHT_BORDER_IGNORE_CAPTION  = 'Right Border Ignore'
	LEFT_BORDER_IGNORE_CAPTION  = 'Left Border Ignore'