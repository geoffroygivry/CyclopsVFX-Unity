#!/usr/bin/env python

#The MIT License (MIT)
#
#Copyright (c) 2015 Geoffroy Givry
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from __future__ import division
import sys
from math import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os


versionNote = 1.04


def setStyleSheet(main):
		main.setStyleSheet("""


QMainWindow{background-color: rgb(50,50,50);}
QDialog{background-color: rgb(50,50,50);}

QLabel{color: white;}
QLabel[mandatory="true"] { 
				color: red; 
				}

QLineEdit {border: 1px solid grey;
				color: white;
				background: rgb(50,50,50);
				selection-color: white;
				selection-background-color: orange;}
				

QSpinBox {color: white;
				background-color:orange;
				background: rgb(75,75,75);
				selection-color: white;
				selection-background-color: orange;}				
QTextBrowser {border: 1px solid orange;
				color: white;
				background: rgb(100,100,100);
				selection-color: white;
				selection-background-color: orange;}
QTextEdit {border: 1px solid orange;
				color: white;
				background: rgb(100,100,100);
				selection-color: white;
				selection-background-color: orange;}
QCheckBox {color: white;
				background-color:orange;
				background: rgb(50,50,50);
				selection-color: white;
				selection-background-color: orange;}


QGroupBox{color: white;}
QComboBox{color: white;
				background-color: rgb(100,100,100);}


				
				
		
QMessageBox{background: rgb(50,50,50);}
QListWidget {background: rgb(70,70,70);
				color: white;
				selection-color: white;
				selection-background-color: orange;
				alternate-background-color: rgb(50,50,50);
				border: 2px solid grey;}
				
QCalendar {background: rgb(100,100,100);
				color: white;
				selection-color: white;
				selection-background-color: orange;
				alternate-background-color: rgb(25,25,25);
				border: 1px solid orange;}
				
QTableWidget {background: rgb(100,100,100);
				color: white;
				selection-color: white;
				selection-background-color: orange;
				alternate-background-color: rgb(90,90,90);
				border: 1px solid orange;}
QProgressBar{color: white;
				background-color: rgb(75,75,75);
				selection-color: black;
				border-style: outset;
				border-width: 1px;
				border-color: black;
				selection-background-color: orange;
				text-align: center;}


QTabWidget {background: rgb(50,50,50);
				color: white;
				selection-color: white;
				selection-background-color: orange;
				alternate-background-color: rgb(90,90,90);
				border: 1px solid orange;}
QPushButton{color: white;
				background-color: rgb(75,75,75);
				selection-color: black;
				border-width: 1px;
				border-color: black;
				selection-background-color: orange;}
QTabWidget {background: rgb(50,50,50);
				color: white;
				selection-color: white;
				selection-background-color: orange;
				alternate-background-color: rgb(90,90,90);
				border: 1px solid orange;}


QPushButton:pressed {
 background-color: rgb(25, 25, 25);}""")



class Form(QDialog):

        def __init__(self, parent=None):

                super(Form, self).__init__(parent)
                self.browser = QTextEdit()
                self.browser2 = QTextEdit()
                #self.lineedit = QLineEdit("")
                self.lineedit2 = QLineEdit("")
                
                self.nothingButton = QPushButton()
                self.nothingButton.hide()
                self.saveButton = QPushButton("Save")
                self.loadButton = QPushButton("Load")
                self.clearButton = QPushButton("Clear")
                self.newButton = QPushButton("New Note")
                
                splitter = QSplitter()
                splitter.addWidget(self.browser)
                splitter.addWidget(self.browser2)
                layoutH = QHBoxLayout()
                layoutH.addWidget(splitter)
                
                buttonLayout = QHBoxLayout()
                buttonLayout.addStretch()
                buttonLayout.addWidget(self.nothingButton)
                buttonLayout.addWidget(self.newButton)
                buttonLayout.addWidget(self.clearButton)
                buttonLayout.addWidget(self.saveButton)
                buttonLayout.addWidget(self.loadButton)
                layout = QVBoxLayout()
                layout.addWidget(self.lineedit2)
                layout.addLayout(layoutH)
                #layout.addWidget(self.lineedit)
                layout.addLayout(buttonLayout)
                self.setLayout(layout)
                
                self.connect(self.newButton, SIGNAL("clicked()"),self.newNote)
                self.connect(self.clearButton, SIGNAL("clicked()"),self.clearTextBrowser)
                self.connect(self.loadButton, SIGNAL("clicked()"),self.showDialog)
                self.connect(self.saveButton, SIGNAL("clicked()"),self.saveDialog)
                self.connect(self.lineedit2, SIGNAL("returnPressed()"),self.updateTitle)
                #self.connect(self.lineedit, SIGNAL("returnPressed()"),self.updateUi)
                self.setWindowIcon(QIcon('C:\Users\Geoffroy\.nuke\icons/WizardFX_icon.png'))
                self.setWindowTitle('GeoffNote'+ str(versionNote))
                setStyleSheet(self)

        def updateUi(self):

                text = unicode(self.lineedit.text())
                self.browser.append(text)
                self.lineedit.clear()
                

        def updateTitle(self):

                textTitle = unicode(self.lineedit2.text())
                self.setWindowTitle(textTitle)
                self.lineedit2.clear()

        def showDialog(self):

            try:
                fname = QFileDialog.getOpenFileName(self, 'Open file',  '/home')
                print 'Location File: ' + fname
                f = open(fname, 'r')
                
                        
                data = f.read()
                self.browser.setText(data)
                newTitle = unicode(fname.split('/')[-1])
                self.setWindowTitle(newTitle)
            except IOError:
                pass

        def saveDialog(self):

            try:
                fname2 = QFileDialog.getSaveFileName(self, 'Save File')
            
                f2 = open(fname2, 'w')
                f2.write(unicode(self.browser.toPlainText()))
                f2.close()
            except IOError:
                pass
            
        def clearTextBrowser(self):

            self.browser.clear()
            self.setWindowTitle('GeoffNote')
            
            
        def newNote(self):
            
            noteVersion = ('~/geoffNote' +str(versionNote) + '.py' + ' & exit')
            os.system(noteVersion)


def launchApp():

    launchApp.panel = Form()
    launchApp.panel.show()



