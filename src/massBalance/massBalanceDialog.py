# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 08:16:14 2020

@author: spark
"""
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, Qt
from PySide2.QtWidgets import QDialog, QDialogButtonBox
from PySide2 import QtGui
from collections import defaultdict

class massBalanceDialog(QDialog):
    def __init__(self,fillData, editData=0, parent=None):
        super(massBalanceDialog,self).__init__(parent)
        ui_file = QFile('massBalance/massBalanceDataEntryDialog.ui')
        ui_file.open(QFile.ReadOnly)
        self.data = fillData
        self.widgetDict = defaultdict(list)
        self.editData = editData
        
        loader = QUiLoader()
        self.window = loader.load(ui_file) # self.window is ui
        
        self.tagName=["Process Parameters","Input","Output","MBC"]
        self.lineEditStartIndex = [2,0,0,0]
        
        self.createwidgets()
        self.fillDataToEntry()
        
        ui_file.close()
        
    def showWindow(self):
        #self.window.show()
        self.window.showMaximized() 
        
    def createwidgets(self):
         ####################### product systems #######################
        self.ps_productsystem_CB = self.window.comboBox_2
        self.ps_feedtype_CB = self.window.comboBox_3
        self.ps_feedsize_LE = self.window.lineEdit_21
        self.ps_feedamount_LE = self.window.lineEdit_22
        self.ps_temp_LE = self.window.lineEdit
        self.ps_residensetime_LE = self.window.lineEdit_2
        self.ps_heatingrate_LE = self.window.lineEdit_3      

        ######################## input output mbc #####################################
        self.in_biomass_LE = self.window.lineEdit_17
        self.in_inertgas_LE = self.window.lineEdit_18
        self.in_total_LE = self.window.lineEdit_19
        
        self.op_biochar_LE = self.window.lineEdit_20
        self.op_biooil_LE = self.window.lineEdit_23
        self.op_gas_LE = self.window.lineEdit_24
        self.op_total_LE = self.window.lineEdit_25
        
        self.mbc_LE = self.window.lineEdit_26
        # Buttons
        self.okButton = self.window.buttonBox.button(QDialogButtonBox.Ok)
        self.okCancel = self.window.buttonBox.button(QDialogButtonBox.Cancel)
        
        ######### energy auto fill##############      
        self.in_biomass_LE.editingFinished.connect(self.filliptotal)
        self.in_inertgas_LE.editingFinished.connect(self.filliptotal)
        
        self.op_biochar_LE.editingFinished.connect(self.filloptotal)
        self.op_biooil_LE.editingFinished.connect(self.filloptotal)
        self.op_gas_LE.editingFinished.connect(self.filloptotal)
        
        self.in_total_LE.textChanged.connect(self.fillmbc)
        self.op_total_LE.textChanged.connect(self.fillmbc)
        
        self.entryValidation()
        
    def entryValidation(self):
        self.lineEditValidator = QtGui.QDoubleValidator(self, 0,999999999,4)
        self.lineEditValidator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        
        self.ps_feedsize_LE.setValidator(self.lineEditValidator)
        self.ps_feedamount_LE.setValidator(self.lineEditValidator)
        self.ps_temp_LE.setValidator(self.lineEditValidator)               
        self.ps_residensetime_LE.setValidator(self.lineEditValidator)
        self.ps_heatingrate_LE.setValidator(self.lineEditValidator)
        
        self.in_biomass_LE.setValidator(self.lineEditValidator)
        self.in_inertgas_LE.setValidator(self.lineEditValidator)
        self.in_total_LE.setValidator(self.lineEditValidator)
        
        self.op_biochar_LE.setValidator(self.lineEditValidator)
        self.op_biooil_LE.setValidator(self.lineEditValidator)
        self.op_gas_LE.setValidator(self.lineEditValidator)
        self.op_total_LE.setValidator(self.lineEditValidator)
        
        self.mbc_LE.setValidator(self.lineEditValidator)
        
        
        ################## add to lineEdit List ######################
        self.widgetDict[self.tagName[0]].append(self.ps_productsystem_CB)
        self.widgetDict[self.tagName[0]].append(self.ps_feedtype_CB)
        self.widgetDict[self.tagName[0]].append(self.ps_feedsize_LE)
        self.widgetDict[self.tagName[0]].append(self.ps_feedamount_LE)
        self.widgetDict[self.tagName[0]].append(self.ps_temp_LE)
        self.widgetDict[self.tagName[0]].append(self.ps_residensetime_LE)
        self.widgetDict[self.tagName[0]].append(self.ps_heatingrate_LE)
        
        self.widgetDict[self.tagName[1]].append(self.in_biomass_LE)
        self.widgetDict[self.tagName[1]].append(self.in_inertgas_LE)
        self.widgetDict[self.tagName[1]].append(self.in_total_LE)
        
        self.widgetDict[self.tagName[2]].append(self.op_biochar_LE)
        self.widgetDict[self.tagName[2]].append(self.op_biooil_LE)
        self.widgetDict[self.tagName[2]].append(self.op_gas_LE)
        self.widgetDict[self.tagName[2]].append(self.op_total_LE)
        
        self.widgetDict[self.tagName[3]].append(self.mbc_LE)

        
    def filliptotal(self):
        biomass=0
        inertgas=0
        
        if(self.in_biomass_LE.text()!=""):
            biomass = float(self.in_biomass_LE.text())
        if(self.in_inertgas_LE.text()!=""):
            inertgas = float(self.in_inertgas_LE.text())
        
        netmass = biomass+inertgas
        self.in_total_LE.setText(str(netmass))
        
    def filloptotal(self):        
        biochar=0
        biooil=0
        gas=0
        
        if(self.op_biochar_LE.text()!=""):
            biochar = float(self.op_biochar_LE.text())
        if(self.op_biooil_LE.text()!=""):
            biooil = float(self.op_biooil_LE.text())
        if(self.op_gas_LE.text()!=""):
            gas = float(self.op_gas_LE.text())
        
        netmass = biochar+biooil+gas
        self.op_total_LE.setText(str(netmass))
        
    def fillmbc(self):        
        in_total=0
        op_total=0
        
        if(self.in_total_LE.text()!=""):
            in_total = float(self.in_total_LE.text())
        if(self.op_total_LE.text()!=""):
            op_total = float(self.op_total_LE.text())
        
        if(in_total !=0 and op_total !=0):
            netmbc = op_total/in_total
            self.mbc_LE.setText(str(netmbc))
         
    def fillDataToEntry(self):    
        if(self.editData==1):
            for i in range(len(self.tagName)):
                for j in range(self.lineEditStartIndex[i]):                
                    setIndex = self.widgetDict[self.tagName[i]][j].findText(self.data[self.tagName[i]][j],flags=Qt.MatchExactly)
                    self.widgetDict[self.tagName[i]][j].setCurrentIndex(setIndex)
                 
            for i in range(len(self.tagName)):
                for j in range(self.lineEditStartIndex[i], len(self.widgetDict[self.tagName[i]]), 1):
                    self.widgetDict[self.tagName[i]][j].setText(self.data[self.tagName[i]][j])
            
                
    def fetchData(self):
        for i in range(len(self.tagName)):
            for j in range(self.lineEditStartIndex[i]):
                self.data[self.tagName[i]][j] = self.widgetDict[self.tagName[i]][j].currentText()
                 
        for i in range(len(self.tagName)):
            for j in range(self.lineEditStartIndex[i], len(self.widgetDict[self.tagName[i]]), 1):
                self.data[self.tagName[i]][j] = self.widgetDict[self.tagName[i]][j].text()
