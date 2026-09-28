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
            self.start("adb devices")

    def updatea(self,l):
        out = self.readAllStandardOutput().data().decode('utf-8', errors='ignore').strip()
        try:
            if out:
                if len(out.split("\n")) == 1:
                    l.setText("Not connected")
                else:
                    if len(out.split("\n")) == 2:
                        l.setText(f"Connected to {out.split("\n")[-1].split("\t")[0]}")
                    else:
                        l.setText(f"Connected to {out.split("\n")[1].split("\t")[0]} and more")

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
            self.start("fastboot getvar product")

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
                        l.setText(f'Connected to {err.partition("Finished")[0].partition("\n")[0].partition("product: ")[2]}')
                    else:
                        self.kill()
                        self.runtime.isRunning = False
                        l.setText('Not connected')
        except:
            pass


    def finish(self):
        self.runtime.isRunning = False