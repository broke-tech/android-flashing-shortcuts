from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QListWidgetItem, QDialog, QGroupBox, QRadioButton, QFrame, QScrollArea, QFileDialog, QComboBox, QCheckBox, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QPushButton, QLineEdit, QTextEdit, QListWidget
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor, QFontDatabase, QPalette
import os
import json
import requests
from webbrowser import open as opensite
import subprocess
import sys
version = "2.2"
jojoreferences = ["jojo","jjba","joseph","jonathan","joestar","jotaro","giorno","jolyne","jonny","dio","kars","stand","koichi","josuke","yareyare","polnareff","avdol","iggy","kakyoin"]
workdir = os.getcwd()
filenames = os.listdir(workdir)

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

def check_devices():
    workercheck = QProcess()
    workercheck.setWorkingDirectory(os.getcwd() + "/assets/platform-tools")
    def updatecheck():
        try:
            out = bytes(workercheck.readAllStandardOutput()).decode().strip()
            err = bytes(workercheck.readAllStandardError()).decode().strip()
            if out:
                pass
            if err:
                if "waiting for any device" in err:
                    workercheck.kill()
                    #righttitle.setText('TOOLS | Fastboot: No devices')
                    secondconnect.setText('Not connected\n')
                else:
                    if "product:" in err:
                        #righttitle.setText(f"TOOLS | Fastboot: {err.partition("Finished")[0].partition("\n")[0].partition("product: ")[2]}")
                        secondconnect.setText(f'Connected to {err.partition("Finished")[0].partition("\n")[0].partition("product: ")[2]}\n')
                    else:
                        workercheck.kill()
                        #righttitle.setText('TOOLS | Fastboot: No devices')
                        secondconnect.setText('Not connected\n')
        except:
            pass
    workercheck.readyReadStandardOutput.connect(updatecheck)
    workercheck.readyReadStandardError.connect(updatecheck)
    workercheck.finished.connect(updatecheck)

    workercheck.start(fastbootdir, ["getvar", "product"])

        

def listapps():
    if worker.state() != QProcess.Running:
        terminal.clear()
        try:
            apps = subprocess.check_output([adb, "shell","cmd","package","list", "packages","-3"],text=True).split()
            window.listedapps = []
            for b in apps:
                if "package:" in b:
                    if len(searchapps.text()) != 0:
                        if searchapps.text() in b:
                            window.listedapps.append(b[8:])
                    else:
                        window.listedapps.append(b[8:])
            apps = subprocess.check_output([adb, "shell","cmd","package","list", "packages","-s"],text=True).split()
            window.systemapps = []
            for b in apps:
                if "package:" in b:
                    if len(searchapps.text()) != 0:
                        if searchapps.text() in b:
                            window.systemapps.append(b[8:])
                    else:
                        window.systemapps.append(b[8:])
            apps = subprocess.check_output([adb, "shell","cmd","package","list", "packages","-d"],text=True).split()
            window.disabledapps = []
            for b in apps:
                if "package:" in b:
                    if len(searchapps.text()) != 0:
                        if searchapps.text() in b:
                            window.disabledapps.append(b[8:])
                    else:
                        window.disabledapps.append(b[8:])
        except:
            messagebox("Error while listing apps.\nProbable reason: no devices detected")
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
            if window.selectedfile == None:
                messagebox("Select a file first.")
                return False
            file = os.path.join(workdir,window.selectedfile)
            if os.path.exists(file):
                pass
            else:
                messagebox("File does not exist.")
                return False
            window.yesno = False
            dialog("WARNING",f"Are you sure you want to run the command '{adbinstall.command+window.selectedfile}'? This is your own risk btw!", "YES YES YES","Like hell I will (no)")
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
            if window.selectedfile == None:
                messagebox("Select a file first.")
                return False
            file = os.path.join(workdir,window.selectedfile)
            if os.path.exists(file):
                pass
            else:
                messagebox("File does not exist.")
                return False
            window.yesno = False
            dialog("WARNING",f"Are you sure you want to run the command '{adbsideload.command+window.selectedfile}'? This is your own risk btw!", "YES YES YES","Like hell I will (no)")
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
        window.yesno = False
        dialog("WARNING",f"Are you sure you want to run the command '{unlockblnew.command}'? This is your own risk btw!", "YES YES YES","Like hell I will (no)")
        if window.yesno:
            worker.start(fastbootdir, ["flashing", "unlock"])
        else:
            pass
    else: 
        messagebox("Another process is running!")

def flashing_lock():
    if worker.state() != QProcess.Running:
        terminal.clear()
        window.yesno = False
        dialog("WARNING",f"Are you sure you want to run the command '{relockblnew.command}'? This is your own risk btw!", "YES YES YES","Like hell I will (no)")
        if window.yesno:
            worker.start(fastbootdir, ["flashing", "lock"])
        else:
            pass
    else: 
        messagebox("Another process is running!")

def oem_unlock():
    if worker.state() != QProcess.Running:
        terminal.clear()
        window.yesno = False
        dialog("WARNING",f"Are you sure you want to run the command '{unlockblold.command}'? This is your own risk btw!", "YES YES YES","Like hell I will (no)")
        if window.yesno:
            worker.start(fastbootdir, ["oem", "unlock"])
        else:
            pass
    else: 
        messagebox("Another process is running!")
    
def oem_lock():
    if worker.state() != QProcess.Running:
        terminal.clear()
        window.yesno = False
        dialog("WARNING",f"Are you sure you want to run the command '{relockblold.command}'? This is your own risk btw!", "YES YES YES","Like hell I will (no)")
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
                window.yesno = False
                dialog("WARNING",f"Are you sure you want to run the command '{magisk.command}'? This is your own risk btw!", "YES YES YES","Like hell I will (no)")
                if window.yesno:
                    worker.start(adb, ["sideload", magiskdir+"."+magisk.combobox.currentText()])
                else:
                    pass
            except:
                messagebox("Error")
        else:
            messagebox(r"Magisk file not found inside /assets/magisk.")
    else: 
        messagebox("Another process is running!")

