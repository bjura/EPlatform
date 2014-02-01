#!/bin/env python2.7
# -*- coding: utf-8 -*-



# This file is part of EPlatform.
#
# EPlatform is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# EPlatform is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EPlatform. If not, see <http://www.gnu.org/licenses/>.



import wxversion
wxversion.select('2.8')

import glob, os, time
import time
from random import shuffle

import wx
import wx.lib.buttons as bt
from pymouse import PyMouse
import Tkinter
import numpy as np

import subprocess as sp
import shlex
import pygame
from pygame import mixer

import EGaps, EMistake, EPuzzle, EMatch




class cwiczenia(wx.Frame):
	def __init__(self, parent, id):
		
		wx.Frame.__init__( self , parent , id , 'e-platform main menu')
		self.Maximize( True )
		self.winWidth, self.winHeight = wx.DisplaySize( )
		self.parent=parent
                style = self.GetWindowStyle()
		self.SetWindowStyle( style | wx.STAY_ON_TOP )
		self.initializeParameters()
		self.createGui()
		self.initializeTimer()
		self.Bind( wx.EVT_CLOSE , self.OnExit )

	def initializeParameters(self):
                self.pathToEPlatform = './'
		    
		with open( self.pathToEPlatform + 'parameters', 'r' ) as parametersFile:
			for line in parametersFile:

				if line[ :line.find('=')-1 ] == 'timeGap':
					self.timeGap = int( line[ line.rfind('=')+2:-1 ] )
				elif line[ :line.find('=')-1 ] == 'backgroundColour':
					self.backgroundColour = line[ line.rfind('=')+2:-1 ]
				elif line[ :line.find('=')-1 ] == 'textColour':
					self.textColour = line[ line.rfind('=')+2:-1 ]
				elif line[ :line.find('=')-1 ] == 'scanningColour':
					self.scanningColour = line[ line.rfind('=')+2:-1 ]
				elif line[ :line.find('=')-1 ] == 'selectionColour':
					self.selectionColour = line[ line.rfind('=')+2:-1 ]
				elif line[ :line.find('=')-1 ] == 'musicVolume':
					pass
				elif line[ :line.find('=')-1 ] == 'filmVolume':
					pass

				elif not line.isspace( ):
					print '\nNiewłaściwie opisany parametr. Błąd w linii:\n%s' % line
					
					self.timeGap = 1500
					self.backgroundColour = 'white'
					self.textColour = 'black'
					self.scanningColour =  '#E7FAFD'
					self.selectionColour = '#9EE4EF'

		
                with open( self.pathToEPlatform + 'parametersCW', 'r' ) as parametersFile:
			for line in parametersFile:

                                

                                if line[ :line.find('=')-1 ] == 'textSize':
					self.textSize = int( line[ line.rfind('=')+2:-1 ])
				elif line[ :line.find('=')-1 ] == 'checkTime':
                                        pass
				elif line[ :line.find('=')-1 ] == 'colorGrat':
                                        pass
                                
				elif line[ :line.find('=')-1 ] == 'maxPoints':
					self.maxPoints = int(line[ line.rfind('=')+2:-1 ])
				elif line[ :line.find('=')-1 ] == 'colorNiest':
                                        pass
                                elif line[ :line.find('=')-1 ] == 'ileLuk':
                                        pass
						
				elif not line.isspace( ):
					print 'Niewłaściwie opisane parametry'
					print 'Błąd w linii', line

					self.textSize=200
					#self.maxPoints=2

		#self.ownWord=''
		self.flaga=0
		#self.PicNr=0
		#self.result=0
		self.mouseCursor = PyMouse( )
		#self.WordsList=os.listdir(self.pathToEPlatform+'multimedia/pictures')
		#shuffle(self.WordsList)
                self.poczatek=True
		self.numberOfPresses = 1
		#self.czyBack=False
		mixer.init()

	def initializeTimer(self):

                id1=wx.NewId()
                wx.RegisterId(id1)
		self.stoper = wx.Timer(self,id1)
		self.Bind( wx.EVT_TIMER, self.timerUpdate, self.stoper,id1 )
		
		self.stoper.Start( self.timeGap )

	def timerUpdate(self,event):

                self.mouseCursor.move( self.winWidth - 12, self.winHeight - 12 )

                self.numberOfPresses = 0
                		
		for i in range(4):
			item = self.mainSizer.GetItem(i)
                        b = item.GetWindow()
                        b.SetBackgroundColour( self.backgroundColour )
                        b.SetFocus()

                   
                item = self.mainSizer.GetItem(self.flaga)
                b = item.GetWindow()
                b.SetBackgroundColour( self.scanningColour )
                b.SetFocus()
                if self.flaga==3:
                        self.flaga=0
                else:
                        self.flaga+=1

			
	
	def createGui(self):


                self. mainSizer = wx.BoxSizer( wx.VERTICAL )

                nazwy=[u'UŁÓŻ PUZZLE',u'ZNAJDŹ BŁĄD', u'UZUPEŁNIJ LUKĘ',u'NAZWIJ OBRAZEK']
                kolory=['indian red', 'green', 'orange red', 'cadet blue' ]
                        
                for i in range(4):
                        b = bt.GenButton( self, -1, nazwy[i], name = nazwy[i])
			b.SetFont( wx.Font( 75, wx.FONTFAMILY_ROMAN, wx.FONTWEIGHT_LIGHT,  False ) )
			b.SetBezelWidth( 3 )
			b.SetBackgroundColour( self.backgroundColour )
			b.SetForegroundColour(kolory[i])
			b.Bind( wx.EVT_LEFT_DOWN, self.onPress )
                        self. mainSizer.Add( b, proportion=1, flag=wx.EXPAND )
                self.SetSizer( self. mainSizer)
		self.Layout()
		self.Refresh()
		self.Center()
		self.MakeModal(True)
		self.flaga=0



	def OnExit(self,event):
                self.MakeModal(False)
                self.Destroy()


	def onPress(self,event):


                self.numberOfPresses += 1
		
		if self.numberOfPresses == 1:

                
                        items=self.mainSizer.GetChildren()
                        if self.flaga ==0:
                                b = items[3].GetWindow()
                        else:
                                b = items[self.flaga-1].GetWindow()
                        b.SetBackgroundColour( self.selectionColour )
                        b.SetFocus()
                        b.Update()
                
                	if self.flaga-1 == 0 :
                		self.stoper.Stop()
                		EPuzzle.cwiczenia( self,id= -1).Show(True)
                                self.MakeModal(False)
                                self.Hide()

                        if self.flaga-1 == 1 :
                		self.stoper.Stop()
                		EMistake.cwiczenia( self,id=-1).Show(True)
                                self.MakeModal(False)
                                self.Hide()

                        if self.flaga-1 == 2 :
                		self.stoper.Stop()
                		EGaps.cwiczenia( self,id=-1).Show(True)
                                self.MakeModal(False)
                                self.Hide()

                        if self.flaga-1 == -1 :
                		self.stoper.Stop()
                		EMatch.cwiczenia( self,id=-1).Show(True)
                                self.MakeModal(False)
                                self.Hide()


                else:
                        event.Skip( )
                        
		

if __name__ == '__main__':

	app = wx.PySimpleApp()
	frame = cwiczenia(parent = None, id = -1)
	frame.Show()
	app.MainLoop()
