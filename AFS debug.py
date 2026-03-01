from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QListWidgetItem, QDialog, QFrame, QScrollArea, QFileDialog, QComboBox, QCheckBox, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QPushButton, QLineEdit, QTextEdit, QListWidget
from PyQt5.QtGui import QPixmap, QIcon, QFont, QFontDatabase
import os
import json
import requests
from webbrowser import open as opensite

version = "2.0"

def adb_reboot():    
    if worker.state() != QProcess.Running:
        terminal.clear()
        if adbreboot.combobox.currentText() == "system":
            worker.start(adb, ["reboot"])
        else:
            worker.start(adb, ["reboot", adbreboot.combobox.currentText()])
    else:
        messagebox("Another process is running!")

def fastboot_devices():
    if worker.state() != QProcess.Running:
        terminal.clear()
        worker.start(fastbootdir, ["devices"])
    else:
        messagebox("Another process is running!")

def fastboot_getvar():
    if worker.state() != QProcess.Running:
        terminal.clear()
        worker.start(fastbootdir, ["getvar","all"])
    else:
        messagebox("Another process is running!")

def fastboot_reboot():    
    if worker.state() != QProcess.Running:
        terminal.clear()
        if reboot.combobox.currentText() == "system":
            worker.start(fastbootdir, ["reboot"])
        else:
            worker.start(fastbootdir, ["reboot", reboot.combobox.currentText()])
    else:
        messagebox("Another process is running!")

def adb_install():
    if worker.state() != QProcess.Running:
        try:
            terminal.clear()
            file = os.path.join(workdir,window.selectedfile)
            if os.path.exists(file):
                pass
            else:
                messagebox("File does not exist.")
                return False
            dialog("WARNING",adbinstall.command+window.selectedfile, "YES YES YES","Like hell I will (no)")
            if window.yesno:
                worker.start(adb, ["install", file])
            else:
                pass
        except:
            messagebox("Unknown error")
    else: 
        messagebox("Another process is running!")

def adb_sideload():
    if worker.state() != QProcess.Running:
        try:
            terminal.clear()
            file = os.path.join(workdir,window.selectedfile)
            if os.path.exists(file):
                pass
            else:
                messagebox("File does not exist.")
                return False
            dialog("WARNING",adbsideload.command+window.selectedfile, "YES YES YES","Like hell I will (no)")
            if window.yesno:
                worker.start(adb, ["sideload", file])
            else:
                pass
        except:
            messagebox("Unknown error")
    else: 
        messagebox("Another process is running!")

def flashing_unlock():
    if worker.state() != QProcess.Running:
        terminal.clear()
        dialog("WARNING",unlockblnew.command, "YES YES YES","Like hell I will (no)")
        if window.yesno:
            worker.start(fastbootdir, ["flashing", "unlock"])
        else:
            pass
    else: 
        messagebox("Another process is running!")

def flashing_lock():
    if worker.state() != QProcess.Running:
        terminal.clear()
        dialog("WARNING",relockblnew.command, "YES YES YES","Like hell I will (no)")
        if window.yesno:
            worker.start(fastbootdir, ["flashing", "lock"])
        else:
            pass
    else: 
        messagebox("Another process is running!")

def oem_unlock():
    if worker.state() != QProcess.Running:
        terminal.clear()
        dialog("WARNING",unlockblold.command, "YES YES YES","Like hell I will (no)")
        if window.yesno:
            worker.start(fastbootdir, ["oem", "unlock"])
        else:
            pass
    else: 
        messagebox("Another process is running!")
    
def oem_lock():
    if worker.state() != QProcess.Running:
        terminal.clear()
        dialog("WARNING",relockblold.command, "YES YES YES","Like hell I will (no)")
        if window.yesno:
            worker.start(fastbootdir, ["oem", "lock"])
        else:
            pass
    else: 
        messagebox("Another process is running!")

def magisk_sideload():
    if worker.state() != QProcess.Running:
        if os.path.exists(magiskdir+"."+magisk.combobox.currentText()):
            try:
                terminal.clear()
                dialog("WARNING",magisk.command, "YES YES YES","Like hell I will (no)")
                if window.yesno:
                    worker.start(adb, ["sideload", magiskdir+"."+magisk.combobox.currentText()])
                else:
                    pass
            except:
                messagebox("Error")
        else:
            messagebox(r"Magisk file not found inside /magisk.")
    else: 
        messagebox("Another process is running!")