def boot_image():
    if worker.state() != QProcess.Running:
        try:
            if window.selectedfile == None:
                messagebox("Select a file first.")
                return False
            file = os.path.join(workdir,window.selectedfile)
            if os.path.exists(file):
                pass
            else:
                messagebox("File does not exist.")
                return False
            terminal.clear()
            window.yesno = False
            dialog("WARNING",f"Are you sure you want to run the command '{bootimg.command+window.selectedfile}'? This is your own risk btw!", "YES YES YES","Like hell I will (no)")
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
            if window.selectedfile == None:
                messagebox("Select a file first.")
                return False
            file = os.path.join(workdir,window.selectedfile)
            if os.path.exists(file):
                pass
            else:
                messagebox("File does not exist.")
                return False
            if flash.lineedit.text().lower() in jojoreferences:
                if window.config["jojo"] != "True":
                    messagebox("EASTER EGG!:\nYou've unlocked a JoJo meme in options!\nv2.2: Kakoyin seeing")
                    with open(window.configdir,"w") as file:
                        window.config["jojo"] = "True"
                        json.dump(window.config,file)
                else:
                    messagebox("That's lowkey a JoJo reference.")
            if len(flash.lineedit.text()) != 0:
                pass
            else:
                messagebox("Enter a partition.")
                return False
            terminal.clear()
            window.yesno = False
            dialog("WARNING",f"Are you sure you want to run the command '{flash.command+window.selectedfile}'? This is your own risk btw!", "YES YES YES","Like hell I will (no)")
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
            if window.selectedfile == None:
                messagebox("Select a file first.")
                return False
            file = os.path.join(workdir,window.selectedfile)
            if os.path.exists(file):
                pass
            else:
                messagebox("File does not exist.")
                return False
            terminal.clear()
            window.yesno = False
            dialog("WARNING",f"Are you sure you want to run the command '{flashvbmeta_disable.command}'? This is your own risk btw!", "YES YES YES","Like hell I will (no)")
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
        if erase.lineedit.text().lower() in jojoreferences:
            if window.config["jojo"] != "True":
                messagebox("EASTER EGG!:\nYou've unlocked a JoJo meme in options!\nv2.2: Kakoyin seeing")
                with open(window.configdir,"w") as file:
                    window.config["jojo"] = "True"
                    json.dump(window.config,file)
            else:
                messagebox("That's lowkey a JoJo reference.")
        if len(erase.lineedit.text().lower()) != 0:
            pass
        else:
            messagebox("Enter a partition.")
            return False
        terminal.clear()
        window.yesno = False
        dialog("WARNING",f"Are you sure you want to run the command '{erase.command}'? This is your own risk btw!", "YES YES YES","Like hell I will (no)")
        if window.yesno:
            worker.start(fastbootdir, ["erase", erase.lineedit.text()])
        else:
            pass 
    else:
        messagebox("Another process is running!")

def erase_userdata():
    if worker.state() != QProcess.Running:
        terminal.clear()
        window.yesno = False
        dialog("WARNING",f"Are you sure you want to run the command '{formatuserdata.command}'? This is your own risk btw!", "YES YES YES","Like hell I will (no)")
        if window.yesno:
            worker.start(fastbootdir, ["erase", "userdata"])
        else:
            pass
    else:
        messagebox("Another process is running!")

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

app = QApplication([])
app.setStyle("Fusion")
window = QWidget()
window.setWindowTitle("AFS - Android Flashing Shortcuts")
window.setWindowIcon(QIcon(os.getcwd()+r"\assets\icons\icon.png"))
extentions = [".zip",".img"]
window.yesno = False
window.selectedfile = None
window.firsttitle = True
window.listedapps = []
window.systemapps = []
window.disabledapps = []
window.configdir = os.getcwd()+r"\assets\config.json"

worker = QProcess()
worker.setWorkingDirectory(os.getcwd()+r"/assets/platform-tools")
worker.readyReadStandardOutput.connect(update)
worker.finished.connect(update)
worker.errorOccurred.connect(update)
worker.readyReadStandardError.connect(update)

msg = QMessageBox()
msg.setWindowTitle("AFS - Message")
def messagebox(message):
    msg.setText(message)
    msg.exec()

if not os.path.exists(window.configdir):
    messagebox("window.config.json not found")
    sys.exit()
else:
    with open(window.configdir,"r") as file:
        window.config = json.load(file)
    darkmode = window.config["darkmode"]

def setline(line):
    line.setStyleSheet("border-radius: 8px; padding: 4px;")

def clear_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clear_layout(item.layout())

def colorsblack(but, before, after):
    but.setStyleSheet(
        "QPushButton {"
            f"background-color: {before};"
            "color: #ffffff;"
            "padding: 8px;"
            "border-radius: 9px;"
            "}"
        "QPushButton:hover {"
            f"background-color: {after};"
            "color: #ffffff;"
            "padding: 8px;"
            "border-radius: 9px;"
            "}"
    )

def colorswhite(but, before, after):
    but.setStyleSheet(
        "QPushButton {"
            f"background-color: {before};"
            "color: #000000;"
            "padding: 8px;"
            "border-radius: 9px;"
            "}"
        "QPushButton:hover {"
            f"background-color: {after};"
            "color: #000000;"
            "padding: 8px;"
            "border-radius: 9px;"
            "}"
    )

