from PyQt5.QtCore import *
import os

class RunTime(QProcess):
    def __init__(self,parentv):
        super().__init__()
        self.parentv = parentv
        self.isRunning = False
        self.curterminal = None
        self.setWorkingDirectory(os.path.join(self.parentv.curdir,"assets","platform-tools"))
        self.readyReadStandardOutput.connect(self.update)
        self.errorOccurred.connect(self.update)
        self.readyReadStandardError.connect(self.update)
        self.finished.connect(self.finish)

    def startc(self, command, terminal):
        if self.parentv.config["dialogs"] == True:
            self.parentv.dialogbox.showup(f"Are you sure you want to run '{command}'?\nThe risk is entirely yours!")
            if self.parentv.yesno == True:
                self.isRunning = True
                self.curterminal = terminal
                self.start("bash", ["-c", f"./{command}"])
        else:
            self.isRunning = True
            self.curterminal = terminal
            self.start("bash", ["-c", f"./{command}"])
    def update(self):
        out = self.readAllStandardOutput().data().decode().strip()
        if out:
            self.curterminal.append(out)

        err = self.readAllStandardError().data().decode().strip()
        if err:
            self.curterminal.append(err)

    def finish(self):
        self.isRunning = False
        if self.curterminal == self.parentv.applogs:
            self.parentv.s3.switch(self.parentv.sidebars,self.parentv.gs,self)
        self.curterminal = None

class AppRunTime(QProcess):
    def __init__(self,parentv,runtime):
        super().__init__()
        self.isRunning = False
        self.parentv = parentv
        self.runtime = runtime
        self.installedapps = []
        self.systemapps = []
        self.disabledapps = []

    def startc(self):
        if self.runtime.isRunning == False:
            try:
                self.readyReadStandardOutput.disconnect()
                self.errorOccurred.disconnect()
                self.readyReadStandardError.disconnect()
                self.finished.disconnect()
            except:
                pass

            self.installedapps = []
            self.systemapps = []
            self.disabledapps = []

            self.setWorkingDirectory(os.path.join(self.parentv.curdir,"assets","platform-tools"))
            self.readyReadStandardOutput.connect(self.update)
            self.errorOccurred.connect(self.update)
            self.readyReadStandardError.connect(self.update)
            self.finished.connect(self.second)
            self.runtime.isRunning = True
            self.start("bash",["-c","./adb shell cmd package list packages -3"])
            print("Started first phase")

    def update(self):
        out = self.readAllStandardOutput().data().decode().strip()
        try:
            if out:
                sout = out.split("\n")
                for i in sout:
                    if "package" in i:
                        self.installedapps.append(i[8:])
        except:
            pass

        err = self.readAllStandardError().data().decode().strip()
        try:
            if err:
                serr = err.split("\n")
                for i in serr:
                    if "package" in i:
                        self.installedapps.append(i[8:])
        except:
            pass

    def update2(self):
        out = self.readAllStandardOutput().data().decode().strip()
        try:
            if out:
                sout = out.split("\n")
                for i in sout:
                    if "package" in i:
                        self.systemapps.append(i[8:])
        except:
            pass

        err = self.readAllStandardError().data().decode().strip()
        try:
            if err:
                serr = err.split("\n")
                for i in serr:
                    if "package" in i:
                        self.systemapps.append(i[8:])
        except:
            pass

    def update3(self):
        out = self.readAllStandardOutput().data().decode().strip()
        try:
            if out:
                sout = out.split("\n")
                for i in sout:
                    if "package" in i:
                        self.disabledapps.append(i[8:])
        except:
            pass

        err = self.readAllStandardError().data().decode().strip()
        try:
            if err:
                serr = err.split("\n")
                for i in serr:
                    if "package" in i:
                        self.disabledapps.append(i[8:])
        except:
            pass

    def second(self):
        try:
            self.readyReadStandardOutput.disconnect()
            self.errorOccurred.disconnect()
            self.readyReadStandardError.disconnect()
            self.finished.disconnect()
        except:
            pass

        self.readyReadStandardOutput.connect(self.update2)
        self.errorOccurred.connect(self.update2)
        self.readyReadStandardError.connect(self.update2)
        self.finished.connect(self.third)
        self.start("bash",["-c","./adb shell cmd package list packages -s"])
        print("started second phase")
        print(self.installedapps)

    def third(self):
        try:
            self.readyReadStandardOutput.disconnect()
            self.errorOccurred.disconnect()
            self.readyReadStandardError.disconnect()
            self.finished.disconnect()
        except:
            pass

        self.readyReadStandardOutput.connect(self.update3)
        self.errorOccurred.connect(self.update3)
        self.readyReadStandardError.connect(self.update3)
        self.finished.connect(self.parentv.detectapps)
        self.start("bash",["-c","./adb shell cmd package list packages -d"])
        print("Started third phase")

