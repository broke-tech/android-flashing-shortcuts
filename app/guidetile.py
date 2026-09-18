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

class GuideTile(QGroupBox):
    def __init__(self, name ,placement, iconlocation,desc):
        super().__init__()
        self.p = QLabel()
        self.placementrules = {"top":"border-top-left-radius: 20px ;border-top-right-radius: 20px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px",
                               "middle":"border-top-left-radius: 7px ;border-top-right-radius: 7px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px",
                               "bottom":"border-top-left-radius: 7px ;border-top-right-radius: 7px; border-bottom-right-radius: 20px; border-bottom-left-radius: 20px"}
        self.placement = placement
        
        self.l = QVBoxLayout()
        self.setLayout(self.l)

        self.gt = TitleBox(name, iconlocation)
        self.l.addWidget(self.gt)

        self.descl = QHBoxLayout()
        self.l.addLayout(self.descl)
        self.desc = QTextEdit(desc)
        self.desc.setReadOnly(True)
        self.descl.addWidget(self.desc)
        self.setStyleSheet("QGroupBox{"+f"{self.placementrules[self.placement]};"+"background-color: #303030;} QPushButton { background-color: #5A5A5A; border-radius: 7px; padding: 5px} QPushButton::hover { background-color: #636363; border-radius: 7px; padding: 5px} QTextEdit { background-color: #5A5A5A; border-radius: 7px; padding: 5px}")


class TitleBox(QGroupBox):
    clicked = pyqtSignal()
    def __init__(self,name, icon):
        super().__init__()
        self.setMaximumHeight(70)
        self.tl = QHBoxLayout()
        self.setLayout(self.tl)
        self.i = QPixmap(icon).scaled(25,25,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.p = QLabel()
        self.p.setPixmap(self.i)
        self.tl.addWidget(self.p)
        self.ft = QLabel(name)
        self.ft.setStyleSheet("font-size: 16px")
        self.tl.addWidget(self.ft)
        self.tl.addStretch()

    def mouseReleaseEvent(self, event: QMouseEvent):
        # Only trigger if left mouse button is released inside the widget
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)