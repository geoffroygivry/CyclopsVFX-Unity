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




def setStyleSheet(main):
		main.setStyleSheet("""


QMainWindow{background-color: rgb(50,50,50);}
QDialog{background-color: rgb(50,50,50);}

QLabel{color: white;}

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




QCheckBox {color: white;
				background-color:orange;
				background: rgb(50,50,50);
				selection-color: white;
				selection-background-color: orange;}


QGroupBox{color: white;}

 /*QComboBox*/
QComboBox {
   color : white;
   border: 1px outset #282b2e;
   background-color: QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #585e62,
        stop:0.5 #474c50,
        stop:1 #393e41
    );
     border-radius: 8px;
     padding: 5px 18px 5px 5px;
     min-width: 30px;
 }
 QComboBox:editable {
 background-color: QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #585e62,
        stop:0.5 #474c50,
        stop:1 #393e41
    );
 }
 QComboBox:!editable, QComboBox::drop-down:editable {
      background: QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #585e62,
        stop:0.5 #474c50,
        stop:1 #393e41
    );
 }
 QComboBox:!editable:on, QComboBox::drop-down:editable:on {
     background: QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #1a1d1e,
        stop:0.2 #2a2d30,
        stop:1 #2d3033
    );
 }
 QComboBox::drop-down {
     subcontrol-origin: padding;
     subcontrol-position: top right;
     width: 20px;

 background-color:QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #c8ced2,
        stop:0.5 #a1a6aa,
        stop:1 #7f8387
    );

     border-left-width: 1px;
     border-left-color: #2d3033;
     border-left-style: solid;
     border-top-right-radius: 8px;
     border-bottom-right-radius: 8px;
 }
 QComboBox::down-arrow {
    image: url(C:/Dropbox/CyclopsVFX/Apps/Steropes/StyleSheet/images/down_arrow.png);
 }
 QComboBox::down-arrow:on {
    image: url(C:/Dropbox/CyclopsVFX/Apps/Steropes/StyleSheet/images/up_arrow.png);
 }


QComboBox QAbstractItemView {
    border: 2px solid darkgray;
    selection-background-color: gray;
 }

QMessageBox{background: rgb(50,50,50);}
QListWidget {background: rgb(70,70,70);
				color: white;
				selection-color: white;
				selection-background-color: orange;
				alternate-background-color: rgb(50,50,50);
				border: 2px solid grey;}

QTreeView {color: white;
        background: rgb(20,20,20);
        border: 1px black;
        border-radius : 10px;
        color: white;
        selection-color: white;
        outline: none;
        selection-background-color: gray;

}

QTreeView::item:hover {
    background: gray;
}

QTreeView::item:selected {
    background: rgb(55,55,55);
}

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
QPushButton[labelClass="pushB"]{color: grey;
				background-color: rgb(45,45,45);
                border-radius : 3px;
				selection-color: black;
				border-style: outset;
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
 background-color: rgb(25, 25, 25);}

QTextEdit[labelClass="DailiesComment"]{
        background: rgb(50,50,50);
        border: 1px black;
        border-radius : 10px;
		color: white;
		selection-color: white;
		selection-background-color: orange;
}

QLabel[labelClass="Main"]{
        background: rgb(20,20,20);
        background-image: url(/Dropbox/CyclopsVFX/Apps/Steropes/SteropesDailies/resources/DailiesBanner04.jpg);
        font-size : 24px;
        font-weight : bold;
        font-family : Arial;
        border-radius : 2px;
        padding : 25px
}

QLabel[labelClass="Pic"]{
        background: rgb(60,60,60);
        padding : 10px
}

QLabel[labelClass="itemInfo"]{
        background: rgb(60,60,60);
        padding : 25px;
        font-size : 11px;
        font-weight : bold;
        font-family : Arial
}

QLabel[labelClass="MiniIcon"]{
        background: rgb(60,60,60);
        padding : 0px;
}


QWidget{
        background: rgb(40,40,40);
        padding : 10px
}

QLineEdit[labelClass="frameIO"] {
				color: white;
				padding : 1 px
}

QListWidget{
        show-decoration-selected: 1;
        border-radius : 10px;
        outline: none;
}

QListView::item:selected {
    border: 3px solid #6a6ea9;
}

QListView:item {
    border: 1px solid black;
}

/*QScrollBar*/
QScrollBar:horizontal {
    background-color: QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #171a1b,
        stop:0.2 #272a2c,
        stop:1 #232528
    );
  max-height: 8px;
    border-radius: 4px;
    }
QScrollBar::handle:horizontal {
    background-color: QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #c8ced2,
        stop:0.5 #a1a6aa,
        stop:1 #7f8387
    );
    border-radius: 4px;
    }
QScrollBar::handle:horizontal:hover, QScrollBar::handle:horizontal:pressed {
    background-color: QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #c8ced2,
        stop:1 #a1a6aa
    );
    border-radius: 4px;
    }
QScrollBar::add-line:horizontal {
      background: none;
      }
QScrollBar::sub-line:horizontal {
      background: none;
      }
QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:pressed , QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:pressed {
      background: none;
      }
QScrollBar::left-arrow:horizontal {
      background: none;
      }
QScrollBar::right-arrow:horizontal{
      background: none;
      }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
    }


QScrollBar:vertical {
    background-color: QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #171a1b,
        stop:0.2 #272a2c,
        stop:1 #232528
    );
    max-width: 8px;
    border-radius: 4px;
    }
QScrollBar::handle:vertical {
    background-color: QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #c8ced2,
        stop:0.5 #a1a6aa,
        stop:1 #7f8387
    );
    border-radius: 4px;
    }
QScrollBar::handle:vertical:hover, QScrollBar::handle:vertical:pressed {
    background-color: QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #c8ced2,
        stop:1 #a1a6aa
    );
    }
QScrollBar::add-line:vertical {
      background: none;
      }
QScrollBar::sub-line:vertical {
      background: none;
      }
QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:pressed , QScrollBar::sub-line:vertical:hover, QScrollBar::sub-line:vertical:pressed {
      background: none;
      }
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
      background: none;
      }
QScrollBar::down-arrow:vertical {
      background: none;
      }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
      background: none;
      }





""")


