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

import check



#"nazwij obrazek"



class cwiczenia(wx.Frame):
	def __init__(self, parent, id):
		
		wx.Frame.__init__( self , parent , id , 'EMatch')
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

					self.textSize=80
					sel.maxPoints=2

		
		self.flaga=0
		self.PicNr=0
		self.result=0
		self.mouseCursor = PyMouse( )
		self.WordsList=os.listdir(self.pathToEPlatform+'multimedia/pictures')
		shuffle(self.WordsList)
                self.poczatek=True
		self.numberOfPresses = 1
		self.czyBack=False
		mixer.init()
		self.numberOfExtraWords= 4
		#self.ktorySizer='wyrazy'
		

	def initializeTimer(self):

                id1=wx.NewId()
                wx.RegisterId(id1)
		self.stoper = wx.Timer(self,id1)
		self.Bind( wx.EVT_TIMER, self.timerUpdate, self.stoper,id1 )
		
		#self.id2=wx.NewId()
                #wx.RegisterId(self.id2)
                #self.stoper2 = wx.Timer( self ,self.id2)

                self.id3=wx.NewId()
                wx.RegisterId(self.id3)
                self.stoper3 = wx.Timer( self ,self.id3)

                self.id4=wx.NewId()
                wx.RegisterId(self.id4)
                self.stoper4=wx.Timer(self,self.id4)
                self.Bind(wx.EVT_TIMER, self.pomocniczyStoper, self.stoper4,self.id4 )
                
		self.stoper.Start( self.timeGap )

	def timerUpdate(self,event):

                self.mouseCursor.move( self.winWidth - 12, self.winHeight - 12 )

                self.numberOfPresses = 0

                #print self.flaga, len(self.wordSizer)
		for i in range(5):
			item = self.subSizer.GetChildren()
			b=item[i].GetWindow()
                        b.SetBackgroundColour( self.backgroundColour )
                        b.SetFocus()
                for i in range(self.numberOfExtraWords+1):
                        item = self.wordSizer.GetChildren()
			b=item[i].GetWindow()
                        b.SetBackgroundColour( self.backgroundColour )
                        b.SetFocus()

				
                if self.flaga >= self.numberOfExtraWords+1:
                        if self.poczatek:
                                time.sleep(1)
                                self.stoper.Stop()
                                mixer.music.load(self.pathToEPlatform+'multimedia/voices/'+str(self.word)+'.ogg')
                                mixer.music.play()
                                time.sleep(2)
                                self.stoper.Start(self.timeGap)
                                self.poczatek=False
                        item = self.subSizer.GetChildren()
                        b=item[self.flaga-self.numberOfExtraWords -1].GetWindow()
                        b.SetBackgroundColour( self.scanningColour )
                        b.SetFocus()
                else:
                        if self.poczatek:
                                time.sleep(1)
                                self.stoper.Stop()
                                mixer.music.load(self.pathToEPlatform+'multimedia/voices/'+str(self.word)+'.ogg')
                                mixer.music.play()
                                time.sleep(2)
                                self.stoper.Start(self.timeGap)
                                self.poczatek=False
                        item = self.wordSizer.GetChildren()
                        b = item[self.flaga].GetWindow()
                        b.SetBackgroundColour( self.scanningColour )
                        b.SetFocus()
                print self.flaga


                #if self.ktorySizer=='opcje' and self.flaga==1:
                #        self.ktorySizer='wyrazy'
                #if self.ktorySizer=='wyrazy' and self.flaga==1:
                #        self.ktorySizer='opcje'

                        
                if self.flaga== 4 +self.numberOfExtraWords+1:
                        self.flaga=0
                else:
                        self.flaga+=1

			
	
	def createGui(self):

                if self.PicNr ==len(self.WordsList):
                        self.PicNr=0
		self.picture=self.WordsList[self.PicNr]
                self.PicNr+=1
		self.path=self.pathToEPlatform+'multimedia/pictures/'
                im=wx.ImageFromStream( open(self.path+self.picture, "rb"))
		x=im.GetWidth()
		y=im.GetHeight()
		if x >y:
                        im=im.Scale(600,500)
                elif x==y:
                        im=im.Scale(600,600)
                else:
                        im=im.Scale(500,600)
		picture=wx.BitmapFromImage(im)
		self.word=self.picture[:self.picture.index('.')]
		
		self.extraWords=[] #wybiera dodatkowe slowa
		while len(self.extraWords)<self.numberOfExtraWords:
                        slowo=self.WordsList[np.random.randint(0,len(self.WordsList),1)[0]]
                        slowo=slowo[:slowo.index('.')]
                        if slowo not in self.extraWords and slowo!= self.word:
                                self.extraWords.append(slowo)
                                
		b = bt.GenBitmapButton( self, -1, bitmap=picture,name='picture') #zdjecie
		b.SetBackgroundColour( self.backgroundColour)
		b.Bind( wx.EVT_LEFT_DOWN, self.onPress )

                obiekty_wyrazow=[] #wyrazy
                self.wyrazy_w_kolejnosci=[]
                gdzie_poprawne=np.random.randint(0,self.numberOfExtraWords,1)[0]
                for i,j in enumerate(self.extraWords):
                        be = bt.GenButton( self, -1, j)
                        be.SetFont( wx.Font(50, wx.FONTFAMILY_ROMAN, wx.FONTWEIGHT_LIGHT,  False) )
                        be.SetBackgroundColour( self.backgroundColour)
                        be.Bind( wx.EVT_LEFT_DOWN, self.onPress )
                        obiekty_wyrazow.append(be)
                        self.wyrazy_w_kolejnosci.append(j)
                        

                be = bt.GenButton( self, -1, self.word)
                be.SetFont( wx.Font(50, wx.FONTFAMILY_ROMAN, wx.FONTWEIGHT_LIGHT,  False) )
                be.SetBackgroundColour( self.backgroundColour)
                be.Bind( wx.EVT_LEFT_DOWN, self.onPress )
                obiekty_wyrazow.insert(gdzie_poprawne,be)
                self.wyrazy_w_kolejnosci.insert(gdzie_poprawne,self.word)
                

                #punkty
                res = bt.GenButton( self, -1, u'twój wynik:   '+str(self.result)+' / '+str(self.maxPoints))
		res.SetFont( wx.Font(27, wx.FONTFAMILY_ROMAN, wx.FONTWEIGHT_LIGHT,  False) )
		res.SetBackgroundColour( self.backgroundColour)
		res.Bind( wx.EVT_LEFT_DOWN, self.onPress )
		

                self.wordSizer=wx.BoxSizer( wx.VERTICAL )
                for i in obiekty_wyrazow:
                        self.wordSizer.Add( i, proportion=1, flag=wx.EXPAND )
		
		try:
                        self.subSizerP.Hide(0)
                        self.subSizerP.Remove(0)
                        self.subSizerP.Add( res, 0,wx.EXPAND) #dodanie wyniku
                        self.subSizer0.Hide(0)
                        self.subSizer0.Remove(0)
                        self.subSizer0.Hide(0)
                        self.subSizer0.Remove(0)
                        self.subSizer0.Add( b, 0,wx.EXPAND) #dodanie zdjecia
		        self.subSizer0.Add( self.wordSizer, 0,wx.EXPAND ) #tutaj trzeba dodac caly zagniezdzony subsizer ze slowami
                except AttributeError:
                        if self.czyBack:
                                self.SetBackgroundColour((220, 220, 220, 255))
                                self.czyBack=False
                        else:
                                self. mainSizer = wx.BoxSizer( wx.VERTICAL )
                        self.subSizerP=wx.GridSizer(1,1,3,3)
                        self.subSizer0 = wx.GridSizer(1,2,3,3)
                        self.subSizer=wx.GridSizer(1,5,3,3)
                        self.subSizerP.Add(res,0,wx.EXPAND)
                        self.subSizer0.Add( b, 0,wx.EXPAND )
		        self.subSizer0.Add( self.wordSizer, 0,wx.EXPAND )
                        self.icons=sorted(os.listdir(self.pathToEPlatform+'multimedia/icons'))
                        self.path=self.pathToEPlatform+'multimedia/icons/'
                        for idx,icon in enumerate(self.icons):
                                if icon[0].isdigit():
                                        i=wx.BitmapFromImage( wx.ImageFromStream( open(self.path+icon, "rb")))
                                        b = bt.GenBitmapButton( self, -1, bitmap=i)
                                        b.SetBackgroundColour( self.backgroundColour)
                                        b.Bind( wx.EVT_LEFT_DOWN, self.onPress )
                                        self.subSizer.Add( b, 0,wx.EXPAND )
                        self. mainSizer.Add( self.subSizerP, proportion=1, flag=wx.EXPAND )
                        self. mainSizer.Add( self.subSizer0, proportion=7, flag=wx.EXPAND )
                        self. mainSizer.Add( self.subSizer, proportion=2, flag=wx.EXPAND )
                        self.SetSizer( self. mainSizer,deleteOld=True )
		self.Layout()
		self.Refresh()
		self.Center()
		self.MakeModal(True)
		self.flaga=0
		self.poczatek=True



	def OnExit(self,event):
                if self.parent:
                        self.parent.MakeModal(True)
                        self.parent.Show()
                        self.parent.stoper.Start(self.parent.timeGap)
                else:
                        pass
                self.MakeModal(False)
                self.Destroy()


	def onPress(self,event):


                self.numberOfPresses += 1
		
		if self.numberOfPresses == 1:


                        if self.flaga==0 :
                                items = self.subSizer.GetChildren()
                                item=items[ 4]

                        else:
                                if self.flaga >= self.numberOfExtraWords+2:
                                        items = self.subSizer.GetChildren()
                                        item=items[  self.flaga-self.numberOfExtraWords -2]
                                else:
                                        items = self.wordSizer.GetChildren()
                                        item=items[ self.flaga -1 ]
                        
                        b = item.GetWindow()
                        b.SetBackgroundColour( self.selectionColour )
                        b.SetFocus()
                        b.Update()
                
                	if 'speller' in self.icons[self.flaga-self.numberOfExtraWords -2] and self.flaga>=self.numberOfExtraWords+2:
                                pass
                		#self.stoper.Stop()
                		#self.mainSizer.Clear(deleteWindows=True)
                		#self.spellerW = spellerMistake.speller( self)
                		#self.Bind( wx.EVT_TIMER, self.spellerW.timerUpdate, self.stoper2,self.id2 )
                                #self.stoper2.Start( self.spellerW.timeGap )
                                
                	elif self.flaga == 0: #cancel     or self.flaga==0:
                		if __name__ == '__main__':
                                        self.stoper.Stop( )
                                        self.Destroy( )
                                else:
                                        self.stoper.Stop( )
                                        self.MakeModal( False )
                                        self.parent.Show( True )
                                        self.parent.stoper.Start( self.parent.timeGap )
                                        self.Destroy( )
                        elif 'speak' in self.icons[self.flaga-self.numberOfExtraWords -2] and self.flaga>=self.numberOfExtraWords+2:
                        	time.sleep(1)
                        	self.stoper.Stop()
                        	mixer.music.load(self.pathToEPlatform+'multimedia/voices/'+str(self.word)+'.ogg')
                                mixer.music.play()
                                self.stoper4.Start(2000)

                        elif 'literuj' in  self.icons[self.flaga-self.numberOfExtraWords -2]and self.flaga>=self.numberOfExtraWords+2 :
                                self.stoper.Stop()
                                if str(self.word)+'.ogg' not in os.listdir(self.pathToEPlatform+'multimedia/spelling/'):        
                                        command='sox -m '+self.pathToEPlatform+'sounds/phone/'+list(self.word)[0].swapcase()+'.wav'
                                        ile=0
                                        for l in list(self.word)[1:]:
                                                ile+=2
                                                command+=' "|sox '+self.pathToEPlatform+'sounds/phone/'+l.swapcase()+'.wav'+' -p pad '+str(ile)+'"'
                                        command+=' '+self.pathToEPlatform+'multimedia/spelling/'+self.word+'.ogg'
                                        wykonaj=sp.Popen(shlex.split(command))
                                time.sleep(1.5)
                                do_literowania=mixer.Sound(self.pathToEPlatform+'multimedia/spelling/'+self.word+'.ogg')
                                do_literowania.play()
                                self.stoper4.Start((do_literowania.get_length()+0.5 )* 1000)
                                
		
                        elif 'undo' in self.icons[self.flaga-self.numberOfExtraWords -2]and self.flaga>=self.numberOfExtraWords+2 :
			
                        	self.stoper.Stop()
                        	self.createGui()			
                        	self.stoper.Start(self.timeGap)

                        else:
                                if self.wyrazy_w_kolejnosci[self.flaga-1] ==self.word:
                                        self.ownWord=self.word

                                else:
                                        self.ownWord=''
                                #self.MakeModal(False)
                                #self.Hide()
                                self.stoper.Stop()
                                self.check()

                else:
                        event.Skip( )

        def pomocniczyStoper(self,event):
                self.stoper4.Stop()
                self.stoper.Start( self.timeGap )
        

	def check(self):
                self.mainSizer.Clear(deleteWindows=True)
		self.checkW=check.check( self )
		self.Bind( wx.EVT_TIMER, self.checkW.zamknij, self.stoper3,self.id3 )

	def back(self):
                self.czyBack=True
                del self.checkW
                self.mainSizer.Clear(deleteWindows=True)
		self.createGui()
		self.stoper.Start(self.timeGap)
		

if __name__ == '__main__':

	app = wx.PySimpleApp()
	frame = cwiczenia(parent = None, id = -1)
	frame.Show()
	app.MainLoop()
