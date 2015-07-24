#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  State.py
#  
#  Copyright 2015 jokersays <joker@joker-laptop>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

class State:
	
	# run method, should be called by main loop after state change
	def run(self):
		assert 0, "run() not implemented"

	# next method, called for state change, returns next state
	def next(self, input)
		assert 0, "next(input) not implemented"