if darkmode == "True":
    palette = app.palette()
    palette.setColor(QPalette.Base, QColor("#242424"))
    palette.setColor(QPalette.Button, QColor("#242424"))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.Window, Qt.black)
    palette.setColor(QPalette.Window, Qt.black)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.WindowText, Qt.white)

if darkmode != "True":
    palette = app.palette()
    palette.setColor(QPalette.Base, QColor("#D3D3D3"))
    palette.setColor(QPalette.Button, QColor("#D3D3D3"))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.Window, Qt.white)
    palette.setColor(QPalette.Window, Qt.white)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.WindowText, Qt.black)

def setmode():
    msg.setPalette(palette)
    app.setPalette(palette)

def setsize(widget,size):
    widget.setStyleSheet(f"font-size: {size}px;")

def semititle(title,layout):
    label = QLabel(title)
    if darkmode == "True":
        
        label.setStyleSheet("color: #ffffff; font-size: 30px;")
    else:
        label.setStyleSheet("color: #000000; font-size: 30px;")
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
        if darkmode == "True":
            self.title.setStyleSheet("QLabel { color: #ffffff;}")
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
            setline(self.lineedit)
        self.layout.addStretch()
        self.layout.addWidget(self.but)
        self.but.clicked.connect(self.function)
        toolsLayout.addLayout(self.layout)

class AndroidApp():
    def uninstall(self):
        window.yesno = False
        window.yesno = False
        dialog("Confirmation",f"Are you sure you want to uninstall this app?\n({self.pkg})\nRemoving will have the same effect with\nuninstalling from settings.\nContinue?","Uh, yes ig","No bro are u fr?!")
        if window.yesno:
            try:
                subprocess.run([adb, "shell" ,"pm", "uninstall" ,"-k","--user" ,"0", self.pkg])
                messagebox(f"Successfully uninstalled {self.pkg}")
            except:
                messagebox(f"Error occured while enabling {self.pkg}\nProbable reasons:\n -No device detected")
            appmanagement()

    def enable(self):
        window.yesno = False
        window.yesno = False
        dialog("Confirmation",f"Are you sure you want to enable this app?\n({self.pkg})\nEnabling will have the same effect with\nenableng from settings.\nContinue?","Uh, yes ig","No bro are u fr?!")
        if window.yesno:
            try:
                subprocess.run([adb,"shell" ,"pm", "enable" , self.pkg])
                messagebox(f"Successfully enabled {self.pkg}")
            except:
                messagebox(f"Error occured while enabling {self.pkg}\nProbable reasons:\n -No device detected")
            appmanagement()

    def disable(self):
        window.yesno = False
        window.yesno = False
        dialog("Confirmation",f"Are you sure you want to disable this app?\n({self.pkg})\nDisabling will have the same effect with\ndisabling from settings.\nContinue?","Uh, yes ig","No bro are u fr?!")
        if window.yesno:
            try:
                subprocess.run([adb, "shell" ,"pm", "disable-user" ,"--user" ,"0", self.pkg])
                messagebox(f"Successfully disabled {self.pkg}")
            except:
                messagebox(f"Error occured while enabling {self.pkg}\nProbable reasons:\n -No device detected")
            appmanagement()

    def __init__(self,pkg='',typeapp=''):
        self.pkg = pkg
        self.typeapp = typeapp
        self.name = QLabel(self.pkg)
        setsize(self.name,20)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.name,alignment=Qt.AlignLeft)
        appslayout.addLayout(self.layout)
        self.removebut = QPushButton("")
        if self.typeapp == "3":
            self.typelabel = QLabel("3rd Party app, safe to remove")
            appslayout.addWidget(self.typelabel)
            self.removebut.setText("Uninstall")
            colorsblack(self.removebut,"#19003B","#5C16A7")
            self.removebut.clicked.connect(lambda:self.uninstall())
            self.disablebut = QPushButton("Disable")
            self.disablebut.clicked.connect(lambda:self.disable())
            colorsblack(self.disablebut,"#00567E","#1B87BA")
            self.layout.addWidget(self.disablebut)
        elif self.typeapp == "sys":
            self.typelabel = QLabel("System app. Unsafe to remove. Recommended only for testers.")
            appslayout.addWidget(self.typelabel)
            self.removebut.clicked.connect(lambda:self.disable())
            self.removebut.setText("Disable (RISKY)")
            colorsblack(self.removebut,"#7E0000","#AE0000")
        elif self.typeapp == "d":
            self.typelabel = QLabel("Disabled app, safe to enable only if you disabled it")
            appslayout.addWidget(self.typelabel)
            self.removebut.setText("Enable")
            self.removebut.clicked.connect(lambda:self.enable())
            colorsblack(self.removebut,"#007F15","#21CE03")
        else:
            self.typelabel = QLabel(f"Unknown type")
            appslayout.addWidget(self.typelabel)
            self.removebut.setText("Unknown action")
            colorsblack(self.removebut,"#3C3C3C","#575656")
        self.layout.addWidget(self.removebut)
        self.layout.addStretch()
        
def chooseWorkdir():
    global workdir #calling the global variable
    global filenames
    zipslist.clear()
    workdir = QFileDialog.getExistingDirectory()
    try:
        zipsdir.setText(workdir)
        window.selectedfile = None
        ziptitle.setText(f"Files (Selected: {window.selectedfile})")
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

