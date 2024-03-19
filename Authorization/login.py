from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_authorization(object):
    def setupUi(self, authorization):
        authorization.setObjectName("authorization")
        authorization.resize(300, 200)
        authorization.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(authorization)
        self.centralwidget.setObjectName("centralwidget")

        self.exitlog = QtWidgets.QPushButton(self.centralwidget)
        self.exitlog.setGeometry(QtCore.QRect(2, 2, 50, 18))
        self.exitlog.setStyleSheet("background-color: #FFFFFF\n""")
        self.exitlog.setObjectName("exitlog")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 231, 51))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 0, 0);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 231, 51))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_2.setObjectName("label_2")
        self.loginbtn = QtWidgets.QPushButton(self.centralwidget)
        self.loginbtn.setGeometry(QtCore.QRect(120, 120, 70, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.loginbtn.setFont(font)
        self.loginbtn.setStyleSheet("background-color: #FFFFFF;\n"
"border:2px solid #2f6887;\n"
"border-radius: 30;")
        self.loginbtn.setObjectName("loginbtn")
        self.input_login = QtWidgets.QLineEdit(self.centralwidget)
        self.input_login.setGeometry(QtCore.QRect(93, 37, 160, 20))
        self.input_login.setStyleSheet("color: rgb(0, 0, 0);")
        self.input_login.setObjectName("input_login")
        self.input_password = QtWidgets.QLineEdit(self.centralwidget)
        self.input_password.setGeometry(QtCore.QRect(98, 77, 160, 20))
        self.input_password.setStyleSheet("color: rgb(0, 0, 0);")
        self.input_password.setObjectName("input_password")
        authorization.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(authorization)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 489, 21))
        self.menubar.setObjectName("menubar")
        authorization.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(authorization)
        self.statusbar.setObjectName("statusbar")
        authorization.setStatusBar(self.statusbar)

        self.retranslateUi(authorization)
        QtCore.QMetaObject.connectSlotsByName(authorization)

    def retranslateUi(self, authorization):
        _translate = QtCore.QCoreApplication.translate
        authorization.setWindowTitle(_translate("authorization", "Окно авторизации"))
        self.exitlog.setText(_translate("authorization", "Выйти"))
        self.label.setText(_translate("authorization", "Введите логин:"))
        self.label_2.setText(_translate("authorization", "Введите пароль:"))
        self.loginbtn.setText(_translate("authorization", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    authorization = QtWidgets.QMainWindow()
    ui = Ui_authorization()
    ui.setupUi(authorization)
    authorization.show()
    sys.exit(app.exec())
