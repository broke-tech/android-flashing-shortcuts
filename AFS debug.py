from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QListWidgetItem, QDialogButtonBox, QDialog, QFrame, QScrollArea, QFileDialog, QComboBox, QCheckBox, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QPushButton, QLineEdit, QTextEdit, QListWidget
from PyQt5.QtGui import QPixmap, QIcon
import os
from webbrowser import open

workdir = None
adb = os.getcwd()+r"\platform-tools\adb.exe"
magiskdir = os.getcwd()+r"\magisk\magisk"
fastbootdir = os.getcwd()+r"\platform-tools\fastboot.exe"

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
            file = os.path.join(workdir, zipslist.currentItem().text())
            dialog(adbinstall.command)
            if window.yesno:
                worker.start(adb, ["install", file])
            else:
                pass
        except:
            messagebox("File not found")
    else: 
        messagebox("Another process is running!")

def adb_sideload():
    if worker.state() != QProcess.Running:
        try:
            terminal.clear()
            file = os.path.join(workdir, zipslist.currentItem().text())
            dialog(adbsideload.command)
            if window.yesno:
                worker.start(adb, ["sideload", file])
            else:
                pass
        except:
            messagebox("File not found")
    else: 
        messagebox("Another process is running!")

def flashing_unlock():
    if worker.state() != QProcess.Running:
        terminal.clear()
        dialog(unlockblnew.command)
        if window.yesno:
            worker.start(fastbootdir, ["flashing", "unlock"])
        else:
            pass
    else: 
        messagebox("Another process is running!")

def flashing_lock():
    if worker.state() != QProcess.Running:
        terminal.clear()
        dialog(relockblnew.command)
        if window.yesno:
            worker.start(fastbootdir, ["flashing", "lock"])
        else:
            pass
    else: 
        messagebox("Another process is running!")

def oem_unlock():
    if worker.state() != QProcess.Running:
        terminal.clear()
        dialog(unlockblold.command)
        if window.yesno:
            worker.start(fastbootdir, ["oem", "unlock"])
        else:
            pass
    else: 
        messagebox("Another process is running!")
    
def oem_lock():
    if worker.state() != QProcess.Running:
        terminal.clear()
        dialog(relockblold.command)
        if window.yesno:
            worker.start(fastbootdir, ["oem", "lock"])
        else:
            pass
    else: 
        messagebox("Another process is running!")

def magisk_sideload():
    if worker.state() != QProcess.Running:
        try:
            terminal.clear()
            dialog(magisk.command)
            if window.yesno:
                worker.start(adb, ["sideload", magiskdir+"."+magisk.combobox.currentText()])
            else:
                pass
        except:
            messagebox("File not found")
    else: 
        messagebox("Another process is running!")

def boot_image():
    if worker.state() != QProcess.Running:
        try:
            file = os.path.join(workdir, zipslist.currentItem().text())
            terminal.clear()
            dialog(bootimg.command)
            if window.yesno:
                worker.start(fastbootdir, ["boot", file])
            else:
                pass
        except:
            messagebox("File not found")
    else:
        messagebox("Another process is running!")
        
def flash_image():
    if worker.state() != QProcess.Running:
        try:
            file = os.path.join(workdir, zipslist.currentItem().text())
            terminal.clear()
            dialog(flash.command)
            if window.yesno:
                worker.start(fastbootdir, ["flash", flash.combobox.currentText(), file])
            else:
                pass
        except:
            messagebox("File not found")
    else:
        messagebox("Another process is running!")

def vbmeta():
    if worker.state() != QProcess.Running:
        try:
            file = os.path.join(workdir, zipslist.currentItem().text())
            terminal.clear()
            dialog(flashvbmeta_disable.command)
            if window.yesno:
                worker.start(fastbootdir, ["flash","--disable-verity","--disable-verification","vbmeta",file])
            else:
                pass
        except:
            messagebox("File not found")
    else:
        messagebox("Another process is running!")

def erase_partition():
    if worker.state() != QProcess.Running:
        terminal.clear()
        dialog(erase.command)
        if window.yesno:
            worker.start(fastbootdir, ["erase", erase.combobox.currentText()])
        else:
            pass 
    else:
        messagebox("Another process is running!")

def erase_userdata():
    if worker.state() != QProcess.Running:
        terminal.clear()
        dialog(formatuserdata.command)
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
window.firsttitle = True

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
    def __init__(self,name=" ",butname=" ",function=None,combo=False,items=list(),command=' '):
        self.name = name
        self.butname = butname
        self.function = function
        self.combo = combo
        self.items = items
        self.command = command
        self.layout = QHBoxLayout()
        self.title = QLabel(self.name)
        self.layout.addWidget(self.title)
        self.but = QPushButton(self.butname)
        if self.combo:
            self.combobox = QComboBox()
            self.combobox.addItems(items)
            self.layout.addWidget(self.combobox)
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

def accept():
    window.yesno = True
    window.dialogbox.hide()

def reject():
    window.yesno = False
    window.dialogbox.hide()

def dialog(command):
    window.dialogbox = QDialog()
    window.dialogbox.setWindowTitle("Are you sure?")
    QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
    buttonBox = QDialogButtonBox(QBtn)
    buttonBox.accepted.connect(accept)
    buttonBox.rejected.connect(reject)
    layout = QVBoxLayout()
    message = QLabel(f"Are you sure you want to run the command '{command}'? This is your own risk btw!")
    layout.addWidget(message)
    layout.addWidget(buttonBox)
    window.dialogbox.setLayout(layout)
    window.dialogbox.exec()

