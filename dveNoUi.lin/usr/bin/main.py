import sys
import requests
import ast
import glob
import os.path
import json
import os

import shutil
import pathlib
from pathlib import Path
from colour import Color

from PyQt6 import QtGui
from PyQt6.QtGui import QIcon, QAction, QDesktopServices
from PyQt6.QtCore import Qt, pyqtSignal, QEvent, QTimer, QUrl
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QSystemTrayIcon, QMenu
from PyQt6.QtWidgets import QColorDialog, QDialog, QDialogButtonBox
from dveui import Ui_dveWindow
from confguiui import Ui_FormSettings



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS or _MEIPASS2
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
    # return os.path.join(relative_path)

def home_path(relative_path):
    home_dir = Path.home()
    home = str( home_dir )+"/"
    #return os.path.join(home, relative_path)+"/"
    return home+relative_path

class Dve(QMainWindow, Ui_dveWindow):

    def __init__(self, parent=None):
        super(Dve, self).__init__(parent)

        Ui_dveWindow.__init__(self)
        self.setupUi(self)

        self.setWindowTitle("DVE Escritorio")
        self.center()

        self.setWindowIcon(QIcon(resource_path("usr"+os.sep+"share"+os.sep+"img"+os.sep+"logo-ico.png")))

        self.searchButton.clicked.connect(lambda: self.instanceInput("no"))
        self.dveButton.clicked.connect(lambda: self.instanceInput("no"))
        self.dleButton.clicked.connect(lambda: self.instanceInput("no"))
        self.configButton.clicked.connect(self.abrirConfgui)
        self.infoButton.clicked.connect(self.showInfo)
        self.setFixedWidth(802)
        self.setFixedHeight(580)
        self.wordsList.setAutoScroll(True)
        self.dveInput.installEventFilter(self)

        # //////////// Theme selection ///////////
        with open(home_path(".config"+os.sep+"dve"+os.sep+"config.json")) as config:
            data = config.read()
        CONF = ast.literal_eval(data)
        self.THEME = CONF["THEME"]
        self.api_address = CONF["api_address"]
        THEME = self.THEME
        self.setThemeColors(THEME)

    def abrirConfgui(self):
        Confgui(parent=self).exec()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setThemeColors(self, THEME):
        path = home_path(".config"+os.sep+"dve"+os.sep+"themes"+os.sep+THEME+".json")
        checked = checkPath(path)
        if checked is True:
            with open(path) as f:
                data = f.read()
            theme = ast.literal_eval(data)
            col1 = theme["col1"]
            col2 = theme["col2"]
            fcol = theme["fcol"]
        else:
            col1 = "#e0f0ff"
            col2 = "#f6f5f4"
            fcol = "#3d3846"

        self.setStyleSheet("background-color:"+col1+";")
        self.dveInput.setStyleSheet(
            "background-color:"+col2+"; color:"+fcol+";")
        self.wordsList.setStyleSheet(
            "background-color:"+col2+"; color:"+fcol+";")
        self.resScreen.setStyleSheet("color:"+fcol+";")
        self.textDefiniciones.setStyleSheet(
            "background-color:"+col2+"; color:"+fcol+";")
        self.dveButton.setStyleSheet("color:"+fcol+";")
        self.dleButton.setStyleSheet("color:"+fcol+";")

    def instanceInput(self, from_keyevent):
        if from_keyevent == "no":
            sender = self.sender()
            source = str(sender.objectName())
            query = self.dveInput.text()
        elif from_keyevent == "yes":
            source = "keyevent"
            query = self.dveInput.text()

        if query != "":
            if source == "dveButton":
                s_address = "https://diccionariovariantesespa%C3%B1ol.org/glosario/itemlist/buscar?q="+query
                QDesktopServices.openUrl(QUrl(s_address))
                self.dveInput.clear()
            elif source == "dleButton":
                s_address = "https://dle.rae.es/?w="+query
                QDesktopServices.openUrl(QUrl(s_address))
                self.dveInput.clear()
            else:
                self.resScreen.setText("Buscando "+query+"...")
                self.launchSearch(query)
        else:
            self.resScreen.setText(
                "Consulta vacía. Por favor rellene el campo de busqueda.")
            QTimer.singleShot(3000, self.clearResScreen)

    def eventFilter(self, source, event):
        if source == self.dveInput and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return.value:
                self.instanceInput("yes")
            elif event.key() == Qt.Key.Key_Enter.value:
                self.instanceInput("yes")
        return super().eventFilter(source, event)

    def clearResScreen(self):
        self.resScreen.clear()

    def launchSearch(self, query):
        if self.api_address == "default":
            api_address = "https://xn--diccionariovariantesespaol-4rc.org/api/jsearch.php?q="
        else:
            api_address = self.api_address

        response = requests.get(api_address+query)
        self.json_data = response.json()
        json_data = self.json_data

        with open(home_path(".config"+os.sep+"dve"+os.sep+"temp"+os.sep+"temp.txt"), "w", errors="ignore") as data:
            data.write(str(json_data))

        self.dveInput.clear()
        self.textDefiniciones.clear()

        if json_data != []:
            self.populateWordsList(json_data)
            self.resScreen.setText("Resultados para la búsqueda: '"+query+"'")
        else:
            self.resScreen.setText("Lo sentimos pero no hay resultados para su búsqueda.")
            QTimer.singleShot(3000, self.clearResScreen)
            self.showRaeOption(query)

    def showRaeOption(self, query):
        html = ("<div style='text-align:center;'><br /><br /><br /><hr />"
                "<p>Lo sentimos, no hemos encontrado resultados para su búsqueda <b>'"+query+"'</b> en nuestra base de datos.</p>"
                "<p>Si lo desea pueda probar buscando en el Diccionario de la Lengua Española <b>DLe-RAE</b></p>"
                "<p><b><a href='https://dle.rae.es/?w="+query+"'>BUSCAR '"+query+"' en DLe</a></b></p>"
                "<hr />"
                "</div>")
        self.textDefiniciones.clear()
        self.wordsList.clear()
        self.textDefiniciones.setOpenExternalLinks(True)
        self.textDefiniciones.setHtml(html)

    def populateWordsList(self, json_data):
        self.wordsList.clear()
        for word in json_data:
            alias = word['alias']

            self.wordsList.addItem(alias)

        self.wordsList.itemClicked.connect(self.showDefinition)
        self.wordsList.itemActivated.connect(self.showDefinition)

    def showDefinition(self, item):
        id = self.wordsList.row(item)

        data = self.json_data
        titulo = data[id]['title']
        definicion = data[id]['introtext']

        self.textDefiniciones.clear()
        self.textDefiniciones.setOpenExternalLinks(True)
        self.textDefiniciones.setHtml("<b><u>"+titulo+"</u></b>\n\n"+definicion)

    def showInfo(self):
        html = ("<div style='text-align:center;'><br /><br /><hr />"
                "<p><b>Aplicación: </b>DVE - Escritorio</p>"
                "<p><b>Version: </b>1.23.4 Beta</p>"
                "<p><b>PyQt6 App </b></p>"
                "<p><b>Web: </b><a href='https://tinyurl.com/diccvar'>https://diccionariovariantesespañol.org</a></p>"
                "<p><b>Git: </b><a href='https://github.com/jernesten/DVE_Escritorio'>https://github.com/jernesten/DVE_Escritorio</a></p>"
                "<p><b>Autor: </b>Nacho González</p><hr />"
                "</div>")
        self.textDefiniciones.clear()
        self.wordsList.clear()
        self.textDefiniciones.setOpenExternalLinks(True)
        self.textDefiniciones.setHtml(html)

    def reloadTheme(self):
        with open(home_path(".config"+os.sep+"dve"+os.sep+"config.json")) as config:
            data = config.read()
        CONF = ast.literal_eval(data)
        THEME = CONF["THEME"]
        self.setThemeColors(THEME)


