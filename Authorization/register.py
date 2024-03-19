from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_registration(object):
    def setupUi(self, registration):
        registration.setObjectName("registration")
        registration.resize(300, 200)
        registration.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(registration)
        self.centralwidget.setObjectName("centralwidget")

        self.exitreg = QtWidgets.QPushButton(self.centralwidget)
        self.exitreg.setGeometry(QtCore.QRect(2, 2, 50, 18))
        self.exitreg.setStyleSheet("background-color: #FFFFFF\n""")
        self.exitreg.setObjectName("exitreg")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 231, 51))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0,0, 0);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 231, 51))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_2.setObjectName("label_2")
        self.regbtn = QtWidgets.QPushButton(self.centralwidget)
        self.regbtn.setGeometry(QtCore.QRect(120, 120, 70, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.regbtn.setFont(font)
        self.regbtn.setStyleSheet("background-color: #FFFFFF;\n"
"border:2px solid #2f6887;\n"
"border-radius: 0;")
        self.regbtn.setObjectName("regbtn")
        self.new_login = QtWidgets.QLineEdit(self.centralwidget)
        self.new_login.setGeometry(QtCore.QRect(93, 37, 160, 20))
        self.new_login.setStyleSheet("color: rgb(0, 0, 0);")
        self.new_login.setObjectName("new_login")
        self.new_pass = QtWidgets.QLineEdit(self.centralwidget)
        self.new_pass.setGeometry(QtCore.QRect(98, 77, 160, 20))
        self.new_pass.setStyleSheet("color: rgb(0, 0, 0);")
        self.new_pass.setObjectName("new_pass")
        registration.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(registration)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 552, 21))
        self.menubar.setObjectName("menubar")
        registration.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(registration)
        self.statusbar.setObjectName("statusbar")
        registration.setStatusBar(self.statusbar)

        self.retranslateUi(registration)
        QtCore.QMetaObject.connectSlotsByName(registration)

    def retranslateUi(self, registration):
        _translate = QtCore.QCoreApplication.translate
        registration.setWindowTitle(_translate("registration", "Окно регистрации"))
        self.exitreg.setText(_translate("authorization", "Выйти"))
        self.label.setText(_translate("registration", "Введите логин:"))
        self.label_2.setText(_translate("registration", "Введите пароль:"))
        self.regbtn.setText(_translate("registration", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    registration = QtWidgets.QMainWindow()
    ui = Ui_registration()
    ui.setupUi(registration)
    registration.show()
    sys.exit(app.exec())
