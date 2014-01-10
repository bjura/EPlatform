#!/bin/env python2.7
# -*- coding: utf-8 -*-


# This file is part of AT-Platform.
#
# AT-Platform is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# AT-Platform is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with AT-Platform. If not, see <http://www.gnu.org/licenses/>.


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
from pygame import mixer


class check(wx.Frame):


	def __init__(self,parent):
                
		self.parent=parent
		self.createGui()

	def createGui(self):
                self.subSizer = wx.GridSizer( 1, 1,0,0)
                self.subSizer2 = wx.GridSizer( 1, 1,0,0)
                mixer.init()
                
                with open( './.pathToATPlatform' ,'r' ) as textFile:
			self.pathToATPlatform = textFile.readline( )
		    
		with open( self.pathToATPlatform + 'parametersCW', 'r' ) as parametersFile:
			for line in parametersFile:
                                
				if line[ :line.find('=')-1 ] == 'checkTime':
					self.checkTime = int( line[ line.rfind('=')+2:-1 ])
				elif line[ :line.find('=')-1 ] == 'colorGrat':
					self.colorGrat =  line[ line.rfind('=')+2:-1 ]
				elif line[ :line.find('=')-1 ] == 'colorNiest':
					self.colorNiest = line[ line.rfind('=')+2:-1 ]
				elif line[ :line.find('=')-1 ] == 'maxPoints':
					pass
				elif line[ :line.find('=')-1 ] == 'ileLuk':
					pass
				elif line[ :line.find('=')-1 ] == 'textSize':
					pass
				elif not line.isspace( ):
					print 'Niewłaściwie opisane parametry'
					print 'Błąd w linii', line
					self.checkTime=8000
					self.colorGrat='lime green'
					self.colorNiest='indian red'
                
                if self.parent.ownWord==self.parent.word:
                        self.parent.result+=1
                        if self.parent.result==self.parent.maxPoints:
                                text=u'Brawo! \n \nZdobyłeś wszystkie punkty. \n \nKliknij.'
                                self.parent.mouseCursor.move( self.parent.winWidth - 12, self.parent.winHeight - 20 )
                                self.parent.result=0
                                kolor='dark slate blue'
                                self.app=False
                                self.oklaski=True
                                i=wx.BitmapFromImage( wx.ImageFromStream( open(self.pathToATPlatform+'/multimedia/cwiczenia/icons/thumbup.png', "rb")))
                                be = bt.GenBitmapButton( self.parent, -1, bitmap=i)
                                be.SetBackgroundColour('white')
                                self.parent.mouseCursor.move( self.parent.winWidth - 12, self.parent.winHeight - 12 )
                                be.Bind(wx.EVT_LEFT_DOWN,self.reward)

                        else:
                                text=u'Gratulacje! \n \nWpisałeś poprawne słowo!'
                                kolor=self.colorGrat
                                self.app=True
                                self.oklaski=True
                                i=wx.BitmapFromImage( wx.ImageFromStream( open(self.pathToATPlatform+'/multimedia/cwiczenia/icons/thumbup.png', "rb")))
                                be = bt.GenBitmapButton( self.parent, -1, bitmap=i)
                                be.SetBackgroundColour('white')
                        
                else:
                        text=u'Niestety. \n \nSpróbuj jeszcze raz!'
                        kolor=self.colorNiest
			self.parent.PicNr-=1
			self.app=True
			self.oklaski=False
			i=wx.BitmapFromImage( wx.ImageFromStream( open(self.pathToATPlatform+'/multimedia/cwiczenia/icons/sad.png', "rb")))
                        be = bt.GenBitmapButton( self.parent, -1, bitmap=i)
                        be.SetBackgroundColour( 'white')
		b = bt.GenButton( self.parent, -1, text)
		b.SetFont( wx.Font(50, wx.FONTFAMILY_ROMAN, wx.FONTWEIGHT_LIGHT,  False) )
		b.SetBezelWidth( 3 )
		b.SetBackgroundColour('white' )
		b.SetForegroundColour( kolor)
		b.SetFocus()
		self.subSizer.Add( b, 0, wx.EXPAND )
		self.subSizer2.Add( be, 0, wx.EXPAND )
		self.parent.mainSizer.Add( self.subSizer, proportion=7, flag=wx.EXPAND )
		self.parent.mainSizer.Add(self.subSizer2, proportion=3, flag=wx.EXPAND )
		self.parent.SetSizer( self.parent.mainSizer )
		self.parent.Layout()
		if self.app:
                        self.parent.stoper3.Start(self.checkTime)
		if self.oklaski:
                        mixer.music.load(self.pathToATPlatform+'multimedia/cwiczenia/oklaski.ogg')
                        mixer.music.play()
                self.ileklik=0

                
                #self.parent.mainSizer.Hide(0)
                #self.parent.mainSizer.Hide(1)
                #self.dc=wx.PaintDC(self.parent)
                #self.dc.SetFont(wx.NORMAL_FONT)
                #self.dc.DrawText('brawo',10, 20)
                #self.dc.SetBrush(wx.RED_BRUSH)
                #self.dc.DrawRectangle(40, 40, 16, 16)


        def reward(self,event):
                self.parent.mainSizer.Clear(deleteWindows=True)
                self.subSizer=wx.GridSizer(1,1,0,0)
                b = bt.GenButton( self.parent, -1, u'Chcesz wyłączyć?\n \nKliknij.')
		b.SetFont( wx.Font(25, wx.FONTFAMILY_ROMAN, wx.FONTWEIGHT_LIGHT,  False) )
		b.SetBezelWidth( 3 )
		b.SetBackgroundColour('white' )
		b.Bind(wx.EVT_LEFT_DOWN,self.OnExit)
		self.subSizer.Add(b,0,wx.EXPAND)
                self.parent.mainSizer.Add(self.subSizer,proportion=1,flag=wx.EXPAND)
                self.parent.SetSizer( self.parent.mainSizer )
                self.parent.Layout()
                path=self.pathToATPlatform+'multimedia/cwiczenia/rewards/'
                song=os.listdir(path)[np.random.randint(0,len(os.listdir(path)),1)]
                mixer.music.stop()
                mixer.music.load(path+song)
                mixer.music.play()
                

        def OnExit(self,event):
                self.ileklik+=1
                if self.ileklik==1:
                        mixer.music.stop()
                        self.parent.back()
		else:
                        event.Skip()
                        
	def zamknij(self,event):
                self.parent.stoper3.Stop()
		self.parent.back()
                if self.oklaski:
                        mixer.music.stop()