class CustomDialog(QDialog):
    def __init__(self, mensaje):
        super().__init__()

        self.setWindowTitle("Notificación!")
        self.setStyleSheet("background-color:#fcfcfc; color:#1c1c1c;")

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.No

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(mensaje)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class Confgui(QDialog, Ui_FormSettings):

    def __init__(self, parent=None):
        super(Confgui, self).__init__()
        self.parent = parent

        Ui_FormSettings.__init__(self)
        self.setupUi(self)

        self.setWindowTitle("DVE Escritorio - configuración")
        self.editorNotifications.setText("")
        self.trayCheckBox.stateChanged.connect(self.onStateChanged)

        self.setFixedWidth(542)
        self.setFixedHeight(476)

        # ////////// Theme selection /////////////
        with open(home_path(".config"+os.sep+"dve"+os.sep+"config.json")) as config:
            data = config.read()
        CONF = ast.literal_eval(data)
        self.THEME = CONF["THEME"]
        self.minToTray = CONF["minToTray"]
        THEME = self.THEME
        self.setThemeColors(THEME)
        self.setTrayOption()

        # //////////////////////////// BUTTONS
        self.cancelarButton.clicked.connect(self.exit)
        self.aceptarButton.clicked.connect(self.aceptarAction)

        self.color1Button.clicked.connect(self.onColorClick)
        self.color2Button.clicked.connect(self.onColorClick)
        self.fontColorButton.clicked.connect(self.onColorClick)

        self.borrarTemaButton.clicked.connect(self.borrarTemaAction)
        # //////////////////////////// BUTTONS END

        self.themeSelBox.currentTextChanged.connect(self.onThemeSelBox_changed)
        line1 = "lineCol1"
        line2 = "lineCol2"
        lineF = "lineFontCol"

        self.lineCol1.textChanged.connect(self.lineColChange)
        self.lineCol2.textChanged.connect(self.lineColChange)
        self.lineFontCol.textChanged.connect(self.lineColChange)

        self.listThemeFiles()
        self.populateNombreInput()

    def setThemeColors(self, THEME):

        with open(home_path(".config"+os.sep+"dve"+os.sep+"themes"+os.sep+THEME+".json")) as f:
            data = f.read()
        theme = ast.literal_eval(data)
        col1 = theme["col1"]
        col2 = theme["col2"]
        fcol = theme["fcol"]

        self.setStyleSheet("background-color:"+col1+";")
        self.marco0.setStyleSheet("background-color:"+col1+";")
        self.marco1.setStyleSheet("background-color:"+col1+";")
        self.marco2.setStyleSheet("background-color:"+col1+";")
        self.label0.setStyleSheet("color: "+fcol+";")
        self.label02.setStyleSheet("color: "+fcol+";")
        self.trayCheckBox.setStyleSheet("color: "+fcol+";")
        self.themeSelBox.setStyleSheet(
            "background-color:"+col2+"; color:"+fcol+";")
        self.infoBrowser.setStyleSheet(
            "background-color:"+col2+"; color:"+fcol+";")
        self.nombreInput.setStyleSheet(
            "background-color:"+col2+"; color:"+fcol+";")
        self.lineCol1.setStyleSheet(
            "background-color:"+col2+"; color:"+fcol+";")
        self.lineCol2.setStyleSheet(
            "background-color:"+col2+"; color:"+fcol+";")
        self.lineFontCol.setStyleSheet(
            "background-color:"+col2+"; color:"+fcol+";")
        self.borrarTemaButton.setStyleSheet(
            "background-color:"+col2+"; color:"+fcol+";")
        self.aceptarButton.setStyleSheet(
            "background-color:"+col2+"; color:"+fcol+";")
        self.cancelarButton.setStyleSheet(
            "background-color:"+col2+"; color:"+fcol+";")
        self.label1.setStyleSheet("color:"+fcol+";")
        self.label2.setStyleSheet("color:"+fcol+";")
        self.labelNombre.setStyleSheet("color:"+fcol+";")

        self.populateColors(col1, col2, fcol)

    def setTrayOption(self):
        if self.minToTray == "True":
            self.trayCheckBox.setCheckState(Qt.CheckState.Checked)
            self.trayCheckBox.setText("SI")
        if self.minToTray == "False":
            self.trayCheckBox.setCheckState(Qt.CheckState.Unchecked)
            self.trayCheckBox.setText("NO")

    def onStateChanged(self):
        file_address = home_path(".config"+os.sep+"dve"+os.sep+"config.json")
        with open(file_address) as theme_file:
            data = json.load(theme_file)
        if self.trayCheckBox.isChecked():
            data["minToTray"] = "True"
            self.trayCheckBox.setText("SI")
        else:
            data["minToTray"] = "False"
            self.trayCheckBox.setText("NO")

        with open(file_address, "w") as theme_file:
            json.dump(data, theme_file, indent=4)

    def lineColChange(self, text):
        sender = self.sender()
        source = str(sender.objectName())
        if self.check_color(text) is True:
            if source == "lineCol1":
                self.color1Button.setIcon(QIcon(""))
                self.color1Button.setStyleSheet("background-color:"+ text +";")
                self.threeColorsGood()
            elif source == "lineCol2":
                self.color2Button.setIcon(QIcon(""))
                self.color2Button.setStyleSheet("background-color:"+ text +";")
                self.threeColorsGood()
            elif source == "lineFontCol":
                self.fontColorButton.setIcon(QIcon(""))
                self.fontColorButton.setStyleSheet("background-color:"+ text +";")
                self.threeColorsGood()
        else:
            if source == "lineCol1":
                self.color1Button.setIcon(QIcon(resource_path("usr"+os.sep+"share"+os.sep+"img"+os.sep+"stop.png")))
                self.color1Button.setStyleSheet("background-color:white;")
                self.threeColorsGood()
            elif source == "lineCol2":
                self.color2Button.setIcon(QIcon(resource_path("usr"+os.sep+"share"+os.sep+"img"+os.sep+"stop.png")))
                self.color2Button.setStyleSheet("background-color:white;")
                self.threeColorsGood()
            elif source == "lineFontCol":
                self.fontColorButton.setIcon(QIcon(resource_path("usr"+os.sep+"share"+os.sep+"img"+os.sep+"stop.png")))
                self.fontColorButton.setStyleSheet("background-color:white;")
                self.threeColorsGood()

    def threeColorsGood(self):
        col1 = self.check_color(self.lineCol1.text())
        col2 = self.check_color(self.lineCol2.text())
        col3 = self.check_color(self.lineFontCol.text())
        if (col1 is True) and (col2 is True) and (col3 is True):
            self.aceptarButton.setEnabled(True)
            self.editorNotifications.setText("")
        else:
            self.aceptarButton.setEnabled(False)
            self.editorNotifications.setText("Color erroneo. Aceptar bloqueado.")

    def check_color(self, color_str):
        try:
            color = str(color_str).replace(" ","")
            Color(color)
            return True
        except AttributeError:
            return False
        except ValueError:
            return False

    def listThemeFiles(self):
        path = home_path(".config"+os.sep+"dve"+os.sep+"themes"+os.sep)
        theme_files = glob.glob(path+"*.json", recursive=False)
        assert isinstance(theme_files, list)
        self.addThemeFilesBox(theme_files)

    def addThemeFilesBox(self, theme_files):
        self.themeSelBox.clear()
        self.themeSelBox.addItems(theme_files)

        self.populateThemeBox(theme_files)

    def populateThemeBox(self, theme_files):
        THEME = self.THEME
        myTheme = home_path(".config"+os.sep+"dve"+os.sep+"themes"+os.sep+THEME+".json")
        self.themeSelBox.setCurrentIndex(theme_files.index(myTheme))

    def onThemeSelBox_changed(self, value):
        theme_file = value.rsplit(os.sep, 1)[1]
        themeName = theme_file.rsplit(".", 1)[0]

        self.nombreInput.setText(themeName)
        with open(value) as theme:
            data = theme.read()
        MyTheme = ast.literal_eval(data)
        col1 = MyTheme["col1"]
        col2 = MyTheme["col2"]
        fcol = MyTheme["fcol"]

        self.populateColors(col1, col2, fcol)
        self.setThemeColors(themeName)
        print(value)

    def populateNombreInput(self):
        myTheme = self.THEME
        self.nombreInput.setText(myTheme)

    def populateColors(self, col1, col2, fcol):
        self.lineCol1.setText(col1)
        self.lineCol2.setText(col2)
        self.lineFontCol.setText(fcol)

        self.color1Button.setStyleSheet("background-color:"+col1+";")
        self.color2Button.setStyleSheet("background-color:"+col2+";")
        self.fontColorButton.setStyleSheet("background-color:"+fcol+";")

    def aceptarAction(self):
        fileName = self.nombreInput.text()
        col1 = self.lineCol1.text()
        col2 = self.lineCol2.text()
        fcol = self.lineFontCol.text()

        file_exists = os.path.exists(home_path(".config"+os.sep+"dve"+os.sep+"themes"+os.sep+fileName+".json"))
        if file_exists is True:
            file_address = home_path(".config"+os.sep+"dve"+os.sep+"themes"+os.sep+fileName+".json")
            with open(file_address) as theme:
                data = theme.read()
            MyTheme = ast.literal_eval(data)
            fileCol1 = MyTheme["col1"]
            fileCol2 = MyTheme["col2"]
            fileFcol = MyTheme["fcol"]
            if (
                col1 == fileCol1) and (
                col2 == fileCol2) and (
                    fcol == fileFcol):
                file_address = home_path(".config"+os.sep+"dve"+os.sep+"config.json")
                with open(file_address) as theme_file:
                    data = json.load(theme_file)
                data["THEME"] = fileName
                with open(file_address, "w") as theme_file:
                    json.dump(data, theme_file, indent=4)

                self.exit()
                self.parent.reloadTheme()
            else:
                self.dialogSobrescribir()
        else:
            self.guardarTema(fileName)

    def guardarTema(self, fileName):
        x =  {
            "col1" : self.lineCol1.text(),
            "col2" : self.lineCol2.text(),
            "fcol" : self.lineFontCol.text()
        }
        with open(home_path(".config"+os.sep+"dve"+os.sep+"themes"+os.sep+fileName+".json", "w")) as new_file:
            json.dump(x, new_file, indent=4)
        THEME = fileName
        self.exit()
        self.reloadConfgui()

    def removeNotification(self):
        self.editorNotifications.clear()

    def onColorClick(self):
        sending_button = self.sender()
        whichButton = str(sending_button.objectName())
        self.openColorDialog(whichButton)

    def openColorDialog(self, whichButton):
        color = QColorDialog.getColor()

        if color.isValid():
            if whichButton == "color1Button":
                self.lineCol1.setText(color.name())
                self.color1Button.setStyleSheet(
                    "background-color:"+color.name()+";")
            if whichButton == "color2Button":
                self.lineCol2.setText(color.name())
                self.color2Button.setStyleSheet(
                    "background-color:"+color.name()+";")
            if whichButton == "fontColorButton":
                self.lineFontCol.setText(color.name())
                self.fontColorButton.setStyleSheet(
                    "background-color:"+color.name()+";")

    def borrarTemaAction(self):
        inUseTheme = self.THEME
        fileName = self.nombreInput.text()
        if inUseTheme == fileName:
            self.editorNotifications.setText("Tema actualmente en uso, no puede borrarse.")
            QTimer.singleShot(2000, self.removeNotification)
        else:
            file_exists = os.path.exists(home_path(".config"+os.sep+"dve"+os.sep+"themes"+os.sep+fileName+".json"))
            if file_exists is True:
                self.dialogBorrar()
            else:
                self.editorNotifications.setText("El tema seleccionado no existe.")
                QTimer.singleShot(2000, self.removeNotification)

    def dialogBorrar(self):
        tema = self.nombreInput.text()
        mensaje = "\nEstá apunto de borrar el tema: "+ tema +"\n¿Seguro que desea continuar?\n"
        tema_p = "themes"+os.sep+tema+".json"

        dlg = CustomDialog(mensaje)
        if dlg.exec():
            self.borrarTema(tema_p)
        else:
            self.editorNotifications.setText("Borrar el tema 'Cancelado'")
            QTimer.singleShot(2000, self.removeNotification)

    def borrarTema(self, path):
        os.remove(path)
        self.reloadConfgui()

    def reloadConfgui(self):
        self.exit()
        self.parent.abrirConfgui()

    def dialogSobrescribir(self):
        tema = self.nombreInput.text()
        mensaje = "\nEl tema: "+ tema + " ya existe. Si continua, este se sobrescribirá.\n¿Seguro que desea continuar?\n"
        tema_p = ".config"+os.sep+"dve"+os.sep+"themes"+os.sep+tema+".json"

        dlg = CustomDialog(mensaje)
        if dlg.exec():
            self.sobrescribirTema(tema_p, tema)
        else:
            self.editorNotifications.setText("Sobrescribir el tema 'Cancelado'")
            QTimer.singleShot(2000, self.removeNotification)

    def sobrescribirTema(self, tema_p, tema):
        file_address = tema_p
        col1 = self.lineCol1.text()
        col2 = self.lineCol2.text()
        fcol = self.lineFontCol.text()
        with open(file_address) as f:
            data = json.load(f)
        data["col1"] = col1
        data["col2"] = col2
        data["fcol"] = fcol
        with open(file_address, "w") as updated_file:
            json.dump(data, updated_file, indent=4)

        THEME = tema
        self.setThemeColors(THEME)

    def exit(self):
        self.close()


