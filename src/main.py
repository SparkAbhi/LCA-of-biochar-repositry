# -*- coding: utf-8 -*-
"""
Created on Sun May 31 09:53:08 2020

@author: spark
For all pwd is /src folder only
"""
import sys
from PySide2.QtWidgets import QApplication

from PySide2.QtCore import QCoreApplication
from PySide2.QtCore import Qt
from start.start import startAppWindow
###########################################################
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
app = QApplication(sys.argv)

mywindow = startAppWindow()
mywindow.showWindow() 

sys.exit(app.exec_())



