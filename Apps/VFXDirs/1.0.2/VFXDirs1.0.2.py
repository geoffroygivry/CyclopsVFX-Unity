# -*- coding: utf-8 -*-

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



from PyQt4 import QtCore, QtGui
import os




def setStyleSheet(main):
        main.setStyleSheet("""


QMainWindow{background-color: rgb(50,50,50);}
QDialog{background-color: rgb(50,50,50);}

QLabel{color: white;}
QLabel[mandatory="true"] { 
                color: red; 
                }

QLineEdit {border: 1px solid orange;
                color: white;
                background: rgb(50,50,50);
                selection-color: white;
                selection-background-color: orange;}
                
                
QLineEdit:disabled
{
color: grey;
background: black;
} 


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
QListWidget {background: rgb(90,90,90);
                color: white;
                selection-color: white;
                selection-background-color: orange;
                alternate-background-color: rgb(50,50,50);
                border: 1px solid orange;}
                
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

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DialogVFXDirs(object):
    def setupUi(self, DialogVFXDirs):
        DialogVFXDirs.setObjectName(_fromUtf8("DialogVFXDirs"))
        DialogVFXDirs.resize(750, 175)
        DialogVFXDirs.setMinimumSize(QtCore.QSize(750, 175))
        DialogVFXDirs.setMaximumSize(QtCore.QSize(750, 175))
        DialogVFXDirs.setWindowTitle(QtGui.QApplication.translate("DialogVFXDirs", "VFX Dirs1.01", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDI = QtGui.QLabel(DialogVFXDirs)
        self.labelDI.setGeometry(QtCore.QRect(650, 140, 91, 31))
        self.labelDI.setText(QtGui.QApplication.translate("DialogVFXDirs", "Digital Iluminati", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDI.setObjectName(_fromUtf8("labelDI"))
        self.listWidget = QtGui.QListWidget(DialogVFXDirs)
        self.listWidget.setGeometry(QtCore.QRect(60, 60, 111, 111))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        item = QtGui.QListWidgetItem()
        item.setText(QtGui.QApplication.translate("DialogVFXDirs", "ROOT", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setText(QtGui.QApplication.translate("DialogVFXDirs", "ASSET", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setText(QtGui.QApplication.translate("DialogVFXDirs", "ONSET", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setText(QtGui.QApplication.translate("DialogVFXDirs", "SEQUENCE", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setText(QtGui.QApplication.translate("DialogVFXDirs", "SHOT", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setText(QtGui.QApplication.translate("DialogVFXDirs", "TASK", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.addItem(item)
        self.labelVFXDirs = QtGui.QLabel(DialogVFXDirs)
        self.labelVFXDirs.setGeometry(QtCore.QRect(10, 10, 61, 16))
        self.labelVFXDirs.setText(QtGui.QApplication.translate("DialogVFXDirs", "VFX Dirs1.01", None, QtGui.QApplication.UnicodeUTF8))
        self.labelVFXDirs.setObjectName(_fromUtf8("labelVFXDirs"))
        self.labelCreate = QtGui.QLabel(DialogVFXDirs)
        self.labelCreate.setGeometry(QtCore.QRect(10, 60, 51, 16))
        self.labelCreate.setText(QtGui.QApplication.translate("DialogVFXDirs", "Create:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCreate.setObjectName(_fromUtf8("labelCreate"))
        self.labelPath = QtGui.QLabel(DialogVFXDirs)
        self.labelPath.setGeometry(QtCore.QRect(200, 60, 31, 16))
        self.labelPath.setText(QtGui.QApplication.translate("DialogVFXDirs", "Path:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPath.setObjectName(_fromUtf8("labelPath"))
        self.lineEditPath = QtGui.QLineEdit(DialogVFXDirs)
        self.lineEditPath.setGeometry(QtCore.QRect(240, 60, 371, 20))
        self.lineEditPath.setText(QtGui.QApplication.translate("DialogVFXDirs", "C:\Dropbox\jobs\Babiru3D", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditPath.setObjectName(_fromUtf8("lineEditPath"))
        self.mkDirButton = QtGui.QPushButton(DialogVFXDirs)
        self.mkDirButton.setGeometry(QtCore.QRect(620, 60, 121, 24))
        self.mkDirButton.setText(QtGui.QApplication.translate("DialogVFXDirs", "Create VFX Dir!", None, QtGui.QApplication.UnicodeUTF8))
        self.mkDirButton.setObjectName(_fromUtf8("mkDirButton"))
        self.multiShotsCB = QtGui.QCheckBox(DialogVFXDirs)
        self.multiShotsCB.setGeometry(QtCore.QRect(240, 140, 141, 19))
        self.multiShotsCB.setText(QtGui.QApplication.translate("DialogVFXDirs", "Multi shots creation", None, QtGui.QApplication.UnicodeUTF8))
        self.multiShotsCB.setObjectName(_fromUtf8("multiShotsCB"))
        self.numberInt = QtGui.QLineEdit(DialogVFXDirs)
        self.numberInt.setGeometry(QtCore.QRect(380, 140, 51, 20))
        self.numberInt.setText(QtGui.QApplication.translate("DialogVFXDirs", "3", None, QtGui.QApplication.UnicodeUTF8))
        self.numberInt.setObjectName(_fromUtf8("numberInt"))
        self.lineTop = QtGui.QFrame(DialogVFXDirs)
        self.lineTop.setGeometry(QtCore.QRect(10, 30, 731, 16))
        self.lineTop.setFrameShape(QtGui.QFrame.HLine)
        self.lineTop.setFrameShadow(QtGui.QFrame.Sunken)
        self.lineTop.setObjectName(_fromUtf8("lineTop"))
        self.lineEditName = QtGui.QLineEdit(DialogVFXDirs)
        self.lineEditName.setGeometry(QtCore.QRect(240, 90, 191, 20))
        self.lineEditName.setText(QtGui.QApplication.translate("DialogVFXDirs", "PEP", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditName.setObjectName(_fromUtf8("lineEditName"))
        self.labelName = QtGui.QLabel(DialogVFXDirs)
        self.labelName.setGeometry(QtCore.QRect(200, 90, 41, 20))
        self.labelName.setText(QtGui.QApplication.translate("DialogVFXDirs", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelName.setObjectName(_fromUtf8("labelName"))
        self.lineEditshotNumber = QtGui.QLineEdit(DialogVFXDirs)
        self.lineEditshotNumber.setGeometry(QtCore.QRect(470, 90, 141, 20))
        self.lineEditshotNumber.setText(QtGui.QApplication.translate("DialogVFXDirs", "001", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditshotNumber.setObjectName(_fromUtf8("lineEditshotNumber"))
        self.labelNumberShot = QtGui.QLabel(DialogVFXDirs)
        self.labelNumberShot.setGeometry(QtCore.QRect(440, 90, 31, 20))
        self.labelNumberShot.setText(QtGui.QApplication.translate("DialogVFXDirs", "#:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelNumberShot.setObjectName(_fromUtf8("labelNumberShot"))

        QtCore.QObject.connect(self.mkDirButton, QtCore.SIGNAL("clicked()"),self.makeDirs)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("currentTextChanged(QString)")), self.disableField)
        
        setStyleSheet(DialogVFXDirs)
        
        

        
        
    def disableField(self):
        Field01 = self.lineEditName
        Field02 = self.lineEditshotNumber
        labelShot = self.labelNumberShot
        folderType = self.listWidget.currentItem().text()
        if folderType == "ROOT":
          Field01.setEnabled(False)
          Field01.setText("N/A")
          Field02.setEnabled(False)
          Field02.setText("N/A")
          labelShot.setText("#:")
          
        if folderType == "ASSET":
          Field01.setEnabled(True)
          Field01.setText("")
          Field02.setEnabled(False)
          Field02.setText("N/A")
          labelShot.setText("#:")
          
        if folderType == "SEQUENCE":
          Field01.setEnabled(True)
          Field01.setText("")
          Field02.setEnabled(True)
          Field02.setText("001")
          labelShot.setText("#:")
          
        if folderType == "ONSET":
          Field01.setEnabled(True)
          Field01.setText("")
          Field02.setEnabled(True)
          Field02.setText("01")
          labelShot.setText("pos:")
          
        if folderType == "SHOT":
          Field01.setEnabled(True)
          Field01.setText("")
          Field02.setEnabled(True)
          Field02.setText("001")
          labelShot.setText("#:")

        if folderType == "TASK":
          Field01.setEnabled(True)
          Field01.setText("")
          Field02.setEnabled(False)
          Field02.setText("N/A")
          labelShot.setText("")
        
    def makeDirs(self):
        Field01 = unicode(self.lineEditName.text())
        Field02 = unicode(self.lineEditshotNumber.text())
        folderType = self.listWidget.currentItem().text()
        if folderType == "ROOT":
            pathProj = unicode(self.lineEditPath.text())
            os.makedirs(pathProj + "/PRE/REF/")
            os.makedirs(pathProj + "/PRE/StoryBoard")
            os.makedirs(pathProj + "/GEN/")
            os.makedirs(pathProj + "/ASSET/")
            os.makedirs(pathProj + "/ONSET/")
            os.makedirs(pathProj + "/SEQUENCE/")
            os.makedirs(pathProj + "/TEST/")
            print (' the %s folders have been created!' % pathProj)
        if folderType == "ASSET":
            pathProj = unicode(self.lineEditPath.text()) + "/ASSET/" + Field01
            os.makedirs(pathProj + "/01_REF/")
            os.makedirs(pathProj + "/02_MODEL/Work/Maya")
            os.makedirs(pathProj + "/02_MODEL/Work/Zbrush/")
            os.makedirs(pathProj + "/02_MODEL/Work/Mari/")
            os.makedirs(pathProj + "/02_MODEL/Work/Nuke/")
            os.makedirs(pathProj + "/02_MODEL/Work/Clarisse/")
            os.makedirs(pathProj + "/02_MODEL/Work/Photoshop/")
            os.makedirs(pathProj + "/03_TEXTURE/Hro/")
            os.makedirs(pathProj + "/04_RENDER/Turntable/")
            os.makedirs(pathProj + "/04_RENDER/Thumbnail/")
            os.makedirs(pathProj + "/05_PUBLISHED/")
            print (' the %s folders have been created!' % pathProj)
        if folderType == "SEQUENCE":
            pathProj = unicode(self.lineEditPath.text()) + "/SEQUENCE/" + Field01 + Field02
            os.makedirs(pathProj + "/01_Clips/")
            os.makedirs(pathProj + "/02_Cut/")
            print (' the %s folder have been created!' % pathProj)
        if folderType == "ONSET":
            pathProj = unicode(self.lineEditPath.text()) + "/ONSET/" + Field01
            os.makedirs(pathProj + "/01_HDRI/position" + Field02 + "/jpg/")
            os.makedirs(pathProj + "/01_HDRI/position" + Field02 + "/ibl/")
            try:
                os.makedirs(pathProj + "/02_img_Survey/")
            except WindowsError:
                pass

            print (' the %s folders have been created!' % pathProj)
            
            
        if folderType == "SHOT":
            count = 1
            numberOfShot = int(self.numberInt.text())
            if self.multiShotsCB.isChecked():
              while (count < numberOfShot+1):
                pathProj = unicode(self.lineEditPath.text()) + "/" +  unicode(self.lineEditName.text()) + ("_") + '%03d' %(count)
                try:
                  os.makedirs(pathProj + "/CG")
                  os.makedirs(pathProj + "/Elements")
                  os.makedirs(pathProj + "/OUT")
                  os.makedirs(pathProj + "/REF")
                  os.makedirs(pathProj + "/PLATES")
                except OSError:
                  pass
                count = count + 1
              print "%02d Shot Folders have been created!" % (numberOfShot)
            else:
              pathProj = unicode(self.lineEditPath.text()) + "/" +  unicode(self.lineEditName.text()) + ("_") + unicode(self.lineEditshotNumber.text())
              os.makedirs(pathProj + "/CG")
              os.makedirs(pathProj + "/Elements")
              os.makedirs(pathProj + "/OUT")
              os.makedirs(pathProj + "/REF")
              os.makedirs(pathProj + "/PLATES")
              print (' the %s folders have been created!' % pathProj)

        if folderType == "TASK":
            pathProj = unicode(self.lineEditPath.text()) + "/TASKS/" + Field01
            os.makedirs(pathProj + "/Work/Nuke")
            os.makedirs(pathProj + "/Work/Maya")
            os.makedirs(pathProj + "/Work/Clarisse")
            os.makedirs(pathProj + "/Work/3DE")
            os.makedirs(pathProj + "/Work/Mari")
            os.makedirs(pathProj + "/Work/Photoshop")
            os.makedirs(pathProj + "/PUBLISHED")
            print (' the %s folders have been created!' % pathProj)
            

        

    def retranslateUi(self, DialogVFXDirs):
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item = self.listWidget.item(1)
        item = self.listWidget.item(2)
        item = self.listWidget.item(3)
        item = self.listWidget.item(4)
        self.listWidget.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DialogVFXDirs = QtGui.QDialog()
    ui = Ui_DialogVFXDirs()
    ui.setupUi(DialogVFXDirs)
    DialogVFXDirs.show()
    sys.exit(app.exec_())