def seticons():
    if darkmode == "True":
        setmode()
        releasenotesbut.setIcon(QIcon(os.getcwd()+r"\assets\icons\whiteinfo.png"))
        windowguides.but.setIcon(QIcon(os.getcwd()+r"\assets\icons\whitepaper.png"))
        maintoolsbox.but.setIcon(QIcon(os.getcwd()+r"\assets\icons\whitehome.png"))
        windowapps.but.setIcon(QIcon(os.getcwd()+r"\assets\icons\whiteapps.png"))
        windowopts.but.setIcon(QIcon(os.getcwd()+r"\assets\icons\whiteoptions.png"))
        tiktokpagebut.setIcon(QIcon(os.getcwd()+r"\assets\icons\whitetiktok.png"))
        githubpagebut.setIcon(QIcon(os.getcwd()+r"\assets\icons\whitegithub.png"))
        githubrelease.setIcon(QIcon(os.getcwd()+r"\assets\icons\whitegithub.png"))
        githubupdate.setIcon(QIcon(os.getcwd()+r"\assets\icons\whitegithub.png"))
        latestversion.setIcon(QIcon(os.getcwd()+r"\assets\icons\whiteupdate.png"))
    else:
        setmode()
        releasenotesbut.setIcon(QIcon(os.getcwd()+r"\assets\icons\info.png"))
        windowguides.but.setIcon(QIcon(os.getcwd()+r"\assets\icons\paper.png"))
        maintoolsbox.but.setIcon(QIcon(os.getcwd()+r"\assets\icons\home.png"))
        windowapps.but.setIcon(QIcon(os.getcwd()+r"\assets\icons\apps.png"))
        windowopts.but.setIcon(QIcon(os.getcwd()+r"\assets\icons\options.png"))
        tiktokpagebut.setIcon(QIcon(os.getcwd()+r"\assets\icons\tiktok.png"))
        githubpagebut.setIcon(QIcon(os.getcwd()+r"\assets\icons\github.png"))
        githubrelease.setIcon(QIcon(os.getcwd()+r"\assets\icons\github.png"))
        githubupdate.setIcon(QIcon(os.getcwd()+r"\assets\icons\github.png"))
        latestversion.setIcon(QIcon(os.getcwd()+r"\assets\icons\update.png"))

def dialog(title,command,yestext,notext):
    window.yesno = False
    window.dialogbox = QDialog()
    window.dialogbox.setWindowTitle(title)
    if darkmode == "True":
        
        window.dialogbox.setPalette(palette)
    butts = QHBoxLayout()
    accepted = QPushButton(yestext)
    rejected = QPushButton(notext)
    for i in [accepted,rejected]:
        if darkmode == "True":
            
            colorsblack(i,"#00000000","#3c3c3c37")
        else:
            colorswhite(i,"#00000000","#3c3c3c37")
    accepted.clicked.connect(accept)
    rejected.clicked.connect(reject)
    butts.addStretch()
    butts.addWidget(accepted)
    butts.addWidget(rejected)
    layout = QVBoxLayout()
    message = QLabel(command)
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
        dialogstart.setText("On")
    elif window.config["dialog"] == "False":
        dialogstart.setChecked(False)
        dialogstart.setText("Off")

def dialogclicked():
    if dialogstart.isChecked():
        dialogstart.setText("On")
        window.config["dialog"] = "True"
    elif not dialogstart.isChecked():
        dialogstart.setText("Off")
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
    try:
        window.selectedfile = zipslist.currentItem().text()
        if len(window.selectedfile) <= 20:
            ziptitle.setText(f"Files (Selected: {window.selectedfile})")
        else:
            ziptitle.setText(f"Files (Selected: {window.selectedfile[0:20]+"..."})")
    except:
        pass

def modeclicked():
    if blackradio.isChecked():
        window.config["darkmode"] = "True"
    elif whiteradio.isChecked():
        window.config["darkmode"] = "False"
    with open(window.configdir,"w") as file:
        json.dump(window.config,file)
        messagebox("Display mode saved. Restart to apply changes")

def modechanged():
    if window.config["darkmode"] == "True":
        blackradio.setChecked(True)
        whiteradio.setChecked(False)
    elif window.config["darkmode"] == "False":
        whiteradio.setChecked(True)
        blackradio.setChecked(False)

def setbuts(list):
    for i in list:
        if darkmode == "True":
            colorsblack(i,"#434343","#777777")
        else:
            colorswhite(i,"#A4A4A4","#d4d4d4")

def openoptions():
    change_section([windowguides,maintoolsbox,windowapps],windowopts)
    windowopts.but.setIcon(QIcon(os.getcwd()+r"/assets/icons/whiteoptions.png"))

def openmain():
    change_section([windowguides,windowopts,windowapps],maintoolsbox)
    maintoolsbox.but.setIcon(QIcon(os.getcwd()+r"/assets/icons/whitehome.png"))

def openreleasenotes():
    windownotes.show()

def openupdates():
    windowupdate.show()

def change_section(widgets,sel):
    for i in widgets:
        i.hide()
        if darkmode == "True":
            colorsblack(i.but,"#00000000","#3c3c3c37")
        else:
            colorswhite(i.but,"#00000000","#3c3c3c37")
    seticons()
    colorsblack(sel.but,"#006eff","#0084FF")
    sel.show()

logo = QLabel()
logo.setPixmap(QPixmap(os.getcwd()+r"\assets\icons\logo.png").scaled(150,150,Qt.KeepAspectRatio,Qt.SmoothTransformation))
main = QHBoxLayout()
window.setLayout(main)
sectionl = QVBoxLayout()
sectionb = QGroupBox()
sectionb.setLayout(sectionl)
main.addWidget(sectionb)
mainsections = QVBoxLayout()
main.addLayout(mainsections)
maintools = QVBoxLayout()
maintoolsbox = QGroupBox()
maintoolsbox.setLayout(maintools)
mainsections.addWidget(maintoolsbox)
titleLayout = QHBoxLayout()
logolayout = QVBoxLayout()
titleLayout.addLayout(logolayout)
sectionb.setStyleSheet("border: none;")

