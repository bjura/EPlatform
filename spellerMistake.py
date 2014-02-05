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
                                        self.ileLuk= int(line[ line.rfind('=')+2:-1 ])
						
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
                

                self.labels = [ 'a e b c d f g h i o j k l m n p u y r s t w z SPECIAL_CHARACTERS DELETE TRASH CHECK ORISPEAK SPEAK EXIT'.split( ), '. . . . . . . . . 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 DELETE TRASH CHECK ORISPEAK SPEAK EXIT'.split( ) ]
                self.colouredLabels = [ 'a','e','i','o','u','y']


                self.winWidth, self.winHeight = wx.DisplaySize( )
                self.voice=False
		self.slowo=self.parent.word

                self.numberOfRows = [ 4, 4 ]
                self.numberOfColumns = [ 8, 9 ]
				
                self.flag = 'row'						
                self.rowIteration = 0						
                self.columnIteration = 0							
                self.countRows = 0
                self.countColumns = 0										

                self.maxNumberOfColumns = 2									
	    
                self.numberOfPresses = 1
                self.subSizerNumber = 1

                self.mouseCursor = PyMouse( )

                self.krokCyfry=0

                
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
            labelFiles = [ file for file in [ self.path+'icons/speller/special_characters.png', self.path+'icons/speller/WSTECZ.png', self.path+'icons/speller/TRASH.png',   self.path+'icons/speller/CHECK.png',self.path+'icons/speller/ORISPEAK.png', self.path+'icons/speller/SPEAK.png', self.path+'icons/speller/exit.png', ] ]
            
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


                
                self.slowoZBledem=''  #slowo z jedna bledna litera
                ktora_zmienic=np.random.randint(0,len(self.slowo),1)[0]
                for i,j in enumerate(self.slowo):
                        if i == ktora_zmienic:
                                litera=self.labels[0][np.random.randint(0,(self.numberOfRows[0]-1)* self.numberOfColumns[0]-1 ,1)[0]]
                                while litera==j:
                                        litera=self.labels[0][np.random.randint(0,(self.numberOfRows[0]-1)* self.numberOfColumns[0]-1 ,1)[0]]
                                self.slowoZBledem+=litera
                        else:
                                self.slowoZBledem+=j
                                
                self.textField.WriteText(self.slowoZBledem)
                self.ktora_bledna=ktora_zmienic  #numer litery ktora jest bledna
                self.ileNumerow=len(self.slowo)   #ile liter ma dane slowo
                

                self.ktore=range(9,len(self.slowo)+9)   #ktore indeksy itemow iterowac w cyfrach, plus 9 bo pierwszy rzad pusty
                for i in range(self.numberOfRows[1]* self.numberOfColumns[1] -9  , self.numberOfRows[1]* self.numberOfColumns[1] -3  ):
                        self.ktore.append(i)
		
		self.subSizers = [ ]
		
		subSizer = wx.GridBagSizer( 3, 3 )

		for index_1, item in enumerate( self.labels[ 0 ][ :-7 ] ):
			b = bt.GenButton( self.parent, -1, item, name = item, size = ( 0.985*self.winWidth / self.numberOfColumns[ 0 ], 0.79 * self.winHeight / self.numberOfRows[ 0 ] ) )
			b.SetFont( wx.Font( 60, wx.FONTFAMILY_ROMAN, wx.FONTWEIGHT_LIGHT,  False ) )
			b.SetBezelWidth( 3 )
			b.SetBackgroundColour( self.backgroundColour )

			if item in self.colouredLabels and self.vowelColour != 'False':
				b.SetForegroundColour( self.vowelColour )
			else:
				b.SetForegroundColour( self.textColour )

			b.Bind( wx.EVT_LEFT_DOWN, self.onPress )
			subSizer.Add( b, ( index_1 / self.numberOfColumns[ 0 ], index_1 % self.numberOfColumns[ 0 ] ), wx.DefaultSpan, wx.EXPAND )

		for index_2, item in enumerate( self.labels[ 0 ][ -7 : ] ):
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

                #wyjscie z tego subsizera tez wychodzi

		for index_1, item in enumerate( self.labels[ 1 ][ :-6 ] ):
                                
			b = bt.GenButton( self.parent, -1, item, name = item, size = ( 0.985*self.winWidth / self.numberOfColumns[ 1 ], 0.79 * self.winHeight / self.numberOfRows[ 1 ] ) )
			b.SetFont( wx.Font( 55, wx.FONTFAMILY_ROMAN, wx.FONTWEIGHT_LIGHT,  False ) )
			b.SetBezelWidth( 3 )
			if index_1 in self.ktore:
                                b.SetForegroundColour( self.textColour )
                                b.SetBackgroundColour( self.backgroundColour )
                        else:
                                b.SetBackgroundColour( 'grey' )
                                b.SetForegroundColour( 'grey') #???????????
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
		self.parent.mainSizer.Show( item = self.subSizers[ 1 ], show = True , recursive = True )
		self.parent.mainSizer.Show( item = self.subSizers[ 0 ], show = False, recursive = True )
		self.parent.SetSizer( self.parent.mainSizer )
		

		self.parent.Layout()

	
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
		
		if self.numberOfPresses == 1 and self.subSizerNumber==0:

			if self.flag == 'rest':
				self.flag = 'row'
				self.rowIteration = 0

			elif self.flag == 'row':
				
				if self.rowIteration != self.numberOfRows[ self.subSizerNumber ]:
					buttonsToHighlight = range( ( self.rowIteration - 1 ) * self.numberOfColumns[ self.subSizerNumber ], ( self.rowIteration - 1 ) * self.numberOfColumns[ self.subSizerNumber ] + self.numberOfColumns[ self.subSizerNumber ] )
				else:
					buttonsToHighlight = range( ( self.rowIteration - 1 ) * self.numberOfColumns[ self.subSizerNumber ], ( self.rowIteration - 1 ) * self.numberOfColumns[ self.subSizerNumber ] + 6 )
			
				for i,button in enumerate(buttonsToHighlight):
                                        if self.rowIteration-1 ==self.numberOfRows[self.subSizerNumber]-1 and i==len(buttonsToHighlight)-2 and self.voice:
                                                pass
                                        else:
                                                item = self.subSizers[ self.subSizerNumber ].GetItem( button )
                                                b = item.GetWindow( )
                                                b.SetBackgroundColour( self.selectionColour )
                                                b.SetFocus( )
                                                b.Update( )

				self.flag = 'columns' 
				self.rowIteration -= 1
				self.columnIteration = 0
			
			elif self.flag == 'columns' and self.rowIteration != self.numberOfRows[ self.subSizerNumber ] - 1:

				item = self.subSizers[ self.subSizerNumber ].GetItem( ( self.rowIteration ) * self.numberOfColumns[ self.subSizerNumber ] + self.columnIteration - 1 )
				b = item.GetWindow( )
				b.SetBackgroundColour( self.selectionColour )
				b.SetFocus( )
				b.Update( )

				label = self.labels[ self.subSizerNumber ][ self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + self.columnIteration - 1 ]
				
				if label == 'SPECIAL_CHARACTERS':								
					pass

				else:
                                        if not self.wpisalem:
                                                self.textField.Remove(self.nr,self.nr+1)
                                                self.textField.SetInsertionPoint(self.nr)
                                                self.textField.WriteText(label)
                                                self.typewriterKeySound.play( )
                                                self.wpisalem=True
                                
				self.flag = 'row'
				self.rowIteration = 0
				self.columnIteration = 0
				self.countColumns = 0

			elif self.flag == 'columns' and self.rowIteration == self.numberOfRows[ self.subSizerNumber ] - 1:
			
				item = self.subSizers[ self.subSizerNumber ].GetItem( ( self.rowIteration ) * self.numberOfColumns[ self.subSizerNumber ] + self.columnIteration-1 )
				b = item.GetWindow( )
				b.SetBackgroundColour( self.selectionColour )
				b.SetFocus( )
				b.Update( )
				
				label = self.labels[ self.subSizerNumber ][ self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + self.columnIteration-1 ]
				
				if label == 'DELETE':
                                        self.textField.Remove(0,len(self.slowo))
                                        #self.textField.SetInsertionPoint(self.nr)
                                        self.textField.WriteText(self.slowoZBledem)
                                        b.SetBackgroundColour( self.backgroundColour )
                                        b.SetFocus( )
                                        b.Update( )
                                        self.subSizerNumber=1
                                        items=self.subSizers[1].GetChildren()
                                        b=items[self.ktore[-2]].GetWindow()
                                        b.SetBackgroundColour(self.backgroundColour)
                                        b.SetFocus( )
                                        b.Update()
                                        self.parent.mainSizer.Show( item = self.subSizers[ 1 ], show = True, recursive = True )
                                        self.parent.mainSizer.Show( item = self.subSizers[ 0 ], show = False , recursive = True )
                                        self.parent.SetSizer( self.parent.mainSizer )
                                        self.parent.Layout()
                                        self.wpisalem=False
                                        self.voice=False
                                        self.krokCyfry=0
                                                
                                        #if self.ilejuz >0 and self.czyjuz: 
                                        #        self.typewriterForwardSound.play( )
                                        #        self.textField.Replace(self.textField.GetInsertionPoint()-1, self.textField.GetInsertionPoint(),'_')
                                        #        self.ilejuz-=1
                                        #        self.czyjuz=False
				
				elif label == 'SPEAK':
                                        if not self.voice:
                                                self.voice=True
                                                b.SetBackgroundColour('indian red')
                                                b.SetFocus()
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
                                        if hasattr(self,'wpisalem'):
                                                if self.wpisalem:
                                                        self.textField.Remove(self.nr,self.nr+1)
                                                        self.textField.SetInsertionPoint(self.nr)
                                                        self.textField.WriteText('_')
                                                        self.typewriterForwardSound.play( )
                                                        self.wpisalem=False
                                                else:
                                                        pass
                                        #text=self.textField.GetValue()
                                        #if text.count('_')< self.ileLuk:
                                        #        self.typewriterForwardSound.play( )
                                        #        for i in self.ktore:
                                        #                self.textField.Replace(i,i+1,'_')
                                        #                self.ilejuz=0

	 			elif label == 'EXIT':
					self.onExit( )

				else:
					self.parent.stoper2.Stop()
                                        self.parent.ownWord=self.textField.GetValue()
                                        self.parent.check()

                                            
                                self.flag = 'row'
				self.rowIteration = 0
				self.columnIteration = 0
				self.countRows = 0
				self.countColumns = 0
				
                elif self.numberOfPresses == 1 and self.subSizerNumber==1:

                        item = self.subSizers[ 1 ].GetItem(self.ktore[ self.krokCyfry-1] )
			b = item.GetWindow( )
			b.SetBackgroundColour( self.selectionColour )
			b.SetFocus( )
			b.Update( )
                        

                        label=self.labels[1][self.ktore[self.krokCyfry-1]]
                        if label == 'ORISPEAK':
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
                                pass
                        elif label == 'SPEAK':
                                pass
                        elif label == 'EXIT':
                                self.onExit( )
                        elif label == 'DELETE':
                                pass
                        elif label == 'CHECK':
				self.parent.stoper2.Stop()
                                self.parent.ownWord=self.textField.GetValue()
                                self.parent.check()
                        else:
                                nr=int(label)
                                self.nr=nr-1
                                self.wpisalem=False
                                self.textField.Remove(nr-1,nr)
                                self.textField.SetInsertionPoint(nr-1)
                                self.textField.WriteText('_')
                                self.subSizerNumber=0
                                b.SetBackgroundColour( self.backgroundColour )
				b.SetFocus( )
				b.Update( )
                                self.parent.mainSizer.Show( item = self.subSizers[ 1 ], show = False, recursive = True )
                                self.parent.mainSizer.Show( item = self.subSizers[ 0 ], show = True , recursive = True )
                                self.parent.SetSizer( self.parent.mainSizer )
                                self.parent.Layout()
                                
                
		else:
			event.Skip( )		
	
	#-------------------------------------------------------------------------
	def timerUpdate(self, event):

		self.mouseCursor.move( self.winWidth - 12, self.winHeight - 20 )
		
		self.numberOfPresses = 0		

		if self.flag == 'row' and self.subSizerNumber==0:


			self.rowIteration = self.rowIteration % self.numberOfRows[ self.subSizerNumber ]


			items = self.subSizers[ self.subSizerNumber ].GetChildren( )
			for i,item in enumerate(items):
                                if self.voice and i == len(items)-2:
                                        pass
                                else:
                                        b = item.GetWindow( )
                                        b.SetBackgroundColour( self.backgroundColour )
                                        b.SetFocus( )
                                        b.Update( )

			if self.rowIteration == self.numberOfRows[ self.subSizerNumber ] - 1:
				self.countRows += 1
				buttonsToHighlight = range( self.rowIteration * self.numberOfColumns[ self.subSizerNumber ], self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + 6 )
				
			else:
				buttonsToHighlight = range( self.rowIteration * self.numberOfColumns[ self.subSizerNumber ], self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + self.numberOfColumns[ self.subSizerNumber ] )
					
			for i,button in enumerate(buttonsToHighlight):

                                if self.voice and i == len(buttonsToHighlight)-2 and self.rowIteration==self.numberOfRows[self.subSizerNumber]-1:
                                        pass
                                else:
                                        item = self.subSizers[ self.subSizerNumber ].GetItem( button )
                                        b = item.GetWindow( )
                                        b.SetBackgroundColour( self.scanningColour )
                                        b.SetFocus( )
                                        b.Update( )

			self.rowIteration += 1
				
			#if self.voice == 'True':
				#os.system( 'milena_say %i' % ( self.rowIteration ) )

		elif self.flag == 'columns' and self.subSizerNumber==0:

				if self.countColumns == self.maxNumberOfColumns:
					self.flag = 'row'

					item = self.subSizers[ self.subSizerNumber ].GetItem( self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + self.columnIteration - 1 )
                                        
					b = item.GetWindow( )
					b.SetBackgroundColour( self.backgroundColour )

					self.rowIteration = 0
					self.columnIteration = 0
					self.countColumns = 0

				else:
					if self.columnIteration == self.numberOfColumns[ self.subSizerNumber ] - 1 or (self.subSizerNumber == 0 and self.columnIteration == self.numberOfColumns[ self.subSizerNumber ] - 3 and self.rowIteration == self.numberOfRows[ self.subSizerNumber ] - 1 ) or ( self.subSizerNumber == 1 and self.columnIteration == self.numberOfColumns[ self.subSizerNumber ] - 4 and self.rowIteration == self.numberOfRows[ self.subSizerNumber ] - 1 ):
						self.countColumns += 1

					if self.columnIteration == self.numberOfColumns[ self.subSizerNumber ] or ( self.subSizerNumber == 0 and self.columnIteration == self.numberOfColumns[ self.subSizerNumber ] - 2 and self.rowIteration == self.numberOfRows[ self.subSizerNumber ] - 1 ) or ( self.subSizerNumber == 1 and self.columnIteration == self.numberOfColumns[ self.subSizerNumber ] - 3 and self.rowIteration == self.numberOfRows[ self.subSizerNumber ] - 1 ):
						self.columnIteration = 0

					items = self.subSizers[ self.subSizerNumber ].GetChildren( )
					for i,item in enumerate(items):
                                                 if self.voice and i == len(items)-2:
                                                        b = item.GetWindow( )
                                                        b.SetBackgroundColour( 'indian red' )
                                                        b.SetFocus( )
                                                        b.Update( )
                                                 else:
                                                        b = item.GetWindow( )
                                                        b.SetBackgroundColour( self.backgroundColour )
                                                        b.SetFocus( )
                                                        b.Update( )

                                        if self.voice and self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + self.columnIteration ==self.numberOfRows[self.subSizerNumber] * self.numberOfColumns[ self.subSizerNumber ] -(4+self.subSizerNumber):
                                                item = self.subSizers[ self.subSizerNumber ].GetItem( self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + self.columnIteration )
                                                b = item.GetWindow( )
                                                b.SetBackgroundColour( 'orange red')
                                                b.SetFocus( )
                                                b.Update( )
					else:
                                                item = self.subSizers[ self.subSizerNumber ].GetItem( self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + self.columnIteration )
                                                b = item.GetWindow( )
                                                b.SetBackgroundColour( self.scanningColour )
                                                b.SetFocus( )
                                                b.Update( )

                
					if self.voice and self.subSizerNumber==0 and self.rowIteration != self.numberOfRows[0]-1:
                                                self.parent.stoper2.Stop()
                                                label = self.labels[ 0 ][ self.rowIteration * self.numberOfColumns[ 0 ]+ self.columnIteration ]
                                                if label != 'SPECIAL_CHARACTERS':
                                                        self.czytajLitere(label)
                                                else:
                                                        time.sleep(1.5)
                                                self.parent.stoper2.Start(self.timeGap)
						#try:
							#soundIndex = self.phoneLabels.index( [ item for item in self.phoneLabels if item == label ][ 0 ] )
							#sound = self.sounds[ soundIndex ]
							#sound.play( )
							
						#except IndexError:
							#pass
					
					self.columnIteration += 1

		else:
                                items=self.subSizers[1].GetChildren()
                                for i in self.ktore:
                                        b=items[i].GetWindow()
                                        b.SetBackgroundColour( self.backgroundColour )
                                        b.SetFocus( )
                                        b.Update( )

                                b=items[self.ktore[self.krokCyfry]].GetWindow()
                                b.SetBackgroundColour( self.scanningColour )
                                b.SetFocus( )
                                b.Update( )

                                

                                if self.krokCyfry==len(self.ktore)-1:
                                        self.krokCyfry=0
                                else:
                                        self.krokCyfry+=1
