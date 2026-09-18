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

class AppearanceSettings(QGroupBox):
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

        self.gl.addWidget(QLabel("Display mode"),alignment=Qt.AlignHCenter)
        self.glmode = QHBoxLayout()
        self.glmodeh1 = QVBoxLayout()
        self.glmodeh2 = QVBoxLayout()
        self.gl.addLayout(self.glmode)
        self.glmode.addStretch()
        self.glmode.addLayout(self.glmodeh1)
        self.glmode.addLayout(self.glmodeh2)
        self.glmode.addStretch()

        self.llabel = QLabel()
        self.dlabel = QLabel()
        self.llabel.setPixmap(QPixmap(os.path.join(self.parentv.curdir,"assets","images","light.png")).scaled(300,150,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))
        self.dlabel.setPixmap(QPixmap(os.path.join(self.parentv.curdir,"assets","images","dark.png")).scaled(300,150,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))
        self.lradio = QRadioButton("Light mode")
        self.lradio.clicked.connect(lambda:self.changemode("light"))
        self.dradio = QRadioButton("Dark mode")
        self.dradio.clicked.connect(lambda:self.changemode("dark"))
        if self.parentv.mode == "dark":
            self.dradio.setChecked(True)
        else:
            self.lradio.setChecked(True)
        self.glmodeh1.addWidget(self.llabel)
        self.glmodeh1.addWidget(self.lradio,alignment=Qt.AlignHCenter)
        self.glmodeh2.addWidget(self.dlabel)
        self.glmodeh2.addWidget(self.dradio,alignment=Qt.AlignHCenter)

        self.l.addWidget(self.g)
        self.setLayout(self.l)
        self.gl.addStretch()
        self.setStyleSheet("QGroupBox{"+f"{self.placementrules[self.placement]};"+"background-color: "+uitools.colors["toolgb"][self.parentv.mode]+";} QPushButton { background-color: #5A5A5A; border-radius: 7px; padding: 5px} QPushButton::hover { background-color: #636363; border-radius: 7px; padding: 5px} QLineEdit { background-color: #5A5A5A; border-radius: 7px; padding: 5px}")

    def changemode(self,towhat):
        self.parentv.config["mode"] = towhat
        with open(os.path.join(self.parentv.curdir,"assets","config.json"),"w") as f:
            json.dump(self.parentv.config,f)
        self.mode = self.parentv.config["mode"]
        self.parentv.msg.showup("Restart AFS to apply changes.")

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