logo2 = QLabel()
logo2.setPixmap(QPixmap(os.getcwd()+r"\assets\icons\icon.png").scaled(400,100,Qt.KeepAspectRatio,Qt.SmoothTransformation))
releasenotesbut = QPushButton("Release Notes")
releasenotesbut.clicked.connect(openreleasenotes)

title2 = QLabel("AFS - Android Flashing Shortcuts")
setsize(title2,30)
titleLayout.addWidget(logo2)
titleLayout.addWidget(title2)
titleLayout.addStretch()
titleLayout.addWidget(QLabel("     "), alignment=Qt.AlignVCenter)
maintools.addLayout(titleLayout)

sidesLayout = QHBoxLayout()
leftLayout = QVBoxLayout()
rightLayout = QVBoxLayout()
sidesLayout.addLayout(leftLayout)
sidesLayout.addLayout(rightLayout)
maintools.addLayout(sidesLayout)

dirLayout = QHBoxLayout()
zipsdir = QLineEdit()
zipsdir.setReadOnly(True)
loaddir = QPushButton("Select folder")
colorswhite(loaddir,"#FFBB00","#fcdf4c")
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

terminaltitlelayout = QHBoxLayout()
terminaltitle = QLabel("Output")
terminalkill = QPushButton("Kill")
colorswhite(terminalkill,"#ff0000","#f16868")
terminaltitlelayout.addWidget(terminaltitle)
terminaltitlelayout.addStretch()
terminalkill.clicked.connect(kill)
terminaltitlelayout.addWidget(terminalkill)
terminal = QTextEdit() #a8a8a8"
terminal.setReadOnly(True)
rightLayout.addLayout(terminaltitlelayout)
rightLayout.addWidget(terminal)

toolbar = QHBoxLayout()
versionlabel = QLabel()
toolbar.addWidget(releasenotesbut)
latestversion = QPushButton()
latestversion.clicked.connect(openupdates)
toolbar.addWidget(latestversion)
toolbar.addStretch()
toolbar.addWidget(versionlabel)

adb = os.getcwd()+r"\assets\platform-tools\adb.exe"
magiskdir = os.getcwd()+r"\assets\magisk\magisk"
fastbootdir = os.getcwd()+r"\assets\platform-tools\fastboot.exe"
window.releasedir = os.getcwd()+r"\assets\releasenotes.json"

if os.path.exists(adb):
    pass
else:
    messagebox("Adb.exe not found")
    sys.exit()
if os.path.exists(fastbootdir):
    pass
else:
    messagebox("Fastboot.exe not found")
    sys.exit()

#Update checking
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

if os.path.exists(window.releasedir): 
    with open(window.releasedir,"r") as file:
        window.releases = json.load(file)
else:
    window.releases = {"latest":version,"releases":[{"name":version,"date":"???","notes":"releasenotes.json is deleted, it will be restored\nwhen you connect to the Internet."}]}

if window.config["dialog"] == 'True':
    window.yesno = False
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
# Change these two lines
windownotes = QWidget()
windownotes.setWindowTitle("AFS - Release Notes")
windownotes.setWindowIcon(QIcon(os.getcwd()+r"\assets\icons\icon.png"))
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
githubrelease.clicked.connect(lambda:opensite("https://github.com/broke-tech/android-flashing-shortcuts"))
mainnotes.addWidget(githubrelease)

#GUIDES
def openguide(state):
    if state:
        searchbut.setText("Search")
        clear_layout(guidelayout)
        name = QLabel(f"{window.guides[guidecombo.currentText()]["brand"]} guides")
        guidelayout.addWidget(name,alignment=Qt.AlignHCenter)
        setsize(name,40)
        for i in range(len(window.guides[guidecombo.currentText()]["guides"])):
            secname = QLabel(window.guides[guidecombo.currentText()]["guides"][i]["name"]+":")
            setsize(secname,30)
            guidelayout.addWidget(secname,alignment=Qt.AlignHCenter)
            guidelayout.addWidget(QLabel(window.guides[guidecombo.currentText()]["guides"][i]["how"],alignment=Qt.AlignHCenter))
            guidelayout.addWidget(QLabel("\n\n"))
        guidelayout.addWidget(QLabel("Guides are AI generated by Claude"),alignment=Qt.AlignRight)
        guidelayout.addStretch()
    elif not state:
        if searchbut.text() == "Search":
            clear_layout(guidelayout)
            name = QLabel(f"{window.guides[guidecombo.currentText()]["brand"]} guides")
            guidelayout.addWidget(name,alignment=Qt.AlignHCenter)
            setsize(name,40)
            for i in range(len(window.guides[guidecombo.currentText()]["guides"])):
                if searchguide.text().lower() in window.guides[guidecombo.currentText()]["guides"][i]["name"].lower() or searchguide.text().lower() in window.guides[guidecombo.currentText()]["guides"][i]["how"].lower():
                    secname = QLabel(window.guides[guidecombo.currentText()]["guides"][i]["name"]+":")
                    setsize(secname,30)
                    guidelayout.addWidget(secname,alignment=Qt.AlignHCenter)
                    guidelayout.addWidget(QLabel(window.guides[guidecombo.currentText()]["guides"][i]["how"],alignment=Qt.AlignHCenter))
                    guidelayout.addWidget(QLabel("\n\n"))
            guidelayout.addStretch()
            searchbut.setText("Reset")
        else:
            clear_layout(guidelayout)
            name = QLabel(f"{window.guides[guidecombo.currentText()]["brand"]} guides")
            guidelayout.addWidget(name,alignment=Qt.AlignHCenter)
            setsize(name,40)
            for i in range(len(window.guides[guidecombo.currentText()]["guides"])):
                secname = QLabel(window.guides[guidecombo.currentText()]["guides"][i]["name"]+":")
                setsize(secname,30)
                guidelayout.addWidget(secname,alignment=Qt.AlignHCenter)
                guidelayout.addWidget(QLabel(window.guides[guidecombo.currentText()]["guides"][i]["how"],alignment=Qt.AlignHCenter))
                guidelayout.addWidget(QLabel("\n\n"))
            guidelayout.addWidget(QLabel("Guides are AI generated by Claude"),alignment=Qt.AlignRight)
            guidelayout.addStretch()
            searchbut.setText("Search")
            searchguide.clear()
    change_section([windowapps,maintoolsbox,windowopts],windowguides)
    windowguides.but.setIcon(QIcon(os.getcwd()+r"/assets/icons/whitepaper.png"))