def checkPath(path):
    if os.path.exists(path):
        return True
    else:
        return False

def checkExternalFiles():
    files = {
        resource_path("usr"+os.sep+"share"+os.sep+"config"+os.sep+"config.json") : home_path(".config"+os.sep+"dve"+os.sep),
        #check temp dir
        resource_path("usr"+os.sep+"share"+os.sep+"temp"+os.sep) : home_path(".config"+os.sep+"dve"+os.sep+"temp"+os.sep),
        #check themes dir
        resource_path("usr"+os.sep+"share"+os.sep+"themes"+os.sep) : home_path(".config"+os.sep+"dve"+os.sep+"themes"+os.sep),
    }

    for item in files:
        element = checkPath(files[item])
        if element is False:
            inpath = item
            expath = files[item]
            createExternalFile(inpath, expath)

def createExternalFile(inpath, expath):
    if inpath == resource_path("usr"+os.sep+"share"+os.sep+"temp"+os.sep) or inpath == resource_path("usr"+os.sep+"share"+os.sep+"themes"+os.sep):
        src = inpath
        dst = expath
        shutil.copytree(src, dst)

    else:
        dir_path = expath.rsplit("/", 1)[0]
        dp = checkPath(dir_path)
        if dp is False:
            pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
        src = inpath
        dst = expath
        shutil.copy(src, dst)

