# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LogIn.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName(_fromUtf8("Login"))
        Login.resize(371, 213)
        Login.setAcceptDrops(False)
        self.userNameLabel = QtGui.QLabel(Login)
        self.userNameLabel.setGeometry(QtCore.QRect(20, 50, 101, 16))
        self.userNameLabel.setObjectName(_fromUtf8("userNameLabel"))
        self.passwordLabel = QtGui.QLabel(Login)
        self.passwordLabel.setGeometry(QtCore.QRect(20, 100, 91, 21))
        self.passwordLabel.setObjectName(_fromUtf8("passwordLabel"))
        self.userNameLine = QtGui.QLineEdit(Login)
        self.userNameLine.setGeometry(QtCore.QRect(20, 70, 171, 27))
        self.userNameLine.setObjectName(_fromUtf8("userNameLine"))
        self.passwordLine = QtGui.QLineEdit(Login)
        self.passwordLine.setGeometry(QtCore.QRect(20, 120, 171, 27))
        self.passwordLine.setObjectName(_fromUtf8("passwordLine"))
        self.logInBtn = QtGui.QCommandLinkButton(Login)
        self.logInBtn.setGeometry(QtCore.QRect(20, 160, 81, 31))
        self.logInBtn.setObjectName(_fromUtf8("logInBtn"))
        self.signUpBtn = QtGui.QPushButton(Login)
        self.signUpBtn.setGeometry(QtCore.QRect(250, 30, 99, 27))
        self.signUpBtn.setObjectName(_fromUtf8("signUpBtn"))
        self.notAmemberLabel = QtGui.QLabel(Login)
        self.notAmemberLabel.setGeometry(QtCore.QRect(250, 10, 121, 20))
        self.notAmemberLabel.setObjectName(_fromUtf8("notAmemberLabel"))

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        Login.setWindowTitle(_translate("Login", "Form", None))
        self.userNameLabel.setText(_translate("Login", "UserName", None))
        self.passwordLabel.setText(_translate("Login", "PassWord", None))
        self.logInBtn.setText(_translate("Login", "Log in", None))
        self.signUpBtn.setText(_translate("Login", "Sign Up", None))
        self.notAmemberLabel.setText(_translate("Login", "Not A Member?", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Login = QtGui.QWidget()
    ui = Ui_Login()
    ui.setupUi(Login)
    Login.show()
    sys.exit(app.exec_())

