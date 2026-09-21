from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QSizePolicy,QListWidgetItem, QDialog, QGroupBox, QSpacerItem, QProgressBar,QRadioButton, QFrame, QScrollArea, QFileDialog, QComboBox, QCheckBox, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QPushButton, QLineEdit, QTextEdit, QListWidget
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor, QFontDatabase, QPalette, QMouseEvent
from webbrowser import open_new_tab as opensite
import uitools
import runtime
import adbtools
import fastboottools
import sidewidget
import abouttiles
import start
import appruntime
import apptile
import appearancesetting
import safetysetting
import os
import json
import requests
import sys

curdir = os.getcwd()
version = "3.0"

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(curdir,"assets","icons","icon.ico")))
        self.setWindowTitle("AFS - Android Flashing Shortcuts")
        with open(os.path.join(curdir,"assets","config.json"),"r") as f:
            self.config = json.load(f)
        self.mode = self.config["mode"]
        
        if self.mode == "dark":
            uitools.setmodeblack(app)
        else:
            uitools.setmodewhite(app)

        self.curdir = os.getcwd()    
        self.Runtime = runtime.RunTime(self)
        self.AppRuntime = appruntime.RunTime(self,self.Runtime)
        self.l = QHBoxLayout()
        self.setLayout(self.l)

        self.yesno = False
        self.dialogbox = Dialog(self)
        self.msg = MessageBox(self)

        self.sidel = QVBoxLayout()
        self.sideg = QGroupBox()
        self.sideg.setStyleSheet("QGroupBox {background-color:"+uitools.colors["backgb"][self.mode]+";border-radius: 20} QScrollArea > QWidget > QWidget {background-color:"+uitools.colors["backgb"][self.mode]+"}")
        self.l.addWidget(self.sideg)
        self.sideg.setLayout(self.sidel)
        self.sideg.setFixedWidth(320)

        self.adbwidget = QWidget()
        self.adbl = QVBoxLayout()
        self.adbwidget.setLayout(self.adbl)
        self.adbscroll = QScrollArea()
        self.adbscroll.setMinimumWidth(500)
        self.adbscroll.setWidgetResizable(True)
        self.adbscroll.setFrameShape(QFrame.NoFrame)
        self.adbscroll.setWidget(self.adbwidget)
        self.adbg = QGroupBox()
        self.adbg.setStyleSheet("QGroupBox {background-color:"+uitools.colors["backgb"][self.mode]+";border-radius: 20} QScrollArea > QWidget > QWidget {background-color:"+uitools.colors["backgb"][self.mode]+"}")
        self.l.addWidget(self.adbg)
        self.adb = QVBoxLayout()
        self.adb.addWidget(self.adbscroll)
        self.adbg.setLayout(self.adb)

        self.fastbootwidget = QWidget()
        self.fastbootl = QVBoxLayout()
        self.fastbootwidget.setLayout(self.fastbootl)
        self.fastbootscroll = QScrollArea()
        self.fastbootscroll.setMinimumWidth(500)
        self.fastbootscroll.setWidgetResizable(True)
        self.fastbootscroll.setFrameShape(QFrame.NoFrame)
        self.fastbootscroll.setWidget(self.fastbootwidget)
        self.fastbootg = QGroupBox()
        self.fastbootg.setStyleSheet("QGroupBox {background-color: "+uitools.colors["backgb"][self.mode]+";border-radius: 20} QScrollArea > QWidget > QWidget {background-color: "+uitools.colors["backgb"][self.mode]+"}")
        self.l.addWidget(self.fastbootg)
        self.fastboot = QVBoxLayout()
        self.fastboot.addWidget(self.fastbootscroll)
        self.fastbootg.setLayout(self.fastboot)

        self.aboutwidget = QWidget()
        self.aboutl = QVBoxLayout()
        self.aboutwidget.setLayout(self.aboutl)
        self.aboutscroll = QScrollArea()
        self.aboutscroll.setMinimumWidth(500)
        self.aboutscroll.setWidgetResizable(True)
        self.aboutscroll.setFrameShape(QFrame.NoFrame)
        self.aboutscroll.setWidget(self.aboutwidget)
        self.aboutg = QGroupBox()
        self.aboutg.setStyleSheet("QGroupBox {background-color: "+uitools.colors["backgb"][self.mode]+";border-radius: 20} QScrollArea > QWidget > QWidget {background-color: "+uitools.colors["backgb"][self.mode]+"}")
        self.l.addWidget(self.aboutg)
        self.about = QVBoxLayout()
        self.about.addWidget(self.aboutscroll)
        self.aboutg.setLayout(self.about)

        self.guidewidget = QWidget()
        self.guidel = QVBoxLayout()
        self.guidewidget.setLayout(self.guidel)
        self.guidescroll = QScrollArea()
        self.guidescroll.setMinimumWidth(500)
        self.guidescroll.setWidgetResizable(True)
        self.guidescroll.setFrameShape(QFrame.NoFrame)
        self.guidescroll.setWidget(self.guidewidget)
        self.guideg = QGroupBox()
        self.guideg.setStyleSheet("QGroupBox {background-color: "+uitools.colors["backgb"][self.mode]+";border-radius: 20} QScrollArea > QWidget > QWidget {background-color: "+uitools.colors["backgb"][self.mode]+"}")
        self.l.addWidget(self.guideg)
        self.guide = QVBoxLayout()
        self.guide.addWidget(self.guidescroll)
        self.guideg.setLayout(self.guide)

        self.appswidget = QWidget()
        self.appsl = QVBoxLayout()
        self.appswidget.setLayout(self.appsl)
        self.appsscroll = QScrollArea()
        self.appsscroll.setMinimumWidth(500)
        self.appsscroll.setWidgetResizable(True)
        self.appsscroll.setFrameShape(QFrame.NoFrame)
        self.appsscroll.setWidget(self.appswidget)
        self.appsg = QGroupBox()
        self.appsg.setStyleSheet("QGroupBox {background-color: "+uitools.colors["backgb"][self.mode]+";border-radius: 20} QScrollArea > QWidget > QWidget {background-color: "+uitools.colors["backgb"][self.mode]+"} QPushButton { background-color: "+uitools.colors["line"][self.config["mode"]]+"; border-radius: 10; padding: 5} QPushButton::hover { background-color: #636363; border-radius: 10; padding: 5} QLineEdit { background-color: "+uitools.colors["line"][self.config["mode"]]+"; border-radius: 7; padding: 5}")
        self.l.addWidget(self.appsg)
        self.apps = QVBoxLayout()
        self.apps.addWidget(self.appsscroll)
        self.appsg.setLayout(self.apps)

        self.settingswidget = QWidget()
        self.settingsl = QVBoxLayout()
        self.settingswidget.setLayout(self.settingsl)
        self.settingsscroll = QScrollArea()
        self.settingsscroll.setMinimumWidth(500)
        self.settingsscroll.setWidgetResizable(True)
        self.settingsscroll.setFrameShape(QFrame.NoFrame)
        self.settingsscroll.setWidget(self.settingswidget)
        self.settingsg = QGroupBox()
        self.settingsg.setStyleSheet("QGroupBox {background-color: "+uitools.colors["backgb"][self.mode]+";border-radius: 20} QScrollArea > QWidget > QWidget {background-color: "+uitools.colors["backgb"][self.mode]+"} QPushButton { background-color: "+uitools.colors["line"][self.config["mode"]]+"; border-radius: 10; padding: 5} QPushButton::hover { background-color: #636363; border-radius: 10; padding: 5} QLineEdit { background-color: "+uitools.colors["line"][self.config["mode"]]+"; border-radius: 7; padding: 5}")
        self.l.addWidget(self.settingsg)
        self.settings = QVBoxLayout()
        self.settings.addWidget(self.settingsscroll)
        self.settingsg.setLayout(self.settings)

        self.updateswidget = QWidget()
        self.updatesl = QVBoxLayout()
        self.updateswidget.setLayout(self.updatesl)
        self.updatesscroll = QScrollArea()
        self.updatesscroll.setMinimumWidth(500)
        self.updatesscroll.setWidgetResizable(True)
        self.updatesscroll.setFrameShape(QFrame.NoFrame)
        self.updatesscroll.setWidget(self.updateswidget)
        self.updatesg = QGroupBox()
        self.updatesg.setStyleSheet("QGroupBox {background-color: "+uitools.colors["backgb"][self.mode]+";border-radius: 20} QScrollArea > QWidget > QWidget {background-color: "+uitools.colors["backgb"][self.mode]+"} QPushButton { background-color: "+uitools.colors["line"][self.config["mode"]]+"; border-radius: 10; padding: 5} QPushButton::hover { background-color: #636363; border-radius: 10; padding: 5} QLineEdit { background-color: "+uitools.colors["line"][self.config["mode"]]+"; border-radius: 7; padding: 5}")
        self.l.addWidget(self.updatesg)
        self.updates = QVBoxLayout()
        self.updatesg.setLayout(self.updates)
        
        self.gs = [self.fastbootg,self.adbg,self.aboutg,self.guideg,self.appsg,self.settingsg,self.updatesg]

        self.safs = sidewidget.SideWidget("AFS by @br0ke.tech","alone",os.path.join(curdir,"assets","icons","icon.png"),self.adbg,self,"afs")

        self.s1 = sidewidget.SideWidget("ADB Tools","top",os.path.join(curdir,"assets","sideicons","adb.png"),self.adbg,self,self.Runtime)
        self.s2 = sidewidget.SideWidget("Fastboot Tools","middle",os.path.join(curdir,"assets","sideicons","fastboot.png"),self.fastbootg,self,self.Runtime)
        self.s3 = sidewidget.SideWidget("App Management","bottom",os.path.join(curdir,"assets","sideicons","appmanagement.png"),self.appsg,self,self.Runtime)

        #self.s4 = sidewidget.SideWidget("Guides","top",os.path.join(curdir,"assets","sideicons","guides.png"),self.guideg,self,self.Runtime)
        self.s5 = sidewidget.SideWidget("About","alone",os.path.join(curdir,"assets","sideicons","info.png"),self.aboutg,self,self.Runtime)

        self.s6 = sidewidget.SideWidget("Settings","top",os.path.join(curdir,"assets","sideicons","settings.png"),self.settingsg,self,self.Runtime)
        self.s7 = sidewidget.SideWidget("Updates","bottom",os.path.join(curdir,"assets","sideicons","update.png"),self.updatesg,self,self.Runtime)

        self.sidel.addWidget(self.safs)
        self.sidel.addSpacerItem(QSpacerItem(0,12))
        self.sidel.addWidget(self.s1)
        self.sidel.addWidget(self.s2)
        self.sidel.addWidget(self.s3)
        self.sidel.addSpacerItem(QSpacerItem(0,12))
        #self.sidel.addWidget(self.s4)
        self.sidel.addWidget(self.s5)
        self.sidel.addSpacerItem(QSpacerItem(0,12))
        self.sidel.addWidget(self.s6)
        self.sidel.addWidget(self.s7)
        self.sidel.addStretch()
        self.sideg.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding)

        self.sidebars = [self.s1,self.s2,self.s3,self.s5,self.s6,self.s7]
        self.s1.switch(self.sidebars,self.gs,self.Runtime)

        self.t1 = adbtools.ADBTools("Install APK","top",os.path.join(curdir,"assets","adbicons","apk.png"),"Installs APKs to your device directly from your PC.\n - Risk: 1/10\n - Command: adb install "+'"[file]"'+"","adb install "+'"[file]"'+"",True,self,True,False,self.Runtime,True)
        self.t2 = adbtools.ADBTools("Sideload ROMs","bottom",os.path.join(curdir,"assets","adbicons","sideload.png"),"Sideload ROMs when booted into recovery, usually requires an unlocked bootloader.\n - Risk: 5/10\n - Command: adb sideload "+'"[file]"'+"","adb sideload "+'"[file]"'+"",True,self,True,False,self.Runtime,False)
        self.t3 = adbtools.ADBTools("Reboot to system","top",os.path.join(curdir,"assets","adbicons","reboot.png"),"Reboot to system.\n - Risk: 0/10\n - Command: adb reboot","adb reboot",False,self,True,False,self.Runtime,True)
        self.t4 = adbtools.ADBTools("Reboot to ...","bottom",os.path.join(curdir,"assets","adbicons","reboot.png"),"Reboot to a specified location \n - Risk: 1/10\n - Command: adb reboot [line]","adb reboot [line]",False,self,True,"Where to reboot?",self.Runtime,True)
        self.t5 = adbtools.ADBTools("Get logs","top",os.path.join(curdir,"assets","adbicons","logs.png"),"Get device's logs \n - Risk: 0/10\n - Command: adb logcat","adb logcat",False,self,True,False,self.Runtime,True)
        self.t6 = adbtools.ADBTools("Push file to device","middle",os.path.join(curdir,"assets","adbicons","file.png"),"Send a local file to your device's Downloads folder \n - Risk: 0/10\n - Command: adb push "+'"[file]"'+" sdcard/Download","adb push "+'"[file]"'+" sdcard/Download",True,self,True,False,self.Runtime,True)
        self.t7 = adbtools.ADBTools("Run a custom adb command","bottom",os.path.join(curdir,"assets","adbicons","adb.png"),"Run a custom adb command. Type it below without the word 'adb' \n - Risk: 5/10\n - Command: adb [line]","adb [line]",False,self,True,"Type your command here:",self.Runtime,False)

        self.tools = [self.t1,self.t2,self.t3,self.t4,self.t5,self.t6,self.t7]

        self.f2 = fastboottools.FastbootTools("Reboot to ...","middle",os.path.join(curdir,"assets","fasticons","reboot.png"),"Reboot to a specified location \n - Risk: 1/10\n - Command: fastboot reboot [line]","fastboot reboot [line]",False,"Where to reboot?",self,True,self.Runtime,True)
        self.f7 = fastboottools.FastbootTools("Get information","bottom",os.path.join(curdir,"assets","fasticons","info.png"),"Get device's information \n - Risk: 1/10\n - Command: fastboot getvar","fastboot getvar",False,False,self,True,self.Runtime,True)
        self.f1 = fastboottools.FastbootTools("Reboot","top",os.path.join(curdir,"assets","fasticons","reboot.png"),"Reboot to a specified location \n - Risk: 1/10\n - Command: fastboot reboot","fastboot reboot",False,False,self,True,self.Runtime,True)
        self.f3 = fastboottools.FastbootTools("Flash to partition","top",os.path.join(curdir,"assets","fasticons","flash.png"),"Flash a file to a specified partition. Esnure that the file you are flashing is compatible with your device\n - Risk: 7/10\n - Command: fastboot flash [line] "+'"[file]"'+"","fastboot flash [line] "+'"[file]"'+"",True,"Where to flash?",self,True,self.Runtime,False)
        self.f4 = fastboottools.FastbootTools("Erase partition","bottom",os.path.join(curdir,"assets","fasticons","erase.png"),"Erase a specified partition. Make sure you have backups and know what is the partition that you are erasing \n - Risk: 6/10\n - Command: fastboot erase [line]","fastboot erase [line]",False,"What to erase?",self,True,self.Runtime,False)
        self.f5 = fastboottools.FastbootTools("Unlock bootloader","top",os.path.join(curdir,"assets","fasticons","unlock.png"),"Unlocks your device's bootloader. Doesn't work on most phone brands, like Samsung or Xiaomi. Erases userdata \n - Risk: 5/10\n - Command: fastboot flashing unlock","fastboot flashing unlock",False,False,self,True,self.Runtime,False)
        self.f6 = fastboottools.FastbootTools("Lock bootloader","bottom",os.path.join(curdir,"assets","fasticons","lock.png"),"Locks your device's bootloader. Doesn't work on most phone brands, like Samsung or Xiaomi. Erases userdata \n - Risk: 4/10\n - Command: fastboot flashing lock","fastboot flashing lock",False,False,self,True,self.Runtime,False)
        self.f8 = fastboottools.FastbootTools("Boot image temporarily","middle",os.path.join(curdir,"assets","fasticons","boot.png"),"Boot an image temporarily. Esnure that the file you are flashing is compatible with your device\n - Risk: 4/10\n - Command: fastboot boot "+'"[file]"'+"","fastboot boot "+'"[file]"'+"",True,False,self,True,self.Runtime,False)
        self.fastools = [self.f1,self.f2,self.f3,self.f4,self.f5,self.f6,self.f7,self.f8]

        self.i1 = abouttiles.AboutTile("Android Flashing Shortcuts Version","top",os.path.join(curdir,"assets","icons","afs.png"),version,False,self)
        self.i2 = abouttiles.AboutTile("AFS location","middle",os.path.join(curdir,"assets","icons","afs.png"),curdir,True,self)
        self.i3 = abouttiles.AboutTile("GitHub repository","bottom",os.path.join(curdir,"assets","icons","github.png"),"https://www.github.com/broke-tech/android-flashing-shortcuts",True,self)

        self.i4 = abouttiles.AboutTile("My TikTok (Broke Tech)","top",os.path.join(curdir,"assets","icons","tiktok.png"),"https://www.tiktok.com/@br0ke.tech",True,self)
        self.i5 = abouttiles.AboutTile("My Discord server","bottom",os.path.join(curdir,"assets","icons","discord.png"),"https://www.discord.gg/FRbg2Vzq7X",True,self)

        """
        self.guides = []
        self.guideslabel = QLabel("These guides are AI generated by Claude, so please be careful when following those. I really don't want to use AI on my projects but I only use these guides as placeholders before writing my own. Anyways, I'm not responsible for any damages, blah blah, you get the point. THE RISK IS YOURS!\n")
        self.guideslabel.setWordWrap(True)
        self.guidel.addWidget(self.guideslabel)
        with open(os.path.join(curdir,"assets","guides.json"),"r") as file:
            self.guidesfile = json.load(file)
        for i in self.guidesfile:
            self.guidel.addWidget(QLabel(self.guidesfile[i]["brand"]))
            c = 0
            for a in range(len(self.guidesfile[i]["guides"])):
                c = c+1
                if c == 1:
                    p = "top"
                elif c == len(self.guidesfile[i]["guides"]):
                    p = "bottom"
                else:
                    p = "middle"
                t = guidetile.GuideTile(self.guidesfile[i]["guides"][a]["name"],p,os.path.join(curdir,"assets","sideicons","guides.png"),self.guidesfile[i]["guides"][a]["how"],self)
                self.guidel.addWidget(t)
                self.guides.append(t)
            self.guidel.addSpacerItem(QSpacerItem(0,12))
        self.guidel.addStretch()
        """

        self.aboutl.addWidget(self.i1)
        self.aboutl.addWidget(self.i2)
        self.aboutl.addWidget(self.i3)
        self.aboutl.addSpacerItem(QSpacerItem(0,12))
        self.aboutl.addWidget(self.i4)
        self.aboutl.addWidget(self.i5)
        self.aboutl.addStretch()

        self.adbl.addWidget(self.t1)
        self.adbl.addWidget(self.t2)
        self.adbl.addSpacerItem(QSpacerItem(0,12))
        self.adbl.addWidget(self.t3)
        self.adbl.addWidget(self.t4)
        self.adbl.addSpacerItem(QSpacerItem(0,12))
        self.adbl.addWidget(self.t5)
        self.adbl.addWidget(self.t6)
        self.adbl.addWidget(self.t7)
        self.adbl.addStretch()

        self.fastbootl.addWidget(self.f1)
        self.fastbootl.addWidget(self.f2)
        self.fastbootl.addWidget(self.f7)
        self.fastbootl.addSpacerItem(QSpacerItem(0,12))
        self.fastbootl.addWidget(self.f3)
        self.fastbootl.addWidget(self.f8)
        self.fastbootl.addWidget(self.f4)
        self.fastbootl.addSpacerItem(QSpacerItem(0,12))
        self.fastbootl.addWidget(self.f5)
        self.fastbootl.addWidget(self.f6)
        self.fastbootl.addStretch()

        self.appsearch = QHBoxLayout()
        self.apps.addLayout(self.appsearch)
        self.appsline = QLineEdit()
        self.appsline.setPlaceholderText("Search quota (leave empty to show all)")
        self.appsbut = QPushButton("Refresh")
        self.appsbut.clicked.connect(lambda:self.s3.switch(self.sidebars,self.gs,self.Runtime))
        self.appsearch.addWidget(self.appsline)
        self.appsearch.addWidget(self.appsbut)
        self.applogs = QTextEdit()
        self.applogs.setReadOnly(True)
        self.applogs.setMaximumHeight(120)
        self.apps.addWidget(QLabel("LOGS:"))
        self.apps.addWidget(self.applogs)

        self.settingsl.addWidget(appearancesetting.AppearanceSettings("Appearance Settings" ,"top", os.path.join(curdir,"assets","icons","brush.png"),self))
        self.safetys =  safetysetting.SafetySettings("Safety Settings" ,"bottom", os.path.join(curdir,"assets","icons","security.png"),self)
        self.settingsl.addWidget(self.safetys)
        self.settingsl.addStretch()

        self.updatetext = QLabel("Automatic updates are\ndisabled.",alignment=Qt.AlignHCenter)
        self.updatetext.setWordWrap(True)
        self.updatetext.setStyleSheet("font-size: 25px")
        self.updates.addWidget(self.updatetext,alignment=Qt.AlignHCenter)
        self.updates.addWidget(self.updatesscroll)

        self.updatetextdesc = QLabel("",alignment=Qt.AlignHCenter)
        self.updatetextdesc.setWordWrap(True)
        self.updatetextdesc.setStyleSheet("font-size: 17px")
        self.updatesl.addWidget(self.updatetextdesc,alignment=Qt.AlignHCenter|Qt.AlignVCenter)

        self.updatebut = QPushButton("Check for updates")
        self.githubbut = QPushButton("Get the latest version on GitHub")
        self.githubbut.clicked.connect(lambda:opensite("https://www.github.com/broke-tech/android-flashing-shortcuts"))
        self.updates.addWidget(self.updatebut,alignment=Qt.AlignHCenter)
        self.updatebut.clicked.connect(self.checkforupdates)
        self.updates.addWidget(self.githubbut,alignment=Qt.AlignHCenter)


    def detectapps(self):
        print("end")
        print(self.AppRuntime.disabledapps)
        uitools.clear_layout(self.appsl)
        self.Runtime.isRunning = False
        if len(self.AppRuntime.installedapps) > 0: self.appsl.addWidget(QLabel("3rd Party apps"))
        c = 0
        for a in self.AppRuntime.installedapps:
            c = c+1
            if c == 1:
                p = "top"
            elif c == len(self.AppRuntime.installedapps):
                p = "bottom"
            else:
                p = "middle"

            if self.appsline.text() != "":
                if self.appsline.text().lower() in a.lower():
                    self.appsl.addWidget(apptile.AppTile(a,"3",self,self.Runtime,p))
            else:
                self.appsl.addWidget(apptile.AppTile(a,"3",self,self.Runtime,p))

        if len(self.AppRuntime.systemapps) > 0: self.appsl.addWidget(QLabel("\nSystem apps"))
        c = 0
        for a in self.AppRuntime.systemapps:
            c = c+1
            if c == 1:
                p = "top"
            elif c == len(self.AppRuntime.systemapps):
                p = "bottom"
            else:
                p = "middle"
            if self.appsline.text() != "":
                if self.appsline.text().lower() in a.lower():
                    self.appsl.addWidget(apptile.AppTile(a,"s",self,self.Runtime,p))
            else:
                self.appsl.addWidget(apptile.AppTile(a,"s",self,self.Runtime,p))

        if len(self.AppRuntime.disabledapps) > 0: self.appsl.addWidget(QLabel("\nDisabled apps"))
        c = 0
        for a in self.AppRuntime.disabledapps:
            c = c+1
            if c == 1:
                p = "top"
            elif c == len(self.AppRuntime.disabledapps):
                p = "bottom"
            else:
                p = "middle"
            if self.appsline.text() != "":
                if self.appsline.text().lower() in a.lower():
                    self.appsl.addWidget(apptile.AppTile(a,"d",self,self.Runtime,p))
            else:
                self.appsl.addWidget(apptile.AppTile(a,"d",self,self.Runtime,p))

        if len(self.AppRuntime.systemapps) == 0 and len(self.AppRuntime.disabledapps) == 0 and len(self.AppRuntime.installedapps) == 0:
            self.msg.showup("No apps found!")
        else:
            print("Loaded apps successfully!")

    def checkforupdates(self):
        self.updatetext.setText("Checking for updates\nPlease wait...")
        try:
            releasenotesurl = "https://raw.githubusercontent.com/broke-tech/android-flashing-shortcuts/refs/heads/main/app/assets/newreleases.json"
            r = requests.get(releasenotesurl)
            with open(curdir+r"\assets\newreleases.json","w") as file:
                file.write(r.text)
        except:
            with open(curdir+r"\assets\newreleases.json","w") as file:
                json.dump({"latest":version,"releases":{version:{"name":version,"date":"???","notes":"No internet connection!"}}},file)

        with open(curdir+r"\assets\newreleases.json","r") as file:
            releasenotes = json.load(file)

        if releasenotes["latest"] != version:
            self.updatetext.setText(f"Update available! (v{releasenotes["latest"]})\nPublish date: {releasenotes["releases"][releasenotes["latest"]]["date"]}")
            self.updatetextdesc.setText("RELEASE NOTES:\n"+releasenotes["releases"][releasenotes["latest"]]["notes"])
            self.s7.ft.setText("Updates"+" •")
        else:
            try:
                a = releasenotes["releases"][version]["notes"]
                self.updatetext.setText(f"You are running the latest version of AFS! (v{version})\nPublish date: {releasenotes["releases"][version]["date"]}")
                self.updatetextdesc.setText("RELEASE NOTES:\n"+releasenotes["releases"][version]["notes"])
            except:
                self.updatetext.setText("YOU ARE RUNNING AN UNKNOWN OR\nUNRELEASED VERSION OF AFS!")
                self.updatetextdesc.setText("Please contact me or install the official\nrelease on GitHub.")