def boot_image():
    if worker.state() != QProcess.Running:
        try:
            file = os.path.join(workdir,window.selectedfile)
            if os.path.exists(file):
                pass
            else:
                messagebox("File does not exist.")
                return False
            terminal.clear()
            dialog("WARNING",bootimg.command+window.selectedfile, "YES YES YES","Like hell I will (no)")
            if window.yesno:
                worker.start(fastbootdir, ["boot", file])
            else:
                pass
        except:
            messagebox("Unknown error")
    else:
        messagebox("Another process is running!")
        
def flash_image():
    if worker.state() != QProcess.Running:
        try:
            file = os.path.join(workdir,window.selectedfile)
            if os.path.exists(file):
                pass
            else:
                messagebox("File does not exist.")
                return False
            if len(flash.lineedit.text()) != 0:
                pass
            else:
                messagebox("Enter a partition.")
                return False
            terminal.clear()
            dialog("WARNING",flash.command+window.selectedfile, "YES YES YES","Like hell I will (no)")
            if window.yesno:
                worker.start(fastbootdir, ["flash", flash.lineedit.text(), file])
            else:
                pass
        except:
            messagebox("Unknown error")
    else:
        messagebox("Another process is running!")

def vbmeta():
    if worker.state() != QProcess.Running:
        try:
            file = os.path.join(workdir,window.selectedfile)
            if os.path.exists(file):
                pass
            else:
                messagebox("File does not exist.")
                return False
            terminal.clear()
            dialog("WARNING",flashvbmeta_disable.command, "YES YES YES","Like hell I will (no)")
            if window.yesno:
                worker.start(fastbootdir, ["flash","--disable-verity","--disable-verification","vbmeta",file])
            else:
                pass
        except:
            messagebox("Unknown error")
    else:
        messagebox("Another process is running!")

def erase_partition():
    if worker.state() != QProcess.Running:
        if len(erase.lineedit.text()) != 0:
            pass
        else:
            messagebox("Enter a partition.")
            return False
        terminal.clear()
        dialog("WARNING",erase.command, "YES YES YES","Like hell I will (no)")
        if window.yesno:
            worker.start(fastbootdir, ["erase", erase.lineedit.text()])
        else:
            pass 
    else:
        messagebox("Another process is running!")

def erase_userdata():
    if worker.state() != QProcess.Running:
        terminal.clear()
        dialog("WARNING",formatuserdata.command, "YES YES YES","Like hell I will (no)")
        if window.yesno:
            worker.start(fastbootdir, ["erase", "userdata"])
        else:
            pass
    else:
        messagebox("Another process is running!")

app = QApplication([])
window = QWidget()
window.setWindowTitle("AFS - Android Flashing Shortcuts")
window.setWindowIcon(QIcon(os.getcwd()+r"\assets\icon.png"))
extentions = [".zip",".img"]
window.yesno = False
window.selectedfile = None
window.firsttitle = True

def colorsbut(but, before, after):
    but.setStyleSheet(
        "QPushButton {"
            f"background-color: {before};"
            "color: #000000;"
            "padding: 10px;"
            "padding-top: 6px;"
            "padding-bottom: 6px;"
            "border-radius: 9px;"
            "}"
        "QPushButton:hover {"
            f"background-color: {after};"
            "color: #000000;"
            "padding: 1px;"
            "border-radius: 9px;"
            "}"
    )
#Worker
def update():
    out = worker.readAllStandardOutput().data().decode().strip()
    if out:
        terminal.append(out)

    err = worker.readAllStandardError().data().decode().strip()
    if err:
        terminal.append(err)

def kill():
    terminal.setText("")
    worker.kill()

worker = QProcess()
worker.setWorkingDirectory(os.getcwd()+r"/platform-tools")
worker.readyReadStandardOutput.connect(update)
worker.finished.connect(update)
worker.errorOccurred.connect(update)
worker.readyReadStandardError.connect(update)


def messagebox(message):
    msg = QMessageBox()
    msg.setWindowTitle("AFS - Message")
    msg.setText(message)
    msg.exec()

