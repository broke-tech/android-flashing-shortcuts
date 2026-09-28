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

class MiscellaneousSettings(QGroupBox):
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
        self.setLayout(self.l)

        self.gt = TitleBox(name, iconlocation)
        self.l.addWidget(self.gt)

        self.g = QGroupBox()
        self.gl = QVBoxLayout()
        self.g.setLayout(self.gl)
        self.l.addWidget(self.g)

        self.gl.addWidget(QLabel("Update settings"),alignment=Qt.AlignHCenter)
        self.glstart = QHBoxLayout()
        self.gl.addLayout(self.glstart)
        self.glstart.addWidget(QLabel("Check for updates on startup:"),alignment=Qt.AlignHCenter)
        self.glstart.addStretch()
        self.glstartbox = QCheckBox()
        self.glstartbox.stateChanged.connect(self.changeucheck)
        self.glstart.addWidget(self.glstartbox)
        l1 = QLabel("AFS checks for updates when starting up. If one is available, a symbol will be shown next to the 'Updates' text in the sidebar. This might delay startup times.")
        l1.setWordWrap(True)
        self.gl.addWidget(l1)
        
        if self.parentv.config["ucheck"] == True:
            self.glstartbox.setChecked(True)
        else:
            self.glstartbox.setChecked(False)
        
        self.setStyleSheet("QGroupBox{"+f"{self.placementrules[self.placement]};"+"background-color: "+uitools.colors["toolgb"][self.parentv.mode]+";} QPushButton { background-color: #5A5A5A; border-radius: 7px; padding: 5px} QPushButton::hover { background-color: #636363; border-radius: 7px; padding: 5px} QLineEdit { background-color: #5A5A5A; border-radius: 7px; padding: 5px}")

    def changeucheck(self):
        self.parentv.config["ucheck"] = self.glstartbox.isChecked()
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