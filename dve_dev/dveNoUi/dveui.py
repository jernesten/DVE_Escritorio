# Form implementation generated from reading ui file 'ui/dve.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dveWindow(object):
    def setupUi(self, dveWindow):
        dveWindow.setObjectName("dveWindow")
        dveWindow.resize(802, 580)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/logo-ico.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dveWindow.setWindowIcon(icon)
        dveWindow.setStyleSheet("")
        self.label = QtWidgets.QLabel(parent=dveWindow)
        self.label.setGeometry(QtCore.QRect(0, 0, 802, 82))
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.label.setLineWidth(0)
        self.label.setText("")
        self.label.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.label.setPixmap(QtGui.QPixmap("img/logo.png"))
        self.label.setScaledContents(True)
        self.label.setIndent(0)
        self.label.setObjectName("label")
        self.dveInput = QtWidgets.QLineEdit(parent=dveWindow)
        self.dveInput.setGeometry(QtCore.QRect(10, 95, 782, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.dveInput.setFont(font)
        self.dveInput.setStyleSheet("padding: 0 5px;")
        self.dveInput.setText("")
        self.dveInput.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.dveInput.setObjectName("dveInput")
        self.textDefiniciones = QtWidgets.QTextBrowser(parent=dveWindow)
        self.textDefiniciones.setGeometry(QtCore.QRect(270, 165, 521, 401))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(False)
        self.textDefiniciones.setFont(font)
        self.textDefiniciones.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.textDefiniciones.setObjectName("textDefiniciones")
        self.wordsList = QtWidgets.QListWidget(parent=dveWindow)
        self.wordsList.setGeometry(QtCore.QRect(10, 165, 251, 401))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.wordsList.setFont(font)
        self.wordsList.setObjectName("wordsList")
        self.resScreen = QtWidgets.QLabel(parent=dveWindow)
        self.resScreen.setGeometry(QtCore.QRect(20, 140, 561, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(True)
        self.resScreen.setFont(font)
        self.resScreen.setText("")
        self.resScreen.setObjectName("resScreen")
        self.configButton = QtWidgets.QPushButton(parent=dveWindow)
        self.configButton.setGeometry(QtCore.QRect(770, 140, 21, 21))
        self.configButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.configButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/gear.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.configButton.setIcon(icon1)
        self.configButton.setObjectName("configButton")
        self.infoButton = QtWidgets.QPushButton(parent=dveWindow)
        self.infoButton.setGeometry(QtCore.QRect(745, 140, 21, 21))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/i.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.infoButton.setIcon(icon2)
        self.infoButton.setObjectName("infoButton")
        self.searchButton = QtWidgets.QPushButton(parent=dveWindow)
        self.searchButton.setGeometry(QtCore.QRect(756, 100, 31, 31))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("img/search.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.searchButton.setIcon(icon3)
        self.searchButton.setObjectName("searchButton")
        self.dleButton = QtWidgets.QPushButton(parent=dveWindow)
        self.dleButton.setGeometry(QtCore.QRect(720, 140, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setItalic(False)
        self.dleButton.setFont(font)
        self.dleButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.dleButton.setObjectName("dleButton")
        self.dveButton = QtWidgets.QPushButton(parent=dveWindow)
        self.dveButton.setGeometry(QtCore.QRect(695, 140, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.dveButton.setFont(font)
        self.dveButton.setObjectName("dveButton")

        self.retranslateUi(dveWindow)
        QtCore.QMetaObject.connectSlotsByName(dveWindow)

    def retranslateUi(self, dveWindow):
        _translate = QtCore.QCoreApplication.translate
        dveWindow.setWindowTitle(_translate("dveWindow", "Form"))
        self.label.setToolTip(_translate("dveWindow", "<html><head/><body><p><a href=\"https://diccionariovariantesespañol.org\"><span style=\" text-decoration: underline; color:#ffffff;\">https://diccionariovariantesespañol.org</span></a></p></body></html>"))
        self.dveInput.setPlaceholderText(_translate("dveWindow", "Buscar en DVE"))
        self.textDefiniciones.setToolTip(_translate("dveWindow", "info"))
        self.wordsList.setSortingEnabled(False)
        self.configButton.setToolTip(_translate("dveWindow", "<html><head/><body><p>Preferences</p></body></html>"))
        self.infoButton.setToolTip(_translate("dveWindow", "<html><head/><body><p>Info</p></body></html>"))
        self.searchButton.setToolTip(_translate("dveWindow", "<html><head/><body><p>Info</p></body></html>"))
        self.dleButton.setToolTip(_translate("dveWindow", "<html><head/><body><p>Preferences</p></body></html>"))
        self.dleButton.setText(_translate("dveWindow", "DLE"))
        self.dveButton.setToolTip(_translate("dveWindow", "<html><head/><body><p>Info</p></body></html>"))
        self.dveButton.setText(_translate("dveWindow", "DVE"))