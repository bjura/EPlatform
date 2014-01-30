#!/bin/env python2.7
# -*- coding: utf-8 -*-

# This file is part of AT-Platform.
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
wxversion.select( '2.8' )

import glob, os, time
import wx, alsaaudio
import wx.lib.buttons as bt

from pymouse import PyMouse
from string import maketrans
from pygame import mixer
import subprocess as sp
import shlex

import numpy as np
from random import shuffle


#=============================================================================
class speller( wx.Frame ):
	def __init__(self, parent):

		self.parent = parent

		self.initializeParameters( )
		self.initializeBitmaps( )
		self.createGui( )

	#-------------------------------------------------------------------------
	def initializeParameters(self):

                
                self.pathToEPlatform = './'
		    
		with open( self.pathToEPlatform + 'spellerParameters', 'r' ) as parametersFile:
			for line in parametersFile:

				if line[ :line.find('=')-1 ] == 'polishLettersColour':
					self.polishLettersColour =  line[ line.rfind('=')+2:-1 ]
				elif line[ :line.find('=')-1 ] == 'voice':
					pass
				elif line[ :line.find('=')-1 ] == 'vowelColour':
                                        self.vowelColour= line[ line.rfind('=')+2:-1 ]

                                elif not line.isspace( ):
					print '\nNiewłaściwie opisany parametr. Błąd w linii:\n%s' % line

                                
                                        self.vowelColour = 'red'
                                        self.polishLettersColour = 'blue'


                with open( self.pathToEPlatform + 'parametersCW', 'r' ) as parametersFile:
			for line in parametersFile:

                                

                                if line[ :line.find('=')-1 ] == 'textSize':
					pass
				elif line[ :line.find('=')-1 ] == 'checkTime':
                                        pass
                                
				elif line[ :line.find('=')-1 ] == 'maxPoints':
					pass
				elif line[ :line.find('=')-1 ] == 'colorGrat':
                                        pass
				elif line[ :line.find('=')-1 ] == 'colorNiest':
                                        pass
                                elif line[ :line.find('=')-1 ] == 'ileLuk':
                                        pass
                                        #self.ileLuk= int(line[ line.rfind('=')+2:-1 ])
						
				elif not line.isspace( ):
					print 'Niewłaściwie opisane parametry'
					print 'Błąd w linii', line

					#self.ileLuk=2

		    
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
                

                self.labels = [ 'a e b c d f g h i o j k l m n p u y r s t w z SPECIAL_CHARACTERS DELETE TRASH CHECK ORISPEAK SPEAK EXIT'.split( ), '1 2 3 4 5 6 7 8 9 0 + - * / = % $ & . , ; : " ? ! @ # ( ) [ ] { } < > ~ DELETE TRASH CHECK ORISPEAK SPEAK EXIT'.split( ) ]
                self.colouredLabels = [ 'a','e','i','o','u','y']


                self.winWidth, self.winHeight = wx.DisplaySize( )
                self.voice=False
		self.slowo=self.parent.word
		self.ileLiter =len(self.slowo)
		#if self.ileLuk >=len(self.slowo):
                        #self.ileLuk=len(self.slowo)-1

                self.numberOfRows =  [4, 5 ]
                self.numberOfColumns = [ 8, 9 ]
				
                #self.flag = 'row'						
                #self.rowIteration = 0						
                #self.columnIteration = 0							
                #self.countRows = 0
                #self.countColumns = 0
                self.kolejnyKrok=0

                #self.maxNumberOfColumns = 2									
	    
                self.numberOfPresses = 1
                self.subSizerNumber = 0

                self.mouseCursor = PyMouse( )

                
                mixer.init( )
                self.typewriterKeySound = mixer.Sound( self.pathToEPlatform+'sounds/typewriter_key.wav' )
                self.typewriterForwardSound = mixer.Sound( self.pathToEPlatform+'sounds/typewriter_forward.wav' )
                self.typewriterSpaceSound = mixer.Sound( self.pathToEPlatform+'sounds/typewriter_space.wav' )

                
                self.phones = glob.glob( self.pathToEPlatform+'sounds/phone/*' )
                self.phoneLabels = [ item[ item.rfind( '/' )+1 : item.rfind( '_' ) ] for item in self.phones ]
                self.sounds = [ mixer.Sound( self.sound ) for self.sound in self.phones ]
	    
                self.parent.SetBackgroundColour( 'dark grey' )
		
	#-------------------------------------------------------------------------
        def initializeBitmaps(self):

        
            self.path=self.pathToEPlatform+'multimedia/'
            labelFiles = [ file for file in [ self.path+'icons/speller/special_characters.png', self.path+'icons/speller/DELETE.png', self.path+'icons/speller/TRASH.png',   self.path+'icons/speller/CHECK.png',self.path+'icons/speller/ORISPEAK.png', self.path+'icons/speller/SPEAK.png', self.path+'icons/speller/exit.png', ] ]
            
            self.labelBitmaps = { }
	    
	    labelBitmapIndex = [ self.labels[ 0 ].index( self.labels[ 0 ][ -7 ] ), self.labels[ 0 ].index( self.labels[ 0 ][ -6 ] ), self.labels[ 0 ].index( self.labels[ 0 ][ -5 ] ), self.labels[ 0 ].index( self.labels[ 0 ][ -4 ] ), self.labels[ 0 ].index( self.labels[ 0 ][ -3 ] ),self.labels[ 0 ].index( self.labels[ 0 ][ -2 ] ), self.labels[ 0 ].index( self.labels[ 0 ][ -1 ] ) ]

            for labelFilesIndex, labelIndex in enumerate( labelBitmapIndex ):
		    self.labelBitmaps[ self.labels[ 0 ][ labelIndex ] ] = wx.BitmapFromImage( wx.ImageFromStream( open( labelFiles[ labelFilesIndex ], 'rb' )) )      

            self.labelBitmaps2 = { }
	    
	    labelBitmapIndex2 = [ self.labels[ 1 ].index( self.labels[ 1 ][ -6 ] ), self.labels[ 1 ].index( self.labels[ 1 ][ -5 ] ), self.labels[ 1 ].index( self.labels[ 1 ][ -4 ] ), self.labels[ 1 ].index( self.labels[ 1 ][ -3 ] ),self.labels[ 1 ].index( self.labels[ 1 ][ -2 ] ), self.labels[ 1 ].index( self.labels[ 1 ][ -1 ] ) ]

            for labelFilesIndex2, labelIndex2 in enumerate( labelBitmapIndex2 ):
		    self.labelBitmaps2[ self.labels[ 1 ][ labelIndex2 ] ] = wx.BitmapFromImage( wx.ImageFromStream( open( labelFiles[ 1: ][ labelFilesIndex2 ], 'rb' )) )

	#-------------------------------------------------------------------------	
	def createGui(self):
		

		self.textField = wx.TextCtrl( self.parent, style = wx.TE_LEFT|wx.TE_RICH2, size = ( self.winWidth, 0.2 * self.winHeight ) )
		self.textField.SetFont( wx.Font( 60, wx.SWISS, wx.NORMAL, wx.NORMAL ) )
		self.parent.mainSizer.Add( self.textField, flag = wx.EXPAND | wx.TOP | wx.BOTTOM, border = 3 )
		
		self.subSizers = [ ]
		
		subSizer = wx.GridBagSizer( 3, 3 )


                self.pomieszane=[]

                for i in self.slowo:
                        self.pomieszane.append(self.labels[0].index(i))

                shuffle(self.pomieszane)
                #print self.pomieszane
                
                for litera in self.pomieszane:
                        if self.pomieszane.count(litera) > 1:
                                self.pomieszane.remove(litera)
                                zakres=(self.numberOfRows[0]-1)* self.numberOfColumns[0] -1
                                print zakres
                                dodaj=np.random.randint(0,zakres,1)[0]
                                while dodaj in self.pomieszane:
                                        dodaj=np.random.randint(0,zakres,1)[0]
                                self.pomieszane.append(dodaj)
                                
                slowoList=list(self.slowo)
                shuffle(slowoList)
                zmieszane_slowo= ''.join(slowoList)
                #print zmieszane_slowo

                for i in self.pomieszane:
                        self.labels[0][i]=zmieszane_slowo[-1]
                        zmieszane_slowo=zmieszane_slowo[:-1]
                        
                self.pomieszane.sort()
		
                ile=0
		for index_1, item in enumerate( self.labels[ 0 ][ :-7 ] ):
                        ile+=1

                        b = bt.GenButton( self.parent, -1, item  , name = item+str(ile), size = ( 0.985*self.winWidth / self.numberOfColumns[ 0 ], 0.79 * self.winHeight / self.numberOfRows[ 0 ] ) )
			b.SetFont( wx.Font( 40, wx.FONTFAMILY_ROMAN, wx.FONTWEIGHT_LIGHT,  False ) )
			b.SetBezelWidth( 3 )


			if index_1 not in self.pomieszane:
                                b.SetBackgroundColour( 'grey' )

                        else:
                                
                                b.SetBackgroundColour( self.backgroundColour )

			if item in self.colouredLabels and self.vowelColour != 'False':
                                if index_1 not in self.pomieszane:
                                        b.SetForegroundColour( 'grey' )
                                else:
                                        b.SetForegroundColour( self.vowelColour )
			else:
                                if index_1 not in self.pomieszane:
                                        b.SetForegroundColour( 'grey' )
                                else:
                                        b.SetForegroundColour( self.textColour )

			b.Bind( wx.EVT_LEFT_DOWN, self.onPress )
			subSizer.Add( b, ( index_1 / self.numberOfColumns[ 0 ], index_1 % self.numberOfColumns[ 0 ] ), wx.DefaultSpan, wx.EXPAND )

		for index_2, item in enumerate( self.labels[ 0 ][ -7 : ] ):
                        if item == 'SPECIAL_CHARACTERS':
                                b = bt.GenButton( self.parent, -1, item, name = item, size = ( 0.985*self.winWidth / self.numberOfColumns[ 0 ], 0.79 * self.winHeight / self.numberOfRows[ 0 ] ) )
                                b.SetFont( wx.Font( 40, wx.FONTFAMILY_ROMAN, wx.FONTWEIGHT_LIGHT,  False ) )
                                b.SetForegroundColour( 'grey' )
                                b.SetBackgroundColour( 'grey' )
			else:
                                b = bt.GenBitmapButton( self.parent, -1, bitmap = self.labelBitmaps[ item ] )
                                b.SetBackgroundColour( self.backgroundColour )
			b.SetBezelWidth( 3 )
                        b.Bind( wx.EVT_LEFT_DOWN, self.onPress )
                        if index_2==3:
                                subSizer.Add( b, ( ( index_1 + index_2 +1) / self.numberOfColumns[ 0 ], ( index_1 + index_2+1 ) % self.numberOfColumns[ 0 ] ), (1,3), wx.EXPAND )
                        elif index_2>3:
                                subSizer.Add( b, ( ( index_1 + index_2 +3) / self.numberOfColumns[ 0 ], ( index_1 + index_2 +3) % self.numberOfColumns[ 0 ] ), wx.DefaultSpan, wx.EXPAND )
                        else:
                                subSizer.Add( b, ( ( index_1 + index_2+1 ) / self.numberOfColumns[ 0 ], ( index_1 + index_2 +1) % self.numberOfColumns[ 0 ] ), wx.DefaultSpan, wx.EXPAND )
                        
		self.subSizers.append( subSizer )		    
		self.parent.mainSizer.Add( self.subSizers[ 0 ], proportion = 1, flag = wx.EXPAND )
		self.parent.SetSizer( self.parent.mainSizer )
		
		subSizer2 = wx.GridBagSizer( 3, 3 )

		for index_1, item in enumerate( self.labels[ 1 ][ :-6 ] ):
			b = bt.GenButton( self.parent, -1, item, name = item, size = ( 0.985*self.winWidth / self.numberOfColumns[ 1 ], 0.75 * self.winHeight / self.numberOfRows[ 1 ] ) )
			b.SetFont( wx.Font( 40, wx.FONTFAMILY_ROMAN, wx.FONTWEIGHT_LIGHT,  False ) )
			b.SetBezelWidth( 3 )
			b.SetBackgroundColour( self.backgroundColour )
			b.SetForegroundColour( self.textColour )
			b.Bind( wx.EVT_LEFT_DOWN, self.onPress )
			subSizer2.Add( b, ( index_1 / self.numberOfColumns[ 1 ], index_1 % self.numberOfColumns[ 1 ] ), wx.DefaultSpan, wx.EXPAND )

		for index_2, item in enumerate( self.labels[ 1 ][ -6 :  ] ):
			b = bt.GenBitmapButton( self.parent, -1, bitmap = self.labelBitmaps2[ item ] )
			b.SetBackgroundColour( self.backgroundColour )
			b.SetBezelWidth( 3 )
                        b.Bind( wx.EVT_LEFT_DOWN, self.onPress )
			if index_2==2:
                                subSizer2.Add( b, ( ( index_1 + index_2 +1) / self.numberOfColumns[ 1 ], ( index_1 + index_2 +1) % self.numberOfColumns[ 1 ] ), (1,4), wx.EXPAND )
                        elif index_2>2:
                                subSizer2.Add( b, ( ( index_1 + index_2 +4) / self.numberOfColumns[ 1], ( index_1 + index_2+4 ) % self.numberOfColumns[ 1 ] ), wx.DefaultSpan, wx.EXPAND )
                        else:
                                subSizer2.Add( b, ( ( index_1 + index_2+1 ) / self.numberOfColumns[ 1 ], ( index_1 + index_2 +1) % self.numberOfColumns[ 1 ] ), wx.DefaultSpan, wx.EXPAND )
                        

		self.subSizers.append( subSizer2 )		   
		self.parent.mainSizer.Add( self.subSizers[ 1 ], proportion = 1, flag = wx.EXPAND )
		self.parent.mainSizer.Show( item = self.subSizers[ 1 ], show = False, recursive = True )
		self.parent.SetSizer( self.parent.mainSizer )



                ikony=range(self.numberOfColumns[0]*self.numberOfRows[0]-8,self.numberOfColumns[0]*self.numberOfRows[0]-2)



                self.ktore=self.pomieszane

		for i in ikony:
                        self.ktore.append(i)

		self.parent.Layout()

		self.usuniete=[]

	
	def onExit(self):
                self.parent.PicNr-=1
		self.parent.stoper2.Stop( )
		self.parent.back()
		

        def czytajLitere(self,litera):
                time.sleep(1)
                soundIndex = self.phoneLabels.index( [ item for item in self.phoneLabels if litera.swapcase() in item ][ 0 ] )
		sound = self.sounds[ soundIndex ]
		sound.play( )
                self.parent.SetFocus()


	#----------------------------------------------------------------------------
	def onPress(self, event):

		self.numberOfPresses += 1
		
		if self.numberOfPresses == 1:

                        label = self.labels[ 0 ][self.ktore[self.kolejnyKrok-1]] 

			item = self.subSizers[ 0 ].GetChildren()
                        b = item[self.ktore[self.kolejnyKrok-1]]
                        b=b.GetWindow( )
			
			if label != 'SPEAK':
                                b.SetBackgroundColour( self.selectionColour )
                        else:
                                pass
			b.SetFocus( )
			b.Update( )
				
		

                        if label in self.slowo:
                                self.typewriterKeySound.play()
                                self.textField.WriteText(label)
                                item = self.subSizers[ 0 ].GetChildren()
                                b = item[self.ktore[self.kolejnyKrok-1]]
                                b=b.GetWindow( )
                                b.SetBackgroundColour( 'grey' )
                                b.SetForegroundColour('grey')
                                b.SetFocus( )
                                b.Update( )
                                self.usuniete.append(self.ktore[self.kolejnyKrok-1])
                                self.ktore.remove( self.ktore[self.kolejnyKrok-1] )
                                self.kolejnyKrok=0
				
                        elif label == 'DELETE':
                                text=self.textField.GetValue()
                                if text:
                                        self.typewriterForwardSound.play( )
                                        item = self.subSizers[ 0 ].GetChildren()
                                        b = item[self.usuniete[-1]]
                                        b=b.GetWindow( )
                                        b.SetBackgroundColour( self.backgroundColour)
                                        
                                        if self.labels[0][self.usuniete[-1]] in self.colouredLabels:
                                                b.SetForegroundColour( self.vowelColour )
                                        else:
                                                b.SetForegroundColour( self.textColour )
                                        
                                        b.SetFocus( )
                                        b.Update( )
                                        self.ktore.append(self.usuniete[-1])
                                        self.ktore.sort()
                                        self.usuniete.remove( self.usuniete[-1] )
                                        self.textField.Remove(self.textField.GetInsertionPoint()-1, self.textField.GetInsertionPoint())
                                        self.kolejnyKrok=0
                                else:
                                        pass
				
			elif label == 'SPEAK':
                                if not self.voice:
                                        self.voice=True
                                        b.SetBackgroundColour('indian red')
                                        b.SetFocus( )
                                        b.Update()
                                else:
                                        b.SetBackgroundColour(self.backgroundColour)
                                        b.SetFocus( )
                                        b.Update()
                                        self.voice=False
				
			elif label == 'ORISPEAK':
                                self.parent.stoper2.Stop()
                                if str(self.parent.word)+'.ogg' not in os.listdir(self.pathToEPlatform+'multimedia/spelling/'):
                                        command='sox -m '+self.pathToEPlatform+'sounds/phone/'+list(self.parent.word)[0].swapcase()+'.wav'
                                        ile=0
                                        for l in list(self.parent.word)[1:]:
                                                ile+=2
                                                command+=' "|sox '+self.pathToEPlatform+'sounds/phone/'+l.swapcase()+'.wav'+' -p pad '+str(ile)+'"'
                                        command+=' '+self.pathToEPlatform+'multimedia/spelling/'+self.parent.word+'.ogg'
                                        wykonaj=sp.Popen(shlex.split(command))
                                time.sleep(1.5)
                                do_literowania=mixer.Sound(self.pathToEPlatform+'multimedia/spelling/'+self.parent.word+'.ogg')
                                do_literowania.play()
                                self.parent.stoper4.Start((do_literowania.get_length()+0.5 )* 1000)

				
			elif label == 'TRASH':
                                text=self.textField.GetValue()
                                if text:
                                        self.typewriterForwardSound.play()
                                        self.textField.Remove(0,self.textField.GetInsertionPoint())
                                        for litera in self.usuniete:
                                                item = self.subSizers[ 0 ].GetChildren()
                                                b = item[litera]
                                                b=b.GetWindow( )
                                                b.SetBackgroundColour( self.backgroundColour)

                                                if self.labels[0][litera] in self.colouredLabels:
                                                        b.SetForegroundColour( self.vowelColour )
                                                else:
                                                        b.SetForegroundColour( self.textColour )
                                                #print self.usuniete,self.ktore
                                
                                                b.SetFocus( )
                                                b.Update( )
                                        while self.usuniete:
                                                self.ktore.append(self.usuniete[-1])
                                                self.ktore.sort()
                                                self.usuniete.remove(self.usuniete[-1] )
                                        self.kolejnyKrok=0

                                                
                                else:
                                        pass

	 		elif label == 'EXIT':
                                self.onExit( )
                                                

			elif label =='CHECK':
				self.parent.stoper2.Stop()
                                self.parent.ownWord=self.textField.GetValue()
                                self.parent.check()
                        else:
                                pass


		else:
			event.Skip( )		
	
	#-------------------------------------------------------------------------
	def timerUpdate(self, event):

		self.mouseCursor.move( self.winWidth - 12, self.winHeight - 20 )
		
		self.numberOfPresses = 0		


                for i in self.ktore:
                        if self.voice and i == self.numberOfRows[0]*self.numberOfColumns[0]-4:
                                items = self.subSizers[ 0 ].GetChildren()
                                b = items[i]
                                b=b.GetWindow( )
                                b.SetBackgroundColour( 'indian red')
                                b.SetFocus( )
                                b.Update( )
                        else:
                                items = self.subSizers[ 0 ].GetChildren()
                                b = items[i]
                                b=b.GetWindow( )
                                b.SetBackgroundColour( self.backgroundColour )
                                b.SetFocus( )
                                b.Update( )

                if self.voice and self.ktore[self.kolejnyKrok] == self.numberOfRows[0]*self.numberOfColumns[0]-4:
                        item = self.subSizers[ 0 ].GetChildren()
                        b = item[self.ktore[self.kolejnyKrok]]
                        b=b.GetWindow( )
                        b.SetBackgroundColour( 'orange red')
                        b.SetFocus( )
                        b.Update( )
                else:
                        item = self.subSizers[ 0 ].GetChildren()
                        b = item[self.ktore[self.kolejnyKrok]]
                        b=b.GetWindow( )
                        b.SetBackgroundColour( self.scanningColour)
                        b.SetFocus( )
                        b.Update( )

                if self.voice and self.labels[0][self.ktore[self.kolejnyKrok]] in self.slowo:
                        self.parent.stoper2.Stop()
                        label = self.labels[ 0 ][self.ktore[self.kolejnyKrok]]
                        self.czytajLitere(label)
                        self.parent.stoper2.Start(self.timeGap)




                if self.kolejnyKrok == len(self.ktore)-1:
                        self.kolejnyKrok=0
                else:
                        self.kolejnyKrok+=1
	
