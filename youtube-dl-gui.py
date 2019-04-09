#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QProgressBar, QApplication, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import QProcess
import sys

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
                
    def initUI(self):
        
        vbox = QVBoxLayout(self)

        self.text = QLineEdit(self)
        self.text.setPlaceholderText("Video URL here")
        self.text.setText("https://www.youtube.com/watch?v=RqjNBI5pgFU")
        label = QLabel(self)
        label.setText("URL")
        button = QPushButton(self)
        button.setText("Download")
        button.clicked.connect(self.download)
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        
        vbox.addWidget(label)
        vbox.addWidget(self.text)
        vbox.addWidget(button)
        vbox.addWidget(self.progress)
        
        self.setLayout(vbox)
        self.resize(400, 120)
        self.show()
        
    def download(self):
        self.process = QProcess()
        self.process.readyRead.connect(self.analyze)
        self.process.finished.connect(self.finished)
        self.process.start("/usr/bin/youtube-dl", [self.text.text()])
        
    def finished(self, rc, status):
        if rc == 0:
            QMessageBox.information(self, "Completed", "Download finished")
            self.progress.setValue(0)
        
    def analyze(self):
        line = str(self.process.readLine())
        if "has already been downloaded" in line:
            self.progress.setValue(100)
        elif "[download]" in line and "Destination:" not in line:
            progress = float(line.split()[1][:-1])
            self.progress.setValue(int(progress))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
