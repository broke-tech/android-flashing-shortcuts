from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QSizePolicy,QListWidgetItem, QDialog, QGroupBox, QSpacerItem, QProgressBar,QRadioButton, QFrame, QScrollArea, QFileDialog, QComboBox, QCheckBox, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QPushButton, QLineEdit, QTextEdit, QListWidget
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor, QFontDatabase, QPalette, QMouseEvent
import uitools

class ADBTools(QGroupBox):
    def __init__(self, name ,placement, iconlocation,desc, command, file, parentv, terminal,lineedit,runtime,safe):
        super().__init__()
        self.state = False
        self.safe = safe
        self.command = command
        self.lineedit = lineedit
        self.runtime = runtime
        self.parentv = parentv
        self.p = QLabel()
        self.files = file
        self.terminals = terminal
        self.placementrules = {"top":"border-top-left-radius: 20px ;border-top-right-radius: 20px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px",
                               "middle":"border-top-left-radius: 7px ;border-top-right-radius: 7px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px",
                               "bottom":"border-top-left-radius: 7px ;border-top-right-radius: 7px; border-bottom-right-radius: 20px; border-bottom-left-radius: 20px"}
        self.placement = placement
        
        self.l = QVBoxLayout()

        self.gt = TitleBox(name, iconlocation)
        self.l.addWidget(self.gt)
        self.gt.clicked.connect(self.showhide)

        self.g = QGroupBox()
        self.g.hide()
        self.gl = QVBoxLayout()
        self.g.setLayout(self.gl)
        self.gd = QLabel(desc)
        self.gd.setWordWrap(True)
        self.gd.setStyleSheet("font-size: 15px")
        self.gl.addWidget(self.gd)
        if self.lineedit != False:
            self.line = QLineEdit()
            self.linelabel = QLabel(self.lineedit)
            self.linel = QHBoxLayout()
            self.gl.addLayout(self.linel)
            self.linel.addWidget(self.linelabel)
            self.linel.addWidget(self.line)
        if self.files == True:
            self.ge = QHBoxLayout()
            self.gl.addLayout(self.ge)
            self.file = QLineEdit()
            self.filebutton = QPushButton("Select File")
            self.filebutton.clicked.connect(lambda:self.file.setText(QFileDialog.getOpenFileName(self,"Select a file","","Any (*.*)")[0]))
            self.ge.addWidget(self.file)
            self.file.setReadOnly(True)
            self.ge.addWidget(self.filebutton)
        self.logst = QLabel("LOGS:")
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.killbut = QPushButton("Kill")
        self.killbut.setStyleSheet("QPushButton { color: #ffffff; background-color: #880808; border-radius: 10; padding: 5} QPushButton::hover { color: #ffffff; background-color: #AA4A44; border-radius: 10; padding: 5}")
        self.killbut.clicked.connect(self.killp)
        self.logsh = QHBoxLayout()
        if self.terminals == True:
            self.gl.addLayout(self.logsh)
            self.logsh.addWidget(self.logst)
            self.logsh.addStretch()
            self.logsh.addWidget(self.killbut)
            self.gl.addWidget(self.logs)

        self.runbut = QPushButton("Excecute command")
        self.runbut.clicked.connect(self.run)
        self.gl.addWidget(self.runbut)
        self.l.addWidget(self.g)
        self.setLayout(self.l)
        self.setStyleSheet("QGroupBox{"+f"{self.placementrules[self.placement]};"+"background-color: "+uitools.colors["toolgb"][self.parentv.mode]+";} QPushButton { background-color: "+uitools.colors["line"][self.parentv.config["mode"]]+"; border-radius: 7px; padding: 5px} QPushButton::hover { background-color: #636363; border-radius: 7px; padding: 5px} QLineEdit { background-color: "+uitools.colors["line"][self.parentv.config["mode"]]+"; border-radius: 7px; padding: 5px}")

    def showhide(self):
        if self.runtime.isRunning != True:
            if self.state == True:
                self.g.hide()
                self.state = False
            elif self.state == False:
                for i in self.parentv.tools:
                    i.hidei()
                self.g.show()
                self.state = True

    def killp(self):
        self.runtime.kill()
        self.isRunning = False
        if self.runtime.curterminal != None:
            self.runtime.curterminal.append("<Killed process>")
        self.curterminal = None

    def showi(self):
        self.g.show()
        self.state = True

    def hidei(self):
        self.g.hide()
        self.state = False

    def run(self):
        if self.runtime.isRunning == False:
            if self.safe == False and self.parentv.config["safe"] == True:
                self.parentv.msg.showup("Cannot run this command, because Safe mode is on.\nIn order to use this tool you need to turn Safe mode off in settings.")
            else:
                self.logs.setText("")
                c = self.command
                if self.files == True:
                    c = c.replace("[file]",self.file.text())
                    self.file.setText("")
                if self.lineedit:
                    c = c.replace("[line]",self.line.text())
                    self.line.setText("")
                self.runtime.startc(c, self.logs)

class TitleBox(QGroupBox):
    clicked = pyqtSignal()
    def __init__(self,name, icon):
        super().__init__()
        self.setMaximumHeight(70)
        self.tl = QHBoxLayout()
        self.setLayout(self.tl)
        self.i = QPixmap(icon).scaled(50,50,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.p = QLabel()
        self.p.setPixmap(self.i)
        self.tl.addWidget(self.p)
        self.ft = QLabel(name)
        self.ft.setStyleSheet("font-size: 20px")
        self.tl.addWidget(self.ft)
        self.tl.addStretch()

    def mouseReleaseEvent(self, event: QMouseEvent):
        # Only trigger if left mouse button is released inside the widget
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)