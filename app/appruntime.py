from PyQt5.QtCore import *
import os

class RunTime(QProcess):
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
            self.start("adb shell cmd package list packages -3")
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
        self.start("adb shell cmd package list packages -s")
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
        self.start("adb shell cmd package list packages -d")
        print("Started third phase")