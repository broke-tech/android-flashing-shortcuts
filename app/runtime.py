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
                self.start(command)
        else:
            self.isRunning = True
            self.curterminal = terminal
            self.start(command)

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