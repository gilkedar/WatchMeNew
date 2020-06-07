# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WatchMe.ui'
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

class Ui_WatchMe(object):
    def setupUi(self, WatchMe):
        WatchMe.setObjectName(_fromUtf8("WatchMe"))
        WatchMe.resize(998, 784)
        self.TabsObject = QtGui.QTabWidget(WatchMe)
        self.TabsObject.setGeometry(QtCore.QRect(10, 110, 941, 571))
        self.TabsObject.setObjectName(_fromUtf8("TabsObject"))
        self.MostPopular = QtGui.QWidget()
        self.MostPopular.setObjectName(_fromUtf8("MostPopular"))
        self.gridLayoutWidget = QtGui.QWidget(self.MostPopular)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 19, 921, 281))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.columnView = QtGui.QColumnView(self.MostPopular)
        self.columnView.setGeometry(QtCore.QRect(10, 320, 256, 192))
        self.columnView.setObjectName(_fromUtf8("columnView"))
        self.listWidget = QtGui.QListWidget(self.MostPopular)
        self.listWidget.setGeometry(QtCore.QRect(330, 320, 256, 192))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.tableWidget = QtGui.QTableWidget(self.MostPopular)
        self.tableWidget.setGeometry(QtCore.QRect(630, 320, 256, 192))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.TabsObject.addTab(self.MostPopular, _fromUtf8(""))
        self.MostRecent = QtGui.QWidget()
        self.MostRecent.setObjectName(_fromUtf8("MostRecent"))
        self.listView = QtGui.QListView(self.MostRecent)
        self.listView.setGeometry(QtCore.QRect(10, 10, 256, 341))
        self.listView.setObjectName(_fromUtf8("listView"))
        self.frame = QtGui.QFrame(self.MostRecent)
        self.frame.setGeometry(QtCore.QRect(330, 20, 571, 331))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.TabsObject.addTab(self.MostRecent, _fromUtf8(""))
        self.toolButton = QtGui.QToolButton(WatchMe)
        self.toolButton.setGeometry(QtCore.QRect(900, 20, 51, 31))
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.pushButton = QtGui.QPushButton(WatchMe)
        self.pushButton.setGeometry(QtCore.QRect(10, 700, 99, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.DownloadBtn = QtGui.QCommandLinkButton(WatchMe)
        self.DownloadBtn.setGeometry(QtCore.QRect(790, 700, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.DownloadBtn.setFont(font)
        self.DownloadBtn.setObjectName(_fromUtf8("DownloadBtn"))
        self.WelcomeLabel = QtGui.QLabel(WatchMe)
        self.WelcomeLabel.setGeometry(QtCore.QRect(30, 20, 68, 17))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.WelcomeLabel.setFont(font)
        self.WelcomeLabel.setObjectName(_fromUtf8("WelcomeLabel"))
        self.LastVisitLabel = QtGui.QLabel(WatchMe)
        self.LastVisitLabel.setGeometry(QtCore.QRect(30, 60, 91, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.LastVisitLabel.setFont(font)
        self.LastVisitLabel.setObjectName(_fromUtf8("LastVisitLabel"))

        self.retranslateUi(WatchMe)
        self.TabsObject.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(WatchMe)

    def retranslateUi(self, WatchMe):
        WatchMe.setWindowTitle(_translate("WatchMe", "Form", None))
        self.TabsObject.setTabText(self.TabsObject.indexOf(self.MostPopular), _translate("WatchMe", "Tab 1", None))
        self.TabsObject.setTabText(self.TabsObject.indexOf(self.MostRecent), _translate("WatchMe", "Tab 2", None))
        self.toolButton.setText(_translate("WatchMe", "...", None))
        self.pushButton.setText(_translate("WatchMe", "Close", None))
        self.DownloadBtn.setText(_translate("WatchMe", "Download", None))
        self.WelcomeLabel.setText(_translate("WatchMe", "Hello ", None))
        self.LastVisitLabel.setText(_translate("WatchMe", "Last Visit", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    WatchMe = QtGui.QWidget()
    ui = Ui_WatchMe()
    ui.setupUi(WatchMe)
    WatchMe.show()
    sys.exit(app.exec_())