class Dialog(QDialog):
    def __init__(self,parentv):
        super().__init__()
        self.parentv = parentv
        self.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.setWindowIcon(QIcon(os.path.join(curdir,"assets","icons","icon.ico")))
        self.setWindowTitle("AFS - Dialog")

        if self.parentv.mode == "dark":
            uitools.setmodeblack(self)
        else:
            uitools.setmodewhite(self)
        self.l = QVBoxLayout()
        self.setLayout(self.l)

        self.g = QGroupBox()
        self.gl = QVBoxLayout()
        self.g.setLayout(self.gl)
        self.l.addWidget(self.g)

        self.p = QLabel()
        self.i = QPixmap(os.path.join(curdir,"assets","icons","warning.png")).scaled(50,50,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.p.setPixmap(self.i)
        self.l = QHBoxLayout()
        self.gl.addWidget(self.p,alignment=Qt.AlignHCenter)
        self.gl.addStretch()

        self.setWindowTitle("AFS - Warning Dialog")
        self.setStyleSheet("QGroupBox{ border-radius: 20; background-color: "+uitools.colors["backgb"][self.parentv.mode]+";} QPushButton { background-color: "+uitools.colors["line"][self.parentv.config["mode"]]+"; border-radius: 10; padding: 5} QPushButton::hover { background-color: #636363; border-radius: 10; padding: 5} QLineEdit { background-color: "+uitools.colors["line"][self.parentv.config["mode"]]+"; border-radius: 7; padding: 5}")
        self.label = QLabel("Message",alignment=Qt.AlignHCenter)
        self.label.setWordWrap(True)
        self.yesbut  = QPushButton("Yes")
        self.yesbut.clicked.connect(lambda: self.setvalue(True))
        self.nobut  = QPushButton("No")
        self.nobut.clicked.connect(lambda: self.setvalue(False))
        self.nobut.setStyleSheet("QPushButton { color: #ffffff; background-color: #880808; border-radius: 10; padding: 5} QPushButton::hover { color: #ffffff; background-color: #AA4A44; border-radius: 10; padding: 5}")
        self.gl.addWidget(self.label,alignment=Qt.AlignHCenter)
        self.gl.addStretch()

        self.gl.addWidget(self.nobut)
        self.gl.addWidget(self.yesbut)

    def showup(self,message):
        self.label.setText(message)
        self.parentv.yesno = False
        self.resize(500,500)
        self.exec()

    def setvalue(self,value):
        self.parentv.yesno = value
        self.hide()

class MessageBox(QDialog):
    def __init__(self,parentv):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(curdir,"assets","icons","icon.ico")))
        self.setWindowTitle("AFS - Message")

        self.parentv = parentv
        self.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)

        if self.parentv.mode == "dark":
            uitools.setmodeblack(self)
        else:
            uitools.setmodewhite(self)
        self.l = QVBoxLayout()
        self.setLayout(self.l)

        self.g = QGroupBox()
        self.gl = QVBoxLayout()
        self.g.setLayout(self.gl)
        self.l.addWidget(self.g)

        self.p = QLabel()
        self.i = QPixmap(os.path.join(curdir,"assets","icons","warning.png")).scaled(50,50,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.p.setPixmap(self.i)
        self.l = QHBoxLayout()
        self.gl.addWidget(self.p,alignment=Qt.AlignHCenter)
        self.gl.addStretch()

        self.setWindowTitle("AFS - Message")
        self.setStyleSheet("QWidget { border-radius: 20px} QGroupBox{ border-radius: 20px; background-color: "+uitools.colors["backgb"][self.parentv.mode]+";} QPushButton { background-color: "+uitools.colors["line"][self.parentv.config["mode"]]+"; border-radius: 10; padding: 5} QPushButton::hover { background-color: #636363; border-radius: 10; padding: 5} QLineEdit { background-color: "+uitools.colors["line"][self.parentv.config["mode"]]+"; border-radius: 7; padding: 5}")
        self.label = QLabel("Message",alignment=Qt.AlignHCenter)
        self.yesbut  = QPushButton("Ok")
        self.yesbut.clicked.connect(lambda: self.hide())
        self.gl.addWidget(self.label,alignment=Qt.AlignHCenter)
        self.gl.addStretch()
        self.gl.addWidget(self.yesbut)

    def showup(self,message):
        if "[startmsg]" in message:
            self.label.setWordWrap(True)
        else:
            self.label.setWordWrap(False)
        self.label.setText(message)
        self.exec()

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        
        uitools.setfont(os.path.join(curdir,"assets","font","main.ttf"),app,app)
        w = App()
        if w.config["startd"] == True:
            w.msg.showup("WARNING! PLEASE READ!\nAndroid Flashing Shortcuts is a very useful but risky tool. Wrong usage by you can result in data loss and damages to your device. So my warning is DON'T use this tool if you don't know what you are doing. If you still want to use my tool without the risks you can enable Safe mode in settings. You can also hide this warning in settings.\n\nI AM NOT RESPONSIBLE FOR ANY DAMAGES CAUSED TO YOUR DEVICE!\n\nMESSAGE FOR TESTERS: This is not the final version. I want to fix any bugs that you encounter and add some finishing touches later. For now, if you notice anything strange, please inform me. [startmsg]")

        s = start.Start(w, w.Runtime)
        if w.config["first"] == True:
            s.exec()
        w.show()
        app.setStyle("Fushion")
        app.exec()
    except FileNotFoundError:
        QMessageBox.critical(None,"Error","Some of AFS's required files could not be found. Please reinstall AFS.\n\nNote: If you launched AFS via Windows Search or Spotlight, try opening the application directly from its installation folder.")