checkExternalFiles()


def main():
    app = QApplication(sys.argv)
    dve = Dve()
    with open(home_path(".config"+os.sep+"dve"+os.sep+"config.json")) as config:
        data = config.read()
    CONF = ast.literal_eval(data)
    tray = CONF["minToTray"]

    if tray == "True":
        app.setQuitOnLastWindowClosed(False)
        icon = QIcon(resource_path("usr"+os.sep+"share"+os.sep+"img"+os.sep+"logo-ico.png"))

        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)
        tray.activated.connect(dve.show)

        menu = QMenu()

        abrir = QAction("Abrir")
        abrir.triggered.connect(dve.show)

        toTray = QAction("Minimizar")
        toTray.triggered.connect(dve.close)

        settings = QAction("Configuración")
        settings.triggered.connect(dve.abrirConfgui)

        quit = QAction("Quit")
        quit.triggered.connect(app.quit)

        menu.addAction(abrir)
        menu.addAction(toTray)
        menu.addAction(settings)
        menu.addAction(quit)

        # Adding options to the System Tray
        tray.setContextMenu(menu)

    # qss for scrollbars
    app.setStyleSheet(
        "QScrollBar:vertical {border-radius : 5px; width: 10px;}"
        "QScrollBar:horizontal {border-radius : 5px;height: 10px;}"
        "QScrollBar::handle:vertical, QScrollBar::handle:horizontal {border-radius : 5px; background-color: #2E85BC; min-height: 80px; width : 12px;}"
        "QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {background-color: #2E85BC;}"
        "QScrollBar::add-line:vertical, QScrollBar::add-line:horizontal {background: transparent; height: 0px; subcontrol-position: bottom; subcontrol-origin: margin;}"
        "QScrollBar::add-line:vertical:hover, QScrollBar::add-line:horizontal:hover {background-color: transparent;}"
        "QScrollBar::add-line:vertical:pressed, QScrollBar::add-line:horizontal:pressed {background-color: #3f3f3f;}"
        "QScrollBar::sub-line:vertical, QScrollBar::sub-line:horizontal {background: transparent; height: 0px; }"
        "QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:horizontal:hover{background-color: transparent;}"
        "QScrollBar::sub-line:vertical:pressed, QScrollBar::sub-line:horizontal:pressed{background-color: #3f3f3f;}"
        "QScrollBar::up-arrow:vertical,QScrollBar::up-arrow:horizontal{width: 0px; height: 0px; background: transparent;}"
        "QScrollBar::down-arrow:vertical, QScrollBar::down-arrow:horizontal{width: 0px; height: 0px; background: transparent;}"
        "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical, QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal{background-color: transparent;}"
        )

    dve.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