def setsize(widget,size):
    widget.setStyleSheet(f"font-size: {size}px;")

def semititle(title,layout):
    label = QLabel(title)
    setsize(label,30)
    if not window.firsttitle:
        layout.addWidget(QLabel())
    layout.addWidget(label,alignment=Qt.AlignLeft)
    window.firsttitle = False

def unavailable():
    messagebox("This command is not available yet, I recommend you run it directly from cmd")

class Commands():
    def __init__(self,name=" ",butname=" ",function=None,combo=False,items=list(),command=' ',linetext=""):
        self.name = name
        self.butname = butname
        self.function = function
        self.combo = combo
        self.items = items
        self.command = command
        self.linetext = linetext
        self.layout = QHBoxLayout()
        self.title = QLabel(self.name)
        self.layout.addWidget(self.title)
        self.but = QPushButton(self.butname)
        self.but.setStyleSheet(
            "QPushButton {"
                "background-color: #2451CC;"
                "color: #ffffff;"
                "padding: 10px;"
                "padding-top: 6px;"
                "padding-bottom: 6px;"
                "border-radius: 8px;"
                "}"
            "QPushButton:hover {"
                "background-color: #94AAE6;"
                "color: #ffffff;"
                "padding: 1px;"
                "border-radius: 8px;"
                "}"
        )
        if self.combo:
            self.combobox = QComboBox()
            self.combobox.addItems(items)
            self.layout.addWidget(self.combobox)

        if len(self.linetext) != 0:
            self.lineedit = QLineEdit()
            self.lineedit.setFixedWidth(250)
            self.lineedit.setPlaceholderText(linetext)
            self.layout.addWidget(self.lineedit)
            self.lineedit.setStyleSheet("border-radius: 8px; padding: 4;")
        self.layout.addStretch()
        self.layout.addWidget(self.but)
        self.but.clicked.connect(self.function)
        toolsLayout.addLayout(self.layout)

def chooseWorkdir():
    global workdir #calling the global variable
    global filenames
    zipslist.clear()
    workdir = QFileDialog.getExistingDirectory()
    try:
        zipsdir.setText(workdir)
        filenames = os.listdir(workdir)
        addfiles()
    except:
        messagebox("Select a directory fisrt!")

def chooseDefaultdir():
    global workdir #calling the global variable
    global filenames
    zipslist.clear()
    workdir = QFileDialog.getExistingDirectory()
    try:
        if os.path.exists(workdir):
            defaultdir.setText(workdir)
            window.config["defaultdir"] = workdir
            with open(window.configdir,"w") as file:
                json.dump(window.config,file)
        else:
            messagebox("Select a vaild directory fisrt!")
    except:
        messagebox("Select a directory fisrt!")

def accept():
    window.yesno = True
    window.dialogbox.hide()

def reject():
    window.yesno = False
    window.dialogbox.hide()

def dialog(title,command,yestext,notext):
    window.dialogbox = QDialog()
    window.dialogbox.setWindowTitle(title)
    butts = QHBoxLayout()
    accepted = QPushButton(yestext)
    rejected = QPushButton(notext)
    accepted.clicked.connect(accept)
    rejected.clicked.connect(reject)
    butts.addStretch()
    butts.addWidget(accepted)
    butts.addWidget(rejected)
    layout = QVBoxLayout()
    message = QLabel(f"Are you sure you want to run the command '{command}'? This is your own risk btw!")
    layout.addWidget(message)
    layout.addLayout(butts)
    window.dialogbox.setLayout(layout)
    window.dialogbox.exec()

def addfiles():
    zipslist.clear()
    zips = []
    img = []
    apk = []
    for item in filenames:
        if item.endswith(".zip"):
            zips.append(item)
        elif item.endswith(".img"):
            img.append(item)
        elif item.endswith(".apk"):
            apk.append(item)
    if len(zips) != 0:
        addHeader("----Zip Files----")
        zipslist.addItems(zips)
    if len(img) != 0:
        addHeader(" ")
        addHeader("----Img Files----")
        zipslist.addItems(img)    
    if len(apk) != 0:
        addHeader(" ")
        addHeader("----Apk Files----")
        zipslist.addItems(apk)

