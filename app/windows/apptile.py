from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QSizePolicy,QListWidgetItem, QDialog, QGroupBox, QSpacerItem, QProgressBar,QRadioButton, QFrame, QScrollArea, QFileDialog, QComboBox, QCheckBox, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QPushButton, QLineEdit, QTextEdit, QListWidget
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor, QFontDatabase, QPalette, QMouseEvent
import uitools

class AppTile(QGroupBox):
    def __init__(self, name, type, parentv, runtime,placement):
        super().__init__()
        self.state = False
        self.name = name
        self.placement = placement
        self.typeapp = type
        self.runtime = runtime
        self.parentv = parentv
        self.placementrules = {"top":"border-top-left-radius: 20px ;border-top-right-radius: 20px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px",
                               "middle":"border-top-left-radius: 7px ;border-top-right-radius: 7px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px",
                               "bottom":"border-top-left-radius: 7px ;border-top-right-radius: 7px; border-bottom-right-radius: 20px; border-bottom-left-radius: 20px"}
        self.rules = {"3":"Safe","s":"risky","d":"idk"}
        
        self.l = QVBoxLayout()

        self.gt = TitleBox(name,self.typeapp)
        self.l.addWidget(self.gt)
        self.gt.clicked.connect(self.showhide)

        self.g = QGroupBox()
        self.g.hide()
        self.gl = QVBoxLayout()
        self.g.setLayout(self.gl)
        self.gd = QLabel(self.rules[self.typeapp])
        self.gd.setWordWrap(True)
        self.gd.setStyleSheet("font-size: 15px")
        self.gl.addWidget(self.gd)

        self.runbut1 = QPushButton("Excecute command")
        self.runbut1.clicked.connect(self.run1)
        self.gl.addWidget(self.runbut1)
        self.runbut2 = QPushButton("Disable")
        self.runbut2.clicked.connect(self.run2)
        if self.typeapp == "3": self.gl.addWidget(self.runbut2)

        self.runbut1.setText({"3":"Uninstall","s":"Disable","d":"Enable"}[self.typeapp])
        self.l.addWidget(self.g)
        self.setLayout(self.l)
        self.setStyleSheet("QGroupBox{"+f"{self.placementrules[self.placement]};"+"background-color: "+uitools.colors["toolgb"][self.parentv.mode]+";} QPushButton { background-color: "+uitools.colors["line"][self.parentv.config["mode"]]+"; border-radius: 7px; padding: 5px} QPushButton::hover { background-color: #636363; border-radius: 7px; padding: 5px} QLineEdit { background-color: "+uitools.colors["line"][self.parentv.config["mode"]]+"; border-radius: 7px; padding: 5px}")

    def showhide(self):
        if self.runtime.isRunning != True:
            if self.state == True:
                self.g.hide()
                self.state = False
            elif self.state == False:
                self.g.show()
                self.state = True

    def showi(self):
        self.g.show()
        self.state = True

    def hidei(self):
        self.g.hide()
        self.state = False

    def run1(self):
        if self.runtime.isRunning == False:
            self.parentv.applogs.setText("")
            if self.typeapp == "3":
                self.runtime.startc(f"adb uninstall {self.name}",self.parentv.applogs)
            if self.typeapp == "s":
                if self.parentv.config["safe"] == True:
                    self.parentv.msg.showup("Cannot run this command, because Safe mode is on.\nIn order to use this tool you need to turn Safe mode off in settings.")
                else:
                    self.runtime.startc(f"adb shell pm disable-user --user 0 {self.name}",self.parentv.applogs)
            if self.typeapp == "d":
                if self.parentv.config["safe"] == True:
                    self.parentv.msg.showup("Cannot run this command, because Safe mode is on.\nIn order to use this tool you need to turn Safe mode off in settings.")
                else:
                    self.runtime.startc(f"adb shell pm enable {self.name}",self.parentv.applogs)

    def run2(self):
        if self.runtime.isRunning == False:
            if self.typeapp == "3":
                self.runtime.startc(f"adb shell pm disable-user --user 0 {self.name}",self.parentv.applogs)
            
class TitleBox(QGroupBox):
    clicked = pyqtSignal()
    def __init__(self,name, typeapp):
        super().__init__()
        self.setMaximumHeight(70)
        self.tl = QHBoxLayout()
        self.setLayout(self.tl)
        self.ft = QLineEdit(name)
        self.ft.setReadOnly(True)
        self.ft.setStyleSheet("font-size: 20px")
        self.tl.addWidget(self.ft)
        self.typel = QLabel(alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.tl.addWidget(self.typel)
        if typeapp == '3':
            self.typel.setText("3rd party app")
            self.typel.setStyleSheet("font-size: 15px; color: #097969")
        if typeapp == 's':
            self.typel.setText("System app")
            self.typel.setStyleSheet("font-size: 15px; color:#006796")
        if typeapp == 'd':
            self.typel.setText("Disabled app")
            self.typel.setStyleSheet("font-size: 15px; color: #800020")

    def mouseReleaseEvent(self, event: QMouseEvent):
        # Only trigger if left mouse button is released inside the widget
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)