def addfiles():
    zipslist.clear()
    zips = []
    img = []
    apk = []
    other = []
    for item in filenames:
        if item.endswith(".zip"):
            zips.append(item)
        elif item.endswith(".img"):
            img.append(item)
        elif item.endswith(".apk"):
            apk.append(item)
        else:
            if not item.endswith(""):
                other.append(item)
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
    if len(other) != 0:
        addHeader(" ")
        addHeader("----Other Files----")
        zipslist.addItems(other)

def addHeader(text):
    item = QListWidgetItem(text)
    item.setFlags(Qt.NoItemFlags)
    zipslist.addItem(item)

main = QVBoxLayout()
titleLayout = QHBoxLayout()

def githubopen():
    open("https://github.com/broke-tech/android-flashing-shortcuts")

def ttopen():
    open("https://tiktok.com/@br0ke.tech")

title = QLabel("AFS - Android Flashing Shortcuts")
setsize(title,40)
logo = QLabel()
logo.setPixmap(QPixmap(os.getcwd()+r"\assets\logo.png").scaled(400,100,Qt.KeepAspectRatio,Qt.SmoothTransformation))
githubpagebut = QPushButton("GitHub page")
githubpagebut.clicked.connect(githubopen)
tiktokpagebut = QPushButton("TikTok page")
tiktokpagebut.clicked.connect(ttopen)
titleLayout.addWidget(logo, alignment=Qt.AlignVCenter)
titleLayout.addWidget(title, alignment=Qt.AlignVCenter)

titleLayout.addStretch()
titleLayout.addWidget(QLabel("     "), alignment=Qt.AlignVCenter)
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
zipsdir.setReadOnly(True)
loaddir = QPushButton("Load")
loaddir.clicked.connect(chooseWorkdir)
dirLayout.addWidget(zipsdir)
dirLayout.addWidget(loaddir,)
zipslist = QListWidget()

zipslist.setFixedWidth(410)
zipsdir.setFixedWidth(300)
loaddir.setFixedWidth(100)

leftLayout.addLayout(dirLayout)
leftLayout.addWidget(QLabel("Files"))
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
adbreboot = Commands("ADB reboot to","Reboot",adb_reboot,True,["system","recovery","bootloader","fastboot"],"adb reboot [selected partition]")
adbinstall = Commands("Install APK","Install",adb_install,False,"adb install [selected file]")

semititle("---Sideloading and flashing---",toolsLayout)
adbsideload = Commands("ADB sideload","Sideload",adb_sideload,False,[],'adb sideload [selected file]')
flash = Commands("Flash image to partition","Flash",flash_image,True,["boot","recovery","system","vendor","vbmeta","userdata","super"],"fastboot flash [selected partition] [selected file]")
flashvbmeta_disable = Commands("Flash vbmeta (disable verity/verification)","Flash vbmeta",vbmeta,False,[],"fastboot flash vbmeta --disable-verity --disable-verification [selected vbmeta]")

semititle("---Get information---",toolsLayout)
fastbootdevices = Commands("Detect fastboot device","Devices",fastboot_devices,False,[],"fastboot devices")
getvars = Commands("Get device info","Info",fastboot_getvar,False,[],"fastboot getvar all")

semititle("---Booting and rebooting---",toolsLayout)
reboot = Commands("Reboot to","Reboot",fastboot_reboot,True,["system","recovery","bootloader","fastboot"],"fastboot reboot [selected partition]")
bootimg = Commands("Boot image temporarily","Boot",boot_image,False,[],"fastboot boot [selected file]")

semititle("---Erasing---",toolsLayout)
erase = Commands("Erase partition","Erase",erase_partition,True,["cache","metadata","product","boot","recovery","system","vendor","vbmeta","super"],"fastboot erase [selected partition]")
formatuserdata = Commands("Format userdata (factory reset)","Format data",erase_userdata,False,[],"fastboot erase userdata")

semititle("---Bootloader---",toolsLayout)
unlockblnew = Commands("Flashing Unlock (modern devices)","Unlock",flashing_unlock,False,[],"fastboot flashing unlock")
unlockblold = Commands("Oem Unlock (older devices)","Unlock",oem_unlock,False,[],"fastboot oem unlock")
relockblnew = Commands("Flashing Lock (modern devices)","Relock",flashing_lock,False,[],"fastboot flashing lock")
relockblold = Commands("Oem Lock (older devices)","Relock",oem_lock,False,[],"fastboot oem lock")

semititle("---Other---",toolsLayout)
magisk = Commands("Flash Magisk with ADB Sideload","Flash",magisk_sideload,True,["apk","zip"],"adb sideload [path to magisk]")

terminaltitlelayout = QHBoxLayout()
terminaltitle = QLabel("Output")
terminalkill = QPushButton("Kill")
terminaltitlelayout.addWidget(terminaltitle)
terminaltitlelayout.addStretch()
terminalkill.clicked.connect(kill)
terminaltitlelayout.addWidget(terminalkill)
terminal = QTextEdit()
terminal.setReadOnly(True)
rightLayout.addLayout(terminaltitlelayout)
rightLayout.addWidget(terminal)

messagebox(
    "Friendly reminder:\n\n"
    "Some Fastboot commands may only work on certain devices.\n"
    "For example, bootloader unlocking can differ between newer and older phones.\n\n"
    "If a command fails, it doesn't necessarily mean something is wrong "
    "your device may simply not support it.\n\n"
    "Please double-check your device model before continuing."
)

window.setLayout(main)
window.show()
app.exec()