from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QSizePolicy,QListWidgetItem, QDialog, QGroupBox, QSpacerItem, QProgressBar,QRadioButton, QFrame, QScrollArea, QFileDialog, QComboBox, QCheckBox, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QPushButton, QLineEdit, QTextEdit, QListWidget
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor, QFontDatabase, QPalette, QMouseEvent
import uitools
from main import *
import os
from webbrowser import open_new_tab as opensite
import sys

class Start(QDialog):
    def __init__(self, parentv, runtime):
        super().__init__()
        self.parentv = parentv
        self.setWindowTitle("AFS - Setup")
        self.setWindowIcon(QIcon(os.path.join(self.parentv.curdir,"assets","icons","icon.ico")))
        self.resize(400,700)

        self.l = QVBoxLayout()
        self.setLayout(self.l)
        self.runtime = runtime
        self.setStyleSheet("QGroupBox{ border-radius: 20; background-color: "+uitools.colors["backgb"][self.parentv.mode]+";} QPushButton { background-color: "+uitools.colors["line"][self.parentv.config["mode"]]+"; border-radius: 10; padding: 5} QPushButton::hover { background-color: #636363; border-radius: 10; padding: 5} QLineEdit { background-color: "+uitools.colors["line"][self.parentv.config["mode"]]+"; border-radius: 7; padding: 5}")

        self.g1 = QGroupBox()
        self.g1l = QVBoxLayout()
        self.g1.setLayout(self.g1l)
        self.p = QLabel()
        self.i = QPixmap(os.path.join(parentv.curdir,"assets","icons","afstinted.png")).scaled(50,50,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.p.setPixmap(self.i)
        self.g1l.addWidget(self.p,alignment=Qt.AlignHCenter)
        self.g1l.addWidget(QLabel("Welcome to Android Flashing Shortcuts!"),alignment=Qt.AlignHCenter)
        self.g1l.addStretch()

        self.g1label = QLabel("Thanks for using AFS! Here you can:\n - Run ADB commands\n - Run Fastboot commands\n - Manage your apps (including system apps)\n..and more!\n\nLet's go through a basic setup to make your experience as good as possible!")
        self.g1l.addWidget(self.g1label,alignment=Qt.AlignHCenter)

        self.g1l.addStretch()
        self.g1but = QPushButton("Next (1/3)")
        self.g1l.addWidget(self.g1but)
        self.g1but.clicked.connect(lambda: self.nextt(self.g1,self.g2))
        self.l.addWidget(self.g1)

        self.g2 = QGroupBox()
        self.g2.hide()
        self.g2l = QVBoxLayout()
        self.g2.setLayout(self.g2l)
        self.p = QLabel()
        self.i = QPixmap(os.path.join(parentv.curdir,"assets","sideicons","fastboot.png")).scaled(50,50,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.p.setPixmap(self.i)
        self.g2l.addWidget(self.p,alignment=Qt.AlignHCenter)
        self.g2l.addWidget(QLabel("Let's check if all drivers are working correctly.\n"),alignment=Qt.AlignHCenter)
        self.g2l.addStretch()

        self.g2label = QLabel("WARNING: DON'T FOLLOW THESE STEPS WITH A SAMSUNG PHONE AS IT CAN'T USE FASTBOOT!\n\nTo make sure you can use all functions let's check if fastboot drivers are installed properly:\n\n1. Power off your device.\n2. Press and hold the Power and Volume Down buttons.\n3. Your device should enter Fastboot mode.\n4. Finally click the Refresh button below\n\nIf the text below shows 'Not connected' even though your device is connected in Fastboot mode, you should reinstall the Fastboot drivers.\n")
        self.g2label.setWordWrap(True)
        self.g2l.addWidget(self.g2label,alignment=Qt.AlignHCenter)
        self.refreshtext = QLabel("Click the refresh button")
        self.refresh = QPushButton("Refresh")
        self.refresh.clicked.connect(self.check_devices)
        self.g2l.addWidget(self.refreshtext,alignment=Qt.AlignHCenter)
        self.g2l.addWidget(self.refresh,alignment=Qt.AlignHCenter)
        self.g2l.addWidget(QLabel("\n"))

        self.g2l.addStretch()
        self.g2butl = QHBoxLayout()
        self.g2l.addLayout(self.g2butl)
        self.g2but = QPushButton("Next (2/3)")
        self.g2fbut = QPushButton("Reinstall fastboot drivers")
        self.g2fbut.clicked.connect(lambda:opensite("https://github.com/fawazahmed0/Latest-adb-fastboot-installer-for-windows"))
        self.g2butl.addWidget(self.g2but)
        self.g2butl.addWidget(self.g2fbut)
        self.g2but.clicked.connect(lambda: self.nextt(self.g2,self.g3))
        self.l.addWidget(self.g2)

        self.g3 = QGroupBox()
        self.g3.hide()
        self.g3l = QVBoxLayout()
        self.g3.setLayout(self.g3l)
        self.p = QLabel()
        self.i = QPixmap(os.path.join(parentv.curdir,"assets","icons","check.png")).scaled(50,50,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.p.setPixmap(self.i)
        self.g3l.addWidget(self.p,alignment=Qt.AlignHCenter)
        self.g3l.addWidget(QLabel("Final touches\n"),alignment=Qt.AlignHCenter)
        self.g3l.addStretch()

        self.g3label = QLabel("Automatic updates are off. You can check manually in Updates.\n\nIf you aren't familiar with android modding, I recommend turning on Safe mode. It disables commands that may put your device at risk.\nThere are more configurations in Settings.")
        self.g3label.setWordWrap(True)
        self.g3l.addWidget(self.g3label,alignment=Qt.AlignHCenter)
        self.safe = QPushButton("Turn on Safe mode")
        if self.parentv.config["safe"] == True:
            self.safe.setText("Safe mode is on")
        self.safe.clicked.connect(self.changesafe)
        self.g3l.addWidget(self.safe,alignment=Qt.AlignHCenter)
        self.g3l.addWidget(QLabel("\n"))

        self.g3l.addStretch()
        self.g3butl = QHBoxLayout()
        self.g3l.addLayout(self.g3butl)
        self.g3but = QPushButton("Finish (3/3)")
        self.g3fbut = QPushButton("Join Discord server")
        self.g3fbut.clicked.connect(lambda:opensite("https://www.discord.gg/FRbg2Vzq7X"))
        self.g3butl.addWidget(self.g3but)
        self.g3butl.addWidget(self.g3fbut)
        self.g3but.clicked.connect(self.finish)
        self.l.addWidget(self.g3)
        
    def nextt(self,a,b):
        a.hide()
        b.show()

    def check_devices(self):
        workercheck = QProcess()
        workercheck.setWorkingDirectory(os.path.join(self.parentv.curdir,"assets","platform-tools"))
        def updatecheck():
            try:
                out = bytes(workercheck.readAllStandardOutput()).decode().strip()
                err = bytes(workercheck.readAllStandardError()).decode().strip()
                if out:
                    pass
                if err:
                    if "waiting for" in err:
                        workercheck.kill()
                        #righttitle.setText('TOOLS | Fastboot: No devices')
                        self.refreshtext.setText('Not connected')
                    else:
                        if "product:" in err:
                            #righttitle.setText(f"TOOLS | Fastboot: {err.partition("Finished")[0].partition("\n")[0].partition("product: ")[2]}")
                            self.refreshtext.setText(f'Connected to {err.partition("Finished")[0].partition("\n")[0].partition("product: ")[2]}')
                        else:
                            workercheck.kill()
                            #righttitle.setText('TOOLS | Fastboot: No devices')
                            self.refreshtext.setText('Not connected\n')
            except:
                pass
        workercheck.readyReadStandardOutput.connect(updatecheck)
        workercheck.readyReadStandardError.connect(updatecheck)
        workercheck.finished.connect(updatecheck)

        workercheck.start("fastboot getvar product")

    def changesafe(self):
        self.parentv.config["safe"] = True
        self.safe.setText("Safe mode is on")
        with open(os.path.join(self.parentv.curdir,"assets","config.json"),"w") as f:
            json.dump(self.parentv.config,f)

    def finish(self):
        self.parentv.config["first"] = False
        with open(os.path.join(self.parentv.curdir,"assets","config.json"),"w") as f:
            json.dump(self.parentv.config,f)
        self.hide()