windowguides = QGroupBox()
windowguides.hide()
mainsections.addWidget(windowguides)
windowguides.setWindowTitle("AFS - Guides")
windowguides.setWindowIcon(QIcon(os.getcwd()+r"\assets\icons\icon.png"))
mainguides = QVBoxLayout()
windowguides.setLayout(mainguides)
titleguides = QLabel("AFS - Guides")
setsize(titleguides,30)
mainguides.addWidget(titleguides,alignment=Qt.AlignHCenter)
barguides = QHBoxLayout()
mainguides.addLayout(barguides)
guidecombo = QComboBox()
titlecombo = QLabel("Select your brand here:")
barguides.addWidget(titlecombo)
barguides.addWidget(guidecombo)
barguides.addStretch()
claudeicon = QPixmap(os.getcwd()+r"\assets\icons\claude.png").scaled(20,20,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
claudelbl = QLabel()
claudelbl.setPixmap(claudeicon)
barguides.addWidget(claudelbl)
barguides.addWidget(QLabel("Guides are AI generated by Claude"))
searchguide = QLineEdit()
searchguide.setPlaceholderText("Search...")
searchbut = QPushButton("Search")
searchbut.clicked.connect(lambda:openguide(False))
searchbut.setStyleSheet("QPushButton {"
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
                "padding: 10px;"
                "padding-top: 6px;"
                "padding-bottom: 6px;"
                "border-radius: 8px;"
                "}")
guidelayout = QVBoxLayout()
scrollwidgetguide = QWidget()
scrollwidgetguide.setLayout(guidelayout)
scrollguide = QScrollArea()
scrollguide.setWidgetResizable(True)
scrollguide.setFrameShape(QFrame.NoFrame)
scrollguide.setWidget(scrollwidgetguide)
with open(os.getcwd()+r"\assets\guides.json","r") as file:
    window.guides = json.load(file)
guidecombo.clear()
for i in window.guides:
    guidecombo.addItem(window.guides[i]["brand"])
guidecombo.currentTextChanged.connect(lambda:openguide(True))
mainguides.addWidget(scrollguide)
searchguidel = QHBoxLayout()
mainguides.addLayout(searchguidel)
searchguidel.addWidget(searchguide)
searchguidel.addWidget(searchbut)
mainguides.addWidget(QLabel("I nor Claude are responsible for any damages caused while following these guides.\nFollow the instructions carefully and always research when you're confused about something"))

#APPS
def appmanagement():
    change_section([windowguides,maintoolsbox,windowopts],windowapps)
    windowapps.but.setIcon(QIcon(os.getcwd()+r"/assets/icons/whiteapps.png"))
    window.listedapps.sort()
    window.systemapps.sort()
    window.disabledapps.sort()
    if len(windowapps.apps) != 0:
        clear_layout(appslayout)
        windowapps.apps.clear()
    if not window.stateapps:
        window.stateapps = True
        listapps()
        window.firsttitle = True
        if len(window.listedapps) != 0:
            semititle("--3RD PARTY APPS--",appslayout)
            for a in range(len(window.listedapps)):
                if not window.listedapps[a] in window.disabledapps:
                    a = AndroidApp(window.listedapps[a],"3")
                    windowapps.apps.append(a)
        if len(window.systemapps) != 0:
            semititle("--SYSTEM APPS--",appslayout)
            for a in range(len(window.systemapps)):
                if not window.systemapps[a] in window.disabledapps:
                    a = AndroidApp(window.systemapps[a],"sys")
                    windowapps.apps.append(a)
        if len(window.disabledapps) != 0:
            semititle("--DISABLED APPS--",appslayout)
            for a in range(len(window.disabledapps)):
                a = AndroidApp(window.disabledapps[a],"d")
                windowapps.apps.append(a)
        appslayout.addStretch()
        window.stateapps = False

windowapps = QGroupBox()
window.stateapps = False
windowapps.hide()
mainsections.addWidget(windowapps)
windowapps.apps = []
windowapps.setWindowTitle("AFS - App management")
windowapps.setWindowIcon(QIcon(os.getcwd()+r"\assets\icons\icon.png"))
mainapps = QVBoxLayout()
windowapps.setLayout(mainapps)
titleapps = QLabel("AFS - App management")
setsize(titleapps,30)
mainapps.addWidget(titleapps,alignment=Qt.AlignHCenter)
barapps = QHBoxLayout()
mainapps.addLayout(barapps)
barapps.addWidget(QLabel("Here you can manage your apps\nwith love, @br0ke.tech <3"))
barapps.addStretch()
searchapps = QLineEdit()
searchapps.setPlaceholderText("Search query (leave blank to show all)")
searchapps.setFixedWidth(500)
barapps.addWidget(searchapps)
refreshbut = QPushButton("Refresh")
refreshbut.setStyleSheet("QPushButton {"
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
                "}")
refreshbut.clicked.connect(appmanagement)
barapps.addWidget(refreshbut)
appslayout = QVBoxLayout()
scrollwidgetapps = QWidget()
scrollwidgetapps.setLayout(appslayout)
scrollapps = QScrollArea()
scrollapps.setWidgetResizable(True)
scrollapps.setFrameShape(QFrame.NoFrame)
scrollapps.setWidget(scrollwidgetapps)
mainapps.addWidget(scrollapps)

#UPDATES
windowupdate = QWidget()
windowupdate.setWindowTitle("AFS - Updates")
windowupdate.setWindowIcon(QIcon(os.getcwd()+r"\assets\icons\icon.png"))
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
githubupdate.clicked.connect(lambda:opensite("https://github.com/broke-tech/android-flashing-shortcuts"))
mainupdate.addWidget(githubupdate)

#START
guideafs = "AFS Quick Start Guide\n\nSELECTING FILES\nClick 'Select Folder' to choose a directory, then click a file to select it\n\nADB TOOLS\nReboot, install APKs, sideload ZIPs, or manage apps\n\nFASTBOOT TOOLS\nFlash/erase partitions, unlock bootloader, get device info\n\nNOTES\n- All commands ask for confirmation before running\n- Only one command can run at a time\n- Samsung devices are NOT supported for Fastboot\n- Use the Kill button to stop a stuck process\n"
def next(place):
    if place == 1:
        firstb.hide()
        secondb.show()
    if place == 2:
        secondb.hide()
        thirdb.show()
    if place == 3:
        windowstart.hide()
        window.show()
        window.config["first"] = "False"
        with open(window.configdir,"w") as file:
            json.dump(window.config,file)

windowstart = QWidget()
windowstart.setWindowTitle("AFS - Start Up")
windowstart.setWindowIcon(QIcon(os.getcwd()+r"\assets\icons\icon.png"))
mainstart = QVBoxLayout()
windowstart.setLayout(mainstart)
titlestart = QLabel("AFS - Start Up")
setsize(titlestart,30)
mainstart.addWidget(titlestart,alignment=Qt.AlignHCenter)
firstb = QGroupBox()
firstl = QVBoxLayout()
firstbig = QLabel("WELCOME TO AFS!")
setsize(firstbig,30)
firstb.setLayout(firstl)
firstl.addWidget(firstbig,alignment=Qt.AlignHCenter)
firstl.addStretch()
firstl.addWidget(QLabel(guideafs,alignment=Qt.AlignHCenter))
firstbut = QPushButton("Next step (1/3)")
firstbut.clicked.connect(lambda:next(1))
firstl.addWidget(firstbut,alignment=Qt.AlignHCenter)
firstl.addStretch()
mainstart.addWidget(firstb)

secondb = QGroupBox()
secondl = QVBoxLayout()
secondb.setLayout(secondl)
secondl.addWidget(QLabel("WARNING: DON'T FOLLOW THESE STEPS WITH\nA SAMSUNG PHONE AS IT CAN'T USE FASTBOOT!\n\nTo make sure you can use all functions properly\nlet's check if fastboot drivers are installed properly:\n\n\n1. Power off your device.\n2. Press and hold the Power and Volume Down buttons.\n3. Your device should enter Fastboot mode.\n4. Finally click the Refresh button below\n\nIf the text below shows 'Not connected' even though your\ndevice is connected in Fastboot mode, you should reinstall the Fastboot drivers.\n",alignment=Qt.AlignHCenter))
secondconnect = QLabel("Press the Refresh button\n")
secondrefresh = QPushButton("Refresh")
secondrefresh.clicked.connect(check_devices)
secondrefresh.setStyleSheet("QPushButton {"
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
                "}")
setsize(secondconnect,20)
secondl.addStretch()
secondl.addWidget(secondrefresh,alignment=Qt.AlignHCenter)
secondl.addWidget(secondconnect,alignment=Qt.AlignHCenter)
secondl.addStretch()
secondbut = QPushButton("Next 2/3")
secondl.addStretch()
secondbut.clicked.connect(lambda:next(2))
secondl.addWidget(secondbut,alignment=Qt.AlignHCenter)
secondl.addStretch()
secondl.addWidget(QLabel("Issue with Fastboot drivers?"),alignment=Qt.AlignHCenter)
secondfastboot = QPushButton("Fastboot drivers install")
secondfastboot.clicked.connect(lambda:opensite("https://github.com/fawazahmed0/Latest-adb-fastboot-installer-for-windows"))
secondl.addWidget(secondfastboot,alignment=Qt.AlignHCenter)
mainstart.addWidget(secondb)
secondb.hide()

thirdb = QGroupBox()
thirdl = QVBoxLayout()
thirdb.setLayout(thirdl)
thirdl.addStretch()
thirdl.addWidget(QLabel(f"That's it! AFS is ready to use\nFor any questions you can DM me on TikTok (@br0ke.tech)\n\nAFS version {version} by Broke Tech",alignment=Qt.AlignHCenter))
thirdbut = QPushButton("Finish 3/3")
thirdbut.clicked.connect(lambda:next(3))
thirdl.addWidget(thirdbut,alignment=Qt.AlignHCenter)
thirdl.addWidget(QLabel("\nFind me on TikTok"),alignment=Qt.AlignHCenter)
thirdtt = QPushButton("TikTok page")
thirdtt.clicked.connect(lambda:opensite("tiktok.com/@br0ke.tech"))
thirdl.addWidget(thirdtt,alignment=Qt.AlignHCenter)
thirdl.addStretch()
mainstart.addWidget(thirdb)
thirdb.hide()

#OPTIONS
windowopts = QGroupBox()
mainsections.addWidget(windowopts)
windowopts.hide()
windowopts.setWindowTitle("AFS - Options")
windowopts.setWindowIcon(QIcon(os.getcwd()+r"\assets\icons\icon.png"))
mainopts = QVBoxLayout()
windowopts.setLayout(mainopts)
titleopts = QLabel("AFS - Options")
setsize(titleopts,30)
mainopts.addWidget(titleopts,alignment=Qt.AlignHCenter)

optionslayout = QVBoxLayout()
scrollwidgetoptions = QWidget()
scrollwidgetoptions.setLayout(optionslayout)
scrolloptions = QScrollArea()
scrolloptions.setWidgetResizable(True)
scrolloptions.setFrameShape(QFrame.NoFrame)
scrolloptions.setWidget(scrollwidgetoptions)
mainopts.addWidget(scrolloptions)
optionslayout.addWidget(QLabel("Starting options:"),alignment=Qt.AlignHCenter)

defaultdirlayout = QHBoxLayout()
defaultdirtitle = QLabel("Default files directory")
defaultdir = QLineEdit()
defaultdir.setFixedWidth(400)
defaultdir.setReadOnly(True)
defaultdirbut = QPushButton("Select folder")
colorswhite(defaultdirbut,"#FFBB00","#fcdf4c")
defaultdirbut.clicked.connect(chooseDefaultdir)
defaultdirlayout.addWidget(defaultdirtitle)
defaultdirlayout.addStretch()
defaultdirlayout.addWidget(defaultdir)
defaultdirlayout.addWidget(defaultdirbut)
optionslayout.addLayout(defaultdirlayout)

dialogstartlayout = QHBoxLayout()
dialogstarttitle = QLabel("Warning dialog at start")
dialogstart = QCheckBox()
dialogstart.setTristate(False)
dialogchange()
dialogstart.stateChanged.connect(dialogclicked)
dialogstartlayout.addWidget(dialogstarttitle)
dialogstartlayout.addStretch()
dialogstartlayout.addWidget(dialogstart)
optionslayout.addLayout(dialogstartlayout)

#.show()
optionslayout.addWidget(QLabel())
optionslayout.addWidget(QLabel("Select display mode:"),alignment=Qt.AlignHCenter)
themelayout = QHBoxLayout()
blackthemelayout = QVBoxLayout()
whitethemelayout = QVBoxLayout()
blacklogo = QPixmap(os.path.join(os.getcwd(),"assets","images","black.png")).scaled(400,400,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
whitelogo = QPixmap(os.path.join(os.getcwd(),"assets","images","white.png")).scaled(400,400,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
whitelabel = QLabel()
whitelabel.setPixmap(whitelogo)
whiteradio = QRadioButton("Light mode (high cortisol)")
blacklabel = QLabel()
blacklabel.setPixmap(blacklogo)
blackradio = QRadioButton("Dark mode (low cortisol)")
modechanged()
blackradio.clicked.connect(modeclicked)
whiteradio.clicked.connect(modeclicked)
blackthemelayout.addWidget(blacklabel)
blackthemelayout.addWidget(blackradio)
whitethemelayout.addWidget(whitelabel)
whitethemelayout.addWidget(whiteradio)
themelayout.addStretch()
themelayout.addLayout(blackthemelayout)
themelayout.addLayout(whitethemelayout)
themelayout.addStretch()
optionslayout.addLayout(themelayout)
optionslayout.addWidget(QLabel("\n"))
optionslayout.addStretch()

bottomopts = QHBoxLayout()
optionslayout.addLayout(bottomopts)
if window.config["jojo"] == "True":
    jojolabel = QLabel()
    jojopix = QPixmap(os.path.join(os.getcwd(),"assets","images","jojo.png")).scaled(300,300,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
    jojolabel.setPixmap(jojopix)
    bottomopts.addWidget(jojolabel)
bottomopts.addStretch()    
bottomopts.addWidget(QLabel(f"(c) Android Flashing Shortcuts v{version} by @brOke.tech"),alignment=Qt.AlignBottom)

githubpagebut = QPushButton("GitHub page")
githubpagebut.clicked.connect(lambda:opensite("https://github.com/broke-tech/android-flashing-shortcuts"))
tiktokpagebut = QPushButton("TikTok page")
windowopts.but = QPushButton("Options")
windowopts.but.clicked.connect(openoptions)
windowapps.but = QPushButton("App Manager")
windowapps.but.clicked.connect(lambda:appmanagement())
maintoolsbox.but = QPushButton("Main Tools")
maintoolsbox.but.clicked.connect(openmain)
tiktokpagebut.clicked.connect(lambda:opensite("https://tiktok.com/@br0ke.tech"))
windowguides.but = QPushButton("Guides")
windowguides.but.clicked.connect(lambda:openguide(True))
sectionl.addWidget(logo)
for i in [maintoolsbox.but,windowguides.but,windowapps.but,windowopts.but]:
    sectionl.addWidget(i,alignment=Qt.AlignLeft)
sectionl.addStretch()
sectionl.addWidget(tiktokpagebut,alignment=Qt.AlignLeft)
sectionl.addWidget(githubpagebut,alignment=Qt.AlignLeft)

setbuts([windowapps.but,tiktokpagebut,githubpagebut,windowopts.but,releasenotesbut,githubrelease,latestversion,githubupdate,windowguides.but,firstbut,secondbut,secondfastboot,thirdbut,thirdtt,maintoolsbox.but])

#Tools
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

defaultdirectorycheck()
mainsections.addLayout(toolbar)

change_section([windowapps,windowguides,windowopts],maintoolsbox)
maintoolsbox.but.setIcon(QIcon(os.getcwd()+r"/assets/icons/whitehome.png"))
for i in [searchguide,zipsdir,searchapps,defaultdir]:
    setline(i)

if window.config["first"] == "True":    
    windowstart.show()
else: window.show()

app.exec()