class CheckRunTime(QProcess):
    def __init__(self,parentv,runtime):
        super().__init__()
        self.isRunning = False
        self.parentv = parentv
        self.runtime = runtime
        self.installedapps = []
        self.systemapps = []
        self.disabledapps = []

    def startc(self,l):
        if self.runtime.isRunning == False:
            try:
                self.readyReadStandardOutput.disconnect()
                self.errorOccurred.disconnect()
                self.readyReadStandardError.disconnect()
                self.finished.disconnect()
            except:
                pass

            self.installedapps = []
            self.systemapps = []
            self.disabledapps = []

            self.setWorkingDirectory(os.path.join(self.parentv.curdir,"assets","platform-tools"))
            self.readyReadStandardOutput.connect(lambda:self.updatea(l))
            self.errorOccurred.connect(lambda:self.updatea(l))
            self.readyReadStandardError.connect(lambda:self.updatea(l))
            self.finished.connect(self.finish)
            self.runtime.isRunning = True
            self.start("bash",["-c","./adb devices"])

    def updatea(self,l):
        out = self.readAllStandardOutput().data().decode('utf-8', errors='ignore').strip()
        try:
            if out:
                if len(out.split("\n")) == 1:
                    l.setText("Not connected")
                else:
                    if len(out.split("\n")) == 2:
                        l.setText('Connected to '+out.split("\n")[-1].split("\t")[0])
                    else:
                        l.setText('Connected to '+out.split("\n")[1].split("\t")[0]+ 'and more')

        except:
            l.setText("Error occured")

    def startf(self,l):
        if self.runtime.isRunning == False:
            try:
                self.readyReadStandardOutput.disconnect()
                self.errorOccurred.disconnect()
                self.readyReadStandardError.disconnect()
                self.finished.disconnect()
            except:
                pass

            self.installedapps = []
            self.systemapps = []
            self.disabledapps = []

            self.setWorkingDirectory(os.path.join(self.parentv.curdir,"assets","platform-tools"))
            self.readyReadStandardOutput.connect(lambda:self.updatef(l))
            self.errorOccurred.connect(lambda:self.updatef(l))
            self.readyReadStandardError.connect(lambda:self.updatef(l))
            self.finished.connect(self.finish)
            self.runtime.isRunning = True
            self.start("bash",["-c","./fastboot devices"])

    def updatef(self,l):
        try:
            out = bytes(self.readAllStandardOutput()).decode('utf-8', errors='ignore').strip()
            err = bytes(self.readAllStandardError()).decode('utf-8', errors='ignore').strip()
            if out:
                pass
            if err:
                if "waiting for" in err:
                    self.kill()
                    self.runtime.isRunning = False
                    l.setText('Not connected')
                else:
                    if "product:" in err:
                        l.setText(f'Connected to '+err.partition("Finished")[0].partition("\n")[0].partition("product: ")[2])
                    else:
                        self.kill()
                        self.runtime.isRunning = False
                        l.setText('Not connected')
        except:
            pass


    def finish(self):
        self.runtime.isRunning = False