def addHeader(text):
    item = QListWidgetItem(text)
    item.setFlags(Qt.NoItemFlags)
    zipslist.addItem(item)

def dialogchange():
    if window.config["dialog"] == "True":
        dialogstart.setChecked(True)
    elif window.config["dialog"] == "False":
        dialogstart.setChecked(False)
    
def dialogclicked():
    if dialogstart.isChecked():
        window.config["dialog"] = "True"
    elif not dialogstart.isChecked():
        window.config["dialog"] = "False"
    with open(window.configdir,"w") as file:
        json.dump(window.config,file)

def defaultdirectorycheck():
    global defaultdirectory
    global filenames
    global workdir
    defaultdirectory = window.config["defaultdir"]
    if defaultdirectory != 'None':
        if os.path.exists(defaultdirectory):
            try:
                zipsdir.setText(defaultdirectory)
                defaultdir.setText(defaultdirectory)
                filenames = os.listdir(defaultdirectory)
                addfiles()
                workdir = defaultdirectory
            except:
                messagebox("Unknown error!")
                workdir = None
                window.config["defaultdir"] = "None"
                with open(window.configdir,"w") as file:
                    json.dump(window.config,file)
        elif not os.path.exists(defaultdirectory):
            messagebox("Your default directory was deleted.")
            window.config["defaultdir"] = "None"
            with open(window.configdir,"w") as file:
                json.dump(window.config,file)

def filechange():
    window.selectedfile = zipslist.currentItem().text()
    if len(window.selectedfile) <= 20:
        ziptitle.setText(f"Files (Selected: {window.selectedfile})")
    else:
        ziptitle.setText(f"Files (Selected: {window.selectedfile[0:20]+"..."})")

main = QVBoxLayout()
titleLayout = QHBoxLayout()
logolayout = QVBoxLayout()
titleLayout.addLayout(logolayout)

def openoptions():
    windowopts.show()

def githubopensite():
    opensite("https://github.com/broke-tech/android-flashing-shortcuts")

def ttopensite():
    opensite("https://tiktok.com/@br0ke.tech")

def openreleasenotes():
    windownotes.show()

def openupdates():
    windowupdate.show()

title = QLabel("Android Flashing Shortcuts")
setsize(title,20)
logo = QLabel()
logo.setPixmap(QPixmap(os.getcwd()+r"\assets\logo.png").scaled(400,100,Qt.KeepAspectRatio,Qt.SmoothTransformation))
githubpagebut = QPushButton("GitHub page")
githubpagebut.setIcon(QIcon(os.getcwd()+r"\assets\github.png"))
githubpagebut.clicked.connect(githubopensite)
tiktokpagebut = QPushButton("TikTok page")
tiktokpagebut.setIcon(QIcon(os.getcwd()+r"\assets\tiktok.png"))
optionsbut = QPushButton("Options")
optionsbut.clicked.connect(openoptions)
optionsbut.setIcon(QIcon(os.getcwd()+r"\assets\options.png"))
releasenotesbut = QPushButton("Release Notes")
releasenotesbut.setIcon(QIcon(os.getcwd()+r"\assets\info.png"))
releasenotesbut.clicked.connect(openreleasenotes)
for i in [tiktokpagebut,githubpagebut,optionsbut,releasenotesbut]:
    colorsbut(i,"#00000000","#3c3c3c37")

tiktokpagebut.clicked.connect(ttopensite)
logolayout.addWidget(logo, alignment=Qt.AlignHCenter)
logolayout.addWidget(title, alignment=Qt.AlignHCenter)

titleLayout.addStretch()
titleLayout.addWidget(QLabel("     "), alignment=Qt.AlignVCenter)
titleLayout.addWidget(optionsbut, alignment=Qt.AlignVCenter)
titleLayout.addWidget(tiktokpagebut, alignment=Qt.AlignVCenter)
titleLayout.addWidget(githubpagebut, alignment=Qt.AlignVCenter)
main.addLayout(titleLayout)
main.addWidget(QLabel())

sidesLayout = QHBoxLayout()
leftLayout = QVBoxLayout()
rightLayout = QVBoxLayout()
sidesLayout.addLayout(leftLayout)
sidesLayout.addLayout(rightLayout)
main.addLayout(sidesLayout)

