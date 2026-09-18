from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QSizePolicy,QListWidgetItem, QDialog, QGroupBox, QSpacerItem, QProgressBar,QRadioButton, QFrame, QScrollArea, QFileDialog, QComboBox, QCheckBox, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QPushButton, QLineEdit, QTextEdit, QListWidget
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor, QFontDatabase, QPalette
import os
import json
import requests
from webbrowser import open as opensite
import subprocess
import sys

colors = {
    "toolgb":{"light":"#D4D4D4","dark":"#303030"},
    "backgb":{"light":"#E2E2E2","dark":"#1a1a1a"},
    "selgb":{"light":"#A7A7A7","dark":"#5A5A5A"}
}

def refresh_ui(app): #By chatGPT
    app.processEvents()
    for widget in app.allWidgets():
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()

def setfont(fonts,widget,app):
    font_path = fonts
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        widget.setFont(QFont(font_family,11))
    else:
        pass
    refresh_ui(app)

def setmodeblack(widget):
    palette = QPalette()
    palette.setColor(QPalette.Window, Qt.black)
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, Qt.black)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor("#242424"))
    palette.setColor(QPalette.ButtonText, Qt.white)
    widget.setPalette(palette)

def setmodewhite(widget):
    palette = QPalette()
    palette.setColor(QPalette.Window, Qt.white)
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, Qt.white)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor("#B9B9B9"))
    palette.setColor(QPalette.ButtonText, Qt.black)
    widget.setPalette(palette)

def clear_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clear_layout(item.layout())