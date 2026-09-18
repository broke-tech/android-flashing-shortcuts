from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QSizePolicy,QListWidgetItem, QDialog, QGroupBox, QSpacerItem, QProgressBar,QRadioButton, QFrame, QScrollArea, QFileDialog, QComboBox, QCheckBox, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QPushButton, QLineEdit, QTextEdit, QListWidget
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor, QFontDatabase, QPalette, QMouseEvent
import uitools
import os
import json
import requests
from webbrowser import open as opensite
import subprocess
import sys

class SideWidget(QGroupBox):
    clicked = pyqtSignal()

    def __init__(self, name ,placement, iconlocation, g, parentv, runtime):
        super().__init__()
        self.g = g
        self.parentv = parentv
        self.p = QLabel()
        self.placementrules = {"top":"border-top-left-radius: 20px ;border-top-right-radius: 20px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px",
                               "middle":"border-top-left-radius: 7px ;border-top-right-radius: 7px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px",
                               "bottom":"border-top-left-radius: 7px ;border-top-right-radius: 7px; border-bottom-right-radius: 20px; border-bottom-left-radius: 20px"}
        self.placement = placement
        self.i = QPixmap(iconlocation).scaled(50,50,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.p.setPixmap(self.i)
        self.l = QHBoxLayout()
        self.l.addWidget(self.p)

        self.tl = QVBoxLayout()
        self.tl.addStretch()
        self.ft = QLabel(name)
        self.ft.setStyleSheet("font-size: 20px")
        self.tl.addWidget(self.ft)
        #self.tl.addWidget(self.dt)
        self.tl.addStretch()

        self.l.addLayout(self.tl)
        self.l.addStretch()

        self.setLayout(self.l)
        self.setStyleSheet(f"{self.placementrules[self.placement]}; background-color: "+uitools.colors["toolgb"][self.parentv.mode])
        self.clicked.connect(lambda: self.switch(self.parentv.sidebars,self.parentv.gs,runtime))
        self.setFixedHeight(70)

    def mouseReleaseEvent(self, event: QMouseEvent):
        # Only trigger if left mouse button is released inside the widget
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def switch(self, others,othergs,runtime):
        if runtime.isRunning != True:
            if self.g == self.parentv.appsg:
                self.parentv.AppRuntime.startc()
                

            for i in others:
                i.setStyleSheet(f"{i.placementrules[i.placement]}; background-color: "+uitools.colors["toolgb"][self.parentv.mode]+"")
            self.setStyleSheet(f"{self.placementrules[self.placement]}; background-color: "+uitools.colors["selgb"][self.parentv.mode]+"")

            for i in othergs:
                i.hide()
            self.g.show()