dirLayout = QHBoxLayout()
zipsdir = QLineEdit()
zipsdir.setStyleSheet("border-radius: 8px; padding: 4;")
zipsdir.setReadOnly(True)
loaddir = QPushButton("Select folder")
colorsbut(loaddir,"#FFBB00","#fcdf4c")
loaddir.clicked.connect(chooseWorkdir)
dirLayout.addWidget(zipsdir)
dirLayout.addWidget(loaddir)
zipslist = QListWidget()
zipslist.currentItemChanged.connect(filechange)
ziptitle = QLabel(f"Files (Selected: {window.selectedfile})")

zipslist.setFixedWidth(410)
zipsdir.setFixedWidth(280)
loaddir.setFixedWidth(120)

leftLayout.addLayout(dirLayout)
leftLayout.addWidget(ziptitle)
leftLayout.addWidget(zipslist)

righttitle = QLabel('TOOLS')
setsize(righttitle,20)
rightLayout.addWidget(righttitle,alignment=Qt.AlignLeft)

scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)
scroll_area.setFrameShape(QFrame.NoFrame)

scrollwidget = QWidget()
toolsLayout = QVBoxLayout()
scrollwidget.setLayout(toolsLayout)
scroll_area.setWidget(scrollwidget)
rightLayout.addWidget(scroll_area)

#TOOLS
semititle("---USB debugging---",toolsLayout)
adbreboot = Commands("ADB reboot to","Reboot",adb_reboot,True,["system","recovery","bootloader","fastboot"],"adb reboot [selected partition]","")
adbinstall = Commands("Install APK","Install",adb_install,False,[],f"adb install ","")

semititle("---Sideloading and flashing---",toolsLayout)
adbsideload = Commands("ADB sideload","Sideload",adb_sideload,False,[],f'adb sideload ',"")
flash = Commands("Flash image to partition","Flash",flash_image,False,["boot","recovery","system","vendor","vbmeta","userdata","super"],f"fastboot flash [selected partition] ","Type valid partition name")
flashvbmeta_disable = Commands("Flash vbmeta (disable verity/verification)","Flash vbmeta",vbmeta,False,[],f"fastboot flash vbmeta --disable-verity --disable-verification ")

semititle("---Get information---",toolsLayout)
fastbootdevices = Commands("Detect fastboot device","Devices",fastboot_devices,False,[],"fastboot devices","")
getvars = Commands("Get device info","Info",fastboot_getvar,False,[],"fastboot getvar all","")

semititle("---Booting and rebooting---",toolsLayout)
reboot = Commands("Reboot to","Reboot",fastboot_reboot,True,["system","recovery","bootloader","fastboot"],"fastboot reboot [selected partition]","")
bootimg = Commands("Boot image temporarily","Boot",boot_image,False,[],f"fastboot boot ","")

semititle("---Erasing---",toolsLayout)
erase = Commands("Erase partition","Erase",erase_partition,False,["cache","metadata","product","boot","recovery","system","vendor","vbmeta","super"],"fastboot erase [selected partition]","Type valid partition name")
formatuserdata = Commands("Format userdata (factory reset)","Format data",erase_userdata,False,[],"fastboot erase userdata","")

semititle("---Bootloader---",toolsLayout)
unlockblnew = Commands("Flashing Unlock (modern devices)","Unlock",flashing_unlock,False,[],"fastboot flashing unlock","")
unlockblold = Commands("Oem Unlock (older devices)","Unlock",oem_unlock,False,[],"fastboot oem unlock","")
relockblnew = Commands("Flashing Lock (modern devices)","Relock",flashing_lock,False,[],"fastboot flashing lock","")
relockblold = Commands("Oem Lock (older devices)","Relock",oem_lock,False,[],"fastboot oem lock","")

semititle("---Other---",toolsLayout)
magisk = Commands("Flash Magisk with ADB Sideload","Flash",magisk_sideload,True,["apk","zip"],"adb sideload [path to magisk]","")

terminaltitlelayout = QHBoxLayout()
terminaltitle = QLabel("Output")
terminalkill = QPushButton("Kill")
colorsbut(terminalkill,"#ff0000","#f16868")
terminaltitlelayout.addWidget(terminaltitle)
terminaltitlelayout.addStretch()
terminalkill.clicked.connect(kill)
terminaltitlelayout.addWidget(terminalkill)
terminal = QTextEdit()
terminal.setReadOnly(True)
rightLayout.addLayout(terminaltitlelayout)
rightLayout.addWidget(terminal)

