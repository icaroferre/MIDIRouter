#!/usr/bin/python3

import mido
import mido.backends.portmidi
from PyQt5.QtWidgets import (QComboBox, QLineEdit, QSlider, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QLabel)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from objc import pathForFramework, loadBundle
import sys
import os
from pathlib import Path
import plistlib

"""
MIDIROUTER
DEVELOPED BY ICARO FERRE 

SPEKTRO AUDIO
http://spektroaudio.com/
"""


available_input_ports = mido.get_input_names()
available_output_ports = mido.get_output_names()

print(sys.executable)
print(os.path.dirname(os.path.abspath(__file__)))

basedir = sys.executable
app_dir = basedir.rfind("/")
basedir = basedir[:app_dir]
basedir = str(Path(basedir).parent)



try:
    pl = plistlib.readPlist(basedir + '/Info.plist')
    appversionNumber = str(pl["CFBundleShortVersionString"])
except FileNotFoundError:
    appversionNumber = "0.0"

iconImage = 'icon.png'
titleImage = basedir + '/Resources/title.png'

app = QApplication(sys.argv)

class Window(QWidget):
    def __init__ (self):
        super().__init__()
        self.init_ui()

    def init_ui(self):


        self.midi_input = QComboBox(self)
        for i in available_input_ports:
            self.midi_input.addItem(i)
        self.midi_input.setCurrentIndex(0)

        self.midi_output = QComboBox(self)
        for i in available_output_ports:
            self.midi_output.addItem(i)
        self.midi_output.setCurrentIndex(0)

        input_box = QHBoxLayout()
        input_box.addWidget(QLabel("MIDI In Port:"))
        input_box.addWidget(self.midi_input)

        output_box = QHBoxLayout()
        output_box.addWidget(QLabel("MIDI Out Port:"))
        output_box.addWidget(self.midi_output)      

        top_box = QHBoxLayout()
        topImage = QLabel()
        topImage.setPixmap(QtGui.QPixmap(titleImage).scaledToWidth(113, Qt.SmoothTransformation))
        top_box.addStretch()
        top_box.addWidget(topImage) 
        top_box.addStretch()
        
        dev_box = QHBoxLayout()
        developer = QLabel("Developed by Icaro Ferre")
        developer.setStyleSheet('color: gray')      
        dev_box.addStretch()
        dev_box.addWidget(developer)    
        dev_box.addStretch()

        version_box = QHBoxLayout()
        # version = QLabel("Version: " + appversionNumber)
        version =  QLabel(basedir)
        version.setStyleSheet('color: gray')        
        version_box.addStretch()
        version_box.addWidget(version)  
        version_box.addStretch()


        v_box = QVBoxLayout()
        v_box.addLayout(top_box)
        v_box.addLayout(version_box)
        v_box.addLayout(dev_box)
        v_box.addLayout(input_box)
        v_box.addLayout(output_box)

        self.bu = QPushButton("Check for Update")

        self.bu.clicked.connect(self.checkUpdate)

        # v_box.addWidget(self.bu)
        # v_box.addWidget(QLabel('/Frameworks/Sparkle.framework'))

        self.midi_input.activated[str].connect(self.inputSel)
        self.midi_output.activated[str].connect(self.outputSel)

        self.setLayout(v_box)

        self.setWindowTitle("MIDI Router")

        self.show()

    def inputSel(self, text):
        changeinputPort(text)

    def outputSel(self, text):
        changeoutputPort(text)

    def checkUpdate(self):
        print("Checking for Updates...")
        sparkle.checkForUpdatesInBackground()

def InMSG(message):
    try:
        global outputPort
        outputPort.send(message)
    except NameError:
        print("No port selected.")

def changeinputPort(x):
    global inputPort
    try:
        inputPort.close()
    except NameError:
        pass
    inputPort = mido.open_input(x, callback=InMSG)
    print("Input port changed to: " + x)


def changeoutputPort(x):
    global outputPort
    try:
        outputPort.close()
    except NameError:
        pass
    outputPort = mido.open_output(x)
    print("Output port changed to: " + x)

# SPARKLE

QT_APP = app
APPCAST_URL = 'https://s3.amazonaws.com/files.icaroferre.com/midirouter/appcast.xml'
SPARKLE_PATH = basedir + '/Frameworks/Sparkle.framework'

from objc import pathForFramework, loadBundle
sparkle_path = pathForFramework(SPARKLE_PATH)
print(sparkle_path)
objc_namespace = dict()
loadBundle('Sparkle', objc_namespace, bundle_path=sparkle_path)


def about_to_quit():
    # See https://github.com/sparkle-project/Sparkle/issues/839
    objc_namespace['NSApplication'].sharedApplication().terminate_(None)

app.aboutToQuit.connect(about_to_quit)
sparkle = objc_namespace['SUUpdater'].sharedUpdater()
sparkle.setAutomaticallyChecksForUpdates_(True)
sparkle.setAutomaticallyDownloadsUpdates_(False)
NSURL = objc_namespace['NSURL']
sparkle.setFeedURL_(NSURL.URLWithString_(APPCAST_URL))
sparkle.checkForUpdatesInBackground()

a_window = Window()

changeinputPort(available_input_ports[0])
changeoutputPort(available_output_ports[0])

sys.exit(app.exec_())
input("Hello")
