from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QSizePolicy,QListWidgetItem, QDialog, QGroupBox, QSpacerItem, QProgressBar,QRadioButton, QFrame, QScrollArea, QFileDialog, QComboBox, QCheckBox, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QPushButton, QLineEdit, QTextEdit, QListWidget
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor, QFontDatabase, QPalette, QMouseEvent
import uitools
import runtime
import os
import json
import requests
from webbrowser import open as opensite
import subprocess
import sys

class SafetySettings(QGroupBox):
    def __init__(self, name ,placement, iconlocation,parentv):
        super().__init__()
        self.runtime = runtime
        self.parentv = parentv
        self.p = QLabel()
        self.placementrules = {"top":"border-top-left-radius: 20px ;border-top-right-radius: 20px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px",
                               "middle":"border-top-left-radius: 7px ;border-top-right-radius: 7px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px",
                               "bottom":"border-top-left-radius: 7px ;border-top-right-radius: 7px; border-bottom-right-radius: 20px; border-bottom-left-radius: 20px"}
        self.placement = placement
        
        self.l = QVBoxLayout()

        self.gt = TitleBox(name, iconlocation)
        self.l.addWidget(self.gt)

        self.g = QGroupBox()
        self.gl = QVBoxLayout()
        self.g.setLayout(self.gl)

        self.gl.addWidget(QLabel("Warning dialogs"),alignment=Qt.AlignHCenter)
        self.glstart = QHBoxLayout()
        self.gl.addLayout(self.glstart)
        self.glstart.addWidget(QLabel("Show warning dialog on startup:"),alignment=Qt.AlignHCenter)
        self.glstart.addStretch()
        self.glstartbox = QCheckBox()
        self.glstartbox.stateChanged.connect(self.changestartd)
        self.glstart.addWidget(self.glstartbox)
        l1 = QLabel("When starting up AFS, a warning dialog pops up about the risks of this app. You can disable this but the risks still apply.\n")
        l1.setWordWrap(True)
        self.gl.addWidget(l1)
        
        if self.parentv.config["startd"] == True:
            self.glstartbox.setChecked(True)
        else:
            self.glstartbox.setChecked(False)

        self.gldialogs = QHBoxLayout()
        self.gl.addLayout(self.gldialogs)
        self.gldialogs.addWidget(QLabel("Confirm before running command:"),alignment=Qt.AlignHCenter)
        self.gldialogs.addStretch()
        self.gldialogsbox = QCheckBox()
        self.gldialogsbox.stateChanged.connect(self.changedialog)
        self.gldialogs.addWidget(self.gldialogsbox)
        l2 = QLabel("NOT RECOMMENDED TO DISABLE!!! These are the confirmation dialogs before running a command, in order you are not sure or you pressed a button accidentally.\n")
        l2.setWordWrap(True)
        self.gl.addWidget(l2)
        
        if self.parentv.config["dialogs"] == True:
            self.gldialogsbox.setChecked(True)
        else:
            self.gldialogsbox.setChecked(False)

        self.glsafe = QHBoxLayout()
        self.gl.addLayout(self.glsafe)
        self.glsafe.addWidget(QLabel("Safe mode:"),alignment=Qt.AlignHCenter)
        self.glsafe.addStretch()
        self.glsafebox = QCheckBox()
        self.glsafebox.stateChanged.connect(self.changesafe)
        self.glsafe.addWidget(self.glsafebox)
        l3 = QLabel("Safe mode disables risky tools that have the ability to damage your device. Recommended for android modding begginers and people with a locked bootloader\n")
        l3.setWordWrap(True)
        self.gl.addWidget(l3)
        
        if self.parentv.config["safe"] == True:
            self.glsafebox.setChecked(True)
        else:
            self.glsafebox.setChecked(False)

        self.l.addWidget(self.g)
        self.setLayout(self.l)
        self.gl.addStretch()
        self.setStyleSheet("QGroupBox{"+f"{self.placementrules[self.placement]};"+"background-color: "+uitools.colors["toolgb"][self.parentv.mode]+";} QPushButton { background-color: #5A5A5A; border-radius: 7px; padding: 5px} QPushButton::hover { background-color: #636363; border-radius: 7px; padding: 5px} QLineEdit { background-color: #5A5A5A; border-radius: 7px; padding: 5px}")

    def showhide(self):
        if self.parentv.Runtime.isRunning != True:
            if self.state == True:
                self.g.hide()
                self.state = False
            elif self.state == False:
                for i in self.parentv.tools:
                    i.hidei()
                self.g.show()
                self.state = True

    def showi(self):
        self.g.show()
        self.state = True

    def hidei(self):
        self.g.hide()
        self.state = False

    def changestartd(self):
        self.parentv.config["startd"] = self.glstartbox.isChecked()
        with open(os.path.join(self.parentv.curdir,"assets","config.json"),"w") as f:
            json.dump(self.parentv.config,f)

    def changedialog(self):
        self.parentv.config["dialogs"] = self.gldialogsbox.isChecked()
        with open(os.path.join(self.parentv.curdir,"assets","config.json"),"w") as f:
            json.dump(self.parentv.config,f)

    def changesafe(self):
        self.parentv.config["safe"] = self.glsafebox.isChecked()
        with open(os.path.join(self.parentv.curdir,"assets","config.json"),"w") as f:
            json.dump(self.parentv.config,f)

class TitleBox(QGroupBox):
    def __init__(self,name, icon):
        super().__init__()
        self.setMaximumHeight(70)
        self.tl = QHBoxLayout()
        self.setLayout(self.tl)
        self.i = QPixmap(icon).scaled(50,50,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.p = QLabel()
        self.p.setPixmap(self.i)
        self.tl.addWidget(self.p)
        self.ft = QLabel(name)
        self.ft.setStyleSheet("font-size: 20px")
        self.tl.addWidget(self.ft)
        self.tl.addStretch()