toolbar = QHBoxLayout()
main.addLayout(toolbar)
versionlabel = QLabel()
toolbar.addWidget(releasenotesbut)
latestversion = QPushButton()
latestversion.setIcon(QIcon(os.getcwd()+r"\assets\update.png"))
latestversion.clicked.connect(openupdates)
colorsbut(latestversion,"#00000000","#3c3c3c37")
toolbar.addWidget(latestversion)
toolbar.addStretch()
toolbar.addWidget(versionlabel)

adb = os.getcwd()+r"\platform-tools\adb.exe"
magiskdir = os.getcwd()+r"\magisk\magisk"
fastbootdir = os.getcwd()+r"\platform-tools\fastboot.exe"
window.configdir = os.getcwd()+r"\assets\config.json"
window.releasedir = os.getcwd()+r"\assets\releasenotes.json"

if os.path.exists(adb):
    pass
else:
    messagebox("Adb.exe not found")
    exit()
if os.path.exists(fastbootdir):
    pass
else:
    messagebox("Fastboot.exe not found")
    exit()
if os.path.exists(window.configdir):
    pass
else:
    messagebox("window.config.json not found")
    exit()

#Update checkong
try:
    releasenotesurl = "https://raw.githubusercontent.com/broke-tech/android-flashing-shortcuts/refs/heads/main/releasenotes.json"
    r = requests.get(releasenotesurl)
    with open(os.getcwd()+r"\assets\releasenotes.json","w") as file:
        file.write(r.text)
except:
    messagebox("Failed to check for updates;\nDisconnected from the internet.")

font_path = os.path.join(os.getcwd(), "assets", "Nunito","static","Nunito-Medium.ttf")
font_id = QFontDatabase.addApplicationFont(font_path)
if font_id != -1:
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_family, 11))
else:
    messagebox("Font not found.")

with open(window.configdir,"r") as file:
    window.config = json.load(file)

with open(window.releasedir,"r") as file:
    window.releases = json.load(file)

if window.config["dialog"] == 'True':
    dialog("WARNING",
        "Friendly reminder:\n\n"
        "Some Fastboot commands may only work on certain devices.\n"
        "For example, bootloader unlocking can differ between newer and older phones.\n\n"
        "If a command fails, it doesn't necessarily mean something is wrong "
        "your device may simply not support it.\n\n"
        "Please double-check your device model before continuing.","Ok","Don't show again"
    )
    if window.yesno:
        pass
    elif not window.yesno:
        with open(window.configdir,"w") as file:
            window.config["dialog"] = "False"
            json.dump(window.config,file)


#RELEASE NOTES
windownotes = QWidget()
windownotes.setWindowTitle("AFS - Release Notes")
windownotes.setWindowIcon(QIcon(os.getcwd()+r"\assets\icon.png"))
mainnotes = QVBoxLayout()
windownotes.setLayout(mainnotes)
titlenotes = QLabel("AFS - Release Notes")
setsize(titlenotes,20)
mainnotes.addWidget(titlenotes,alignment=Qt.AlignHCenter)
releaselayout = QVBoxLayout()
scrollwidgetrelease = QWidget()
scrollwidgetrelease.setLayout(releaselayout)
scrollrelease = QScrollArea()
scrollrelease.setWidgetResizable(True)
scrollrelease.setFrameShape(QFrame.NoFrame)
scrollrelease.setWidget(scrollwidgetrelease)
for i in range(len(window.releases["releases"])):
    name = QLabel(f"Release {window.releases["releases"][i]["name"]} in {window.releases["releases"][i]["date"]}")
    setsize(name,30)
    releaselayout.addWidget(name,alignment=Qt.AlignLeft)
    releaselayout.addWidget(QLabel(window.releases["releases"][i]["notes"]))
    releaselayout.addStretch()
mainnotes.addWidget(scrollrelease)
githubrelease = QPushButton("See and download all releases on GitHub")
githubrelease.setIcon(QIcon(os.getcwd()+r"\assets\github.png"))
githubrelease.clicked.connect(githubopensite)
colorsbut(githubrelease,"#00000000","#3c3c3c37")
mainnotes.addWidget(githubrelease)

#UPDATES
windowupdate = QWidget()
windowupdate.setWindowTitle("AFS - Updates")
windowupdate.setWindowIcon(QIcon(os.getcwd()+r"\assets\icon.png"))
mainupdate = QVBoxLayout()
windowupdate.setLayout(mainupdate)
titleupdate = QLabel("AFS - Updates")
setsize(titleupdate,20)
mainupdate.addWidget(titleupdate,alignment=Qt.AlignHCenter)
updatelayout = QVBoxLayout()
scrollwidgetupdate = QWidget()
scrollwidgetupdate.setLayout(updatelayout)
scrollupdate = QScrollArea()
scrollupdate.setWidgetResizable(True)
scrollupdate.setFrameShape(QFrame.NoFrame)
scrollupdate.setWidget(scrollwidgetupdate)

if window.releases["latest"] != version:
    latestversion.setText("Update available!")
    versionlabel.setText(f"Version {version} (newer available)")
    name = QLabel(f"UPDATE: Release {window.releases["latest"]} in {window.releases["releases"][0]["date"]}")
    setsize(name,30)
    mainupdate.addWidget(name,alignment=Qt.AlignLeft)
    updatelayout.addWidget(QLabel(window.releases["releases"][0]["notes"]))
    updatelayout.addStretch()
    mainupdate.addWidget(scrollupdate)
else:
    latestversion.setText("No updates found")
    versionlabel.setText(f"Version {version} (latest)")
    name = QLabel(f"Latest release (this one) {window.releases["latest"]} in {window.releases["releases"][0]["date"]}")
    setsize(name,30)
    mainupdate.addWidget(name,alignment=Qt.AlignLeft)
    updatelayout.addWidget(QLabel(window.releases["releases"][0]["notes"]))
    updatelayout.addStretch()
    mainupdate.addWidget(scrollupdate)

githubupdate = QPushButton("Download newest version on Github")
githubupdate.setIcon(QIcon(os.getcwd()+r"\assets\github.png"))
githubupdate.clicked.connect(githubopensite)
colorsbut(githubupdate,"#00000000","#3c3c3c37")
mainupdate.addWidget(githubupdate)

#OPTIONS
windowopts = QWidget()
windowopts.setWindowTitle("AFS - Options")
windowopts.setWindowIcon(QIcon(os.getcwd()+r"\assets\icon.png"))
mainopts = QVBoxLayout()
windowopts.setLayout(mainopts)
titleopts = QLabel("AFS - Options")
setsize(titleopts,20)
mainopts.addWidget(titleopts,alignment=Qt.AlignHCenter)
mainopts.addStretch()

defaultdirlayout = QHBoxLayout()
defaultdirtitle = QLabel("Default files directory")
defaultdir = QLineEdit()
defaultdir.setFixedWidth(400)
defaultdir.setStyleSheet("border-radius: 8px; padding: 4;")
defaultdir.setReadOnly(True)
defaultdirbut = QPushButton("Select folder")
colorsbut(defaultdirbut,"#FFBB00","#fcdf4c")
defaultdirbut.clicked.connect(chooseDefaultdir)
defaultdirlayout.addWidget(defaultdirtitle)
defaultdirlayout.addStretch()
defaultdirlayout.addWidget(defaultdir)
defaultdirlayout.addWidget(defaultdirbut)
mainopts.addLayout(defaultdirlayout)

dialogstartlayout = QHBoxLayout()
dialogstarttitle = QLabel("Warning dialog at start")
dialogstart = QCheckBox()
dialogchange()
dialogstart.stateChanged.connect(dialogclicked)
dialogstartlayout.addWidget(dialogstarttitle)
dialogstartlayout.addStretch()
dialogstartlayout.addWidget(dialogstart)
mainopts.addLayout(dialogstartlayout)
defaultdirectorycheck()
mainopts.addStretch()
mainopts.addWidget(QLabel(f"(c) Android Flashing Shortcuts v{version} by @brOke.tech"),alignment=Qt.AlignRight)

window.setLayout(main)
window.show()
app.exec()